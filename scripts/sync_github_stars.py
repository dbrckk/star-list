#!/usr/bin/env python3
"""Read public GitHub Stars and prepare a review report; never edit catalog.json."""
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
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER_PATTERN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
REPO_PATTERN = re.compile(r"([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/([A-Za-z0-9_.-]{1,100})\Z")
ISSUE_MARKER = "<!-- star-list-star-sync -->"


def validate_user(user):
    if not isinstance(user, str) or not USER_PATTERN.fullmatch(user):
        raise ValueError("GitHub username must be 1-39 letters, digits or interior hyphens")
    return user


def normalize_repo(repo):
    if not isinstance(repo, str) or not REPO_PATTERN.fullmatch(repo):
        raise ValueError("GitHub returned an invalid repository identity")
    return repo.lower()


def api_stars(user, token=None, max_pages=100, opener=urlopen, sleeper=time.sleep):
    """Fetch all public stars. A failed/truncated page aborts the entire synchronization."""
    validate_user(user)
    if not isinstance(max_pages, int) or max_pages < 1:
        raise ValueError("max_pages must be >= 1")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "star-list-star-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token

    found = {}
    duplicate_items = 0
    pages = 0
    for page in range(1, max_pages + 1):
        url = "https://api.github.com/users/" + user + "/starred?" + urlencode(
            {"per_page": 100, "page": page}
        )
        request = Request(url, headers=headers)
        for attempt in range(3):
            try:
                with opener(request, timeout=20) as response:
                    raw = response.read()
                    link = response.headers.get("Link", "")
                break
            except HTTPError as exc:
                retryable = exc.code in (429, 500, 502, 503, 504)
                if retryable and attempt < 2:
                    try:
                        delay = min(8.0, max(0.0, float(exc.headers.get("Retry-After", 2 ** attempt))))
                    except (ValueError, TypeError, AttributeError):
                        delay = float(2 ** attempt)
                    sleeper(delay)
                    continue
                hint = " (check token permissions or API rate limits)" if exc.code in (401, 403, 429) else ""
                raise RuntimeError("GitHub Stars API returned HTTP " + str(exc.code) + hint) from exc
            except (OSError, URLError) as exc:
                if attempt < 2:
                    sleeper(float(2 ** attempt))
                    continue
                raise RuntimeError("GitHub Stars API request failed") from exc

        try:
            payload = json.loads(raw)
        except (ValueError, UnicodeDecodeError) as exc:
            raise RuntimeError("Invalid GitHub Stars API JSON response") from exc
        if not isinstance(payload, list) or len(payload) > 100:
            raise RuntimeError("Unexpected GitHub Stars API response; refusing partial report")
        pages += 1
        for entry in payload:
            if not isinstance(entry, dict):
                raise RuntimeError("Malformed GitHub Stars API repository record")
            repo = entry.get("full_name")
            try:
                key = normalize_repo(repo)
            except ValueError as exc:
                raise RuntimeError("Malformed repository identity in GitHub Stars response") from exc
            if key in found:
                duplicate_items += 1
                continue
            license_obj = entry.get("license")
            license_name = license_obj.get("spdx_id") if isinstance(license_obj, dict) else None
            found[key] = {
                "repo": repo,
                "url": "https://github.com/" + repo,
                "stars": entry.get("stargazers_count") if isinstance(entry.get("stargazers_count"), int) else None,
                "language": entry.get("language") if isinstance(entry.get("language"), str) else None,
                "license": license_name if isinstance(license_name, str) else None,
                "archived": entry.get("archived") is True,
                "disabled": entry.get("disabled") is True,
                "pushedAt": entry.get("pushed_at") if isinstance(entry.get("pushed_at"), str) else None,
            }
        # We generate the next URL locally; never follow an untrusted Link URL.
        has_next = bool(re.search(r'rel\s*=\s*["\x27]?next(?:["\x27]|[,;\s]|$)', link, re.IGNORECASE))
        if not has_next:
            return [found[k] for k in sorted(found)], pages, duplicate_items
        if not payload:
            raise RuntimeError("GitHub returned an empty page with a next-page link")
    raise RuntimeError(
        "Stars pagination exceeded --max-pages; refusing truncated results"
    )


