#!/usr/bin/env python3
"""Keep the public v1 documentation aligned with the executable pipeline."""
import importlib.util
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
SCORING=ROOT/"docs"/"DISCOVERY_SCORING.md"
VERSION=ROOT/"VERSION"
CHANGELOG=ROOT/"CHANGELOG.md"

assert README.exists(), "README.md is required"
assert SCORING.exists(), "docs/DISCOVERY_SCORING.md is required"
assert VERSION.exists(), "VERSION is required for stable releases"
assert CHANGELOG.exists(), "CHANGELOG.md is required for stable releases"

readme=README.read_text()
scoring=SCORING.read_text()
version=VERSION.read_text().strip()
changelog=CHANGELOG.read_text()

assert re.fullmatch(r"\d+\.\d+\.\d+",version), f"invalid semantic version: {version!r}"
assert version=="1.0.0", f"expected v1 release version 1.0.0, got {version!r}"
assert f"## {version} - 2026-09-16" in changelog, "CHANGELOG missing current release entry"
assert "CHANGELOG.md" in readme, "README must link the changelog"
assert "WEB_RESOURCES.md" in readme and "websites.json" in readme, "README must advertise curated website references"
website_guide = (ROOT / "WEB_RESOURCES.md").read_text()
websites = __import__("json").loads((ROOT / "websites.json").read_text())
assert len(websites["websites"]) >= 11
assert any(site["id"] == "skill-issue" for site in websites["websites"])
assert all(site["url"] in website_guide for site in websites["websites"])
assert "--websites" in (ROOT / "RECOMMENDER.md").read_text()
assert "website_references" in (ROOT / "scripts/portfolio_daily.py").read_text()
assert "validate_websites.py" in (ROOT / ".github/workflows/validate.yml").read_text()
assert f"Current stable release: **{version}**" in readme, "README stable release marker is stale"

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

# The hourly Stars job pushes with GITHUB_TOKEN; GitHub deliberately
# suppresses a second workflow's normal push trigger for that commit.
# Keep the qualified reusable audit dependency wired to the actual push.
sync_yaml = (ROOT / ".github/workflows/sync-github-stars.yml").read_text()
audit_yaml = (ROOT / ".github/workflows/catalog-quality-on-change.yml").read_text()
stars_docs = (ROOT / "docs/GITHUB_STARS_SYNC.md").read_text()
assert 'id: catalog_push' in sync_yaml
assert 'catalog_changed: ${{ steps.catalog_push.outputs.catalog_changed }}' in sync_yaml
assert 'echo "catalog_changed=true" >> "$GITHUB_OUTPUT"' in sync_yaml
assert "needs.sync.outputs.catalog_changed == 'true'" in sync_yaml
assert "uses: ./.github/workflows/catalog-quality-on-change.yml" in sync_yaml
assert "  workflow_call:" in audit_yaml
assert "  schedule:" in audit_yaml and "47 3 * * *" in audit_yaml
assert "          ref: main" in audit_yaml
assert "git ls-remote --exit-code origin refs/heads/main" in audit_yaml
assert "main moved repeatedly" in audit_yaml
assert "refusing stale issue publication" in audit_yaml
assert "        if: always()" in audit_yaml
assert "GITHUB_TOKEN" in stars_docs and "reusable workflow" in stars_docs
identity_yaml = (ROOT / ".github/workflows/backfill-github-ids.yml").read_text()
identity_code = (ROOT / "scripts/backfill_github_ids.py").read_text()
assert "python scripts/backfill_github_ids.py --write" in identity_yaml
assert "schemas/github-id-backfill-report.schema.json" in identity_yaml
assert "needs.backfill.outputs.catalog_changed == 'true'" in identity_yaml
assert "uses: ./.github/workflows/catalog-quality-on-change.yml" in identity_yaml
assert "git rebase origin/main" in identity_yaml and "git push origin HEAD:main" in identity_yaml
assert "from sync_github_stars import SAFE_GITHUB_HTTP" in identity_code
assert "not isinstance(actual, str) or actual.casefold() != repo.casefold()" in identity_code
skills_workflow = (ROOT / ".github/workflows/audit-agent-skill-sources.yml").read_text()
skills_validator = (ROOT / "scripts/audit_agent_skill_sources.py").read_text()
assert "python scripts/audit_agent_skill_sources.py --online" in skills_workflow
assert "        if: always()" in skills_workflow
assert "if [[ \"$COMPLETE\" != true ]]" in skills_workflow
assert "agent-skill-source-audit.schema.json" in skills_workflow
assert "class RejectRedirect(HTTPRedirectHandler)" in skills_validator
assert "sourceContentReviewed" in skills_validator and "automaticInstallation" in skills_validator
maintenance_yaml = (ROOT / ".github/workflows/refresh-metadata.yml").read_text()
assert "  quality-after-refresh:" in maintenance_yaml
assert "    needs: refresh" in maintenance_yaml
assert "    uses: ./.github/workflows/catalog-quality-on-change.yml" in maintenance_yaml
assert "git rebase origin/main" in maintenance_yaml
assert "git push origin HEAD:main" in maintenance_yaml
assert "      - name: Publish catalog quality audit" not in maintenance_yaml
skills_docs = (ROOT / "AGENT_SKILLS.md").read_text()
skills_catalog = (ROOT / "agent-skills.json").read_text()
skills_scanner = (ROOT / "scripts/agent_skill_discovery.py").read_text()
portfolio_scanner = (ROOT / "scripts/portfolio_daily.py").read_text()
portfolio_yaml = (ROOT / ".github/workflows/daily-portfolio-integration.yml").read_text()
assert "https://skill-issue.in/" in skills_docs and '"schemaVersion": 1' in skills_catalog
assert "automaticInstallation" in skills_scanner
assert "row[\"skill_discovery\"]" in portfolio_scanner
assert '"agent-skills.json"' in portfolio_yaml
assert "AGENT_SKILLS.md" in readme and "--skills" in readme

print("OK: documentation contract tests passed")
