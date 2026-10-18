#!/usr/bin/env python3
"""Validate and search curated non-GitHub website resources (stdlib only)."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "web-resources.json"
KINDS = {"prompt-library", "design-gallery", "motion-gallery", "component-library", "web-3d-engine", "shader-gallery", "app-builder"}
POLICIES = {"reference-only", "per-item-license", "verify-upstream-license", "service-terms"}
DOMAINS = {"web_frontend", "graphics", "software_engineering"}


def validate(data):
    errors = []
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        return ["schemaVersion must be 1"]
    resources = data.get("resources")
    if not isinstance(resources, list) or not resources:
        return ["resources must be a non-empty list"]
    ids, urls = set(), set()
    for index, item in enumerate(resources):
        prefix = f"resources[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append(f"{prefix}: invalid id")
        elif identifier in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(identifier)
        url = item.get("url")
        if not isinstance(url, str):
            errors.append(f"{prefix}: url must be a string")
        else:
            parsed = urlsplit(url)
            if (parsed.scheme != "https" or not parsed.hostname or parsed.username
                    or parsed.password or parsed.port or parsed.query or parsed.fragment
                    or parsed.path not in ("", "/") or parsed.hostname.lower() in {"localhost", "127.0.0.1"}):
                errors.append(f"{prefix}: url must be a canonical public HTTPS origin")
            key = (parsed.hostname or "").lower().removeprefix("www.")
            if key in urls:
                errors.append(f"{prefix}: duplicate domain")
            urls.add(key)
        if item.get("kind") not in KINDS:
            errors.append(f"{prefix}: invalid kind")
        if item.get("domain") not in DOMAINS:
            errors.append(f"{prefix}: invalid domain")
        if item.get("usagePolicy") not in POLICIES:
            errors.append(f"{prefix}: invalid usagePolicy")
        if item.get("verification") not in {"pending", "verified"}:
            errors.append(f"{prefix}: invalid verification")
        if item.get("source") != "user-supplied-screenshot":
            errors.append(f"{prefix}: missing source provenance")
        if not isinstance(item.get("tags"), list) or not item["tags"] or any(not isinstance(t, str) or not t.strip() for t in item["tags"]):
            errors.append(f"{prefix}: tags must be nonempty strings")
        for field in ("name", "description", "licenseNote", "addedOn"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}: missing {field}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Search name, tags and description")
    parser.add_argument("--domain", choices=sorted(DOMAINS))
    parser.add_argument("--kind", choices=sorted(KINDS))
    parser.add_argument("--json", action="store_true", help="Print matched website resources as JSON")
    args = parser.parse_args()
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    query = args.query.casefold().strip()
    matches = [r for r in data["resources"]
               if (not args.domain or r["domain"] == args.domain)
               and (not args.kind or r["kind"] == args.kind)
               and (not query or query in " ".join([r["name"], r["description"], *r["tags"]]).casefold())]
    if args.json:
        print(json.dumps({"resources": matches, "count": len(matches)}, indent=2, ensure_ascii=False))
    else:
        print(f"OK: {len(data['resources'])} valid websites | {len(matches)} matching")
        for r in matches:
            print(f"- {r['name']}: {r['url']} [{r['kind']}; {r['usagePolicy']}; {r['verification']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