def catalog_identities(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RuntimeError("Catalog is missing or invalid; no synchronization performed") from exc
    rows = data.get("repositories") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise RuntimeError("Catalog repositories must be a list")
    known = set()
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError("Malformed catalog entry")
        try:
            identity = normalize_repo(row.get("repo"))
        except ValueError as exc:
            raise RuntimeError("Catalog contains an invalid repository identity") from exc
        if identity in known:
            raise RuntimeError("Catalog has duplicate repository identities")
        known.add(identity)
    return known


def build_report(username, stars, catalog, pages, duplicates=0, now=None):
    new = [entry for entry in stars if normalize_repo(entry["repo"]) not in catalog]
    new.sort(key=lambda item: item["repo"].lower())
    return {
        "schemaVersion": 1,
        "username": validate_user(username),
        "checkedAt": (now or datetime.now(timezone.utc)).isoformat(),
        "source": "GitHub public starred repositories API",
        "summary": {
            "starred": len(stars),
            "alreadyCataloged": len(stars) - len(new),
            "new": len(new),
            "pages": pages,
            "duplicateApiItems": duplicates,
        },
        "newRepositories": new,
    }


def render_issue(report, limit=50):
    if limit < 1:
        raise ValueError("limit must be >= 1")
    user = report["username"]
    counts = report["summary"]
    entries = report["newRepositories"]
    lines = [
        ISSUE_MARKER,
        "# GitHub Stars awaiting review",
        "",
        "Account: " + user,
        "Last checked: " + report["checkedAt"],
        "",
        "Public stars: **{}**; cataloged: **{}**; awaiting review: **{}**.".format(
            counts["starred"], counts["alreadyCataloged"], counts["new"]
        ),
        "",
        "New repositories are **not** imported or approved automatically.",
        "Review identity, licensing, functionality and compatibility before using the existing reviewed-metadata importer.",
        "",
    ]
    if not entries:
        lines.append("All accessible starred repositories are already in the catalog.")
    else:
        lines.extend([
            "| GitHub repository | Stars | Language | License metadata | Status |",
            "| --- | ---: | --- | --- | --- |",
        ])
        for row in entries[:limit]:
            status = "archived" if row["archived"] else ("disabled" if row["disabled"] else "review")
            stars = str(row["stars"]) if row["stars"] is not None else "?"
            language = (row["language"] or "unknown").replace("|", "/").replace("\n", " ")
            license_name = (row["license"] or "unresolved").replace("|", "/").replace("\n", " ")
            lines.append(
                "| [{repo}]({url}) | {stars} | {language} | {license} | {status} |".format(
                    repo=row["repo"], url=row["url"], stars=stars,
                    language=language, license=license_name, status=status
                )
            )
        if len(entries) > limit:
            lines.extend(["", "Showing {} of {} new repositories; see the workflow artifact for all entries.".format(limit, len(entries))])
    lines.extend([
        "",
        "Only public/accessible stars are discoverable with the workflow token.",
        "A repository's GitHub license label does not establish model-weight or other third-party asset rights.",
        "",
    ])
    return "\n".join(lines)


def write_json(path, payload):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check GitHub Stars against star-list (read-only).")
    parser.add_argument("--user", default="dbrckk")
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--max-pages", type=int, default=100)
    parser.add_argument("--issue-limit", type=int, default=50)
    args = parser.parse_args(argv)
    if args.max_pages < 1 or args.issue_limit < 1:
        parser.error("max-pages and issue-limit must be >= 1")
    try:
        catalog = catalog_identities(args.catalog)
        stars, pages, duplicates = api_stars(
            args.user, token=os.environ.get("GITHUB_TOKEN"), max_pages=args.max_pages
        )
        report = build_report(args.user, stars, catalog, pages, duplicates)
    except (RuntimeError, ValueError) as exc:
        parser.exit(2, "Star sync failed: " + str(exc) + "\n")

    if args.report_json:
        write_json(args.report_json, report)
    if args.report_md:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(render_issue(report, args.issue_limit) + "\n", encoding="utf-8")
    if args.manifest:
        write_json(args.manifest, {
            "source": "GitHub public Stars of " + args.user,
            "checkedAt": report["checkedAt"],
            "repositories": [entry["repo"] for entry in stars],
        })
    print("GitHub stars checked: {} | cataloged: {} | new: {} | pages: {}".format(
        report["summary"]["starred"],
        report["summary"]["alreadyCataloged"],
        report["summary"]["new"],
        report["summary"]["pages"],
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
