#!/usr/bin/env python3
"""Backfill only unknown repository licenses using conservative root-file detection."""
import argparse
import json
import os
from pathlib import Path

import refresh_github_metadata as refresh

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN = {None, "", "NOASSERTION"}


def backfill(repos, resolver, token=None):
    changed = []
    checked = 0
    for repo in repos:
        github = repo.get("github")
        if not isinstance(github, dict) or github.get("license") not in UNKNOWN:
            continue
        checked += 1
        name = repo.get("repo")
        branch = github.get("defaultBranch")
        if not name or not branch:
            continue
        detected = resolver(name, branch, token)
        if detected:
            github["license"] = detected
            changed.append({"repo": name, "license": detected})
    return checked, changed


def main():
    parser = argparse.ArgumentParser(description="Backfill unknown licenses without refreshing unrelated metadata.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    data = json.loads(CATALOG.read_text())
    token = os.environ.get("GITHUB_TOKEN")
    checked, changed = backfill(data.get("repositories", []), refresh.fallback_license, token)

    result = {"checked": checked, "changed": len(changed), "licenses": changed}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.write and changed:
        CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
