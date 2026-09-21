#!/usr/bin/env python3
"""Refresh non-opinionated GitHub metadata for catalog repositories.

Uses only the Python standard library. GITHUB_TOKEN is optional but strongly
recommended in CI to avoid anonymous API rate limits.
"""
import argparse, base64, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
API = "https://api.github.com/repos/{}"
CONTENTS_API = "https://api.github.com/repos/{}/contents/{}"
LICENSE_NAMES = ("license", "licence", "copying", "notice")
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


def _request_json(url, token=None, retries=2):
    headers = {"Accept":"application/vnd.github+json","User-Agent":"star-list-metadata-refresh","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
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


def fetch(repo, token=None, retries=2):
    return _request_json(API.format(repo), token=token, retries=retries)


def fetch_contents(repo, path="", ref=None, token=None, retries=2):
    encoded = quote(path, safe="/")
    url = CONTENTS_API.format(repo, encoded)
    if ref:
        url += "?ref=" + quote(ref, safe="")
    return _request_json(url, token=token, retries=retries)


def detect_license_text(text):
    normalized = re.sub(r"\s+", " ", (text or "")).strip().lower()
    signatures = [
        ("Apache-2.0", ("apache license", "version 2.0, january 2004")),
        ("AGPL-3.0", ("gnu affero general public license", "version 3, 19 november 2007")),
        ("LGPL-3.0", ("gnu lesser general public license", "version 3, 29 june 2007")),
        ("LGPL-2.1", ("gnu lesser general public license", "version 2.1, february 1999")),
        ("GPL-3.0", ("gnu general public license", "version 3, 29 june 2007")),
        ("GPL-2.0", ("gnu general public license", "version 2, june 1991")),
        ("MPL-2.0", ("mozilla public license version 2.0",)),
        ("BSD-3-Clause", ("redistribution and use in source and binary forms", "neither the name of")),
        ("ISC", ("permission to use, copy, modify, and/or distribute this software for any purpose with or without fee",)),
        ("Unlicense", ("this is free and unencumbered software released into the public domain",)),
        ("BUSL-1.1", ("business source license 1.1",)),
        ("MIT", ("permission is hereby granted, free of charge, to any person obtaining a copy",)),
    ]
    for spdx, parts in signatures:
        if all(part in normalized for part in parts):
            return spdx
    if (
        "redistribution and use in source and binary forms" in normalized
        and "redistributions of source code must retain" in normalized
        and "redistributions in binary form must reproduce" in normalized
        and "neither the name of" not in normalized
    ):
        return "BSD-2-Clause"
    return None


def fallback_license(repo, default_branch, token=None):
    try:
        root = fetch_contents(repo, ref=default_branch, token=token)
    except Exception:
        return None
    if not isinstance(root, list):
        return None
    candidates = []
    for item in root:
        if not isinstance(item, dict) or item.get("type") != "file":
            continue
        name = str(item.get("name", "")).lower()
        stem = re.split(r"[._-]", name, maxsplit=1)[0]
        if stem in LICENSE_NAMES:
            candidates.append(item)
    candidates.sort(key=lambda item: (0 if str(item.get("name","")).lower().startswith(("license","licence")) else 1, str(item.get("name","")).lower()))
    for item in candidates[:4]:
        path = item.get("path")
        if not path:
            continue
        try:
            payload = fetch_contents(repo, path=path, ref=default_branch, token=token)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        encoded = payload.get("content")
        if not isinstance(encoded, str):
            continue
        try:
            text = base64.b64decode(encoded, validate=False).decode("utf-8", errors="replace")
        except Exception:
            continue
        detected = detect_license_text(text)
        if detected:
            return detected
    return None


def metadata(raw):
    out = {}
    for target, source in FIELDS.items():
        if target == "license":
            lic = raw.get("license")
            out[target] = lic.get("spdx_id") if isinstance(lic, dict) else None
        else:
            out[target] = raw.get(source)
    return out


def refresh_primary_language(repo, raw):
    current=repo.get("languages")
    if not isinstance(current,list) or not current or all(str(value).strip().lower()=="unknown" for value in current):
        language=raw.get("language")
        if isinstance(language,str) and language.strip():
            repo["languages"]=[language.strip().lower()]

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
            raw = fetch(name, token)
            fresh = metadata(raw)
            if fresh.get("license") in (None, "", "NOASSERTION"):
                detected = fallback_license(name, raw.get("default_branch"), token)
                if detected:
                    fresh["license"] = detected
                else:
                    current_github = r.get("github")
                    current_license = current_github.get("license") if isinstance(current_github, dict) else None
                    if current_license not in (None, "", "NOASSERTION"):
                        fresh["license"] = current_license
            refresh_primary_language(r, raw)
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
