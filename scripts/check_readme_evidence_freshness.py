#!/usr/bin/env python3
"""Read-only freshness check for manually reviewed GitHub README blob evidence.

A changed README requires a new review; it never authorizes automatic changes
to a catalog or target repository.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

import refresh_github_metadata as gh

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog-readme-evidence.json"


def inspect(record, fetch_repo=gh.fetch, fetch_contents=gh.fetch_contents, token=None):
    name = record["repository"]
    entry = {"repo": name, "recordedBlobSha": record["blobSha"],
             "currentBlobSha": None, "status": "unknown"}
    try:
        info = fetch_repo(name, token=token)
        if not isinstance(info, dict) or info.get("id") != record["githubRepositoryId"]:
            entry["status"] = "repository-identity-changed"
            return entry
        payload = fetch_contents(name, path=record["path"], token=token)
        sha = payload.get("sha") if isinstance(payload, dict) else None
        if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{40}", sha):
            entry["status"] = "readme-unavailable"
            return entry
        entry["currentBlobSha"] = sha
        entry["status"] = "unchanged" if sha == record["blobSha"] else "review-outdated"
    except Exception as exc:
        entry["status"] = "api-error"
        entry["error"] = str(exc)[:240]
    return entry


def check(sources, batch_size=12, batch_index=0, fetch_repo=gh.fetch,
          fetch_contents=gh.fetch_contents, token=None):
    if batch_size < 1 or batch_size > 40:
        raise ValueError("batch-size must be in 1..40")
    size = (len(sources) + batch_size - 1) // batch_size
    if batch_index < 0 or batch_index >= max(1, size):
        raise ValueError("invalid batch-index")
    start = batch_index * batch_size
    selected = sources[start:start + batch_size]
    findings = [inspect(x, fetch_repo, fetch_contents, token) for x in selected]
    counts = {k: sum(x["status"] == k for x in findings)
              for k in ("unchanged", "review-outdated", "repository-identity-changed",
                        "readme-unavailable", "api-error")}
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "totalSources": len(sources),
        "batchSize": batch_size,
        "batchIndex": batch_index,
        "inspected": len(findings),
        "counts": counts,
        "findings": findings,
        "catalogOrIntegrationChanged": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--batch-index", type=int, default=0)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    try:
        result = check(data["sources"], batch_size=args.batch_size,
                       batch_index=args.batch_index, token=os.environ.get("GITHUB_TOKEN"))
    except ValueError as exc:
        parser.error(str(exc))
    encoded = json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    print(encoded,end="")
    return 1 if result["counts"]["api-error"] else 0


if __name__=="__main__":
    sys.exit(main())
