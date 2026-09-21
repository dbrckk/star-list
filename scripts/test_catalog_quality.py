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
        "selfHosted": "unknown",
        "github": {
            "archived": False,
            "disabled": False,
            "license": "NOASSERTION",
            "pushedAt": "2023-01-01T00:00:00Z",
        },
    },
    {
        "repo": "x/archived",
        "selfHosted": False,
        "github": {
            "archived": True,
            "disabled": False,
            "license": None,
            "pushedAt": "2020-01-01T00:00:00Z",
        },
    },
    {"repo": "x/missing", "selfHosted": True},
]

report = mod.analyze(repos, stale_days=730, now=now)
assert report["repositories"] == 4
assert report["summary"]["review"] == 3
assert report["summary"]["byCode"]["stale-over-threshold"] == 1
assert report["summary"]["byCode"]["archived"] == 1
assert report["summary"]["byCode"]["missing-github-metadata"] == 1
assert report["summary"]["byCode"]["license-unknown"] == 2
assert report["summary"]["byCode"]["self-hosting-uncertain"] == 1
assert report["guidanceCoverage"]["bestFor"] == {"populated": 1, "missing": 3}
markdown = mod.render_markdown(report)
assert "<!-- star-list-catalog-quality -->" in markdown
assert "x/stale" in markdown
assert "Review required" in markdown
print("OK: catalog quality audit tests passed")
