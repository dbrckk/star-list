#!/usr/bin/env python3
"""Offline regression: improve indexed source discovery without auto-authorization."""
import json
from pathlib import Path

from catalog_domain_evidence import advisory_domain_evidence
from portfolio_daily import recommendations, review_blockers
from recommend import score_repo, tokens

ROOT = Path(__file__).resolve().parents[1]
repos = json.loads((ROOT / "catalog.json").read_text())["repositories"]
by_name = {r["repo"]: r for r in repos}

assert advisory_domain_evidence({
    "tier": "indexed", "domain": "other", "capabilities": ["video-generation"]
}) == {"ai_media": ["capability:video-generation"]}
assert advisory_domain_evidence({
    "tier": "indexed", "domain": "other",
    "capabilities": ["automation", "tool", "ai", "web"], "bestFor": ["AI app agent automation"]
}) == {}
assert advisory_domain_evidence({
    "tier": "indexed", "domain": "other", "capabilities": [],
    "bestFor": ["Music generation toolkit"]
}) == {"ai_media": ["description:music generation"]}
assert advisory_domain_evidence({
    "tier": "recommended", "domain": "backend", "capabilities": ["video-generation"]
}) == {"backend": ["catalog-domain"]}

# Real GitHub metadata: identify unambiguous sources without rewriting catalog.
other = [r for r in repos if r["tier"] == "indexed" and r.get("domain") == "other"]
routed = [r for r in other if advisory_domain_evidence(r)]
assert len(routed) >= 20, len(routed)
for name, domain in (
    ("ace-step/ACE-Step-1.5", "ai_media"),
    ("krillinai/OpenCreator", "ai_media"),
    ("tursodatabase/libsql", "backend"),
):
    assert name in by_name
    assert by_name[name]["domain"] == "other"
    assert domain in advisory_domain_evidence(by_name[name])

def project(domain, query, language="python"):
    return {"full_name": "dbrckk/target-app", "name": "target-app"}, {
        "domains": [domain], "terms": tokens(query), "language": language,
        "dependencies": "", "overview": "real software project",
    }

for domain, query, required in (
    ("ai_media", "video editing voice music generation animation tts video production", "krillinai/OpenCreator"),
    ("backend", "database persistence sql orm backend", "tursodatabase/libsql"),
):
    target, profile = project(domain, query)
    decisions = {}
    suggestions = recommendations(target, profile, repos, None, decisions)
    assert len(decisions) == len(repos), "All indexed and curated sources get a disposition"
    matched = {s["repository"]: s for s in suggestions}
    assert required in matched, (domain, required)
    picked = matched[required]
    assert picked["mode"] == "domain-review"
    assert picked["integrationEligible"] is False
    assert "inferred-domain-needs-confirmation" in picked["policyReview"]
    assert domain in picked["domainEvidence"]
    assert decisions[required]["integrationEligible"] is False
    assert decisions[required]["reason"] == "domain-review"
    ranking_query = [
        __import__("sys").executable, str(ROOT / "scripts/recommend.py"),
        query, "--top", "3000", "--json",
    ]
    import subprocess
    ranking = json.loads(subprocess.check_output(ranking_query, text=True, cwd=ROOT))
    ranked = next(row for row in ranking["recommendations"] if row["repo"] == required)
    assert ranked["reviewRequired"] is True
    assert "inferred-domain-needs-confirmation" in ranked["domainReviewGates"]


# Playwright MCP was formerly an unclassified indexed source; it is now
# explicitly curated as a software-engineering browser-testing MCP adapter.
# This must NOT weaken the inference regression above or authorize native
# application dependency installation.
browser_mcp = by_name["microsoft/playwright-mcp"]
assert browser_mcp["tier"] == "specialized"
assert browser_mcp["domain"] == "software_engineering"
assert browser_mcp["guidanceSource"] == "curated"
target, profile = project(
    "software_engineering", "playwright browser automation web testing", "typescript"
)
decisions = {}
suggestions = recommendations(target, profile, repos, None, decisions)
matched = {row["repository"]: row for row in suggestions}
assert "microsoft/playwright-mcp" in matched
assert matched["microsoft/playwright-mcp"]["mode"] == "adapter-review"
assert matched["microsoft/playwright-mcp"]["integrationEligible"] is False
assert decisions["microsoft/playwright-mcp"]["integrationEligible"] is False


# No weak/reused topic labels become grounds for autonomous execution.
unsafe = {
    "repo": "example/generic-agent", "domain": "other", "tier": "indexed",
    "capabilities": ["automation"], "bestFor": ["AI agent app"],
    "score": 10, "github": {"license": "MIT", "archived": False},
    "languages": ["python"], "costModel": "open-source",
    "integrationComplexity": "low",
}
assert not advisory_domain_evidence(unsafe)
target, profile = project("ai_agents", "mcp agent automation")
assert recommendations(target, profile, [unsafe]) == []

# All original review blockers still apply when evidence is strong.
flagged = {
    **by_name["tursodatabase/libsql"],
    "github": {**by_name["tursodatabase/libsql"]["github"], "license": None},
}
assert "license-not-approved" in review_blockers(flagged)
target, profile = project("backend", "database persistence sql orm backend", "rust")
matches = recommendations(target, profile, [flagged])
assert all(not row["integrationEligible"] for row in matches)

print(f"OK: {len(routed)}/{len(other)} generic-domain indexed repositories gain evidence-backed advisory routing; all auto-integration gates preserved.")
