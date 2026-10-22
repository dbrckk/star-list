#!/usr/bin/env python3
"""Inspect evidence-backed advisory domain coverage without mutating catalog."""
import argparse
from collections import Counter
import json
from pathlib import Path

from catalog_domain_evidence import advisory_domain_evidence

ROOT = Path(__file__).resolve().parents[1]


def analyze(catalog):
    repositories = catalog["repositories"]
    rows = [r for r in repositories if r.get("domain") == "other"]
    matched, unmatched = [], []
    domains = Counter()
    for row in rows:
        evidence = advisory_domain_evidence(row)
        if evidence:
            domains.update(evidence.keys())
            matched.append({
                "repo": row["repo"],
                "advisoryDomains": sorted(evidence),
                "domainEvidence": evidence,
                "discoveryAvailable": True,
                "automaticIntegrationApproved": False,
            })
        else:
            unmatched.append({"repo": row["repo"],
                              "reason": "no-unambiguous-task-evidence",
                              "discoveryAvailable": True,
                              "automaticIntegrationApproved": False})
    return {
        "schemaVersion": 1,
        "catalogRepositories": len(repositories),
        "genericDomainRepositories": len(rows),
        "advisoryRouted": len(matched),
        "unresolvedAdvisoryDomain": len(unmatched),
        "domainCounts": dict(sorted(domains.items())),
        "routed": matched,
        "unrouted": unmatched,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = analyze(json.loads(args.catalog.read_text(encoding="utf-8")))
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
