#!/usr/bin/env python3
"""Audit website catalog URL identity and source usage without network access.

The schema checks structure. This adds security and deduplication rules that
JSON Schema cannot express; neither stage authorizes copying third-party code.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from validate_json_contract import validate

ROOT = Path(__file__).resolve().parents[1]


def canonical_url(value):
    if not isinstance(value, str) or value != value.strip():
        raise ValueError("invalid untrimmed website URL")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.port not in (None, 443)
            or not re.fullmatch(r"[a-z0-9.-]+", parsed.hostname)
            or parsed.hostname.startswith(".") or parsed.hostname.endswith(".")
            or ".." in parsed.hostname
            or not re.fullmatch(r"/[a-zA-Z0-9/_-]*", parsed.path or "/")):
        raise ValueError("website URL must be a plain HTTPS address without credentials or query")
    return parsed.hostname.lower().removeprefix("www.") + (parsed.path.rstrip("/") or "/")


def check_websites(data, schema):
    errors = list(validate(data, schema))
    if errors:
        return errors
    ids = set()
    owner_by_url = {}
    for site in data["websites"]:
        identity = site["id"]
        if identity in ids:
            errors.append(f"duplicate website ID: {identity}")
        ids.add(identity)
        # 'originalUrl' records an old URL or user-supplied alternate link.
        # Each such alias must remain attached
        # to the same entry, not silently create an extra website identity.
        for url in [site["url"], *([site["originalUrl"]] if site.get("originalUrl") else [])]:
            try:
                normalized = canonical_url(url)
            except (ValueError, TypeError) as exc:
                errors.append(f"{identity}: {exc}")
                continue
            prior = owner_by_url.get(normalized)
            if prior is not None and prior != identity:
                errors.append(f"{identity}: URL collides with {prior}: {normalized}")
            owner_by_url[normalized] = identity
        # Always-review declarations must not escape a website\'s stated domain.
        baseline = set(site.get("portfolioBaselineDomains", []))
        if baseline - set(site["domains"]):
            errors.append(f"{identity}: baseline domains must be included in website domains")
        # Specialist triggers must be explicit canonical labels, not prose.
        required_signals = site.get("portfolioRequiredSignals", [])
        if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", signal)
               for signal in required_signals):
            errors.append(f"{identity}: invalid specialist project-fit token")
        # Converted HF weights inherit upstream usage restrictions. The
        # 'other' hub tag is unknown permission, never an approval to install
        # or use images commercially; checkpoint provenance is mandatory.
        if site["type"] == "model-checkpoint":
            if (site.get("reuse") != "licensed-material"
                    or not site.get("upstreamModel")
                    or not site.get("sourceLicenseTag")):
                errors.append(f"{identity}: model checkpoint requires reviewed licence and upstream provenance")
            if site.get("portfolioBaselineDomains"):
                errors.append(f"{identity}: model checkpoint cannot be a blanket domain recommendation")
            if not site.get("portfolioRequiredSignals"):
                errors.append(f"{identity}: model checkpoint requires task-specific project signals")
        # An MCP endpoint is an authenticated remote service, not a harmless
        # website link. Require a bounded HTTPS /mcp URL owned by the
        # documented provider; no credentials, foreign hosts or auto-install.
        endpoint = site.get("mcpEndpoint")
        is_mcp = site["type"] == "mcp-service"
        if is_mcp and not endpoint:
            errors.append(f"{identity}: MCP service is missing mcpEndpoint")
        if endpoint is not None and not is_mcp:
            errors.append(f"{identity}: only MCP services may declare mcpEndpoint")
        if endpoint is not None:
            try:
                canonical_url(endpoint)
                service = urlsplit(endpoint)
                website = urlsplit(site["url"])
                host = service.hostname.lower()
                root = website.hostname.lower().removeprefix("www.")
                if (service.path != "/mcp" or
                        not (host == root or host.endswith("." + root))):
                    errors.append(f"{identity}: MCP endpoint must be /mcp on a provider-owned subdomain")
            except (ValueError, TypeError, AttributeError) as exc:
                errors.append(f"{identity}: invalid MCP endpoint: {exc}")
        if site["reuse"] not in {
            "reference-only", "license-per-item", "licensed-material",
            "open-source-upstream", "hosted-service",
        }:
            errors.append(f"{identity}: unsupported source reuse policy")
    return errors


def main():
    data = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/websites.schema.json").read_text(encoding="utf-8"))
    errors = check_websites(data, schema)
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {len(data['websites'])} unique website identities with restricted reuse")


if __name__ == "__main__":
    main()
