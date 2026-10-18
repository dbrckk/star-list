#!/usr/bin/env python3
"""Validate curated website references without treating them as GitHub repos.

This is a catalog/data integrity gate. It makes no network calls and grants
no license or authorization to copy code from the listed websites.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from validate_json_contract import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "web-resources.json"
SCHEMA = ROOT / "schemas" / "web-resources.schema.json"


def canonical_url(value):
    if not isinstance(value, str) or value != value.strip():
        raise ValueError("website URL must be a trimmed string")
    parts = urlsplit(value)
    if (parts.scheme != "https" or not parts.hostname or parts.username
            or parts.password or parts.port not in (None, 443)
            or parts.query or parts.fragment
            or not re.fullmatch(r"[a-z0-9.-]+", parts.hostname)
            or ".." in parts.hostname or parts.hostname.startswith(".")
            or parts.hostname.endswith(".")
            or not re.fullmatch(r"/[a-zA-Z0-9/_-]*", parts.path or "/")):
        raise ValueError("website URL must be a plain HTTPS location without credentials or query")
    host = parts.hostname.lower().removeprefix("www.")
    return host + (parts.path.rstrip("/") or "/")


def check(data, schema):
    errors = list(validate(data, schema))
    if errors:
        return errors
    ids = set()
    urls = set()
    for item in data["resources"]:
        name = item["id"]
        if name in ids:
            errors.append(f"duplicate website resource ID: {name}")
        ids.add(name)
        seen_aliases = set()
        for url in [item["url"], *item["aliases"]]:
            try:
                key = canonical_url(url)
            except (ValueError, TypeError) as exc:
                errors.append(f"{name}: {exc}")
                continue
            if key in seen_aliases:
                errors.append(f"{name}: canonical/alias duplicate {key}")
            seen_aliases.add(key)
            if key in urls:
                errors.append(f"{name}: URL is used by another resource: {key}")
            urls.add(key)
        if item["usagePolicy"] == "reference-only" and item["autoIntegrate"] is not False:
            errors.append(f"{name}: reference sites cannot auto-integrate")
    return errors


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = check(data, schema)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {len(data['resources'])} web resources validated; no automatic integration allowed")


if __name__ == "__main__":
    main()
