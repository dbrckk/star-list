#!/usr/bin/env python3
"""Catalog-wide availability contract: no audit tier / no silent admission queue."""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from portfolio_daily import eligible, recommendations, review_blockers, website_references_for_project
from recommend import tokens

catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["repositories"]
websites = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))["websites"]
names = [entry["repo"].lower() for entry in catalog]
assert len(set(names)) == len(catalog), "every source must retain a unique catalog identity"
counts = Counter(entry["tier"] for entry in catalog)
assert not counts.get("audit"), "legacy audit admission tier must be empty"
assert set(counts).issubset({"core", "recommended", "specialized", "indexed"})
assert counts["indexed"] > 0, "automatic Star admission should keep uncurated sources discoverable"

# An indexed source is never blocked *just* because it has not been hand-curated.
clean = {
    "repo": "test/indexed", "tier": "indexed", "score": 9,
    "integrationComplexity": "medium", "costModel": "open-source",
    "lifecycle": "active",
    "github": {"archived": False, "disabled": False, "license": "MIT"},
}
assert not review_blockers(clean)
assert eligible(clean)
assert "tier-not-approved" not in review_blockers(clean)
unsafe = {**clean, "github": {**clean["github"], "license": None}}
assert not eligible(unsafe), "unknown upstream licensing cannot automatically authorize installation"
assert "license-not-approved" in review_blockers(unsafe)

query = [
    sys.executable, str(ROOT / "scripts/recommend.py"),
    "AI video animation Android automation", "--top", "3000",
    "--websites", "--rank-all-websites", "--top-websites", "200", "--json",
]
payload = json.loads(subprocess.check_output(query, cwd=ROOT, text=True))
assert payload["diagnostics"]["catalogSize"] == len(catalog)
assert payload["diagnostics"]["eligible"] == len(catalog)
assert payload["diagnostics"]["returned"] == len(catalog)
recs = payload["recommendations"]
assert {r["repo"].lower() for r in recs} == set(names)
assert all(r["availableForDiscovery"] is True for r in recs)
assert all(r["automaticIntegrationApproved"] is False for r in recs)
assert "indexed" in {r["tier"] for r in recs}
assert all("indexed-unverified" not in r["rankingReviewGates"] for r in recs)
assert len(payload["websiteRecommendations"]) == len(websites)
assert all(site["integrationEligible"] is False for site in payload["websiteRecommendations"])

project = {"full_name": "dbrckk/Moneyprinterturbo_perso", "name": "Moneyprinterturbo_perso",
           "description": "YouTube video automation"}
profile = {"domains": ["ai_media", "productivity"],
           "terms": tokens("video AI animation audio narration speech video editing automation"),
           "language": "python", "dependencies": "", "overview": "AI video production"}
assessed = {}
site_assessed = {}
matches = recommendations(project, profile, catalog, None, assessed)
references = website_references_for_project(project, profile, None, site_assessed)
assert set(assessed) == {entry["repo"] for entry in catalog}
assert set(site_assessed) == {site["id"] for site in websites}
assert all(decision["decision"] in {"matched", "not-relevant"} for decision in assessed.values())
assert matches is not None and references is not None
print(
    "OK: full catalog is immediately available: "
    f"{len(catalog)} GitHub repositories, {counts['indexed']} indexed (0 audit); "
    f"{len(websites)} websites; {len(assessed)} project decisions."
)
