#!/usr/bin/env python3
"""Daily, read-only portfolio discovery with optional idempotent Production-OS handoff.

The GitHub Actions token can scan public repositories but cannot write to
other repositories. Actual code integration is delegated to a qualified
Production-OS worker, never treated as completed by this script.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from recommend import DOMAIN_ALIASES, infer_domains, score_repo, tokens

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
ALLOWED_LICENSES = {
    "mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc",
    "mpl-2.0", "unlicense", "cc0-1.0", "0bsd",
}
KEYWORDS = {
    "game_dev": ("roblox", "luau", "godot", "game", "gaming", "unity", "jelly", "zombie", "jumpy"),
    "trading": ("trading", "quant", "backtest", "ftmo", "forex", "stock", "finance"),
    "mobile": ("android", "kotlin", "flutter", "mobile", "apk"),
    "ai_media": ("video", "audio", "voice", "tts", "xtts", "media", "artist", "music"),
    "cybersecurity": ("security", "bug bounty", "pentest", "xbow", "vulnerability"),
    "ai_agents": ("agent", "llm", "ai", "model", "autonomous", "automation"),
    "web_frontend": ("web", "frontend", "website", "react", "ui"),
    "backend": ("backend", "server", "api", "fastapi", "database"),
    "devops": ("production", "deploy", "infra", "ci", "repo", "workflow"),
    "productivity": ("promo", "discount", "deal", "price", "finder", "watch", "money"),
}
GENERIC = {"ai", "agent", "dev", "web", "python", "typescript", "app", "open", "tools", "github", "repo"}
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does",
    "each", "etc", "for", "from", "has", "have", "in", "into", "is",
    "it", "its", "not", "of", "on", "or", "our", "that", "the", "their",
    "these", "this", "to", "using", "via", "was", "we", "were", "what",
    "when", "where", "which", "while", "will", "with", "you", "your",
}
# Portfolio READMEs include French; shared prose must never be treated as
# evidence that a developer tool is genuinely compatible with an app.
STOPWORDS.update({
    "afin", "ainsi", "alors", "avec", "avoir", "aux", "autre", "autres",
    "car", "ce", "cela", "ces", "cette", "chez", "comme", "comment",
    "dans", "de", "des", "donc", "du", "elle", "elles", "en", "entre",
    "est", "et", "etre", "fait", "faire", "ici", "ils", "il", "je",
    "la", "le", "les", "leur", "leurs", "mais", "mes", "mon", "nos",
    "notre", "nous", "ou", "oui", "par", "pas", "peut", "peuvent",
    "plus", "pour", "quand", "que", "quel", "quelle", "quelles",
    "quels", "qui", "quoi", "sans", "ses", "se", "sont", "son",
    "sur", "tous", "tout", "toute", "toutes", "une", "un", "vous",
    "votre", "vos",
})


# Engine-specific runtime components are not drop-in replacements for
# incompatible engines. This is a hard gate, not a soft relevance penalty.
ENGINE_CONFLICTS = {
    "roblox": ("godotengine/", "godot", "unity", "unreal", "bevy", "defold"),
    "godot": ("roblox", "unity", "unreal", "bevy", "defold"),
}

MANIFESTS = ("pyproject.toml", "package.json", "requirements.txt", "Cargo.toml",
             "build.gradle.kts", "pubspec.yaml")


def request_json(url: str, token: str = "", *, method: str = "GET", data: dict | None = None):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("HTTPS endpoint required")
    headers = {
        "Accept": "application/vnd.github+json" if parsed.hostname == "api.github.com" else "application/json",
        "User-Agent": "star-list-portfolio-daily/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers, method=method, data=body), timeout=25) as response:
                raw = response.read(3_000_000)
                return json.loads(raw)
        except HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {exc.code} for {parsed.path}") from exc
        except (URLError, TimeoutError) as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error for {parsed.path}: {type(exc).__name__}") from exc
    raise RuntimeError("request retry budget exhausted")


def github_repos(owner: str, token: str, portfolio_token: str) -> list[dict]:
    base = (API + "/user/repos?affiliation=owner&sort=full_name&per_page=100"
            if portfolio_token else
            API + "/users/" + quote(owner, safe="") + "/repos?type=owner&sort=full_name&per_page=100")
    result = []
    for page in range(1, 51):
        separator = "&" if "?" in base else "?"
        rows = request_json(base + separator + "page=" + str(page), portfolio_token or token)
        if not isinstance(rows, list):
            raise RuntimeError("Cannot enumerate owner repositories")
        result.extend(r for r in rows if r.get("owner", {}).get("login", "").lower() == owner.lower())
        if len(rows) < 100:
            break
    else:
        raise RuntimeError("Repository pagination safety limit reached")
    if not result:
        raise RuntimeError("No accessible repositories returned; refusing an empty success")
    return sorted({r["full_name"].lower(): r for r in result}.values(), key=lambda r: r["full_name"].lower())


def file_text(full_name: str, path: str, token: str, *, limit: int = 5500) -> str:
    endpoint = API + "/repos/" + "/".join(quote(part, safe="") for part in full_name.split("/")) + "/contents/" + quote(path, safe="")
    payload = request_json(endpoint, token)
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        return ""
    if int(payload.get("size") or 0) > 200_000:
        return ""
    raw = base64.b64decode(payload.get("content", ""), validate=False)
    return raw.decode("utf-8", errors="replace")[:limit]


def project_profile(repo: dict, token: str) -> dict:
    name = repo["full_name"]
    description = str(repo.get("description") or "")
    topics = repo.get("topics") or []
    intro = file_text(name, "README.md", token, limit=2800)
    dependency_text = ""
    for filename in MANIFESTS:
        value = file_text(name, filename, token, limit=3500)
        if value:
            dependency_text += "\n" + value
            break
    overview = " ".join([repo["name"], description, " ".join(topics), intro[:1200]])
    label_text = " ".join([repo["name"], description, " ".join(topics)]).lower()
    domains = set(infer_domains(tokens(label_text)))
    for domain, words in KEYWORDS.items():
        if any(re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", label_text) for word in words):
            domains.add(domain)
    # README may refine a known project, but never invent a domain solely from README.
    return {"domains": sorted(domains), "terms": tokens(overview), "dependencies": dependency_text.lower(),
            "overview": overview[:900], "language": str(repo.get("language") or "").lower()}


def eligible(item: dict) -> bool:
    gh = item.get("github") or {}
    if (item.get("tier") not in {"core", "recommended", "specialized"}
            or item.get("lifecycle") in {"legacy", "reference"}
            or gh.get("archived") or gh.get("disabled")):
        return False
    if (item.get("costModel") not in (None, "open-source")
            or item.get("integrationComplexity") == "high"
            or float(item.get("score") or 0) < 8):
        return False
    license_key = str(gh.get("license") or "").strip().lower()
    return license_key in ALLOWED_LICENSES


def is_reference_candidate(tool: dict) -> bool:
    """Keep example applications and architecture guides out of auto-implementation."""
    guidance = " ".join(str(v).lower() for v in (tool.get("bestFor") or []))
    reference_clues = (
        "architecture reference", "reference app", "reference application",
        "reference project", "example application", "sample application",
        "tutorial project", "reference app structure",
    )
    return any(clue in guidance for clue in reference_clues)


def recommendations(repo: dict, profile: dict, catalog: list[dict], count: int) -> list[dict]:
    name = repo["full_name"].lower()
    domains = set(profile["domains"])
    if not domains:
        return []
    matches = []
    for tool in catalog:
        slug = str(tool.get("repo") or "")
        if slug.lower() == name or not eligible(tool):
            continue
        if tool.get("domain") not in domains:
            continue
        terms = (tokens(slug) | tokens(" ".join(tool.get("capabilities") or []))
                 | tokens(" ".join(tool.get("bestFor") or [])))
        shared = sorted((profile["terms"] & terms) - GENERIC - STOPWORDS)
        if not shared:
            continue
        # A lone match must describe an actual candidate capability/use case,
        # not merely an organization name (or an incidental README word).
        capability_terms = (tokens(" ".join(tool.get("capabilities") or []))
                            | tokens(" ".join(tool.get("bestFor") or []))) - GENERIC - STOPWORDS
        if len(shared) < 2 and not (set(shared) & capability_terms):
            continue
        target_identity = repo["name"].lower()
        if profile["language"] == "luau" or "roblox" in target_identity:
            if any(marker in slug.lower() for marker in ENGINE_CONFLICTS["roblox"]):
                continue
        if profile["language"] == "gdscript" or "godot" in target_identity:
            if any(marker in slug.lower() for marker in ENGINE_CONFLICTS["godot"]):
                continue
        slug_name = slug.rsplit("/", 1)[-1].lower()
        if slug_name in profile["dependencies"] or slug_name in profile["overview"].lower():
            continue
        candidate_languages = set(str(x).lower() for x in (tool.get("languages") or []))
        # Missing language metadata is unknown compatibility, not native support.
        languages_match = bool(profile["language"]) and profile["language"] in candidate_languages
        score = score_repo(tool, profile["terms"], domains, set(), set())
        if score is None or score < 35:
            continue
        # A language mismatch is reviewable as a service/CLI integration, never a direct dependency.
        matches.append({"repository": slug, "score": round(score, 2),
                        "quality": tool["score"], "domain": tool["domain"],
                        "shared_terms": shared[:5],
                        "mode": ("reference-review" if is_reference_candidate(tool)
                                 else "native" if languages_match else "adapter-review"),
                        "license": tool.get("github", {}).get("license"),
                        "url": "https://github.com/" + slug})
    # A native library gets precedence over example applications and adapters.
    # Otherwise a reference app can fill the three slots before a usable SDK.
    priority = {"native": 0, "adapter-review": 1, "reference-review": 2}
    matches.sort(key=lambda r: (priority.get(r["mode"], 3),
                                -r["score"], -r["quality"], r["repository"].lower()))
    return matches[:count]


INTEGRATION_TOKEN_BUDGET = 90000


def count_active_integrations(projects: list[dict]) -> int:
    """Only in-flight portfolio jobs occupy coding-worker capacity slots."""
    return sum(
        1 for row in projects
        if "starlist-integration-v" in str(row.get("final_goal") or "")
        and str(row.get("status") or "").upper().replace("-", "_")
            in {"ACTIVE", "QUEUED", "RUNNING"}
    )


def count_failed_v2_integrations(projects: list[dict]) -> int:
    """Protect the free worker quota until failed high-budget jobs are reviewed."""
    return sum(
        1 for row in projects
        if "starlist-integration-v2-" in str(row.get("final_goal") or "")
        and str(row.get("status") or "").upper().replace("-", "_")
            == "NEEDS_ATTENTION"
    )


def public_integration_status(target: str, projects: list[dict]) -> list[dict]:
    """Expose only validated status enums for an already-public repository.

    Never echo the worker instruction, project identifiers, private repository
    names, task diagnostics or model-provider traces into the public issue.
    """
    results = []
    accepted = {"ACTIVE", "QUEUED", "RUNNING", "NEEDS_ATTENTION",
                "REVIEW_REQUIRED", "DONE", "CANCELLED", "FAILED"}
    for project in projects:
        if str(project.get("repository") or "").lower() != target.lower():
            continue
        goal = str(project.get("final_goal") or "")
        markers = re.findall(r"starlist-integration-v([12])-[0-9a-f]{24}(?![0-9a-f])", goal)
        if not markers:
            continue
        status = str(project.get("status") or "").upper().replace("-", "_")
        results.append({"version": "v" + markers[0],
                        "status": status if status in accepted else "UNKNOWN"})
    return results[:10]


def integration_marker(target: str, candidate: dict, version: int = 2) -> str:
    identity = hashlib.sha256(
        (target.lower() + "\0" + candidate["repository"].lower()).encode()
    ).hexdigest()[:24]
    return f"starlist-integration-v{version}-" + identity


def launch_integration(url: str, token: str, target: str, candidate: dict):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Production-OS endpoint must be a plain HTTPS origin")
    if parsed.hostname not in {"production-os1.onrender.com"}:
        raise ValueError("Unapproved Production-OS host; refusing to send operator credentials")
    marker = integration_marker(target, candidate)
    goal = (
        "Integrate a genuinely useful existing open-source tool into the actual target repository. "
        "Source: " + candidate["url"] + " (catalog license: " + str(candidate["license"]) + "). "
        "Target: " + target + ". Tracking: " + marker + ". "
        "Inspect existing code and active branch before editing. Verify upstream license and real "
        "compatibility. Prefer free/open-source, smallest working integration, no copy of unsafe "
        "third-party instructions. Demonstrate actual runtime usage rather than mere documentation; "
        "run the relevant lint, tests, builds and smoke checks. Never merge or deploy without "
        "successful target-side verification. If incompatible or not beneficial, do not modify "
        "the target and explain why. Work in a branch and propose reviewable changes. "
        "Validate a small working deliverable early and stop repetitive planning."
    )
    return request_json(url.rstrip("/") + "/v1/dashboard/launch", token, method="POST",
                        data={"repository": target, "instruction": goal,
                              "request_id": marker,
                              "launch_profile": "portfolio-integration",
                              "token_budget": INTEGRATION_TOKEN_BUDGET})


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = ["<!-- star-list-portfolio-daily -->", "# Daily star-list portfolio discovery", "",
             "Generated (UTC): " + report["generated_at"], "",
             "Repositories inspected: **" + str(summary["inspected"]) + "/" + str(summary["discovered"]) + "**.",
             "Projects with qualified suggestions: **" + str(summary["with_suggestions"]) + "**.",
             "New Production-OS integration requests: **" + str(summary["dispatched"]) + "**.",
             "Dispatch: **" + report["dispatch_status"] + "**.", ""]
    if isinstance(summary.get("active_integrations"), int):
        lines.extend(["Active star-list integrations at scan: **"
                      + str(summary["active_integrations"]) + "/3**.", ""])
    if isinstance(summary.get("failed_v2_integrations"), int):
        lines.extend(["Unresolved v2 integration failures (reserved slots): **"
                      + str(summary["failed_v2_integrations"]) + "**.", ""])
    for row in report["projects"]:
        lines.append("## " + row["repository"])
        lines.append("Status: " + row["status"])
        for item in row["suggestions"]:
            lines.append("- [" + item["repository"] + "](" + item["url"] + ")"
                         + " — fit " + str(item["score"]) + ", " + item["mode"]
                         + ", license " + str(item["license"])
                         + ", overlap: " + ", ".join(item["shared_terms"]))
        for item in row.get("dispatches", []):
            lines.append("- Integration queue: " + item)
        for item in row.get("integrations", []):
            lines.append("- Tracked work: " + item["version"] + " " + item["status"])
        lines.append("")
    if report["errors"]:
        lines.extend(["## Errors", ""])
        lines.extend("- " + error for error in report["errors"])
    lines.extend(["", "Only qualified licensed matches can be sent to Production-OS. "
                  "A queued request is not a completed integration: runtime checks "
                  "and a real validated code change are mandatory."])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default="dbrckk")
    ap.add_argument("--repository", default="", help="Inspect one target, including a private repo with its own token")
    ap.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    ap.add_argument("--output", type=Path, default=Path("portfolio-daily.json"))
    ap.add_argument("--markdown", type=Path, default=Path("portfolio-daily.md"))
    ap.add_argument("--max-dispatch", type=int, default=3)
    args = ap.parse_args()
    if args.max_dispatch < 0 or args.max_dispatch > 10:
        ap.error("--max-dispatch must be between 0 and 10")
    gh_token = os.getenv("GITHUB_TOKEN", "")
    portfolio_token = os.getenv("PORTFOLIO_GITHUB_TOKEN", "")
    operator_token = os.getenv("PRODUCTION_OS_OPERATOR_TOKEN", "")
    service = os.getenv("PRODUCTION_OS_URL", "https://production-os1.onrender.com")
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "owner": args.owner,
              "dispatch_status": "enabled" if operator_token else "disabled (missing PRODUCTION_OS_OPERATOR_TOKEN)",
              "projects": [], "errors": [], "summary": {}}
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))["repositories"]
        if args.repository:
            if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository):
                raise ValueError("Invalid target repository")
            if args.repository.split("/")[0].lower() != args.owner.lower():
                raise ValueError("Target is not owned by requested account")
            target = request_json(API + "/repos/" + args.repository, portfolio_token or gh_token)
            if not isinstance(target, dict) or target.get("full_name", "").lower() != args.repository.lower():
                raise RuntimeError("Target repository is not accessible")
            source = [target]
        else:
            source = github_repos(args.owner, gh_token, portfolio_token)
            # The central issue is public: never publish private target metadata there.
            source = [repo for repo in source if not repo.get("private")]
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
        report["errors"].append("Cannot initialize scan: " + str(exc))
        source, catalog = [], []
    for repo in source:
        target = repo["full_name"]
        row = {"repository": target, "status": "scanned", "suggestions": [], "dispatches": []}
        try:
            if repo.get("archived") or repo.get("disabled"):
                row["status"] = "skipped-inactive"
            else:
                profile = project_profile(repo, portfolio_token or gh_token)
                row["suggestions"] = recommendations(repo, profile, catalog, 3)
                row["status"] = "qualified-candidates" if row["suggestions"] else "no-qualified-candidate"
        except (RuntimeError, ValueError, TypeError, KeyError) as exc:
            row["status"] = "scan-failed"
            report["errors"].append(target + ": " + str(exc))
        report["projects"].append(row)
    dispatched = 0
    active_integrations = None
    failed_v2_integrations = None
    if operator_token:
        # Validate the origin before even the read-only authenticated request.
        parsed_service = urlparse(service)
        if (parsed_service.scheme != "https"
                or parsed_service.hostname != "production-os1.onrender.com"
                or parsed_service.username or parsed_service.password
                or parsed_service.query or parsed_service.fragment):
            report["errors"].append("Production-OS URL rejected: unapproved operator-token destination")
            operator_token = ""
    if operator_token:
        # Always prioritize highest-confidence matches, irrespective of repository order.
        queue = sorted(((item["score"], row, item) for row in report["projects"]
                        for item in row["suggestions"] if item["mode"] == "native"),
                        key=lambda p: (-p[0], p[1]["repository"]))
        try:
            existing = request_json(service.rstrip("/") + "/v1/managed-projects", operator_token)
            already = [p for p in (existing or {}).get("projects", []) if isinstance(p, dict)]
        except (RuntimeError, ValueError, TypeError) as exc:
            existing = None
            report["errors"].append("Cannot inspect existing managed projects: " + str(exc))
        if existing is not None:
            # Public issue rows originate only from public GitHub discovery.
            # Never include private managed-project names or instruction text.
            for public_row in report["projects"]:
                public_row["integrations"] = public_integration_status(
                    public_row["repository"], already
                )
            # Limit active portfolio work across multiple scheduled/manual runs,
            # not merely the number of launches in this one workflow run.
            active_integrations = count_active_integrations(already)
            failed_v2_integrations = count_failed_v2_integrations(already)
            # A v2 failure still occupies one admission slot. Continue
            # scanning daily, but do not spend unlimited tokens on new
            # projects while the free coding worker has unresolved failures.
            available_slots = min(
                args.max_dispatch,
                max(0, 3 - active_integrations - failed_v2_integrations),
            )
            for _, row, item in queue:
                marker = integration_marker(row["repository"], item)
                previous = integration_marker(row["repository"], item, version=1)
                if any(marker in str(p.get("final_goal") or "") for p in already):
                    row["dispatches"].append("existing-v2: " + item["repository"])
                    continue
                old = next(
                    (p for p in already if previous in str(p.get("final_goal") or "")),
                    None,
                )
                # Do not duplicate active/reviewable jobs. Allow exactly one
                # idempotent higher-budget restart when a v1 job has failed.
                is_recovery = False
                if old is not None:
                    status = str(old.get("status") or "").upper().replace("-", "_")
                    if status != "NEEDS_ATTENTION":
                        row["dispatches"].append("existing-v1: " + item["repository"])
                        continue
                    is_recovery = True
                if dispatched >= available_slots:
                    break
                try:
                    result = launch_integration(service, operator_token, row["repository"], item)
                    if not isinstance(result, dict) or not isinstance(result.get("project"), dict):
                        raise RuntimeError("Production-OS did not confirm a managed project")
                    row["dispatches"].append(
                        ("recovery-v2: " if is_recovery else "submitted-v2: ") + item["repository"]
                    )
                    already.append({"final_goal": marker, "status": "ACTIVE"})
                    dispatched += 1
                except (RuntimeError, ValueError, TypeError) as exc:
                    report["errors"].append(row["repository"] + " dispatch: " + str(exc))
    report["summary"] = {
        "discovered": len(source), "inspected": sum(p["status"] != "scan-failed" for p in report["projects"]),
        "with_suggestions": sum(bool(p["suggestions"]) for p in report["projects"]),
        "dispatched": dispatched, "active_integrations": active_integrations,
        "failed_v2_integrations": failed_v2_integrations,
        "failures": len(report["errors"]),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], sort_keys=True))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
