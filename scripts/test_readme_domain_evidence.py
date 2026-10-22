#!/usr/bin/env python3
"""Offline evidence-integrity and relevance regressions for immutable README hints."""
import json
import re
import subprocess
import sys
from pathlib import Path

from catalog_domain_evidence import (
    advisory_domain_evidence, reviewed_readme_source, reviewed_readme_task_terms
)
from portfolio_daily import recommendations, review_blockers
from recommend import infer_domains, tokens
from report_domain_coverage import analyze

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
repos = catalog["repositories"]
by_repo = {r["repo"]: r for r in repos}
manifest = json.loads((ROOT / "catalog-readme-evidence.json").read_text(encoding="utf-8"))
sources = manifest["sources"]
assert manifest["schemaVersion"] == 1 and manifest["sourceType"] == "reviewed-readme-blob"
assert len(sources) >= 25
assert len(set(x["repository"] for x in sources)) == len(sources)
allowed = {
    "ai_media", "ai_agents", "data_ml", "graphics", "game_dev", "marketing",
    "software_engineering", "writing", "productivity", "backend", "web_frontend",
    "embedded_iot", "education", "cybersecurity", "ai_memory", "devops",
}
for entry in sources:
    name = entry["repository"]
    assert name in by_repo, name
    row = by_repo[name]
    assert row["domain"] == "other", name
    assert entry["githubRepositoryId"] == row["githubRepositoryId"]
    assert re.fullmatch(r"[a-f0-9]{40}", entry["blobSha"]), name
    assert entry["path"] == "README.md"
    assert len(entry["evidenceSnippet"]) >= 3
    assert len(entry["evidenceSnippet"]) <= 250
    assert entry["reviewNotes"] and len(entry["reviewNotes"]) < 260
    assert set(entry["advisoryDomains"]) <= allowed
    assert len(entry["advisoryDomains"]) <= 4
    assert len(entry["taskTerms"]) <= 10
    assert all(re.fullmatch(r"[a-z0-9-]+", term) for term in entry["taskTerms"]), name
    ev = advisory_domain_evidence(row)
    assert set(entry["advisoryDomains"]) <= ev.keys(), name
    assert all("readme:README.md@" + entry["blobSha"] in ev[d]
               for d in entry["advisoryDomains"])
    assert reviewed_readme_source(row) == entry
    assert reviewed_readme_task_terms(row) == entry["taskTerms"]
    wrong_id = {**row, "githubRepositoryId": row["githubRepositoryId"] + 1000000}
    assert reviewed_readme_source(wrong_id) is None
    assert reviewed_readme_task_terms(wrong_id) == []
    curated = {**row, "domain": "game_dev"}
    assert reviewed_readme_source(curated) is None
    assert advisory_domain_evidence(curated) == {"game_dev": ["catalog-domain"]}

report = analyze(catalog)
assert report["catalogRepositories"] == len(repos)
assert report["reviewedReadmeSources"] == len(sources)
assert report["advisoryRouted"] + report["unresolvedAdvisoryDomain"] == report["genericDomainRepositories"]
assert report["advisoryRouted"] >= 145
assert len(report["unrouted"]) >= 1  # Never invent a domain to reach 100% classification.
assert all("readmeEvidence" not in row for row in report["unrouted"])
for row in report["routed"]:
    if "readmeEvidence" not in row:
        continue
    ref = row["readmeEvidence"]
    assert ref["url"] == (
        "https://api.github.com/repos/" + row["repo"]
        + "/git/blobs/" + ref["blobSha"]
    )
    assert "reviewNotes" in ref and "snapshotCapturedOn" in ref
    assert row["automaticIntegrationApproved"] is False

# Grounded examples: targeted routes derived from upstream README snapshots.
cases = [
    ("hexgrad/kokoro", "ai_media", "tts speech voice audio"),
    ("Asad-Ismail/MoneyPrinterTurbo-Extended", "ai_media",
     "video subtitles tts voice clips"),
    ("mcncarl/jianying-headless", "ai_media", "video editing drafts subtitles export mp4"),
    ("neilsonnn/image-blaster", "graphics", "3d models meshes assets environments"),
    ("alexngdev99/rork-restaurant-tycoon", "game_dev",
     "game tycoon simulation react"),
    ("withmarbleapp/os-taxonomy", "education",
     "curriculum education learning teaching"),
    ("GoogleCloudPlatform/genmedia-izumi-agent", "marketing",
     "multimedia advertising marketing"),
]
for name,domain,query in cases:
    tool = by_repo[name]
    assert domain in advisory_domain_evidence(tool), name
    project = {"full_name": "dbrckk/target-test", "name": "target-test"}
    profile = {"domains":[domain],"terms":tokens(query),"language":"python",
               "dependencies":"","overview":""}
    assessment = {}
    picks = recommendations(project, profile, [tool], None, assessment)
    assert len(assessment) == 1
    if not picks:
        raise AssertionError((name, domain, query, assessment))
    picked = picks[0]
    assert picked["repository"] == name
    assert picked["mode"] == "domain-review"
    assert picked["integrationEligible"] is False
    assert "inferred-domain-needs-confirmation" in picked["policyReview"]
    assert any(x.startswith("readme:README.md@") for x in picked["domainEvidence"][domain])
    assert assessment[name]["integrationEligible"] is False

# A source with conflicting identity or unsupported domain must not inherit
# the vetted README instructions / routing.
for fake in [
    {"repo": "unknown/fake", "domain": "other", "githubRepositoryId": 123,
     "bestFor": ["AI agent app"], "capabilities": ["automation"]},
    {"repo": "hexgrad/kokoro", "domain": "other", "githubRepositoryId": 999999,
     "bestFor": [], "capabilities": []},
]:
    assert reviewed_readme_source(fake) is None
    assert reviewed_readme_task_terms(fake) == []

# CLI ranking works with a new task domain without mutating catalog.
args = [sys.executable, str(ROOT / "scripts/recommend.py"),
        "curriculum education learning", "--domain", "education", "--top", "2500", "--json"]
payload = json.loads(subprocess.check_output(args,cwd=ROOT,text=True))
assert payload["diagnostics"]["eligible"] == len(repos)
record = next(row for row in payload["recommendations"] if row["repo"] == "withmarbleapp/os-taxonomy")
assert "education" in record["advisoryDomains"]
assert record["automaticIntegrationApproved"] is False
assert "inferred-domain-needs-confirmation" in record["domainReviewGates"]

# Real safeguards remain independent of source evidence.
unsafe = {**by_repo["hexgrad/kokoro"],
          "github": {**by_repo["hexgrad/kokoro"]["github"], "license": None}}
assert "license-not-approved" in review_blockers(unsafe)
print("OK: %d reviewed README blobs; %d/%d 'other' sources get advisory domains; no automatic integration approval."
      % (len(sources), report["advisoryRouted"], report["genericDomainRepositories"]))
