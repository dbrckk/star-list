#!/usr/bin/env python3
"""Check immutable upstream SKILL.md links without executing remote instructions.

Offline mode validates local pinned-source contracts only. Online mode checks
GitHub API *file metadata*, never imports, executes or trusts remote SKILL.md.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.client import HTTPException
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from agent_skill_discovery import load_skills

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "star-list-pinned-skill-source-audit/1.0"
MAX_RESPONSE = 500_000


class RejectRedirect(HTTPRedirectHandler):
    """Never forward a GitHub bearer token to a redirected URL."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


HTTP = build_opener(RejectRedirect())


def inspect_source(row: dict, token: str) -> tuple[str, str]:
    """Check the pinned SKILL.md file metadata; never read/parse its instructions."""
    owner, name = row["sourceRepository"].split("/")
    path = "/".join(quote(part, safe="") for part in row["sourcePath"].split("/"))
    url = ("https://api.github.com/repos/" + quote(owner, safe="")
           + "/" + quote(name, safe="") + "/contents/" + path
           + "?ref=" + row["sourceCommit"])
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(2):
        try:
            with HTTP.open(Request(url, headers=headers), timeout=20) as response:
                payload = response.read(MAX_RESPONSE + 1)
            if len(payload) > MAX_RESPONSE:
                return "invalid", "metadata-too-large"
            value = json.loads(payload.decode("utf-8"))
            if not isinstance(value, dict):
                return "invalid", "unexpected-metadata"
            if (value.get("type") != "file"
                    or value.get("path") != row["sourcePath"]
                    or type(value.get("size")) is not int
                    or not 0 < value["size"] <= 200_000
                    or not isinstance(value.get("sha"), str)
                    or not re.fullmatch(r"[0-9a-f]{40}", value["sha"])):
                return "invalid", "unexpected-file-metadata"
            return "verified", "pinned-file-metadata"
        except HTTPError as exc:
            if exc.code == 404:
                return "missing", "pinned-file-not-found"
            if exc.code in (500, 502, 503, 504) and attempt == 0:
                time.sleep(1)
                continue
            return "unavailable", ("rate-limited" if exc.code in (403, 429)
                                    else "upstream-http-error")
        except (URLError, TimeoutError, OSError, HTTPException, ValueError,
                UnicodeError, json.JSONDecodeError):
            if attempt == 0:
                time.sleep(1)
                continue
            return "unavailable", "upstream-response-unavailable"
    return "unavailable", "retry-budget-exhausted"


def make_report(*, online: bool, token: str) -> dict:
    rows = load_skills()["skills"]
    entries = []
    for row in rows:
        status, reason = inspect_source(row, token) if online else ("unchecked", "offline-validation-only")
        entries.append({
            "id": row["id"],
            "sourceRepository": row["sourceRepository"],
            "sourceCommit": row["sourceCommit"],
            "sourcePath": row["sourcePath"],
            "sourceUrl": row["sourceUrl"] + "/blob/" + row["sourceCommit"] + "/" + row["sourcePath"],
            "status": status,
            "reason": reason,
        })
    counts = {status: sum(item["status"] == status for item in entries)
              for status in ("verified", "missing", "invalid", "unavailable", "unchecked")}
    complete = online and counts["unavailable"] == 0 and counts["unchecked"] == 0
    return {
        "schemaVersion": 1,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "mode": "online" if online else "offline",
        "total": len(entries),
        "coverageComplete": complete,
        "counts": counts,
        "findings": counts["missing"] + counts["invalid"],
        "sourceContentReviewed": False,
        "automaticInstallation": False,
        "entries": entries,
    }


def markdown(report: dict) -> str:
    counts = report["counts"]
    lines = [
        "<!-- star-list-agent-skill-source-audit -->",
        "# Pinned agent skill source audit",
        "",
        f"- Pinned SKILL.md references: **{report['total']}**",
        f"- Source metadata verified: **{counts['verified']}**",
        f"- Missing or invalid: **{report['findings']}**",
        f"- Unavailable (inconclusive): **{counts['unavailable']}**",
        f"- Coverage complete: **{'yes' if report['coverageComplete'] else 'no'}**",
        "",
        "This is link/metadata verification only, not a review of SKILL.md instructions,",
        "licensing, safety, installation or suitability for automatic execution.",
        "",
    ]
    failures = [e for e in report["entries"] if e["status"] in ("missing", "invalid", "unavailable")]
    if failures:
        lines.extend(["## References requiring attention", "",
                      "| Skill | Source | Status | Detail |",
                      "| --- | --- | --- | --- |"])
        for item in failures:
            lines.append(
                f"| `{item['id']}` | [pinned file]({item['sourceUrl']})"
                f" | {item['status']} | {item['reason']} |"
            )
    else:
        lines.append("No missing or invalid pinned source references were detected.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true", help="Check pinned sources against GitHub metadata")
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    args = parser.parse_args()
    report = make_report(online=args.online, token=os.environ.get("GITHUB_TOKEN", ""))
    data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.write_text(data, encoding="utf-8")
    else:
        print(data)
    if args.markdown_output:
        args.markdown_output.write_text(markdown(report), encoding="utf-8")
    if args.online and not report["coverageComplete"]:
        print("INCOMPLETE: could not verify every pinned skill source; refusing a clean claim", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
