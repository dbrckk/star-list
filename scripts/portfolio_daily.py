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
from urllib.request import HTTPRedirectHandler, Request, build_opener

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
# A repository *using* an engine should not be told to integrate that engine's
# complete source tree as if it were a missing application dependency.
EXISTING_ENGINE_SOURCES = {
    "godot": frozenset({"godotengine/godot"}),
}

MANIFESTS = ("pyproject.toml", "package.json", "requirements.txt", "Cargo.toml",
             "build.gradle.kts", "pubspec.yaml")


class SameOriginRedirect(HTTPRedirectHandler):
    """Never forward GitHub or Production-OS bearer tokens to another origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        original = urlparse(req.full_url)
        destination = urlparse(newurl)
        if (destination.scheme != "https"
                or destination.hostname != original.hostname
                or destination.port != original.port
                or destination.username or destination.password):
            raise RuntimeError("Refusing cross-origin redirect of authenticated API request")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


SAFE_HTTP = build_opener(SameOriginRedirect())


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
            # Render free instances may need time to wake up. Restrict the
            # extended timeout to the approved control-plane host; keep
            # ordinary GitHub catalog lookups bounded at 25 seconds.
            request_timeout = 60 if parsed.hostname == "production-os1.onrender.com" else 25
            with SAFE_HTTP.open(Request(url, headers=headers, method=method, data=body),
                                timeout=request_timeout) as response:
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
    """Keep demos, samples and architecture guides out of auto-implementation."""
    guidance = " ".join(str(v).lower() for v in (tool.get("bestFor") or []))
    capabilities = set(str(v).strip().lower() for v in (tool.get("capabilities") or []))
    slug = str(tool.get("repo") or "").lower()
    reference_clues = (
        "architecture reference", "reference app", "reference application",
        "reference project", "example application", "sample application",
        "tutorial project", "reference app structure", "étudier des exemples",
        "study examples", "reproducible examples",
    )
    return (
        any(clue in guidance for clue in reference_clues)
        or bool(capabilities & {"example", "examples", "demo", "demos", "samples"})
        or bool(re.search(r"(?:^|[-_/])(?:demo|demos|examples|samples)(?:[-_/]|$)", slug))
    )


# Generic README prose is not proof that a package provides an actionable
# capability. Such matches may stay in the review report, but cannot trigger
# an autonomous dependency integration solely because languages match.
WEAK_CAPABILITY_TERMS = {
    "workflow", "workflows", "tool", "tools", "data", "general",
    "example", "examples", "demo", "demos", "project", "projects",
}


def recommendations(repo: dict, profile: dict, catalog: list[dict], count: int) -> list[dict]:
    name = repo["full_name"].lower()
    domains = set(profile["domains"])
    if not domains:
        return []
    target_identity = repo["name"].lower()
    godot_target = profile["language"] == "gdscript" or "godot" in target_identity
    existing_engine_sources = set(EXISTING_ENGINE_SOURCES["godot"]) if godot_target else set()
    # Engine alternatives are replacement *platforms*, not dependencies.
    # Derive them from the catalog's own explicit alternative relationships,
    # rather than chasing individual incompatible engine names by hand.
    excluded_engine_sources = existing_engine_sources | {
        alternative.lower()
        for engine in catalog
        if str(engine.get("repo") or "").lower() in existing_engine_sources
        for alternative in (engine.get("alternatives") or [])
        if isinstance(alternative, str)
    }
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
        if slug.lower() in excluded_engine_sources:
            # Ignore the installed engine source and explicit substitute
            # engines. Continue recommending compatible plugins/addons.
            continue
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
        # An incidental word such as "workflows" from a README must not
        # qualify an otherwise unrelated same-language library for dispatch.
        concrete_terms = (
            tokens(" ".join(tool.get("capabilities") or []))
            - GENERIC - STOPWORDS - WEAK_CAPABILITY_TERMS
        )
        capability_overlap = bool(set(shared) & concrete_terms)
        # An MCP control bridge runs alongside Roblox Studio. Its Lua/Luau
        # plugin is not a library embedded in the published game: external
        # Studio access, an MCP client and a development host are required.
        # Do not spend autonomous runtime-integration budget on this match.
        capabilities = {str(v).strip().lower() for v in (tool.get("capabilities") or [])}
        external_studio_bridge = (
            "mcp" in capabilities and "roblox" in capabilities
            and ("roblox" in target_identity or profile["language"] in {"lua", "luau"})
        )
        # A language mismatch remains adapter-review; same-language tools
        # with only prose overlap remain discoverable but require review.
        mode = (
            "reference-review" if is_reference_candidate(tool) else
            "adapter-review" if external_studio_bridge or not languages_match else
            "native" if capability_overlap else "capability-review"
        )
        matches.append({"repository": slug, "score": round(score, 2),
                        "quality": tool["score"], "domain": tool["domain"],
                        "shared_terms": shared[:5],
                        "mode": mode,
                        "license": tool.get("github", {}).get("license"),
                        "url": "https://github.com/" + slug})
    # A native library gets precedence over example applications and adapters.
    # Otherwise a reference app can fill the three slots before a usable SDK.
    priority = {"native": 0, "capability-review": 1,
                "adapter-review": 2, "reference-review": 3}
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


def busy_integration_targets(projects: list[dict]) -> set[str]:
    """Do not launch concurrent or review-conflicting changes into one repo.

    Unlike the fleet's worker cap, REVIEW_REQUIRED also blocks the target:
    that result may still have a branch/PR awaiting review. DONE and failed
    attempts are handled independently by versioned tracking/quarantine.
    """
    return {
        str(row["repository"]).lower()
        for row in projects
        if re.search(
            r"starlist-integration-v[123]-[0-9a-f]{24}(?![0-9a-f])",
            str(row.get("final_goal") or ""),
        )
        and str(row.get("status") or "").upper().replace("-", "_")
            in {"ACTIVE", "REVIEW_REQUIRED", "QUEUED", "RUNNING"}
        and isinstance(row.get("repository"), str)
    }


def unresolved_failed_v2_integrations(projects: list[dict]) -> list[dict]:
    """Failed v2 jobs still needing review after any successful v3 recovery.

    The v2 record itself remains NEEDS_ATTENTION forever: a later completed
    v3 recovery for the same exact candidate supersedes it for admission and
    reporting. Other failed candidate identities remain quarantined.
    """
    recovered = set()
    for row in projects:
        if str(row.get("status") or "").upper().replace("-", "_") != "DONE":
            continue
        marker = re.search(
            r"starlist-integration-v3-([0-9a-f]{24})(?![0-9a-f])",
            str(row.get("final_goal") or ""),
        )
        if marker:
            recovered.add(marker.group(1))

    unresolved = []
    for row in projects:
        if str(row.get("status") or "").upper().replace("-", "_") != "NEEDS_ATTENTION":
            continue
        marker = re.search(
            r"starlist-integration-v2-([0-9a-f]{24})(?![0-9a-f])",
            str(row.get("final_goal") or ""),
        )
        if marker and marker.group(1) not in recovered:
            unresolved.append(row)
    return unresolved


def count_failed_v2_integrations(projects: list[dict]) -> int:
    """Count only still-unresolved failed high-budget jobs."""
    return len(unresolved_failed_v2_integrations(projects))


def count_launches_on_utc_date(projects: list[dict], utc_day: str) -> int:
    """Account for the UTC launch quota, regardless of an API timestamp offset.

    Call only after verified_managed_projects has validated timezone-aware
    timestamps. A local-calendar comparison can admit extra launches around
    midnight even when the per-UTC-day safety quota is already exhausted.
    """
    return sum(
        1 for project in projects
        if re.search(
            r"starlist-integration-v[23]-[0-9a-f]{24}",
            project["final_goal"],
        )
        and datetime.fromisoformat(
            project["created_at"].replace("Z", "+00:00")
        ).astimezone(timezone.utc).date().isoformat() == utc_day
    )



def verified_managed_projects(payload: object) -> list[dict]:
    """Fail closed unless the inventory can safely authorize more launches.

    Production-OS returns *every* star-list tracking record, with a known
    lifecycle state and timestamp. An unknown state must not be interpreted
    as idle capacity; a duplicate marker or missing timestamp must not make
    retries look safe.
    """
    if not isinstance(payload, dict):
        raise RuntimeError("Production-OS managed-project inventory is unavailable")
    projects = payload.get("projects")
    if not isinstance(projects, list) or any(not isinstance(p, dict) for p in projects):
        raise RuntimeError("Production-OS managed-project inventory has invalid projects")
    if (payload.get("complete") is not True
            or type(payload.get("total_count")) is not int
            or payload["total_count"] != len(projects)):
        raise RuntimeError("Production-OS integration inventory is incomplete")

    known_states = {"ACTIVE", "REVIEW_REQUIRED", "NEEDS_ATTENTION", "DONE"}
    seen_markers: set[str] = set()
    for project in projects:
        goal = project.get("final_goal")
        marker = re.search(
            r"(?<![a-z0-9])starlist-integration-v[123]-[0-9a-f]{24}(?![0-9a-f])",
            goal if isinstance(goal, str) else "",
        )
        if marker is None or marker.group(0) in seen_markers:
            raise RuntimeError("Production-OS integration inventory has invalid or duplicate tracking")
        seen_markers.add(marker.group(0))

        repo = project.get("repository")
        if not isinstance(repo, str) or not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo
        ):
            raise RuntimeError("Production-OS inventory has an invalid tracked repository")
        status = project.get("status")
        if not isinstance(status, str) or status not in known_states:
            raise RuntimeError("Production-OS inventory has an unknown integration state")

        timestamp = project.get("created_at")
        if not isinstance(timestamp, str) or not timestamp.strip():
            raise RuntimeError("Production-OS inventory has a missing integration timestamp")
        try:
            created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if created.tzinfo is None:
                raise ValueError("timezone missing")
        except ValueError as exc:
            raise RuntimeError("Production-OS inventory has an invalid integration timestamp") from exc
    return projects


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
        markers = re.findall(r"starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])", goal)
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


def recoverable_failure_targets(
    failures: list[dict], projects: list[dict], inventory: list[dict],
) -> set[str]:
    """Quarantine only targets with an *eligible* v3 retry still available.

    A previous candidate may later be rejected as a reference application,
    incompatible capability or low-value match. Keep the failed v2 record
    visible, but do not permanently block an unrelated qualified native tool.
    Existing v3 records (any status) are non-retryable.
    """
    available: dict[str, set[str]] = {}
    for project in projects:
        target = str(project.get("repository") or "").lower()
        for candidate in project.get("suggestions") or []:
            if isinstance(candidate, dict) and candidate.get("mode") == "native":
                available.setdefault(target, set()).add(
                    integration_marker(target, candidate)
                )

    return {
        str(failure["repository"]).lower()
        for failure in failures
        if isinstance(failure.get("repository"), str)
        and str(failure["repository"]).lower() in available
        and any(
            marker in str(failure.get("final_goal") or "")
            and not any(
                marker.replace("starlist-integration-v2-", "starlist-integration-v3-")
                in str(previous.get("final_goal") or "")
                for previous in inventory
            )
            for marker in available[str(failure["repository"]).lower()]
        )
    }


def launch_integration(url: str, token: str, target: str, candidate: dict, *, version: int = 2):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Production-OS endpoint must be a plain HTTPS origin")
    if parsed.hostname not in {"production-os1.onrender.com"}:
        raise ValueError("Unapproved Production-OS host; refusing to send operator credentials")
    if version not in (2, 3):
        raise ValueError("unsupported integration tracking version")
    marker = integration_marker(target, candidate, version=version)
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


def confirmed_launch(result: object, target: str, candidate: dict, *, version: int = 2) -> bool:
    """Accept only a bound, persistent, idempotent Production-OS receipt.

    An HTTP success containing {"project": {}} is not proof of the requested
    launch. Wrong-target acknowledgements must not consume a fleet slot or
    permit the dispatcher to submit more work under an inconsistent inventory.
    """
    if not isinstance(result, dict):
        return False
    project, launch = result.get("project"), result.get("launch")
    if not isinstance(project, dict) or not isinstance(launch, dict):
        return False
    identifier = project.get("id")
    if not isinstance(identifier, str) or not re.fullmatch(r"[0-9a-f]{32}", identifier):
        return False
    marker = integration_marker(target, candidate, version=version)
    goal = project.get("final_goal")
    return (
        project.get("project_id") == identifier
        and isinstance(project.get("repository"), str)
        and project["repository"].lower() == target.lower()
        and isinstance(goal, str)
        and "Tracking: " + marker in goal
        and project.get("token_budget") == INTEGRATION_TOKEN_BUDGET
        and type(project.get("token_budget")) is int
        and launch.get("mode") == "managed-project"
        and launch.get("persistent") is True
        and launch.get("request_id") == marker
        and launch.get("idempotent") is True
        and type(launch.get("token_budget")) is int
        and launch.get("token_budget") == INTEGRATION_TOKEN_BUDGET
    )


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = ["<!-- star-list-portfolio-daily -->", "# Daily star-list portfolio discovery", "",
             "Generated (UTC): " + report["generated_at"], "",
             "Repositories inspected: **" + str(summary["inspected"]) + "/" + str(summary["discovered"]) + "**.",
             "Projects with reviewable suggestions: **" + str(summary["with_suggestions"]) + "**.",
             "Projects with native-mode candidates: **" + str(summary["with_native_suggestions"]) + "**.",
             "Native-mode candidates: **" + str(summary["native_suggestions"]) + "**.",
             "New Production-OS integration requests: **" + str(summary["dispatched"]) + "**.",
             "Dispatch: **" + report["dispatch_status"] + "**.", ""]
    if isinstance(summary.get("active_integrations"), int):
        lines.extend(["Active star-list integrations at scan: **"
                      + str(summary["active_integrations"]) + "/3**.", ""])
    if isinstance(summary.get("failed_v2_integrations"), int):
        lines.extend(["Unresolved earlier v2 integration failures: **"
                      + str(summary["failed_v2_integrations"]) + "**.", ""])
    if isinstance(summary.get("available_dispatch_slots"), int):
        lines.extend(["Available launch slots for this scan: **"
                      + str(summary["available_dispatch_slots"]) + "**.", ""])
    if isinstance(summary.get("launches_today_utc"), int):
        lines.extend(["Previously launched v2/v3 tasks today (UTC): **"
                      + str(summary["launches_today_utc"]) + "**.", ""])
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
    lines.extend(["", "Native-mode means a preliminary language/capability match, "
                  "not verified installability. Review-only suggestions cannot be "
                  "dispatched automatically. A queued request is not a completed "
                  "integration: runtime checks and a real validated code change "
                  "are mandatory."])
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
    # Discovery must be complete before starting any potentially mutating
    # managed project. A per-repository read error is not a partial success.
    scan_complete = not report["errors"]
    if not scan_complete and operator_token:
        report["dispatch_status"] = "blocked (incomplete repository scan)"
    dispatched = 0
    # A lost response does not prove a POST was rejected. Stop sending other
    # candidates until the next run reconciles a fresh managed-project inventory.
    launch_outcome_uncertain = False
    active_integrations = None
    failed_v2_integrations = None
    available_slots = None
    launches_today = None
    if operator_token:
        # Validate the origin before even the read-only authenticated request.
        parsed_service = urlparse(service)
        if (parsed_service.scheme != "https"
                or parsed_service.hostname != "production-os1.onrender.com"
                or parsed_service.username or parsed_service.password
                or parsed_service.query or parsed_service.fragment):
            report["errors"].append("Production-OS URL rejected: unapproved operator-token destination")
            report["dispatch_status"] = "blocked (unapproved Production-OS URL)"
            operator_token = ""
    if operator_token and scan_complete and not report["errors"]:
        # Always prioritize highest-confidence matches, irrespective of repository order.
        queue = sorted(((item["score"], row, item) for row in report["projects"]
                        for item in row["suggestions"] if item["mode"] == "native"),
                        key=lambda p: (-p[0], p[1]["repository"]))
        try:
            existing = request_json(service.rstrip("/") + "/v1/managed-projects/integration-inventory", operator_token)
            already = verified_managed_projects(existing)
        except (RuntimeError, ValueError, TypeError) as exc:
            existing = None
            report["errors"].append("Cannot inspect existing managed projects: " + str(exc))
            report["dispatch_status"] = "blocked (Production-OS inventory unavailable)"
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
            busy_targets = busy_integration_targets(already)
            # Failed projects are quarantined instead of occupying all
            # capacity slots forever. While failures remain, admit at most
            # ONE distinct project per UTC day and only with an idle portfolio
            # worker. This avoids both deadlock and unlimited paid/free-token
            # retries from scans triggered repeatedly by GitHub events.
            unresolved_failures = unresolved_failed_v2_integrations(already)
            failed_targets = recoverable_failure_targets(
                unresolved_failures, report["projects"], already
            )
            # Historical failures for candidates now disqualified remain
            # counted and reported; they cannot hold a target hostage forever.
            # The global one-launch-per-day cap still applies whenever a
            # historical v2 failure remains unresolved.
            if failed_v2_integrations:
                current_day = report["generated_at"][:10]
                launches_today = count_launches_on_utc_date(already, current_day)
                available_slots = (
                    min(args.max_dispatch, max(0, 1 - launches_today))
                    if active_integrations == 0 else 0
                )
            else:
                available_slots = min(
                    args.max_dispatch,
                    max(0, 3 - active_integrations),
                )
            # Reevaluate a previously failed compatible candidate before
            # consuming the single daily slot on an unrelated new project.
            # A v3 marker is distinct and can be submitted only once.
            if failed_targets:
                queue.sort(key=lambda entry: (
                    not any(
                        integration_marker(entry[1]["repository"], entry[2])
                        in str(p.get("final_goal") or "")
                        and str(p.get("status") or "").upper().replace("-", "_")
                            == "NEEDS_ATTENTION"
                        for p in unresolved_failures
                    ),
                    -entry[0], entry[1]["repository"],
                ))
            for _, row, item in queue:
                # Existing work and earlier successful dispatches in this same
                # run must not modify one target repository concurrently.
                if row["repository"].lower() in busy_targets:
                    row["dispatches"].append("deferred: target integration active or awaiting review")
                    continue
                if row["repository"].lower() in failed_targets:
                    failed_marker = integration_marker(row["repository"], item)
                    recovery_marker = integration_marker(row["repository"], item, version=3)
                    matching_failure = any(
                        failed_marker in str(p.get("final_goal") or "")
                        and str(p.get("status") or "").upper().replace("-", "_")
                            == "NEEDS_ATTENTION"
                        for p in unresolved_failures
                    )
                    if not matching_failure:
                        row["dispatches"].append(
                            "quarantined-v2: other prior candidate needs review"
                        )
                        continue
                    if any(
                        recovery_marker in str(p.get("final_goal") or "")
                        for p in already
                    ):
                        row["dispatches"].append("existing-v3: " + item["repository"])
                        continue
                    if dispatched >= available_slots:
                        break
                    try:
                        result = launch_integration(
                            service, operator_token, row["repository"], item, version=3
                        )
                        if not confirmed_launch(result, row["repository"], item, version=3):
                            raise RuntimeError("Production-OS launch receipt did not match requested v3 project")
                        row["dispatches"].append("recovery-v3: " + item["repository"])
                        already.append({"repository": row["repository"],
                                        "final_goal": recovery_marker, "status": "ACTIVE"})
                        busy_targets.add(row["repository"].lower())
                        dispatched += 1
                    except (RuntimeError, ValueError, TypeError) as exc:
                        report["errors"].append(row["repository"] + " recovery: " + str(exc))
                        launch_outcome_uncertain = True
                        break
                    continue
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
                    if not confirmed_launch(result, row["repository"], item):
                        raise RuntimeError("Production-OS launch receipt did not match requested v2 project")
                    row["dispatches"].append(
                        ("recovery-v2: " if is_recovery else "submitted-v2: ") + item["repository"]
                    )
                    already.append({"repository": row["repository"],
                                    "final_goal": marker, "status": "ACTIVE"})
                    busy_targets.add(row["repository"].lower())
                    dispatched += 1
                except (RuntimeError, ValueError, TypeError) as exc:
                    report["errors"].append(row["repository"] + " dispatch: " + str(exc))
                    launch_outcome_uncertain = True
                    break
    if operator_token and scan_complete and available_slots is not None:
        if launch_outcome_uncertain:
            report["dispatch_status"] = "blocked (unconfirmed Production-OS launch)"
        elif report["errors"]:
            report["dispatch_status"] = "failed (integration dispatch errors)"
        elif args.max_dispatch == 0:
            report["dispatch_status"] = "disabled (read-only scan)"
        elif available_slots == 0:
            if active_integrations:
                report["dispatch_status"] = "paused (active portfolio integrations)"
            elif failed_v2_integrations and launches_today is not None and launches_today >= 1:
                report["dispatch_status"] = "throttled (UTC daily launch quota exhausted)"
            else:
                report["dispatch_status"] = "paused (fleet capacity unavailable)"
        elif dispatched == 0:
            report["dispatch_status"] = "idle (no new eligible integration)"
    report["summary"] = {
        "discovered": len(source), "inspected": sum(p["status"] != "scan-failed" for p in report["projects"]),
        "with_suggestions": sum(bool(p["suggestions"]) for p in report["projects"]),
        "with_native_suggestions": sum(
            any(item["mode"] == "native" for item in p["suggestions"])
            for p in report["projects"]
        ),
        "native_suggestions": sum(
            item["mode"] == "native"
            for p in report["projects"] for item in p["suggestions"]
        ),
        "dispatched": dispatched, "active_integrations": active_integrations,
        "failed_v2_integrations": failed_v2_integrations,
        "available_dispatch_slots": available_slots,
        "launches_today_utc": launches_today,
        "failures": len(report["errors"]),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], sort_keys=True))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
