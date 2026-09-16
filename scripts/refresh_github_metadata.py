#!/usr/bin/env python3
"""Refresh non-opinionated GitHub metadata for catalog repositories.

Uses only the Python standard library. GITHUB_TOKEN is optional but strongly
recommended in CI to avoid anonymous API rate limits.
"""
import argparse, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
API = "https://api.github.com/repos/{}"
FIELDS = {
    "stars": "stargazers_count",
    "forks": "forks_count",
    "openIssues": "open_issues_count",
    "archived": "archived",
    "disabled": "disabled",
    "defaultBranch": "default_branch",
    "license": None,
    "pushedAt": "pushed_at",
}


def fetch(repo, token=None, retries=2):
    headers = {"Accept":"application/vnd.github+json","User-Agent":"star-list-metadata-refresh","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"] = f"Bearer {token}"
    req = Request(API.format(repo), headers=headers)
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=20) as res:
                return json.load(res)
        except HTTPError as e:
            if e.code in (403, 429) and attempt < retries:
                time.sleep(2 ** attempt); continue
            raise
        except URLError:
            if attempt < retries:
                time.sleep(2 ** attempt); continue
            raise


def metadata(raw):
    out = {}
    for target, source in FIELDS.items():
        if target == "license":
            lic = raw.get("license")
            out[target] = lic.get("spdx_id") if isinstance(lic, dict) else None
        else:
            out[target] = raw.get(source)
    return out


def is_missing_repository_error(error):
    return isinstance(error, HTTPError) and error.code in (404, 410)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Update catalog.json in place")
    ap.add_argument("--limit", type=int, default=0, help="Refresh only first N repositories (0 = all)")
    ap.add_argument("--fail-fast", action="store_true")
    args = ap.parse_args()

    data = json.loads(CATALOG.read_text())
    repos = data.get("repositories", [])
    if args.limit > 0: repos = repos[:args.limit]
    token = os.environ.get("GITHUB_TOKEN")
    failures, fatal_failures, changed = [], [], 0

    for i, r in enumerate(repos, 1):
        name = r["repo"]
        try:
            fresh = metadata(fetch(name, token))
            if r.get("github") != fresh:
                r["github"] = fresh
                changed += 1
            print(f"[{i}/{len(repos)}] OK {name}", file=sys.stderr)
        except Exception as e:
            failure = {"repo":name,"error":str(e)}
            failures.append(failure)
            if args.fail_fast or not is_missing_repository_error(e):
                fatal_failures.append(failure)
            print(f"[{i}/{len(repos)}] ERROR {name}: {e}", file=sys.stderr)
            if args.fail_fast: break

    data["metadata"] = data.get("metadata", {})
    data["metadata"]["githubRefreshedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    data["metadata"]["githubRefreshFailures"] = failures

    if args.write:
        CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    else:
        print(json.dumps({"checked":len(repos),"changed":changed,"failures":failures}, indent=2))

    if fatal_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
