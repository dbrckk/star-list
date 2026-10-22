#!/usr/bin/env python3
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_catalog_quality.py"
spec = importlib.util.spec_from_file_location("audit_catalog_quality", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = datetime(2026, 9, 21, tzinfo=timezone.utc)
repos = [
    {
        "repo": "x/healthy",
        "githubRepositoryId": 101,
        "tier": "recommended",
        "lifecycle": "active",
        "selfHosted": True,
        "bestFor": ["api"],
        "avoidWhen": ["mobile"],
        "alternatives": [],
        "complements": [],
        "github": {
            "archived": False,
            "disabled": False,
            "license": "MIT",
            "pushedAt": "2026-09-01T00:00:00Z",
        },
    },
    {
        "repo": "x/stale",
        "tier": "specialized",
        "selfHosted": "unknown",
        "licenseEvidence": "no-root-license-file",
        "github": {
            "archived": False,
            "disabled": False,
            "license": "NOASSERTION",
            "pushedAt": "2023-01-01T00:00:00Z",
        },
    },
    {
        "repo": "x/stable",
        "tier": "recommended",
        "lifecycle": "stable",
        "selfHosted": True,
        "github": {
            "archived": False,
            "disabled": False,
            "license": "MIT",
            "pushedAt": "2023-01-01T00:00:00Z",
        },
    },
    {
        "repo": "x/reference",
        "tier": "specialized",
        "lifecycle": "reference",
        "selfHosted": True,
        "github": {
            "archived": False,
            "disabled": False,
            "license": "MIT",
            "pushedAt": "2023-01-01T00:00:00Z",
        },
    },
    {
        "repo": "x/legacy-archive",
        "tier": "indexed",
        "lifecycle": "legacy",
        "selfHosted": False,
        "github": {
            "archived": True,
            "disabled": False,
            "license": None,
            "pushedAt": "2020-01-01T00:00:00Z",
        },
    },
    {
        "repo": "x/audit-stale",
        "tier": "indexed",
        "selfHosted": True,
        "github": {
            "archived": False,
            "disabled": False,
            "license": "MIT",
            "pushedAt": "2023-01-01T00:00:00Z",
        },
    },
    {"repo": "x/missing", "tier": "indexed", "selfHosted": True},
    {"repo":"x/custom","tier":"specialized","selfHosted":True,"licenseStatus":"custom-restrictive","github":{"archived":False,"disabled":False,"license":None,"pushedAt":"2026-09-01T00:00:00Z"}},
    {"repo":"x/partial","tier":"indexed","selfHosted":True,"licenseStatus":"partial","github":{"archived":False,"disabled":False,"license":None,"pushedAt":"2026-09-01T00:00:00Z"}},
    {"repo":"x/external","tier":"indexed","selfHosted":True,"licenseStatus":"external-terms","github":{"archived":False,"disabled":False,"license":None,"pushedAt":"2026-09-01T00:00:00Z"}},
    {"repo":"x/notfound","tier":"specialized","selfHosted":True,"licenseStatus":"not-found","github":{"archived":False,"disabled":False,"license":None,"pushedAt":"2026-09-01T00:00:00Z"}},
]

report = mod.analyze(repos, stale_days=730, now=now)
assert report["repositories"] == 11
assert report["summary"]["review"] == 2
assert report["summary"]["byCode"]["stale-over-threshold"] == 1
assert report["summary"]["byCode"]["stale-stable"] == 1
assert report["summary"]["byCode"]["stale-reference"] == 1
assert report["summary"]["byCode"]["archived-legacy-retained"] == 1
assert report["summary"]["byCode"]["stale-indexed-retained"] == 1
assert report["summary"]["byCode"]["missing-github-metadata"] == 1
assert report["summary"]["byCode"]["license-unknown"] == 1
assert report["summary"]["byCode"]["license-file-missing"] == 1
assert report["summary"]["byCode"]["self-hosting-uncertain"] == 1
assert report["summary"]["byCode"]["license-custom-restrictive"] == 1
assert report["summary"]["byCode"]["license-partial"] == 1
assert report["summary"]["byCode"]["license-external-terms"] == 1
assert report["summary"]["byCode"]["license-not-found"] == 1
assert report["guidanceCoverage"]["bestFor"] == {"populated": 1, "missing": 10}
assert report["identityCoverage"] == {"verified": 1, "missing": 10}
assert sum(report["identityCoverage"].values()) == report["repositories"]
markdown = mod.render_markdown(report)
assert "<!-- star-list-catalog-quality -->" in markdown
assert "x/stable" in markdown
assert "x/legacy-archive" in markdown
assert "Review required" in markdown
assert "Verified permanent GitHub IDs: **1/11**" in markdown
assert "Name-only or unverified entries: **10**" in markdown
# Large collections must not exceed the GitHub issue-body limit: full
# structured evidence remains available from the workflow artifact.
oversized = {**report, "findings": report["findings"] * 1000}
oversized_markdown = mod.render_markdown(oversized)
assert len(oversized_markdown.encode("utf-8")) <= 60_000
assert "display truncated" in oversized_markdown
assert "<!-- star-list-catalog-quality -->" in oversized_markdown
assert "x/stale" in oversized_markdown
print("OK: catalog quality audit tests passed")
