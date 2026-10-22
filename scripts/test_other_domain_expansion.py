#!/usr/bin/env python3
"""Regression tests for broad yet conservative advisory classification."""
import json
from pathlib import Path

from catalog_domain_evidence import advisory_domain_evidence
from portfolio_daily import recommendations, review_blockers
from recommend import infer_domains, tokens
from report_domain_coverage import analyze

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
rows = catalog["repositories"]
lookup = {r["repo"]: r for r in rows}
report = analyze(catalog)

assert report["catalogRepositories"] == len(rows)
assert report["genericDomainRepositories"] == sum(r.get("domain") == "other" for r in rows)
assert report["advisoryRouted"] >= 100, report["advisoryRouted"]
assert report["advisoryRouted"] + report["unresolvedAdvisoryDomain"] == report["genericDomainRepositories"]
assert all(row["discoveryAvailable"] for row in report["routed"] + report["unrouted"])
assert all(row["automaticIntegrationApproved"] is False
           for row in report["routed"] + report["unrouted"])
assert report["domainCounts"]["embedded_iot"] >= 30
assert report["domainCounts"]["ai_media"] >= 20

# Explicit high-quality labels and descriptions. Never rewrite original domain.
for name, expected in (
    ("espressif/arduino-esp32", "embedded_iot"),
    ("espressif/esp32-camera", "embedded_iot"),
    ("anthropics/claude-agent-sdk-python", "ai_agents"),
    ("FFmpeg/FFmpeg", "ai_media"),
    ("audacity/audacity", "ai_media"),
    ("openai/whisper", "ai_media"),
    ("frappe/erpnext", "productivity"),
    ("TheCraigHewitt/seomachine", "marketing"),
    ("shiyu-coder/Kronos", "trading"),
    ("OpenBMB/MiniCPM-V", "data_ml"),
):
    row = lookup[name]
    assert row["domain"] == "other"
    evidence = advisory_domain_evidence(row)
    assert expected in evidence, (name, evidence)
    assert all(signal.startswith(("capability:", "description:", "repo-name:"))
               for signals in evidence.values() for signal in signals)

# Ambiguous metadata must never gain a domain merely to increase the metric.
for row in (
    {"domain": "other", "repo": "any/some-tool", "capabilities": ["ai", "agent", "automation"],
     "bestFor": ["AI agent automation tool"]},
    {"domain": "other", "repo": "any/random-project", "capabilities": [],
     "bestFor": ["manual source review before reuse"]},
    {"domain": "other", "repo": "any/guestbook", "capabilities": [],
     "bestFor": ["simple web based demo"]},
):
    assert advisory_domain_evidence(row) == {}, row

assert "embedded_iot" in infer_domains(tokens("esp32 firmware arduino"))
assert "ai_agents" not in infer_domains(tokens("AI ESP32 camera"))
assert "embedded_iot" in infer_domains(tokens("AI ESP32 camera"))
assert "embedded_iot" not in infer_domains(tokens("Godot gameplay shaders"))

# An inferred domain can be suggested to a compatible task but never silently
# authorize a third-party integration. The existing trust boundary must hold.
project = {"full_name": "dbrckk/esp32-project", "name": "esp32-project"}
profile = {
    "domains": ["embedded_iot"], "terms": tokens(
        "esp32 esp-idf arduino microcontroller embedded firmware driver camera"
    ),
    "language": "c++", "dependencies": "", "overview": "",
}
decision_trace = {}
suggestions = recommendations(project, profile, rows, None, decision_trace)
assert len(decision_trace) == len(rows)
by_suggestion = {r["repository"]: r for r in suggestions}
for name in ("espressif/arduino-esp32", "espressif/esp32-camera"):
    assert name in by_suggestion, name
    row = by_suggestion[name]
    assert row["mode"] == "domain-review"
    assert row["integrationEligible"] is False
    assert "inferred-domain-needs-confirmation" in row["policyReview"]
    assert "embedded_iot" in row["domainEvidence"]
    assert decision_trace[name]["integrationEligible"] is False

# Real inactive or unresolved sources continue to carry source-specific guards.
unsafe = dict(lookup["espressif/arduino-esp32"])
unsafe["github"] = {**unsafe["github"], "license": None, "archived": True}
assert "license-not-approved" in review_blockers(unsafe)
assert "github-inactive" in review_blockers(unsafe)

print("OK: wider advisory domains, full coverage, negative examples and non-dispatch safety verified "
      f"({report['advisoryRouted']}/{report['genericDomainRepositories']} other sources).")
