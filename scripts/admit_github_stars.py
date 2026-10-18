#!/usr/bin/env python3
"""Admit every accessible starred repository into the catalog, conservatively.

New entries receive an audit tier until a human or richer analysis verifies
license terms, suitability, and production readiness. Never silently skip a
Star or save a partly built catalog.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request

from star_import_pipeline import write_catalog_if_valid
from sync_github_stars import ROOT, SAFE_GITHUB_HTTP, normalize_repo

DOMAINS = (
    ("cybersecurity", ("cybersecurity", "security", "pentest", "vulnerability", "bug bounty", "ctf", "malware", "osint", "exploit")),
    ("trading", ("trading", "backtest", "finance", "market data", "stock market", "quantitative finance", "cryptocurrency exchange")),
    ("game_dev", ("roblox", "godot", "unity", "unreal engine", "game development", "gamedev", "game engine", "blender addon")),
    ("ai_memory", ("vector database", "rag", "retrieval augmented", "llm memory", "knowledge graph")),
    ("ai_media", ("image generation", "video generation", "text to speech", "speech synthesis", "stable diffusion", "comfyui", "image editing")),
    ("ai_agents", ("ai agent", "agentic", "llm", "large language model", "autonomous agent", "langchain", "openai", "ollama")),
    ("mobile", ("android", "ios app", "flutter", "react native", "kotlin multiplatform")),
    ("web_frontend", ("frontend", "front-end", "react", "vue.js", "svelte", "next.js", "ui components")),
    ("backend", ("backend", "back-end", "fastapi", "django", "web api", "database server")),
    ("devops", ("kubernetes", "docker", "terraform", "devops", "infrastructure as code", "ci/cd")),
    ("data_ml", ("machine learning", "data science", "pytorch", "tensorflow", "data analytics")),
    ("graphics", ("3d modeling", "3d rendering", "graphics", "svg", "animation", "texture")),
    ("software_engineering", ("developer tools", "code editor", "programming language", "static analysis", "build system")),
    ("productivity", ("productivity", "note taking", "task management", "automation")),
)
CATEGORIES = {
    "cybersecurity": "Cybersécurité", "trading": "Trading / finance",
    "game_dev": "Développement de jeux", "ai_memory": "Mémoire / IA",
    "ai_media": "Génération de médias / IA", "ai_agents": "Agents / IA / développement",
    "mobile": "Applications mobiles", "web_frontend": "Développement web",
    "backend": "Backend / API", "devops": "DevOps / infrastructure",
    "data_ml": "Data / Machine Learning", "graphics": "Graphisme / 3D",
    "software_engineering": "Outils de développement",
    "productivity": "Productivité", "other": "Autres / à examiner",
}


def classify(meta):
    text = " ".join([
        str(meta.get("name") or ""),
        str(meta.get("description") or ""),
        " ".join(x for x in meta.get("topics", []) if isinstance(x, str)),
    ]).lower()
    for domain, markers in DOMAINS:
        if any(m in text for m in markers):
            return domain
    return "other"


def get_repo(repo, token=None, opener=SAFE_GITHUB_HTTP.open, sleeper=time.sleep):
    """Fetch full repository metadata, with bounded retry and canonical ID check."""
    normalize_repo(repo)
    url = "https://api.github.com/repos/" + repo
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "star-list-admission",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(4):
        try:
            with opener(Request(url, headers=headers), timeout=25) as response:
                result = json.load(response)
            if not isinstance(result, dict):
                raise RuntimeError("Malformed GitHub repository metadata: " + repo)
            return result
        except HTTPError as exc:
            if exc.code in (403, 429, 500, 502, 503, 504) and attempt < 3:
                raw_delay = exc.headers.get("Retry-After", str(2 ** attempt))
                try:
                    delay = min(20, max(0, float(raw_delay)))
                except (ValueError, TypeError):
                    delay = float(2 ** attempt)
                sleeper(delay)
                continue
            raise RuntimeError(f"Repository metadata unavailable: {repo} (HTTP {exc.code})") from exc
        except (OSError, URLError, ValueError) as exc:
            if attempt < 3:
                sleeper(float(2 ** attempt))
                continue
            raise RuntimeError("Repository metadata unavailable: " + repo) from exc
    raise RuntimeError("Repository metadata retry budget exhausted: " + repo)


def catalog_entry(meta):
    repo = meta.get("full_name")
    normalize_repo(repo)
    repo_id = meta.get("id")
    if type(repo_id) is not int or repo_id <= 0:
        raise RuntimeError("Invalid stable GitHub ID: " + repo)
    license_data = meta.get("license")
    license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else None
    if not isinstance(license_id, str):
        license_id = None

    def count(key):
        value = meta.get(key)
        if type(value) is not int or value < 0:
            raise RuntimeError(f"Missing or invalid {key}: {repo}")
        return value

    branch = meta.get("default_branch")
    if not isinstance(branch, str) or not branch:
        branch = "unknown"  # Nonempty schema value; the audit tier marks the gap.
    domain = classify(meta)
    language = meta.get("language")
    languages = [language.lower()] if isinstance(language, str) and language.strip() else []
    description = meta.get("description")
    guidance = [re.sub(r"\s+", " ", description).strip()[:200]] if isinstance(description, str) and description.strip() else []
    topics = meta.get("topics")
    capabilities = [x[:80] for x in topics if isinstance(x, str) and x.strip()][:12] if isinstance(topics, list) else []
    return {
        "repo": repo,
        "githubRepositoryId": repo_id,
        "score": 6.0,
        "tier": "audit",
        "category": CATEGORIES[domain],
        "domain": domain,
        "capabilities": capabilities,
        "languages": languages,
        "platforms": [],
        "selfHosted": "unknown",
        "runtime": [],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "unknown",
        "github": {
            "stars": count("stargazers_count"),
            "forks": count("forks_count"),
            "openIssues": count("open_issues_count"),
            "archived": meta.get("archived") is True,
            "disabled": meta.get("disabled") is True,
            "defaultBranch": branch,
            "license": license_id,
            "pushedAt": meta.get("pushed_at") if isinstance(meta.get("pushed_at"), str) else None,
        },
        "bestFor": guidance,
        "avoidWhen": ["production use before licensing and security review"],
        "guidanceSource": "inferred",
        "lifecycle": "legacy" if meta.get("archived") or meta.get("disabled") else "reference",
    }


def manifest_stable_ids(manifest, report):
    """Verify that all identity rows belong to the exact read-only Stars scan."""
    if not isinstance(manifest, dict) or not isinstance(report, dict):
        raise RuntimeError("Stars identity manifest is malformed")
    if (manifest.get("source") != "GitHub public Stars of dbrckk"
            or manifest.get("checkedAt") != report.get("checkedAt")):
        raise RuntimeError("Stars identity manifest does not match the sync report")
    names, rows = manifest.get("repositories"), manifest.get("identities")
    summary = report.get("summary")
    if (not isinstance(summary, dict) or type(summary.get("starred")) is not int
            or not isinstance(names, list) or not isinstance(rows, list)
            or len(names) != len(rows) or len(names) != summary["starred"]):
        raise RuntimeError("Stars identity manifest does not cover the complete scan")
    expected_new = report.get("newRepositories")
    if (not isinstance(expected_new, list)
            or type(summary.get("new")) is not int
            or len(expected_new) != summary["new"]
            or summary.get("alreadyCataloged") != len(names) - len(expected_new)):
        raise RuntimeError("Stars identity manifest disagrees with the review counts")
    ids = {}
    owners = {}
    for name, row in zip(names, rows):
        if not isinstance(row, dict) or row.get("repo") != name:
            raise RuntimeError("Stars identity manifest has mismatched repository rows")
        key = normalize_repo(name)
        rid = row.get("githubRepositoryId")
        if key in ids or (rid is not None and (type(rid) is not int or rid <= 0)):
            raise RuntimeError("Stars identity manifest has invalid or duplicate IDs")
        if rid is not None and rid in owners and owners[rid] != key:
            raise RuntimeError("Stars identity manifest maps one ID to multiple names")
        ids[key] = rid
        if rid is not None:
            owners[rid] = key
    for star in expected_new:
        key = normalize_repo(star["repo"])
        if key not in ids or ids[key] != star.get("githubRepositoryId"):
            raise RuntimeError("Stars identity manifest disagrees with new repositories")
    return ids


def admit(catalog, stars, fetcher, known_star_ids=None):
    """Reconcile by both canonical name and permanent ID; fail on any ambiguity."""
    old = catalog.get("repositories")
    if not isinstance(old, list):
        raise RuntimeError("Malformed source catalog")
    by_name = {normalize_repo(x["repo"]): x.get("githubRepositoryId") for x in old}
    by_id = {x["githubRepositoryId"] for x in old if type(x.get("githubRepositoryId")) is int}
    if len(by_name) != len(old):
        raise RuntimeError("Duplicate identities in source catalog")
    fresh = []
    already = 0
    transfers = []
    for star in stars:
        key = normalize_repo(star["repo"])
        rid = star.get("githubRepositoryId")
        recorded_id = by_name.get(key)
        if recorded_id is not None and rid is not None and recorded_id != rid:
            # Re-check even when a stale read-only report reached admission:
            # a recycled owner/name is not the same GitHub repository.
            raise RuntimeError(
                "Star repository identity conflict (name reused with a new GitHub ID): "
                + star["repo"]
            )
        if key in by_name or (rid is not None and rid in by_id):
            already += 1
            if key not in by_name:
                transfers.append(star["repo"])
            continue
        meta = fetcher(star["repo"])
        entry = catalog_entry(meta)
        if rid is None or entry["githubRepositoryId"] != rid:
            raise RuntimeError("Star identity changed while synchronizing: " + star["repo"])
        canonical = normalize_repo(entry["repo"])
        if canonical in by_name:
            previous_id = by_name[canonical]
            if previous_id is not None and previous_id != entry["githubRepositoryId"]:
                raise RuntimeError(
                    "GitHub metadata reused a cataloged repository name with a new ID: "
                    + entry["repo"]
                )
        if canonical in by_name or entry["githubRepositoryId"] in by_id:
            already += 1
            continue
        if meta.get("private") is True:
            raise RuntimeError("Unexpected private repository in public Stars: " + star["repo"])
        fresh.append(entry)
        by_name[canonical] = entry["githubRepositoryId"]
        by_id.add(entry["githubRepositoryId"])
    result = dict(catalog)
    # Do not mutate the caller's loaded catalog before all checks pass.
    entries = [dict(row) for row in old] + sorted(fresh, key=lambda r: r["repo"].lower())
    enriched = 0
    if known_star_ids is not None:
        rows_by_name = {normalize_repo(row["repo"]): row for row in entries}
        rows_by_id = {
            row["githubRepositoryId"]: row
            for row in entries if type(row.get("githubRepositoryId")) is int
        }
        if len(rows_by_name) != len(entries) or len(rows_by_id) != sum(
            type(row.get("githubRepositoryId")) is int for row in entries
        ):
            raise RuntimeError("Catalog has duplicate permanent repository identities")
        for original_name, rid in known_star_ids.items():
            key = normalize_repo(original_name)
            if rid is not None and (type(rid) is not int or rid <= 0):
                raise RuntimeError("Stars manifest contains an invalid repository ID")
            entry = rows_by_name.get(key)
            if entry is None:
                # An existing repository may have transferred to this new
                # owner/name while preserving its stable ID.
                if rid is None or rid not in rows_by_id:
                    raise RuntimeError("Star is missing from candidate catalog: " + original_name)
                continue
            recorded_id = entry.get("githubRepositoryId")
            if rid is not None and recorded_id is not None and rid != recorded_id:
                raise RuntimeError("Star repository identity conflict: " + original_name)
            if rid is not None and recorded_id is None:
                occupied = rows_by_id.get(rid)
                if occupied is not None and occupied is not entry:
                    raise RuntimeError("Star stable ID belongs to another catalog entry: " + original_name)
                entry["githubRepositoryId"] = rid
                rows_by_id[rid] = entry
                enriched += 1
    result["repositories"] = entries
    return result, {"starred": len(stars), "alreadyCataloged": already,
                    "admitted": len(fresh), "identityEnriched": enriched,
                    "transfersRecognizedById": transfers,
                    "catalogAfter": len(result["repositories"]),
                    "admittedRepositories": [x["repo"] for x in fresh]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync-report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, help="Same-run full Stars identity snapshot")
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = json.loads(args.sync_report.read_text(encoding="utf-8"))
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        if report.get("username") != "dbrckk" or report.get("schemaVersion") != 1:
            raise RuntimeError("Stars report source is not verified")
        # A report lists only missing Stars. The manifest provides the complete
        # snapshot, and admission operates on a report produced in the same job.
        stars = report.get("newRepositories")
        if not isinstance(stars, list) or len(stars) != report["summary"]["new"]:
            raise RuntimeError("Stars report is incomplete")
        known_star_ids = None
        if args.manifest:
            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
            known_star_ids = manifest_stable_ids(manifest, report)
        token = os.environ.get("GITHUB_TOKEN")
        updated, summary = admit(
            catalog, stars, lambda repo: get_repo(repo, token),
            known_star_ids=known_star_ids,
        )
        summary["starred"] = report["summary"]["starred"]
        summary["alreadyCataloged"] = report["summary"]["starred"] - summary["admitted"]
        summary["checkedAt"] = datetime.now(timezone.utc).isoformat()
        if args.report_json:
            args.report_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if (summary["admitted"] or summary["identityEnriched"]) and not args.dry_run:
            ok, output = write_catalog_if_valid(updated, args.catalog)
            if not ok:
                raise RuntimeError("Catalog failed validation: " + output[-5000:])
        print(json.dumps(summary, ensure_ascii=False))
        return 0
    except (OSError, KeyError, ValueError, RuntimeError) as exc:
        print("Automatic Stars admission failed: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
