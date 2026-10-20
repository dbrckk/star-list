#!/usr/bin/env python3
"""Reconcile missing permanent GitHub repository IDs, without changing curation.

Read-only by default. --write needs an authenticated GitHub token, validates
current canonical names and existing IDs, and writes catalog.json atomically.
404/renamed repositories remain unresolved; an API outage blocks all writes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request

from sync_github_stars import SAFE_GITHUB_HTTP

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
NAME = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


def github_metadata(repo: str, token: str) -> dict | None:
    """One bounded GitHub metadata lookup for an already curated repository."""
    owner, name = repo.split("/")
    url = "https://api.github.com/repos/" + quote(owner, safe="") + "/" + quote(name, safe="")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "star-list-permanent-repo-id-backfill/1.0",
        "Authorization": "Bearer " + token,
    }
    for attempt in range(3):
        try:
            with SAFE_GITHUB_HTTP.open(Request(url, headers=headers), timeout=20) as res:
                raw = res.read(150_001)
            if len(raw) > 150_000:
                raise RuntimeError("Oversized GitHub metadata response")
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise RuntimeError("GitHub repository metadata was not an object")
            return value
        except HTTPError as exc:
            if exc.code in (404, 410):
                return None
            if exc.code in (500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("GitHub ID backfill API request failed: HTTP " + str(exc.code)) from exc
        except (URLError, TimeoutError, OSError, ValueError, UnicodeError) as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("GitHub ID backfill API response was unavailable") from exc
    raise RuntimeError("GitHub ID backfill retry budget exhausted")


def reconcile(data: dict, token: str | None = None, *, max_requests: int = 250) -> tuple[dict, dict]:
    rows = data.get("repositories")
    if not isinstance(rows, list):
        raise ValueError("Catalog repositories must be a list")
    owner_by_id = {}
    names = set()
    missing = []
    for row in rows:
        if not isinstance(row, dict) or not NAME.fullmatch(str(row.get("repo") or "")):
            raise ValueError("Invalid catalog repository identity")
        canonical = row["repo"].casefold()
        if canonical in names:
            raise ValueError("Duplicate catalog repository name")
        names.add(canonical)
        rid = row.get("githubRepositoryId")
        if rid is None:
            missing.append(row)
            continue
        if type(rid) is not int or rid <= 0:
            raise ValueError("Invalid existing permanent GitHub ID")
        if rid in owner_by_id:
            raise ValueError("Duplicate permanent GitHub repository ID")
        owner_by_id[rid] = canonical
    report = {
        "mode": "online" if token else "offline",
        "catalogSize": len(rows),
        "previouslyVerified": len(owner_by_id),
        "missingBefore": len(missing),
        "checked": 0,
        "assigned": 0,
        "missingAfter": len(missing),
        "unresolved": [],
        "complete": bool(token) and len(missing) <= max_requests,
    }
    if token:
        for row in missing[:max_requests]:
            repo = row["repo"]
            try:
                response = github_metadata(repo, token)
            except RuntimeError as exc:
                report["complete"] = False
                report["error"] = str(exc)
                break
            report["checked"] += 1
            if response is None:
                report["unresolved"].append({"repo": repo, "reason": "not-found"})
                continue
            actual = response.get("full_name")
            stable_id = response.get("id")
            if not isinstance(actual, str) or actual.casefold() != repo.casefold():
                report["unresolved"].append({"repo": repo, "reason": "renamed-or-transferred"})
                continue
            if response.get("private") is True or type(stable_id) is not int or stable_id <= 0:
                report["unresolved"].append({"repo": repo, "reason": "invalid-or-private"})
                continue
            previous = owner_by_id.get(stable_id)
            if previous is not None and previous != repo.casefold():
                report["unresolved"].append({"repo": repo, "reason": "identity-conflict"})
                continue
            row["githubRepositoryId"] = stable_id
            owner_by_id[stable_id] = repo.casefold()
            report["assigned"] += 1
    report["missingAfter"] = report["missingBefore"] - report["assigned"]
    return data, report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="Write a fully reconciled catalog after API success")
    ap.add_argument("--max-requests", type=int, default=250)
    ap.add_argument("--report-json", type=Path)
    args = ap.parse_args()
    if not 1 <= args.max_requests <= 500:
        ap.error("--max-requests must be between 1 and 500")
    token = (os.environ.get("GITHUB_TOKEN") or "").strip() if args.write else None
    if args.write and not token:
        print("Authenticated GITHUB_TOKEN required to write IDs", file=sys.stderr)
        return 1
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    data, report = reconcile(data, token, max_requests=args.max_requests)
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report_json:
        args.report_json.write_text(output, encoding="utf-8")
    else:
        print(output)
    if args.write and not report["complete"]:
        print("Incomplete GitHub ID scan; refusing partial catalog publication", file=sys.stderr)
        return 1
    if args.write and report["assigned"]:
        # Do not publish a partially serialized catalog; preserve all other
        # repository fields, order, selection policy and metadata unchanged.
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=CATALOG.parent,
                                         prefix=".catalog-id-backfill-", suffix=".json",
                                         delete=False) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp.write("\n")
            temporary = Path(tmp.name)
        os.replace(temporary, CATALOG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
