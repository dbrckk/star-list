This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*.{py,js,mjs,cjs,ts,tsx,jsx,java,kt,kts,gd,groovy,gradle,toml,json,yaml,yml,sql,sh}, README.md, AGENTS.md, PROJECT_*.md
- Files matching these patterns are excluded: .ai/**, **/node_modules/**, **/.gradle/**, **/build/**, **/dist/**, **/.venv/**, **/__pycache__/**, **/.pytest_cache/**, **/.git/**, **/coverage/**, **/*.lock, **/*.min.js, **/*.map, assets/**, art/**, art_sources/**, marketing/**, colab/**, kaggle/**, discovery-cache.json, health-snapshot.json, history.json
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
````
.github/
  workflows/
    ai-repo-map.yml
    audit-agent-skill-sources.yml
    backfill-github-ids.yml
    catalog-quality-on-change.yml
    daily-portfolio-integration.yml
    license-backfill.yml
    metadata-evidence-review.yml
    portfolio-failure-diagnostics.yml
    portfolio-scan-smoke.yml
    production-os-review-handoff.yml
    readme-evidence-freshness.yml
    refresh-metadata.yml
    semantic-refresh.yml
    sync-github-stars.yml
    validate.yml
.serena/
  project.yml
schemas/
  agent-skill-source-audit.schema.json
  cache-health-history.schema.json
  cache-health-trend.schema.json
  cache-health.schema.json
  catalog-quality.schema.json
  catalog-stats.schema.json
  coverage-report.schema.json
  discovery-cache.schema.json
  discovery-candidates.schema.json
  discovery-evaluated.schema.json
  discovery-memory.schema.json
  discovery-watchlist.schema.json
  github-id-backfill-report.schema.json
  health-drift.schema.json
  health-snapshot.schema.json
  health-trends.schema.json
  history.schema.json
  metadata-evidence.schema.json
  readme-domain-evidence.schema.json
  replacement-report.schema.json
  star-sync-report.schema.json
  websites.schema.json
scripts/
  admit_github_stars.py
  agent_skill_discovery.py
  analyze_cache_health.py
  analyze_coverage.py
  audit_agent_skill_sources.py
  audit_catalog_quality.py
  backfill_github_ids.py
  backfill_licenses.py
  build_discovery_watchlist.py
  catalog_domain_evidence.py
  catalog_stats.py
  check_readme_evidence_freshness.py
  detect_health_drift.py
  discover_candidates.py
  evaluate_candidates.py
  filter_discovery_memory.py
  find_replacements.py
  health_score.py
  infer_selection_guidance.py
  portfolio_daily.py
  portfolio_failure_diagnostics.py
  recommend.py
  refresh_github_metadata.py
  render_discovery_issue.py
  render_health_issue.py
  report_domain_coverage.py
  star_import_pipeline.py
  sync_github_stars.py
  test_analyze_coverage.py
  test_auto_stars_admission.py
  test_backfill_licenses.py
  test_cache_health_history.py
  test_cache_health.py
  test_catalog_domain_evidence.py
  test_catalog_quality.py
  test_degraded_inputs.py
  test_discover_candidates.py
  test_discovery_cache_stats.py
  test_discovery_cache.py
  test_discovery_memory.py
  test_discovery_watchlist.py
  test_documentation.py
  test_evaluate_candidates.py
  test_find_replacements.py
  test_full_catalog_availability.py
  test_health_drift.py
  test_health_score.py
  test_history.py
  test_json_contracts.py
  test_other_domain_expansion.py
  test_pipeline_integration.py
  test_readme_domain_evidence.py
  test_readme_evidence_freshness.py
  test_recommend.py
  test_refresh_github_metadata.py
  test_render_discovery_issue.py
  test_render_health_issue.py
  test_selection_guidance.py
  test_star_import_pipeline.py
  test_sync_github_stars.py
  test_verify_catalog_evidence.py
  update_cache_health_history.py
  update_history.py
  validate_catalog.py
  validate_json_contract.py
  validate_websites.py
  verify_catalog_evidence.py
.repo-standards.yml
agent-skills.json
AGENTS.md
catalog-readme-evidence.json
catalog.schema.json
README.md
stacks.json
websites.json
````

# Files

## File: .github/workflows/ai-repo-map.yml
````yaml
name: Repository standards

on:
  push:
    branches: [main]
    paths-ignore:
      - ".ai/**"
  workflow_dispatch:

permissions:
  contents: write
  actions: read

concurrency:
  group: repo-standards-${{ github.repository }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  repository-standards:
    uses: dbrckk/repo-standards/.github/workflows/reusable-unified.yml@main
````

## File: .github/workflows/audit-agent-skill-sources.yml
````yaml
name: Audit pinned Skill Issue sources

on:
  schedule:
    - cron: '23 5 * * *'
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - 'agent-skills.json'
      - 'scripts/agent_skill_discovery.py'
      - 'scripts/audit_agent_skill_sources.py'
      - '.github/workflows/audit-agent-skill-sources.yml'

permissions:
  contents: read
  issues: write

concurrency:
  group: star-list-agent-skill-source-audit
  cancel-in-progress: false

jobs:
  audit:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
        with:
          ref: main
          persist-credentials: false
      - uses: actions/setup-python@v7
        with:
          python-version: '3.12'
      - name: Verify pinned SKILL.md source metadata only
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/audit_agent_skill_sources.py --online \
            --json-output agent-skill-source-audit.json \
            --markdown-output agent-skill-source-audit.md
          python scripts/validate_json_contract.py \
            schemas/agent-skill-source-audit.schema.json agent-skill-source-audit.json
      - name: Preserve audit evidence even when upstream verification fails
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pinned-agent-skill-source-audit
          path: |
            agent-skill-source-audit.json
            agent-skill-source-audit.md
          if-no-files-found: warn
          retention-days: 14
      - name: Maintain actionable broken-source review issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
        shell: bash
        run: |
          set -euo pipefail
          # Incomplete API scans fail before this step. Never publish a false
          # clean result after GitHub rate-limiting or transient failures.
          read -r COMPLETE FINDINGS < <(python - <<'PY'
          import json
          d = json.load(open("agent-skill-source-audit.json", encoding="utf-8"))
          print(str(d["coverageComplete"]).lower(), d["findings"])
          PY
          )
          if [[ "$COMPLETE" != true ]]; then
            echo "::error::Incomplete source verification; refusing issue update"
            exit 1
          fi
          existing="$(gh issue list --state open --limit 100 --json number,body \
            --jq '[.[] | select(.body != null and (.body | contains("<!-- star-list-agent-skill-source-audit -->")))] | .[0].number // empty')"
          if [[ "$FINDINGS" == 0 ]]; then
            if [[ -n "$existing" ]]; then
              gh issue close "$existing" --comment "All pinned agent skill source files are accessible again."
            fi
          elif [[ -n "$existing" ]]; then
            gh issue edit "$existing" --title "Review broken pinned Skill Issue source links ($FINDINGS)" \
              --body-file agent-skill-source-audit.md
          else
            gh issue create --title "Review broken pinned Skill Issue source links ($FINDINGS)" \
              --body-file agent-skill-source-audit.md
          fi
````

## File: .github/workflows/backfill-github-ids.yml
````yaml
name: Backfill permanent GitHub repository IDs

on:
  schedule:
    - cron: '06 4 * * 2'
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - 'scripts/backfill_github_ids.py'
      - '.github/workflows/backfill-github-ids.yml'

permissions:
  contents: write

concurrency:
  group: star-list-github-identity-backfill
  cancel-in-progress: false

jobs:
  backfill:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    outputs:
      catalog_changed: ${{ steps.catalog_push.outputs.catalog_changed }}
    steps:
      - uses: actions/checkout@v7
        with:
          ref: main
      - uses: actions/setup-python@v7
        with:
          python-version: '3.12'
      - name: Resolve missing stable GitHub IDs with verified repository metadata
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/backfill_github_ids.py --write \
            --max-requests 250 --report-json github-id-backfill-report.json
          python scripts/validate_catalog.py
          python scripts/validate_json_contract.py catalog.schema.json catalog.json
          python scripts/validate_json_contract.py \
            schemas/github-id-backfill-report.schema.json github-id-backfill-report.json
      - name: Preserve reconciliation evidence on success or failure
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: permanent-github-id-backfill
          path: github-id-backfill-report.json
          if-no-files-found: warn
          retention-days: 14
      - name: Publish only a validated non-force catalog update
        id: catalog_push
        shell: bash
        run: |
          set -euo pipefail
          if git diff --quiet -- catalog.json; then
            echo "No permanent GitHub IDs to update"
            echo "catalog_changed=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add catalog.json
          git commit -m "chore: reconcile missing permanent GitHub repository IDs"
          for attempt in 1 2 3 4; do
            git fetch origin main
            # A conflict is a visible failure, never a reason to overwrite
            # concurrent Stars admissions or identity changes.
            git rebase origin/main
            python scripts/validate_catalog.py
            python scripts/validate_json_contract.py catalog.schema.json catalog.json
            if git push origin HEAD:main; then
              echo "catalog_changed=true" >> "$GITHUB_OUTPUT"
              exit 0
            fi
            sleep "$attempt"
          done
          echo "::error::Could not publish validated catalog after four attempts"
          exit 1

  audit-after-backfill:
    needs: backfill
    if: needs.backfill.outputs.catalog_changed == 'true'
    permissions:
      contents: read
      issues: write
    uses: ./.github/workflows/catalog-quality-on-change.yml
````

## File: .github/workflows/catalog-quality-on-change.yml
````yaml
name: Refresh catalog quality on catalog changes

on:
  # Fallback reconciliation covers missed/cancelled bot-triggered audits.
  schedule:
    - cron: '47 3 * * *'
  push:
    branches: [main]
    paths:
      - 'catalog.json'
      - '.github/workflows/catalog-quality-on-change.yml'
  workflow_dispatch:
  workflow_call:

permissions:
  contents: read
  issues: write

concurrency:
  group: star-list-catalog-quality-publication
  cancel-in-progress: false

jobs:
  audit:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
        with:
          # Reusable calls run on the Star-sync event SHA, which predates its
          # own catalog push. Always audit the newly committed default branch.
          ref: main
          persist-credentials: false
      - uses: actions/setup-python@v7
        with:
          python-version: '3.12'
      - name: Audit the actual current catalog
        run: |
          python scripts/audit_catalog_quality.py --markdown-output catalog-quality.md > catalog-quality.json
          python scripts/validate_json_contract.py schemas/catalog-quality.schema.json catalog-quality.json
          python - <<'PY'
          import json
          from pathlib import Path
          catalog = json.loads(Path('catalog.json').read_text(encoding='utf-8'))
          audit = json.loads(Path('catalog-quality.json').read_text(encoding='utf-8'))
          markdown = Path('catalog-quality.md').read_text(encoding='utf-8')
          assert audit['repositories'] == len(catalog['repositories'])
          assert sum(audit['identityCoverage'].values()) == audit['repositories']
          assert 'Verified permanent GitHub IDs:' in markdown
          assert '<!-- star-list-catalog-quality -->' in markdown
          assert f"Repositories: **{audit['repositories']}**" in markdown
          PY
      - name: Reconcile concurrent changes before creating the audit artifact
        shell: bash
        run: |
          set -euo pipefail
          for attempt in 1 2 3; do
            checked_sha="$(git rev-parse HEAD)"
            remote_sha="$(git ls-remote --exit-code origin refs/heads/main | awk '{print $1}')"
            if [[ "$checked_sha" == "$remote_sha" ]]; then
              echo "Validated audit matches current main: $checked_sha"
              exit 0
            fi
            echo "main advanced during the audit; recomputing on the latest catalog ($attempt/3)"
            git fetch --depth=1 origin main
            git -c advice.detachedHead=false checkout --detach FETCH_HEAD
            python scripts/audit_catalog_quality.py --markdown-output catalog-quality.md > catalog-quality.json
            python scripts/validate_json_contract.py schemas/catalog-quality.schema.json catalog-quality.json
          done
          checked_sha="$(git rev-parse HEAD)"
          remote_sha="$(git ls-remote --exit-code origin refs/heads/main | awk '{print $1}')"
          if [[ "$checked_sha" != "$remote_sha" ]]; then
            echo "::error::main moved repeatedly; keeping audit artifact and refusing stale publication"
            exit 1
          fi
      - name: Preserve current audit evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: catalog-quality-on-change
          if-no-files-found: warn
          path: |
            catalog-quality.json
            catalog-quality.md
          retention-days: 14
      - name: Update catalog-quality review issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
        shell: bash
        run: |
          set -euo pipefail
          # An additional change after artifact creation must not overwrite
          # the live issue with an older catalog snapshot. A later bot-triggered
          # or daily scheduled audit will reconcile if this race occurs.
          checked_sha="$(git rev-parse HEAD)"
          remote_sha="$(git ls-remote --exit-code origin refs/heads/main | awk '{print $1}')"
          if [[ "$checked_sha" != "$remote_sha" ]]; then
            echo "::error::Catalog changed after audit; refusing stale issue publication"
            exit 1
          fi
          read -r REVIEW INFO TOTAL < <(python - <<'PY'
          import json
          summary = json.load(open('catalog-quality.json', encoding='utf-8'))['summary']
          print(summary['review'], summary['info'], summary['findings'])
          PY
          )
          existing="$(gh issue list --state open --limit 100 --json number,body \
            --jq '[.[] | select(.body != null and (.body | contains("<!-- star-list-catalog-quality -->")))] | .[0].number // empty')"
          if [ "$TOTAL" = '0' ]; then
            if [ -n "$existing" ]; then
              gh issue close "$existing" --comment 'Current catalog quality audit has no findings.'
            fi
          elif [ -n "$existing" ]; then
            gh issue edit "$existing" --title "Catalog quality: $REVIEW review / $INFO info" \
              --body-file catalog-quality.md
          else
            gh issue create --title "Catalog quality: $REVIEW review / $INFO info" \
              --body-file catalog-quality.md
          fi
````

## File: .github/workflows/daily-portfolio-integration.yml
````yaml
name: Daily portfolio star-list integration

on:
  schedule:
    - cron: "37 3 * * *"
  workflow_dispatch:
  # GitHub may omit a scheduled workflow; use the already-qualified star
  # synchronization schedule as a second, trusted entrypoint.
  workflow_run:
    workflows: ["Sync GitHub Stars"]
    types: [completed]
  push:
    branches: [main]
    paths:
      - "scripts/portfolio_daily.py"
      - "scripts/agent_skill_discovery.py"
      - "agent-skills.json"
      - "websites.json"
      - ".github/workflows/daily-portfolio-integration.yml"

permissions:
  contents: read
  issues: write

concurrency:
  group: star-list-portfolio-daily
  cancel-in-progress: false

jobs:
  scan:
    # Never use secrets on a workflow_run fired from a PR or a fork.
    # Do not consume predecessor artifacts; always checkout trusted main.
    if: >-
      github.event_name != 'workflow_run' ||
      (github.event.workflow_run.conclusion == 'success' &&
       github.event.workflow_run.event == 'schedule' &&
       github.event.workflow_run.head_branch == 'main' &&
       github.event.workflow_run.head_repository.full_name == github.repository)
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      # The Stars workflow runs every hour. Its workflow_run trigger is a
      # fallback for a missed daily cron, not a request for 24 full scans.
      # A published review issue is written only after a successful scan.
      - name: Skip duplicate UTC-day scheduled scans
        id: cadence
        if: github.event_name == 'schedule' || github.event_name == 'workflow_run'
        shell: bash
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
        run: |
          set -euo pipefail
          today="$(date -u +%F)"
          report="$(gh issue list --state open --limit 100 --json number,body \
            --jq '[.[] | select(.body != null and (.body | contains("<!-- star-list-portfolio-daily -->")))] | .[0].body // ""')"
          if [[ "$report" == *"Generated (UTC): ${today}T"* ]]; then
            echo "skip_scan=true" >> "$GITHUB_OUTPUT"
            echo "Full portfolio report for ${today} UTC already published; skipping duplicate scan."
          else
            echo "skip_scan=false" >> "$GITHUB_OUTPUT"
          fi
      - uses: actions/checkout@v7
        if: steps.cadence.outputs.skip_scan != 'true'
      - uses: actions/setup-python@v7
        if: steps.cadence.outputs.skip_scan != 'true'
        with:
          python-version: "3.12"
      - name: Validate scanner syntax
        if: steps.cadence.outputs.skip_scan != 'true'
        run: python -m py_compile scripts/portfolio_daily.py
      - name: Inspect every accessible owner repository and submit qualified work
        if: steps.cadence.outputs.skip_scan != 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PRODUCTION_OS_OPERATOR_TOKEN: ${{ secrets.PRODUCTION_OS_OPERATOR_TOKEN }}
          PRODUCTION_OS_URL: https://production-os1.onrender.com
        run: |
          python scripts/portfolio_daily.py \
            --owner dbrckk \
            --output portfolio-daily.json \
            --markdown portfolio-daily.md \
            --max-dispatch 3
      - name: Preserve evidence for all scanned repositories
        if: always() && steps.cadence.outputs.skip_scan != 'true'
        uses: actions/upload-artifact@v4
        with:
          name: daily-portfolio-star-list-review
          path: |
            portfolio-daily.json
            portfolio-daily.md
          if-no-files-found: warn
          retention-days: 30
      - name: Update the persistent portfolio review issue
        # Preserve the last verified report if discovery or dispatch fails.
        # The failed run still exposes the full diagnostic artifact.
        if: success() && steps.cadence.outputs.skip_scan != 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
        shell: bash
        run: |
          set -euo pipefail
          if [ ! -s portfolio-daily.md ]; then
            echo "::error::No portfolio report available; refusing to report success"
            exit 1
          fi
          existing="$(gh issue list --state open --limit 100 --json number,body \
            --jq '[.[] | select(.body != null and (.body | contains("<!-- star-list-portfolio-daily -->")))] | .[0].number // empty')"
          if [ -n "$existing" ]; then
            gh issue edit "$existing" \
              --title "Daily star-list portfolio integration review" \
              --body-file portfolio-daily.md
          else
            gh issue create \
              --title "Daily star-list portfolio integration review" \
              --body-file portfolio-daily.md
          fi
````

## File: .github/workflows/license-backfill.yml
````yaml
name: One-shot license backfill

on:
  push:
    branches:
      - main
    paths:
      - ".github/workflows/license-backfill.yml"
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: one-shot-license-backfill
  cancel-in-progress: false

jobs:
  backfill:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Backfill unknown licenses
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/backfill_licenses.py --write
      - name: Validate catalog
        run: |
          python scripts/validate_catalog.py
          python scripts/validate_json_contract.py catalog.schema.json catalog.json
          python scripts/test_refresh_github_metadata.py
          python scripts/test_backfill_licenses.py
      - name: Commit catalog backfill
        run: |
          if git diff --quiet -- catalog.json; then
            echo "No catalog changes"
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add catalog.json
          git commit -m "chore: backfill detected repository licenses"
          git pull --rebase origin main
          git push
````

## File: .github/workflows/metadata-evidence-review.yml
````yaml
name: Review uncertain catalog metadata

on:
  schedule:
    - cron: "27 5 * * *"
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: catalog-metadata-evidence-review
  cancel-in-progress: false

jobs:
  review:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Select a bounded rotating evidence batch
        id: batch
        run: |
          python - <<'PY' >> "$GITHUB_OUTPUT"
          import datetime, json
          from pathlib import Path
          data = json.loads(Path("catalog.json").read_text(encoding="utf-8"))
          import sys
          sys.path.insert(0, "scripts")
          from verify_catalog_evidence import requires_review
          uncertain = sum(requires_review(row) for row in data["repositories"])
          batches = max(1, (uncertain + 14) // 15)
          print(f"index={datetime.date.today().toordinal() % batches}")
          PY
      - name: Verify GitHub evidence without modifying catalog
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/verify_catalog_evidence.py --limit 15 \
            --batch-index "${{ steps.batch.outputs.index }}" \
            --report-out metadata-evidence.json > /tmp/evidence-summary.json
          python scripts/validate_json_contract.py \
            schemas/metadata-evidence.schema.json metadata-evidence.json
      - name: Upload evidence report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: catalog-metadata-evidence
          path: metadata-evidence.json
          if-no-files-found: warn
          retention-days: 35
````

## File: .github/workflows/portfolio-failure-diagnostics.yml
````yaml
name: Diagnose failed star-list integrations

on:
  schedule:
    # Run after the 03:37 UTC portfolio scan; GitHub may delay schedules.
    - cron: "17 4 * * *"
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - "scripts/portfolio_failure_diagnostics.py"
      - ".github/workflows/portfolio-failure-diagnostics.yml"

permissions:
  contents: read

concurrency:
  group: star-list-failure-diagnostics
  cancel-in-progress: false

jobs:
  inspect:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Read-only operator diagnosis with strict public-field allowlist
        env:
          PRODUCTION_OS_OPERATOR_TOKEN: ${{ secrets.PRODUCTION_OS_OPERATOR_TOKEN }}
        run: |
          python -m py_compile scripts/portfolio_failure_diagnostics.py
          python scripts/portfolio_failure_diagnostics.py \
            --output portfolio-failure-diagnostics.json
      - name: Preserve sanitized public diagnostics
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: sanitized-public-portfolio-failures
          path: portfolio-failure-diagnostics.json
          if-no-files-found: warn
          retention-days: 14
````

## File: .github/workflows/portfolio-scan-smoke.yml
````yaml
name: Portfolio discovery live smoke

on:
  pull_request:
    paths:
      - "scripts/portfolio_daily.py"
      - "websites.json"
      - "agent-skills.json"
      - "scripts/agent_skill_discovery.py"
      - "scripts/validate_websites.py"
      - "scripts/recommend.py"
      - "scripts/portfolio_failure_diagnostics.py"
      - ".github/workflows/portfolio-failure-diagnostics.yml"
      - ".github/workflows/daily-portfolio-integration.yml"
      - ".github/workflows/portfolio-scan-smoke.yml"
      - "docs/DAILY_PORTFOLIO_INTEGRATION.md"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Read-only live portfolio discovery, without integration credentials
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/portfolio_daily.py \
            --owner dbrckk --max-dispatch 0 \
            --output portfolio-daily.json --markdown portfolio-daily.md
          python - <<'PY'
          import json
          from pathlib import Path
          result = json.loads(Path("portfolio-daily.json").read_text())
          assert result["summary"]["discovered"] >= 1
          assert result["summary"]["inspected"] == result["summary"]["discovered"]
          assert result["summary"]["dispatched"] == 0
          assert result["summary"]["qualifying_repositories"] == sum(
              len(row["suggestions"]) for row in result["projects"]
          )
          assert result["summary"]["policy_review_suggestions"] == sum(
              bool(item["policyReview"])
              for row in result["projects"] for item in row["suggestions"]
          )
          assert result["summary"]["catalog_repositories"] >= 1000
          catalog_names = {x["repo"] for x in json.loads(Path("catalog.json").read_text())["repositories"]}
          website_ids = {x["id"] for x in json.loads(Path("websites.json").read_text())["websites"]}
          assert len(catalog_names) == result["summary"]["catalog_repositories"]
          assert len(website_ids) == result["summary"]["catalog_websites"]
          assert "fasth3-omni-collection" in website_ids
          assert "atomicchat-flux3-image-klein-gguf" in website_ids
          assert {"hugging-face-hub", "minicpm-v-4-7-1b-heretic"} <= website_ids
          assert "sopilot" in website_ids
          assert "jialinyyzz-humanizer-12b" in website_ids
          animation_ids = {
              "sakugabooru", "shot-cafe", "posemy-art",
              "niwatoliver-costume-atlas", "youmind-video-prompts", "carat-ai-media",
          }
          assert animation_ids <= website_ids
          fully_scanned = [row for row in result["projects"]
                           if row["status"] != "skipped-inactive"]
          assert result["summary"]["fully_assessed_projects"] == len(fully_scanned)
          assert result["summary"]["repository_assessments"] == len(fully_scanned) * len(catalog_names)
          assert result["summary"]["website_assessments"] == len(fully_scanned) * len(website_ids)
          for project in fully_scanned:
              decision = project["source_assessment"]
              assert project["source_coverage"]["complete"] is True
              assert set(decision["repositories"]) == catalog_names
              assert set(decision["websites"]) == website_ids
              assert all(x["reason"] and x["decision"]
                         for group in decision.values() for x in group.values())
              for suggestion in project["suggestions"]:
                  record = decision["repositories"][suggestion["repository"]]
                  assert record["decision"] == "matched", suggestion
                  assert record["integrationEligible"] == suggestion["integrationEligible"]
              for site in project["website_references"]:
                  verified_site = decision["websites"][site["id"]]
                  assert verified_site["decision"] == "matched", site
                  assert verified_site["integrationEligible"] is False
                  assert verified_site["reviewGates"] == (
                      site["reviewGates"] or ["third-party-source-review"]
                  ), site
                  if site.get("safetyRisk") == "reduced-refusal":
                      assert "reduced-refusal-public-safety-review" in site["reviewGates"], site
                  if site.get("sourceLicenseTag") == "other":
                      assert "unverified-hub-license-tag" in site["reviewGates"], site
          tts_audit = next((row for row in result["projects"]
                            if row["repository"].lower() == "dbrckk/tts"), None)
          if tts_audit is not None and tts_audit["source_coverage"]["complete"]:
              assert tts_audit["source_assessment"]["websites"]["fasth3-omni-collection"]["decision"] != "matched"
              assert tts_audit["source_assessment"]["websites"]["atomicchat-flux3-image-klein-gguf"]["decision"] != "matched"
              assert tts_audit["source_assessment"]["websites"]["minicpm-v-4-7-1b-heretic"]["decision"] != "matched"
              assert tts_audit["source_assessment"]["websites"]["jialinyyzz-humanizer-12b"]["decision"] != "matched"
          # Scene/storyboard tools may be useful for explicitly labelled
          # video studios, but not for generic TTS or financial libraries.
          if tts_audit is not None and tts_audit["source_coverage"]["complete"]:
              for identity in animation_ids:
                  assert (tts_audit["source_assessment"]["websites"]
                          [identity]["decision"] != "matched"), identity
          movie_studio = next((row for row in result["projects"]
                               if row["repository"].lower() == "dbrckk/monteur-video"), None)
          if movie_studio is not None and movie_studio["source_coverage"]["complete"]:
              for identity in ("youmind-video-prompts", "carat-ai-media"):
                  assert movie_studio["source_assessment"]["websites"][identity]["decision"] == "matched"
                  assert any(ref["id"] == identity and ref["integrationEligible"] is False
                             for ref in movie_studio["website_references"]), identity
          # A supermarket-coupon discovery app must not be sent an
          # X auto-engagement/backlink automation service as a dependency.
          retail = next((row for row in result["projects"]
                         if row["repository"].lower() == "dbrckk/promo-alimentaire"), None)
          if retail is not None and retail["source_coverage"]["complete"]:
              assert retail["source_assessment"]["websites"]["sopilot"]["decision"] != "matched"
              assert not any(site["id"] == "sopilot"
                             for site in retail["website_references"])
              assert (retail["source_assessment"]["websites"]
                      ["jialinyyzz-humanizer-12b"]["decision"] != "matched")
          for project in fully_scanned:
              for site in project["website_references"]:
                  if site["id"] == "jialinyyzz-humanizer-12b":
                      assert site["supportedLanguages"] == ["en", "zh"], site
                      assert "factual-and-format-preservation-review" in site["reviewGates"], site
                      assert "source-and-target-language-review" in site["reviewGates"], site
                      assert site["integrationEligible"] is False
          for full_name, expected_source in (
              ("dbrckk/asset-forge", "atomicchat-flux3-image-klein-gguf"),
              ("dbrckk/monteur-video", "fasth3-omni-collection"),
          ):
              target = next((row for row in result["projects"]
                             if row["repository"].lower() == full_name), None)
              if target is not None and target["source_coverage"]["complete"]:
                  assert (target["source_assessment"]["websites"]
                          [expected_source]["decision"] == "matched"), target
                  assert any(ref["id"] == expected_source
                             for ref in target["website_references"]), target
                  if expected_source == "atomicchat-flux3-image-klein-gguf":
                      assert "unverified-hub-license-tag" in (
                          target["source_assessment"]["websites"][expected_source]["reviewGates"]
                      ), target

          native_by_project = [
              sum(item["mode"] == "native" for item in row["suggestions"])
              for row in result["projects"]
          ]
          assert result["summary"]["native_suggestions"] == sum(native_by_project)
          assert result["summary"]["with_native_suggestions"] == sum(
              count > 0 for count in native_by_project
          )
          assert result["summary"]["with_native_suggestions"] <= result["summary"]["with_suggestions"]
          assert result["summary"]["native_suggestions"] >= result["summary"]["with_native_suggestions"]
          assert result["summary"]["with_website_references"] == sum(
              bool(row["website_references"]) for row in result["projects"]
          )
          assert result["summary"]["website_references"] == sum(
              len(row["website_references"]) for row in result["projects"]
          )
          assert "Projects with website references: **" in Path("portfolio-daily.md").read_text()
          assert "All qualifying GitHub matches (uncapped artifact): **" in Path("portfolio-daily.md").read_text()
          assert result["summary"]["skill_directory_references"] == len(result["projects"])
          assert result["summary"]["with_skill_recommendations"] == sum(
              bool(row["skill_discovery"]["recommendations"]) for row in result["projects"]
          )
          assert result["summary"]["skill_recommendations"] == sum(
              len(row["skill_discovery"]["recommendations"]) for row in result["projects"]
          )
          assert "Repositories informed about Skill Issue: **" in Path("portfolio-daily.md").read_text()
          for row in result["projects"]:
              assert row["skill_discovery"]["directory"] == "https://skill-issue.in/"
              assert row["skill_discovery"]["reviewRequired"] is True
              assert len({skill["id"] for skill in row["skill_discovery"]["recommendations"]}) == len(row["skill_discovery"]["recommendations"])
              for skill in row["skill_discovery"]["recommendations"]:
                  assert skill["integrationEligible"] is False
                  assert skill["reviewRequired"] is True
                  assert skill["installCommand"] is None
                  assert skill["url"].startswith("https://github.com/")
          for row in result["projects"]:
              for website in row["website_references"]:
                  assert website["integrationEligible"] is False
                  assert website["url"].startswith("https://")
                  assert "repo" not in website
                  assert website["why"]["domains"], website
                  assert (website["why"]["tags"] or website["why"]["terms"]
                          or website["why"].get("portfolioBaselineDomains")
                          or (website["id"] in {"game-art-style", "jupiter-game-art-style"}
                              and "game_dev" in website["why"]["domains"])), website
          tts = next((row for row in result["projects"]
                      if row["repository"].lower() == "dbrckk/tts"), None)
          if tts is not None:
              assert all(site["id"] != "game-art-style"
                         for site in tts["website_references"]), tts
          jumpy = next((row for row in result["projects"]
                        if row["repository"].lower() == "dbrckk/jumpy"), None)
          if jumpy is not None and jumpy["status"] != "skipped-inactive":
              assert {"game-art-style", "jupiter-game-art-style",
                      "rosebud-ai", "ludo-ai", "modl-ai"} <= {
                  site["id"] for site in jumpy["website_references"]
              }, jumpy
          report_markdown = Path("portfolio-daily.md").read_text()
          assert ("Projects with native-mode candidates: **"
                  + str(result["summary"]["with_native_suggestions"]) + "**.") in report_markdown
          for project in result["projects"]:
              for candidate in project["suggestions"]:
                  assert candidate["integrationEligible"] == (
                      candidate["mode"] == "native"
                  ), candidate
                  assert isinstance(candidate["policyReview"], list), candidate
                  if candidate["policyReview"]:
                      assert candidate["mode"] != "native", candidate
                  if candidate["mode"] == "policy-review":
                      assert candidate["policyReview"], candidate
                  if "roblox" in project["repository"].lower():
                      assert candidate["repository"].lower() not in {"libgdx/libgdx", "godotengine/godot"}, candidate
                      if candidate["repository"].lower() == "chrrxs/robloxstudio-mcp":
                          assert candidate["mode"] == "adapter-review", candidate
                  assert not ({"and", "as", "the", "with", "et", "pour", "avec", "dans", "les", "des"} & set(candidate["shared_terms"])), candidate
                  if "roblox" in project["repository"].lower():
                      assert "godot" not in candidate["repository"].lower(), candidate
          import sys
          sys.path.insert(0, "scripts")
          from portfolio_failure_diagnostics import (
              failure_category, safe_public_failure, public_diagnostics,
              task_failure_evidence, add_deep_task_diagnostics,
              inventory_diagnostic_inbox,
          )
          assert failure_category({"summary": "Provider quota exceeded"}) == "provider-quota-or-token-budget"
          assert failure_category({"summary": "check secret text"}) == "unknown"
          from portfolio_daily import (
              is_reference_candidate, count_active_integrations,
              package_skill_signals,
              count_failed_v2_integrations, count_failed_v3_integrations,
              verified_managed_projects,
              integration_marker, recoverable_failure_targets,
              count_launches_on_utc_date, busy_integration_targets,
          )
          assert verified_managed_projects({"projects": [], "total_count": 0, "complete": True}) == []
          domains, terms = package_skill_signals(
              "package.json",
              json.dumps({"dependencies": {"react-native": "0.76.0", "expo": "*"},
                          "scripts": {"build": "use unrelated cookies tokens browser"}}),
          )
          assert domains == {"mobile"}
          assert {"react", "native", "expo"} <= terms
          assert "cookies" not in terms and "browser" not in terms
          assert package_skill_signals("README.md", '{"dependencies":{"react":"*"}}') == (set(), set())
          assert package_skill_signals("package.json", '{"dependencies":') == (set(), set())
          assert package_skill_signals(
              "package.json", '{"dependencies":{"unrelated-browser-package":"*"}}'
          ) == (set(), set())
          assert package_skill_signals(
              "package.json", '{"devDependencies":{"@playwright/test":"*"}}'
          )[0] == {"software_engineering", "web_frontend"}
          # Multi-manifest repositories retain their historical integration
          # profile while exposing verified Flutter/React skills. Untrusted
          # comments, arbitrary YAML and README strings are not SDK evidence.
          assert package_skill_signals(
              "pubspec.yaml", "dependencies:\n  flutter:\n    sdk: flutter\n"
          ) == ({"mobile"}, {"flutter", "dart", "mobile"})
          assert package_skill_signals(
              "pubspec.yaml", "dependencies:\n  example:\n    sdk: flutter\n"
          ) == (set(), set())
          assert package_skill_signals(
              "pubspec.yaml", "# dependencies:\n#   flutter:\n#     sdk: flutter\n"
          ) == (set(), set())
          from portfolio_daily import project_profile
          from agent_skill_discovery import recommend_skills, word_set
          from unittest.mock import patch as skill_patch
          hybrid_files = {
              "pyproject.toml": "[project]\nname = 'polyglot'\n",
              "package.json": json.dumps({"dependencies": {"next": "15.0.0"}}),
              "pubspec.yaml": "dependencies:\n  flutter:\n    sdk: flutter\n",
          }
          manifest_reads = []
          def fake_file_text(repo, filename, token, *, limit=5500):
              assert repo == "dbrckk/polyglot"
              manifest_reads.append(filename)
              return hybrid_files.get(filename, "")
          hybrid = {
              "full_name": "dbrckk/polyglot", "name": "polyglot",
              "language": "GDScript", "description": "", "topics": [],
          }
          with skill_patch("portfolio_daily.file_text", side_effect=fake_file_text):
              hybrid_profile = project_profile(hybrid, "")
          assert hybrid_profile["dependencies"].strip() == hybrid_files["pyproject.toml"].strip()
          # The main scorer may use exact, already-reviewed framework evidence
          # from secondary manifests without treating arbitrary manifest scripts
          # or README words as a new project domain.
          assert {"web_frontend", "mobile", "game_dev"} <= set(hybrid_profile["domains"])
          assert {"nextjs", "flutter", "godot"} <= hybrid_profile["terms"]
          assert manifest_reads.count("package.json") == 1
          assert manifest_reads.count("pubspec.yaml") == 1
          # Flutter-only manifests are already probed before the fallback
          # skill loop; a negative package.json lookup must not be repeated.
          flutter_reads = []
          def flutter_file_text(repo, filename, token, *, limit=5500):
              flutter_reads.append(filename)
              return hybrid_files["pubspec.yaml"] if filename == "pubspec.yaml" else ""
          with skill_patch("portfolio_daily.file_text", side_effect=flutter_file_text):
              flutter_profile = project_profile({
                  **hybrid, "name": "flutter-app", "language": "Dart",
              }, "")
          assert flutter_reads.count("package.json") == 1
          assert flutter_reads.count("pubspec.yaml") == 1
          assert {"mobile"} <= set(flutter_profile["skill_domains"])
          assert "mobile" in flutter_profile["domains"]
          assert {"flutter", "dart"} <= flutter_profile["terms"]
          assert {"web_frontend", "mobile", "game_dev"} <= set(hybrid_profile["skill_domains"])
          assert {"nextjs", "flutter", "dart", "godot", "gdscript"} <= set(hybrid_profile["skill_terms"])
          with skill_patch("portfolio_daily.file_text", side_effect=fake_file_text):
              luau_profile = project_profile({**hybrid, "language": "Luau"}, "")
              lua_profile = project_profile({**hybrid, "language": "Lua"}, "")
          assert "luau" in luau_profile["skill_terms"]
          assert "game_dev" in luau_profile["skill_domains"]
          assert "game_dev" in luau_profile["domains"]
          assert "luau" in luau_profile["terms"]
          assert "luau" not in lua_profile["skill_terms"]
          assert "game_dev" not in lua_profile["skill_domains"]
          assert "game_dev" not in lua_profile["domains"]
          roblox_matched = recommend_skills(
              set(luau_profile["skill_terms"]), set(luau_profile["skill_domains"]),
              language="Luau", limit=20,
          )
          assert any(row["id"] == "roblox-luau-development" and
                     row["sourcePath"] == "SKILL.md" for row in roblox_matched)
          assert any(row["id"] == "android-play-policy-insights" for row in
                     recommend_skills(word_set("android play policy"), {"mobile"},
                                      language="Kotlin", limit=20))
          assert any(row["id"] == "android-compose-performance" for row in
                     recommend_skills(word_set("jetpack compose"), {"mobile"},
                                      language="Kotlin", limit=20))
          assert not any(row["id"] == "android-compose-performance" for row in
                         recommend_skills(word_set("android mobile"), {"mobile"},
                                          language="Kotlin", limit=20))
          matched = recommend_skills(
              set(hybrid_profile["skill_terms"]), set(hybrid_profile["skill_domains"]),
              language="GDScript", limit=20,
          )
          assert any(row["id"] == "godot-gdscript" for row in matched)
          flutter_matches = recommend_skills(
              word_set("flutter dart responsive mobile"), {"mobile"},
              language="Dart", limit=20,
          )
          assert {"flutter-responsive-layout", "flutter-layout-diagnostics"} <= {
              row["id"] for row in flutter_matches
          }
          assert not any(row["id"].startswith("flutter-") for row in
                         recommend_skills(word_set("flutter mobile"), {"mobile"},
                                          language="Kotlin", limit=20))
          assert all(row["reviewRequired"] and row["integrationEligible"] is False
                     and row["installCommand"] is None for row in matched + flutter_matches)
          # Functional transport smoke: an ambiguous mutating request is sent
          # once; a read-only GET retains the bounded retry policy.
          import portfolio_daily as portfolio_transport
          from urllib.error import URLError
          from unittest.mock import patch as transport_patch
          class UnavailableTransport:
              def __init__(self):
                  self.calls = 0
              def open(self, request, timeout):
                  self.calls += 1
                  raise URLError("simulated transient outage")
          for method, expected_calls in (("POST", 1), ("GET", 3)):
              transport = UnavailableTransport()
              with transport_patch.object(portfolio_transport, "SAFE_HTTP", transport), \
                   transport_patch.object(portfolio_transport.time, "sleep", return_value=None):
                  try:
                      portfolio_transport.request_json(
                          "https://production-os1.onrender.com/v1/dashboard/launch",
                          "dummy", method=method,
                          data={"request_id": "offline-smoke"} if method == "POST" else None,
                      )
                  except RuntimeError:
                      pass
                  else:
                      raise AssertionError("A failed transport was accepted")
              assert transport.calls == expected_calls, (method, transport.calls)
          test_failure = {
              "repository": "dbrckk/Ai-trading", "status": "NEEDS_ATTENTION",
              "final_goal": "Private instruction. Tracking: " +
                  "starlist-integration-v2-" + "a" * 24,
              "project_id": "sensitive-id",
              "outcome": {"summary": "Provider quota exhausted. secret=private",
                          "commit_shas": [], "pull_request": None, "ci": None,
                          "workflow_status": "failed", "validation_status": "failed"},
              "runtime": {"phase": "needs_attention", "task_status": "failed",
                          "worker_id": "sensitive-worker"},
          }
          safe = safe_public_failure(test_failure)
          assert safe["target"] == "dbrckk/ai-trading"
          assert safe["tracking_version"] == "v2"
          assert safe["failure_category"] == "provider-quota-or-token-budget"
          assert not ({"project_id", "final_goal", "summary", "worker_id"} & set(safe))
          report = public_diagnostics({
              "schema_version": "production-os/production-inbox/v1",
              "summary": {"matching": 2},
              "items": [test_failure, {
                  **test_failure, "repository": "private/secret",
                  "outcome": {"summary": "secret=DO_NOT_LEAK"},
              }],
          })
          assert report["observed_public_v2_targets"] == 1
          assert report["coverage_complete"] is False
          assert "DO_NOT_LEAK" not in json.dumps(report)
          assert "sensitive-worker" not in json.dumps(report)
          # The fast Production-OS tracking index stays private; only four
          # allowlisted public target rows may reach the sanitized output.
          tracking_index = {
              "complete": True, "total_count": 2, "projects": [
                  {"repository": "dbrckk/Ai-trading",
                   "status": "NEEDS_ATTENTION",
                   "final_goal": test_failure["final_goal"],
                   "project_id": "a" * 32},
                  {"repository": "private/secret",
                   "status": "NEEDS_ATTENTION",
                   "final_goal": test_failure["final_goal"],
                   "project_id": "b" * 32},
              ],
          }
          transformed = inventory_diagnostic_inbox(tracking_index)
          assert transformed["summary"]["matching"] == 2
          safe_fast = public_diagnostics(transformed)
          assert safe_fast["observed_public_v2_targets"] == 1
          assert "private/secret" not in json.dumps(safe_fast)
          for malformed in (
              {},
              {**tracking_index, "complete": False},
              {**tracking_index, "total_count": 1},
              {**tracking_index, "projects": [
                  {k: v for k, v in tracking_index["projects"][0].items()
                   if k != "project_id"}]},
          ):
              try:
                  inventory_diagnostic_inbox(malformed)
              except RuntimeError:
                  pass
              else:
                  raise AssertionError("Incomplete privileged index was accepted")
          evidence = task_failure_evidence({
              "current_workflow": {"tasks": [{
                  "status": "failed", "attempts": 3, "max_attempts": 3,
                  "result": {"error": "provider rate limit 429: secret=hidden",
                             "evidence": {"next_stage": "inference"}},
              }]}
          })
          assert evidence["details_checked"] is True
          assert evidence["failed_task_count"] == 1
          assert evidence["task_attempts"] == 3
          assert evidence["task_max_attempts"] == 3
          assert evidence["retry_budget_exhausted"] is True
          assert evidence["failure_category"] == "provider-quota-or-token-budget"
          assert evidence["result_fields_present"] == ["error", "evidence"]
          capacity = task_failure_evidence({
              "current_workflow": {"tasks": [{
                  "status": "failed", "attempts": 1, "max_attempts": 3,
                  "result": {"ai_dev_server_status": "capacity_exhausted",
                             "evidence": {"pipeline_status": "capacity_exhausted",
                                          "message": "private diagnostic"}}
              }]}
          })
          assert capacity["failure_category"] == "worker-capacity-exhausted"
          assert capacity["retry_budget_exhausted"] is False
          assert capacity["worker_result_status"] == "capacity_exhausted"
          assert capacity["pipeline_status"] == "capacity_exhausted"
          assert capacity["evidence_fields_present"] == ["message", "pipeline_status"]
          # Missing/empty/nonterminal workflow tasks must not be certified
          # as fully diagnosed, even when the project itself needs attention.
          for sparse in ({}, {"current_workflow": {}},
                         {"current_workflow": {"tasks": []}},
                         {"current_workflow": {"tasks": [{"status": "running"}]}}):
              assert task_failure_evidence(sparse)["details_checked"] is False
          assert "private diagnostic" not in json.dumps(capacity)
          from unittest.mock import patch as diagnostic_patch
          import portfolio_failure_diagnostics as failure_diagnostics
          public_record = {**test_failure, "project_id": "a" * 32,
                           "outcome": {}}
          diagnostic_inbox = {
              "schema_version": "production-os/production-inbox/v1",
              "summary": {"matching": 1}, "items": [public_record],
          }
          synthetic_detail = {"project": {
              "repository": public_record["repository"],
              "status": "NEEDS_ATTENTION",
              "final_goal": public_record["final_goal"],
              "current_workflow": {"tasks": [{
                  "status": "failed", "attempts": 2, "max_attempts": 2,
                  "result": {"message": "connection timed out; secret=hidden"},
              }]},
          }}
          with diagnostic_patch.object(failure_diagnostics, "request_json",
                                       return_value=synthetic_detail):
              deep = add_deep_task_diagnostics(
                  public_diagnostics(diagnostic_inbox), diagnostic_inbox, "dummy")
          assert deep["details_checked_v2"] == 1
          assert deep["details_complete"] is False  # 3 others not returned
          assert deep["failures"][0]["failure_category"] == "network-or-timeout"
          assert deep["failures"][0]["retry_budget_exhausted"] is True
          assert deep["failures"][0]["task_attempts"] == 2
          assert deep["failures"][0]["task_max_attempts"] == 2
          assert deep["failures"][0]["worker_result_status"] == "unknown"
          assert "hidden" not in json.dumps(deep)
          assert "project_id" not in json.dumps(deep)
          # v2 + v3 on a single public repo are separate allowed identities.
          # Diagnose the final failed recovery independently and redact both
          # underlying opaque project IDs and worker result content.
          final_v3 = {
              **public_record,
              "project_id": "b" * 32,
              "final_goal": "Tracking: starlist-integration-v3-" + "c" * 24,
          }
          mixed_inbox = {
              "schema_version": "production-os/production-inbox/v1",
              "summary": {"matching": 2},
              "items": [public_record, final_v3],
          }
          final_detail = {
              "project": {
                  **synthetic_detail["project"],
                  "final_goal": final_v3["final_goal"],
                  "current_workflow": {"tasks": [{
                      "status": "failed", "attempts": 1, "max_attempts": 3,
                      "result": {
                          "ai_dev_server_status": "capacity_exhausted",
                          "evidence": {"pipeline_status": "capacity_exhausted",
                                       "message": "PRIVATE_V3_TRACE"},
                      },
                  }]},
              },
          }
          def get_versioned_project(url, _token, **_kwargs):
              if url.endswith("a" * 32):
                  return synthetic_detail
              if url.endswith("b" * 32):
                  return final_detail
              raise AssertionError("Unknown internal project")
          with diagnostic_patch.object(failure_diagnostics, "request_json",
                                       side_effect=get_versioned_project):
              mixed = add_deep_task_diagnostics(
                  public_diagnostics(mixed_inbox), mixed_inbox, "dummy")
          assert mixed["observed_public_v3_failures"] == 1
          assert mixed["details_checked_v2"] == 1
          assert mixed["details_checked_v3"] == 1
          assert mixed["coverage_complete"] is False  # three v2 targets missing
          assert mixed["details_complete"] is False
          v3_row = next(row for row in mixed["failures"]
                        if row["tracking_version"] == "v3")
          assert v3_row["worker_result_status"] == "capacity_exhausted"
          assert v3_row["pipeline_status"] == "capacity_exhausted"
          assert "PRIVATE_V3_TRACE" not in json.dumps(mixed)
          assert "project_id" not in json.dumps(mixed)
          # A missing v3 task result must block complete deep coverage.
          with diagnostic_patch.object(failure_diagnostics, "request_json",
                                       side_effect=lambda url, token, **kwargs:
                                           synthetic_detail if url.endswith("a" * 32)
                                           else {"project": {
                                               **final_detail["project"],
                                               "current_workflow": {"tasks": []}}}):
              incomplete_v3 = add_deep_task_diagnostics(
                  public_diagnostics(mixed_inbox), mixed_inbox, "dummy")
          assert incomplete_v3["details_checked_v2"] == 1
          assert incomplete_v3["details_checked_v3"] == 0
          assert incomplete_v3["details_complete"] is False
          # Even an operator API outage must leave a sanitized failure
          # artifact with a bounded enum; no raw exception may leak.
          import contextlib
          import io
          import os
          import sys
          import tempfile
          for api_response in (
              RuntimeError("backend-private-secret-DO_NOT_LEAK"),
              ValueError("malformed operator response: DO_NOT_LEAK"),
          ):
              with tempfile.TemporaryDirectory() as folder:
                  out = Path(folder) / "diagnosis.json"
                  with diagnostic_patch.dict(os.environ, {
                      "PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"
                  }), diagnostic_patch.object(sys, "argv", [
                      "portfolio_failure_diagnostics.py", "--output", str(out)
                  ]), diagnostic_patch.object(failure_diagnostics, "request_json",
                                             side_effect=api_response):
                      printed = io.StringIO()
                      with contextlib.redirect_stdout(printed):
                          assert failure_diagnostics.main() == 2
                  missing = json.loads(out.read_text())
                  assert missing["diagnostic_status"] == "unavailable-inbox"
                  assert missing["coverage_complete"] is False
                  assert missing["details_complete"] is False
                  assert missing["failures"] == []
                  assert "DO_NOT_LEAK" not in out.read_text() + printed.getvalue()
          with tempfile.TemporaryDirectory() as folder:
              out = Path(folder) / "diagnosis.json"
              with diagnostic_patch.dict(os.environ, {
                  "PRODUCTION_OS_OPERATOR_TOKEN": ""
              }), diagnostic_patch.object(sys, "argv", [
                  "portfolio_failure_diagnostics.py", "--output", str(out)
              ]), diagnostic_patch.object(failure_diagnostics, "request_json",
                                         side_effect=AssertionError("No API call allowed")):
                  with contextlib.redirect_stdout(io.StringIO()):
                      assert failure_diagnostics.main() == 2
              assert json.loads(out.read_text())["diagnostic_status"] == "missing-operator-token"
          # A syntactically valid detail object is insufficient unless it
          # contains actual terminal task evidence for this same project.
          for missing in ({}, {"current_workflow": {"tasks": []}},
                          {"current_workflow": {"tasks": [{"status": "queued"}]}}):
              incomplete_detail = {"project": {
                  **synthetic_detail["project"], **missing}}
              if "current_workflow" not in missing:
                  incomplete_detail["project"].pop("current_workflow", None)
              with diagnostic_patch.object(failure_diagnostics, "request_json",
                                           return_value=incomplete_detail):
                  partial = add_deep_task_diagnostics(
                      public_diagnostics(diagnostic_inbox), diagnostic_inbox, "dummy")
              assert partial["details_checked_v2"] == 0, partial
              assert partial["details_complete"] is False, partial
              assert partial["failures"][0]["details_checked"] is False, partial
          # Multiple v2 failures for one target must never receive a single
          # candidate's project details or count as complete coverage.
          duplicate = {**public_record, "project_id": "b" * 32,
                       "final_goal": "Tracking: starlist-integration-v2-" + "c" * 24}
          duplicate_inbox = {
              "schema_version": "production-os/production-inbox/v1",
              "summary": {"matching": 2},
              "items": [public_record, duplicate],
          }
          duplicate_report = public_diagnostics(duplicate_inbox)
          assert duplicate_report["coverage_complete"] is False
          with diagnostic_patch.object(failure_diagnostics, "request_json",
                                       side_effect=AssertionError("Ambiguous GET attempted")):
              ambiguous = add_deep_task_diagnostics(
                  duplicate_report, duplicate_inbox, "dummy")
          assert ambiguous["details_checked_v2"] == 0
          assert all(row["details_checked"] is False for row in ambiguous["failures"])
          assert ambiguous["details_complete"] is False
          try:
              public_diagnostics({"schema_version": "production-os/production-inbox/v1",
                                  "summary": {"matching": 201}, "items": []})
          except RuntimeError:
              pass
          else:
              raise AssertionError("Incomplete diagnosis page was accepted")
          # All four actual Production-OS lifecycle states are recognized.
          active = {"repository": "dbrckk/Ai-trading",
                    "final_goal": "Tracking: starlist-integration-v2-" + "a" * 24,
                    "status": "ACTIVE", "created_at": "2026-10-16T00:00:00+00:00"}
          completed = {"repository": "dbrckk/Jumpy",
                       "final_goal": "Tracking: starlist-integration-v3-" + "b" * 24,
                       "status": "DONE", "created_at": "2026-10-15T23:00:00Z"}
          valid = {"projects": [active, completed], "total_count": 2, "complete": True}
          assert verified_managed_projects(valid) == valid["projects"]
          assert count_active_integrations(valid["projects"]) == 1
          # A target is single-flight even when its previous job is already
          # REVIEW_REQUIRED (no worker active but changes may need review).
          pending_review = {**completed, "status": "REVIEW_REQUIRED"}
          busy = busy_integration_targets([active, pending_review, completed])
          assert busy == {"dbrckk/ai-trading", "dbrckk/jumpy"}
          assert busy_integration_targets([completed]) == set()
          assert busy_integration_targets([{
              **active, "final_goal": "unrelated-project",
          }]) == set()
          assert "dbrckk/ai-trading" in busy_integration_targets([
              {**active, "repository": "dbrckk/AI-Trading"},
          ])
          # Exercise the actual dispatcher with three qualified suggestions
          # spread across two repositories. No network, token or worker call.
          import os
          import tempfile
          from datetime import datetime, timezone
          from unittest.mock import patch
          import portfolio_daily as scanner
          # Use the real catalog metadata to verify that a Roblox Studio MCP
          # sidecar cannot be mistaken for a native Lua game dependency.
          catalog_entries = json.loads(Path("catalog.json").read_text())["repositories"]
          bridge = next(item for item in catalog_entries
                        if item["repo"].lower() == "chrrxs/robloxstudio-mcp")
          assert "mcp" in bridge["capabilities"]
          profile = {"domains": ["game_dev"], "terms": scanner.tokens(
              "roblox playtesting debugging studio multiplayer profiling"),
              "dependencies": "", "overview": "roblox game", "language": "lua"}
          game = {"full_name": "dbrckk/chaos-survival-roblox",
                  "name": "chaos-survival-roblox"}
          from portfolio_daily import recommendations
          matched = recommendations(game, profile, [bridge], 3)
          assert len(matched) == 1, matched
          assert matched[0]["mode"] == "adapter-review", matched
          # A relevant curated tool must remain visible when its admission
          # tier/license/complexity require human review. It must never become
          # native or eligible for a mutating Production-OS request.
          unsafe_bridge = {
              **bridge, "tier": "indexed", "integrationComplexity": "high",
              "github": {**bridge["github"], "license": "NOASSERTION"},
          }
          advisory = recommendations(game, profile, [unsafe_bridge], 3)
          assert len(advisory) == 1 and advisory[0]["mode"] == "policy-review", advisory
          assert advisory[0]["integrationEligible"] is False
          assert {"high-integration-complexity",
                  "license-not-approved"} <= set(advisory[0]["policyReview"]), advisory
          assert "tier-not-approved" not in advisory[0]["policyReview"]
          # Development bridges remain reviewable, not dispatched natively.
          assert not any(x["mode"] == "native" for x in matched)
          engines = [item for item in catalog_entries if item["repo"].lower()
                     in {"godotengine/godot", "libgdx/libgdx"}]
          assert len(engines) == 2
          assert any("libgdx/libgdx" in (e.get("alternatives") or []) for e in engines)
          game_profile = {"domains": ["game_dev"],
                          "terms": scanner.tokens("roblox game development cross platform"),
                          "language": "lua", "dependencies": "", "overview": ""}
          # Explicitly declared alternative engines are not Roblox plugins.
          assert recommendations(game, game_profile, engines, 3) == []
          # Hermes/OpenCode are standalone agent processes. Even a matching
          # implementation language must not turn them into native libraries.
          for slug, language, terms in (
              ("NousResearch/hermes-agent", "python",
               "agent delegation memory automation mcp research scheduled workflows"),
              ("anomalyco/opencode", "typescript",
               "agent coding debugging tests mcp terminal repository development"),
          ):
              source = next(item for item in catalog_entries
                            if item["repo"].lower() == slug.lower())
              agent_profile = {
                  "domains": ["ai_agents"],
                  "language": language,
                  "terms": scanner.tokens(terms),
                  "dependencies": "",
                  "overview": "",
              }
              target = {"name": "ai-service", "full_name": "dbrckk/ai-service"}
              suggestions = recommendations(target, agent_profile, [source], 3)
              assert len(suggestions) == 1, (slug, suggestions)
              assert suggestions[0]["mode"] == "adapter-review", suggestions
          from urllib.request import Request
          protected = Request("https://production-os1.onrender.com/v1/dashboard/launch",
                              headers={"Authorization": "Bearer offline-test"})
          redirect = scanner.SameOriginRedirect()
          for destination in (
              "http://production-os1.onrender.com/unsafe",
              "https://example.com/collect",
              "https://production-os1.onrender.com.evil.test/collect",
              "https://user:password@production-os1.onrender.com/collect",
          ):
              try:
                  redirect.redirect_request(protected, None, 302, "Found", {}, destination)
              except RuntimeError:
                  pass
              else:
                  raise AssertionError("Cross-origin API redirect accepted: " + destination)
          same_origin = redirect.redirect_request(
              protected, None, 302, "Found", {},
              "https://production-os1.onrender.com/v1/managed-projects")
          assert same_origin.get_header("Authorization") == "Bearer offline-test"
          targets = [
              {"name": name, "full_name": "dbrckk/" + name, "private": False}
              for name in ("alpha", "beta")
          ]
          def suggestion(slug, score):
              return {"repository": slug, "score": score, "mode": "native",
                      "integrationEligible": True, "policyReview": [],
                      "url": "https://github.com/" + slug, "license": "MIT",
                      "shared_terms": ["integration"]}
          offers = {
              "dbrckk/alpha": [suggestion("upstream/one", 60),
                               suggestion("upstream/two", 59)],
              "dbrckk/beta": [suggestion("upstream/three", 58)],
          }
          launches = []
          def fake_launch(_url, _token, target, candidate, **kwargs):
              launches.append((target, candidate["repository"]))
              identity = f"{len(launches):032x}"
              marker = integration_marker(target, candidate,
                                          version=kwargs.get("version", 2))
              return {
                  "project": {
                      "id": identity, "project_id": identity,
                      "repository": target, "final_goal": "Tracking: " + marker,
                      "token_budget": scanner.INTEGRATION_TOKEN_BUDGET,
                  },
                  "launch": {
                      "mode": "managed-project", "persistent": True,
                      "idempotent": True, "request_id": marker,
                      "token_budget": scanner.INTEGRATION_TOKEN_BUDGET,
                  },
              }
          with tempfile.TemporaryDirectory() as scratch:
              p = Path(scratch)
              (p / "catalog.json").write_text('{"repositories": []}')
              argv = ["portfolio_daily.py", "--catalog", str(p / "catalog.json"),
                      "--output", str(p / "scan.json"),
                      "--markdown", str(p / "scan.md"), "--max-dispatch", "3"]
              with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                   patch.object(sys, "argv", argv), \
                   patch.object(scanner, "github_repos", return_value=targets), \
                   patch.object(scanner, "project_profile", return_value={}), \
                   patch.object(scanner, "recommendations",
                                side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                   patch.object(scanner, "request_json", return_value={
                       "projects": [], "total_count": 0, "complete": True}), \
                   patch.object(scanner, "launch_integration", side_effect=fake_launch):
                  assert scanner.main() == 0
              evidence = json.loads((p / "scan.json").read_text())
              assert evidence["summary"]["dispatched"] == 2
              assert evidence["summary"]["with_native_suggestions"] == 2
              assert evidence["summary"]["native_suggestions"] == 3
              assert evidence["summary"]["with_suggestions"] == 2
              assert evidence["dispatch_status"] == "enabled"
              assert launches == [("dbrckk/alpha", "upstream/one"),
                                  ("dbrckk/beta", "upstream/three")], launches
              # The server may accept a launch before its response is lost.
              # Neither transport failure nor malformed acknowledgement can
              # authorize a second POST for a different repository.
              def ambiguous_launch(_url, _token, target, candidate, **_kwargs):
                  launches.append((target, candidate["repository"]))
                  raise RuntimeError("simulated timeout after accepted POST")
              def unconfirmed_launch(_url, _token, target, candidate, **_kwargs):
                  launches.append((target, candidate["repository"]))
                  return {"project": None}
              def mismatched_target(_url, _token, target, candidate, **kwargs):
                  result = fake_launch(_url, _token, target, candidate, **kwargs)
                  result["project"]["repository"] = "dbrckk/wrong-target"
                  return result
              def mismatched_marker(_url, _token, target, candidate, **kwargs):
                  result = fake_launch(_url, _token, target, candidate, **kwargs)
                  result["launch"]["request_id"] = "other-request-id"
                  return result
              def wrong_budget(_url, _token, target, candidate, **kwargs):
                  result = fake_launch(_url, _token, target, candidate, **kwargs)
                  result["launch"]["token_budget"] = 30000
                  return result
              for launch_impl in (ambiguous_launch, unconfirmed_launch,
                                  mismatched_target, mismatched_marker, wrong_budget):
                  launches.clear()
                  with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                       patch.object(sys, "argv", argv), \
                       patch.object(scanner, "github_repos", return_value=targets), \
                       patch.object(scanner, "project_profile", return_value={}), \
                       patch.object(scanner, "recommendations",
                                    side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                       patch.object(scanner, "request_json", return_value={
                           "projects": [], "total_count": 0, "complete": True}), \
                       patch.object(scanner, "launch_integration", side_effect=launch_impl):
                      assert scanner.main() == 1
                  uncertain = json.loads((p / "scan.json").read_text())
                  assert uncertain["summary"]["dispatched"] == 0
                  assert uncertain["summary"]["failures"] == 1
                  assert uncertain["dispatch_status"] == "blocked (unconfirmed Production-OS launch)"
                  assert launches == [("dbrckk/alpha", "upstream/one")], launches
              # The v3 recovery branch must also stop the queue after an
              # ambiguous launch, even if another target has eligible work.
              launches.clear()
              failed_prior = {
                  "repository": "dbrckk/alpha", "status": "NEEDS_ATTENTION",
                  "created_at": "2026-01-01T00:00:00Z",
                  "final_goal": integration_marker(
                      "dbrckk/alpha", {"repository": "upstream/one"}),
              }
              with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                   patch.object(sys, "argv", argv), \
                   patch.object(scanner, "github_repos", return_value=targets), \
                   patch.object(scanner, "project_profile", return_value={}), \
                   patch.object(scanner, "recommendations",
                                side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                   patch.object(scanner, "request_json", return_value={
                       "projects": [failed_prior], "total_count": 1, "complete": True}), \
                   patch.object(scanner, "launch_integration", side_effect=ambiguous_launch):
                  assert scanner.main() == 1
              recovery = json.loads((p / "scan.json").read_text())
              assert recovery["summary"]["failed_v2_integrations"] == 1
              assert recovery["summary"]["dispatched"] == 0
              assert recovery["dispatch_status"] == "blocked (unconfirmed Production-OS launch)"
              assert launches == [("dbrckk/alpha", "upstream/one")], launches
              # A failed repository scan must fail closed before even reading
              # Production-OS inventory, despite earlier eligible suggestions.
              launches.clear()
              def fail_second_profile(repo, _token):
                  if repo["name"] == "beta":
                      raise RuntimeError("injected GitHub read failure")
                  return {}
              with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                   patch.object(sys, "argv", argv), \
                   patch.object(scanner, "github_repos", return_value=targets), \
                   patch.object(scanner, "project_profile", side_effect=fail_second_profile), \
                   patch.object(scanner, "recommendations",
                                side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                   patch.object(scanner, "request_json",
                                side_effect=AssertionError("Production-OS called after scan failure")), \
                   patch.object(scanner, "launch_integration", side_effect=fake_launch):
                  assert scanner.main() == 1
              failed_evidence = json.loads((p / "scan.json").read_text())
              assert failed_evidence["summary"]["discovered"] == 2
              assert failed_evidence["summary"]["inspected"] == 1
              assert failed_evidence["summary"]["dispatched"] == 0
              assert failed_evidence["summary"]["failures"] == 1
              assert failed_evidence["dispatch_status"] == "blocked (incomplete repository scan)"
              assert failed_evidence["projects"][1]["status"] == "scan-failed"
              assert launches == [], launches
              # Even a healthy scan must explain why an exhausted UTC quota
              # prevents dispatch. No Production-OS launch may occur.
              current_time = datetime.now(timezone.utc).isoformat()
              inventory = {"complete": True, "total_count": 2, "projects": [
                  {"repository": "dbrckk/other", "status": "NEEDS_ATTENTION",
                   "created_at": current_time,
                   "final_goal": integration_marker(
                       "dbrckk/other", {"repository": "upstream/failure"})},
                  {"repository": "dbrckk/another", "status": "DONE",
                   "created_at": current_time,
                   "final_goal": integration_marker(
                       "dbrckk/another", {"repository": "upstream/earlier"})},
              ]}
              with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                   patch.object(sys, "argv", argv), \
                   patch.object(scanner, "github_repos", return_value=targets), \
                   patch.object(scanner, "project_profile", return_value={}), \
                   patch.object(scanner, "recommendations",
                                side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                   patch.object(scanner, "request_json", return_value=inventory), \
                   patch.object(scanner, "launch_integration", side_effect=fake_launch):
                  assert scanner.main() == 0
              throttled = json.loads((p / "scan.json").read_text())
              assert throttled["summary"]["available_dispatch_slots"] == 0
              assert throttled["summary"]["dispatched"] == 0
              assert throttled["dispatch_status"] == "throttled (UTC daily launch quota exhausted)"
              assert throttled["summary"]["failed_v3_integrations"] == 0
              assert launches == [], launches
              # A final v3 recovery failure is a fleet-wide hard stop, even
              # on a fresh UTC day with otherwise eligible unrelated tools.
              # The scanner must still produce complete public discovery.
              final_v3_failure = {
                  "repository": "dbrckk/alpha", "status": "NEEDS_ATTENTION",
                  "created_at": "2026-01-01T00:00:00Z",
                  "final_goal": integration_marker(
                      "dbrckk/alpha", {"repository": "upstream/one"}, version=3),
              }
              assert count_failed_v3_integrations([final_v3_failure]) == 1
              assert count_failed_v3_integrations([
                  {**final_v3_failure, "status": "DONE"}
              ]) == 0
              launches.clear()
              final_inventory = {"complete": True, "total_count": 1,
                                 "projects": [final_v3_failure]}
              with patch.dict(os.environ, {"PRODUCTION_OS_OPERATOR_TOKEN": "offline-test"}), \
                   patch.object(sys, "argv", argv), \
                   patch.object(scanner, "github_repos", return_value=targets), \
                   patch.object(scanner, "project_profile", return_value={}), \
                   patch.object(scanner, "recommendations",
                                side_effect=lambda repo, *_: offers[repo["full_name"]]), \
                   patch.object(scanner, "request_json", return_value=final_inventory), \
                   patch.object(scanner, "launch_integration",
                                side_effect=AssertionError("Final v3 failure was ignored")):
                  assert scanner.main() == 0
              gated = json.loads((p / "scan.json").read_text())
              assert gated["summary"]["inspected"] == 2
              assert gated["summary"]["with_suggestions"] == 2
              assert gated["summary"]["dispatched"] == 0
              assert gated["summary"]["available_dispatch_slots"] == 0
              assert gated["summary"]["failed_v3_integrations"] == 1
              assert gated["dispatch_status"] == (
                  "paused (failed v3 recovery needs operator review)")
              assert "Failed final v3 recovery attempts requiring operator review: **1**" in (
                  p / "scan.md").read_text()
              assert launches == [], launches
          # The dispatch quota is tied to UTC, not to the worker's local date.
          utc_boundary = [
              {"final_goal": integration_marker("dbrckk/Jumpy", {"repository": "a/b"}),
               "created_at": "2026-10-17T00:20:00+02:00"},
              {"final_goal": integration_marker("dbrckk/Jumpy", {"repository": "c/d"}),
               "created_at": "2026-10-16T23:20:00-02:00"},
              {"final_goal": "unrelated", "created_at": "2026-10-16T15:00:00Z"},
          ]
          assert count_launches_on_utc_date(utc_boundary, "2026-10-16") == 1
          assert count_launches_on_utc_date(utc_boundary, "2026-10-17") == 1
          for changes in (
              {"status": "IN_PROGRESS"},
              {"status": []},
              {"status": ""},
              {"created_at": ""},
              {"created_at": "tomorrow"},
              {"created_at": "2026-10-16T00:00:00"},
              {"repository": ""},
              {"repository": "not-a-repository"},
              {"final_goal": "starlist-integration-v2-invalid"},
          ):
              corrupt = dict(active, **changes)
              try:
                  verified_managed_projects({
                      "projects": [corrupt], "total_count": 1, "complete": True,
                  })
              except RuntimeError:
                  pass
              else:
                  raise AssertionError("Corrupt tracked integration was accepted: " + str(changes))
          try:
              verified_managed_projects({
                  "projects": [active, dict(active)], "total_count": 2, "complete": True,
              })
          except RuntimeError:
              pass
          else:
              raise AssertionError("Duplicate tracking marker was accepted")
          for malformed in (
              None, {}, {"projects": "unavailable"}, {"projects": [None]},
              {"projects": []}, {"projects": [], "total_count": 1, "complete": True},
              {"projects": [], "total_count": 0, "complete": False},
              {"projects": [], "total_count": True, "complete": True},
              {"projects": [{"final_goal": "starlist-integration-v2-broken", "status": "ACTIVE"}]},
          ):
              try:
                  verified_managed_projects(malformed)
              except RuntimeError:
                  pass
              else:
                  raise AssertionError("Malformed managed-project inventory was accepted")
          assert count_active_integrations([
              {"final_goal": "starlist-integration-v2-project", "status": "ACTIVE"},
              {"final_goal": "starlist-integration-v1-previous", "status": "NEEDS_ATTENTION"},
              {"final_goal": "unrelated", "status": "ACTIVE"},
              {"final_goal": "starlist-integration-v2-another", "status": "QUEUED"},
          ]) == 2
          failed_v2 = {
              "final_goal": "starlist-integration-v2-" + "a" * 24,
              "status": "NEEDS_ATTENTION",
          }
          completed_v3 = {
              "final_goal": "starlist-integration-v3-" + "a" * 24,
              "status": "DONE",
          }
          assert count_failed_v2_integrations([
              {"final_goal": "starlist-integration-v1-old", "status": "NEEDS_ATTENTION"},
              failed_v2,
              {"final_goal": "starlist-integration-v2-" + "b" * 24, "status": "ACTIVE"},
          ]) == 1
          assert count_failed_v2_integrations([failed_v2, completed_v3]) == 0
          assert count_failed_v2_integrations([
              failed_v2, {**completed_v3, "status": "REVIEW_REQUIRED"},
          ]) == 1
          assert count_failed_v2_integrations([
              failed_v2, {**completed_v3,
                          "final_goal": "starlist-integration-v3-" + "b" * 24},
          ]) == 1
          target = "dbrckk/vibecheck-android"
          old = {"repository": "android/nowinandroid"}
          new = {"repository": "rive-app/rive-android"}
          obsolete_failure = {
              "repository": target,
              "final_goal": integration_marker(target, old),
              "status": "NEEDS_ATTENTION",
          }
          rows = [{"repository": target, "suggestions": [
              {**old, "mode": "reference-review"},
              {**new, "mode": "native"},
          ]}]
          # A disqualified prior tool is still a visible failure but must
          # not permanently block a different qualified implementation.
          assert recoverable_failure_targets([obsolete_failure], rows, []) == set()
          rows[0]["suggestions"][0]["mode"] = "native"
          assert recoverable_failure_targets(
              [obsolete_failure], rows, [],
          ) == {target.lower()}
          terminal_retry = {"repository": target, "status": "NEEDS_ATTENTION",
                            "final_goal": integration_marker(target, old, 3)}
          assert recoverable_failure_targets(
              [obsolete_failure], rows, [terminal_retry],
          ) == set()
          assert count_failed_v2_integrations(
              [obsolete_failure, terminal_retry],
          ) == 1
          assert result["summary"]["active_integrations"] is None
          assert result["summary"]["failed_v2_integrations"] is None
          catalog = json.loads(Path("catalog.json").read_text())["repositories"]
          # Regression from the real Jumpy scan: a Godot game cannot
          # "integrate" the whole Godot engine as a new dependency.
          godot_engine = next(x for x in catalog if x["repo"].lower() == "godotengine/godot")
          libgdx_engine = next(x for x in catalog if x["repo"].lower() == "libgdx/libgdx")
          assert "libgdx/libgdx" in [
              x.lower() for x in godot_engine.get("alternatives", [])
          ], "Catalog must explicitly identify libGDX as an alternative to Godot"
          jumpy = {"name": "Jumpy", "full_name": "dbrckk/Jumpy"}
          godot_profile = {
              "domains": ["game_dev"], "language": "gdscript",
              "terms": scanner.tokens("godot game development cross-platform"),
              "dependencies": "", "overview": "",
          }
          assert scanner.recommendations(
              jumpy, godot_profile, [godot_engine, libgdx_engine], 3
          ) == []
          # The exclusion is specific to engine sources and their explicit
          # alternatives, not normal Godot plugins or compatible addons.
          assert "godotengine/godot" in scanner.EXISTING_ENGINE_SOURCES["godot"]
          for project in result["projects"]:
              if project["repository"].lower() == "dbrckk/jumpy":
                  assert all(item["repository"].lower() not in {
                      "godotengine/godot", "libgdx/libgdx"
                  } for item in project["suggestions"]), project
          reference = next(x for x in catalog if x["repo"].lower() == "android/nowinandroid")
          assert is_reference_candidate(reference), "Architecture example must be review-only"
          for project in result["projects"]:
              for candidate in project["suggestions"]:
                  if candidate["repository"].lower() == "android/nowinandroid":
                      assert candidate["mode"] == "reference-review", candidate
          print("Verified reference applications cannot enter the automated dispatch queue")
          print("Verified meaningful matching and Roblox engine compatibility")
          print("Read-only scan verified:", result["summary"])
          PY
      - name: Preserve real scan evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: portfolio-live-readonly-smoke
          path: |
            portfolio-daily.json
            portfolio-daily.md
          if-no-files-found: warn
          retention-days: 14
````

## File: .github/workflows/production-os-review-handoff.yml
````yaml
name: Trusted Production-OS PR Handoff

# Runs from the default branch only. Never checks out or executes Studio code.
on:
  repository_dispatch:
    types: [production_os_review_handoff]

permissions:
  contents: read
  pull-requests: write
  actions: write

concurrency:
  group: production-os-review-handoff
  cancel-in-progress: false

jobs:
  create-review:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    env:
      REVIEW_TOKEN: ${{ github.token }}
    steps:
      - name: Verify published checkpoint and open a review PR
        shell: bash
        run: |
          set -euo pipefail
          python3 - <<'PY'
          import json
          import os
          import re
          import urllib.error
          import urllib.parse
          import urllib.request

          repo = os.environ["GITHUB_REPOSITORY"]
          if repo != "dbrckk/star-list":
              raise SystemExit("Review handoff must run in the trusted repository")
          with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as source:
              event = json.load(source)
          payload = event.get("client_payload")
          if not isinstance(payload, dict) or set(payload) != {"branch", "commit_sha"}:
              raise SystemExit("Invalid Production-OS review handoff payload")
          branch = payload.get("branch")
          sha = payload.get("commit_sha")
          if not isinstance(branch, str) or not re.fullmatch(r"studio/mp-[a-f0-9]{24}", branch):
              raise SystemExit("Handoff branch does not match managed Studio namespace")
          if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{40}", sha):
              raise SystemExit("Handoff commit SHA is invalid")

          token = os.environ["REVIEW_TOKEN"]
          base = "https://api.github.com/repos/" + repo
          headers = {
              "Authorization": "Bearer " + token,
              "Accept": "application/vnd.github+json",
              "X-GitHub-Api-Version": "2022-11-28",
              "User-Agent": "production-os-review-handoff",
          }

          def request(method, path, data=None):
              body = json.dumps(data).encode("utf-8") if data is not None else None
              action = urllib.request.Request(
                  base + path, data=body, method=method, headers={
                      **headers, **({"Content-Type": "application/json"} if body else {}),
                  }
              )
              try:
                  with urllib.request.urlopen(action, timeout=20) as response:
                      raw = response.read(1000000)
                      return json.loads(raw) if raw else {}
              except urllib.error.HTTPError as exc:
                  if exc.code in {401, 403}:
                      raise SystemExit(
                          "Target GitHub Actions must allow pull-request creation "
                          "(Pull requests:write and repository setting)"
                      ) from None
                  raise SystemExit("Review handoff GitHub API returned HTTP " + str(exc.code)) from None

          ref = request("GET", "/git/ref/heads/" + branch)
          verified = (ref.get("object") or {}).get("sha")
          if verified != sha:
              raise SystemExit("Review handoff rejected a stale or unverified branch tip")
          delta = request("GET", "/compare/main..." + branch)
          files = delta.get("files")
          if (delta.get("status") not in {"ahead", "diverged"}
                  or not isinstance(files, list) or not 0 < len(files) < 300):
              raise SystemExit("Review handoff requires a bounded nonempty compare")
          if len(files) != 1 or files[0].get("filename") != "scripts/validate_websites.py" or files[0].get("status") != "modified":
              raise SystemExit("Review handoff only accepts the vetted one-file website source fix")

          # A single named file is not sufficient: another generic engine
          # previously overwrote the same reserved branch with an EMPTY
          # validator (98 lines deleted). Require the exact operator-reviewed
          # one-line repair, and reject omissions, chmod-only changes, extra
          # edits, unverified patch evidence and unexpected AI output.
          changed = files[0]
          patch = changed.get("patch")
          if (type(changed.get("additions")) is not int
                  or type(changed.get("deletions")) is not int
                  or changed["additions"] != 1 or changed["deletions"] != 1
                  or type(changed.get("changes")) is not int
                  or changed["changes"] != 2
                  or not isinstance(patch, str) or len(patch) > 4000):
              raise SystemExit("Review handoff rejected an unbounded source diff")
          source_edits = [
              line for line in patch.splitlines()
              if line.startswith(("+", "-"))
              and not line.startswith(("+++", "---"))
          ]
          if source_edits != [
              "-                root = website.hostname.lower()",
              '+                root = website.hostname.lower().removeprefix("www.")',
          ]:
              raise SystemExit("Review handoff rejected a source edit outside the approved assignment")

          # Require the same exact branch head immediately before opening the
          # review. Never trust a previously compared SHA after a concurrent
          # worker updates the managed branch.
          latest_ref = request("GET", "/git/ref/heads/" + branch)
          if (latest_ref.get("object") or {}).get("sha") != sha:
              raise SystemExit("Review handoff rejected a branch movement after comparison")

          owner = repo.split("/", 1)[0]
          query = urllib.parse.urlencode({
              "state": "open", "head": owner + ":" + branch, "base": "main",
              "per_page": "20",
          })
          existing = request("GET", "/pulls?" + query)
          if not isinstance(existing, list):
              raise SystemExit("Pull request list returned an invalid response")
          for item in existing:
              if ((item.get("head") or {}).get("ref") == branch
                      and (item.get("base") or {}).get("ref") == "main"):
                  print("Reused existing review: " + str(item.get("html_url") or ""))
                  break
          else:
              created = request("POST", "/pulls", {
                  "title": "Review Production-OS verified checkpoint: " + branch,
                  "head": branch,
                  "base": "main",
                  "draft": True,
                  "body": (
                      "Production-OS published this checkpoint to a review branch. "
                      "This PR was opened by the trusted target-repository handoff "
                      "after independently validating the exact branch tip and diff. "
                      "Review all changed files and run required CI before any merge. "
                      "No changes are merged automatically.\n\n"
                      "Checkpoint: `" + sha + "`"
                  ),
              })
              if not isinstance(created, dict) or not created.get("number"):
                  raise SystemExit("Review handoff did not receive a real PR number")
              print("Opened draft review: " + str(created.get("html_url") or ""))
          # Trigger the pre-existing trusted catalog workflow against the
          # exact reviewed branch; the model cannot modify workflow files.
          request("POST", "/actions/workflows/validate.yml/dispatches", {
              "ref": branch,
          })
          print("Requested independent catalog CI for " + sha)
          PY
````

## File: .github/workflows/readme-evidence-freshness.yml
````yaml
name: Verify README evidence freshness

on:
  schedule:
    - cron: "37 6 * * *"
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: star-list-readme-freshness
  cancel-in-progress: false

jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Select a rotating batch of reviewed README evidence
        id: batch
        run: |
          python - <<'PY' >> "$GITHUB_OUTPUT"
          import datetime, json
          from pathlib import Path
          sources = json.loads(Path("catalog-readme-evidence.json").read_text())["sources"]
          batches = max(1, (len(sources) + 11) // 12)
          print(f"index={datetime.date.today().toordinal() % batches}")
          PY
      - name: Check upstream README hashes without writes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/check_readme_evidence_freshness.py --batch-size 12             --batch-index "${{ steps.batch.outputs.index }}"             --out readme-evidence-freshness.json > /tmp/readme-evidence-summary.json
      - name: Upload source change report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: readme-evidence-freshness
          path: readme-evidence-freshness.json
          if-no-files-found: warn
          retention-days: 35
````

## File: .github/workflows/refresh-metadata.yml
````yaml
name: Refresh GitHub metadata

on:
  schedule:
    - cron: "17 4 * * 1"
  workflow_dispatch:

permissions:
  contents: write
  issues: write

concurrency:
  group: refresh-github-metadata
  cancel-in-progress: false

jobs:
  refresh:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Refresh repository metadata
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/refresh_github_metadata.py --write
      - name: Validate refreshed catalog
        run: |
          python scripts/validate_catalog.py
          python scripts/test_recommend.py
      - name: Build catalog quality audit
        run: |
          python scripts/audit_catalog_quality.py --markdown-output catalog-quality.md > catalog-quality.json
          python scripts/validate_json_contract.py schemas/catalog-quality.schema.json catalog-quality.json
      - name: Build current health snapshot and drift report
        run: |
          python scripts/health_score.py > health-snapshot-current.json
          python scripts/detect_health_drift.py health-snapshot.json health-snapshot-current.json > health-drift.json
          python scripts/validate_json_contract.py schemas/health-snapshot.schema.json health-snapshot-current.json
          python scripts/validate_json_contract.py schemas/health-drift.schema.json health-drift.json
      - name: Update compact repository history
        run: |
          python scripts/update_history.py history.json catalog.json health-snapshot-current.json --write --trends health-trends.json
          python scripts/validate_json_contract.py schemas/history.schema.json history.json
          python scripts/validate_json_contract.py schemas/health-trends.schema.json health-trends.json
      - name: Build discovery watchlist and candidate shortlist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/analyze_coverage.py > coverage-report.json
          python scripts/build_discovery_watchlist.py coverage-report.json > discovery-watchlist.json
          python scripts/discover_candidates.py discovery-watchlist.json catalog.json --top 50 --cache discovery-cache.json --search-cache-ttl-hours 24 --metadata-cache-ttl-hours 336 > discovery-candidates.json
          python scripts/evaluate_candidates.py discovery-candidates.json > discovery-evaluated-raw.json
          python scripts/filter_discovery_memory.py discovery-evaluated-raw.json discovery-memory.json --output discovery-evaluated.json --write-memory
          python scripts/validate_json_contract.py schemas/coverage-report.schema.json coverage-report.json
          python scripts/validate_json_contract.py schemas/discovery-watchlist.schema.json discovery-watchlist.json
          python scripts/validate_json_contract.py schemas/discovery-candidates.schema.json discovery-candidates.json
          python scripts/validate_json_contract.py schemas/discovery-evaluated.schema.json discovery-evaluated-raw.json
          python scripts/validate_json_contract.py schemas/discovery-evaluated.schema.json discovery-evaluated.json
          python scripts/validate_json_contract.py schemas/discovery-cache.schema.json discovery-cache.json
          python scripts/validate_json_contract.py schemas/discovery-memory.schema.json discovery-memory.json
      - name: Analyze discovery cache health
        run: |
          python scripts/analyze_cache_health.py discovery-candidates.json --markdown-output cache-health.md > cache-health.json
          python scripts/update_cache_health_history.py cache-health-history.json cache-health.json --write --trend-output cache-health-trend.json --markdown-output cache-health-trend.md
          python scripts/validate_json_contract.py schemas/cache-health.schema.json cache-health.json
          python scripts/validate_json_contract.py schemas/cache-health-trend.schema.json cache-health-trend.json
          python scripts/validate_json_contract.py schemas/cache-health-history.schema.json cache-health-history.json
          cat cache-health-trend.md >> cache-health.md
      - name: Publish discovery cache health issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          ALERT_STATE=$(python -c "import json; print(json.load(open('cache-health-trend.json')).get('alertState','healthy'))")
          ISSUE_ACTION=$(python -c "import json; print(json.load(open('cache-health-trend.json')).get('issueAction','open'))")
          MARKER='<!-- star-list-cache-health -->'
          EXISTING=$(gh issue list --state open --search "$MARKER in:body" --json number --jq '.[0].number // empty')
          if [ "$ISSUE_ACTION" = "close" ]; then
            if [ -n "$EXISTING" ]; then gh issue close "$EXISTING" --comment "Discovery cache health returned to normal after two consecutive healthy observations."; fi
          elif [ "$ISSUE_ACTION" = "hold" ]; then
            echo "Cache-health issue cooldown active; leaving issue state unchanged."
          elif [ -n "$EXISTING" ]; then
            gh issue edit "$EXISTING" --title "Discovery cache health: $ALERT_STATE" --body-file cache-health.md
          else
            gh issue create --title "Discovery cache health: $ALERT_STATE" --body-file cache-health.md --label maintenance || gh issue create --title "Discovery cache health: $ALERT_STATE" --body-file cache-health.md
          fi
      - name: Build discovery candidate issue
        run: python scripts/render_discovery_issue.py discovery-evaluated.json --output discovery-review.md
      - name: Publish discovery candidate issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          ACTIONABLE=$(python -c "import json; d=json.load(open('discovery-evaluated.json')); print(d['counts']['accept']+d['counts']['review'])")
          MARKER='<!-- star-list-discovery-candidates -->'
          EXISTING=$(gh issue list --state open --search "$MARKER in:body" --json number --jq '.[0].number // empty')
          if [ "$ACTIONABLE" = "0" ]; then
            if [ -n "$EXISTING" ]; then gh issue close "$EXISTING" --comment "No actionable discovery candidates remain."; fi
          elif [ -n "$EXISTING" ]; then
            gh issue edit "$EXISTING" --title "Discovery candidates" --body-file discovery-review.md
          else
            gh issue create --title "Discovery candidates" --body-file discovery-review.md --label enhancement || gh issue create --title "Discovery candidates" --body-file discovery-review.md
          fi
      - name: Build repository health review
        run: |
          python scripts/find_replacements.py > replacement-report.json
          python scripts/validate_json_contract.py schemas/replacement-report.schema.json replacement-report.json
          python scripts/render_health_issue.py replacement-report.json --drift health-drift.json --output health-review.md
      - name: Publish health review issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          COUNT=$(python -c "import json; print(json.load(open('replacement-report.json'))['findings'])")
          DRIFT_COUNT=$(python -c "import json; print(json.load(open('health-drift.json'))['findings'])")
          MARKER='<!-- star-list-health-review -->'
          EXISTING=$(gh issue list --state open --search "$MARKER in:body" --json number --jq '.[0].number // empty')
          if [ "$COUNT" = "0" ] && [ "$DRIFT_COUNT" = "0" ]; then
            if [ -n "$EXISTING" ]; then
              gh issue close "$EXISTING" --comment "Automated health review is clean; no repositories currently require replacement review."
            fi
          elif [ -n "$EXISTING" ]; then
            gh issue edit "$EXISTING" --title "Automated repository health review" --body-file health-review.md
          else
            gh issue create --title "Automated repository health review" --body-file health-review.md --label maintenance || gh issue create --title "Automated repository health review" --body-file health-review.md
          fi
      - name: Commit changes
        run: |
          cp health-snapshot-current.json health-snapshot.json
          if git diff --quiet -- catalog.json health-snapshot.json discovery-memory.json history.json discovery-cache.json cache-health-history.json; then
            echo "No metadata, history, memory, or cache changes"
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add catalog.json health-snapshot.json discovery-memory.json history.json discovery-cache.json cache-health-history.json
          git commit -m "chore: refresh GitHub metadata and discovery cache"
          # Stars admission and metadata refresh can overlap. Never overwrite a
          # newer catalog or force-push; first rebase on the latest remote.
          for attempt in 1 2 3 4; do
            git fetch origin main
            git rebase origin/main
            if git push origin HEAD:main; then
              exit 0
            fi
            sleep "$attempt"
          done
          echo "::error::Could not publish validated metadata after four non-destructive retries"
          exit 1

  quality-after-refresh:
    # GitHub suppresses normal push triggers for GITHUB_TOKEN commits.
    # Publish only after the validated catalog/history push succeeded, and
    # audit the actual remote main rather than a pre-commit local snapshot.
    needs: refresh
    permissions:
      contents: read
      issues: write
    uses: ./.github/workflows/catalog-quality-on-change.yml
````

## File: .github/workflows/semantic-refresh.yml
````yaml
name: Precise semantic refresh

on:
  workflow_dispatch:
  schedule:
    - cron: "23 3 * * 1"

permissions:
  contents: write

concurrency:
  group: semantic-refresh-${{ github.repository }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  semantic:
    uses: dbrckk/repo-brain/.github/workflows/reusable-semantic.yml@main
    with:
      commit_changes: true
````

## File: .github/workflows/sync-github-stars.yml
````yaml
name: Sync GitHub Stars

on:
  schedule:
    - cron: "11 * * * *"
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - ".github/workflows/sync-github-stars.yml"
      - "catalog.json"

permissions:
  contents: write
  issues: write

concurrency:
  group: star-list-stars-sync
  cancel-in-progress: false

jobs:
  sync:
    outputs:
      catalog_changed: ${{ steps.catalog_push.outputs.catalog_changed }}
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Test offline star synchronization
        run: python scripts/test_sync_github_stars.py
      - name: Read and compare public GitHub Stars
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/sync_github_stars.py --user dbrckk \
            --report-json star-sync-report.json \
            --report-md star-sync-review.md \
            --manifest star-sync-manifest.json
          python scripts/validate_json_contract.py \
            schemas/star-sync-report.schema.json star-sync-report.json
      - name: Admit every newly starred public repository
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/admit_github_stars.py \
            --sync-report star-sync-report.json \
            --manifest star-sync-manifest.json \
            --report-json star-admission-report.json
          python scripts/validate_catalog.py
          python scripts/test_catalog_quality.py
      - name: Commit validated catalog changes
        id: catalog_push
        run: |
          if ! git diff --quiet -- catalog.json; then
            git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add catalog.json
            git commit -m "chore: sync all accessible GitHub Stars into catalog"
            for attempt in 1 2 3 4; do
              git fetch origin main
              git rebase origin/main
              if git push origin HEAD:main; then
                echo "catalog_changed=true" >> "$GITHUB_OUTPUT"
                exit 0
              fi
              sleep "$attempt"
            done
            echo "::error::Could not push the validated catalog after four non-destructive retries"
            exit 1
          fi
      - name: Preserve synchronization and admission results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          if-no-files-found: warn
          name: star-list-public-stars-admission
          path: |
            star-sync-report.json
            star-sync-review.md
            star-sync-manifest.json
            star-admission-report.json
          retention-days: 14
      - name: Open, update or close GitHub Stars review issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          COUNT=$(python -c 'import json; s=json.load(open("star-sync-report.json"))["summary"]; a=json.load(open("star-admission-report.json")); print(s["new"] - a["admitted"])')
          EXISTING=$(gh issue list --state open --limit 200 --json number,body \
            --jq '[.[] | select(.body != null and (.body | contains("<!-- star-list-star-sync -->")))] | .[0].number // empty')
          if [ "$COUNT" = "0" ]; then
            if [ -n "$EXISTING" ]; then
              gh issue close "$EXISTING" --comment "All accessible public GitHub Stars have been accounted for and admitted to the catalog."
            fi
          elif [ -n "$EXISTING" ]; then
            gh issue edit "$EXISTING" --title "GitHub Stars: $COUNT repositories requiring intervention" \
              --body-file star-sync-review.md
          else
            gh issue create --title "GitHub Stars: $COUNT repositories requiring intervention" \
              --body-file star-sync-review.md
          fi

  audit-after-admission:
    # GITHUB_TOKEN commits do not trigger ordinary push workflows. Call the
    # existing quality auditor explicitly only after a successful catalog push.
    if: always() && needs.sync.outputs.catalog_changed == 'true'
    needs: sync
    permissions:
      contents: read
      issues: write
    uses: ./.github/workflows/catalog-quality-on-change.yml
````

## File: .github/workflows/validate.yml
````yaml
name: Validate catalog

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: validate-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Compile Python utilities
        run: python -m compileall -q scripts
      - name: Test star import pipeline
        run: python scripts/test_star_import_pipeline.py
      - name: Validate permanent GitHub ID inventory without network
        run: |
          python scripts/backfill_github_ids.py --report-json /tmp/github-id-inventory.json
          python scripts/validate_json_contract.py \
            schemas/github-id-backfill-report.schema.json /tmp/github-id-inventory.json
          python - <<'PY'
          import json
          row = json.load(open('/tmp/github-id-inventory.json', encoding='utf-8'))
          assert row['mode'] == 'offline' and row['checked'] == 0
          assert row['assigned'] == 0 and row['complete'] is False
          assert row['catalogSize'] == row['previouslyVerified'] + row['missingBefore']
          assert row['missingBefore'] == row['missingAfter']
          PY
      - name: Test public GitHub Stars synchronization
        run: python scripts/test_sync_github_stars.py
      - name: Test reviewed Stars admission and repository transfers
        run: python scripts/test_auto_stars_admission.py
      - name: Validate catalog
        run: |
          python scripts/validate_catalog.py
          python scripts/validate_json_contract.py catalog.schema.json catalog.json
      - name: Validate curated website resources
        run: |
          python scripts/validate_json_contract.py schemas/websites.schema.json websites.json
      - name: Validate normalized website URLs and identities
        run: python scripts/validate_websites.py
      - name: Verify game art atlas appears in website recommendations
        run: |
          python scripts/recommend.py "game art style pixel voxel 3d" --websites --top-websites 12 --json > /tmp/game-art-websites.json
          python -c 'import json; d=json.load(open("/tmp/game-art-websites.json")); assert any(s["id"] == "game-art-style" and s["integrationEligible"] is False and s["reuse"] == "reference-only" for s in d["websiteRecommendations"])'
      - name: Validate pinned agent-skill source audit offline
        run: |
          python scripts/audit_agent_skill_sources.py \
            --json-output /tmp/skill-source-offline.json \
            --markdown-output /tmp/skill-source-offline.md
          python scripts/validate_json_contract.py \
            schemas/agent-skill-source-audit.schema.json /tmp/skill-source-offline.json
          python - <<'PY'
          import json
          report = json.load(open('/tmp/skill-source-offline.json', encoding='utf-8'))
          assert report['total'] >= 20
          assert report['coverageComplete'] is False
          assert report['counts']['unchecked'] == report['total']
          assert report['sourceContentReviewed'] is False
          assert report['automaticInstallation'] is False
          PY
      - name: Validate and exercise curated Skill Issue discovery
        run: |
          python scripts/agent_skill_discovery.py
          python scripts/agent_skill_discovery.py "react frontend performance" --domain web_frontend --language TypeScript --json > /tmp/skills-react.json
          python scripts/agent_skill_discovery.py "api backend rest" --domain backend --json > /tmp/skills-api.json
          python scripts/recommend.py "mobile ui design" --skills --json > /tmp/skills-mobile.json
          python - <<'PY'
          import json
          from pathlib import Path
          react = json.loads(Path("/tmp/skills-react.json").read_text())
          api = json.loads(Path("/tmp/skills-api.json").read_text())
          mobile = json.loads(Path("/tmp/skills-mobile.json").read_text())["skillDiscovery"]
          assert react["automaticInstallation"] is False
          assert {"frontend-design", "react-best-practices"} & {x["id"] for x in react["recommendations"]}
          assert "api-design-principles" in {x["id"] for x in api["recommendations"]}
          assert "ui-ux-pro-max-skill" in {x["id"] for x in mobile["recommendations"]}
          assert all(x["integrationEligible"] is False and x["installCommand"] is None
                     for rows in (react["recommendations"], api["recommendations"], mobile["recommendations"])
                     for x in rows)
          PY
      - name: Test catalog quality audit
        run: python scripts/test_catalog_quality.py
      - name: Generate catalog quality audit
        run: python scripts/audit_catalog_quality.py > catalog-quality.json
      - name: Validate catalog quality audit contract
        run: python scripts/validate_json_contract.py schemas/catalog-quality.schema.json catalog-quality.json
      - name: Test GitHub metadata refresh resilience
        run: python scripts/test_refresh_github_metadata.py
      - name: Test targeted license backfill
        run: python scripts/test_backfill_licenses.py
      - name: Test evidence-based metadata verification
        run: python scripts/test_verify_catalog_evidence.py
      - name: Test selection guidance inference
        run: python scripts/test_selection_guidance.py
      - name: Test recommendation engine
        run: python scripts/test_recommend.py
      - name: Test evidence-backed domain routing for indexed sources
        run: python scripts/test_catalog_domain_evidence.py
      - name: Test expanded evidence-only routing and IoT projects
        run: python scripts/test_other_domain_expansion.py
      - name: Validate reviewed README evidence manifest
        run: python scripts/validate_json_contract.py schemas/readme-domain-evidence.schema.json catalog-readme-evidence.json
      - name: Test immutable README advisory routing
        run: python scripts/test_readme_domain_evidence.py
      - name: Test README evidence freshness checks
        run: python scripts/test_readme_evidence_freshness.py
      - name: Export unresolved domain evidence
        run: python scripts/report_domain_coverage.py --out domain-coverage.json > /tmp/domain-coverage-output.json
      - name: Upload domain coverage evidence
        uses: actions/upload-artifact@v4
        with:
          name: indexed-domain-coverage
          path: domain-coverage.json
          retention-days: 30
      - name: Verify full catalog discovery with no audit tier
        run: python scripts/test_full_catalog_availability.py
      - name: Functional game-production recommendations
        run: |
          python scripts/recommend.py "roblox studio luau playtesting agent" --json > /tmp/star-list-roblox.json
          python scripts/recommend.py "godot gameplay shaders vfx" --json > /tmp/star-list-godot.json
          python -c 'import json; r=json.load(open("/tmp/star-list-roblox.json")); assert r["recommendations"] and r["recommendedStack"]["name"] == "Roblox Studio Agent Production", r.get("recommendedStack")'
          python -c 'import json; r=json.load(open("/tmp/star-list-godot.json")); assert r["recommendations"] and r["recommendedStack"]["name"] == "Godot Gameplay and VFX", r.get("recommendedStack")'
      - name: Test repository health scoring
        run: python scripts/test_health_score.py
      - name: Test replacement detection
        run: python scripts/test_find_replacements.py
      - name: Test health issue renderer
        run: python scripts/test_render_health_issue.py
      - name: Generate replacement report
        run: python scripts/find_replacements.py > replacement-report.json
      - name: Validate replacement report contract
        run: python scripts/validate_json_contract.py schemas/replacement-report.schema.json replacement-report.json
      - name: Test catalog coverage analysis
        run: python scripts/test_analyze_coverage.py
      - name: Generate coverage report
        run: python scripts/analyze_coverage.py > coverage-report.json
      - name: Validate coverage report contract
        run: python scripts/validate_json_contract.py schemas/coverage-report.schema.json coverage-report.json
      - name: Test discovery watchlist
        run: python scripts/test_discovery_watchlist.py
      - name: Test discovery candidate scoring
        run: python scripts/test_discover_candidates.py
      - name: Test persistent discovery cache
        run: python scripts/test_discovery_cache.py
      - name: Test discovery cache telemetry
        run: python scripts/test_discovery_cache_stats.py
      - name: Test cache health degradation detection
        run: python scripts/test_cache_health.py
      - name: Test cache health history
        run: python scripts/test_cache_health_history.py
      - name: Test candidate admission evaluation
        run: python scripts/test_evaluate_candidates.py
      - name: Test degraded input robustness
        run: python scripts/test_degraded_inputs.py
      - name: Test pipeline JSON contracts
        run: python scripts/test_json_contracts.py
      - name: Test offline discovery pipeline integration
        run: python scripts/test_pipeline_integration.py
      - name: Test v1 documentation contract
        run: python scripts/test_documentation.py
      - name: Test discovery issue renderer
        run: python scripts/test_render_discovery_issue.py
      - name: Test persistent discovery memory
        run: python scripts/test_discovery_memory.py
      - name: Test repository trend history
        run: python scripts/test_history.py
      - name: Generate discovery watchlist
        run: python scripts/build_discovery_watchlist.py coverage-report.json > discovery-watchlist.json
      - name: Validate discovery watchlist contract
        run: python scripts/validate_json_contract.py schemas/discovery-watchlist.schema.json discovery-watchlist.json
      - name: Validate discovery cache contract
        run: python scripts/validate_json_contract.py schemas/discovery-cache.schema.json discovery-cache.json
      - name: Validate cache health history contract
        run: python scripts/validate_json_contract.py schemas/cache-health-history.schema.json cache-health-history.json
      - name: Generate catalog statistics
        run: python scripts/catalog_stats.py > catalog-stats.json
      - name: Validate catalog statistics contract
        run: python scripts/validate_json_contract.py schemas/catalog-stats.schema.json catalog-stats.json
````

## File: .serena/project.yml
````yaml
project_name: "star-list"
language_servers:
  - python
  - json
ls_workspace_folders:
  - "."
ignore_all_files_in_gitignore: true
ignored_paths:
  - "**/__pycache__/**"
  - "discovery-cache.json"
  - "health-snapshot.json"
  - "history.json"
read_only: false
encoding: utf-8
symbol_info_budget: 8
initial_prompt: |
  Use Serena's symbol and reference tools before reading whole files. Start with symbol overviews, find_symbol and find_referencing_symbols; fetch full file bodies only when required for the task. Prefer targeted edits and preserve the existing architecture.
````

## File: schemas/agent-skill-source-audit.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pinned Skill Source Metadata Audit",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "checkedAt",
    "mode",
    "total",
    "coverageComplete",
    "counts",
    "findings",
    "sourceContentReviewed",
    "automaticInstallation",
    "entries"
  ],
  "properties": {
    "schemaVersion": {
      "const": 1
    },
    "checkedAt": {
      "type": "string",
      "minLength": 1
    },
    "mode": {
      "enum": [
        "online",
        "offline"
      ]
    },
    "total": {
      "type": "integer",
      "minimum": 1
    },
    "coverageComplete": {
      "type": "boolean"
    },
    "counts": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "verified",
        "missing",
        "invalid",
        "unavailable",
        "unchecked"
      ],
      "properties": {
        "verified": {
          "type": "integer",
          "minimum": 0
        },
        "missing": {
          "type": "integer",
          "minimum": 0
        },
        "invalid": {
          "type": "integer",
          "minimum": 0
        },
        "unavailable": {
          "type": "integer",
          "minimum": 0
        },
        "unchecked": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "findings": {
      "type": "integer",
      "minimum": 0
    },
    "sourceContentReviewed": {
      "const": false
    },
    "automaticInstallation": {
      "const": false
    },
    "entries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "id",
          "sourceRepository",
          "sourceCommit",
          "sourcePath",
          "sourceUrl",
          "status",
          "reason"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          },
          "sourceRepository": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "sourceCommit": {
            "type": "string",
            "pattern": "^[a-f0-9]{40}$"
          },
          "sourcePath": {
            "type": "string",
            "pattern": "^(?:[A-Za-z0-9_.-]+/)*SKILL[.]md$"
          },
          "sourceUrl": {
            "type": "string",
            "pattern": "^https://github[.]com/"
          },
          "status": {
            "enum": [
              "verified",
              "missing",
              "invalid",
              "unavailable",
              "unchecked"
            ]
          },
          "reason": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}
````

## File: schemas/cache-health-history.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health History","type":"object","required":["schemaVersion","points"],"properties":{"schemaVersion":{"type":"integer","const":1},"points":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health History Point","type":"object","required":["date","status","logicalRequests","apiCallAvoidanceRate","bodyReuseRate","networkFetchRate","staleFallbackRate"],"properties":{"date":{"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"},"status":{"enum":["healthy","watch","degraded","unknown"]},"logicalRequests":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"staleFallbackRate":{"type":"number","minimum":0,"maximum":1},"candidateSeverity":{"enum":["healthy","watch","degraded"]},"alertState":{"enum":["healthy","watch","degraded"]},"issueAction":{"enum":["open","hold","close"]}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/cache-health-trend.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Trend","type":"object","required":["direction","findings","windowPoints","apiCallAvoidanceDelta","networkFetchDelta","adaptiveBaseline","adaptiveSeverity","candidateSeverity","alertState","issueAction"],"properties":{"direction":{"enum":["insufficient-data","declining","stable","improving"]},"findings":{"type":"array","items":{"type":"string"}},"windowPoints":{"type":"integer","minimum":0},"apiCallAvoidanceDelta":{"type":["number","null"]},"networkFetchDelta":{"type":["number","null"]},"bodyReuseDelta":{"type":["number","null"]},"fromDate":{"type":["string","null"]},"toDate":{"type":["string","null"]},"adaptiveBaseline":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Adaptive Cache Baseline","type":"object","required":["status","sampleSize","threshold","confidence","confidenceScore","findings"],"properties":{"status":{"enum":["insufficient-data","normal","anomalous"]},"sampleSize":{"type":"integer","minimum":0},"threshold":{"type":"number","minimum":0},"confidence":{"enum":["insufficient-data","low","medium","high"]},"confidenceScore":{"type":"number","minimum":0,"maximum":1},"findings":{"type":"array","items":{"type":"string"}},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"deltas":{"type":"object","additionalProperties":{"type":"number"}}},"additionalProperties":true},"adaptiveSeverity":{"enum":["healthy","watch","degraded"]},"candidateSeverity":{"enum":["healthy","watch","degraded"]},"alertState":{"enum":["healthy","watch","degraded"]},"issueAction":{"enum":["open","hold","close"]}},"additionalProperties":false}
````

## File: schemas/cache-health.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Report","type":"object","required":["status","findings","metrics"],"properties":{"status":{"enum":["healthy","watch","degraded"]},"findings":{"type":"array","items":{"type":"string"}},"metrics":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Metrics","type":"object","required":["logicalRequests","freshCacheHits","notModifiedHits","staleFallbacks","networkFetches","apiCallAvoidanceRate","bodyReuseRate","networkFetchRate","staleFallbackRate"],"properties":{"logicalRequests":{"type":"integer","minimum":0},"freshCacheHits":{"type":"integer","minimum":0},"notModifiedHits":{"type":"integer","minimum":0},"staleFallbacks":{"type":"integer","minimum":0},"networkFetches":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"staleFallbackRate":{"type":"number","minimum":0,"maximum":1}},"additionalProperties":false}},"additionalProperties":false}
````

## File: schemas/catalog-quality.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Catalog Quality Audit",
  "type": "object",
  "required": [
    "staleDays",
    "repositories",
    "summary",
    "guidanceCoverage",
    "identityCoverage",
    "findings"
  ],
  "properties": {
    "staleDays": {
      "type": "integer",
      "minimum": 1
    },
    "repositories": {
      "type": "integer",
      "minimum": 0
    },
    "summary": {
      "type": "object",
      "required": [
        "findings",
        "review",
        "info",
        "byCode"
      ],
      "properties": {
        "findings": {
          "type": "integer",
          "minimum": 0
        },
        "review": {
          "type": "integer",
          "minimum": 0
        },
        "info": {
          "type": "integer",
          "minimum": 0
        },
        "byCode": {
          "type": "object",
          "additionalProperties": {
            "type": "integer",
            "minimum": 0
          }
        }
      },
      "additionalProperties": false
    },
    "guidanceCoverage": {
      "type": "object",
      "required": [
        "bestFor",
        "avoidWhen",
        "alternatives",
        "complements"
      ],
      "properties": {
        "bestFor": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "avoidWhen": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "alternatives": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "complements": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "identityCoverage": {
      "type": "object",
      "required": ["verified", "missing"],
      "properties": {
        "verified": {"type": "integer", "minimum": 0},
        "missing": {"type": "integer", "minimum": 0}
      },
      "additionalProperties": false
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repo",
          "severity",
          "code",
          "message"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "minLength": 1
          },
          "severity": {
            "enum": [
              "review",
              "info"
            ]
          },
          "code": {
            "type": "string",
            "minLength": 1
          },
          "message": {
            "type": "string",
            "minLength": 1
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
````

## File: schemas/catalog-stats.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Catalog Statistics","type":"object","required":["repositories","averageScore","selfHosted","selfHostedPercent","domains","tiers","topLanguages","topPlatforms","topCapabilities","domainLeaders"],"properties":{"repositories":{"type":"integer","minimum":0},"averageScore":{"type":"number"},"selfHosted":{"type":"integer","minimum":0},"selfHostedPercent":{"type":"number","minimum":0,"maximum":100},"domains":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"tiers":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topLanguages":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topPlatforms":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topCapabilities":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"domainLeaders":{"type":"object","additionalProperties":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Domain Leader","type":"object","required":["repo","score","tier"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"score":{"type":["number","null"]},"tier":{"type":["string","null"]}},"additionalProperties":false}}}},"additionalProperties":false}
````

## File: schemas/coverage-report.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Report","type":"object","required":["policy","domainGaps","capabilityGaps","qualityGaps","summary"],"properties":{"policy":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Policy","type":"object","required":["minHealthyPerDomain","minHealthyPerCapability"],"properties":{"minHealthyPerDomain":{"type":"integer","minimum":1},"minHealthyPerCapability":{"type":"integer","minimum":1}},"additionalProperties":false},"domainGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Domain Gap","type":"object","required":["domain","total","healthy","deficit","severity"],"properties":{"domain":{"type":"string","minLength":1},"total":{"type":"integer","minimum":0},"healthy":{"type":"integer","minimum":0},"deficit":{"type":"integer","minimum":0},"severity":{"enum":["critical","warning"]}},"additionalProperties":false}},"capabilityGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Capability Gap","type":"object","required":["capability","total","healthy","deficit","severity"],"properties":{"capability":{"type":"string","minLength":1},"total":{"type":"integer","minimum":0},"healthy":{"type":"integer","minimum":0},"deficit":{"type":"integer","minimum":0},"severity":{"enum":["critical","warning"]}},"additionalProperties":false}},"qualityGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Quality Gap","type":"object","required":["domain","repositories","issue"],"properties":{"domain":{"type":"string","minLength":1},"repositories":{"type":"integer","minimum":0},"issue":{"type":"string","minLength":1}},"additionalProperties":false}},"summary":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Summary","type":"object","required":["domains","capabilities","domainGaps","capabilityGaps","qualityGaps"],"properties":{"domains":{"type":"integer","minimum":0},"capabilities":{"type":"integer","minimum":0},"domainGaps":{"type":"integer","minimum":0},"capabilityGaps":{"type":"integer","minimum":0},"qualityGaps":{"type":"integer","minimum":0}},"additionalProperties":false}},"additionalProperties":false}
````

## File: schemas/discovery-cache.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache","type":"object","required":["schemaVersion","entries"],"properties":{"schemaVersion":{"type":"integer","const":1},"entries":{"type":"object","additionalProperties":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache Entry","type":"object","required":["fetchedAt","data","headers"],"properties":{"fetchedAt":{"type":"number","minimum":0},"data":{},"headers":{"type":"object"}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/discovery-candidates.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Candidates","type":"object","required":["candidates","repositories","errors","staleSources","cacheStats"],"properties":{"candidates":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"type":"object","required":["repo","stars","forks","discoveryScore","matchedTargets"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"url":{"type":["string","null"]},"description":{"type":["string","null"]},"stars":{"type":"integer","minimum":0},"forks":{"type":"integer","minimum":0},"language":{"type":["string","null"]},"license":{"type":["string","null"]},"pushedAt":{"type":["string","null"]},"discoveryScore":{"type":"number","minimum":0,"maximum":100},"matchedTargets":{"type":"array","minItems":1,"items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Matched Target","type":"object","required":["kind","target","priority"],"properties":{"kind":{"type":"string","minLength":1},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0}},"additionalProperties":false}},"topics":{"type":"array","items":{"type":"string"}},"watchers":{"type":"integer","minimum":0},"size":{"type":["integer","null"],"minimum":0},"openIssues":{"type":"integer","minimum":0},"createdAt":{"type":["string","null"]},"homepage":{"type":["string","null"]},"hasDiscussions":{"type":"boolean"},"latestRelease":{"type":["object","null"]},"contributors":{"type":["integer","null"],"minimum":0},"metadataStale":{"type":"boolean"},"staleEndpoints":{"type":"array","items":{"type":"string"}},"enrichmentError":{"type":"string"}},"additionalProperties":true}},"errors":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Error","type":"object","required":["target","error"],"properties":{"target":{"type":"string","minLength":1},"error":{"type":"string","minLength":1}},"additionalProperties":false}},"staleSources":{"type":"array","items":{"type":"object"}},"cacheStats":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache Stats","type":"object","required":["logicalRequests","freshCacheHits","notModifiedHits","staleFallbacks","networkFetches","apiCallAvoidanceRate","bodyReuseRate"],"properties":{"logicalRequests":{"type":"integer","minimum":0},"freshCacheHits":{"type":"integer","minimum":0},"notModifiedHits":{"type":"integer","minimum":0},"staleFallbacks":{"type":"integer","minimum":0},"networkFetches":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1}},"additionalProperties":true}},"additionalProperties":false}
````

## File: schemas/discovery-evaluated.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluated Discovery Candidates","type":"object","required":["candidates","counts","repositories","errors"],"properties":{"candidates":{"type":"integer","minimum":0},"counts":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluation Counts","type":"object","required":["accept","review","reject"],"properties":{"accept":{"type":"integer","minimum":0},"review":{"type":"integer","minimum":0},"reject":{"type":"integer","minimum":0}},"additionalProperties":false},"repositories":{"type":"array","items":{"type":"object","required":["repo","evaluationScore","decision","scoreBreakdown","evaluationConfidence","reasons"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"url":{"type":["string","null"]},"description":{"type":["string","null"]},"stars":{"type":"integer","minimum":0},"forks":{"type":"integer","minimum":0},"language":{"type":["string","null"]},"license":{"type":["string","null"]},"pushedAt":{"type":["string","null"]},"discoveryScore":{"type":"number","minimum":0,"maximum":100},"matchedTargets":{"type":"array","minItems":1,"items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Matched Target","type":"object","required":["kind","target","priority"],"properties":{"kind":{"type":"string","minLength":1},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0}},"additionalProperties":false}},"topics":{"type":"array","items":{"type":"string"}},"watchers":{"type":"integer","minimum":0},"size":{"type":["integer","null"],"minimum":0},"openIssues":{"type":"integer","minimum":0},"createdAt":{"type":["string","null"]},"homepage":{"type":["string","null"]},"hasDiscussions":{"type":"boolean"},"latestRelease":{"type":["object","null"]},"contributors":{"type":["integer","null"],"minimum":0},"metadataStale":{"type":"boolean"},"staleEndpoints":{"type":"array","items":{"type":"string"}},"enrichmentError":{"type":"string"},"evaluationScore":{"type":"number","minimum":0,"maximum":100},"decision":{"enum":["accept","review","reject"]},"ageDays":{"type":["integer","null"],"minimum":0},"repositoryAgeDays":{"type":["integer","null"],"minimum":0},"releaseAgeDays":{"type":["integer","null"],"minimum":0},"textFit":{"type":"number","minimum":0,"maximum":1},"openIssueRatio":{"type":["number","null"],"minimum":0},"scoreBreakdown":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluation Score Breakdown","type":"object","required":["fit","activity","adoption","maturity","maintenance"],"properties":{"fit":{"type":"number","minimum":0,"maximum":100},"activity":{"type":"number","minimum":0,"maximum":100},"adoption":{"type":"number","minimum":0,"maximum":100},"maturity":{"type":"number","minimum":0,"maximum":100},"maintenance":{"type":"number","minimum":0,"maximum":100}},"additionalProperties":false},"evaluationConfidence":{"enum":["low","medium","high"]},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":true}},"errors":{"type":"array"},"suppressedUnchanged":{"type":"integer","minimum":0}},"additionalProperties":false}
````

## File: schemas/discovery-memory.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Memory","type":"object","required":["schemaVersion","candidates"],"properties":{"schemaVersion":{"type":"integer","const":1},"candidates":{"type":"object","additionalProperties":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Memory Entry","type":"object","required":["fingerprint","lastSeenAt"],"properties":{"fingerprint":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Candidate Fingerprint","type":"object","required":["decision","score","stars","pushedAt","targets"],"properties":{"decision":{"enum":["accept","review","reject"]},"score":{"type":"number","minimum":0,"maximum":100},"stars":{"type":"integer","minimum":0},"pushedAt":{"type":["string","null"]},"targets":{"type":"array","items":{"type":"array","minItems":2,"maxItems":2}}},"additionalProperties":false},"lastSeenAt":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/discovery-watchlist.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Watchlist","type":"object","required":["items","watchlist"],"properties":{"items":{"type":"integer","minimum":0},"watchlist":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Watch Item","type":"object","required":["kind","target","priority","query","reason"],"properties":{"kind":{"enum":["domain","capability","quality"]},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0},"query":{"type":"string","minLength":1},"reason":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/github-id-backfill-report.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Permanent GitHub Repository ID Backfill Report",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "mode",
    "catalogSize",
    "previouslyVerified",
    "missingBefore",
    "checked",
    "assigned",
    "missingAfter",
    "complete",
    "unresolved"
  ],
  "properties": {
    "mode": {
      "enum": [
        "online",
        "offline"
      ]
    },
    "catalogSize": {
      "type": "integer",
      "minimum": 0
    },
    "previouslyVerified": {
      "type": "integer",
      "minimum": 0
    },
    "missingBefore": {
      "type": "integer",
      "minimum": 0
    },
    "checked": {
      "type": "integer",
      "minimum": 0
    },
    "assigned": {
      "type": "integer",
      "minimum": 0
    },
    "missingAfter": {
      "type": "integer",
      "minimum": 0
    },
    "complete": {
      "type": "boolean"
    },
    "unresolved": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "repo",
          "reason"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "reason": {
            "enum": [
              "not-found",
              "renamed-or-transferred",
              "invalid-or-private",
              "identity-conflict"
            ]
          }
        }
      }
    },
    "error": {
      "type": "string",
      "minLength": 1
    }
  }
}
````

## File: schemas/health-drift.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Drift","type":"object","required":["dropThreshold","findings","repositories"],"properties":{"dropThreshold":{"type":"number","minimum":0},"findings":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Drift Finding","type":"object","required":["repo","previousScore","currentScore","delta","previousStatus","currentStatus"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"previousScore":{"type":"number","minimum":0,"maximum":100},"currentScore":{"type":"number","minimum":0,"maximum":100},"delta":{"type":"number"},"previousStatus":{"type":"string","minLength":1},"currentStatus":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/health-snapshot.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Snapshot","type":"object","required":["repositories"],"properties":{"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository Health","type":"object","required":["repo","score","status","reasons"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"enum":["unknown","inactive","healthy","watch","weak"]},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/health-trends.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trends","type":"object","required":["repositories"],"properties":{"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository Trend","type":"object","required":["repo","trend","week","fourWeeks","full"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"trend":{"enum":["stable","declining","improving","growing"]},"week":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false},"fourWeeks":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false},"full":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/history.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository History","type":"object","required":["schemaVersion","repositories"],"properties":{"schemaVersion":{"type":"integer","const":1},"repositories":{"type":"object","additionalProperties":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository History Point","type":"object","required":["date","health","status","stars","forks"],"properties":{"date":{"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"},"health":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":["string","null"]},"stars":{"type":["integer","null"],"minimum":0},"forks":{"type":["integer","null"],"minimum":0}},"additionalProperties":false}}}},"additionalProperties":false}
````

## File: schemas/metadata-evidence.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List evidence audit",
  "type": "object",
  "required": [
    "generatedAt",
    "catalogSize",
    "uncertainEntries",
    "selected",
    "inspected",
    "counts",
    "results",
    "updates",
    "errors",
    "batchIndex",
    "wroteCatalog"
  ],
  "properties": {
    "generatedAt": {
      "type": "string",
      "minLength": 1
    },
    "catalogSize": {
      "type": "integer",
      "minimum": 0
    },
    "uncertainEntries": {
      "type": "integer",
      "minimum": 0
    },
    "selected": {
      "type": "integer",
      "minimum": 0
    },
    "inspected": {
      "type": "integer",
      "minimum": 0
    },
    "batchIndex": {
      "type": "integer",
      "minimum": 0
    },
    "wroteCatalog": {
      "type": "boolean"
    },
    "counts": {
      "type": "object",
      "required": [
        "verifiedRootLicenses",
        "githubClaimsOnly",
        "hostingCandidates",
        "proposedLicenseUpdates",
        "appliedUpdates",
        "errors",
        "scopedLicenses"
      ],
      "properties": {
        "verifiedRootLicenses": {
          "type": "integer",
          "minimum": 0
        },
        "githubClaimsOnly": {
          "type": "integer",
          "minimum": 0
        },
        "hostingCandidates": {
          "type": "integer",
          "minimum": 0
        },
        "proposedLicenseUpdates": {
          "type": "integer",
          "minimum": 0
        },
        "appliedUpdates": {
          "type": "integer",
          "minimum": 0
        },
        "errors": {
          "type": "integer",
          "minimum": 0
        },
        "scopedLicenses": {
          "type": "integer",
          "minimum": 0
        }
      },
      "additionalProperties": false
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "repositoryId",
          "defaultBranch",
          "license",
          "hosting",
          "proposedLicense"
        ],
        "properties": {
          "repository": {
            "type": "string",
            "pattern": "^[^/]+/[^/]+$"
          },
          "repositoryId": {
            "type": "integer",
            "minimum": 1
          },
          "defaultBranch": {
            "type": "string",
            "minLength": 1
          },
          "proposedLicense": {
            "type": [
              "string",
              "null"
            ]
          },
          "license": {
            "type": "object",
            "required": [
              "status",
              "value",
              "evidence"
            ],
            "properties": {
              "status": {
                "enum": [
                  "unverified",
                  "verified-root-file",
                  "github-claim-only",
                  "conflict",
                  "scoped-licensing-review"
                ]
              },
              "value": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "method",
                    "value",
                    "url"
                  ],
                  "properties": {
                    "method": {
                      "enum": [
                        "github-repository-spdx",
                        "root-license-signature",
                        "root-license-scope-warning"
                      ]
                    },
                    "value": {
                      "type": "string"
                    },
                    "path": {
                      "type": "string"
                    },
                    "blobSha": {
                      "type": "string",
                      "pattern": "^[a-f0-9]{40}$"
                    },
                    "url": {
                      "type": "string",
                      "pattern": "^https://api.github.com/repos/"
                    }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "hosting": {
            "type": "object",
            "required": [
              "status",
              "evidence"
            ],
            "properties": {
              "status": {
                "enum": [
                  "unverified",
                  "deployment-file-present-review-required"
                ]
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "method",
                    "path",
                    "blobSha",
                    "url"
                  ],
                  "properties": {
                    "method": {
                      "const": "compose-root-file"
                    },
                    "path": {
                      "type": "string"
                    },
                    "blobSha": {
                      "type": "string",
                      "pattern": "^[a-f0-9]{40}$"
                    },
                    "url": {
                      "type": "string",
                      "pattern": "^https://api.github.com/repos/"
                    }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          }
        },
        "additionalProperties": false
      }
    },
    "updates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "license",
          "evidence"
        ],
        "properties": {
          "repository": {
            "type": "string"
          },
          "license": {
            "type": "string"
          },
          "evidence": {
            "type": "string",
            "pattern": "^https://api.github.com/repos/"
          }
        },
        "additionalProperties": false
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "error"
        ],
        "properties": {
          "repository": {
            "type": "string"
          },
          "error": {
            "type": "string"
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
````

## File: schemas/readme-domain-evidence.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List reviewed upstream README evidence",
  "type": "object",
  "required": [
    "schemaVersion",
    "sourceType",
    "sources"
  ],
  "properties": {
    "schemaVersion": {
      "const": 1
    },
    "sourceType": {
      "const": "reviewed-readme-blob"
    },
    "sources": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "repository",
          "githubRepositoryId",
          "path",
          "blobSha",
          "advisoryDomains",
          "taskTerms",
          "evidenceSnippet",
          "reviewNotes"
        ],
        "properties": {
          "repository": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$"
          },
          "githubRepositoryId": {
            "type": "integer",
            "minimum": 1
          },
          "path": {
            "const": "README.md"
          },
          "blobSha": {
            "type": "string",
            "pattern": "^[a-f0-9]{40}$"
          },
          "advisoryDomains": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "uniqueItems": true,
            "items": {
              "enum": [
                "ai_media",
                "ai_agents",
                "data_ml",
                "graphics",
                "game_dev",
                "marketing",
                "software_engineering",
                "writing",
                "productivity",
                "backend",
                "web_frontend",
                "embedded_iot",
                "education",
                "cybersecurity",
                "ai_memory",
                "devops"
              ]
            }
          },
          "taskTerms": {
            "type": "array",
            "minItems": 1,
            "maxItems": 10,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "pattern": "^[a-z0-9-]+$"
            }
          },
          "evidenceSnippet": {
            "type": "string",
            "minLength": 3
          },
          "reviewNotes": {
            "type": "string",
            "minLength": 5
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
````

## File: schemas/replacement-report.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Report","type":"object","required":["threshold","findings","repositories"],"properties":{"threshold":{"type":"number","minimum":0,"maximum":100},"findings":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Finding","type":"object","required":["repo","health","qualityScore","domain","suggestedReplacements"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]},"suggestedReplacements":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Candidate","type":"object","required":["repo","replacementScore","health","qualityScore","domain"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"replacementScore":{"type":"number","minimum":0},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]}},"additionalProperties":false}}},"additionalProperties":false}}},"additionalProperties":false}
````

## File: schemas/star-sync-report.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Public GitHub Stars review report",
  "type": "object",
  "required": [
    "schemaVersion",
    "username",
    "checkedAt",
    "source",
    "summary",
    "newRepositories"
  ],
  "properties": {
    "schemaVersion": {
      "type": "integer",
      "const": 1
    },
    "username": {
      "type": "string",
      "minLength": 1
    },
    "checkedAt": {
      "type": "string",
      "minLength": 10
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "summary": {
      "type": "object",
      "required": [
        "starred",
        "alreadyCataloged",
        "new",
        "pages",
        "duplicateApiItems"
      ],
      "properties": {
        "starred": {
          "type": "integer",
          "minimum": 0
        },
        "alreadyCataloged": {
          "type": "integer",
          "minimum": 0
        },
        "new": {
          "type": "integer",
          "minimum": 0
        },
        "pages": {
          "type": "integer",
          "minimum": 0
        },
        "duplicateApiItems": {
          "type": "integer",
          "minimum": 0
        }
      },
      "additionalProperties": false
    },
    "newRepositories": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repo",
          "url",
          "stars",
          "language",
          "license",
          "archived",
          "disabled",
          "pushedAt"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "pattern": "^[^/]+/[^/]+$"
          },
          "url": {
            "type": "string",
            "pattern": "^https://github[.]com/"
          },
          "stars": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 0
          },
          "language": {
            "type": [
              "string",
              "null"
            ]
          },
          "license": {
            "type": [
              "string",
              "null"
            ]
          },
          "archived": {
            "type": "boolean"
          },
          "disabled": {
            "type": "boolean"
          },
          "pushedAt": {
            "type": [
              "string",
              "null"
            ]
          },
          "githubRepositoryId": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 1
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
````

## File: schemas/websites.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List Curated Website Resources",
  "type": "object",
  "required": [
    "schemaVersion",
    "websites"
  ],
  "additionalProperties": false,
  "properties": {
    "schemaVersion": {
      "type": "integer",
      "const": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "websites": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "name",
          "url",
          "type",
          "access",
          "domains",
          "tags",
          "bestFor",
          "reuse",
          "caution"
        ],
        "additionalProperties": false,
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          },
          "name": {
            "type": "string",
            "minLength": 2
          },
          "url": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/?(?:[^\\s]*)?$"
          },
          "originalUrl": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/?(?:[^\\s]*)?$"
          },
          "type": {
            "enum": [
              "inspiration-gallery",
              "motion-gallery",
              "component-marketplace",
              "component-library",
              "prompt-template-library",
              "framework-docs",
              "shader-gallery",
              "hosted-builder",
              "agent-skills-directory",
              "mcp-service",
              "npc-platform",
              "narrative-platform",
              "game-design-service",
              "asset-generator",
              "game-testing-service",
              "model-collection",
              "model-checkpoint",
              "model-hub",
              "marketing-automation-service",
              "animation-reference-library",
              "film-stills-library",
              "3d-pose-reference-tool",
              "costume-history-atlas",
              "ai-media-generator",
              "3d-asset-dataset"
            ]
          },
          "access": {
            "enum": [
              "free",
              "freemium",
              "paid",
              "unknown"
            ]
          },
          "domains": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "enum": [
                "web_frontend",
                "graphics",
                "mobile",
                "game_dev",
                "software_engineering",
                "ai_agents",
                "ai_media",
                "other",
                "marketing",
                "writing"
              ]
            }
          },
          "tags": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 2
            }
          },
          "bestFor": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 3
            }
          },
          "reuse": {
            "enum": [
              "reference-only",
              "license-per-item",
              "licensed-material",
              "open-source-upstream",
              "hosted-service"
            ]
          },
          "caution": {
            "type": "string",
            "minLength": 10
          },
          "mcpEndpoint": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/mcp$"
          },
          "portfolioBaselineDomains": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "enum": [
                "web_frontend",
                "graphics",
                "mobile",
                "game_dev",
                "software_engineering",
                "ai_agents",
                "ai_media",
                "other",
                "marketing",
                "writing"
              ]
            }
          },
          "portfolioRequiredSignals": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 2
            }
          },
          "sourceLicenseTag": {
            "type": "string",
            "minLength": 2
          },
          "upstreamModel": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "safetyRisk": {
            "enum": [
              "reduced-refusal",
              "unknown",
              "standard"
            ]
          },
          "supportedLanguages": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "pattern": "^[a-z]{2}(?:-[A-Z]{2})?$"
            }
          }
        }
      }
    }
  }
}
````

## File: scripts/admit_github_stars.py
````python
#!/usr/bin/env python3
"""Admit every accessible starred repository into the catalog, conservatively.

New entries receive an audit tier until a human or richer analysis verifies
license terms, suitability, and production readiness. Never silently skip a
Star or save a partly built catalog.
"""
⋮----
DOMAINS = (
CATEGORIES = {
⋮----
def classify(meta)
⋮----
text = " ".join([
⋮----
def get_repo(repo, token=None, opener=SAFE_GITHUB_HTTP.open, sleeper=time.sleep)
⋮----
"""Fetch full repository metadata, with bounded retry and canonical ID check."""
⋮----
url = "https://api.github.com/repos/" + repo
headers = {
⋮----
result = json.load(response)
⋮----
raw_delay = exc.headers.get("Retry-After", str(2 ** attempt))
⋮----
delay = min(20, max(0, float(raw_delay)))
⋮----
delay = float(2 ** attempt)
⋮----
def catalog_entry(meta)
⋮----
repo = meta.get("full_name")
⋮----
repo_id = meta.get("id")
⋮----
license_data = meta.get("license")
license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else None
⋮----
license_id = None
⋮----
def count(key)
⋮----
value = meta.get(key)
⋮----
branch = meta.get("default_branch")
⋮----
branch = "unknown"  # Nonempty schema value; indexed entries retain an explicit metadata gap.
domain = classify(meta)
language = meta.get("language")
languages = [language.lower()] if isinstance(language, str) and language.strip() else []
description = meta.get("description")
guidance = [re.sub(r"\s+", " ", description).strip()[:200]] if isinstance(description, str) and description.strip() else []
topics = meta.get("topics")
capabilities = [x[:80] for x in topics if isinstance(x, str) and x.strip()][:12] if isinstance(topics, list) else []
⋮----
def manifest_stable_ids(manifest, report)
⋮----
"""Verify that all identity rows belong to the exact read-only Stars scan."""
⋮----
summary = report.get("summary")
⋮----
expected_new = report.get("newRepositories")
⋮----
ids = {}
owners = {}
⋮----
key = normalize_repo(name)
rid = row.get("githubRepositoryId")
⋮----
key = normalize_repo(star["repo"])
⋮----
def admit(catalog, stars, fetcher, known_star_ids=None)
⋮----
"""Reconcile by both canonical name and permanent ID; fail on any ambiguity."""
old = catalog.get("repositories")
⋮----
by_name = {normalize_repo(x["repo"]): x.get("githubRepositoryId") for x in old}
by_id = {x["githubRepositoryId"] for x in old if type(x.get("githubRepositoryId")) is int}
⋮----
fresh = []
already = 0
transfers = []
⋮----
rid = star.get("githubRepositoryId")
recorded_id = by_name.get(key)
⋮----
# Re-check even when a stale read-only report reached admission:
# a recycled owner/name is not the same GitHub repository.
⋮----
meta = fetcher(star["repo"])
entry = catalog_entry(meta)
⋮----
canonical = normalize_repo(entry["repo"])
⋮----
previous_id = by_name[canonical]
⋮----
result = dict(catalog)
# Do not mutate the caller's loaded catalog before all checks pass.
entries = [dict(row) for row in old] + sorted(fresh, key=lambda r: r["repo"].lower())
enriched = 0
⋮----
rows_by_name = {normalize_repo(row["repo"]): row for row in entries}
rows_by_id = {
⋮----
key = normalize_repo(original_name)
⋮----
entry = rows_by_name.get(key)
⋮----
# An existing repository may have transferred to this new
# owner/name while preserving its stable ID.
⋮----
recorded_id = entry.get("githubRepositoryId")
⋮----
occupied = rows_by_id.get(rid)
⋮----
def main(argv=None)
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args(argv)
⋮----
report = json.loads(args.sync_report.read_text(encoding="utf-8"))
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
⋮----
# A report lists only missing Stars. The manifest provides the complete
# snapshot, and admission operates on a report produced in the same job.
stars = report.get("newRepositories")
⋮----
known_star_ids = None
⋮----
manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
known_star_ids = manifest_stable_ids(manifest, report)
token = os.environ.get("GITHUB_TOKEN")
````

## File: scripts/agent_skill_discovery.py
````python
#!/usr/bin/env python3
"""Offline, read-only Skill Issue skill discovery for repository agents.

A directory entry or an upstream repository is not authority to execute
unreviewed SKILL.md instructions, install scripts or network commands.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "agent-skills.json"
SKILL_ISSUE_URL = "https://skill-issue.in/"
VALID_DOMAINS = {
⋮----
def word_set(value: str) -> set[str]
⋮----
def load_skills() -> dict
⋮----
data = json.loads(CATALOG.read_text(encoding="utf-8"))
⋮----
directory = data.get("directory")
⋮----
skills = data.get("skills")
⋮----
ids = set()
⋮----
identifier = row.get("id")
⋮----
name = row.get("name")
description = row.get("description")
⋮----
repo = row.get("sourceRepository")
⋮----
expected = "https://github.com/" + repo
⋮----
url = urlsplit(expected)
⋮----
# The exact SKILL.md path is independently confirmed on a pinned
# upstream revision, rather than delegating review to a mutable repo root.
⋮----
"""Rank skill *references* by declared domain and concrete repo labels.

    Never treat broad README prose as verified compatibility and never return
    shell installers or instructions for agent execution.
    """
source = load_skills()
⋮----
words = set().union(*(word_set(term) for term in terms))
selected = []
⋮----
matched_domains = sorted(set(item["domains"]) & domains)
matched_tags = sorted(set(item["tags"]) & words)
⋮----
languages = {x.casefold() for x in item["languages"]}
⋮----
# An explicit relevant framework term is stronger evidence than
# GitHub's single primary language, but general domain is not.
explicit = {"react", "nextjs", "remotion"} & set(matched_tags)
⋮----
score = 8 * len(matched_domains) + 5 * len(matched_tags)
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args()
⋮----
catalog = load_skills()
matched = recommend_skills(word_set(args.query), set(args.domain), language=args.language, limit=args.top)
output = {
````

## File: scripts/analyze_cache_health.py
````python
#!/usr/bin/env python3
"""Classify discovery-cache efficiency and render an actionable health report."""
⋮----
def _ratio(value, total)
⋮----
def analyze(stats)
⋮----
logical=max(0,int(stats.get("logicalRequests",0) or 0))
fresh=max(0,int(stats.get("freshCacheHits",0) or 0))
not_modified=max(0,int(stats.get("notModifiedHits",0) or 0))
stale=max(0,int(stats.get("staleFallbacks",0) or 0))
network=max(0,int(stats.get("networkFetches",0) or 0))
avoidance=float(stats.get("apiCallAvoidanceRate",_ratio(fresh,logical)) or 0.0)
body_reuse=float(stats.get("bodyReuseRate",_ratio(fresh+not_modified+stale,logical)) or 0.0)
network_ratio=_ratio(network,logical)
stale_ratio=_ratio(stale,logical)
⋮----
findings=[]
severe=False
⋮----
severe=True
⋮----
status="degraded" if severe else "watch" if findings else "healthy"
⋮----
def render_markdown(report)
⋮----
m=report["metrics"]
lines=[
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
data=json.loads(args.discovery_report.read_text())
report=analyze(data.get("cacheStats",{}))
````

## File: scripts/analyze_coverage.py
````python
#!/usr/bin/env python3
"""Analyze catalog coverage and surface functional blind spots."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"catalog.json"
⋮----
def analyze(repos, min_domain=3, min_capability=2)
⋮----
domains=Counter(r.get("domain","other") for r in repos)
caps=Counter(c for r in repos for c in r.get("capabilities",[]))
healthy_domains=Counter()
healthy_caps=Counter()
by_domain=defaultdict(list)
⋮----
h=health_score(r)
usable=h["status"] not in {"inactive","weak"} if h["score"] is not None else True
⋮----
domain_gaps=[]
⋮----
healthy=healthy_domains[domain]
⋮----
capability_gaps=[]
⋮----
healthy=healthy_caps[cap]
⋮----
concentration=[]
⋮----
total=len(items)
top_tier=sum(r.get("tier") in {"core","recommended"} for r in items)
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
repos=json.loads(CATALOG.read_text()).get("repositories",[])
````

## File: scripts/audit_agent_skill_sources.py
````python
#!/usr/bin/env python3
"""Check immutable upstream SKILL.md links without executing remote instructions.

Offline mode validates local pinned-source contracts only. Online mode checks
GitHub API *file metadata*, never imports, executes or trusts remote SKILL.md.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "star-list-pinned-skill-source-audit/1.0"
MAX_RESPONSE = 500_000
⋮----
class RejectRedirect(HTTPRedirectHandler)
⋮----
"""Never forward a GitHub bearer token to a redirected URL."""
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
HTTP = build_opener(RejectRedirect())
⋮----
def inspect_source(row: dict, token: str) -> tuple[str, str]
⋮----
"""Check the pinned SKILL.md file metadata; never read/parse its instructions."""
⋮----
path = "/".join(quote(part, safe="") for part in row["sourcePath"].split("/"))
url = ("https://api.github.com/repos/" + quote(owner, safe="")
headers = {
⋮----
payload = response.read(MAX_RESPONSE + 1)
⋮----
value = json.loads(payload.decode("utf-8"))
⋮----
def make_report(*, online: bool, token: str) -> dict
⋮----
rows = load_skills()["skills"]
entries = []
⋮----
counts = {status: sum(item["status"] == status for item in entries)
complete = online and counts["unavailable"] == 0 and counts["unchecked"] == 0
⋮----
def markdown(report: dict) -> str
⋮----
counts = report["counts"]
lines = [
failures = [e for e in report["entries"] if e["status"] in ("missing", "invalid", "unavailable")]
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args()
report = make_report(online=args.online, token=os.environ.get("GITHUB_TOKEN", ""))
data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
````

## File: scripts/audit_catalog_quality.py
````python
#!/usr/bin/env python3
"""Audit catalog maintenance debt without mutating catalog.json."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
SEVERITY_ORDER = {"review": 0, "info": 1}
⋮----
def _age_days(value, now)
⋮----
pushed = datetime.fromisoformat(value.replace("Z", "+00:00"))
⋮----
pushed = pushed.replace(tzinfo=timezone.utc)
⋮----
def analyze(repos, stale_days=730, now=None)
⋮----
now = now or datetime.now(timezone.utc)
findings = []
guidance_fields = ("bestFor", "avoidWhen", "alternatives", "complements")
⋮----
def add(repo, severity, code, message)
⋮----
name = entry.get("repo", "<unknown>")
gh = entry.get("github")
⋮----
tier = entry.get("tier")
lifecycle = entry.get("lifecycle")
⋮----
code = f"archived-{lifecycle or 'indexed'}-retained"
label = lifecycle or "indexed"
⋮----
age = _age_days(gh.get("pushedAt"), now)
⋮----
license_name = gh.get("license")
⋮----
license_status = entry.get("licenseStatus")
status_messages = {
⋮----
severity_counts = Counter(row["severity"] for row in findings)
code_counts = Counter(row["code"] for row in findings)
guidance = {
⋮----
def render_markdown(report)
⋮----
summary = report["summary"]
lines = [
⋮----
review = [row for row in report["findings"] if row["severity"] == "review"]
info = [row for row in report["findings"] if row["severity"] == "info"]
⋮----
rendered = "\n".join(lines) + "\n"
# GitHub issue bodies have a size limit. Always retain complete JSON
# evidence while presenting a bounded, prioritized public review: the
# review-level rows precede informational findings.
max_bytes = 60_000
⋮----
cost = len((line + "\n").encode("utf-8"))
⋮----
bounded = "\n".join(kept) + "\n"
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Audit catalog maintenance debt.")
⋮----
args = parser.parse_args()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
report = analyze(repos, stale_days=args.stale_days)
````

## File: scripts/backfill_github_ids.py
````python
#!/usr/bin/env python3
"""Reconcile missing permanent GitHub repository IDs, without changing curation.

Read-only by default. --write needs an authenticated GitHub token, validates
current canonical names and existing IDs, and writes catalog.json atomically.
404/renamed repositories remain unresolved; an API outage blocks all writes.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
NAME = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
⋮----
def github_metadata(repo: str, token: str) -> dict | None
⋮----
"""One bounded GitHub metadata lookup for an already curated repository."""
⋮----
url = "https://api.github.com/repos/" + quote(owner, safe="") + "/" + quote(name, safe="")
headers = {
⋮----
raw = res.read(150_001)
⋮----
value = json.loads(raw.decode("utf-8"))
⋮----
def reconcile(data: dict, token: str | None = None, *, max_requests: int = 250) -> tuple[dict, dict]
⋮----
rows = data.get("repositories")
⋮----
owner_by_id = {}
names = set()
missing = []
⋮----
canonical = row["repo"].casefold()
⋮----
rid = row.get("githubRepositoryId")
⋮----
report = {
⋮----
repo = row["repo"]
⋮----
response = github_metadata(repo, token)
⋮----
actual = response.get("full_name")
stable_id = response.get("id")
⋮----
previous = owner_by_id.get(stable_id)
⋮----
def main() -> int
⋮----
ap = argparse.ArgumentParser(description=__doc__)
⋮----
args = ap.parse_args()
⋮----
token = (os.environ.get("GITHUB_TOKEN") or "").strip() if args.write else None
⋮----
data = json.loads(CATALOG.read_text(encoding="utf-8"))
⋮----
output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
⋮----
# Do not publish a partially serialized catalog; preserve all other
# repository fields, order, selection policy and metadata unchanged.
⋮----
temporary = Path(tmp.name)
````

## File: scripts/backfill_licenses.py
````python
#!/usr/bin/env python3
"""Backfill only unknown repository licenses using conservative root-file detection."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN = {None, "", "NOASSERTION"}
⋮----
def backfill(repos, resolver, token=None)
⋮----
changed = []
checked = 0
⋮----
github = repo.get("github")
⋮----
name = repo.get("repo")
branch = github.get("defaultBranch")
⋮----
detected = resolver(name, branch, token)
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Backfill unknown licenses without refreshing unrelated metadata.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
token = os.environ.get("GITHUB_TOKEN")
⋮----
result = {"checked": checked, "changed": len(changed), "licenses": changed}
````

## File: scripts/build_discovery_watchlist.py
````python
#!/usr/bin/env python3
"""Turn coverage gaps into a deterministic GitHub discovery watchlist."""
⋮----
def build(report, max_items=30)
⋮----
items=[]
⋮----
priority=100 if x.get("severity")=="critical" else 70
⋮----
priority=95 if x.get("severity")=="critical" else 65
⋮----
dedup={}
⋮----
key=(x["kind"],x["target"])
⋮----
rows=sorted(dedup.values(),key=lambda x:(-x["priority"],x["kind"],x["target"]))[:max_items]
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
````

## File: scripts/catalog_domain_evidence.py
````python
#!/usr/bin/env python3
"""Evidence-only advisory routing for catalog entries whose domain is unknown.

Neither text clues nor GitHub descriptions authorize installation or execution.
Keep named/curated domains authoritative and do not overwrite catalog metadata.
"""
⋮----
# Only explicit technical capabilities or unambiguous *task phrases* qualify.
# Generic words ("AI", "agent", "web", "app", "automation") never qualify alone.
CAPABILITY_DOMAIN_SIGNALS = {
# A title/description is *less* trustworthy than a structured capability.
# Match task-specific phrases, never freeform single-topic descriptions.
DESCRIPTION_DOMAIN_PHRASES = {
⋮----
def _normalized(value)
⋮----
@lru_cache(maxsize=1)
def _readme_source_map()
⋮----
"""Read a fixed, manually reviewed set of upstream blob references."""
path = Path(__file__).resolve().parents[1] / "catalog-readme-evidence.json"
data = json.loads(path.read_text(encoding="utf-8"))
⋮----
def reviewed_readme_source(item)
⋮----
"""Return reviewed evidence only for the exact catalog identity.

    All claims are advisory. Upstream README text is never executed or parsed as
    instructions; this file records reviewed descriptions and immutable hashes.
    """
⋮----
name = item.get("repo")
record = _readme_source_map().get(name)
⋮----
def reviewed_readme_task_terms(item)
⋮----
"""Task-specific hints only, never proof of software compatibility."""
record = reviewed_readme_source(item)
⋮----
def advisory_domain_evidence(item)
⋮----
"""Return {domain: supporting evidence strings}, for advisory routing only."""
domain = item.get("domain")
⋮----
caps = {str(v).strip().casefold() for v in (
# Structured capability labels may be overly broad or inaccurate. The
# result is therefore advisory even if the label is an exact match.
description = _normalized(" ".join(
# Exact ecosystem tokens from the repository slug are robust enough for
# advisory routing, but ambiguous brand/project names are not.
slug = str(item.get("repo") or "").split("/")[-1]
slug_terms = {x for x in re.split(r"[^a-z0-9]+", slug.lower()) if x}
slug_source = slug.casefold()
⋮----
specific_slug_technology = {
evidence = {}
⋮----
match = sorted(slug_terms & lexemes)
⋮----
hits = sorted(caps & signals)
⋮----
matches = [s for s in phrases if re.search(
⋮----
signal = "readme:" + record["path"] + "@" + record["blobSha"]
````

## File: scripts/catalog_stats.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def main()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
domains = Counter(r.get("domain", "other") for r in repos)
tiers = Counter(r.get("tier", "unknown") for r in repos)
languages = Counter(x for r in repos for x in r.get("languages", []))
platforms = Counter(x for r in repos for x in r.get("platforms", []))
capabilities = Counter(x for r in repos for x in r.get("capabilities", []))
self_hosted = sum(r.get("selfHosted") is True for r in repos)
scores = [r.get("score", 0) for r in repos if isinstance(r.get("score"), (int, float))]
by_domain = defaultdict(list)
⋮----
report = {
````

## File: scripts/check_readme_evidence_freshness.py
````python
#!/usr/bin/env python3
"""Read-only freshness check for manually reviewed GitHub README blob evidence.

A changed README requires a new review; it never authorizes automatic changes
to a catalog or target repository.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog-readme-evidence.json"
⋮----
def inspect(record, fetch_repo=gh.fetch, fetch_contents=gh.fetch_contents, token=None)
⋮----
name = record["repository"]
entry = {"repo": name, "recordedBlobSha": record["blobSha"],
⋮----
info = fetch_repo(name, token=token)
⋮----
payload = fetch_contents(name, path=record["path"], token=token)
sha = payload.get("sha") if isinstance(payload, dict) else None
⋮----
size = (len(sources) + batch_size - 1) // batch_size
⋮----
start = batch_index * batch_size
selected = sources[start:start + batch_size]
findings = [inspect(x, fetch_repo, fetch_contents, token) for x in selected]
counts = {k: sum(x["status"] == k for x in findings)
⋮----
def main()
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
data = json.loads(args.manifest.read_text(encoding="utf-8"))
⋮----
result = check(data["sources"], batch_size=args.batch_size,
⋮----
encoded = json.dumps(result,ensure_ascii=False,indent=2)+"\n"
````

## File: scripts/detect_health_drift.py
````python
#!/usr/bin/env python3
"""Compare repository health snapshots and detect meaningful deterioration."""
⋮----
def index(snapshot)
⋮----
rows = snapshot.get("repositories", snapshot if isinstance(snapshot, list) else [])
⋮----
def detect(previous, current, drop=10.0)
⋮----
findings = []
⋮----
before = old.get(repo)
⋮----
delta = round(b-a, 1)
status_changed = before.get("status") != now.get("status")
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
findings=detect(json.loads(args.previous.read_text()), json.loads(args.current.read_text()), args.drop)
````

## File: scripts/discover_candidates.py
````python
#!/usr/bin/env python3
"""Execute discovery watchlist against GitHub Search API and rank novel candidates."""
⋮----
# Preserve the existing injectable transport for offline cache tests, but
# never forward the authenticated discovery token on cross-origin redirects.
urlopen = SAFE_GITHUB_HTTP.open
⋮----
API="https://api.github.com/search/repositories"
REPO_API="https://api.github.com/repos/{}"
CACHE_SCHEMA_VERSION=1
DEFAULT_SEARCH_CACHE_TTL_HOURS=24
DEFAULT_METADATA_CACHE_TTL_HOURS=336
DEFAULT_SEARCH_STALE_MAX_HOURS=168
DEFAULT_METADATA_STALE_MAX_HOURS=2160
DEFAULT_CACHE_RETENTION_HOURS=max(DEFAULT_SEARCH_STALE_MAX_HOURS,DEFAULT_METADATA_STALE_MAX_HOURS)
⋮----
def empty_cache()
⋮----
def empty_cache_stats()
⋮----
def finalize_cache_stats(stats)
⋮----
result=dict(stats or empty_cache_stats())
total=max(0,int(result.get("logicalRequests",0)))
fresh=max(0,int(result.get("freshCacheHits",0)))
reused=(fresh + max(0,int(result.get("notModifiedHits",0))) +
⋮----
def _stat(stats, key)
⋮----
def load_cache(path)
⋮----
data=json.loads(path.read_text())
⋮----
def prune_cache(cache, max_age_seconds, now=None)
⋮----
now=time.time() if now is None else now
removed=0
⋮----
fetched=entry.get("fetchedAt") if isinstance(entry,dict) else None
⋮----
def save_cache(path, cache, max_age_seconds=DEFAULT_CACHE_RETENTION_HOURS*3600, now=None)
⋮----
tmp=path.with_name(path.name+".tmp")
⋮----
def _cache_entry(cache, url)
⋮----
entry=cache.get("entries",{}).get(url) if isinstance(cache,dict) else None
⋮----
fetched=entry.get("fetchedAt")
⋮----
def _headers_dict(headers)
⋮----
def _header_value(headers, name)
⋮----
wanted=name.lower()
⋮----
def cache_get(cache, url, ttl_seconds, now=None)
⋮----
entry=_cache_entry(cache,url)
⋮----
def cache_get_stale(cache, url, max_age_seconds, now=None)
⋮----
age=max(0,now-entry["fetchedAt"])
⋮----
def cache_put(cache, url, data, headers, now=None)
⋮----
def _api_result(data, headers, source, return_source)
⋮----
def _stale_result(cache, url, stale_max_seconds, now, return_source)
⋮----
stale=cache_get_stale(cache,url,stale_max_seconds,now) if cache is not None else None
⋮----
def _conditional_headers(headers, cache, url)
⋮----
result=dict(headers or {})
⋮----
etag=_header_value(entry.get("headers",{}),"etag")
⋮----
def _not_modified_result(cache, url, response_headers, now, return_source)
⋮----
merged_headers=dict(entry.get("headers",{}) or {})
⋮----
data=entry.get("data")
⋮----
def api_json(url, headers, attempts=4, cache=None, ttl_seconds=0, stale_max_seconds=0, now=None, return_source=False, stats=None)
⋮----
# A future caller must not pass its GitHub bearer token to an arbitrary
# initial URL. The shared opener independently blocks redirected tokens.
⋮----
parsed = urlsplit(url)
⋮----
hit=cache_get(cache,url,ttl_seconds,now)
⋮----
request_headers=_conditional_headers(headers,cache,url) if cache is not None and ttl_seconds>0 else dict(headers or {})
last=None
⋮----
data=json.load(res)
response_headers=_headers_dict(res.headers)
⋮----
last=e
⋮----
not_modified=_not_modified_result(cache,url,e.headers,now,return_source)
⋮----
transient=e.code in (403,429,500,502,503,504)
⋮----
stale=_stale_result(cache,url,stale_max_seconds,now,return_source)
⋮----
retry=e.headers.get("Retry-After")
reset=e.headers.get("X-RateLimit-Reset")
⋮----
wait=min(60,float(retry))
⋮----
wait=max(1,min(60,float(reset)-time.time()))
⋮----
wait=min(30,2**attempt)
⋮----
def fetch(query, token=None, per_page=10, cache=None, ttl_seconds=0, stale_max_seconds=0, return_source=False, stats=None)
⋮----
params=urlencode({"q":query,"sort":"stars","order":"desc","per_page":per_page})
headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
⋮----
def enrich(repo, token=None, cache=None, ttl_seconds=0, stale_max_seconds=0, stats=None)
⋮----
stale_endpoints=[]
⋮----
out={"topics":data.get("topics",[]),"watchers":data.get("subscribers_count",0),
⋮----
link=response_headers.get("Link","")
⋮----
m=re.search(r'[?&]page=(\\d+)>; rel="last"',link)
⋮----
def score(item, priority)
⋮----
stars=max(0,item.get("stargazers_count",0)); forks=max(0,item.get("forks_count",0))
popularity=min(25,5*math.log10(stars+1)); ecosystem=min(15,4*math.log10(forks+1))
metadata=5 if item.get("license") else 2
⋮----
candidates={}
errors=[]
stale_sources=[]
stats=empty_cache_stats()
⋮----
name=item.get("full_name")
⋮----
row={"repo":name,"url":item.get("html_url"),"description":item.get("description"),
⋮----
rows=sorted(candidates.values(),key=lambda x:(-x["discoveryScore"],-x["stars"],x["repo"].lower()))
⋮----
enriched=enrich(row["repo"],token,cache,metadata_ttl_seconds,metadata_stale_max_seconds,stats=stats)
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
ttls=(args.search_cache_ttl_hours,args.metadata_cache_ttl_hours,args.search_stale_max_hours,args.metadata_stale_max_hours)
⋮----
known={r["repo"] for r in json.loads(args.catalog.read_text()).get("repositories",[])}
cache=load_cache(args.cache) if args.cache else None
result=discover(
````

## File: scripts/evaluate_candidates.py
````python
#!/usr/bin/env python3
"""Evaluate discovered repositories into accept/review/reject buckets."""
⋮----
ACCEPT_THRESHOLD=80.0
REVIEW_THRESHOLD=55.0
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _integer(value,default=0)
⋮----
def _dict_list(value)
⋮----
def age_days(value, now=None)
⋮----
try: dt=datetime.fromisoformat(value.replace("Z","+00:00"))
⋮----
def text_fit(repo)
⋮----
text=((repo.get("repo") or "")+" "+(repo.get("description") or "")+" "+(repo.get("language") or "")).lower()
targets=_dict_list(repo.get("matchedTargets",[]))
⋮----
hits=0
⋮----
words=str(m.get("target","")).lower().replace("_"," ").replace("-"," ").split()
⋮----
def _bounded(value)
⋮----
def decision_for_score(score)
⋮----
score=_number(score)
⋮----
def evaluation_confidence(repo)
⋮----
release=repo.get("latestRelease")
signals=(
coverage=sum(signals)/len(signals)
⋮----
def score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues)
⋮----
fit_score=fit*65+min(20,topic_hits*10)+min(15,max(0,len(matches)-1)*7.5)
⋮----
if days is None: activity=0
elif days<=90: activity=70
elif days<=365: activity=55
elif days<=730: activity=35
else: activity=10
⋮----
if stars>=5000: adoption=55
elif stars>=1000: adoption=45
elif stars>=500: adoption=35
elif stars>=100: adoption=25
elif stars>=20: adoption=10
else: adoption=0
⋮----
fork_ratio=forks/max(1,stars) if stars else 0.0
⋮----
maturity=25 if repo.get("license") else 0
⋮----
maintenance=50
⋮----
issue_ratio=open_issues/max(1,stars)
⋮----
def evaluate(repo, now=None)
⋮----
score=_number(repo.get("discoveryScore",0))
reasons=[]
days=age_days(repo.get("pushedAt"),now)
⋮----
fit=text_fit(repo)
⋮----
created_days=age_days(repo.get("createdAt"),now)
⋮----
release=repo.get("latestRelease") or {}
release_days=age_days(release.get("publishedAt"),now) if isinstance(release,dict) else None
⋮----
stars=max(0,_integer(repo.get("stars",0)))
contributors=repo.get("contributors")
⋮----
topics={str(x).lower() for x in repo.get("topics",[]) if x is not None} if isinstance(repo.get("topics",[]),list) else set()
matches=_dict_list(repo.get("matchedTargets",[]))
target_words={w for m in matches for w in str(m.get("target","")).lower().replace("_","-").split("-") if w}
topic_hits=len(topics & target_words)
⋮----
watchers=max(0,_integer(repo.get("watchers",0)))
⋮----
forks=max(0,_integer(repo.get("forks",0)))
open_issues=max(0,_integer(repo.get("openIssues",0)))
⋮----
score=round(max(0,min(100,score)),1)
confidence=evaluation_confidence(repo)
decision=decision_for_score(score)
⋮----
decision="review"
⋮----
breakdown=score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues)
⋮----
def evaluate_all(data, now=None)
⋮----
rows=[]
repositories=data.get("repositories",[]) if isinstance(data,dict) else []
⋮----
counts={k:sum(x["decision"]==k for x in rows) for k in ("accept","review","reject")}
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
````

## File: scripts/filter_discovery_memory.py
````python
#!/usr/bin/env python3
"""Suppress unchanged reviewed/rejected candidates while preserving meaningful changes."""
⋮----
SCHEMA_VERSION=1
⋮----
def empty_memory()
⋮----
def load_memory(path)
⋮----
data=json.loads(path.read_text())
⋮----
candidates={str(name):entry for name,entry in data["candidates"].items() if isinstance(entry,dict)}
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _targets(value)
⋮----
def fingerprint(r)
⋮----
def apply(data,memory,score_delta=5.0)
⋮----
if not isinstance(memory,dict): memory=empty_memory()
known=memory.get("candidates")
⋮----
known={}
memory={"schemaVersion":SCHEMA_VERSION,"candidates":known}
⋮----
visible=[]; suppressed=0
now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
repositories=data.get("repositories",[]) if isinstance(data,dict) else []
⋮----
name=r.get("repo")
⋮----
fp=fingerprint(r); old=known.get(name)
changed=True
⋮----
oldfp=old.get("fingerprint",{})
if not isinstance(oldfp,dict): oldfp={}
score_changed=abs(_number(fp.get("score"))-_number(oldfp.get("score")))>=score_delta
changed=(fp.get("decision")!=oldfp.get("decision") or fp.get("pushedAt")!=oldfp.get("pushedAt")
⋮----
base=data if isinstance(data,dict) else {}
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("memory",type=Path)
⋮----
args=ap.parse_args()
data=json.loads(args.evaluated.read_text()); memory=load_memory(args.memory)
⋮----
text=json.dumps(filtered,indent=2,ensure_ascii=False)+"\n"
````

## File: scripts/find_replacements.py
````python
#!/usr/bin/env python3
"""Detect unhealthy catalog entries and rank safer in-catalog replacements."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def overlap(a, b)
⋮----
def replacement_score(source, candidate)
⋮----
health = health_score(candidate)
⋮----
domain = 1.0 if source.get("domain") == candidate.get("domain") else 0.0
caps = overlap(source.get("capabilities"), candidate.get("capabilities"))
roles = overlap(source.get("roles"), candidate.get("roles"))
⋮----
platforms = overlap(source.get("platforms"), candidate.get("platforms"))
languages = overlap(source.get("languages"), candidate.get("languages"))
self_hosted = 1.0 if source.get("selfHosted") == candidate.get("selfHosted") else 0.0
fit = 35*domain + 25*caps + 12*roles + 8*platforms + 5*languages + 5*self_hosted
⋮----
def analyze(repos, threshold=55, top=3)
⋮----
findings = []
⋮----
health = health_score(source)
⋮----
candidates = []
⋮----
result = replacement_score(source, candidate)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser(description="Find catalog repositories that should be reviewed or replaced.")
⋮----
args = ap.parse_args()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
findings = analyze(repos, args.threshold, args.top)
````

## File: scripts/health_score.py
````python
#!/usr/bin/env python3
"""Deterministic repository health scoring from catalog + refreshed GitHub metadata."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def _number(value, default=0.0)
⋮----
try: result=float(value)
⋮----
def age_days(pushed_at, now=None)
⋮----
dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
⋮----
now = now or datetime.now(timezone.utc)
⋮----
def health_score(repo, now=None)
⋮----
gh = repo.get("github")
⋮----
days = age_days(gh.get("pushedAt"), now)
freshness = 35.0
reasons = []
⋮----
freshness = 12.0; reasons.append("push-date-missing")
elif days <= 30: freshness = 35.0
elif days <= 90: freshness = 32.0
elif days <= 365: freshness = 25.0
elif days <= 730: freshness = 14.0; reasons.append("stale-over-1y")
else: freshness = 4.0; reasons.append("stale-over-2y")
⋮----
stars = max(0.0, _number(gh.get("stars", 0)))
forks = max(0.0, _number(gh.get("forks", 0)))
adoption = min(25.0, 5.0 * math.log10(stars + 1))
ecosystem = min(15.0, 4.0 * math.log10(forks + 1))
quality = max(0.0, min(20.0, 2.0 * _number(repo.get("score", 0))))
metadata = 5.0 if gh.get("license") else 2.0
total = round(min(100.0, freshness + adoption + ecosystem + quality + metadata), 1)
status = "healthy" if total >= 75 else "watch" if total >= 55 else "weak"
⋮----
def main()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
rows = [{"repo":r["repo"], **health_score(r)} for r in repos]
````

## File: scripts/infer_selection_guidance.py
````python
#!/usr/bin/env python3
"""Backfill conservative selection guidance from existing curated catalog metadata."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
CAPABILITY_BEST_FOR = {
⋮----
DOMAIN_AVOID_WHEN = {
⋮----
def _humanize(value)
⋮----
def infer_guidance(repo)
⋮----
caps = list(dict.fromkeys(repo.get("capabilities", []) + repo.get("roles", [])))
best = []
domain = repo.get("domain")
⋮----
phrase = "retrieval and persistent-memory workflows"
⋮----
phrase = "agent memory and context retention"
⋮----
phrase = "knowledge retention and reference workflows"
⋮----
phrase = "stateful memory workflows"
⋮----
phrase = "vector search and embedding retrieval"
⋮----
phrase = "vector animation"
⋮----
phrase = CAPABILITY_BEST_FOR.get(cap)
⋮----
avoid = []
⋮----
domain_avoid = DOMAIN_AVOID_WHEN.get(repo.get("domain"))
⋮----
def enrich(repos, tier="recommended", refresh_inferred=False)
⋮----
changed = 0
⋮----
missing_best = not repo.get("bestFor")
missing_avoid = not repo.get("avoidWhen")
refresh = refresh_inferred and repo.get("guidanceSource") == "inferred"
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Backfill deterministic selection guidance.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
changed = enrich(data.get("repositories", []), tier=args.tier, refresh_inferred=args.refresh_inferred)
````

## File: scripts/portfolio_daily.py
````python
#!/usr/bin/env python3
"""Daily, read-only portfolio discovery with optional idempotent Production-OS handoff.

The GitHub Actions token can scan public repositories but cannot write to
other repositories. Actual code integration is delegated to a qualified
Production-OS worker, never treated as completed by this script.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
ALLOWED_LICENSES = {
KEYWORDS = {
GENERIC = {"ai", "agent", "dev", "web", "python", "typescript", "app", "open", "tools", "github", "repo"}
STOPWORDS = {
# Portfolio READMEs include French; shared prose must never be treated as
# evidence that a developer tool is genuinely compatible with an app.
⋮----
# Engine-specific runtime components are not drop-in replacements for
# incompatible engines. This is a hard gate, not a soft relevance penalty.
ENGINE_CONFLICTS = {
# A repository *using* an engine should not be told to integrate that engine's
# complete source tree as if it were a missing application dependency.
EXISTING_ENGINE_SOURCES = {
⋮----
# These are independently running coding agents/CLIs, not importable runtime
# libraries. Recommend them as development-side adapters, never dispatch a
# native app dependency just because the implementation language matches.
EXTERNAL_CODING_AGENT_CLIS = frozenset({
⋮----
MANIFESTS = ("pyproject.toml", "package.json", "requirements.txt", "Cargo.toml",
⋮----
# Only exact, declared dependency names may contribute framework evidence to
# skill references. Do not tokenize package scripts, README prose or arbitrary
# package names: none is an authorization to execute an upstream skill.
SKILL_FRAMEWORK_PACKAGES = {
⋮----
def package_skill_signals(filename: str, content: str) -> tuple[set[str], set[str]]
⋮----
"""Conservative framework hints from exact manifest dependencies only."""
⋮----
# Flutter is a real SDK dependency, not just a mention of the word
# "flutter" in an arbitrary description, comment or README. We only
# recognize the standard, indented pubspec dependency declaration.
section = ""
flutter_dependency = False
⋮----
line = raw_line.split("#", 1)[0].rstrip()
⋮----
indentation = len(line) - len(line.lstrip(" "))
⋮----
section = line[:-1] if line.endswith(":") else ""
⋮----
flutter_dependency = line.strip() == "flutter:"
⋮----
parsed = json.loads(content)
⋮----
dependencies = parsed.get(field)
⋮----
evidence = SKILL_FRAMEWORK_PACKAGES.get(name.strip().lower())
⋮----
class SameOriginRedirect(HTTPRedirectHandler)
⋮----
"""Never forward GitHub or Production-OS bearer tokens to another origin."""
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
original = urlparse(req.full_url)
destination = urlparse(newurl)
⋮----
SAFE_HTTP = build_opener(SameOriginRedirect())
⋮----
parsed = urlparse(url)
⋮----
# Retrying a POST after a timeout or 5xx can submit the same autonomous
# work twice if the first response was lost. Reconcile the authoritative
# inventory on the next scan instead of replaying a mutating request.
⋮----
max_attempts = 1
headers = {
⋮----
body = json.dumps(data).encode() if data is not None else None
⋮----
# Render free instances may need time to wake up. Restrict the
# extended timeout to the approved control-plane host; keep
# ordinary GitHub catalog lookups bounded at 25 seconds.
request_timeout = 60 if parsed.hostname == "production-os1.onrender.com" else 25
⋮----
raw = response.read(3_000_000)
⋮----
def github_repos(owner: str, token: str, portfolio_token: str) -> list[dict]
⋮----
base = (API + "/user/repos?affiliation=owner&sort=full_name&per_page=100"
result = []
⋮----
separator = "&" if "?" in base else "?"
rows = request_json(base + separator + "page=" + str(page), portfolio_token or token)
⋮----
def file_text(full_name: str, path: str, token: str, *, limit: int = 5500) -> str
⋮----
endpoint = API + "/repos/" + "/".join(quote(part, safe="") for part in full_name.split("/")) + "/contents/" + quote(path, safe="")
payload = request_json(endpoint, token)
⋮----
raw = base64.b64decode(payload.get("content", ""), validate=False)
⋮----
def project_profile(repo: dict, token: str) -> dict
⋮----
name = repo["full_name"]
description = str(repo.get("description") or "")
topics = repo.get("topics") or []
intro = file_text(name, "README.md", token, limit=2800)
dependency_text = ""
⋮----
first_manifest = ""
inspected_manifests = {}
⋮----
# Preserve the first-manifest behavior used by the existing repository
# integration ranker. Only skill discovery inspects more than one
# exact, known manifest; it never executes manifest scripts.
value = file_text(name, filename, token, limit=12000)
⋮----
first_manifest = filename
⋮----
# Polyglot projects often have a root pyproject.toml or Cargo.toml
# alongside frontend/mobile source. Those first manifests must not hide
# a real React/Flutter dependency from advisory Skill Issue discovery.
⋮----
# A missing manifest encountered before the primary one was already
# checked. Avoid a second GitHub GET, including duplicate 404s.
value = inspected_manifests.get(filename)
⋮----
# GitHub's own primary-language metadata is sufficient to identify
# GDScript-specific skill references without trusting README instructions.
primary_language = str(repo.get("language") or "").casefold()
⋮----
# Luau is distinct from general Lua. Do not infer Roblox merely
# because an arbitrary project happens to use Lua scripting.
⋮----
overview = " ".join([repo["name"], description, " ".join(topics), intro[:1200]])
label_text = " ".join([repo["name"], description, " ".join(topics)]).lower()
domains = set(infer_domains(tokens(label_text)))
⋮----
# Exact manifest package declarations and GitHub's primary Luau/GDScript
# language are stronger evidence than a missing or generic repo name.
# Reuse only the bounded, already-inspected technology signals, without
# tokenizing arbitrary dependency scripts or README instructions.
trusted_technology_terms = {
⋮----
project_terms = tokens(overview) | (skill_terms & trusted_technology_terms)
# README may refine a known project, but never invent a domain solely from README.
⋮----
def review_blockers(item: dict) -> list[str]
⋮----
"""Explain why a relevant catalog entry is advisory, never auto-dispatchable.

    A curated catalog row deserves task-relevance evaluation even when its
    licensing, maintenance or deployment maturity does not qualify it for
    autonomous code changes. This function preserves the existing strict
    integration policy and exposes its decisions instead of silently dropping
    most of the catalog before matching.
    """
gh = item.get("github") or {}
blockers = []
⋮----
def eligible(item: dict) -> bool
⋮----
"""Strict integration admission: do not widen with discovery coverage."""
⋮----
def is_reference_candidate(tool: dict) -> bool
⋮----
"""Keep demos, samples and architecture guides out of auto-implementation."""
guidance = " ".join(str(v).lower() for v in (tool.get("bestFor") or []))
capabilities = set(str(v).strip().lower() for v in (tool.get("capabilities") or []))
slug = str(tool.get("repo") or "").lower()
reference_clues = (
⋮----
# Generic README prose is not proof that a package provides an actionable
# capability. Such matches may stay in the review report, but cannot trigger
# an autonomous dependency integration solely because languages match.
WEAK_CAPABILITY_TERMS = {
⋮----
name = repo["full_name"].lower()
domains = set(profile["domains"])
⋮----
# Record each identity before considering any domain/score threshold.
# A rejected candidate remains accounted for in the scan evidence.
⋮----
target_identity = repo["name"].lower()
godot_target = profile["language"] == "gdscript" or "godot" in target_identity
roblox_target = profile["language"] in {"lua", "luau"} or "roblox" in target_identity
existing_engine_sources = set(EXISTING_ENGINE_SOURCES["godot"]) if godot_target else set()
# Engine alternatives are replacement *platforms*, not dependencies.
# Derive them from curated alternative relationships, rather than chasing
# arbitrary incompatible engine names by hand. Roblox has no cataloged
# engine-source counterpart, so exclude both sides of declared engine
# alternatives (e.g. godotengine/godot <-> libgdx/libgdx).
engine_pairs = [
excluded_engine_sources = existing_engine_sources | {
⋮----
matches = []
⋮----
slug = str(tool.get("repo") or "")
⋮----
blockers = review_blockers(tool)
domain_evidence = advisory_domain_evidence(tool)
⋮----
advisory_routing = tool.get("domain") not in domains
⋮----
# Exact hyphenated capability labels are meaningful metadata. Splitting
# them for advisory term matching recovers "video editing" vs
# "video-editing" without changing global tokenizer semantics.
capability_labels = " ".join(str(x) for x in (tool.get("capabilities") or []))
terms = (tokens(slug) | tokens(capability_labels)
exact_slug_terms = {
# Keep the standard tokenizer unchanged: only explicit high-specificity
# name evidence may split a hyphenated repository technology label.
⋮----
shared = sorted((profile["terms"] & terms) - GENERIC - STOPWORDS)
⋮----
# A lone match must describe an actual candidate capability/use case,
# not merely an organization name (or an incidental README word).
capability_terms = (
explicit_slug_match = bool(set(shared) & exact_slug_terms)
readme_term_match = bool(
# High-specificity technology tokens such as ESP32/agent-sdk in a
# repository slug can establish advisory relevance even when GitHub
# has no topics or description. This NEVER permits native dispatch.
⋮----
# Ignore the installed engine source and explicit substitute
# engines. Continue recommending compatible plugins/addons.
⋮----
slug_name = slug.rsplit("/", 1)[-1].lower()
⋮----
candidate_languages = set(str(x).lower() for x in (tool.get("languages") or []))
# Missing language metadata is unknown compatibility, not native support.
languages_match = bool(profile["language"]) and profile["language"] in candidate_languages
score = score_repo(tool, profile["terms"], domains, set(), set())
# Inferred domains remain review-only; rank specific evidence against
# a slightly lower threshold so valid indexed tools don't vanish just
# because the original catalog domain was "other".
threshold = 28 if advisory_routing else 35
⋮----
# An incidental word such as "workflows" from a README must not
# qualify an otherwise unrelated same-language library for dispatch.
concrete_terms = (
capability_overlap = bool(set(shared) & concrete_terms)
# An MCP control bridge runs alongside Roblox Studio. Its Lua/Luau
# plugin is not a library embedded in the published game: external
# Studio access, an MCP client and a development host are required.
# Do not spend autonomous runtime-integration budget on this match.
capabilities = {str(v).strip().lower() for v in (tool.get("capabilities") or [])}
external_studio_bridge = (
# A language mismatch remains adapter-review; same-language tools
# with only prose overlap remain discoverable but require review.
mode = (
policy_review = list(blockers)
⋮----
# A native library gets precedence over example applications and adapters.
# Otherwise a reference app can fill the three slots before a usable SDK.
priority = {"native": 0, "capability-review": 1,
⋮----
INTEGRATION_TOKEN_BUDGET = 90000
⋮----
def count_active_integrations(projects: list[dict]) -> int
⋮----
"""Only in-flight portfolio jobs occupy coding-worker capacity slots."""
⋮----
def busy_integration_targets(projects: list[dict]) -> set[str]
⋮----
"""Do not launch concurrent or review-conflicting changes into one repo.

    Unlike the fleet's worker cap, REVIEW_REQUIRED also blocks the target:
    that result may still have a branch/PR awaiting review. DONE and failed
    attempts are handled independently by versioned tracking/quarantine.
    """
⋮----
def unresolved_failed_v2_integrations(projects: list[dict]) -> list[dict]
⋮----
"""Failed v2 jobs still needing review after any successful v3 recovery.

    The v2 record itself remains NEEDS_ATTENTION forever: a later completed
    v3 recovery for the same exact candidate supersedes it for admission and
    reporting. Other failed candidate identities remain quarantined.
    """
recovered = set()
⋮----
marker = re.search(
⋮----
unresolved = []
⋮----
def count_failed_v2_integrations(projects: list[dict]) -> int
⋮----
"""Count only still-unresolved failed high-budget jobs."""
⋮----
def count_failed_v3_integrations(projects: list[dict]) -> int
⋮----
"""A terminal v3 retry is an operator-review gate, not an open slot.

    Never automatically launch unrelated jobs after a final recovery already
    failed. First establish real model/worker capacity and review the result.
    """
⋮----
def count_launches_on_utc_date(projects: list[dict], utc_day: str) -> int
⋮----
"""Account for the UTC launch quota, regardless of an API timestamp offset.

    Call only after verified_managed_projects has validated timezone-aware
    timestamps. A local-calendar comparison can admit extra launches around
    midnight even when the per-UTC-day safety quota is already exhausted.
    """
⋮----
def verified_managed_projects(payload: object) -> list[dict]
⋮----
"""Fail closed unless the inventory can safely authorize more launches.

    Production-OS returns *every* star-list tracking record, with a known
    lifecycle state and timestamp. An unknown state must not be interpreted
    as idle capacity; a duplicate marker or missing timestamp must not make
    retries look safe.
    """
⋮----
projects = payload.get("projects")
⋮----
known_states = {"ACTIVE", "REVIEW_REQUIRED", "NEEDS_ATTENTION", "DONE"}
seen_markers: set[str] = set()
⋮----
goal = project.get("final_goal")
⋮----
repo = project.get("repository")
⋮----
status = project.get("status")
⋮----
timestamp = project.get("created_at")
⋮----
created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
⋮----
def public_integration_status(target: str, projects: list[dict]) -> list[dict]
⋮----
"""Expose only validated status enums for an already-public repository.

    Never echo the worker instruction, project identifiers, private repository
    names, task diagnostics or model-provider traces into the public issue.
    """
results = []
accepted = {"ACTIVE", "QUEUED", "RUNNING", "NEEDS_ATTENTION",
⋮----
goal = str(project.get("final_goal") or "")
markers = re.findall(r"starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])", goal)
⋮----
status = str(project.get("status") or "").upper().replace("-", "_")
⋮----
def integration_marker(target: str, candidate: dict, version: int = 2) -> str
⋮----
identity = hashlib.sha256(
⋮----
"""Quarantine only targets with an *eligible* v3 retry still available.

    A previous candidate may later be rejected as a reference application,
    incompatible capability or low-value match. Keep the failed v2 record
    visible, but do not permanently block an unrelated qualified native tool.
    Existing v3 records (any status) are non-retryable.
    """
available: dict[str, set[str]] = {}
⋮----
target = str(project.get("repository") or "").lower()
⋮----
def launch_integration(url: str, token: str, target: str, candidate: dict, *, version: int = 2)
⋮----
marker = integration_marker(target, candidate, version=version)
goal = (
⋮----
def confirmed_launch(result: object, target: str, candidate: dict, *, version: int = 2) -> bool
⋮----
"""Accept only a bound, persistent, idempotent Production-OS receipt.

    An HTTP success containing {"project": {}} is not proof of the requested
    launch. Wrong-target acknowledgements must not consume a fleet slot or
    permit the dispatcher to submit more work under an inconsistent inventory.
    """
⋮----
identifier = project.get("id")
⋮----
def render_markdown(report: dict) -> str
⋮----
summary = report["summary"]
lines = ["<!-- star-list-portfolio-daily -->", "# Daily star-list portfolio discovery", "",
⋮----
review_gates = site.get("reviewGates") or ["third-party-source-review"]
# Preserve explicit model/provider risk information in the public
# review; do not treat a discovered model as installable software.
⋮----
"""Suggest websites only for applicable project domains, never as code.

    Game projects benefit from an art-direction atlas and reviewed baseline
    planning/QA/prototyping sources even when their GitHub metadata is sparse.
    Hosted services remain references: no credentials, installs or spending.
    """
domains = set(profile.get("domains") or [])
metadata_terms = tokens(" ".join([
⋮----
# GitHub labels often contain hyphens and have no description/topics;
# split names for advisory website matching, not native integration.
⋮----
# Use explicit repository *labels* to recover domains for reference-only
# sources, without modifying the stricter native-code integration profile.
⋮----
# Hosted social-marketing suggestions require explicit GitHub label
# evidence (not README prose, a generic 'promo' name, or an AI label).
# This does not affect the stricter GitHub native-code dispatch domains.
# Vision-language research is not necessarily marketed with the word
# "AI": OCR/screenshot/vision labels still qualify for *advisory* model
# discovery. No domain promotion reaches native-code integration.
⋮----
# A pipeline called "asset-forge" can be truly graphical while its sparse
# GitHub description and language do not disclose that. Require the asset
# name plus specific README capability evidence (not generic prose)
# before considering graphics/media model references. README text is
# untrusted and may influence advisory relevance only, never dispatch.
visual_terms = {
⋮----
candidates = recommend_websites(metadata_terms, domains, limit=None)
chosen = [
⋮----
game_art = next((site for site in candidates if site["id"] == "game-art-style"), None)
⋮----
# Give real game projects the visual atlas without letting generic
# wording rank it above relevant websites for unrelated projects.
chosen = [game_art] + [site for site in chosen if site["id"] != "game-art-style"]
jupiter_art = next((site for site in candidates if site["id"] == "jupiter-game-art-style"), None)
⋮----
chosen = [site for site in chosen if site["id"] != "jupiter-game-art-style"]
⋮----
# 3D motion/rigging tools need concrete project metadata evidence, not
# simply a generic game label; game-art-style retains top priority.
# Explicit 3D engine names qualify for an advisory motion library review.
# They do NOT establish FBX rig compatibility or grant MCP credentials.
motion_signals = {"mocap", "rigging", "rigged", "skeletal", "blender",
character_animation = {"character", "characters"} & metadata_terms and "animation" in metadata_terms
⋮----
pinoc = next((site for site in candidates if site["id"] == "viggle-pinoc-mcp"), None)
⋮----
position = 1 if chosen and chosen[0]["id"] == "game-art-style" else 0
chosen = [site for site in chosen if site["id"] != "viggle-pinoc-mcp"]
⋮----
# The ranking considers every curated website; retain the disposition
# for those that fail the project/task/licence-safe reference filters.
⋮----
site_domains = set(site["domains"])
required = set(site.get("portfolioRequiredSignals") or [])
⋮----
reason = "skill-directory-discovered-for-every-target"
decision = "directory-review"
⋮----
reason = "project-domain-mismatch"
decision = "not-relevant"
⋮----
reason = "specialist-project-signals-unmatched"
⋮----
reason = "no-specific-project-signal"
⋮----
def main() -> int
⋮----
ap = argparse.ArgumentParser()
⋮----
args = ap.parse_args()
⋮----
gh_token = os.getenv("GITHUB_TOKEN", "")
portfolio_token = os.getenv("PORTFOLIO_GITHUB_TOKEN", "")
operator_token = os.getenv("PRODUCTION_OS_OPERATOR_TOKEN", "")
service = os.getenv("PRODUCTION_OS_URL", "https://production-os1.onrender.com")
report = {"generated_at": datetime.now(timezone.utc).isoformat(), "owner": args.owner,
⋮----
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))["repositories"]
catalog_ids = {str(item["repo"]) for item in catalog}
⋮----
websites = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))["websites"]
website_ids = {str(site["id"]) for site in websites}
⋮----
target = request_json(API + "/repos/" + args.repository, portfolio_token or gh_token)
⋮----
source = [target]
⋮----
source = github_repos(args.owner, gh_token, portfolio_token)
# The central issue is public: never publish private target metadata there.
source = [repo for repo in source if not repo.get("private")]
⋮----
target = repo["full_name"]
row = {"repository": target, "status": "scanned", "suggestions": [], "website_references": [],
⋮----
profile = project_profile(repo, portfolio_token or gh_token)
⋮----
# All targets receive the directory; skill matches are based
# on owned GitHub labels and language, never README instructions.
skill_terms = word_set(" ".join([
skill_domains = (set(profile.get("domains") or [])
⋮----
# Owned GitHub metadata only: reference sites never become
# installable tools, and unrelated domain/prose matches are out.
⋮----
repo_checked = set(row["source_assessment"]["repositories"])
websites_checked = set(row["source_assessment"]["websites"])
⋮----
# Incomplete decision traces must not trigger any mutation.
⋮----
# Discovery must be complete before starting any potentially mutating
# managed project. A per-repository read error is not a partial success.
scan_complete = not report["errors"]
⋮----
dispatched = 0
# A lost response does not prove a POST was rejected. Stop sending other
# candidates until the next run reconciles a fresh managed-project inventory.
launch_outcome_uncertain = False
active_integrations = None
failed_v2_integrations = None
failed_v3_integrations = None
available_slots = None
launches_today = None
⋮----
# Validate the origin before even the read-only authenticated request.
parsed_service = urlparse(service)
⋮----
operator_token = ""
⋮----
# Always prioritize highest-confidence matches, irrespective of repository order.
queue = sorted(((item["score"], row, item) for row in report["projects"]
⋮----
existing = request_json(service.rstrip("/") + "/v1/managed-projects/integration-inventory", operator_token)
already = verified_managed_projects(existing)
⋮----
existing = None
⋮----
# Public issue rows originate only from public GitHub discovery.
# Never include private managed-project names or instruction text.
⋮----
# Limit active portfolio work across multiple scheduled/manual runs,
# not merely the number of launches in this one workflow run.
active_integrations = count_active_integrations(already)
failed_v2_integrations = count_failed_v2_integrations(already)
failed_v3_integrations = count_failed_v3_integrations(already)
busy_targets = busy_integration_targets(already)
# Failed projects are quarantined instead of occupying all
# capacity slots forever. While failures remain, admit at most
# ONE distinct project per UTC day and only with an idle portfolio
# worker. This avoids both deadlock and unlimited paid/free-token
# retries from scans triggered repeatedly by GitHub events.
unresolved_failures = unresolved_failed_v2_integrations(already)
failed_targets = recoverable_failure_targets(
# Historical failures for candidates now disqualified remain
# counted and reported; they cannot hold a target hostage forever.
# The global one-launch-per-day cap still applies whenever a
# historical v2 failure remains unresolved.
⋮----
current_day = report["generated_at"][:10]
launches_today = count_launches_on_utc_date(already, current_day)
available_slots = (
⋮----
available_slots = min(
# The final automatic recovery version has already failed.
# Until operators establish working capacity and review outcomes,
# further autonomous submissions only consume scarce free tokens.
# Continue full discovery, reporting and inventory reconciliation.
⋮----
available_slots = 0
# Reevaluate a previously failed compatible candidate before
# consuming the single daily slot on an unrelated new project.
# A v3 marker is distinct and can be submitted only once.
⋮----
# Existing work and earlier successful dispatches in this same
# run must not modify one target repository concurrently.
⋮----
failed_marker = integration_marker(row["repository"], item)
recovery_marker = integration_marker(row["repository"], item, version=3)
matching_failure = any(
⋮----
result = launch_integration(
⋮----
launch_outcome_uncertain = True
⋮----
marker = integration_marker(row["repository"], item)
previous = integration_marker(row["repository"], item, version=1)
⋮----
old = next(
# Do not duplicate active/reviewable jobs. Allow exactly one
# idempotent higher-budget restart when a v1 job has failed.
is_recovery = False
⋮----
status = str(old.get("status") or "").upper().replace("-", "_")
⋮----
is_recovery = True
⋮----
result = launch_integration(service, operator_token, row["repository"], item)
````

## File: scripts/portfolio_failure_diagnostics.py
````python
#!/usr/bin/env python3
"""Operator-only, read-only diagnosis of failed public star-list integrations.

Do not copy worker goals, error messages, project IDs, job keys, private repos,
tokens or URLs from Production-OS into a public GitHub Actions artifact.
"""
⋮----
PUBLIC_FAILED_TARGETS = frozenset({
# This O(1)-query index replaces the global production inbox, which eagerly
# materializes hundreds of unrelated project statuses before search filtering.
# Only an authenticated operator receives per-project diagnostic IDs.
ENDPOINT = (
TRACKING = re.compile(r"(?<![a-z0-9])starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])")
CATEGORIES = (
WORKFLOW_STATES = frozenset({
VALIDATION_STATES = frozenset({
⋮----
def safe_state(raw: object, allowed: frozenset[str]) -> str
⋮----
value = raw.strip().lower() if isinstance(raw, str) else ""
⋮----
def failure_category(outcome: object) -> str
⋮----
# Scan free text internally only; NEVER persist or print it.
⋮----
message = outcome.get("summary")
⋮----
content = message[:8000].lower()
⋮----
def safe_public_failure(item: object) -> dict | None
⋮----
target = item.get("repository")
⋮----
goal = item.get("final_goal")
marker = TRACKING.search(goal) if isinstance(goal, str) else None
⋮----
outcome = item.get("outcome")
outcome = outcome if isinstance(outcome, dict) else {}
runtime = item.get("runtime")
runtime = runtime if isinstance(runtime, dict) else {}
commits = outcome.get("commit_shas")
commits_count = min(20, len(commits)) if isinstance(commits, list) else 0
⋮----
def task_failure_evidence(detail: object) -> dict
⋮----
"""Summarize failed workflow tasks without exposing source text or identifiers."""
workflow = detail.get("current_workflow") if isinstance(detail, dict) else None
tasks = workflow.get("tasks") if isinstance(workflow, dict) else None
⋮----
failed = [task for task in tasks if isinstance(task, dict)
# A terminal project without any terminal task is missing evidence, not
# proof that a deep task diagnosis has succeeded.
⋮----
category = "unknown"
⋮----
result = task.get("result")
⋮----
fields = [result.get(key) for key in (
evidence = result.get("evidence")
⋮----
# All raw fields are classified in memory only; none are persisted.
description = " ".join(value[:1000] for value in fields if isinstance(value, str))
category = failure_category({"summary": description})
⋮----
final = failed[-1] if failed else {}
attempts = final.get("attempts")
budget = final.get("max_attempts")
exhausted = (attempts >= budget if type(attempts) is int
result = final.get("result") if isinstance(final.get("result"), dict) else {}
evidence = result.get("evidence") if isinstance(result.get("evidence"), dict) else {}
known_result_keys = (
known_evidence_keys = (
⋮----
def add_deep_task_diagnostics(result: dict, inbox: object, token: str) -> dict
⋮----
"""Inspect public failed v2 and v3 projects with operator privileges.

    Internal project IDs are used only in the request path, never in output.
    A missing/mismatched detail makes the diagnosis incomplete, not successful.
    """
⋮----
items = inbox.get("items")
⋮----
selected = {}
ambiguous = set()
⋮----
record = safe_public_failure(item)
⋮----
# v2 and v3 on the same target are distinct projects and must both
# be inspected; only duplicate identities within a version are unsafe.
identity = (record["target"], record["tracking_version"])
⋮----
checked_v2 = 0
checked_v3 = 0
⋮----
item = selected.get(identity)
identifier = item.get("project_id") if isinstance(item, dict) else None
⋮----
response = request_json(
project = response.get("project") if isinstance(response, dict) else None
⋮----
raw_goal = str(project.get("final_goal") or "")
expected_goal = str(item.get("final_goal") or "")
actual = TRACKING.search(raw_goal)
expected = TRACKING.search(expected_goal)
⋮----
# The lightweight tracking index intentionally has no outcome.
# Populate delivery/validation evidence only from this separately
# identity-verified project detail, never assume zero delivery.
verified_detail = safe_public_failure(project)
⋮----
deeper = task_failure_evidence(project)
⋮----
# Fail closed on terminal v3 evidence as well: it is the final allowed
# recovery, and its failure must be understood before further admission.
⋮----
def inventory_diagnostic_inbox(payload: object) -> dict
⋮----
"""Convert a complete operator-only index into filtered-inbox structure.

    Never copy raw worker instructions into artifacts. The server itself
    redacts tracking goals; this in-memory conversion keeps only the fields
    needed to fetch the four public failed v2 project details.
    """
⋮----
rows = payload.get("projects")
total = payload.get("total_count")
⋮----
items = []
⋮----
# An incomplete privileged index cannot prove absence of a job.
⋮----
def public_diagnostics(payload: object) -> dict
⋮----
summary = payload.get("summary")
items = payload.get("items")
⋮----
matching = summary.get("matching")
⋮----
rows = [record for item in items if (record := safe_public_failure(item)) is not None]
# The public issue previously verified exactly these four unresolved v2 targets.
v2_targets = [row["target"] for row in rows if row["tracking_version"] == "v2"]
found = set(v2_targets)
# Multiple failures for the same target and version cannot safely be
# attributed by repository alone. A v2 and v3 pair is expected and valid.
unique_v2_targets = len(v2_targets) == len(found)
v3_targets = [row["target"] for row in rows if row["tracking_version"] == "v3"]
unique_v3_targets = len(v3_targets) == len(set(v3_targets))
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
# Always create a secret-free artifact, including when Render is sleeping,
# an operator credential is missing, or an authenticated read times out.
# The previous early-return behavior concealed why a diagnosis failed.
result = {
token = os.environ.get("PRODUCTION_OS_OPERATOR_TOKEN", "")
⋮----
stage = "inbox"
⋮----
inbox = inventory_diagnostic_inbox(
result = public_diagnostics(inbox)
stage = "task-details"
result = add_deep_task_diagnostics(result, inbox, token)
⋮----
# Never echo network exception text or the private API response:
# both can contain backend details or credential-bearing URLs.
⋮----
# The log and artifact contain only allowlisted public names, enums and
# counters. Unavailable and incomplete diagnoses still exit nonzero.
````

## File: scripts/recommend.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
STACKS = ROOT / "stacks.json"
HISTORY = ROOT / "history.json"
WEBSITES = ROOT / "websites.json"
⋮----
DOMAIN_ALIASES = {
TIER_BONUS = {"core": 1.0, "recommended": 0.6, "specialized": 0.25, "indexed": -0.4}
LEVEL = {"low": 0, "medium": 1, "high": 2}
GUIDANCE_WEIGHT = {"curated": 1.0, "inferred": 0.55}
SPECIALIZED_INFERRED_WEIGHT = 0.35
⋮----
def norm(s)
⋮----
def tokens(s)
⋮----
def load()
⋮----
data = json.loads(CATALOG.read_text())
stacks = json.loads(STACKS.read_text()) if STACKS.exists() else {"stacks": []}
⋮----
def infer_domains(qtokens)
⋮----
domains = {DOMAIN_ALIASES[t] for t in qtokens if t in DOMAIN_ALIASES}
# "AI" alone is generic. In an explicitly media, graphics, marketing, or
# writing task, it should not add a spurious coding-agent domain.
explicit_agents = {"agent", "agents", "coding", "code", "dev"}
⋮----
# Generic connective words in curator prose are not evidence that a website
# applies to a project (e.g. "and" in both a TTS description and art guidance).
WEBSITE_MATCH_STOPWORDS = frozenset(
⋮----
def website_review_gates(site)
⋮----
"""Stable, auditable reasons a curated web resource needs separate review.

    These are discovery metadata only, not install instructions or a grant of
    commercial image/model rights. All web resources remain non-executable.
    """
gates = []
resource_type = site.get("type")
reuse = site.get("reuse")
⋮----
# Rewriting output is never guaranteed to retain names, dates, numbers,
# quotations, formatting or source language. Label these constraints
# independently from a licence or hosted compute review.
⋮----
def recommend_websites(qtokens, domains, limit=5, include_unmatched=False)
⋮----
"""Rank non-GitHub references separately from code integration candidates.

    This remains advisory: no site can be auto-dispatched as a dependency.
    Repository-specific hard filters have no meaning for inspiration pages.
    """
data = json.loads(WEBSITES.read_text(encoding="utf-8"))
ranked = []
⋮----
site_domains = set(site["domains"])
matched_domains = sorted(site_domains & domains)
baseline_domains = sorted(set(site.get("portfolioBaselineDomains", [])) & domains)
matched_tags = sorted(qtokens & set(site["tags"]))
matched_text = sorted((qtokens & tokens(
⋮----
score = (12 * len(matched_domains) + 10 * len(matched_tags)
⋮----
# A verified documentation endpoint is reference metadata only;
# the recommender never connects or authorizes paid MCP tools.
⋮----
def activity_adjustment(r)
⋮----
gh = r.get("github")
⋮----
pushed = gh.get("pushedAt")
⋮----
dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
days = max(0, (datetime.now(timezone.utc) - dt).days)
⋮----
@lru_cache(maxsize=8192)
def trend_adjustment(repo_name)
⋮----
pts=json.loads(HISTORY.read_text()).get("repositories",{}).get(repo_name,[])
⋮----
recent=pts[-5:] if len(pts)>=5 else pts
⋮----
days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
⋮----
days=max(1,7*(len(recent)-1))
def delta(k)
⋮----
stars_week=(sd*7/days) if sd is not None else 0.0
forks_week=(fd*7/days) if fd is not None else 0.0
momentum=max(-3.0,min(3.0, stars_week/50.0)) + max(-1.0,min(1.0, forks_week/10.0))
⋮----
momentum=round(max(-6.0,min(6.0,momentum)),3)
reason="declining" if momentum<=-2 else "improving" if momentum>=2 else "growing" if momentum>0.5 else "stable"
⋮----
def guidance_weight(r)
⋮----
source = r.get("guidanceSource")
⋮----
def ranking_review_gates(r)
⋮----
"""Rank everything, but expose the reasons an entry requires review."""
⋮----
def metadata_review_gates(r)
⋮----
"""Report factual gaps without guessing about hosting or licensing."""
⋮----
def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps)
⋮----
caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
⋮----
rtoks = tokens(" ".join([
# Exact task tokens from manually reviewed upstream README blobs improve
# only advisory relevance. They do not elevate tier or integration trust.
⋮----
lexical = len(qtokens & rtoks) / max(1, len(qtokens))
cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
domain_evidence = advisory_domain_evidence(r)
domain_match = 1.0 if requested_domains and requested_domains & domain_evidence.keys() else 0.0
quality = max(0.0, min(1.0, r.get("score", 0) / 10.0))
tier = TIER_BONUS.get(r.get("tier"), 0.0)
best_for = tokens(" ".join(r.get("bestFor", [])))
best_match = len(qtokens & best_for) / max(1, len(qtokens)) if best_for else 0.0
guidance = guidance_weight(r)
s = 34*cap_match + 22*domain_match + 18*lexical + 12*guidance*best_match + 10*quality + 4*max(0.0, tier)
⋮----
avoid = tokens(" ".join(r.get("avoidWhen", [])))
⋮----
health = health_score(r)
⋮----
def explain_repo(r, qtokens, domains, required_caps)
⋮----
best = tokens(" ".join(r.get("bestFor", [])))
reasons = []
matched_domains = sorted(domains & advisory_domain_evidence(r).keys())
⋮----
matched_caps = sorted(required_caps & caps)
⋮----
matched_terms = sorted(qtokens & (tokens(r.get("repo", "")) | caps | best))
⋮----
# Generic words can occur in unrelated stacks. They cannot establish a fit
# on their own (e.g. "AI video" must not select a coding-agent stack).
STACK_GENERIC_TERMS = frozenset(
⋮----
def choose_stack(stacks, qtokens, domains, allowed_names=None)
⋮----
domain_match = st.get("domain") in domains
⋮----
title_terms = tokens(st.get("name", ""))
goal_terms = tokens(st.get("goal", ""))
significant = (qtokens & (title_terms | goal_terms)) - STACK_GENERIC_TERMS
# Require a strong named match, or two independent task-specific
# signals. Notes cannot be evidence: they often describe caveats,
# alternatives or unrelated technologies.
title_words = norm(st.get("name", "")).split()
anchor = next((word for word in title_words if word not in STACK_GENERIC_TERMS), None)
anchored = anchor is not None and anchor in qtokens
⋮----
score = 4 * len(significant) + (3 if domain_match else 0) + (2 if anchored else 0)
⋮----
def infer_alternatives(source, repos, top=3, allowed_names=None)
⋮----
candidates = []
⋮----
result = replacement_score(source, candidate)
⋮----
def infer_complements(source, stacks, repo_by_name, top=4, allowed_names=None)
⋮----
seen = set()
complements = []
⋮----
members = stack.get("repos", [])
⋮----
candidate = repo_by_name.get(name)
⋮----
health = health_score(candidate)
⋮----
def resolve_relations(source, repos, stacks, repo_by_name, allowed_names=None)
⋮----
# Curated links are suggestions, not exemptions from the user's constraints.
def usable(names)
⋮----
seen = {source["repo"]}
result = []
⋮----
explicit_alternatives = usable(source.get("alternatives", []))
explicit_complements = usable(source.get("complements", []))
alternatives = explicit_alternatives or infer_alternatives(source, repos, allowed_names=allowed_names)
complements = explicit_complements or infer_complements(source, stacks, repo_by_name, allowed_names=allowed_names)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
⋮----
archived_filter = ap.add_mutually_exclusive_group()
⋮----
indexed_filter = ap.add_mutually_exclusive_group()
⋮----
args = ap.parse_args()
⋮----
repo_by_name = {r["repo"]: r for r in repos}
qtokens = tokens(args.query)
domains = set(args.domain) or infer_domains(qtokens)
⋮----
relation_names = set()  # Advisory links may reference indexed sources; installation remains independently gated.
filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "indexed":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}
⋮----
gh = r.get("github", {})
⋮----
s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
⋮----
# Eligibility for related tools/stacks must obey the same hard constraints.
⋮----
top = []
⋮----
relations = resolve_relations(r, repos, stacks, repo_by_name, relation_names)
⋮----
result = {
⋮----
all_gates = (item["rankingReviewGates"] + item["metadataReviewGates"]
⋮----
st = result["recommendedStack"]
````

## File: scripts/refresh_github_metadata.py
````python
#!/usr/bin/env python3
"""Refresh non-opinionated GitHub metadata for catalog repositories.

Uses only the Python standard library. GITHUB_TOKEN is optional but strongly
recommended in CI to avoid anonymous API rate limits.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
API = "https://api.github.com/repos/{}"
CONTENTS_API = "https://api.github.com/repos/{}/contents/{}"
LICENSE_NAMES = ("license", "licence", "copying", "notice")
README_NAMES = ("readme",)
FIELDS = {
⋮----
def _request_json(url, token=None, retries=2)
⋮----
headers = {"Accept":"application/vnd.github+json","User-Agent":"star-list-metadata-refresh","X-GitHub-Api-Version":"2022-11-28"}
⋮----
req = Request(url, headers=headers)
⋮----
# The shared GitHub-only opener refuses authenticated cross-origin
# redirects. urllib.urlopen would forward the refresh bearer token.
⋮----
def fetch(repo, token=None, retries=2)
⋮----
def fetch_contents(repo, path="", ref=None, token=None, retries=2)
⋮----
encoded = quote(path, safe="/")
url = CONTENTS_API.format(repo, encoded)
⋮----
def detect_license_text(text)
⋮----
normalized = re.sub(r"\s+", " ", (text or "")).strip().lower()
signatures = [
⋮----
def root_license_scope_warning(text)
⋮----
"""Catch explicit partial, commercial or directory-specific licence grants."""
⋮----
lower = re.sub(r"\s+", " ", text).lower()
⋮----
def strict_root_license(text)
⋮----
"""No README guesses, SPDX strings alone or isolated 'MIT' mentions."""
⋮----
# Text signatures are accepted only for the authoritative root licence
# file, never for incidental descriptions or nested examples.
⋮----
def _decode_content(payload)
⋮----
encoded = payload.get("content")
⋮----
def fallback_license(repo, default_branch, token=None)
⋮----
root = fetch_contents(repo, ref=default_branch, token=token)
⋮----
candidates = []
⋮----
name = str(item.get("name", "")).lower()
stem = re.split(r"[._-]", name, maxsplit=1)[0]
⋮----
detected_licenses = set()
⋮----
path = item.get("path")
⋮----
payload = fetch_contents(repo, path=path, ref=default_branch, token=token)
⋮----
# Incomplete root-file inspection is not enough to safely infer
# a repository-wide license.
⋮----
text = _decode_content(payload)
⋮----
detected = strict_root_license(text)
⋮----
# Conflicting licence files are treated as unresolved, not first-match wins.
# README prose is never a grant covering all directories.
⋮----
def metadata(raw)
⋮----
out = {}
⋮----
lic = raw.get("license")
⋮----
def refresh_primary_language(repo, raw)
⋮----
current=repo.get("languages")
⋮----
language=raw.get("language")
⋮----
def is_missing_repository_error(error)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser()
⋮----
args = ap.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
repos = data.get("repositories", [])
if args.limit > 0: repos = repos[:args.limit]
token = os.environ.get("GITHUB_TOKEN")
⋮----
known_ids = {
⋮----
name = r["repo"]
⋮----
raw = fetch(name, token)
⋮----
stable_id = raw.get("id")
⋮----
previous_id = r.get("githubRepositoryId")
⋮----
existing_name = known_ids.get(stable_id)
⋮----
fresh = metadata(raw)
⋮----
detected = fallback_license(name, raw.get("default_branch"), token)
⋮----
current_github = r.get("github")
current_license = current_github.get("license") if isinstance(current_github, dict) else None
⋮----
entry_changed = r.get("github") != fresh
⋮----
# No additional API calls: this is the same verified repository
# metadata response already used for the weekly refresh.
⋮----
entry_changed = True
⋮----
failure = {"repo":name,"error":str(e)}
````

## File: scripts/render_discovery_issue.py
````python
#!/usr/bin/env python3
"""Render actionable discovery candidates as a stable GitHub issue."""
⋮----
SCORE_COMPONENTS=("fit","activity","adoption","maturity","maintenance")
⋮----
def score_profile(row)
⋮----
breakdown=row.get("scoreBreakdown") or {}
⋮----
def render(data,limit=20)
⋮----
rows=[x for x in data.get("repositories",[]) if x.get("decision") in {"accept","review"}][:limit]
counts=data.get("counts",{})
lines=["## Discovery candidates","",f"Evaluated **{data.get('candidates',0)}** candidates: **{counts.get('accept',0)} accept**, **{counts.get('review',0)} review**, **{counts.get('reject',0)} reject**.",""]
⋮----
targets=", ".join(f"{m.get('kind')}:{m.get('target')}" for m in x.get("matchedTargets",[]))
url=x.get("url") or ""
repo=f"[{x['repo']}]({url})" if url else x["repo"]
⋮----
reasons=', '.join(x.get('reasons',[])) or 'no additional signals'
profile=score_profile(x)
if profile: reasons=f"{reasons}; score profile: {profile}"
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("--output",type=Path); ap.add_argument("--limit",type=int,default=20)
args=ap.parse_args(); body=render(json.loads(args.evaluated.read_text()),args.limit)
````

## File: scripts/render_health_issue.py
````python
#!/usr/bin/env python3
"""Render replacement and health-drift reports as one stable GitHub issue body."""
⋮----
def render(report, drift=None)
⋮----
rows = report.get("repositories", [])
drift = drift or {"repositories": [], "findings": 0}
drifts = drift.get("repositories", [])
lines = [
⋮----
h=row.get("health",{}); repl=row.get("suggestedReplacements",[]); best=repl[0] if repl else None
⋮----
h=row.get("health",{}); reasons=", ".join(h.get("reasons",[])) or "health threshold"
⋮----
repl=row.get("suggestedReplacements",[])
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
drift=json.loads(args.drift.read_text()) if args.drift else None
body=render(json.loads(args.report.read_text()),drift)
````

## File: scripts/report_domain_coverage.py
````python
#!/usr/bin/env python3
"""Inspect evidence-backed advisory domain coverage without mutating catalog."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def analyze(catalog)
⋮----
repositories = catalog["repositories"]
rows = [r for r in repositories if r.get("domain") == "other"]
⋮----
domains = Counter()
⋮----
evidence = advisory_domain_evidence(row)
⋮----
record = reviewed_readme_source(row)
output = {
⋮----
def main()
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
result = analyze(json.loads(args.catalog.read_text(encoding="utf-8")))
encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
````

## File: scripts/star_import_pipeline.py
````python
#!/usr/bin/env python3
"""Deterministic ingestion for screenshot-derived GitHub star manifests."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def normalize_repo_identity(value: str) -> tuple[str, str]
⋮----
raw = value.strip()
⋮----
parsed = urlsplit(raw)
⋮----
parts = [p for p in parsed.path.split("/") if p]
⋮----
parts = raw.split("/")
⋮----
name = name[:-4] if name.lower().endswith(".git") else name
⋮----
display = f"{owner}/{name}"
⋮----
def load_imports(paths: list[Path]) -> tuple[list[dict], list[dict]]
⋮----
payload = json.loads(path.read_text(encoding="utf-8"))
⋮----
values = payload.get("repositories") if isinstance(payload, dict) else None
⋮----
def partition_candidates(records: list[dict], catalog: dict) -> dict
⋮----
catalog_keys = {}
⋮----
key = record["key"]
⋮----
item = {"key": key, "repo": record["repo"], "sources": sources[key]}
⋮----
duplicates = [{"key": key, "repo": first[key]["repo"], "sources": sources[key]} for key in duplicate_keys]
⋮----
def load_reviewed_metadata(paths: list[Path]) -> tuple[dict[str, dict], list[dict]]
⋮----
"""Load offline metadata snapshots. Only explicitly reviewed entries are eligible."""
⋮----
rows = payload.get("repositories") if isinstance(payload, dict) else None
⋮----
def classify_candidate(candidate: dict, metadata: dict | None = None) -> dict
⋮----
result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])), "status": "needs_review"}
⋮----
entry = copy.deepcopy(metadata["catalogEntry"])
raw_github = metadata.get("github")
⋮----
verified_identity = (normalize_repo_identity(metadata.get("repo"))[0] == candidate["key"]
⋮----
verified_identity = False
required_fields = ("score", "tier", "category", "domain", "resourceLevel", "integrationComplexity")
⋮----
result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])),
⋮----
metadata = metadata or {}
metadata_errors = metadata_errors or []
classified = [classify_candidate(c, metadata.get(c["key"])) for c in partition["new"]]
needs_review = [x for x in classified if x["status"] == "needs_review"]
accepted = [x for x in classified if x["status"] == "accepted"]
unique = len(partition["new"]) + len(partition["already_cataloged"])
⋮----
def render_markdown(report: dict) -> str
⋮----
s = report["summary"]
lines = ["# GitHub Star Import Report", "", f"- Raw records: {s['rawRecords']}", f"- Unique normalized repositories: {s['uniqueNormalized']}", f"- Duplicate imports: {s['duplicateImports']}", f"- Already cataloged: {s['alreadyCataloged']}", f"- New candidates: {s['newCandidates']}", f"- Accepted: {s['accepted']}", f"- Needs review: {s['needsReview']}", f"- Malformed: {s['malformed']}", f"- Metadata errors: {s['malformedMetadata']}", "", "## New candidates", ""]
⋮----
def integrate_catalog(catalog: dict, accepted: list[dict]) -> dict
⋮----
result = copy.deepcopy(catalog)
entries = result.setdefault("repositories", [])
seen = {str(x.get("repo", "")).lower() for x in entries}
additions = []
⋮----
key = str(entry.get("repo", "")).lower()
⋮----
def validate_candidate_catalog(candidate: dict, root: Path) -> tuple[bool, str]
⋮----
root = Path(root).resolve()
⋮----
sandbox = Path(td) / "repo"
⋮----
output = []
⋮----
proc = subprocess.run(command, cwd=sandbox, text=True, capture_output=True)
⋮----
def write_catalog_if_valid(candidate: dict, catalog_path: Path, validator=None) -> tuple[bool, str]
⋮----
catalog_path = Path(catalog_path)
validator = validator or (lambda data: validate_candidate_catalog(data, catalog_path.parent))
⋮----
def main(argv=None) -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args(argv)
paths = args.imports or sorted((ROOT / "imports").glob("github-stars-*.json"))
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
⋮----
partition = partition_candidates(records, catalog)
⋮----
report = build_report(partition, malformed, [str(p) for p in paths],
payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
⋮----
accepted = [x["catalogEntry"] for x in report["newCandidates"] if x["status"] == "accepted"]
⋮----
candidate = integrate_catalog(catalog, accepted)
````

## File: scripts/sync_github_stars.py
````python
#!/usr/bin/env python3
"""Read public GitHub Stars and prepare a review report; never edit catalog.json."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
USER_PATTERN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
REPO_PATTERN = re.compile(r"([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/([A-Za-z0-9_.-]{1,100})\Z")
ISSUE_MARKER = "<!-- star-list-star-sync -->"
⋮----
class SameOriginGitHubRedirect(HTTPRedirectHandler)
⋮----
"""Do not forward the Stars workflow's bearer token outside GitHub API.

    urllib's default redirect handler copies request headers, including
    Authorization. The public Stars sync and metadata admission both use
    authenticated GitHub API calls; fail closed on redirect origin changes.
    """
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
original = urlsplit(req.full_url)
destination = urlsplit(newurl)
⋮----
SAFE_GITHUB_HTTP = build_opener(SameOriginGitHubRedirect())
⋮----
def validate_user(user)
⋮----
def normalize_repo(repo)
⋮----
def api_stars(user, token=None, max_pages=100, opener=SAFE_GITHUB_HTTP.open, sleeper=time.sleep)
⋮----
"""Fetch all public stars. A failed/truncated page aborts the entire synchronization."""
⋮----
headers = {
⋮----
found = {}
names_by_stable_id = {}
duplicate_items = 0
pages = 0
⋮----
url = "https://api.github.com/users/" + user + "/starred?" + urlencode(
request = Request(url, headers=headers)
⋮----
raw = response.read()
link = response.headers.get("Link", "")
⋮----
retryable = exc.code in (429, 500, 502, 503, 504)
⋮----
delay = min(8.0, max(0.0, float(exc.headers.get("Retry-After", 2 ** attempt))))
⋮----
delay = float(2 ** attempt)
⋮----
hint = " (check token permissions or API rate limits)" if exc.code in (401, 403, 429) else ""
⋮----
payload = json.loads(raw)
⋮----
repo = entry.get("full_name")
⋮----
key = normalize_repo(repo)
⋮----
repo_id = entry.get("id")
⋮----
original_id = found[key]["githubRepositoryId"]
⋮----
license_obj = entry.get("license")
license_name = license_obj.get("spdx_id") if isinstance(license_obj, dict) else None
⋮----
# We generate the next URL locally; never follow an untrusted Link URL.
has_next = bool(re.search(r'rel\s*=\s*["\x27]?next(?:["\x27]|[,;\s]|$)', link, re.IGNORECASE))
⋮----
def catalog_identities(path, include_ids=False, include_name_ids=False)
⋮----
data = json.loads(Path(path).read_text(encoding="utf-8"))
⋮----
rows = data.get("repositories") if isinstance(data, dict) else None
⋮----
identity = normalize_repo(row.get("repo"))
⋮----
repo_id = row.get("githubRepositoryId")
⋮----
catalog_ids = catalog_ids or set()
catalog_name_ids = catalog_name_ids or {}
# Owner/name values can be reused after deletion or transfer. If the
# catalog has a trusted numeric ID for that exact name, a different live
# ID must never be counted as already admitted.
⋮----
key = normalize_repo(entry["repo"])
recorded_id = catalog_name_ids.get(key)
observed_id = entry.get("githubRepositoryId")
⋮----
# A verified permanent ID remains the same across owner/name transfers.
new = [
⋮----
def render_issue(report, limit=50)
⋮----
user = report["username"]
counts = report["summary"]
entries = report["newRepositories"]
lines = [
⋮----
status = "archived" if row["archived"] else ("disabled" if row["disabled"] else "review")
stars = str(row["stars"]) if row["stars"] is not None else "?"
language = (row["language"] or "unknown").replace("|", "/").replace("\n", " ")
license_name = (row["license"] or "unresolved").replace("|", "/").replace("\n", " ")
⋮----
def write_json(path, payload)
⋮----
output = Path(path)
⋮----
def main(argv=None)
⋮----
parser = argparse.ArgumentParser(description="Check GitHub Stars against star-list (read-only).")
⋮----
args = parser.parse_args(argv)
⋮----
report = build_report(
⋮----
# This is the *same* verified Stars API response, not another
# GitHub request. Admission uses stable IDs to enrich legacy
# catalog entries and reject mismatched snapshots.
````

## File: scripts/test_analyze_coverage.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"analyze_coverage.py"
spec=importlib.util.spec_from_file_location("coverage",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
repos=[
r=mod.analyze(repos,min_domain=2,min_capability=2)
````

## File: scripts/test_auto_stars_admission.py
````python
#!/usr/bin/env python3
"""Regression checks for the first automated Stars review and canonical transfers."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
def read(path)
⋮----
spec = importlib.util.spec_from_file_location("star_import_pipeline", ROOT / "scripts/star_import_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
⋮----
catalog = read("catalog.json")
manifest = read("imports/github-stars-2026-10-09-auto-1.json")
review = read("reports/github-stars-review-2026-10-09-reviewed.json")
report = read("reports/github-stars-review-2026-10-09-summary.json")
snapshots = (read("reports/github-stars-review-2026-10-09-metadata-1.json")["repositories"]
⋮----
cat = {entry["repo"].lower(): entry for entry in catalog["repositories"]}
⋮----
snapshot_map = {entry["repo"].lower(): entry for entry in snapshots}
⋮----
stable_ids = [entry["githubRepositoryId"] for entry in catalog["repositories"]
⋮----
entry = cat[source["repo"].lower()]
⋮----
transfers = {
⋮----
historic = read("history.json")["repositories"]
health_names = {entry["repo"] for entry in read("health-snapshot.json")["repositories"]}
stack_names = {name for stack in read("stacks.json")["stacks"] for name in stack["repos"]}
⋮----
source = snapshot_map[record["repo"].lower()]
entry = cat[record["repo"].lower()]
⋮----
candidate = {"repo": record["repo"], "key": record["repo"].lower(), "sources": ["automatic"]}
⋮----
partition = pipeline.partition_candidates(import_records, catalog)
⋮----
# A second real sync surfaced three later stars. Keep both historic review batches sound.
followup = read("reports/github-stars-followup-2026-10-09-reviewed.json")
later = read("reports/github-stars-followup-2026-10-09-metadata.json")["repositories"]
⋮----
entry = cat[approved["repo"].lower()]
````

## File: scripts/test_backfill_licenses.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "backfill_licenses.py"
spec = importlib.util.spec_from_file_location("backfill_licenses", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
repos = [
seen = []
def resolver(repo, branch, token=None)
````

## File: scripts/test_cache_health_history.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_cache_health_history.py"
spec = importlib.util.spec_from_file_location("cache_history", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
history={"schemaVersion":1,"points":[
current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.32,"bodyReuseRate":0.55,"networkFetchRate":0.60,"staleFallbackRate":0.05}}
⋮----
baseline_history={"schemaVersion":1,"points":[
baseline_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.48,"bodyReuseRate":0.58,"networkFetchRate":0.52,"staleFallbackRate":0.00}}
⋮----
confidence_points=[]
⋮----
high_history={"schemaVersion":1,"points":[]}
⋮----
healthy_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.70,"bodyReuseRate":0.80,"networkFetchRate":0.30,"staleFallbackRate":0.00}}
⋮----
cooldown_points=[
````

## File: scripts/test_cache_health.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_cache_health.py"
spec = importlib.util.spec_from_file_location("cache_health", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
healthy = mod.analyze({
⋮----
watch = mod.analyze({
⋮----
degraded = mod.analyze({
````

## File: scripts/test_catalog_domain_evidence.py
````python
#!/usr/bin/env python3
"""Offline regression: improve indexed source discovery without auto-authorization."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
repos = json.loads((ROOT / "catalog.json").read_text())["repositories"]
by_name = {r["repo"]: r for r in repos}
⋮----
# Real GitHub metadata: identify unambiguous sources without rewriting catalog.
other = [r for r in repos if r["tier"] == "indexed" and r.get("domain") == "other"]
routed = [r for r in other if advisory_domain_evidence(r)]
⋮----
def project(domain, query, language="python")
⋮----
decisions = {}
suggestions = recommendations(target, profile, repos, None, decisions)
⋮----
matched = {s["repository"]: s for s in suggestions}
⋮----
picked = matched[required]
⋮----
ranking_query = [
⋮----
ranking = json.loads(subprocess.check_output(ranking_query, text=True, cwd=ROOT))
ranked = next(row for row in ranking["recommendations"] if row["repo"] == required)
⋮----
# No weak/reused topic labels become grounds for autonomous execution.
unsafe = {
⋮----
# All original review blockers still apply when evidence is strong.
flagged = {
⋮----
matches = recommendations(target, profile, [flagged])
````

## File: scripts/test_catalog_quality.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_catalog_quality.py"
spec = importlib.util.spec_from_file_location("audit_catalog_quality", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
now = datetime(2026, 9, 21, tzinfo=timezone.utc)
repos = [
⋮----
report = mod.analyze(repos, stale_days=730, now=now)
⋮----
markdown = mod.render_markdown(report)
⋮----
# Large collections must not exceed the GitHub issue-body limit: full
# structured evidence remains available from the workflow artifact.
oversized = {**report, "findings": report["findings"] * 1000}
oversized_markdown = mod.render_markdown(oversized)
````

## File: scripts/test_degraded_inputs.py
````python
#!/usr/bin/env python3
"""Regression tests for degraded, malformed, empty, and large pipeline inputs."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
⋮----
def load(name)
⋮----
path=ROOT/"scripts"/f"{name}.py"
spec=importlib.util.spec_from_file_location(name,path)
mod=importlib.util.module_from_spec(spec)
⋮----
evaluation=load("evaluate_candidates")
health=load("health_score")
memory=load("filter_discovery_memory")
history=load("update_history")
cache_history=load("update_cache_health_history")
⋮----
# Malformed candidate metadata must degrade to conservative defaults, not crash.
bad={
result=evaluation.evaluate(bad,NOW)
⋮----
# Sorting and volume must tolerate numeric strings and malformed rows.
rows=[]
⋮----
bulk=evaluation.evaluate_all({"repositories":rows},NOW)
⋮----
# Health scoring must tolerate corrupt scalar metadata conservatively.
h=health.health_score({
⋮----
# Discovery memory must survive malformed historical fingerprints and targets.
row={"repo":"broken/memory","decision":"review","evaluationScore":"bad","stars":"bad","pushedAt":None,"matchedTargets":None}
old={"schemaVersion":1,"candidates":{"broken/memory":{"fingerprint":{"decision":"review","score":"also-bad","stars":None,"pushedAt":None,"targets":[]}}}}
⋮----
# Persistent memory/history files are caches/state: corrupt JSON or wrong shapes reset safely.
⋮----
td=Path(td)
bad_memory=td/"memory.json"; bad_memory.write_text("{not-json")
bad_history=td/"history.json"; bad_history.write_text("[]")
⋮----
# In-memory malformed history shapes must also recover.
updated_history=history.update(
⋮----
# Cache-health report metrics may be absent or malformed without killing persistence.
point=cache_history.point_from_report({"status":"watch","metrics":{"logicalRequests":"bad","networkFetchRate":"bad"}},"2026-09-15")
````

## File: scripts/test_discover_candidates.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"discover_candidates.py"
spec=importlib.util.spec_from_file_location("discover",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
item={"stargazers_count":10000,"forks_count":1000,"license":{"spdx_id":"MIT"}}
````

## File: scripts/test_discovery_cache_stats.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
stats = mod.empty_cache_stats()
cache = {"schemaVersion": 1, "entries": {}}
⋮----
fresh_url = "https://api.github.test/fresh"
⋮----
etag_url = "https://api.github.test/etag"
⋮----
real_urlopen = mod.urlopen
⋮----
def not_modified(req, *args, **kwargs)
⋮----
stale_url = "https://api.github.test/stale"
⋮----
def offline(*args, **kwargs)
⋮----
class Response
⋮----
def __init__(self): self.headers = {"ETag": '"network"'}
def __enter__(self): return self
def __exit__(self, *args): return False
def read(self): return b'{"ok":"network"}'
⋮----
network_url = "https://api.github.test/network"
⋮----
summary = mod.finalize_cache_stats(stats)
````

## File: scripts/test_discovery_cache.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
# The discoverer must use the shared opener that rejects authenticated
# cross-origin redirects, while the API entrypoint refuses hostile initial
# URLs even before a fresh cache result could conceal them.
⋮----
# Nonsecret GitHub metadata requests continue to use the normal cache path.
api_url = "https://api.github.com/search/repositories"
valid_cache = {"schemaVersion": 1, "entries": {}}
⋮----
cache = {"schemaVersion": 1, "entries": {}}
url = "https://api.github.test/repos/a/x"
⋮----
fresh = mod.cache_get(cache, url, ttl_seconds=60, now=1030)
⋮----
expired = mod.cache_get(cache, url, ttl_seconds=60, now=1061)
⋮----
# Expired data may be used only as a bounded fallback when GitHub/network is unavailable.
stale_url = "https://api.github.test/repos/stale/x"
⋮----
real_urlopen = mod.urlopen
⋮----
def offline(*args, **kwargs)
⋮----
too_old_failed = False
⋮----
too_old_failed = True
⋮----
# Expired entries with an ETag should be conditionally revalidated. A 304 refreshes
# the cache timestamp while preserving the cached body and useful response headers.
revalidate_url = "https://api.github.test/repos/etag/x"
⋮----
seen_headers = {}
⋮----
def not_modified(req, *args, **kwargs)
⋮----
path = Path(td) / "cache.json"
⋮----
loaded = mod.load_cache(path)
⋮----
old={"schemaVersion":1,"entries":{"old":{"fetchedAt":0,"data":{}},"fresh":{"fetchedAt":1900,"data":{}}}}
removed=mod.prune_cache(old,max_age_seconds=500,now=2000)
````

## File: scripts/test_discovery_memory.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"filter_discovery_memory.py"
spec=importlib.util.spec_from_file_location("m",SCRIPT); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
row={"repo":"a/x","decision":"review","evaluationScore":70,"stars":1000,"pushedAt":"2026-09-01","matchedTargets":[]}
data={"repositories":[row],"counts":{"accept":0,"review":1,"reject":0}}
⋮----
changed={**row,"evaluationScore":76}; third,mem=m.apply({"repositories":[changed]},mem); assert third["candidates"]==1
````

## File: scripts/test_discovery_watchlist.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"build_discovery_watchlist.py"
spec=importlib.util.spec_from_file_location("watchlist",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
report={"policy":{"minHealthyPerDomain":3,"minHealthyPerCapability":2},
r=mod.build(report)
````

## File: scripts/test_documentation.py
````python
#!/usr/bin/env python3
"""Keep the public v1 documentation aligned with the executable pipeline."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
SCORING=ROOT/"docs"/"DISCOVERY_SCORING.md"
VERSION=ROOT/"VERSION"
CHANGELOG=ROOT/"CHANGELOG.md"
⋮----
readme=README.read_text()
scoring=SCORING.read_text()
version=VERSION.read_text().strip()
changelog=CHANGELOG.read_text()
⋮----
website_guide = (ROOT / "WEB_RESOURCES.md").read_text()
websites = __import__("json").loads((ROOT / "websites.json").read_text())
⋮----
# Local Markdown links from README must point to repository files/directories.
⋮----
local=target.split("#",1)[0]
⋮----
spec=importlib.util.spec_from_file_location("evaluation",ROOT/"scripts"/"evaluate_candidates.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
⋮----
# The hourly Stars job pushes with GITHUB_TOKEN; GitHub deliberately
# suppresses a second workflow's normal push trigger for that commit.
# Keep the qualified reusable audit dependency wired to the actual push.
sync_yaml = (ROOT / ".github/workflows/sync-github-stars.yml").read_text()
audit_yaml = (ROOT / ".github/workflows/catalog-quality-on-change.yml").read_text()
stars_docs = (ROOT / "docs/GITHUB_STARS_SYNC.md").read_text()
⋮----
identity_yaml = (ROOT / ".github/workflows/backfill-github-ids.yml").read_text()
identity_code = (ROOT / "scripts/backfill_github_ids.py").read_text()
⋮----
skills_workflow = (ROOT / ".github/workflows/audit-agent-skill-sources.yml").read_text()
skills_validator = (ROOT / "scripts/audit_agent_skill_sources.py").read_text()
⋮----
maintenance_yaml = (ROOT / ".github/workflows/refresh-metadata.yml").read_text()
⋮----
skills_docs = (ROOT / "AGENT_SKILLS.md").read_text()
skills_catalog = (ROOT / "agent-skills.json").read_text()
skills_scanner = (ROOT / "scripts/agent_skill_discovery.py").read_text()
portfolio_scanner = (ROOT / "scripts/portfolio_daily.py").read_text()
portfolio_yaml = (ROOT / ".github/workflows/daily-portfolio-integration.yml").read_text()
````

## File: scripts/test_evaluate_candidates.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"evaluate_candidates.py"
spec=importlib.util.spec_from_file_location("evaluate",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
strong={"repo":"a/ai-agents","description":"AI agents framework","language":"Python","discoveryScore":75,"stars":5000,"forks":500,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","createdAt":"2020-01-01T00:00:00Z","latestRelease":{"publishedAt":"2026-08-01T00:00:00Z"},"contributors":50,"watchers":200,"openIssues":20,"hasDiscussions":True,"topics":["ai","agents"],"matchedTargets":[{"target":"ai"},{"target":"agents"}]}
weak={"repo":"b/y","description":"unrelated tool","language":"C","discoveryScore":50,"stars":20,"forks":0,"license":None,"pushedAt":"2020-01-01T00:00:00Z","matchedTargets":[{"target":"mobile"}]}
sparse={"repo":"c/ai-tool","description":"AI tool","language":"Python","discoveryScore":60,"stars":100,"matchedTargets":[{"target":"ai"}]}
sparse_high={"repo":"c/high-score-ai","description":"AI framework","language":"Python","discoveryScore":100,"stars":100,"matchedTargets":[{"target":"ai"}]}
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW); c=mod.evaluate(sparse,NOW); d=mod.evaluate(sparse_high,NOW)
⋮----
components={"fit","activity","adoption","maturity","maintenance"}
⋮----
# Low-confidence metadata can never produce automatic acceptance.
⋮----
# Decision boundaries are part of the public calibration contract.
⋮----
calibration_cases=[
results=[mod.evaluate(repo,NOW) for repo,_ in calibration_cases]
````

## File: scripts/test_find_replacements.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "find_replacements.py"
spec = importlib.util.spec_from_file_location("find_replacements", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
bad = {"repo":"x/bad","score":8.0,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
good = {"repo":"x/good","score":9.5,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
other = {"repo":"x/other","score":9.5,"domain":"graphics","capabilities":["vector"],"platforms":["linux"],"languages":["rust"],"selfHosted":True,
⋮----
rows = mod.analyze([bad, good, other])
````

## File: scripts/test_full_catalog_availability.py
````python
#!/usr/bin/env python3
"""Catalog-wide availability contract: no audit tier / no silent admission queue."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["repositories"]
websites = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))["websites"]
names = [entry["repo"].lower() for entry in catalog]
⋮----
counts = Counter(entry["tier"] for entry in catalog)
⋮----
# An indexed source is never blocked *just* because it has not been hand-curated.
clean = {
⋮----
unsafe = {**clean, "github": {**clean["github"], "license": None}}
⋮----
query = [
payload = json.loads(subprocess.check_output(query, cwd=ROOT, text=True))
⋮----
recs = payload["recommendations"]
⋮----
project = {"full_name": "dbrckk/Moneyprinterturbo_perso", "name": "Moneyprinterturbo_perso",
profile = {"domains": ["ai_media", "productivity"],
assessed = {}
site_assessed = {}
matches = recommendations(project, profile, catalog, None, assessed)
references = website_references_for_project(project, profile, None, site_assessed)
````

## File: scripts/test_health_drift.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"detect_health_drift.py"
spec=importlib.util.spec_from_file_location("drift",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
old={"repositories":[{"repo":"a/x","score":90,"status":"healthy"},{"repo":"b/y","score":60,"status":"watch"}]}
new={"repositories":[{"repo":"a/x","score":78,"status":"healthy"},{"repo":"b/y","score":52,"status":"weak"},{"repo":"c/z","score":20,"status":"weak"}]}
rows=mod.detect(old,new,10)
````

## File: scripts/test_health_score.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "health_score.py"
spec = importlib.util.spec_from_file_location("health_score", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
NOW = datetime(2026, 9, 15, tzinfo=timezone.utc)
⋮----
active = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2026-09-10T00:00:00Z"}}
stale = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2023-01-01T00:00:00Z"}}
````

## File: scripts/test_history.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"update_history.py"
spec=importlib.util.spec_from_file_location("h",SCRIPT); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
pts=[{"date":"2026-08-18","health":70,"stars":100,"forks":10},{"date":"2026-08-25","health":72,"stars":114,"forks":12},{"date":"2026-09-01","health":75,"stars":128,"forks":14},{"date":"2026-09-08","health":78,"stars":142,"forks":16},{"date":"2026-09-15","health":82,"stars":156,"forks":18}]
m=h.window_metrics(pts,5); assert m["healthDelta"]==12 and m["starsPerWeek"]==14 and m["forksPerWeek"]==2
t=h.trends({"repositories":{"a/x":pts}})["repositories"][0]; assert t["trend"]=="improving" and t["fourWeeks"]["points"]==5 and t["week"]["points"]==2
````

## File: scripts/test_other_domain_expansion.py
````python
#!/usr/bin/env python3
"""Regression tests for broad yet conservative advisory classification."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
rows = catalog["repositories"]
lookup = {r["repo"]: r for r in rows}
report = analyze(catalog)
⋮----
# Explicit high-quality labels and descriptions. Never rewrite original domain.
⋮----
row = lookup[name]
⋮----
evidence = advisory_domain_evidence(row)
⋮----
# Ambiguous metadata must never gain a domain merely to increase the metric.
⋮----
# An inferred domain can be suggested to a compatible task but never silently
# authorize a third-party integration. The existing trust boundary must hold.
project = {"full_name": "dbrckk/esp32-project", "name": "esp32-project"}
profile = {
decision_trace = {}
suggestions = recommendations(project, profile, rows, None, decision_trace)
⋮----
by_suggestion = {r["repository"]: r for r in suggestions}
⋮----
row = by_suggestion[name]
⋮----
# Real inactive or unresolved sources continue to carry source-specific guards.
unsafe = dict(lookup["espressif/arduino-esp32"])
````

## File: scripts/test_pipeline_integration.py
````python
#!/usr/bin/env python3
"""Offline integration test for the discovery review pipeline."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
⋮----
def load(name)
⋮----
path=SCRIPTS/f"{name}.py"
spec=importlib.util.spec_from_file_location(name,path)
module=importlib.util.module_from_spec(spec)
⋮----
coverage=load("analyze_coverage")
watchlists=load("build_discovery_watchlist")
discovery=load("discover_candidates")
evaluation=load("evaluate_candidates")
memory=load("filter_discovery_memory")
renderer=load("render_discovery_issue")
⋮----
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
catalog=[{
⋮----
report=coverage.analyze(catalog,min_domain=2,min_capability=2)
⋮----
watchlist=watchlists.build(report,max_items=10)
⋮----
high={
review={
⋮----
def fake_fetch(query,token=None,per_page=10,cache=None,ttl_seconds=0,stale_max_seconds=0,return_source=False,stats=None)
⋮----
payload={"items":[high,review]}
⋮----
def fake_enrich(repo,token=None,cache=None,ttl_seconds=0,stale_max_seconds=0,stats=None)
⋮----
discovered=discovery.discover(watchlist,{"known/agent-core"},per_query=5)
⋮----
evaluated=evaluation.evaluate_all(discovered,NOW)
⋮----
by_repo={row["repo"]:row for row in evaluated["repositories"]}
⋮----
state={"schemaVersion":1,"candidates":{}}
⋮----
body=renderer.render(visible)
````

## File: scripts/test_readme_domain_evidence.py
````python
#!/usr/bin/env python3
"""Offline evidence-integrity and relevance regressions for immutable README hints."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
repos = catalog["repositories"]
by_repo = {r["repo"]: r for r in repos}
manifest = json.loads((ROOT / "catalog-readme-evidence.json").read_text(encoding="utf-8"))
sources = manifest["sources"]
⋮----
allowed = {
⋮----
name = entry["repository"]
⋮----
row = by_repo[name]
⋮----
ev = advisory_domain_evidence(row)
⋮----
wrong_id = {**row, "githubRepositoryId": row["githubRepositoryId"] + 1000000}
⋮----
curated = {**row, "domain": "game_dev"}
⋮----
report = analyze(catalog)
⋮----
assert len(report["unrouted"]) >= 1  # Never invent a domain to reach 100% classification.
⋮----
ref = row["readmeEvidence"]
⋮----
# Grounded examples: targeted routes derived from upstream README snapshots.
cases = [
⋮----
tool = by_repo[name]
⋮----
project = {"full_name": "dbrckk/target-test", "name": "target-test"}
profile = {"domains":[domain],"terms":tokens(query),"language":"python",
assessment = {}
picks = recommendations(project, profile, [tool], None, assessment)
⋮----
picked = picks[0]
⋮----
# A source with conflicting identity or unsupported domain must not inherit
# the vetted README instructions / routing.
⋮----
# CLI ranking works with a new task domain without mutating catalog.
args = [sys.executable, str(ROOT / "scripts/recommend.py"),
payload = json.loads(subprocess.check_output(args,cwd=ROOT,text=True))
⋮----
record = next(row for row in payload["recommendations"] if row["repo"] == "withmarbleapp/os-taxonomy")
⋮----
# Real safeguards remain independent of source evidence.
unsafe = {**by_repo["hexgrad/kokoro"],
````

## File: scripts/test_readme_evidence_freshness.py
````python
#!/usr/bin/env python3
"""Offline proof: drift checks preserve original source facts and identity."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/"catalog-readme-evidence.json").read_text())["sources"]
known=records[0]
def repo(name, token=None)
def content(name, path="", token=None)
base=inspect(known,repo,content)
⋮----
def failed(*args,**kwargs)
⋮----
reports=check([known],1,0,repo,content)
````

## File: scripts/test_refresh_github_metadata.py
````python
#!/usr/bin/env python3
"""Regression tests for resilient GitHub metadata refresh behavior."""
⋮----
def http_error(repo, code, message)
⋮----
def run_main(args)
⋮----
old_argv = sys.argv
⋮----
def test_missing_repo_is_recorded_but_nonfatal()
⋮----
catalog = Path(tmp) / "catalog.json"
⋮----
def fake_fetch(repo, token=None, retries=2)
⋮----
written = json.loads(catalog.read_text())
⋮----
def test_license_signature_detection()
⋮----
# Bare words and README snippets must not grant repo-wide reuse rights.
⋮----
def test_license_fallback_reads_root_license_file()
⋮----
original = refresh.fetch_contents
⋮----
def fake_contents(repo, path="", ref=None, token=None, retries=2)
⋮----
content = base64.b64encode(
⋮----
def test_license_fallback_reads_readme_when_root_license_is_absent()
⋮----
def test_license_fallback_rejects_conflicting_root_files()
⋮----
content = (
⋮----
def test_metadata_refresh_uses_license_fallback()
⋮----
def test_metadata_refresh_preserves_verified_license_when_github_is_inconclusive()
⋮----
def test_server_error_remains_fatal()
⋮----
# Reusing an existing slug for a new GitHub ID must not silently change
# the catalog's established permanent identity.
⋮----
unchanged = json.loads(catalog.read_text())["repositories"][0]
⋮----
# Metadata and license fallback requests must use the same authenticated
# GitHub-only opener as Stars synchronization, never urlopen's default
# unrestricted redirect handling.
⋮----
class RejectingOpener
⋮----
def open(self, request, timeout=20)
previous_opener = refresh.SAFE_GITHUB_HTTP
````

## File: scripts/test_render_discovery_issue.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"render_discovery_issue.py"
spec=importlib.util.spec_from_file_location("renderer",SCRIPT); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
data={"candidates":2,"counts":{"accept":1,"review":1,"reject":0},"repositories":[{"repo":"a/x","url":"https://github.com/a/x","decision":"accept","evaluationScore":90,"evaluationConfidence":"high","scoreBreakdown":{"fit":92.5,"activity":100.0,"adoption":75.0,"maturity":80.0,"maintenance":85.0},"stars":1000,"ageDays":5,"matchedTargets":[{"kind":"domain","target":"mobile"}],"reasons":["active<=90d"]}]}
body=mod.render(data)
````

## File: scripts/test_render_health_issue.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"render_health_issue.py"
spec=importlib.util.spec_from_file_location("renderer",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
report={"threshold":55,"repositories":[]}
drift={"findings":1,"repositories":[{"repo":"a/x","previousScore":90,"currentScore":78,"delta":-12,"previousStatus":"healthy","currentStatus":"healthy"}]}
body=mod.render(report,drift)
⋮----
report={"threshold":55,"repositories":[{"repo":"b/y","health":{"score":40,"status":"weak","reasons":[]},"suggestedReplacements":[]}]}
body=mod.render(report,{"repositories":[]})
````

## File: scripts/test_selection_guidance.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "infer_selection_guidance.py"
spec = importlib.util.spec_from_file_location("infer_selection_guidance", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
repos = [
⋮----
changed = mod.enrich(repos)
````

## File: scripts/test_star_import_pipeline.py
````python
#!/usr/bin/env python3
⋮----
SCRIPT = Path(__file__).with_name("star_import_pipeline.py")
⋮----
# Normalization
⋮----
root = Path(td)
p1 = root / "one.json"
p2 = root / "two.json"
⋮----
catalog = {"repositories": [{"repo": "OPENAI/CODEX", "score": 9.5}]}
partition = partition_candidates(records, catalog)
⋮----
candidate = partition["new"][0]
classified = classify_candidate(candidate)
⋮----
report = build_report(partition, malformed, [str(p1), str(p2)])
⋮----
# A raw GitHub snapshot cannot approve itself. Approval is explicit and tied to GitHub evidence.
verified_github = {
new_entry = {
reviewed = {"repo": "Anthropic/Claude-Code", "github": verified_github,
⋮----
review_report = build_report(partition, malformed, ["batch"], {candidate["key"]: reviewed}, ["metadata"])
⋮----
# Integration preserves existing records, sorts only additions deterministically, and is idempotent.
base = {"schemaVersion": 1, "repositories": [{"repo": "z/existing", "score": 8.0}]}
accepted = [
once = integrate_catalog(base, accepted)
twice = integrate_catalog(once, accepted)
⋮----
# Failed validation never replaces the authoritative catalog.
⋮----
catalog_path = root / "catalog.json"
original = json.dumps(base, indent=2) + "\n"
⋮----
# CLI is dry-run by default, emits requested reports, and leaves catalog unchanged.
⋮----
import_path = root / "stars.json"
⋮----
report_json = root / "report.json"
report_md = root / "report.md"
⋮----
catalog_payload = {"schemaVersion": 1, "repositories": [{"repo": "openai/codex"}]}
original = json.dumps(catalog_payload) + "\n"
⋮----
proc = subprocess.run([
⋮----
cli_report = json.loads(report_json.read_text())
⋮----
# End-to-end CLI: importing needs human approval, accepts reviewed data, and stays idempotent.
⋮----
scripts = root / "scripts"
⋮----
baseline = {**new_entry, "repo": "Existing/Project"}
proposed = {**new_entry, "repo": "New/Project"}
⋮----
args = [sys.executable, str(SCRIPT), str(import_path), "--catalog", str(catalog_path),
before = catalog_path.read_text()
raw = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
success = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
merged = json.loads(catalog_path.read_text())
⋮----
new_before_repeat = catalog_path.read_text()
repeat = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
bad = subprocess.run(args + ["--write"], text=True, capture_output=True)
````

## File: scripts/test_verify_catalog_evidence.py
````python
#!/usr/bin/env python3
"""Deterministic offline tests for evidence-based metadata review."""
⋮----
def source(text)
⋮----
data = text.encode("utf-8")
blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
⋮----
MIT = ("MIT License\nCopyright (c) 2026 Example\n"
LISTING = [
row = {"repo": "example/project", "tier": "indexed", "githubRepositoryId": 123,
⋮----
def fake_repo(name, token=None)
⋮----
def fake_content(name, path="", ref=None, token=None)
⋮----
def main()
⋮----
partial = ('Portions of this software are licensed as follows: '
⋮----
def scoped_content(name, path="", ref=None, token=None)
scoped_row = audit.inspect_entry(row, fake_repo, scoped_content)
⋮----
bad = source(MIT)
⋮----
report = audit.inspect_entry(row, fake_repo, fake_content)
⋮----
changed = dict(row, licenseStatus="partial")
⋮----
changed = dict(row, github={**row["github"], "license": "Apache-2.0"})
⋮----
def conflicting_repo(name, token=None)
⋮----
def reused_repo(name, token=None)
⋮----
# A README claim without a root licence is never promoted.
def readme_only(name, path="", ref=None, token=None)
⋮----
entries = [dict(row), {**row, "repo": "example/second"}]
⋮----
flagged = dict(row, repo="example/audit-only", selfHosted=True,
⋮----
only = [dict(row, github=dict(row["github"]))]
original_self_hosted = only[0]["selfHosted"]
full = audit.audit(only, only, 1, fake_repo, fake_content, apply=True)
⋮----
schema = json.loads((Path(__file__).resolve().parents[1]
report_contract = {**full, "batchIndex": 0, "wroteCatalog": True}
⋮----
unsafe = dict(report_contract, counts={**full["counts"], "scopedLicenses": "not-a-number"})
⋮----
# Caller writes nothing if any individual operation fails, including an
# identity conflict in a later entry in the batch.
⋮----
path = Path(tmp) / "catalog.json"
````

## File: scripts/update_cache_health_history.py
````python
#!/usr/bin/env python3
"""Persist bounded cache-health history and derive multi-week drift signals."""
⋮----
SCHEMA_VERSION=1
DEFAULT_MAX_POINTS=26
ADAPTIVE_MIN_SAMPLES=4
ADAPTIVE_MAX_SAMPLES=8
ADAPTIVE_THRESHOLD=0.20
COOLDOWN_POINTS=2
SEVERITY_RANK={"healthy":0,"watch":1,"degraded":2}
⋮----
def empty_history()
⋮----
def load_history(path)
⋮----
data=json.loads(path.read_text())
⋮----
def save_history(path,history)
⋮----
tmp=path.with_name(path.name+".tmp")
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _metric(metrics,name)
⋮----
value=metrics.get(name,0.0) if isinstance(metrics,dict) else 0.0
⋮----
def point_from_report(report,date)
⋮----
metrics=report.get("metrics",{}) if isinstance(report,dict) else {}
if not isinstance(metrics,dict): metrics={}
⋮----
def _point_metric(point,name)
⋮----
def _baseline_confidence(sample_size)
⋮----
score=round(min(1.0,max(0.0,sample_size/ADAPTIVE_MAX_SAMPLES)),3)
⋮----
def adaptive_baseline(points,min_samples=ADAPTIVE_MIN_SAMPLES,max_samples=ADAPTIVE_MAX_SAMPLES,threshold=ADAPTIVE_THRESHOLD)
⋮----
history=points[:-1][-max_samples:] if points else []
⋮----
result={
⋮----
current=points[-1]
names=("apiCallAvoidanceRate","bodyReuseRate","networkFetchRate")
baselines={name:round(float(median([_point_metric(p,name) for p in history])),4) for name in names}
deltas={name:round(_point_metric(current,name)-baselines[name],4) for name in names}
findings=[]
⋮----
def _adaptive_severity(adaptive)
⋮----
def _severity(value)
⋮----
def combine_severity(status,adaptive_severity,direction)
⋮----
values=[_severity(status),_severity(adaptive_severity)]
⋮----
def hysteresis_state(previous_candidate,current_candidate)
⋮----
previous=_severity(previous_candidate)
current=_severity(current_candidate)
⋮----
def _point_alert(point)
⋮----
def issue_action(points,current_alert,cooldown_points=COOLDOWN_POINTS)
⋮----
current=_severity(current_alert)
⋮----
states=[_point_alert(point) for point in points]
last_close=None
⋮----
last_close=index
⋮----
observations_since_close=len(states)-1-last_close
⋮----
def analyze_trend(points)
⋮----
adaptive=adaptive_baseline(points)
adaptive_severity=_adaptive_severity(adaptive)
recent=points[-3:]
⋮----
avoidance=[_point_metric(p,"apiCallAvoidanceRate") for p in recent]
network=[_point_metric(p,"networkFetchRate") for p in recent]
body=[_point_metric(p,"bodyReuseRate") for p in recent]
ad=round(avoidance[-1]-avoidance[0],4)
nd=round(network[-1]-network[0],4)
bd=round(body[-1]-body[0],4)
⋮----
direction="declining" if findings else "stable"
⋮----
direction="improving"
⋮----
def update(history,current,date=None,max_points=DEFAULT_MAX_POINTS)
⋮----
today=str(date or date_type.today().isoformat())
base=history if isinstance(history,dict) else empty_history()
source_points=base.get("points",[])
if not isinstance(source_points,list): source_points=[]
points=[dict(p) for p in source_points if isinstance(p,dict) and p.get("date")]
points=[p for p in points if p.get("date")!=today]
previous=points[-1] if points else None
point=point_from_report(current,today)
⋮----
points=points[-max_points:]
trend=analyze_trend(points)
candidate=combine_severity(point.get("status"),trend.get("adaptiveSeverity"),trend.get("direction"))
previous_candidate=(previous or {}).get("candidateSeverity") or (previous or {}).get("status")
⋮----
alert="healthy" if candidate=="healthy" else "watch"
⋮----
alert=hysteresis_state(previous_candidate,candidate)
action=issue_action(points[:-1],alert)
⋮----
updated={"schemaVersion":SCHEMA_VERSION,"points":points}
⋮----
def render_markdown(trend)
⋮----
lines=[
⋮----
adaptive=trend.get("adaptiveBaseline",{})
⋮----
deltas=adaptive.get("deltas",{})
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
history=load_history(args.history)
current=json.loads(args.current_report.read_text())
````

## File: scripts/update_history.py
````python
#!/usr/bin/env python3
"""Maintain bounded weekly repository history and derive multi-window trend signals."""
⋮----
SCHEMA_VERSION=1
⋮----
def empty_history()
⋮----
def load_history(path)
⋮----
data=json.loads(path.read_text())
⋮----
repositories={}
⋮----
def update(history,catalog,health,max_points=26,now=None)
⋮----
now=(now or datetime.now(timezone.utc)).date().isoformat()
if not isinstance(history,dict): history=empty_history()
store=history.get("repositories")
⋮----
store={}
history={"schemaVersion":SCHEMA_VERSION,"repositories":store}
⋮----
health_rows=health.get("repositories",[]) if isinstance(health,dict) else []
hmap={x.get("repo"):x for x in health_rows if isinstance(x,dict) and isinstance(x.get("repo"),str)} if isinstance(health_rows,list) else {}
catalog_rows=catalog.get("repositories",[]) if isinstance(catalog,dict) else []
⋮----
name=r.get("repo")
⋮----
gh=r.get("github",{}); gh=gh if isinstance(gh,dict) else {}
h=hmap.get(name,{})
point={"date":now,"health":h.get("score"),"status":h.get("status"),"stars":gh.get("stars"),"forks":gh.get("forks")}
points=store.get(name,[])
points=[p for p in points if isinstance(p,dict)] if isinstance(points,list) else []
⋮----
def window_metrics(points,size)
⋮----
pts=points[-size:] if size else points
⋮----
days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
except (ValueError,TypeError,KeyError): days=max(1,7*(len(pts)-1))
def delta(k)
⋮----
def trends(history)
⋮----
rows=[]
repositories=history.get("repositories",{}) if isinstance(history,dict) else {}
⋮----
pts=[p for p in pts if isinstance(p,dict)]
⋮----
w1=window_metrics(pts,2); w4=window_metrics(pts,5); full=window_metrics(pts,None)
recent=w4 or w1 or full
hd=recent.get("healthDelta")
direction="stable"
if hd is not None and hd<=-10: direction="declining"
elif hd is not None and hd>=10: direction="improving"
elif (recent.get("starsPerWeek") or 0)>0: direction="growing"
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("history",type=Path); ap.add_argument("catalog",type=Path); ap.add_argument("health",type=Path)
⋮----
args=ap.parse_args()
⋮----
history=load_history(args.history)
history=update(history,json.loads(args.catalog.read_text()),json.loads(args.health.read_text()),args.max_points)
````

## File: scripts/validate_catalog.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "catalog.json").read_text())
⋮----
valid_domains = {"ai_agents","ai_memory","ai_media","software_engineering","web_frontend","backend","mobile","graphics","game_dev","trading","cybersecurity","data_ml","devops","productivity","other"}
valid_roles = {"data","alpha","regime","backtest","risk","execution","portfolio","xauusd","macro","ml","microstructure","performance","volatility","optimization","forecasting","feature-engineering","derivatives","diagnostic","feature-selection","filtering"}
valid_tiers = {"core","recommended","specialized","indexed"}
valid_levels = {"low","medium","high"}
valid_lifecycles = {"active","stable","reference","legacy"}
valid_guidance_sources = {"curated","inferred"}
valid_license_evidence = {"verified-file","no-root-license-file"}
valid_license_statuses = {"not-found","custom-restrictive","partial","external-terms"}
seen = set()
repos = data.get("repositories", [])
⋮----
name = r.get("repo", "")
prefix = name or f"entry[{i}]"
⋮----
score = r.get("score")
⋮----
score = -1
⋮----
tier = r.get("tier")
⋮----
domain = r.get("domain")
⋮----
lifecycle = r.get("lifecycle")
⋮----
guidance_source = r.get("guidanceSource")
⋮----
license_evidence = r.get("licenseEvidence")
⋮----
license_status = r.get("licenseStatus")
⋮----
gh_license = (r.get("github") or {}).get("license") if isinstance(r.get("github"), dict) else None
⋮----
value = r.get(field, [])
⋮----
self_hosted = r.get("selfHosted")
⋮----
gh = r.get("github")
⋮----
value = gh.get(field)
⋮----
roles = set(r.get("roles", []))
bad = roles - valid_roles
⋮----
# Relationship integrity: known catalog repos only, no self-links.
⋮----
counts = Counter(r.get("domain") for r in repos)
````

## File: scripts/validate_json_contract.py
````python
#!/usr/bin/env python3
"""Validate JSON documents against the contract-focused JSON Schema subset used by star-list."""
⋮----
def _matches_type(value, expected)
⋮----
def _path(parent, key)
⋮----
SUPPORTED_KEYWORDS={
⋮----
def validate(value, schema, path="$")
⋮----
errors=[]
⋮----
unsupported=sorted(set(schema)-SUPPORTED_KEYWORDS)
⋮----
branches=schema.get("anyOf")
⋮----
expected=schema.get("type")
⋮----
allowed=expected if isinstance(expected, list) else [expected]
⋮----
required=schema.get("required",[])
⋮----
properties=schema.get("properties",{})
⋮----
additional=schema.get("additionalProperties",True)
known=set(properties) if isinstance(properties,dict) else set()
⋮----
seen=set()
⋮----
marker=json.dumps(item,sort_keys=True,ensure_ascii=False)
⋮----
items=schema.get("items")
⋮----
pattern=schema.get("pattern")
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(description="Validate a JSON document against a star-list JSON contract.")
⋮----
args=ap.parse_args()
⋮----
schema=json.loads(args.schema.read_text())
document=json.loads(args.document.read_text())
⋮----
errors=validate(document,schema)
````

## File: scripts/validate_websites.py
````python
#!/usr/bin/env python3
"""Audit website catalog URL identity and source usage without network access.

The schema checks structure. This adds security and deduplication rules that
JSON Schema cannot express; neither stage authorizes copying third-party code.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def canonical_url(value)
⋮----
parsed = urlsplit(value)
⋮----
def check_websites(data, schema)
⋮----
errors = list(validate(data, schema))
⋮----
ids = set()
owner_by_url = {}
⋮----
identity = site["id"]
⋮----
# 'originalUrl' records an old URL or user-supplied alternate link.
# Each such alias must remain attached
# to the same entry, not silently create an extra website identity.
⋮----
normalized = canonical_url(url)
⋮----
prior = owner_by_url.get(normalized)
⋮----
# Always-review declarations must not escape a website\'s stated domain.
baseline = set(site.get("portfolioBaselineDomains", []))
⋮----
# Specialist triggers must be explicit canonical labels, not prose.
required_signals = site.get("portfolioRequiredSignals", [])
⋮----
# Converted HF weights inherit upstream usage restrictions. The
# 'other' hub tag is unknown permission, never an approval to install
# or use images commercially; checkpoint provenance is mandatory.
⋮----
# Rewriting checkpoints must disclose verified supported languages
# and cannot be implicitly recommended to every chatbot.
⋮----
# Safety-modified multimodal checkpoints must carry an explicit
# reduced-refusal flag, not hide behind an open source licence.
⋮----
lowered_tags = {str(t).lower() for t in site["tags"]}
⋮----
# Social network automation is hosted, credential-sensitive and
# platform-policy sensitive. Never admit a blanket auto-publish tool.
⋮----
# Motion/cinema references and hosted visual generators must be
# selected for a concrete creative task. A game-dev domain alone
# never authorizes importing film/anime frames or invoking hosted AI.
visual_reuse_rules = {
expected_visual_reuse = visual_reuse_rules.get(site["type"])
⋮----
# Downloadable 3D datasets are assets, never runnable packages or
# blanket licences to import arbitrary generated meshes into games.
⋮----
# An MCP endpoint is an authenticated remote service, not a harmless
# website link. Require a bounded HTTPS /mcp URL owned by the
# documented provider; no credentials, foreign hosts or auto-install.
endpoint = site.get("mcpEndpoint")
is_mcp = site["type"] == "mcp-service"
⋮----
service = urlsplit(endpoint)
website = urlsplit(site["url"])
host = service.hostname.lower()
root = website.hostname.lower().removeprefix("www.")
⋮----
def main()
⋮----
data = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))
schema = json.loads((ROOT / "schemas/websites.schema.json").read_text(encoding="utf-8"))
errors = check_websites(data, schema)
````

## File: scripts/verify_catalog_evidence.py
````python
#!/usr/bin/env python3
"""Evidence-based, read-only by default triage for uncertain catalog metadata.

GitHub is the only remote source. A verified root licence can be applied with
--apply, but deployment configuration files are never proof that a project
is fully self-hostable.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN_LICENSE = (None, "", "NOASSERTION")
MAX_FILE_BYTES = 128 * 1024
LICENSE_STEMS = frozenset({"license", "licence", "copying"})
COMPOSE_FILES = frozenset({
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
⋮----
def root_files(payload)
⋮----
files = {}
⋮----
name = item.get("name")
path = item.get("path")
⋮----
def is_license_file(name)
⋮----
stem = re.split(r"[._-]", name.lower(), maxsplit=1)[0]
⋮----
def content_with_sha(payload)
⋮----
size = payload.get("size")
⋮----
sha = payload.get("sha")
⋮----
encoded = payload.get("content")
⋮----
raw = base64.b64decode(encoded, validate=False)
⋮----
actual_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
⋮----
text = raw.decode("utf-8")
⋮----
def blob_evidence(name, sha)
⋮----
# Immutable blob reference, not a mutable default-branch page.
⋮----
def inspect_entry(entry, fetch_repo=github.fetch, fetch_content=github.fetch_contents, token=None)
⋮----
name = entry.get("repo")
⋮----
gh = entry.get("github") or {}
⋮----
raw = fetch_repo(name, token=token)
⋮----
expected_id = entry.get("githubRepositoryId")
actual_id = raw.get("id")
⋮----
branch = raw.get("default_branch")
⋮----
files = root_files(fetch_content(name, ref=branch, token=token))
item = {
api_license = raw.get("license")
api_spdx = api_license.get("spdx_id") if isinstance(api_license, dict) else None
⋮----
strong = set()
scoped = False
⋮----
payload = fetch_content(name, path=file["path"], ref=branch, token=token)
⋮----
scoped = True
⋮----
detected = github.strict_root_license(content)
⋮----
verified = next(iter(strong))
⋮----
# A previous restrictive/partial/external-terms review is not
# invalidated by finding one apparently permissive root file.
⋮----
# Never infer selfHosted=True from root Docker files; report candidates
# for human examination instead.
⋮----
file = files.get(filename)
⋮----
def requires_review(row)
⋮----
"""Watch missing facts and inactive projects, without gating discovery."""
gh = row.get("github")
⋮----
def select_entries(repos, limit, batch_index, selected_names)
⋮----
uncertain = [row for row in repos if requires_review(row)]
⋮----
by_name = {row.get("repo"): row for row in repos}
missing = sorted(set(selected_names) - set(by_name))
⋮----
rows = [by_name[name] for name in selected_names]
⋮----
rows = sorted(uncertain, key=lambda x: x["repo"].lower())
chunks = max(1, (len(rows) + limit - 1) // limit)
⋮----
rows = rows[batch_index * limit:(batch_index + 1) * limit]
⋮----
by_name = {x.get("repo"): x for x in repos}
⋮----
result = inspect_entry(entry, fetch_repo, fetch_content, token)
⋮----
license_value = result.get("proposedLicense")
⋮----
current = by_name[result["repository"]]
⋮----
# API failures and identity conflicts are never interpreted as
# 'not licensed' or 'not self-hostable'.
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Verify evidence for uncertain Star List metadata.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(args.catalog.read_text(encoding="utf-8"))
repos = data["repositories"]
⋮----
result = audit(repos, entries, total_uncertain, token=os.environ.get("GITHUB_TOKEN"),
⋮----
# An interrupted process must never leave a partially written catalog.
⋮----
temporary_path = Path(handle.name)
⋮----
# Fail closed; avoid partial catalog writes if even one source failed.
⋮----
encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
````

## File: .repo-standards.yml
````yaml
source: dbrckk/repo-standards
ref: main
version: 20
adopted: true
workflow_mode: unified-single-commit
repo_brain: dbrckk/repo-brain@main
repo_brain_fallback: portable-full-rebuild
hotset_fallback: recent-project-state
graph_routing: compact-sharded-reverse-deps
graph_resolver: java-kotlin-tail-v2
graph_enrichment: unique-type-symbol-references-v1
context_budget: confidence-dynamic-3-6-12
routing_learning: deterministic-term-feedback-v1
auto_routing_learning: source-diff-success-v1
validation_memory: passed-failed-test-history-v1
regression_gate: repo-brain-core-tests-v1
benchmark: routing-benchmark-v1
stability_profile: stable-v1
benchmark_guard: avg-files-le-6-cache-required-v1
ai_context:
  index: .ai/index.md
  project_state: .ai/project-state.md
  change_impact: .ai/change-impact.md
  architecture: .ai/architecture.json
  dependency_map: .ai/dependency-map.json
  commands: .ai/commands.json
  ci_status: .ai/ci-status.md
  security_signals: .ai/security-signals.json
  repo_health: .ai/repo-health.md
  brain_summary: .ai/brain/summary.md
  brain_incremental_state: .ai/brain/incremental-state.json
  brain_impact: .ai/brain/impact.json
  brain_selected_tests: .ai/brain/selected-tests.json
  brain_references: .ai/brain/references.json
  brain_symbol_dependencies: .ai/brain/symbol-dependencies.json
  brain_capabilities: .ai/brain/capabilities.json
  brain_ast_routing: .ai/brain/ast-routing.json
  brain_ast_symbols: .ai/brain/ast-symbols/
  brain_file_outlines: .ai/brain/file-outlines/
  brain_lookup: .ai/brain/lookup.json
  brain_symbols: .ai/brain/symbols.json
  brain_graph: .ai/brain/code-graph.json
  brain_graph_index: .ai/brain/graph-index.json
  brain_graph_enrichment: .ai/brain/graph-enrichment.json
  brain_graph_manifest: .ai/brain/graph-manifest.json
  brain_graph_shards: .ai/brain/graph-shards/
  brain_reverse_deps: .ai/brain/reverse-deps.json
  brain_architecture_mermaid: .ai/brain/architecture.mmd
  brain_semantic_plan: .ai/brain/semantic-plan.json
  brain_semantic_index: .ai/brain/semantic-index.json
  brain_search_manifest: .ai/brain/search-manifest.json
  brain_search_shards: .ai/brain/search-shards/
  brain_query_cache: .ai/brain/query-cache.json
  brain_routing_learning: .ai/brain/routing-learning.json
  brain_auto_learning: .ai/brain/auto-learning.json
  brain_validation_memory: .ai/brain/validation-memory.json
  brain_benchmark: .ai/brain/benchmark.json
  brain_benchmark_health: .ai/brain/benchmark-health.json
  brain_hotset: .ai/brain/hotset.json
  brain_context_manifest: .ai/brain/context-manifest.json
  brain_context_packets: .ai/brain/context/
  brain_hash_cache: .ai/brain/hash-cache.json
  session_state: .ai/session-state.json
  repo_map: .ai/repo-map.md
  segmented_maps: .ai/maps/
workflow:
  file: .github/workflows/ai-repo-map.yml
  reusable_unified: .github/workflows/reusable-unified.yml
  semantic_refresh: .github/workflows/semantic-refresh.yml
````

## File: agent-skills.json
````json
{
  "schemaVersion": 1,
  "directory": {
    "id": "skill-issue",
    "name": "Skill Issue",
    "url": "https://skill-issue.in/",
    "discoveredOn": "2026-10-18",
    "usage": "read-only discovery; never auto-install external instructions",
    "priority": "portfolio-wide"
  },
  "description": "Conservative shortlist of agent-skill references from Skill Issue and supplementary official/engine-specific upstream sources. Every exact SKILL.md path is pinned to a Git commit for manual license, instruction and runtime review; no skill is audited or installed automatically.",
  "skills": [
    {
      "id": "ui-ux-pro-max-skill",
      "name": "UI UX Pro Max",
      "sourceRepository": "nextlevelbuilder/ui-ux-pro-max-skill",
      "domains": [
        "web_frontend",
        "mobile",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "ui",
        "ux",
        "design",
        "android",
        "mobile",
        "game",
        "interface",
        "palettes",
        "typography"
      ],
      "description": "UI design reference and design-system exploration across stacks.",
      "languages": [],
      "sourceUrl": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "56ea9cf174ed86786187daa9de0e6247cb0747e4",
      "sourcePath": ".claude/skills/ui-ux-pro-max/SKILL.md"
    },
    {
      "id": "frontend-design",
      "name": "Frontend Design",
      "sourceRepository": "anthropics/skills",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "frontend",
        "design",
        "ui",
        "web",
        "website",
        "landing",
        "interface"
      ],
      "description": "Distinctive frontend layout and styling guidance.",
      "languages": [],
      "sourceUrl": "https://github.com/anthropics/skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "dbd4588f9e1033efb41dad4bef2f7947c8993d44",
      "sourcePath": "skills/frontend-design/SKILL.md"
    },
    {
      "id": "agent-browser",
      "name": "Agent Browser",
      "sourceRepository": "vercel-labs/agent-browser",
      "domains": [
        "web_frontend",
        "software_engineering",
        "ai_agents",
        "productivity"
      ],
      "tags": [
        "browser",
        "e2e",
        "playwright",
        "automation",
        "testing",
        "website",
        "web"
      ],
      "description": "Automated browser interactions and visual web inspection.",
      "languages": [],
      "sourceUrl": "https://github.com/vercel-labs/agent-browser",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "dac13bb87468fe9d74a040d862720f6cc17a9565",
      "sourcePath": "skills/agent-browser/SKILL.md"
    },
    {
      "id": "react-best-practices",
      "name": "React Best Practices",
      "sourceRepository": "vercel-labs/agent-skills",
      "domains": [
        "web_frontend"
      ],
      "tags": [
        "react",
        "nextjs",
        "next",
        "javascript",
        "typescript",
        "performance",
        "frontend"
      ],
      "description": "React and Next.js rendering/performance guidelines.",
      "languages": [
        "JavaScript",
        "TypeScript"
      ],
      "sourceUrl": "https://github.com/vercel-labs/agent-skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "063bee94c3f4df8453406c830b0a7df0f2860278",
      "sourcePath": "skills/react-best-practices/SKILL.md"
    },
    {
      "id": "web-design-guidelines",
      "name": "Web Design Guidelines",
      "sourceRepository": "vercel-labs/agent-skills",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "web",
        "ui",
        "ux",
        "accessibility",
        "design",
        "frontend"
      ],
      "description": "Interface quality, accessibility, and interaction review guidance.",
      "languages": [],
      "sourceUrl": "https://github.com/vercel-labs/agent-skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "063bee94c3f4df8453406c830b0a7df0f2860278",
      "sourcePath": "skills/web-design-guidelines/SKILL.md"
    },
    {
      "id": "remotion-best-practices",
      "name": "Remotion Best Practices",
      "sourceRepository": "remotion-dev/skills",
      "domains": [
        "ai_media",
        "graphics",
        "web_frontend"
      ],
      "tags": [
        "video",
        "motion",
        "remotion",
        "animation",
        "captions",
        "audio"
      ],
      "description": "Programmatic video editing/animation using Remotion.",
      "languages": [
        "JavaScript",
        "TypeScript"
      ],
      "sourceUrl": "https://github.com/remotion-dev/skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "1441a11e95db35443bd76bb318386c0d3ca00053",
      "sourcePath": "skills/remotion-best-practices/SKILL.md"
    },
    {
      "id": "api-design-principles",
      "name": "API Design Principles",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "backend",
        "software_engineering",
        "devops"
      ],
      "tags": [
        "api",
        "backend",
        "rest",
        "graphql",
        "endpoints",
        "architecture",
        "openapi"
      ],
      "description": "API design patterns and review for REST and GraphQL.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false,
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/backend-development/skills/api-design-principles/SKILL.md"
    },
    {
      "id": "design-taste-frontend",
      "name": "Design Taste Frontend",
      "sourceRepository": "Leonxlnx/taste-skill",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "frontend",
        "design",
        "ui",
        "landing",
        "website",
        "layout",
        "typography",
        "branding"
      ],
      "description": "Art direction and visual quality workflow for frontend work.",
      "languages": [],
      "sourceUrl": "https://github.com/Leonxlnx/taste-skill",
      "sourceCommit": "f624f37a8c650b9cc550253104925efe4c8de246",
      "sourcePath": "skills/taste-skill/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "redesign-existing-projects",
      "name": "Redesign Existing Projects",
      "sourceRepository": "Leonxlnx/taste-skill",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "redesign",
        "ui",
        "ux",
        "layout",
        "website",
        "web",
        "frontend"
      ],
      "description": "Existing-project interface auditing and redesign workflow.",
      "languages": [],
      "sourceUrl": "https://github.com/Leonxlnx/taste-skill",
      "sourceCommit": "f624f37a8c650b9cc550253104925efe4c8de246",
      "sourcePath": "skills/redesign-skill/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "image-to-code",
      "name": "Image to Code",
      "sourceRepository": "Leonxlnx/taste-skill",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "image",
        "screenshot",
        "ui",
        "design",
        "frontend",
        "website"
      ],
      "description": "Reference-image analysis and frontend reconstruction workflow.",
      "languages": [],
      "sourceUrl": "https://github.com/Leonxlnx/taste-skill",
      "sourceCommit": "f624f37a8c650b9cc550253104925efe4c8de246",
      "sourcePath": "skills/image-to-code-skill/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "design-system-patterns",
      "name": "Design System Patterns",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend",
        "graphics",
        "mobile"
      ],
      "tags": [
        "design",
        "system",
        "tokens",
        "theming",
        "components",
        "ui",
        "mobile"
      ],
      "description": "Design tokens and component system architecture; review original skill before use.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/ui-design/skills/design-system-patterns/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "nextjs-app-router-patterns",
      "name": "Next.js App Router Patterns",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend"
      ],
      "tags": [
        "nextjs",
        "react",
        "app",
        "router",
        "frontend",
        "typescript"
      ],
      "description": "Next.js App Router and server component architecture guidance.",
      "languages": [
        "TypeScript",
        "JavaScript"
      ],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/frontend-mobile-development/skills/nextjs-app-router-patterns/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "react-state-management",
      "name": "React State Management",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend"
      ],
      "tags": [
        "react",
        "state",
        "zustand",
        "jotai",
        "query",
        "frontend"
      ],
      "description": "React state-management patterns and library selection.",
      "languages": [
        "TypeScript",
        "JavaScript"
      ],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/frontend-mobile-development/skills/react-state-management/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "tailwind-design-system",
      "name": "Tailwind Design System",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "tailwind",
        "css",
        "shadcn",
        "design",
        "components",
        "frontend"
      ],
      "description": "Tailwind CSS theme and component system patterns.",
      "languages": [
        "TypeScript",
        "JavaScript"
      ],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/frontend-mobile-development/skills/tailwind-design-system/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "responsive-design",
      "name": "Responsive Design",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend",
        "mobile",
        "graphics"
      ],
      "tags": [
        "responsive",
        "layout",
        "css",
        "mobile",
        "web",
        "frontend"
      ],
      "description": "Adaptive layouts and interaction design for changing screen sizes.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/ui-design/skills/responsive-design/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "accessibility-compliance",
      "name": "Accessibility Compliance",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "web_frontend",
        "mobile"
      ],
      "tags": [
        "accessibility",
        "aria",
        "wcag",
        "ux",
        "ui",
        "frontend"
      ],
      "description": "Accessibility audits and WCAG guidance for interface projects.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/ui-design/skills/accessibility-compliance/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "react-native-architecture",
      "name": "React Native Architecture",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "mobile"
      ],
      "tags": [
        "react",
        "native",
        "expo",
        "android",
        "ios",
        "mobile"
      ],
      "description": "React Native and Expo architecture guidance, not native Kotlin tooling.",
      "languages": [
        "JavaScript",
        "TypeScript"
      ],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/frontend-mobile-development/skills/react-native-architecture/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "auth-implementation-patterns",
      "name": "Authentication Implementation Patterns",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "backend",
        "web_frontend",
        "software_engineering"
      ],
      "tags": [
        "auth",
        "authentication",
        "oauth",
        "jwt",
        "security",
        "backend"
      ],
      "description": "Authentication patterns across web services.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/developer-essentials/skills/auth-implementation-patterns/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "openapi-spec-generation",
      "name": "OpenAPI Specification Generation",
      "sourceRepository": "wshobson/agents",
      "domains": [
        "backend",
        "software_engineering"
      ],
      "tags": [
        "api",
        "openapi",
        "rest",
        "schema",
        "documentation",
        "backend"
      ],
      "description": "API schema documentation and OpenAPI generation workflow.",
      "languages": [],
      "sourceUrl": "https://github.com/wshobson/agents",
      "sourceCommit": "0874a27b17a22e2b7c2e2bcd725768e0803cad06",
      "sourcePath": "plugins/documentation-generation/skills/openapi-spec-generation/SKILL.md",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "flutter-responsive-layout",
      "name": "Flutter Responsive Layout",
      "sourceRepository": "flutter/agent-plugins",
      "sourceCommit": "b60d0736a33a0de7d3f4ea2a7ad740ca0daa5c94",
      "sourcePath": "skills/flutter-build-responsive-layout/SKILL.md",
      "domains": [
        "mobile"
      ],
      "tags": [
        "flutter",
        "dart",
        "responsive",
        "mobile",
        "layout",
        "widgets"
      ],
      "description": "Official Flutter guidance for adaptive widgets, screens and layout constraints.",
      "languages": [
        "Dart"
      ],
      "sourceUrl": "https://github.com/flutter/agent-plugins",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "flutter-layout-diagnostics",
      "name": "Flutter Layout Diagnostics",
      "sourceRepository": "flutter/agent-plugins",
      "sourceCommit": "b60d0736a33a0de7d3f4ea2a7ad740ca0daa5c94",
      "sourcePath": "skills/flutter-fix-layout-issues/SKILL.md",
      "domains": [
        "mobile"
      ],
      "tags": [
        "flutter",
        "dart",
        "layout",
        "widgets",
        "overflow",
        "responsive"
      ],
      "description": "Official Flutter reference for diagnosing layout constraints and overflow errors.",
      "languages": [
        "Dart"
      ],
      "sourceUrl": "https://github.com/flutter/agent-plugins",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "godot-gdscript",
      "name": "Godot GDScript 4.x",
      "sourceRepository": "shihabshahrier/Godot-Skill",
      "sourceCommit": "c8bc20f876a8da241274d48461444fab86182d83",
      "sourcePath": "skills/godot/SKILL.md",
      "domains": [
        "game_dev"
      ],
      "tags": [
        "godot",
        "gdscript",
        "game",
        "gameplay",
        "signals",
        "scenes",
        "animation"
      ],
      "description": "Godot 4.3+ GDScript reference for typed scenes, signals, architecture and common gameplay patterns.",
      "languages": [
        "GDScript"
      ],
      "sourceUrl": "https://github.com/shihabshahrier/Godot-Skill",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "android-compose-performance",
      "name": "Jetpack Compose Performance",
      "sourceRepository": "android/skills",
      "sourceCommit": "5bda39f154fb859a08d45e2392f3568e049f83fb",
      "sourcePath": "jetpack-compose/jetpack-compose-performance/SKILL.md",
      "domains": [
        "mobile"
      ],
      "tags": [
        "compose",
        "jetpack",
        "recomposition",
        "material3"
      ],
      "description": "Official Android guidance for diagnosing Jetpack Compose recomposition, scrolling and rendering performance; only relevant to apps confirmed to use Compose.",
      "languages": [
        "Kotlin"
      ],
      "sourceUrl": "https://github.com/android/skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "android-play-policy-insights",
      "name": "Android Play Policy Insights",
      "sourceRepository": "android/skills",
      "sourceCommit": "5bda39f154fb859a08d45e2392f3568e049f83fb",
      "sourcePath": "play/play-policy-insights/SKILL.md",
      "domains": [
        "mobile"
      ],
      "tags": [
        "android",
        "play",
        "store",
        "release",
        "publishing",
        "policy",
        "privacy",
        "compliance"
      ],
      "description": "Official Android guidance for reviewing app permissions, data safety and policy disclosures before Google Play submission.",
      "languages": [],
      "sourceUrl": "https://github.com/android/skills",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    },
    {
      "id": "roblox-luau-development",
      "name": "Roblox Luau Development",
      "sourceRepository": "MSayib/roblox-dev-skill",
      "sourceCommit": "4a35b01cb07eb237081bee705455e19db37342d8",
      "sourcePath": "SKILL.md",
      "domains": [
        "game_dev"
      ],
      "tags": [
        "roblox",
        "luau",
        "studio"
      ],
      "description": "MIT-licensed Roblox Studio and Luau development reference for architecture, secure remotes, performance and current engine APIs.",
      "languages": [],
      "sourceUrl": "https://github.com/MSayib/roblox-dev-skill",
      "verification": "upstream-repository-exists",
      "integrationEligible": false,
      "skillCodeReviewed": false
    }
  ]
}
````

## File: AGENTS.md
````markdown
# Repository agent instructions

## Shared development policy — 88 validated rules (2026-10-09)

The project adopts the [88-rule standard](https://github.com/dbrckk/repo-standards/blob/db2f86657ada74a0561e07189f9942d6b66ebb4a/standards/88-rules.md), the [operational agent skill](https://github.com/dbrckk/repo-standards/blob/db2f86657ada74a0561e07189f9942d6b66ebb4a/skills/repo-excellence-88/SKILL.md), and the [educational wiki](https://github.com/dbrckk/repo-standards/blob/db2f86657ada74a0561e07189f9942d6b66ebb4a/docs/WIKI-88.md). Read the relevant parts before substantial work and apply conditional rules only where appropriate.

**Owner preference: do not create new unit tests.** Existing tests may be run for diagnostics; prioritize real functional and integration verification, lint, build, and reproducible checks. Never claim an unexecuted check passed.

Preserve repository-specific constraints and authorized scope. The pinned policy commit above governs the 88 rules; `.repo-standards.yml` continues to configure existing repository intelligence and reusable workflows independently. Do not change workflow refs merely to adopt these rules.


This repository adopts shared standards from `dbrckk/repo-standards` at the release recorded in `.repo-standards.yml`.

Before substantial work:
1. Read the central `AGENTS.md` and relevant standards at the configured ref.
2. Read `.ai/session-state.json` when present.
3. Read `.ai/project-state.md`.
4. Read `.ai/brain/hotset.json`.
5. Read `.ai/brain/context-manifest.json` and only the relevant `.ai/brain/context/<area>.json` packet.
6. Read `.ai/brain/graph-index.json` and the relevant `.ai/brain/graph-shards/<area>.json` when dependency routing matters.
7. Use `.ai/brain/reverse-deps.json` for upstream/downstream file impact.
8. Read `.ai/brain/impact.json` and `.ai/brain/selected-tests.json`.
9. Read `.ai/brain/references.json` and `.ai/brain/symbol-dependencies.json` only when symbol routing requires them.
10. Read `.ai/change-impact.md` and `.ai/architecture.json` when broader structure is needed.
11. Read `.ai/brain/summary.md`, `.ai/brain/incremental-state.json`, and `.ai/brain/capabilities.json` when index freshness/capabilities matter.
12. If ast-grep enrichment is available, route named symbols through `.ai/brain/ast-routing.json` and one `.ai/brain/ast-symbols/<initial>.json` shard.
13. Fall back to `.ai/brain/lookup.json` when AST routing is unavailable or insufficient.
14. Use `.ai/brain/code-graph.json` and `.ai/brain/imports.json` for cross-module context.
15. Read `.ai/dependency-map.json` when dependency context matters.
16. Read `.ai/commands.json`, `.ai/ci-status.md`, and security signals when relevant.
17. Read `.ai/repo-health.md`.
18. Use `.ai/index.md` and segmented maps only if bounded context is insufficient.
19. Read `.ai/repo-map.md` only as a final broad-context fallback.
20. Fetch only task-relevant source files or line ranges.

## Agent skill discovery

For relevant implementation tasks, first consult
[`AGENT_SKILLS.md`](AGENT_SKILLS.md) and
[`agent-skills.json`](agent-skills.json) for task-specific source references from
[Skill Issue](https://skill-issue.in/). This is discovery guidance; review
full upstream `SKILL.md`, scripts, license, revision, dependencies and
credentials before selective adoption. Never execute remote installers
merely because a site lists a skill, and never use skill recommendations
as Production-OS integration dispatch candidates.

Repository-specific rules:
- Preserve existing architecture and public interfaces unless the task requires a change.
- Prefer the smallest coherent change.
- Prefer targeted functional or integration checks; existing selected tests may be run as diagnostics, but do not create new unit tests. Expand validation when impact is ambiguous.
- Treat hotset/context packets and graph shards as routing hints, not authoritative source.
- Verify reference/dependency/impact/AST hits against authoritative source before editing.
- Treat security signals and static graph edges as heuristics, not proof.
- Never reproduce suspected secret values.
- Update manual project-state sections when status, blockers, or next priority materially changes.
- Maintain `.ai/session-state.json` for substantial multi-turn work so a later "Continue" can resume without reconstructing the repository.
````

## File: catalog-readme-evidence.json
````json
{
  "schemaVersion": 1,
  "sourceType": "reviewed-readme-blob",
  "sources": [
    {
      "repository": "Asad-Ismail/MoneyPrinterTurbo-Extended",
      "githubRepositoryId": 988352805,
      "path": "README.md",
      "blobSha": "affa3a55666123d2f886ea43b86ab091461bad39",
      "advisoryDomains": [
        "ai_media"
      ],
      "taskTerms": [
        "video",
        "subtitles",
        "tts",
        "voice",
        "clips"
      ],
      "evidenceSnippet": "subtitle highlighting and TTS capabilities",
      "reviewNotes": "Fork description; runtime/model costs must be checked."
    },
    {
      "repository": "hexgrad/kokoro",
      "githubRepositoryId": 915054134,
      "path": "README.md",
      "blobSha": "765dcc77ff656885225fd882d3e7c3c67545325b",
      "advisoryDomains": [
        "ai_media"
      ],
      "taskTerms": [
        "tts",
        "speech",
        "voice",
        "audio",
        "synthesis"
      ],
      "evidenceSnippet": "an open-weight TTS model with 82 million parameters",
      "reviewNotes": "Model weights and library licensing must be assessed separately."
    },
    {
      "repository": "HVision-NKU/StoryDiffusion",
      "githubRepositoryId": 789712717,
      "path": "README.md",
      "blobSha": "2b2c0da824c16f0b01ede7b70823eec9ab7864e0",
      "advisoryDomains": [
        "ai_media"
      ],
      "taskTerms": [
        "image",
        "video",
        "generation",
        "characters",
        "comics"
      ],
      "evidenceSnippet": "Image and Video Generation",
      "reviewNotes": "Experimental model; verify model usage rights and runtime requirements."
    },
    {
      "repository": "KarakuriAgent/h3-motion-creator",
      "githubRepositoryId": 1427850125,
      "path": "README.md",
      "blobSha": "087c44ba30913341e18ea212720356eea20e1588",
      "advisoryDomains": [
        "graphics"
      ],
      "taskTerms": [
        "vrm",
        "animation",
        "motion",
        "rig",
        "video",
        "3d"
      ],
      "evidenceSnippet": "VRM Animation",
      "reviewNotes": "Model weights not included; external model and workflow restrictions apply."
    },
    {
      "repository": "Tencent-Hunyuan/Hy-MT2",
      "githubRepositoryId": 1242193963,
      "path": "README.md",
      "blobSha": "5198cf68c804ac698d756934ae24d12d4107b763",
      "advisoryDomains": [
        "data_ml",
        "ai_media"
      ],
      "taskTerms": [
        "translation",
        "multilingual",
        "subtitles",
        "model"
      ],
      "evidenceSnippet": "multilingual translation models",
      "reviewNotes": "Translation model licensing and compute are separate from repository metadata."
    },
    {
      "repository": "mcncarl/jianying-headless",
      "githubRepositoryId": 1371378654,
      "path": "README.md",
      "blobSha": "b27670ba1e9521ef65139927087e0b7552aa97e9",
      "advisoryDomains": [
        "ai_media"
      ],
      "taskTerms": [
        "video",
        "editing",
        "drafts",
        "subtitles",
        "export",
        "mp4"
      ],
      "evidenceSnippet": "多轨工程",
      "reviewNotes": "macOS Jianying version constraints; no claim of Android or arbitrary-platform compatibility."
    },
    {
      "repository": "GoogleCloudPlatform/genmedia-izumi-agent",
      "githubRepositoryId": 1199868922,
      "path": "README.md",
      "blobSha": "e99607138abbf5e886737ca72324ced12cc8fdc4",
      "advisoryDomains": [
        "ai_media",
        "marketing",
        "ai_agents"
      ],
      "taskTerms": [
        "multimedia",
        "advertising",
        "agents",
        "media",
        "creative",
        "video"
      ],
      "evidenceSnippet": "Automated Multimedia Advertisement Creation",
      "reviewNotes": "Example reference architecture; Google Cloud services may incur costs."
    },
    {
      "repository": "higgsfield-ai/skills",
      "githubRepositoryId": 1206425593,
      "path": "README.md",
      "blobSha": "682610d4189c0c6fbfb68b3753fcc86ccd43e247",
      "advisoryDomains": [
        "ai_media",
        "marketing",
        "graphics"
      ],
      "taskTerms": [
        "video",
        "images",
        "animation",
        "branding",
        "marketing"
      ],
      "evidenceSnippet": "AI agent skills for image/video generation",
      "reviewNotes": "External Higgsfield CLI/auth and service terms must be checked."
    },
    {
      "repository": "towfiqi/serpbear",
      "githubRepositoryId": 570178488,
      "path": "README.md",
      "blobSha": "9ad775e1d003648be1f8c6b378e9eba7bee3ca54",
      "advisoryDomains": [
        "marketing"
      ],
      "taskTerms": [
        "seo",
        "serp",
        "keywords",
        "ranking",
        "analytics"
      ],
      "evidenceSnippet": "Search Engine Position Tracking and Keyword Research App",
      "reviewNotes": "External SERP providers may require payment."
    },
    {
      "repository": "neilsonnn/image-blaster",
      "githubRepositoryId": 1216542069,
      "path": "README.md",
      "blobSha": "633aa3bf4ea17d4516138132758b07229948df90",
      "advisoryDomains": [
        "graphics",
        "game_dev"
      ],
      "taskTerms": [
        "3d",
        "models",
        "meshes",
        "assets",
        "sfx",
        "environments"
      ],
      "evidenceSnippet": "Creates 3D environments, SFX, and meshes from a single image",
      "reviewNotes": "World Labs and FAL API keys are required."
    },
    {
      "repository": "baidu/Unlimited-OCR",
      "githubRepositoryId": 1273138090,
      "path": "README.md",
      "blobSha": "b8cbea5cf9be8852e29d1a502175d9999e068428",
      "advisoryDomains": [
        "data_ml"
      ],
      "taskTerms": [
        "ocr",
        "document",
        "parsing",
        "text",
        "images"
      ],
      "evidenceSnippet": "Unlimited OCR Works",
      "reviewNotes": "Model terms, hardware and deployment remain unverified."
    },
    {
      "repository": "anthropics/claude-quickstarts",
      "githubRepositoryId": 849553306,
      "path": "README.md",
      "blobSha": "9cac84096b77c32521c718f5b507aa866ed232b1",
      "advisoryDomains": [
        "ai_agents",
        "software_engineering"
      ],
      "taskTerms": [
        "agent",
        "api",
        "coding",
        "browser",
        "computer",
        "tools"
      ],
      "evidenceSnippet": "Claude Quickstarts is a collection of projects",
      "reviewNotes": "Requires Claude API credentials and possibly paid usage."
    },
    {
      "repository": "richiemcilroy/Tov",
      "githubRepositoryId": 1396004915,
      "path": "README.md",
      "blobSha": "57fd4ce5f60f0e2a1e33a2bc2fc99230d18e6104",
      "advisoryDomains": [
        "software_engineering"
      ],
      "taskTerms": [
        "programming",
        "language",
        "compiler",
        "typescript",
        "coding"
      ],
      "evidenceSnippet": "A programming language for coding agents",
      "reviewNotes": "Early 0.0.1 release; not production-validated."
    },
    {
      "repository": "withmarbleapp/os-taxonomy",
      "githubRepositoryId": 1293375068,
      "path": "README.md",
      "blobSha": "6d05f5b5c5cd60e23ec1bd35ce5a06e26fb87ebe",
      "advisoryDomains": [
        "education"
      ],
      "taskTerms": [
        "curriculum",
        "education",
        "learning",
        "school",
        "teaching",
        "standards"
      ],
      "evidenceSnippet": "An open, structured taxonomy of **what children learn**",
      "reviewNotes": "Education taxonomy is not a runtime dependency."
    },
    {
      "repository": "h0m3us3r/eSpDR",
      "githubRepositoryId": 1387871388,
      "path": "README.md",
      "blobSha": "5c6b1fedc45293e6b10d49adb969b1bb1a0c0a45",
      "advisoryDomains": [
        "embedded_iot"
      ],
      "taskTerms": [
        "esp32",
        "sdr",
        "radio",
        "firmware",
        "receiver"
      ],
      "evidenceSnippet": "ESP32-S3 SDR",
      "reviewNotes": "Hardware-dependent experimental design."
    },
    {
      "repository": "luigifcruz/BirriaSDR",
      "githubRepositoryId": 1416428935,
      "path": "README.md",
      "blobSha": "9ca6a2a6af1875055145882709a68323c3fd5904",
      "advisoryDomains": [
        "embedded_iot"
      ],
      "taskTerms": [
        "sdr",
        "radio",
        "receiver",
        "usb",
        "hardware"
      ],
      "evidenceSnippet": "experimental SDR receiver",
      "reviewNotes": "Experimental hardware and uncalibrated receiver."
    },
    {
      "repository": "mcncarl/yichen-skills",
      "githubRepositoryId": 1155113456,
      "path": "README.md",
      "blobSha": "c2aaa5387062b9b1282ba4c17d3a25ea644d1a8a",
      "advisoryDomains": [
        "writing",
        "marketing",
        "ai_agents"
      ],
      "taskTerms": [
        "writing",
        "skills",
        "articles",
        "content",
        "publishing"
      ],
      "evidenceSnippet": "A skill collection for creators",
      "reviewNotes": "Commercial use requires explicit author permission."
    },
    {
      "repository": "pluginagentmarketplace/custom-plugin-game-developer",
      "githubRepositoryId": 1099329268,
      "path": "README.md",
      "blobSha": "653a0c33cf1326d36e3220ce564b0fefaa7a1863",
      "advisoryDomains": [
        "game_dev",
        "ai_agents"
      ],
      "taskTerms": [
        "game",
        "development",
        "agents",
        "skills",
        "engine"
      ],
      "evidenceSnippet": "Game Developer Assistant",
      "reviewNotes": "Custom licence; inspect before any code reuse."
    },
    {
      "repository": "rivet-dev/skills",
      "githubRepositoryId": 1140411856,
      "path": "README.md",
      "blobSha": "95438b7d2248a1a4bd121288327a78d1c8a7471d",
      "advisoryDomains": [
        "ai_agents"
      ],
      "taskTerms": [
        "skills",
        "agents",
        "integrations",
        "rivet"
      ],
      "evidenceSnippet": "Rivet Skills",
      "reviewNotes": "Generated documentation, not a directly installable library."
    },
    {
      "repository": "alexngdev99/rork-restaurant-tycoon",
      "githubRepositoryId": 1415197387,
      "path": "README.md",
      "blobSha": "8817c3e806540adddfd34989258c2dd26f27d7ef",
      "advisoryDomains": [
        "game_dev",
        "web_frontend"
      ],
      "taskTerms": [
        "game",
        "tycoon",
        "simulation",
        "react",
        "threejs"
      ],
      "evidenceSnippet": "3D restaurant management sim that runs in your browser",
      "reviewNotes": "Reference game, not a reusable engine."
    },
    {
      "repository": "omer-metin/skills-for-antigravity",
      "githubRepositoryId": 1139862645,
      "path": "README.md",
      "blobSha": "a17e4d683bcaf4f1eaeb9308921ed397a1ce3c51",
      "advisoryDomains": [
        "ai_agents"
      ],
      "taskTerms": [
        "skills",
        "agent",
        "development",
        "antigravity"
      ],
      "evidenceSnippet": "collection of **462+ AI Skills**",
      "reviewNotes": "Third-party converted skill instructions require review before use."
    },
    {
      "repository": "dalathegreat/Battery-Emulator",
      "githubRepositoryId": 603860295,
      "path": "README.md",
      "blobSha": "84943baacb1c41522c5f7d65e41414a87c3f3d06",
      "advisoryDomains": [
        "embedded_iot"
      ],
      "taskTerms": [
        "battery",
        "firmware",
        "energy",
        "storage",
        "electric"
      ],
      "evidenceSnippet": "EV battery packs to be repurposed for stationary storage",
      "reviewNotes": "Physical electrical system: do not infer safe deployment from documentation."
    },
    {
      "repository": "RegeneratusLabs/physical-hermes",
      "githubRepositoryId": 1424195755,
      "path": "README.md",
      "blobSha": "1b4fd2f438f5af289125390aaee7379cf866c9a1",
      "advisoryDomains": [
        "embedded_iot",
        "ai_agents"
      ],
      "taskTerms": [
        "esp32",
        "robot",
        "voice",
        "agent",
        "firmware"
      ],
      "evidenceSnippet": "Give your Hermes Agent a body.",
      "reviewNotes": "Requires compatible robot hardware, flashing and a running agent."
    },
    {
      "repository": "AskAillex/comic-maker",
      "githubRepositoryId": 1303321172,
      "path": "README.md",
      "blobSha": "2dda9ddf15f3f32a614c5d9c9a42feb9a4f45168",
      "advisoryDomains": [
        "ai_media",
        "graphics"
      ],
      "taskTerms": [
        "comics",
        "images",
        "illustrations",
        "story",
        "panels"
      ],
      "evidenceSnippet": "one sentence → a lettered comic, fully local",
      "reviewNotes": "Early development and local model dependencies."
    },
    {
      "repository": "Antseed/AIPs",
      "githubRepositoryId": 1291163775,
      "path": "README.md",
      "blobSha": "dbb2eaaeb9789eb8f0d1fb33cce2808b3a3805fe",
      "advisoryDomains": [
        "software_engineering"
      ],
      "taskTerms": [
        "protocol",
        "specification",
        "documentation",
        "p2p",
        "network"
      ],
      "evidenceSnippet": "AntSeed Improvement Proposals (AIPs) describe standards and processes",
      "reviewNotes": "Standards reference, not executable implementation."
    },
    {
      "repository": "Humanive/cogfree",
      "githubRepositoryId": 1403010415,
      "path": "README.md",
      "blobSha": "f3c13842c45552c60dfbb6ab9141341f5c504c00",
      "advisoryDomains": [
        "productivity"
      ],
      "taskTerms": [
        "skills",
        "cognition",
        "thinking",
        "memory",
        "planning"
      ],
      "evidenceSnippet": "28 lightweight cognitive skills",
      "reviewNotes": "Reference skills must be reviewed before adoption."
    },
    {
      "repository": "liseami/CCBaga",
      "githubRepositoryId": 1413898431,
      "path": "README.md",
      "blobSha": "578108a49206b3de64e9ad98306648bae3e4137a",
      "advisoryDomains": [
        "productivity"
      ],
      "taskTerms": [
        "workspace",
        "desktop",
        "system",
        "settings"
      ],
      "evidenceSnippet": "native macOS, Linux and Windows toolkit",
      "reviewNotes": "Host settings and browser identity changes require explicit review."
    },
    {
      "repository": "Xittered/xitter",
      "githubRepositoryId": 1418075921,
      "path": "README.md",
      "blobSha": "f4e05f39279a645656359b88f4702e1d3c97e01c",
      "advisoryDomains": [
        "backend"
      ],
      "taskTerms": [
        "backend",
        "postgres",
        "social",
        "api",
        "server"
      ],
      "evidenceSnippet": "A self-hosted backend for the X (Twitter) web client.",
      "reviewNotes": "Legal constraints for obtaining the original client must be reviewed."
    },
    {
      "repository": "anishfn/shapeshift",
      "githubRepositoryId": 1381152958,
      "path": "README.md",
      "blobSha": "ae51f52b94bf9c846a4b2946b3b9cc072f98eae6",
      "advisoryDomains": [
        "web_frontend",
        "productivity"
      ],
      "taskTerms": [
        "ui",
        "interface",
        "forms",
        "input",
        "text"
      ],
      "evidenceSnippet": "One text box that morphs into the right UI as you type",
      "reviewNotes": "UI demo may require model or runtime components."
    },
    {
      "repository": "mexicat/pdoom-video",
      "githubRepositoryId": 1386391454,
      "path": "README.md",
      "blobSha": "b7de7037ebb1d366099dffabb13086fbf6989c8c",
      "advisoryDomains": [
        "ai_media"
      ],
      "taskTerms": [
        "music",
        "video",
        "render",
        "audio",
        "lyrics",
        "typography"
      ],
      "evidenceSnippet": "A generative, code-rendered music video",
      "reviewNotes": "Music rights are separate from the code."
    },
    {
      "repository": "charlesbel/Microsoft-Rewards-Farmer",
      "githubRepositoryId": 282502417,
      "path": "README.md",
      "blobSha": "960d44b097e56c88e4071fd6674262124398af10",
      "advisoryDomains": [
        "productivity"
      ],
      "taskTerms": [
        "browser",
        "automation",
        "rewards",
        "selenium"
      ],
      "evidenceSnippet": "A simple bot that uses selenium to farm Microsoft Rewards",
      "reviewNotes": "README warns Microsoft may ban accounts; no autonomous account actions."
    }
  ]
}
````

## File: catalog.schema.json
````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List Catalog",
  "type": "object",
  "required": [
    "schemaVersion",
    "repositories"
  ],
  "properties": {
    "schemaVersion": {
      "type": "integer",
      "const": 1
    },
    "generatedFrom": {
      "type": "string"
    },
    "selectionPolicy": {
      "type": "object"
    },
    "repositories": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repo",
          "score",
          "tier",
          "category"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "pattern": "^[^/]+/[^/]+$"
          },
          "score": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
          },
          "tier": {
            "enum": [
              "core",
              "recommended",
              "specialized",
              "indexed"
            ]
          },
          "category": {
            "type": "string",
            "minLength": 1
          },
          "domain": {
            "type": "string",
            "enum": [
              "ai_agents",
              "ai_memory",
              "ai_media",
              "software_engineering",
              "web_frontend",
              "backend",
              "mobile",
              "graphics",
              "game_dev",
              "trading",
              "cybersecurity",
              "data_ml",
              "devops",
              "productivity",
              "other"
            ]
          },
          "roles": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "agentSuitability": {
            "enum": [
              "high",
              "medium-high",
              "medium",
              "low"
            ]
          },
          "capabilities": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "alternatives": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "complements": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "bestFor": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "avoidWhen": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "languages": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "platforms": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "selfHosted": {
            "anyOf": [
              {
                "type": "boolean"
              },
              {
                "type": "string",
                "enum": [
                  "partial",
                  "unknown"
                ]
              }
            ]
          },
          "runtime": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "uniqueItems": true
          },
          "resourceLevel": {
            "enum": [
              "low",
              "medium",
              "high"
            ]
          },
          "integrationComplexity": {
            "enum": [
              "low",
              "medium",
              "high"
            ]
          },
          "costModel": {
            "enum": [
              "open-source",
              "mixed",
              "paid",
              "unknown"
            ]
          },
          "github": {
            "type": "object",
            "required": [
              "stars",
              "forks",
              "openIssues",
              "archived",
              "disabled",
              "defaultBranch",
              "license",
              "pushedAt"
            ],
            "properties": {
              "stars": {
                "type": "integer",
                "minimum": 0
              },
              "forks": {
                "type": "integer",
                "minimum": 0
              },
              "openIssues": {
                "type": "integer",
                "minimum": 0
              },
              "archived": {
                "type": "boolean"
              },
              "disabled": {
                "type": "boolean"
              },
              "defaultBranch": {
                "type": "string",
                "minLength": 1
              },
              "license": {
                "anyOf": [
                  {
                    "type": "string"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "pushedAt": {
                "anyOf": [
                  {
                    "type": "string"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            },
            "additionalProperties": false
          },
          "lifecycle": {
            "enum": [
              "active",
              "stable",
              "reference",
              "legacy"
            ]
          },
          "guidanceSource": {
            "enum": [
              "curated",
              "inferred"
            ]
          },
          "licenseEvidence": {
            "enum": [
              "verified-file",
              "no-root-license-file"
            ]
          },
          "licenseStatus": {
            "enum": [
              "not-found",
              "custom-restrictive",
              "partial",
              "external-terms"
            ]
          },
          "githubRepositoryId": {
            "type": "integer",
            "minimum": 1
          }
        },
        "additionalProperties": false
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "githubRefreshedAt": {
          "type": "string",
          "minLength": 1
        },
        "githubRefreshFailures": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "repo",
              "error"
            ],
            "properties": {
              "repo": {
                "type": "string",
                "pattern": "^[^/]+/[^/]+$"
              },
              "error": {
                "type": "string",
                "minLength": 1
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
````

## File: README.md
````markdown
# star-list

`star-list` is a curated repository catalog plus a small Python toolchain for selecting projects for a task, monitoring catalog health, finding coverage gaps, discovering candidates, and reviewing changes before they enter the catalog.

The repository is intentionally data-first: `catalog.json` is the source catalog, `catalog.schema.json` defines its structure, and the scripts under [`scripts/`](scripts/) validate, rank, analyze, refresh, and review that data.

Current stable release: **1.0.0**. See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## What it does

- validates the catalog and its metadata;
- recommends repositories for a natural-language task with technical constraints;
- scores repository health and tracks trends over time;
- detects weak catalog coverage and searches GitHub for candidates;
- evaluates candidates as `accept`, `review`, or `reject` without adding them automatically;
- remembers unchanged review/reject candidates to reduce repeated noise;
- validates generated JSON against contracts in [`schemas/`](schemas/);
- opens or updates GitHub issues for discovery, cache health, and repository health review.

## Requirements

The local toolchain targets **Python 3.12** and uses the Python standard library. No package installation is required for the validation, recommendation, scoring, or offline integration tests.

Clone the repository and run commands from its root directory.

## Quick start

Validate the catalog:

```bash
python scripts/validate_catalog.py
```

Find repositories for a task:

```bash
python scripts/recommend.py "xauusd backtesting risk execution" --top 8
python scripts/recommend.py "local coding agent" --self-hosted --max-complexity medium
python scripts/recommend.py "python trading backtest" --language python --cap backtesting --json
```

Run the end-to-end pipeline test without network access:

```bash
python scripts/test_pipeline_integration.py
```

For all recommender flags and examples, see [`RECOMMENDER.md`](RECOMMENDER.md).

## Website resources (in addition to GitHub repositories)

The catalog also includes **34 curated web resources** for UI design,
animation, browser 3D, shaders, game-art direction, optional PINOC MCP motion tools,
AI game prototyping, NPC/voice platforms, licensed downloadable 3D assets,
narrative design, gameplay QA, reference-to-video/audio model collections,
quantized image-generation checkpoints, Hugging Face discovery and vision-language
models. Explore them
in [`WEB_RESOURCES.md`](WEB_RESOURCES.md) or use the structured
[`websites.json`](websites.json) directory. They are **not** GitHub
repositories and are never passed to Production-OS as code dependencies.

```bash
python scripts/recommend.py "3d scroll animation website" --websites --json
python scripts/recommend.py "3d character mocap blender" --websites --json
python scripts/validate_json_contract.py schemas/websites.schema.json websites.json
```

The optional website ranking preserves the original repository rankings and
reports licensing/usage cautions separately; do not treat paid design assets
or third-party shaders as open source.

## Exhaustive project-level resource audit

Every active, accessible project receives a **decision for each catalogued
GitHub source and each curated website** in the daily portfolio artifact:
matched / not relevant / requiring review, with per-source reasons. Summary
counters verify total coverage, rather than only counting suggested matches.
See [website and catalog scan documentation](WEB_RESOURCES.md). Review-only
sources are never installed automatically; runtime changes still need a
verified licence, compatible target and independently passing CI.

## Priority agent skills from Skill Issue

The [Skill Issue](https://skill-issue.in/) directory provides reusable agent-skill
references for software work. A curated, **review-only** shortlist of
upstream source repositories is tracked in
[`agent-skills.json`](agent-skills.json), with a matching CLI in
[`scripts/agent_skill_discovery.py`](scripts/agent_skill_discovery.py).

```bash
python scripts/agent_skill_discovery.py "react frontend performance" --domain web_frontend --language TypeScript --json
python scripts/recommend.py "mobile ui design" --skills --websites --json
```

The daily public and private repository scanners include the Skill Issue
directory for **every accessible project** and suggest only relevant skills
based on repository labels, domains, language and narrowly recognized
root React/Flutter dependencies. Pinned Flutter, Godot, Android and Roblox SKILL.md references
are also available for compatible projects. No third-party skill is
automatically downloaded, installed, granted credentials or dispatched. Read
[`AGENT_SKILLS.md`](AGENT_SKILLS.md) for the adoption and security gates.

## Verified pinned Skill Issue source links

Skill Issue and its curated agent-skill source references are documented in
[`AGENT_SKILLS.md`](AGENT_SKILLS.md). A daily read-only
[source metadata audit](.github/workflows/audit-agent-skill-sources.yml)
rechecks exact revision-pinned `SKILL.md` files, reports missing links,
and preserves failed-scan evidence. It never imports or executes the remote
instructions. A valid link is not proof that a skill is safe or licensed for
unattended use.

## Automatic GitHub Stars synchronization

A free, hourly GitHub Actions workflow checks **dbrckk**'s publicly accessible starred
repositories and **adds every missing public Star to `catalog.json`** after
canonical identity and metadata checks. Entries are tagged `audit` until an
independent quality, license and security review; this is inclusion, not
endorsement. It produces a complete sync report, import manifest, and admission
report as short-lived workflow artifacts. No external service or paid token is required.

The reviewed-metadata importer below remains available to promote and enrich
entries after their initial admission.

Run manually from **Actions → Sync GitHub Stars → Run workflow**, or locally:

```bash
python scripts/sync_github_stars.py --user dbrckk --report-json star-sync-report.json --report-md star-sync-review.md --manifest star-sync-manifest.json
```

See [synchronization operations and limitations](docs/GITHUB_STARS_SYNC.md).

## Import GitHub Star screenshots

Screenshot-derived repository names are stored as immutable import manifests. The importer is
**read-only by default**: it reports known repositories, duplicates, and entries requiring
review without changing the curated catalog.

```bash
python scripts/star_import_pipeline.py imports/github-stars-2026-10-09-batch-2.json \
  --report-json star-import-report.json
```

Raw metadata snapshots alone are **not sufficient** for admission. To approve a new entry,
create a separate reviewed metadata file with this structure:

```json
{
  "repositories": [
    {
      "repo": "owner/repository",
      "reviewed": true,
      "github": { "...": "verified GitHub metadata fields" },
      "catalogEntry": {
        "repo": "owner/repository",
        "...": "all required catalog fields",
        "github": { "...": "same verified GitHub metadata fields" }
      }
    }
  ]
}
```

The `github` objects must match exactly. In actual files, replace the illustrative
`...` fields with complete objects conforming to `catalog.schema.json`.
Only set `reviewed: true` after verifying repository identity, licensing, and classification.
The script does not independently authenticate the reviewer.

```bash
python scripts/star_import_pipeline.py imports/github-stars-2026-10-09-batch-2.json \
  --metadata path/to/reviewed-metadata.json \
  --report-json star-import-report.json --write
```

The write path reuses the existing catalog validators and is atomic. Bad metadata or
an unapproved batch cannot silently create catalog entries. Candidates still requiring
review remain outside the catalog; rerunning an already admitted batch is idempotent.
The metadata files from prior imports are historical evidence, not automatic approval.

## Repository layout

| Path | Purpose |
| --- | --- |
| `VERSION` | Current stable semantic version. |
| `CHANGELOG.md` | Stable release notes. |
| `catalog.json` | Curated repository catalog. |
| `catalog.schema.json` | Main catalog schema. |
| `stacks.json` | Predefined repository stacks used by the recommender. |
| `history.json` | Compact repository trend history. |
| `health-snapshot.json` | Last persisted health snapshot. |
| `discovery-cache.json` | Persistent GitHub discovery response cache. |
| `discovery-memory.json` | Fingerprints used to suppress unchanged review/reject candidates. |
| `cache-health-history.json` | Discovery-cache health history. |
| [`scripts/`](scripts/) | Validation, recommendation, health, discovery, rendering, and tests. |
| [`schemas/`](schemas/) | JSON contracts for generated and persistent pipeline outputs. |
| [`.github/workflows/validate.yml`](.github/workflows/validate.yml) | CI validation pipeline. |
| [`.github/workflows/refresh-metadata.yml`](.github/workflows/refresh-metadata.yml) | Scheduled metadata/discovery/health workflow. |

## Pipeline architecture

The discovery path is:

```text
catalog.json
   |
   v
analyze_coverage.py
   |
   v
build_discovery_watchlist.py
   |
   v
discover_candidates.py  <--> discovery-cache.json
   |
   v
evaluate_candidates.py
   |
   v
filter_discovery_memory.py <--> discovery-memory.json
   |
   v
render_discovery_issue.py
   |
   v
GitHub discovery review issue
```

The important separation is deliberate:

1. **Coverage** decides what the catalog is missing.
2. **Discovery** searches for repositories that may fill those gaps.
3. **Evaluation** applies activity, fit, adoption, maturity, and maintenance signals.
4. **Memory** suppresses unchanged non-accepted candidates on later runs.
5. **Rendering** produces review material; candidates are never inserted into `catalog.json` automatically.

The detailed candidate scoring and confidence model is documented in [`docs/DISCOVERY_SCORING.md`](docs/DISCOVERY_SCORING.md).

## Recommendation engine

`scripts/recommend.py` ranks existing catalog entries for a concrete task. Its **selection score** is task-specific and is distinct from both the catalog quality score and discovery candidate evaluation score.

It considers capability/domain/task matches, `bestFor`, catalog quality, tier, activity, repository health, trend history, and `avoidWhen` penalties. It can also enforce platform, language, self-hosting, resource, complexity, capability, archive, and minimum-score constraints.

See [`RECOMMENDER.md`](RECOMMENDER.md) for command examples and supported filters.

## Discovery scoring

Candidate admission uses two stages:

- `discoveryScore` is produced by GitHub discovery and represents search/discovery relevance and repository signals;
- `evaluationScore` starts from that value and applies deterministic admission adjustments.

The current admission thresholds are `accept >= 80`, `review >= 55`, otherwise `reject`. A candidate with `low` metadata confidence cannot be auto-accepted even if its numeric score reaches the accept threshold; it is capped at `review`.

See [`docs/DISCOVERY_SCORING.md`](docs/DISCOVERY_SCORING.md) for the exact adjustments, confidence signals, and diagnostic score breakdown.

## Validation and tests

The CI workflow compiles all Python utilities, validates the catalog, runs component tests, validates JSON contracts, executes the offline end-to-end discovery integration test, checks documentation consistency, and validates generated reports.

Useful local checks:

```bash
python -m compileall -q scripts
python scripts/validate_catalog.py
python scripts/test_recommend.py
python scripts/test_evaluate_candidates.py
python scripts/test_json_contracts.py
python scripts/test_pipeline_integration.py
python scripts/test_documentation.py
```

`python scripts/test_pipeline_integration.py` covers the complete offline chain `coverage -> watchlist -> discovery -> evaluation -> memory -> issue rendering` with deterministic mocked GitHub responses.

## Automated metadata refresh

The **Refresh GitHub metadata** workflow in [`.github/workflows/refresh-metadata.yml`](.github/workflows/refresh-metadata.yml) runs every Monday at `04:17 UTC` and can also be started with `workflow_dispatch`.

It refreshes repository metadata, validates the catalog, updates health/history state, runs discovery, validates every pipeline JSON contract, analyzes cache health, maintains review issues, and commits changed persistent state back to the repository.

The workflow writes or maintains these persistent files:

```text
catalog.json
health-snapshot.json
history.json
discovery-cache.json
discovery-memory.json
cache-health-history.json
```

GitHub API access is supplied by the workflow's `GITHUB_TOKEN`; local recommendation and offline tests do not require a token.

## JSON contracts

Generated pipeline outputs are checked against the contracts under [`schemas/`](schemas/) using `scripts/validate_json_contract.py`. The validator implements the JSON Schema keywords currently used by this repository; it is intentionally a focused validator rather than a general-purpose implementation of every JSON Schema 2020-12 keyword.

Example:

```bash
python scripts/validate_json_contract.py schemas/discovery-evaluated.schema.json discovery-evaluated.json
```

## Safety model for catalog changes

General-purpose GitHub discovery remains advisory and never inserts external candidates. A distinct GitHub Stars workflow automatically admits repositories explicitly starred by `dbrckk`, conservatively at `audit` tier. Human review remains required before promotion to a recommended tier.
````

## File: stacks.json
````json
{
  "schemaVersion": 1,
  "stacks": [
    {
      "name": "AI Dev Server",
      "domain": "ai_agents",
      "goal": "Autonomous software development with memory, observability, browser testing and model routing.",
      "repos": [
        "anomalyco/opencode",
        "BerriAI/litellm",
        "mem0ai/mem0",
        "langfuse/langfuse",
        "microsoft/playwright",
        "firecrawl/firecrawl",
        "e2b-dev/E2B"
      ],
      "notes": [
        "Use OpenHands as an alternative autonomous coding engine.",
        "Use qdrant/qdrant when vector retrieval becomes a first-class requirement."
      ]
    },
    {
      "name": "XAUUSD Research",
      "domain": "trading",
      "goal": "Robust Gold/USD research from data ingestion to backtest, ML, risk and execution.",
      "repos": [
        "openbq-org/OpenBB",
        "microsoft/qlib",
        "dmlc/xgboost",
        "shap/shap",
        "optuna/optuna",
        "polakowo/vectorbt",
        "dcajasn/Riskfolio-Lib",
        "QuantConnect/Lean",
        "nautechsystems/nautilus_trader",
        "ranaroussi/quantstats"
      ],
      "notes": [
        "Prefer out-of-sample profit robustness over win rate.",
        "Model spread, slippage and session/macro regimes explicitly."
      ]
    },
    {
      "name": "Vector Animation Android",
      "domain": "graphics",
      "goal": "Create and deploy high-quality vector animation on Android.",
      "repos": [
        "motion-canvas/motion-canvas",
        "airbnb/lottie-android",
        "EsotericSoftware/spine-runtimes",
        "google/filament"
      ],
      "notes": [
        "Use Lottie for lightweight playback.",
        "Use Spine or Rive-style runtimes for richer interactive animation."
      ]
    },
    {
      "name": "Full-stack Web App",
      "domain": "web_frontend",
      "goal": "Modern full-stack product with strong UI, API, data and test coverage.",
      "repos": [
        "vercel/next.js",
        "shadcn-ui/ui",
        "tailwindlabs/tailwindcss",
        "supabase/supabase",
        "postgres/postgres",
        "microsoft/playwright",
        "GoogleChrome/lighthouse"
      ],
      "notes": [
        "Swap Supabase for FastAPI + Postgres when backend control matters more than speed."
      ]
    },
    {
      "name": "Android Product",
      "domain": "mobile",
      "goal": "Production Android app with modern UI, backend integration and testing.",
      "repos": [
        "android/nowinandroid",
        "JetBrains/compose-multiplatform",
        "firebase/flutterfire",
        "appium/appium"
      ],
      "notes": [
        "Use React Native/Expo or Flutter instead when cross-platform speed matters more than native architecture."
      ]
    },
    {
      "name": "Game Production",
      "domain": "game_dev",
      "goal": "Cross-platform game with rendering, backend and ecosystem tooling.",
      "repos": [
        "godotengine/godot",
        "google/filament",
        "heroiclabs/nakama",
        "Calinou/awesome-godot"
      ],
      "notes": [
        "For Java ecosystems, libgdx/libgdx is the main alternative."
      ]
    },
    {
      "name": "Roblox Studio Agent Production",
      "domain": "game_dev",
      "goal": "Build and polish Roblox Studio gameplay with Luau coding agents, iterative playtesting, animation and performance diagnostics.",
      "repos": [
        "TabooHarmony/roblox-brain",
        "Chrrxs/robloxstudio-mcp",
        "S4US/Roqer"
      ],
      "notes": [
        "Roblox Studio authoring and instrumented playtests require a supported desktop environment; an Android phone alone cannot run Studio.",
        "Treat third-party agent actions as untrusted until scripts, assets, permissions and game behavior are reviewed.",
        "Roqer is AGPL-3.0; assess deployment and redistribution obligations before integration.",
        "Prefer built-in Roblox Studio MCP when available; this stack documents an alternative tested-tooling option, not an official dependency."
      ]
    },
    {
      "name": "Godot Gameplay and VFX",
      "domain": "game_dev",
      "goal": "Create Godot games with engine-supported gameplay, shaders, visual effects and agent-assisted GDScript iteration.",
      "repos": [
        "godotengine/godot",
        "godotengine/godot-demo-projects",
        "Coding-Solo/godot-mcp"
      ],
      "notes": [
        "Use demo project shader examples as references, not as finished studio-quality scenes; verify each game's rendering in engine.",
        "Review source, compatibility and privileges of external Godot MCP extensions before connecting them to a production project.",
        "Engine-level development requires desktop tooling; running a finished Android export is a different workflow."
      ]
    },
    {
      "name": "Authorized Security Validation",
      "domain": "cybersecurity",
      "goal": "Defensive validation and authorized security assessment workflows.",
      "repos": [
        "redcanaryco/atomic-red-team",
        "semgrep/semgrep",
        "github/codeql",
        "danielmiessler/SecLists"
      ],
      "notes": [
        "Use only in authorized environments and keep scope controls fail-closed."
      ]
    }
  ]
}
````

## File: websites.json
````json
{
  "schemaVersion": 1,
  "description": "Curated web resources complementing, but not replacing, the GitHub repository catalog.",
  "websites": [
    {
      "id": "scrolltide",
      "name": "Scrolltide",
      "url": "https://www.scrolltide.co/",
      "type": "prompt-template-library",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "scroll",
        "animation",
        "3d",
        "react",
        "prompt",
        "templates",
        "webgl"
      ],
      "bestFor": [
        "3D landing page prompts",
        "scroll-driven websites",
        "React animation inspiration"
      ],
      "reuse": "licensed-material",
      "caution": "Paid template and prompt access is subject to the provider's terms; a few free examples do not make the whole library open source."
    },
    {
      "id": "awwwards",
      "name": "Awwwards",
      "url": "https://www.awwwards.com/",
      "type": "inspiration-gallery",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "web",
        "design",
        "award",
        "inspiration",
        "typography",
        "3d",
        "animation"
      ],
      "bestFor": [
        "award-winning website references",
        "visual design benchmarking",
        "creative web design"
      ],
      "reuse": "reference-only",
      "caution": "Showcased websites and their images/source are third-party creations, not reusable code by default."
    },
    {
      "id": "recent-design",
      "name": "Recent (formerly Godly)",
      "url": "https://recent.design/",
      "originalUrl": "https://godly.website/",
      "type": "inspiration-gallery",
      "access": "free",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "web",
        "ui",
        "design",
        "inspiration",
        "branding",
        "motion",
        "3d"
      ],
      "bestFor": [
        "curated website references",
        "modern UI and branding inspiration",
        "motion and 3D design examples"
      ],
      "reuse": "reference-only",
      "caution": "The source domain redirects to Recent; examples are references, not assets licensed for copying."
    },
    {
      "id": "60fps",
      "name": "60fps",
      "url": "https://60fps.design/",
      "type": "motion-gallery",
      "access": "freemium",
      "domains": [
        "mobile",
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "ui",
        "ux",
        "motion",
        "animation",
        "microinteraction",
        "mobile",
        "web"
      ],
      "bestFor": [
        "mobile UI animations",
        "interaction and motion references",
        "micro-interaction design"
      ],
      "reuse": "reference-only",
      "caution": "Animation recordings and examples are references; verify rights before copying assets."
    },
    {
      "id": "21st-dev",
      "name": "21st.dev",
      "url": "https://21st.dev/",
      "type": "component-marketplace",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "react",
        "ui",
        "components",
        "tailwind",
        "shadcn",
        "templates",
        "mcp"
      ],
      "bestFor": [
        "discovering React UI components",
        "reusable interface patterns",
        "Tailwind and shadcn component discovery"
      ],
      "reuse": "license-per-item",
      "caution": "Creators retain rights to their components; verify each item's license and free-tier limits before integration."
    },
    {
      "id": "aceternity-ui",
      "name": "Aceternity UI",
      "url": "https://ui.aceternity.com/",
      "type": "component-library",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "react",
        "tailwind",
        "ui",
        "components",
        "animation",
        "3d"
      ],
      "bestFor": [
        "animated React interfaces",
        "high-impact landing page components",
        "3D web UI effects"
      ],
      "reuse": "license-per-item",
      "caution": "Aceternity and third-party items have license restrictions, especially redistribution of components or templates."
    },
    {
      "id": "magic-ui",
      "name": "Magic UI",
      "url": "https://magicui.design/",
      "type": "component-library",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "react",
        "tailwind",
        "ui",
        "components",
        "animated",
        "landing",
        "motion"
      ],
      "bestFor": [
        "animated landing pages",
        "React UI component inspiration",
        "interactive marketing interfaces"
      ],
      "reuse": "license-per-item",
      "caution": "Check the license of the specific component and any paid templates before copying or redistributing."
    },
    {
      "id": "threejs",
      "name": "Three.js",
      "url": "https://threejs.org/",
      "type": "framework-docs",
      "access": "free",
      "domains": [
        "web_frontend",
        "graphics"
      ],
      "tags": [
        "3d",
        "webgl",
        "webgpu",
        "javascript",
        "graphics",
        "animation",
        "shader"
      ],
      "bestFor": [
        "browser 3D rendering",
        "WebGL and WebGPU animation",
        "interactive JavaScript scenes"
      ],
      "reuse": "open-source-upstream",
      "caution": "The core library is open source; third-party demos, models and textures may have separate licenses."
    },
    {
      "id": "shadertoy",
      "name": "Shadertoy",
      "url": "https://www.shadertoy.com/",
      "type": "shader-gallery",
      "access": "free",
      "domains": [
        "graphics",
        "web_frontend",
        "game_dev"
      ],
      "tags": [
        "shader",
        "glsl",
        "3d",
        "vfx",
        "graphics",
        "procedural",
        "webgl"
      ],
      "bestFor": [
        "GLSL shader inspiration",
        "visual effects experiments",
        "procedural graphics"
      ],
      "reuse": "license-per-item",
      "caution": "Individual shaders have creator-specific rights, potentially non-commercial, and may not be production-performant."
    },
    {
      "id": "lovable",
      "name": "Lovable",
      "url": "https://lovable.dev/",
      "type": "hosted-builder",
      "access": "freemium",
      "domains": [
        "web_frontend",
        "software_engineering"
      ],
      "tags": [
        "ai",
        "web",
        "app",
        "website",
        "builder",
        "react",
        "prototype"
      ],
      "bestFor": [
        "rapid web app prototypes",
        "prompt-to-website iteration",
        "interactive app mockups"
      ],
      "reuse": "hosted-service",
      "caution": "A hosted creation service is not a drop-in code dependency. Review plans, generated code, data access and export terms."
    },
    {
      "id": "skill-issue",
      "name": "Skill Issue",
      "url": "https://skill-issue.in/",
      "type": "agent-skills-directory",
      "access": "free",
      "domains": [
        "ai_agents",
        "software_engineering",
        "web_frontend",
        "mobile",
        "game_dev",
        "graphics",
        "ai_media",
        "other"
      ],
      "tags": [
        "agent",
        "skills",
        "design",
        "frontend",
        "backend",
        "game",
        "automation",
        "motion",
        "video",
        "research",
        "workflow",
        "tooling"
      ],
      "bestFor": [
        "Finding task-specific skills for coding agents across software projects",
        "Curating reusable agent workflows for design, web, mobile and game development",
        "Comparing upstream skill sources before human-reviewed installation"
      ],
      "reuse": "reference-only",
      "caution": "A directory listing is not proof that any linked SKILL.md, installer, prompt, source or license is safe. Review original repository, pinned revision, permissions, instructions and compatibility before using; never auto-run remote install commands."
    },
    {
      "id": "game-art-style",
      "name": "Game Art Style",
      "url": "https://gameartstyle.loopyhop.com/",
      "type": "inspiration-gallery",
      "access": "free",
      "domains": [
        "game_dev",
        "graphics",
        "mobile"
      ],
      "tags": [
        "game",
        "art",
        "style",
        "visual",
        "design",
        "art-direction",
        "pixel",
        "retro",
        "2d",
        "3d",
        "low-poly",
        "voxel",
        "painting",
        "cel-shading",
        "characters",
        "environments",
        "ui",
        "vfx"
      ],
      "bestFor": [
        "Comparing original game visual styles across pixel art, illustration and 3D",
        "Defining consistent art direction for characters, environments, UI, effects and animation",
        "Finding real-game visual references and art-direction prompt examples"
      ],
      "reuse": "reference-only",
      "caution": "Screenshots and reference images belong to their respective owners; this gallery does not license artwork for copying or redistribution. Use it to guide original art direction, and check rights before reusing any media."
    },
    {
      "id": "jupiter-game-art-style",
      "name": "Jupiter the Warlock — Game Art Style",
      "url": "https://jupiterthewarlock.com/gameartstyle/",
      "type": "inspiration-gallery",
      "access": "unknown",
      "domains": [
        "game_dev",
        "graphics",
        "mobile"
      ],
      "tags": [
        "game",
        "art",
        "style",
        "visual",
        "design",
        "art-direction",
        "pixel",
        "2d",
        "3d",
        "characters",
        "environments",
        "animation",
        "vfx"
      ],
      "bestFor": [
        "Evaluating visual art-direction references for game projects",
        "Finding inspiration for original characters, environments and effects"
      ],
      "reuse": "reference-only",
      "caution": "The linked page could not be independently fetched at admission time. Treat it as an unverified visual reference, not a licensed source of images, code or game assets. Review live availability and each creator's usage rights before using any content."
    },
    {
      "id": "viggle-pinoc-mcp",
      "name": "Viggle PINOC MCP",
      "url": "https://viggle.ai/pinoc/mcp",
      "originalUrl": "https://viggle.ai/pinoc/app/mcp",
      "mcpEndpoint": "https://pinoc.mcp.viggle.ai/mcp",
      "type": "mcp-service",
      "access": "freemium",
      "domains": [
        "game_dev",
        "graphics",
        "ai_media",
        "software_engineering"
      ],
      "tags": [
        "mcp",
        "game-animation",
        "3d",
        "character",
        "characters",
        "rigging",
        "rig",
        "mocap",
        "motion",
        "animation",
        "skeletal",
        "glb",
        "fbx",
        "blender",
        "unity",
        "unreal",
        "npc",
        "cutscene",
        "video-to-motion",
        "text-to-motion",
        "roblox"
      ],
      "bestFor": [
        "Finding and importing free preset 3D motion clips into compatible games and animation tools",
        "Agent-assisted motion capture from video and text-to-motion character animation",
        "Connecting reviewed MCP clients to rigged character and motion assets for Blender, Unity, Unreal and web 3D"
      ],
      "reuse": "hosted-service",
      "caution": "PINOC MCP requires interactive user login and authorization. Connect read-only first. Preset motion browsing and retrieval are free; generating characters or motion consumes credits (text/video motion 1 credit per second, character 6–10 credits). Never grant write/generate scopes or spend credits automatically; verify asset licenses, privacy and engine/rig compatibility."
    },
    {
      "id": "rosebud-ai",
      "name": "Rosebud AI",
      "url": "https://rosebud.ai/",
      "type": "hosted-builder",
      "access": "freemium",
      "domains": [
        "game_dev",
        "graphics",
        "web_frontend"
      ],
      "tags": [
        "game",
        "gameplay",
        "prototype",
        "prototyping",
        "browser",
        "2d",
        "3d",
        "interactive",
        "threejs",
        "webgl"
      ],
      "bestFor": [
        "Generating playable browser game prototypes",
        "Exploring game mechanics and rapid visual iterations"
      ],
      "reuse": "hosted-service",
      "portfolioBaselineDomains": [
        "game_dev"
      ],
      "caution": "Free game creation does not establish commercial-use rights: check plans and export terms. A hosted game generator is not a drop-in engine library; do not upload private code or auto-publish."
    },
    {
      "id": "convai",
      "name": "Convai",
      "url": "https://convai.com/",
      "type": "npc-platform",
      "access": "freemium",
      "domains": [
        "game_dev",
        "ai_agents",
        "ai_media"
      ],
      "tags": [
        "npc",
        "dialogue",
        "character",
        "voice",
        "conversational",
        "embodied",
        "unity",
        "unreal",
        "3d",
        "spatial"
      ],
      "bestFor": [
        "Evaluating context-aware real-time conversational NPCs",
        "Reviewing Unity, Unreal or web character SDK integrations"
      ],
      "reuse": "hosted-service",
      "caution": "Requires a hosted account and API configuration. Check engine compatibility, latency, privacy, commercial plans and SDK terms; do not grant keys or capture player audio automatically.",
      "portfolioRequiredSignals": [
        "npc",
        "dialogue",
        "character",
        "voice",
        "conversational",
        "rpg"
      ]
    },
    {
      "id": "inworld-ai",
      "name": "Inworld AI",
      "url": "https://inworld.ai/",
      "type": "npc-platform",
      "access": "freemium",
      "domains": [
        "game_dev",
        "ai_media",
        "ai_agents"
      ],
      "tags": [
        "npc",
        "dialogue",
        "voice",
        "speech",
        "tts",
        "stt",
        "realtime",
        "audio",
        "character",
        "inference"
      ],
      "bestFor": [
        "Evaluating real-time speech and game dialogue APIs",
        "Comparing voice infrastructure for interactive characters"
      ],
      "reuse": "hosted-service",
      "caution": "Current offerings emphasize low-latency speech and inference, not necessarily legacy NPC integrations. Verify supported engines, pricing, privacy and API terms before use.",
      "portfolioRequiredSignals": [
        "npc",
        "dialogue",
        "voice",
        "speech",
        "tts",
        "stt",
        "audio"
      ]
    },
    {
      "id": "ludo-ai",
      "name": "Ludo.ai",
      "url": "https://ludo.ai/",
      "type": "game-design-service",
      "access": "freemium",
      "domains": [
        "game_dev",
        "graphics",
        "ai_media"
      ],
      "tags": [
        "game",
        "gameplay",
        "game-design",
        "gdd",
        "ideation",
        "prototype",
        "prototyping",
        "sprites",
        "art",
        "3d",
        "assets",
        "planning"
      ],
      "bestFor": [
        "Brainstorming gameplay mechanics and retention loops",
        "Drafting game design documents and art direction",
        "Reviewing optional asset generation through CLI, MCP or API"
      ],
      "reuse": "hosted-service",
      "portfolioBaselineDomains": [
        "game_dev"
      ],
      "caution": "Hosted and credit-based: generation, CLI, REST API and MCP may require an account or consume credits. Check export/commercial rights; never install agents or spend credits automatically."
    },
    {
      "id": "sloyd-ai",
      "name": "Sloyd AI",
      "url": "https://sloyd.ai/",
      "type": "asset-generator",
      "access": "freemium",
      "domains": [
        "game_dev",
        "graphics",
        "ai_media"
      ],
      "tags": [
        "3d",
        "models",
        "mesh",
        "modeling",
        "props",
        "environment",
        "characters",
        "roblox",
        "blender",
        "unity",
        "low-poly",
        "glb",
        "game-assets"
      ],
      "bestFor": [
        "Exploring generated game-ready 3D meshes and props",
        "Reviewing topology, textures and polygon counts before asset import"
      ],
      "reuse": "hosted-service",
      "caution": "Generated assets are not automatically licensed or optimized for production. Check export formats, commercial terms, rig suitability and performance before importing into a game.",
      "portfolioRequiredSignals": [
        "3d",
        "model",
        "models",
        "mesh",
        "props",
        "roblox",
        "blender"
      ]
    },
    {
      "id": "charisma-ai",
      "name": "Charisma AI",
      "url": "https://charisma.ai/",
      "type": "narrative-platform",
      "access": "unknown",
      "domains": [
        "game_dev",
        "ai_agents",
        "ai_media"
      ],
      "tags": [
        "narrative",
        "dialogue",
        "story",
        "stories",
        "branching",
        "rpg",
        "npc",
        "character",
        "interactive",
        "unity",
        "unreal",
        "conversation"
      ],
      "bestFor": [
        "Designing branching interactive dialogue and plot triggers",
        "Reviewing character-driven narrative SDKs for Unity or Unreal"
      ],
      "reuse": "hosted-service",
      "caution": "Creation may require an account, trial licence or commercial agreement. SDKs and narrative workflows are not compatible with every engine; check pricing, privacy and rights.",
      "portfolioRequiredSignals": [
        "narrative",
        "dialogue",
        "story",
        "stories",
        "branching",
        "rpg",
        "npc",
        "quest",
        "cutscene"
      ]
    },
    {
      "id": "modl-ai",
      "name": "modl.ai",
      "url": "https://modl.ai/",
      "type": "game-testing-service",
      "access": "unknown",
      "domains": [
        "game_dev",
        "software_engineering"
      ],
      "tags": [
        "game",
        "gameplay",
        "qa",
        "testing",
        "playtesting",
        "bugs",
        "regression",
        "crash",
        "performance",
        "automation",
        "ci"
      ],
      "bestFor": [
        "Planning automated gameplay, exploratory and regression tests",
        "Evaluating AI agents that report crashes, softlocks and visual bugs"
      ],
      "reuse": "hosted-service",
      "portfolioBaselineDomains": [
        "game_dev"
      ],
      "caution": "Provider currently advertises build-upload testing without SDK integration; older docs describe Unity plugins. Check current platform support, costs, build privacy and test reproducibility before uploading."
    },
    {
      "id": "fasth3-omni-collection",
      "name": "FastVideo — FastH3 Omni (Hugging Face collection)",
      "url": "https://huggingface.co/collections/FastVideo/fasth3-omni",
      "type": "model-collection",
      "access": "free",
      "domains": [
        "ai_media",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "video",
        "video-generation",
        "image-to-video",
        "reference-to-video",
        "audio",
        "synchronized-audio",
        "diffusion",
        "generative",
        "multimodal",
        "animation",
        "cinematic",
        "comfyui",
        "fastvideo",
        "fasth3",
        "omni",
        "fp8",
        "int8",
        "nvfp4",
        "gpu"
      ],
      "bestFor": [
        "Evaluating prompt- and reference-conditioned video generation with synchronized audio for media workflows",
        "Comparing BF16, INT8, FP8 and NVFP4 model variants and compatible FastVideo or ComfyUI runtimes",
        "Researching storyboards, cutscenes and promotional clips before assessing compute, safety, quality and licensing"
      ],
      "reuse": "licensed-material",
      "portfolioRequiredSignals": [
        "video",
        "animation",
        "cinematic",
        "cutscene",
        "film",
        "movie",
        "montage",
        "trailer",
        "comfyui",
        "image-to-video",
        "reference-to-video"
      ],
      "caution": "This is a collection of third-party model weights, not an executable GitHub dependency or a free hosted inference API. FastH3 Omni weights reference the MiniMax-H3 Community License Agreement, which must be reviewed independently for commercial use and redistribution. Large checkpoint downloads, compatible GPU/VRAM, runtime and additional text encoder/video/audio VAE are required. Never automatically install, fetch large weights, generate media or upload user content; inspect individual model licences and costs."
    },
    {
      "id": "atomicchat-flux3-image-klein-gguf",
      "name": "AtomicChat — FLUX.3 Image Klein GGUF",
      "url": "https://huggingface.co/AtomicChat/FLUX-3-Image-Klein-GGUF",
      "type": "model-checkpoint",
      "access": "unknown",
      "domains": [
        "ai_media",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "text-to-image",
        "image-editing",
        "image-generation",
        "quantized",
        "gguf",
        "flux-3",
        "image",
        "images",
        "graphics",
        "textures",
        "asset",
        "assets",
        "photo",
        "visual",
        "diffusion",
        "comfyui",
        "stable-diffusion.cpp",
        "offline",
        "gpu"
      ],
      "bestFor": [
        "Reviewing quantized FLUX.3 Image Klein transformer checkpoints for local image generation or reference-guided editing",
        "Assessing graphics, illustration, thumbnail, sprite and texture production workflows after checking compatible loaders and quality",
        "Comparing GGUF-specific memory and runtime trade-offs before deploying media tools"
      ],
      "reuse": "licensed-material",
      "portfolioRequiredSignals": [
        "image",
        "images",
        "imagegen",
        "img2img",
        "photo",
        "photos",
        "photography",
        "graphics",
        "graphic",
        "visual",
        "visuals",
        "artwork",
        "illustration",
        "illustrations",
        "sprite",
        "sprites",
        "texture",
        "textures",
        "asset",
        "assets",
        "thumbnail",
        "thumbnails",
        "poster",
        "posters",
        "flux",
        "gguf",
        "diffusion",
        "comfyui",
        "portrait",
        "rendering"
      ],
      "sourceLicenseTag": "other",
      "upstreamModel": "black-forest-labs/flux-3-image-klein",
      "caution": "AtomicChat currently labels this Hugging Face GGUF quantization as license:other (not an automatically approved licence). Upstream FLUX.3 Image Klein uses the FLUX Kommunity License, which restricts commercial and redistribution uses unless its specific conditions are met; verify both upstream and converted-weight rights. GGUF is a transformer checkpoint, not a complete image-generation service: compatible loader, separately licensed Qwen3-VL text encoder, VAE and sufficient CPU/GPU memory may be required. GGUF quantizations and stable-diffusion.cpp loaders are not interchangeable with every Diffusers or ComfyUI build. Never auto-download weights, assume Android-local feasibility, run inference, or use outputs commercially without independent review."
    },
    {
      "id": "hugging-face-hub",
      "name": "Hugging Face — Model, Dataset and Space Hub",
      "url": "https://huggingface.co/",
      "type": "model-hub",
      "access": "freemium",
      "domains": [
        "ai_agents",
        "ai_media",
        "graphics",
        "game_dev",
        "mobile",
        "software_engineering"
      ],
      "tags": [
        "huggingface",
        "hugging-face",
        "hf",
        "model",
        "models",
        "multimodal",
        "machine-learning",
        "vision",
        "ocr",
        "video",
        "audio",
        "image",
        "generation",
        "dataset",
        "datasets",
        "spaces",
        "inference",
        "transformers",
        "diffusers",
        "model-discovery",
        "model-comparison"
      ],
      "bestFor": [
        "Discovering and comparing AI models, datasets, applications and demo Spaces for supported project capabilities",
        "Checking each model's model card, license, lineage, benchmark evidence and required inference hardware before considering adoption",
        "Exploring hosted inference providers and free public resources separately from usage-based GPU and paid endpoints"
      ],
      "reuse": "reference-only",
      "portfolioBaselineDomains": [
        "ai_agents",
        "ai_media"
      ],
      "caution": "Hugging Face is a catalog and hosted community platform, not a single uniformly licensed model or an unlimited free inference endpoint. A public page or open model card does not grant every model's commercial rights. Review each selected repository's exact license, usage restrictions, model quality, token access, provider billing and deployment constraints before use. Do not auto-download checkpoints, run untrusted Spaces, spend credits or upload private files."
    },
    {
      "id": "minicpm-v-4-7-1b-heretic",
      "name": "MiniCPM-V 4.7 1B Heretic — vision-language checkpoint",
      "url": "https://huggingface.co/saidutta69/MiniCPM-V-4.7-1B-heretic",
      "type": "model-checkpoint",
      "access": "free",
      "domains": [
        "ai_media",
        "ai_agents",
        "graphics",
        "mobile",
        "software_engineering"
      ],
      "tags": [
        "vision-language",
        "vlm",
        "minicpm",
        "minicpm-v",
        "multimodal",
        "image-understanding",
        "image-text-to-text",
        "ocr",
        "document",
        "documents",
        "screenshot",
        "screenshots",
        "visual-question-answering",
        "captioning",
        "image-analysis",
        "video-understanding",
        "on-device",
        "gguf",
        "llama.cpp",
        "transformers",
        "vision-projector",
        "heretic",
        "abliterated"
      ],
      "bestFor": [
        "Reviewing local multimodal visual comprehension, OCR and screenshot or document analysis on supported devices",
        "Comparing image question answering, video frame interpretation and visual-agent reasoning with the base MiniCPM-V 4.7 model",
        "Evaluating on-device deployment costs and quality with compatible transformers or llama.cpp multimodal model plus the separate GGUF vision projector"
      ],
      "reuse": "licensed-material",
      "portfolioRequiredSignals": [
        "ocr",
        "vision",
        "vlm",
        "multimodal",
        "screenshot",
        "screenshots",
        "document",
        "documents",
        "captioning",
        "caption",
        "recognition",
        "visual-question-answering",
        "image-analysis",
        "video-analysis",
        "image-understanding",
        "video-understanding",
        "image-to-text",
        "scene-understanding",
        "scene-analysis",
        "image-captioning"
      ],
      "sourceLicenseTag": "apache-2.0",
      "upstreamModel": "openbmb/MiniCPM-V-4.7-1B",
      "safetyRisk": "reduced-refusal",
      "caution": "Community-edited 'heretic' / abliterated variant deliberately suppresses refusal behavior and ships without an additional safety layer. Do not deploy it to unmoderated public-facing or user-content endpoints: use human review, abuse prevention and data controls. The Hugging Face card lists Apache-2.0 inherited from the base, but reports no LICENSE file in either model repository; verify actual licensing and attribution before distribution. Approximately 1.55B parameters total (about 1.01B language plus 0.55B vision). Vision-enabled GGUF requires the separate ~1.11GB mmproj file in addition to compatible main weights and llama.cpp runtime. Neither standalone model nor on-device feasibility is proven by this catalog entry. No automatic weight downloads or inference."
    },
    {
      "id": "sopilot",
      "name": "SoPilot — AI Social Media and SEO Growth",
      "url": "https://sopilot.net/",
      "type": "marketing-automation-service",
      "access": "freemium",
      "domains": [
        "marketing"
      ],
      "tags": [
        "marketing",
        "social",
        "social-media",
        "social-media-marketing",
        "x-marketing",
        "twitter-marketing",
        "creator-growth",
        "audience-growth",
        "promotion",
        "promotional",
        "growth",
        "outreach",
        "seo",
        "backlinks",
        "campaign",
        "campaigns",
        "distribution",
        "product-launch",
        "marketing-content",
        "content-calendar",
        "content-marketing",
        "scheduling",
        "short-form-video",
        "brand-marketing",
        "lead-generation",
        "xrank"
      ],
      "bestFor": [
        "Researching rising topics and creator benchmarks on X for a product launch or creator growth campaign",
        "Planning original social posts, repeatable content columns and short kinetic promotional videos",
        "Evaluating opt-in SEO directory submissions and marketing automation after privacy, platform-policy, quality and pricing checks"
      ],
      "reuse": "hosted-service",
      "portfolioRequiredSignals": [
        "marketing",
        "social",
        "social-media",
        "seo",
        "backlink",
        "backlinks",
        "outreach",
        "campaign",
        "campaigns",
        "creator",
        "audience",
        "growth",
        "distribution",
        "product-launch",
        "x-marketing",
        "content-marketing",
        "promotion",
        "promotional",
        "lead-generation",
        "brand-marketing"
      ],
      "caution": "Commercial hosted service with account/Chrome extension, subscriptions or credit limits; it is not an open-source repository, local inference backend or free unlimited marketing API. AI-generated X replies, follows, reposting and bulk directory submissions may violate platform rules, appear as spam or harm SEO; never auto-install browser extensions, connect social accounts, publish, bulk-comment/follow, submit backlinks, pay or disclose private projects without explicit per-action approval. Check current X/platform policy, consent, account permissions and content originality."
    },
    {
      "id": "jialinyyzz-humanizer-12b",
      "name": "Humanizer 12B — local factual draft rewriting",
      "url": "https://huggingface.co/jialinyyzz/humanizer",
      "type": "model-checkpoint",
      "access": "free",
      "domains": [
        "writing",
        "marketing",
        "ai_agents"
      ],
      "tags": [
        "humanizer",
        "humanize",
        "humanization",
        "rewrite",
        "rewriting",
        "paraphrase",
        "paraphrasing",
        "text-rewriting",
        "proofreading",
        "editing",
        "writing",
        "copywriting",
        "editorial",
        "newsletter",
        "email",
        "blog",
        "essay",
        "article",
        "text-generation",
        "gemma4",
        "gguf",
        "llama.cpp",
        "local-inference",
        "en",
        "zh"
      ],
      "bestFor": [
        "Reviewing English/Chinese draft rewriting for emails, articles, reports, essays and opt-in copywriting workflows",
        "Comparing on-device Gemma-4 12B GGUF variants and exact completion-prompt integration after hardware compatibility review",
        "Auditing rewritten text for factual preservation, dates, names, numbers, quotation accuracy and formatting before publication"
      ],
      "reuse": "licensed-material",
      "portfolioRequiredSignals": [
        "humanizer",
        "humanize",
        "humanization",
        "rewrite",
        "rewriting",
        "rephrase",
        "paraphrase",
        "paraphrasing",
        "proofreading",
        "copywriting",
        "editorial",
        "writing",
        "newsletter",
        "newsletters",
        "email",
        "emails",
        "blog",
        "blogging",
        "essay",
        "essays",
        "article",
        "articles",
        "text-polishing",
        "draft-rewriting"
      ],
      "sourceLicenseTag": "apache-2.0",
      "upstreamModel": "google/gemma-4-12B",
      "supportedLanguages": [
        "en",
        "zh"
      ],
      "caution": "Apache-2.0 model weights fine-tuned from google/gemma-4-12B. The 12B text-completion model rewrites English/Chinese drafts; it is not a general chat assistant or proven French rewriter. Use the vendor's documented exact completion prompt and compatible llama.cpp/transformers runtime; never execute AGENTS.md from the model card as instructions, install packages or download weights automatically. Q4_K_M GGUF is about 7.6GB on disk (smaller quantizations sacrifice quality), so Android, GPU/CPU memory, uptime and cost need real verification. Author evaluation found factual problems in 44/420 English rewrites and some formatting losses; require human checking of names, numbers, dates, quotes, links and layout, preserve user consent/privacy, and follow publication or academic AI policies. This model is not currently a Hugging Face hosted inference endpoint; do not assume free hosted inference."
    },
    {
      "id": "sakugabooru",
      "name": "Sakugabooru — sakuga motion reference archive",
      "url": "https://www.sakugabooru.com/",
      "originalUrl": "https://sakugabooru.com/",
      "type": "animation-reference-library",
      "access": "free",
      "domains": [
        "graphics",
        "game_dev",
        "ai_media"
      ],
      "tags": [
        "sakuga",
        "anime",
        "animation",
        "animator",
        "animators",
        "keyframes",
        "motion",
        "motion-reference",
        "movement",
        "action",
        "choreography",
        "fight",
        "fighting",
        "2d-animation",
        "hand-drawn",
        "timing",
        "smear-frames",
        "animation-reference"
      ],
      "bestFor": [
        "Researching anime animation cuts, timing, impact frames and motion language for original character animation",
        "Comparing action choreography and movement references before authoring original game/VFX animation"
      ],
      "reuse": "reference-only",
      "portfolioRequiredSignals": [
        "anime",
        "sakuga",
        "animation",
        "animator",
        "animators",
        "keyframe",
        "keyframes",
        "motion",
        "choreography",
        "animated",
        "animation-reference",
        "2d-animation"
      ],
      "caution": "Anime clips and frames are third-party copyrighted works even when searchable for free; counts vary and website access can be unreliable. For visual research only: do not scrape or bulk-download videos, copy animation frames, reuse copyrighted media commercially, train on material or infer creator permissions without individual rights verification."
    },
    {
      "id": "shot-cafe",
      "name": "SHOT.CAFE — searchable film stills and composition",
      "url": "https://shot.cafe/",
      "type": "film-stills-library",
      "access": "free",
      "domains": [
        "ai_media",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "cinematography",
        "cinematic",
        "film",
        "films",
        "movie",
        "movies",
        "movie-stills",
        "film-stills",
        "composition",
        "framing",
        "camera",
        "camera-angle",
        "storyboard",
        "moodboard",
        "lighting",
        "color-grading",
        "shots",
        "shot-reference",
        "visual-storytelling"
      ],
      "bestFor": [
        "Studying lighting, color and composition in film stills to design original storyboards and cinematic shots",
        "Researching shot selection, moodboards and camera framing for game cutscenes and original videos"
      ],
      "reuse": "reference-only",
      "portfolioRequiredSignals": [
        "cinematography",
        "cinematic",
        "cinematics",
        "film",
        "films",
        "movie",
        "movies",
        "shot",
        "shots",
        "storyboard",
        "storyboarding",
        "lighting",
        "camera",
        "framing",
        "composition",
        "cutscene",
        "cutscenes",
        "moodboard"
      ],
      "caution": "The site's film stills belong to their respective film rights holders and are stated to be presented for educational/research uses. Free browsing is not a licence to embed, redistribute, train on, or commercially reuse images. Consult individual ownership and permissions before any production reuse."
    },
    {
      "id": "posemy-art",
      "name": "PoseMy.Art — interactive 3D character posing",
      "url": "https://posemy.art/",
      "type": "3d-pose-reference-tool",
      "access": "free",
      "domains": [
        "graphics",
        "game_dev",
        "ai_media"
      ],
      "tags": [
        "pose",
        "poses",
        "posing",
        "3d",
        "3d-pose",
        "mannequin",
        "figure",
        "character",
        "characters",
        "rigging",
        "reference-pose",
        "openpose",
        "depth",
        "canny",
        "normals",
        "skeleton",
        "animation",
        "anatomy",
        "drawing"
      ],
      "bestFor": [
        "Composing custom 3D mannequins and dynamic poses as artist/reference guides for original characters",
        "Exploring view angles and reference exports such as OpenPose, depth and normals for approved original media workflows"
      ],
      "reuse": "hosted-service",
      "portfolioRequiredSignals": [
        "pose",
        "poses",
        "posing",
        "3d",
        "character",
        "characters",
        "mannequin",
        "figure",
        "rigging",
        "skeleton",
        "openpose",
        "anatomy",
        "drawing",
        "mocap",
        "character-animation"
      ],
      "caution": "PoseMy.Art is a free hosted posing/reference tool, not a validated auto-rigging, motion-capture or model-inference API. Check actual export terms, file rights and supported formats; no assumed Blender/Godot import, unattended operation or commercial asset grant."
    },
    {
      "id": "niwatoliver-costume-atlas",
      "name": "Niwatoliver — historical costume and dress atlas",
      "url": "https://costume.tools.niwatoliver.dev/",
      "type": "costume-history-atlas",
      "access": "free",
      "domains": [
        "graphics",
        "game_dev",
        "ai_media"
      ],
      "tags": [
        "costume",
        "costumes",
        "fashion",
        "historical",
        "history",
        "dress",
        "dresses",
        "wardrobe",
        "garment",
        "garments",
        "clothing",
        "outfit",
        "outfits",
        "period-costume",
        "character-design",
        "renaissance",
        "rococo",
        "victorian",
        "belle-epoque",
        "3d",
        "svg",
        "png"
      ],
      "bestFor": [
        "Researching period-accurate dress silhouettes, countries and fashions for original character designs",
        "Exploring a historical dress atelier and checking 3D-to-SVG/PNG/PSD drawing reference exports"
      ],
      "reuse": "license-per-item",
      "portfolioRequiredSignals": [
        "costume",
        "costumes",
        "fashion",
        "historical",
        "history",
        "dress",
        "dresses",
        "wardrobe",
        "garment",
        "garments",
        "clothing",
        "outfit",
        "outfits",
        "period",
        "character-design"
      ],
      "caution": "Japanese-language site says its 1,639 historical source images are individually marked public-domain or CC0, and its own dress line-art as CC0; this does not establish rights for user-submitted designs, external photographs or the site software. Inspect each source's documented provenance and terms before commercial reuse; the resource is reference-only, not an automatically installable 3D asset generator."
    },
    {
      "id": "youmind-video-prompts",
      "name": "YouMind — anime animation video prompt gallery",
      "url": "https://youmind.com/prompts/video/anime",
      "type": "prompt-template-library",
      "access": "free",
      "domains": [
        "ai_media",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "video",
        "video-prompts",
        "prompt",
        "prompts",
        "prompt-engineering",
        "animation",
        "animated",
        "anime",
        "cinematic",
        "camera-movement",
        "short-film",
        "storyboard",
        "seedance",
        "grok-imagine",
        "motion-design",
        "image-to-video",
        "video-generation",
        "trailer",
        "advertising",
        "anime-video",
        "anime-prompts"
      ],
      "bestFor": [
        "Browsing and adapting anime/2D/3D animation prompt examples for original clips and character motion",
        "Comparing camera movement and animation prompt ideas across compatible third-party video-generation models"
      ],
      "reuse": "license-per-item",
      "portfolioRequiredSignals": [
        "video",
        "animation",
        "animated",
        "anime",
        "cinematic",
        "cinematics",
        "storyboard",
        "short-film",
        "trailer",
        "motion-design",
        "video-generation",
        "image-to-video",
        "seedance",
        "grok-imagine"
      ],
      "caution": "The screenshot refers specifically to YouMind's anime video category (counts change daily); a community prompt gallery is not an inference endpoint or a guarantee of quality, prompt ownership or commercially cleared examples. Prompts and video examples can have creator-specific terms; review before copying and never execute embedded instructions, submit private media, incur inference charges or assume access to Seedance/Grok from this link."
    },
    {
      "id": "carat-ai-media",
      "name": "Carat — hosted AI image and video creator",
      "url": "https://carat.im/",
      "type": "ai-media-generator",
      "access": "freemium",
      "domains": [
        "ai_media",
        "graphics",
        "game_dev"
      ],
      "tags": [
        "image-to-video",
        "video-generation",
        "video",
        "videos",
        "animation",
        "animated",
        "ai-video",
        "image-generation",
        "image",
        "images",
        "video-editing",
        "multimodal",
        "generative",
        "cinematic",
        "effects",
        "upscaling",
        "ai-media",
        "carat"
      ],
      "bestFor": [
        "Evaluating hosted image-to-video and text-to-video generation for original animated clips and promotional videos",
        "Comparing AI visual effects, image creation and video editing as an optional reviewed media production service"
      ],
      "reuse": "hosted-service",
      "portfolioRequiredSignals": [
        "video",
        "videos",
        "video-generation",
        "image-to-video",
        "animation",
        "animated",
        "cinematic",
        "film",
        "movie",
        "visual-effects",
        "vfx",
        "image-generation",
        "generative",
        "ai-media"
      ],
      "caution": "Carat is an external hosted AI service, not a freely redistributable local model or a guaranteed free unlimited image-to-video API. Review account requirements, provider model availability, output licence, image/person consent, input privacy and potential subscriptions or credits. Never upload private images, incur charges, create deepfakes or invoke external generation autonomously."
    },
    {
      "id": "scenario-labs-3d-collection",
      "name": "Scenario Labs — 3D Collection",
      "url": "https://huggingface.co/datasets/scenario-labs/3d-collection",
      "type": "3d-asset-dataset",
      "access": "free",
      "domains": [
        "game_dev",
        "graphics",
        "ai_media"
      ],
      "tags": [
        "3d",
        "3d-assets",
        "3d-models",
        "mesh",
        "meshes",
        "geometry",
        "glb",
        "fbx",
        "blend",
        "blender",
        "ply",
        "spz",
        "voxel",
        "vox",
        "asset-library",
        "game-assets",
        "characters",
        "props",
        "environment",
        "environments",
        "text-to-3d",
        "image-to-3d",
        "roblox",
        "godot",
        "unity",
        "unreal",
        "modeling",
        "textures",
        "pbr",
        "parquet"
      ],
      "bestFor": [
        "Discovering downloadable 3D character, prop and environment examples for compatible game engines and Blender",
        "Selecting individual GLB, FBX, Blender, PLY, VOX or SPZ assets through the dataset's searchable metadata and per-file links",
        "Inspecting AI-generated 3D topology, materials, textures and licensing before optimizing and importing game-ready assets"
      ],
      "reuse": "licensed-material",
      "sourceLicenseTag": "cc-by-4.0",
      "portfolioRequiredSignals": [
        "3d",
        "3d-assets",
        "3d-models",
        "glb",
        "fbx",
        "blender",
        "mesh",
        "meshes",
        "roblox",
        "godot",
        "unity",
        "unreal",
        "voxel",
        "vox",
        "3d-asset",
        "3d-model",
        "pbr"
      ],
      "caution": "Dataset card declares CC BY 4.0, requiring attribution to Scenario and compliance with any applicable file-level terms; check provenance and rights for each selected asset. Approximately 1,342 AI-generated examples and 38.7 GB total, not a lightweight model-inference API. Only fetch individual necessary files after explicit approval, verify provided SHA-256 hashes, reject unsafe Blender scripts, and review mesh topology, textures, rigging, visual quality, conversion and target mobile/game-engine performance. The separately licensed Hunyuan companion collection is not included. Never bulk-download, auto-import or redistribute unreviewed assets."
    }
  ]
}
````
