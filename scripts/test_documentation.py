#!/usr/bin/env python3
"""Keep the public v1 documentation aligned with the executable pipeline."""
import importlib.util
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
SCORING=ROOT/"docs"/"DISCOVERY_SCORING.md"

assert README.exists(), "README.md is required"
assert SCORING.exists(), "docs/DISCOVERY_SCORING.md is required"

readme=README.read_text()
scoring=SCORING.read_text()

for text in (
    "python scripts/validate_catalog.py",
    "python scripts/recommend.py",
    "python scripts/test_pipeline_integration.py",
    "Refresh GitHub metadata",
    "docs/DISCOVERY_SCORING.md",
    "RECOMMENDER.md",
):
    assert text in readme, f"README missing {text!r}"

# Local Markdown links from README must point to repository files/directories.
for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",readme):
    if target.startswith(("http://","https://","#")):
        continue
    local=target.split("#",1)[0]
    if local:
        assert (ROOT/local).exists(), f"README has broken local link: {target}"

spec=importlib.util.spec_from_file_location("evaluation",ROOT/"scripts"/"evaluate_candidates.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
assert f"`{mod.ACCEPT_THRESHOLD:g}`" in scoring, "accept threshold documentation is stale"
assert f"`{mod.REVIEW_THRESHOLD:g}`" in scoring, "review threshold documentation is stale"

for component in ("fit","activity","adoption","maturity","maintenance"):
    assert f"`{component}`" in scoring, f"missing score component {component}"
for confidence in ("high","medium","low"):
    assert f"`{confidence}`" in scoring, f"missing confidence level {confidence}"
assert "low-confidence-cap" in scoring
assert "discoveryScore" in scoring
assert "evaluationScore" in scoring

print("OK: documentation contract tests passed")
