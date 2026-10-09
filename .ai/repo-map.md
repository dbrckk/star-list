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
    license-backfill.yml
    refresh-metadata.yml
    semantic-refresh.yml
    validate.yml
.serena/
  project.yml
imports/
  github-stars-2026-09-27-batch-2.json
  github-stars-2026-09-27-batch-3.json
  github-stars-2026-09-27-batch-4.json
  github-stars-2026-09-27.json
  github-stars-2026-10-09-batch-2.json
  github-stars-2026-10-09-batch-3.json
  github-stars-2026-10-09.json
reports/
  star-import-2026-10-09-batch-2-metadata-1.json
  star-import-2026-10-09-batch-2-metadata-2.json
  star-import-2026-10-09-batch-2-metadata-3.json
  star-import-2026-10-09-batch-2-metadata-4.json
  star-import-2026-10-09-batch-2-metadata-5.json
  star-import-2026-10-09-batch-2-metadata-6.json
  star-import-2026-10-09-batch-2-metadata-7.json
  star-import-2026-10-09-batch-2.json
  star-import-2026-10-09-batch-3-metadata-1.json
  star-import-2026-10-09-batch-3-metadata-2.json
  star-import-2026-10-09-batch-3-reviewed.json
  star-import-2026-10-09-batch-3.json
  star-import-2026-10-09-metadata-1.json
  star-import-2026-10-09-metadata-2.json
  star-import-2026-10-09-metadata-3.json
  star-import-2026-10-09.json
schemas/
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
  health-drift.schema.json
  health-snapshot.schema.json
  health-trends.schema.json
  history.schema.json
  replacement-report.schema.json
scripts/
  analyze_cache_health.py
  analyze_coverage.py
  audit_catalog_quality.py
  backfill_licenses.py
  build_discovery_watchlist.py
  catalog_stats.py
  detect_health_drift.py
  discover_candidates.py
  evaluate_candidates.py
  filter_discovery_memory.py
  find_replacements.py
  health_score.py
  infer_selection_guidance.py
  recommend.py
  refresh_github_metadata.py
  render_discovery_issue.py
  render_health_issue.py
  star_import_pipeline.py
  test_analyze_coverage.py
  test_backfill_licenses.py
  test_cache_health_history.py
  test_cache_health.py
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
  test_health_drift.py
  test_health_score.py
  test_history.py
  test_json_contracts.py
  test_pipeline_integration.py
  test_recommend.py
  test_refresh_github_metadata.py
  test_render_discovery_issue.py
  test_render_health_issue.py
  test_selection_guidance.py
  test_star_import_pipeline.py
  update_cache_health_history.py
  update_history.py
  validate_catalog.py
  validate_json_contract.py
.repo-standards.yml
AGENTS.md
cache-health-history.json
catalog.json
catalog.schema.json
discovery-memory.json
README.md
stacks.json
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
      - name: Publish catalog quality audit
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          REVIEW=$(python -c "import json; print(json.load(open('catalog-quality.json'))['summary']['review'])")
          INFO=$(python -c "import json; print(json.load(open('catalog-quality.json'))['summary']['info'])")
          TOTAL=$(python -c "import json; print(json.load(open('catalog-quality.json'))['summary']['findings'])")
          MARKER='<!-- star-list-catalog-quality -->'
          EXISTING=$(gh issue list --state open --search "$MARKER in:body" --json number --jq '.[0].number // empty')
          if [ "$TOTAL" = "0" ]; then
            if [ -n "$EXISTING" ]; then gh issue close "$EXISTING" --comment "Catalog quality audit is clean."; fi
          elif [ -n "$EXISTING" ]; then
            gh issue edit "$EXISTING" --title "Catalog quality: $REVIEW review / $INFO info" --body-file catalog-quality.md
          else
            gh issue create --title "Catalog quality: $REVIEW review / $INFO info" --body-file catalog-quality.md --label maintenance || gh issue create --title "Catalog quality: $REVIEW review / $INFO info" --body-file catalog-quality.md
          fi
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
          git push
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
      - name: Validate catalog
        run: |
          python scripts/validate_catalog.py
          python scripts/validate_json_contract.py catalog.schema.json catalog.json
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
      - name: Test selection guidance inference
        run: python scripts/test_selection_guidance.py
      - name: Test recommendation engine
        run: python scripts/test_recommend.py
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

## File: imports/github-stars-2026-09-27-batch-2.json
````json
{
  "capturedAt": "2026-09-27",
  "source": "user-provided GitHub Stars screenshots (batch 2)",
  "repositories": [
    "JustVugg/colibri",
    "cloudflare/security-audit-skill",
    "CarterPerez-dev/Cybersecurity-Projects",
    "block/buzz",
    "Lakr233/vphone-cli",
    "ruvnet/RuView",
    "rlaope/oh-my-hermes",
    "n8n-io/n8n",
    "Tencent/WeKnora",
    "Tencent/BrowserSkill",
    "openai/codex",
    "cline/cline",
    "addyosmani/agent-skills",
    "supabase/supabase",
    "roboflow/supervision",
    "anthropics/claude-code",
    "NationalSecurityAgency/ghidra",
    "ankitects/anki",
    "anthropics/knowledge-work-plugins",
    "jamiepine/voicebox",
    "Mafifrizi/ARES",
    "AI4Finance-Foundation/FinRL",
    "nautechsystems/nautilus_trader",
    "ccxt/ccxt",
    "freqtrade/freqtrade",
    "virattt/ai-hedge-fund",
    "cactus-compute/needle",
    "ruanyf/weekly",
    "docling-project/docling",
    "Open-Dev-Society/OpenStock",
    "kaiiyer/awesome-vulnerable",
    "latent-spaces/brag",
    "ahmedkhaleel2004/gitdiagram",
    "tradesdontlie/tradingview-mcp",
    "supermemoryai/supermemory",
    "Fission-AI/OpenSpec",
    "earendil-works/pi",
    "Paramchoudhary/ResumeSkills",
    "career-ops-hq/career-ops",
    "Dokploy/dokploy",
    "CopilotKit/CopilotKit",
    "unslothai/unsloth",
    "aaif-goose/goose",
    "code-yeongyu/oh-my-openagent",
    "agno-agi/agno",
    "mindsdb/mindshub",
    "OpenBB-finance/OpenBB",
    "RSSNext/Folo",
    "MemPlace/memplace",
    "infiniflow/ragflow",
    "federicodeponte/opendraft",
    "bradygaster/squad",
    "garrytan/gstack",
    "elie222/rakazo",
    "lidge-jun/opencodex",
    "simplifaisoul/osiris",
    "vercel-labs/json-render",
    "higgsfield-ai/higgsfield",
    "mihail911/modern-software-dev-assignments",
    "paperless-ngx/paperless-ngx",
    "anthropics/financial-services",
    "trycua/cua",
    "Graphify-Labs/graphify",
    "cookiy-ai/user-research-skill",
    "199-biotechnologies/claude-deep-research-skill",
    "myanhorn/last30days-skill",
    "ZeroPointRepo/youtube-skills",
    "bevibing/tutor-skills",
    "pacifico/atlas",
    "MG1937/ASC",
    "open-webui/open-webui",
    "letta-ai/letta",
    "HKUDS/DeepTutor",
    "LasCC/HackTools",
    "reddellexc/hackerone-reports",
    "zeroc00I/AllVideoPocsFromHackerOne",
    "davepoon/buildwithclaude",
    "enjoy-digital/litex",
    "isair/jarvis",
    "koala73/worldmonitor",
    "searxng/searxng",
    "imputnet/cobalt",
    "pydantic/pydantic-ai",
    "moorcheh-ai/memanto",
    "coollabsio/coolify",
    "AppFlowy-IO/AppFlowy",
    "medusajs/medusa",
    "TryGhost/Ghost",
    "plausible/analytics",
    "calcom/cal.com",
    "abue-ammar/tinycast"
  ]
}
````

## File: imports/github-stars-2026-09-27-batch-3.json
````json
{
  "capturedAt": "2026-09-27",
  "source": "user-provided GitHub Stars screenshots (batch 3)",
  "repositories": [
    "microsoft/agent-lightning",
    "lastmile-ai/mcp-agent",
    "simular-ai/Agent-S",
    "VectifyAI/PageIndex",
    "LibreTranslate/LibreTranslate",
    "dgtlmoon/changedetection.io",
    "searxng/searxng",
    "imputnet/cobalt",
    "pydantic/pydantic-ai",
    "moorcheh-ai/memanto",
    "coollabsio/coolify",
    "AppFlowy-IO/AppFlowy",
    "browser-use/jev-ultrafast",
    "Comfy-Org/ComfyUI",
    "caido/skills",
    "caido/caido",
    "Recurse-Labs/recurse",
    "google/artemis",
    "opentoonz/opentoonz",
    "apurvsinghgautam/robin",
    "yynxxxxx/Codex-X",
    "Crosstalk-Solutions/project-nomad",
    "zhouxiaoka/autoclip",
    "mvt-project/mvt",
    "cloudflare/quiche",
    "projectdiscovery/nuclei-templates",
    "projectdiscovery/nuclei",
    "google/ax",
    "muellerberndt/cadence",
    "0x6rss/chat-apps-osint",
    "charlie947/social-media-skills",
    "coreyhaines31/marketingskills",
    "Jakubantalik/transitions.dev",
    "Leonxlnx/taste-skill",
    "nextlevelbuilder/ui-ux-pro-max-skill",
    "anthropics/skills",
    "upstash/context7",
    "FareedKhan-dev/kimi-k3-in-c",
    "HarnessRouter/harnessrouter",
    "TianyuCodings/NanoJev",
    "jarrodwatts/jev-trader",
    "tamaratran/fast-jev-compaction",
    "Scottcjn/Rustchain",
    "henrygd/beszel",
    "harry7557558/spirula-studio",
    "pbakaus/impeccable",
    "HKUDS/CLI-Anything",
    "strands-agents/harness-sdk",
    "browser-use/video-use",
    "superdesigndev/treg",
    "davila7/claude-code-templates",
    "dream-num/univer",
    "elder-plinius/OBLITERATUS",
    "elder-plinius/CL4R1T4S",
    "lahfir/agent-desktop",
    "rohitg00/ai-engineering-from-scratch",
    "superlinked/sie",
    "kserve/kserve",
    "bentoml/BentoML",
    "triton-inference-server/server",
    "mudler/LocalAI",
    "ggml-org/llama.cpp",
    "sgl-project/sglang",
    "vllm-project/vllm",
    "hesreallyhim/awesome-claude-code",
    "awesome-selfhosted/awesome-selfhosted",
    "ripienaar/free-for-dev",
    "squidfunk/mkdocs-material",
    "xiaolai/the-craft-of-selfteaching",
    "ahmadrosid/nakama",
    "zts212653/clowder-ai",
    "maziyarpanahi/openmed",
    "triggerdotdev/trigger.dev",
    "PrefectHQ/fastmcp",
    "drizzle-team/drizzle-orm",
    "better-auth/better-auth",
    "assistant-ui/assistant-ui",
    "vercel/ai",
    "joxeankoret/diaphora",
    "NandhaKishorM/laya",
    "JohnHeibel/PDoomVideo",
    "raulhenchal/Rapid-MLX",
    "tihanyin/REx-skill",
    "leejet/stable-diffusion.cpp",
    "vectorize-io/hindsight",
    "openbao/openbao",
    "kelseyhightower/kubernetes-the-hard-way",
    "androoAGI/starnet",
    "anthropics/claude-plugins-official",
    "paperclipai/paperclip",
    "dubinc/dub",
    "PostHog/posthog",
    "novuhq/novu",
    "openmeterio/openmeter",
    "SigNoz/signoz",
    "promptfoo/promptfoo"
  ]
}
````

## File: imports/github-stars-2026-09-27-batch-4.json
````json
{
  "capturedAt": "2026-09-27",
  "source": "user-provided GitHub Stars screenshots (batch 4)",
  "repositories": [
    "mobile-next/mobile-mcp",
    "actions/runner-images",
    "anthropics/claude-code-action",
    "llvm/llvm-project",
    "zhaoxuya520/reverse-skill",
    "tensorflow/tensorflow",
    "openbao/openbao",
    "kelseyhightower/kubernetes-the-hard-way",
    "androoAGI/starnet",
    "anthropics/claude-plugins-official",
    "paperclipai/paperclip",
    "dubinc/dub",
    "PostHog/posthog",
    "Coding-Solo/godot-mcp",
    "2Retro/GodotOceanWaves",
    "GodotSteam/GodotSteam",
    "godotengine/godot-demo-projects",
    "godotengine/godot-docs",
    "NVIDIA/Model-Optimizer",
    "slavakurilyak/awesome-ai-agents",
    "jankeesvw/omarchy-meeting-recorder",
    "MakazhanAlpamys/Soup",
    "dalathegreat/Battery-Emulator",
    "rynfarr/meridian",
    "microsoft/vscode",
    "vercel/next.js",
    "open-android/Android",
    "greensock/GSAP",
    "lgvalle/Material-Animations",
    "juliangarnier/anime",
    "MisterBooo/LeetCodeAnimation",
    "google/liquidfun",
    "deepinsight/insightface",
    "timzhang642/3D-Machine-Learning",
    "mrdoob/three.js",
    "cgwire/awesome-cg-vfx-pipeline",
    "GodotNuts/GodotFirebase",
    "gdquest-demos/godot-open-rpg",
    "GDRETools/gdsdecomp",
    "gdquest-demos/godot-shaders",
    "KenneyNL/Starter-Kit-3D-Platformer",
    "Zylann/godot_voxel",
    "liangxiegame/QFramework",
    "nibzard/awesome-agentic-patterns",
    "awarexone/Agentic-Bug-Hunter",
    "iamwithai/production-agentic-rag-course",
    "cloudflare/agentic-inbox",
    "sickn33/agentic-awesome-skills",
    "Fosowl/agenticSeek",
    "transitive-bullshit/agentic",
    "JetBrains/android",
    "wgtunnel/android",
    "bitwarden/android",
    "LineageOS/android",
    "nextcloud/android"
  ]
}
````

## File: imports/github-stars-2026-09-27.json
````json
{
  "capturedAt": "2026-09-27",
  "source": "user-provided GitHub Stars screenshots",
  "repositories": [
    "A-poc/RedTeam-Tools",
    "infosecn1nja/Red-Teaming-Toolkit",
    "redcanaryco/atomic-red-team",
    "arch3rPro/PentestTools",
    "juliocesarfort/public-pentesting-reports",
    "m14r41/PentestingEverything",
    "enaqx/awesome-pentest",
    "GreyDGL/PentestGPT",
    "vxcontrol/pentagi",
    "SnailSploit/Claude-Red",
    "asgeirtj/system_prompts_leaks",
    "pascalorg/editor",
    "Solido/awesome-flutter",
    "flutter-team-archive/plugins",
    "flutter/flutter",
    "AgriciDaniel/claude-obsidian",
    "kepano/obsidian-skills",
    "blaCCkHatHacEEkr/PENTESTING-BIBLE",
    "xtekky/gpt4free",
    "freefq/free",
    "cursor/plugins",
    "tt-a1i/archify",
    "bluscreenofjeff/Red-Team-Infrastructure-Wiki",
    "BitterSecurity/Deception",
    "yeyintminthuhtut/Awesome-Red-Teaming",
    "microsoft/ai-agents-for-beginners",
    "langchain-ai/langgraph",
    "FlowiseAI/Flowise",
    "BerriAI/litellm",
    "bytedance/deer-flow",
    "headroomlabs-ai/headroom",
    "langchain-ai/langchain",
    "microsoft/markitdown",
    "langgenius/dify",
    "firebase/flutterfire",
    "toly1994328/FlutterUnit",
    "bytedance/UI-TARS-desktop",
    "animate-css/animate.css",
    "kyegomez/awesome-multi-agent-papers",
    "doobidoo/mcp-memory-service",
    "microsoft/magentic-ui",
    "langfuse/langfuse",
    "microsoft/autogen",
    "soxoj/maigret",
    "sherlock-project/sherlock",
    "payloadcms/payload",
    "danielmiessler/SecLists",
    "infoslack/awesome-web-hacking",
    "rapid7/metasploit-framework",
    "mem0ai/mem0",
    "thedotmack/claude-mem",
    "academic/awesome-datascience",
    "DeusData/codebase-memory-mcp",
    "usermemos/memos",
    "crewAIInc/crewAI",
    "airbnb/lottie-web",
    "airbnb/lottie-ios",
    "airbnb/lottie-android",
    "Calinou/awesome-godot",
    "heroiclabs/nakama",
    "lettier/3d-game-shaders-for-beginners",
    "Donchitos/Claude-Code-Game-Studios",
    "godotengine/godot",
    "shadcn-ui/ui",
    "libgdx/libgdx",
    "google/filament",
    "tech-leads-club/agent-skills",
    "EsotericSoftware/spine-runtimes",
    "inkscape/inkscape",
    "rive-app/rive-android",
    "plattysoft/Leonids",
    "DanielMartinus/Konfetti",
    "online-ml/river",
    "The-Swarm-Corporation/AutoHedge",
    "OpenBMB/VoxCPM",
    "Fincept-Corporation/FinceptTerminal",
    "LibreChat-AI/LibreChat",
    "TauricResearch/TradingAgents",
    "ever-co/ever-gauzy",
    "huggingface/transformers",
    "jihe520/MathModelAgent",
    "alibaba/open-code-review",
    "alphaXiv/OpenResearch",
    "multimodal-art-projection/YuE",
    "calesthio/OpenMontage",
    "n4oPe/on-my-hermes",
    "stablyai/orca",
    "Panniantong/Agent-Reach",
    "trailhq/Graft",
    "opensandbox-group/OpenSandbox",
    "unclecode/crawl4ai",
    "firecrawl/firecrawl",
    "jo-inc/camofox-browser",
    "AgriciDaniel/claude-ads",
    "Open-LLM-VTuber/Open-LLM-VTuber",
    "HKUDS/Vibe-Trading"
  ]
}
````

## File: imports/github-stars-2026-10-09-batch-2.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "user-provided GitHub Stars screenshots (9), batch 2",
  "repositories": [
    "rehan-remade/universal-modder",
    "aarora4/Awesome-Prediction-Market-Tools",
    "caiovicentino/polymarket-mcp-server",
    "ent0n29/polybot",
    "evan-kolberg/prediction-market-backtesting",
    "SII-WANGZJ/Polymarket_data",
    "yangyuan-zhen/PolyWeather",
    "lihanyu81/polymarket_lp_tool",
    "HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits",
    "recogardtech/AutoPilotPM",
    "evidentlyai/evidently",
    "Giskard-AI/giskard-oss",
    "rawfilejson/awesome-osint-arsenal",
    "RickdeJager/stegseek",
    "OpenCut-app/OpenCut",
    "meituan-longcat/LongCat-Video",
    "cloudflare/cloudflare-os",
    "pingdotgg/t3code",
    "localsend/localsend",
    "Diolinux/PhotoGIMP",
    "1N3/Sn1per",
    "ComposioHQ/composio",
    "topoteretes/cognee",
    "mastra-ai/mastra",
    "lfnovo/open-notebook",
    "Stremio/stremio-web",
    "DuarteSantos8/openGym",
    "caddyserver/caddy",
    "earthtojake/text-to-cad",
    "michael-denyer/pstack-claude",
    "tester-army/e2e",
    "deepseek-ai/DeepGEMM",
    "morluto/rea",
    "elder-plinius/T3MP3ST",
    "kargulstudio/sales-crm",
    "open-rmf/rmf",
    "ros2/ros2",
    "google-deepmind/mujoco",
    "isaac-sim/IsaacLab",
    "openvla/openvla",
    "huggingface/lerobot",
    "lfnovo/esperanto",
    "osquery/osquery",
    "Velocidex/velociraptor",
    "guoyww/AnimateDiff",
    "AILab-CVC/VideoCrafter",
    "genmoai/mochi",
    "Lightricks/LTX-Video",
    "zai-org/CogVideo",
    "Wan-Video/Wan2.1",
    "huggingface/diffusers",
    "LaurieWired/GhidraMCP",
    "undefined-ui/second-brain-os",
    "gh1mau/masta-cve-2026-48907",
    "JustExecution/HTF_indicator",
    "boykopovar/AnyPS5",
    "LuxAlgo/PineTS",
    "XHToken/Spark-X2.5",
    "smicallef/spiderfoot",
    "MISP/MISP",
    "mitre-attack/attack-stix-data",
    "OISF/suricata",
    "zeek/zeek",
    "VirusTotal/yara",
    "SigmaHQ/sigma",
    "iamlukethedev/Herald-OS",
    "openai/math",
    "Quincunx33/Ai-jailbreak",
    "fxraptor-alpha/pinescript-indicators",
    "cantolab/open-source-fractal",
    "ict2023trader/Indicators",
    "firecracker-microvm/firecracker",
    "modal-labs/modal-examples",
    "taskflow/taskflow",
    "ray-project/ray",
    "camel-ai/camel",
    "justcallmekoko/ESP32Marauder",
    "trufflesecurity/trufflehog",
    "mitmproxy/mitmproxy",
    "apache/tika",
    "jina-ai/reader",
    "datalab-to/marker",
    "Unstructured-IO/unstructured",
    "rbrus/laya-as-judge",
    "pytest-dev/pytest",
    "github/github-mcp-server",
    "oraios/serena",
    "emilk/egui",
    "liquidslr/system-design-notes",
    "storytold/artcraft",
    "EpicGames/raddebugger",
    "OpenByteInc/QuantDinger",
    "go-gitea/gitea",
    "reviewdog/reviewdog",
    "dagger/dagger"
  ]
}
````

## File: imports/github-stars-2026-10-09-batch-3.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "user-provided GitHub Stars screenshots (2), batch 3",
  "repositories": [
    "metabase/metabase",
    "evidence-dev/evidence",
    "sinaptik-ai/pandas-ai",
    "apache/datafusion",
    "pola-rs/polars",
    "duckdb/duckdb",
    "eosphoros-ai/DB-GPT",
    "yifanfeng97/Hyper-Extract",
    "Jakeschincariol/arena-skill",
    "quarto-dev/quarto-cli",
    "apache/superset",
    "Kanaries/pygwalker",
    "Dataherald/dataherald",
    "open-metadata/OpenMetadata",
    "sodadata/soda-core",
    "fivetran/great_expectations",
    "dlt-hub/dlt",
    "airbytehq/airbyte",
    "defog-ai/sqlcoder",
    "pytest-dev/pytest",
    "github/github-mcp-server",
    "oraios/serena",
    "emilk/egui",
    "liquidslr/system-design-notes"
  ]
}
````

## File: imports/github-stars-2026-10-09.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "user-provided GitHub Stars screenshots",
  "repositories": [
    "MakazhanAlpamys/Soup",
    "dalathegreat/Battery-Emulator",
    "rynfarr/meridian",
    "microsoft/vscode",
    "vercel/next.js",
    "mobile-next/mobile-mcp",
    "actions/runner-images",
    "anthropics/claude-code-action",
    "llvm/llvm-project",
    "zhaoxuya520/reverse-skill",
    "tensorflow/tensorflow",
    "openbao/openbao",
    "kelseyhightower/kubernetes-the-hard-way",
    "GDRETools/gdsdecomp",
    "gdquest-demos/godot-shaders",
    "KenneyNL/Starter-Kit-3D-Platformer",
    "Zylann/godot_voxel",
    "liangxiegame/QFramework",
    "Coding-Solo/godot-mcp",
    "2Retr0/GodotOceanWaves",
    "GodotSteam/GodotSteam",
    "godotengine/godot-demo-projects",
    "godotengine/godot-docs",
    "NVIDIA/Model-Optimizer",
    "slavakurilyak/awesome-ai-agents",
    "jankeesvw/omarchy-meeting-recorder",
    "open-android/Android",
    "greensock/GSAP",
    "lgvalle/Material-Animations",
    "juliangarnier/anime",
    "MisterBooo/LeetCodeAnimation",
    "google/liquidfun",
    "deepinsight/insightface",
    "timzhang642/3D-Machine-Learning",
    "mrdoob/three.js",
    "cgwire/awesome-cg-vfx-pipeline",
    "GodotNuts/GodotFirebase",
    "gdquest-demos/godot-open-rpg",
    "JetBrains/android",
    "wgtunnel/android",
    "bitwarden/android",
    "LineageOS/android",
    "nextcloud/android",
    "owncloud/android",
    "shadcn-ui/lint",
    "arnegiacomo/fugleramme",
    "elliothux/open-compute",
    "chubbyguan/chubbyskills",
    "togg53192-cmd/jailbreaks",
    "nibzard/awesome-agentic-patterns",
    "awarexone/Agentic-Bug-Hunter",
    "jamwithai/production-agentic-rag-course",
    "cloudflare/agentic-inbox",
    "sickn33/agentic-awesome-skills",
    "Fosowl/agenticSeek",
    "transitive-bullshit/agentic",
    "daytonaio/daytona",
    "e2b-dev/E2B",
    "getzep/graphiti",
    "huggingface/smolagents",
    "OffGridPete/Fieldwatch",
    "D4Vinci/Scrapling",
    "whaleyxbt/patchright-enhanced",
    "Ignitetechnologies/Mindmap",
    "JoasASantos/Offensive-Security-AI-Models",
    "letta-ai/letta-code",
    "myschwarz/openrig",
    "InfinityLoop1308/PipePipe",
    "agentverse-os/AgentVerse-OS",
    "yejy53/Editable-Design",
    "pizza-bot-app/pizza-bot",
    "anmolkapil/plexo",
    "vinnylarouge/jevlike",
    "Antseed/openclaw-channel-antseed",
    "Antseed/AIPs",
    "Antseed/antseed",
    "Effect-TS/effect",
    "colbymchenry/codegraph",
    "getsentry/sentry",
    "google/skills",
    "NVIDIA/OpenShell",
    "JuliusBrussee/caveman",
    "Epix-Incorporated/Adonis",
    "roblox-ts/roblox-ts",
    "axstin/rbxfpsunlocker",
    "confident-ai/deepeval",
    "lihanyu81/polymarket_lp_tool",
    "HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits",
    "recogardtech/AutoPilotPM",
    "evidentlyai/evidently",
    "Giskard-AI/giskard-oss",
    "openai/evals",
    "truera/trulens",
    "UKGovernmentBEIS/inspect_ai",
    "Arize-ai/phoenix",
    "comet-ml/opik",
    "vibrantlabsai/ragas"
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-1.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "rehan-remade/universal-modder",
      "description": "Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own: recon, reverse engineering, fal-generated art/3D/audio, in-game testing, showcase videos.",
      "language": "Python",
      "github": {
        "stars": 5656,
        "forks": 530,
        "openIssues": 41,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T23:19:15Z"
      }
    },
    {
      "repo": "aarora4/Awesome-Prediction-Market-Tools",
      "description": "A curated list of Prediction Market Tools - AI Agents, Analytics, APIs, Dashboards, Copy Trading, Alerting, Tracking and More!!",
      "language": null,
      "github": {
        "stars": 767,
        "forks": 268,
        "openIssues": 147,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T03:03:02Z"
      }
    },
    {
      "repo": "caiovicentino/polymarket-mcp-server",
      "description": "🤖 AI-Powered MCP Server for Polymarket - Enable Claude to trade prediction markets with 45 tools, real-time monitoring, and enterprise-grade safety features",
      "language": "Python",
      "github": {
        "stars": 689,
        "forks": 143,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:04:03Z"
      }
    },
    {
      "repo": "ent0n29/polybot",
      "description": "Reverse-engineering of  every polymarket strategy and high-frequency trading infrastructure for Polymarket",
      "language": "Java",
      "github": {
        "stars": 1019,
        "forks": 176,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-02-20T23:34:32Z"
      }
    },
    {
      "repo": "evan-kolberg/prediction-market-backtesting",
      "description": "An extension for Nautilus Trader",
      "language": "Python",
      "github": {
        "stars": 1211,
        "forks": 196,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v4.1-alpha",
        "license": "NOASSERTION",
        "pushedAt": "2026-05-16T21:24:47Z"
      }
    },
    {
      "repo": "SII-WANGZJ/Polymarket_data",
      "description": "A comprehensive dataset of 1.1 billion trading records from Polymarket, processed into multiple analysis-ready formats. Features cleaned data, unified token perspectives, and user-level transformations — ready for market research, behavioral studies, and quantitative analysis.",
      "language": "Python",
      "github": {
        "stars": 858,
        "forks": 121,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-01-01T13:17:37Z"
      }
    },
    {
      "repo": "yangyuan-zhen/PolyWeather",
      "description": "polymarket Intelligent Weather Quant Analysis Bot",
      "language": "Python",
      "github": {
        "stars": 316,
        "forks": 73,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T17:25:12Z"
      }
    },
    {
      "repo": "rawfilejson/awesome-osint-arsenal",
      "description": "OSINT & recon toolkit // 100+ tools, one-command installer, SOCMINT, GEOINT, network recon, dark web, forensics & more.",
      "language": "Shell",
      "github": {
        "stars": 3204,
        "forks": 477,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-29T03:14:19Z"
      }
    },
    {
      "repo": "RickdeJager/stegseek",
      "description": ":zap: Worlds fastest steghide cracker, chewing through millions of passwords per second :zap:",
      "language": "C++",
      "github": {
        "stars": 1332,
        "forks": 136,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-2.0",
        "pushedAt": "2023-10-10T12:20:59Z"
      }
    },
    {
      "repo": "OpenCut-app/OpenCut",
      "description": "The open-source CapCut alternative",
      "language": "TypeScript",
      "github": {
        "stars": 93251,
        "forks": 9153,
        "openIssues": 375,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-24T09:24:44Z"
      }
    },
    {
      "repo": "meituan-longcat/LongCat-Video",
      "description": null,
      "language": "Python",
      "github": {
        "stars": 9110,
        "forks": 1585,
        "openIssues": 82,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-27T02:51:41Z"
      }
    },
    {
      "repo": "cloudflare/cloudflare-os",
      "description": "Agent workspace built on Cloudflare Workers for creating documents, building apps, and running agents with your company’s context and systems.",
      "language": "TypeScript",
      "github": {
        "stars": 11285,
        "forks": 1346,
        "openIssues": 132,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T22:40:55Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-2.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "pingdotgg/t3code",
      "description": null,
      "language": "TypeScript",
      "github": {
        "stars": 26414,
        "forks": 6870,
        "openIssues": 2831,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:31:05Z"
      }
    },
    {
      "repo": "localsend/localsend",
      "description": "An open-source cross-platform alternative to AirDrop",
      "language": "Dart",
      "github": {
        "stars": 93704,
        "forks": 5231,
        "openIssues": 1008,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-07T23:01:53Z"
      }
    },
    {
      "repo": "Diolinux/PhotoGIMP",
      "description": "A Patch for GIMP 3+ for Photoshop Users",
      "language": "Python",
      "github": {
        "stars": 18328,
        "forks": 745,
        "openIssues": 43,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-27T05:10:17Z"
      }
    },
    {
      "repo": "1N3/Sn1per",
      "description": "Automated penetration testing & attack surface management platform. Recon, scan, exploit, report — 600+ exploits, 90+ integrations, 10K+ detections.",
      "language": "Shell",
      "github": {
        "stars": 11393,
        "forks": 2210,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-07-04T21:10:21Z"
      }
    },
    {
      "repo": "ComposioHQ/composio",
      "description": "Composio powers 1000+ toolkits, tool search, context management, authentication, and a sandboxed workbench to help you build AI agents that turn intent into action.",
      "language": "TypeScript",
      "github": {
        "stars": 30474,
        "forks": 4848,
        "openIssues": 110,
        "archived": false,
        "disabled": false,
        "defaultBranch": "next",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:09:09Z"
      }
    },
    {
      "repo": "topoteretes/cognee",
      "description": "Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory with small models for free",
      "language": "Python",
      "github": {
        "stars": 31763,
        "forks": 3275,
        "openIssues": 569,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:22:39Z"
      }
    },
    {
      "repo": "mastra-ai/mastra",
      "description": "Mastra is the modern TypeScript framework for AI-powered applications and agents.",
      "language": "TypeScript",
      "github": {
        "stars": 28649,
        "forks": 2943,
        "openIssues": 566,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T01:27:59Z"
      }
    },
    {
      "repo": "lfnovo/open-notebook",
      "description": "An Open Source implementation of Notebook LM with more flexibility and features",
      "language": "TypeScript",
      "github": {
        "stars": 39969,
        "forks": 4628,
        "openIssues": 153,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T02:29:31Z"
      }
    },
    {
      "repo": "Stremio/stremio-web",
      "description": "Stremio - Freedom to Stream",
      "language": "JavaScript",
      "github": {
        "stars": 14447,
        "forks": 1643,
        "openIssues": 67,
        "archived": false,
        "disabled": false,
        "defaultBranch": "development",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T14:16:34Z"
      }
    },
    {
      "repo": "DuarteSantos8/openGym",
      "description": "Self-hosted gym & body-weight tracker — plan routines, log workouts (supersets, warm-ups, cardio), see which muscles are trained, fatigued or detrained, import from FitNotes/Strong/Hevy, passkey login. Your data, your server.",
      "language": "JavaScript",
      "github": {
        "stars": 8039,
        "forks": 1024,
        "openIssues": 152,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T13:32:09Z"
      }
    },
    {
      "repo": "caddyserver/caddy",
      "description": "Fast and extensible multi-platform HTTP/1-2-3 web server with automatic HTTPS",
      "language": "Go",
      "github": {
        "stars": 77554,
        "forks": 5102,
        "openIssues": 287,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T04:02:21Z"
      }
    },
    {
      "repo": "earthtojake/text-to-cad",
      "description": "Give your agent CAD superpowers.",
      "language": "Python",
      "github": {
        "stars": 18479,
        "forks": 1834,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:16:19Z"
      }
    },
    {
      "repo": "michael-denyer/pstack-claude",
      "description": "Claude Code, Codex, Copilot, Pi, OpenCode, Gemini, and Prime Agent versions of Poteto's pstack. Rigorous agent workflows with Cursor primitives translated for other harnesses.",
      "language": "JavaScript",
      "github": {
        "stars": 1652,
        "forks": 176,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T21:45:55Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-3.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "tester-army/e2e",
      "description": "Next generation e2e testing framework for web and mobile apps.",
      "language": "TypeScript",
      "github": {
        "stars": 8182,
        "forks": 383,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T22:06:20Z"
      }
    },
    {
      "repo": "deepseek-ai/DeepGEMM",
      "description": "DeepGEMM: clean and efficient BLAS kernel library on GPU",
      "language": "Cuda",
      "github": {
        "stars": 8880,
        "forks": 1396,
        "openIssues": 151,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T01:48:05Z"
      }
    },
    {
      "repo": "morluto/rea",
      "description": "Reverse engineer anything with agents, from app behavior down to native binaries.",
      "language": "TypeScript",
      "github": {
        "stars": 27007,
        "forks": 3066,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:29:24Z"
      }
    },
    {
      "repo": "elder-plinius/T3MP3ST",
      "description": "autonomous red teaming platform; multi-agent offensive-security meta-harness",
      "language": "TypeScript",
      "github": {
        "stars": 6452,
        "forks": 1331,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-08T16:37:44Z"
      }
    },
    {
      "repo": "karqulstudio/sales-crm",
      "error": "NOT_FOUND: Error code: NOT_FOUND; Error: GitHub API error 404: {\"message\":\"Not Found\",\"documentation_url\":\"https://docs.github.com/rest/repos/repos#get-a-repository\",\"status\":\"404\"}"
    },
    {
      "repo": "open-rmf/rmf",
      "description": "Root repository for the RMF software",
      "language": "Python",
      "github": {
        "stars": 445,
        "forks": 90,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-08-25T01:22:32Z"
      }
    },
    {
      "repo": "ros2/ros2",
      "description": "The Robot Operating System, is a meta operating system for robots.",
      "language": null,
      "github": {
        "stars": 6136,
        "forks": 963,
        "openIssues": 151,
        "archived": false,
        "disabled": false,
        "defaultBranch": "rolling",
        "license": null,
        "pushedAt": "2026-10-07T13:51:04Z"
      }
    },
    {
      "repo": "google-deepmind/mujoco",
      "description": "Multi-Joint dynamics with Contact. A general purpose physics simulator.",
      "language": "C++",
      "github": {
        "stars": 15528,
        "forks": 1815,
        "openIssues": 292,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:33:34Z"
      }
    },
    {
      "repo": "isaac-sim/IsaacLab",
      "description": "Unified framework for robot learning with multi-physics/renderer support",
      "language": "Python",
      "github": {
        "stars": 8299,
        "forks": 3940,
        "openIssues": 364,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-09T00:55:55Z"
      }
    },
    {
      "repo": "openvla/openvla",
      "description": "OpenVLA: An open-source vision-language-action model for robotic manipulation.",
      "language": "Python",
      "github": {
        "stars": 7124,
        "forks": 854,
        "openIssues": 118,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-03-23T23:41:01Z"
      }
    },
    {
      "repo": "huggingface/lerobot",
      "description": "🤗 LeRobot: Making AI for Robotics more accessible with end-to-end learning",
      "language": "Python",
      "github": {
        "stars": 28017,
        "forks": 5839,
        "openIssues": 966,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T21:24:14Z"
      }
    },
    {
      "repo": "lfnovo/esperanto",
      "description": "A unified interface for various AI model providers",
      "language": "Python",
      "github": {
        "stars": 220,
        "forks": 53,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T21:12:50Z"
      }
    },
    {
      "repo": "osquery/osquery",
      "description": "SQL powered operating system instrumentation, monitoring, and analytics.",
      "language": "C++",
      "github": {
        "stars": 23629,
        "forks": 2610,
        "openIssues": 591,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T01:06:29Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-4.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "Velocidex/velociraptor",
      "description": "Digging Deeper....",
      "language": "Go",
      "github": {
        "stars": 4312,
        "forks": 661,
        "openIssues": 77,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-07T11:34:46Z"
      }
    },
    {
      "repo": "guoyww/AnimateDiff",
      "description": "Official implementation of AnimateDiff.",
      "language": "Python",
      "github": {
        "stars": 12274,
        "forks": 1101,
        "openIssues": 319,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-07-31T01:14:15Z"
      }
    },
    {
      "repo": "AILab-CVC/VideoCrafter",
      "description": "VideoCrafter2: Overcoming Data Limitations for High-Quality Video Diffusion Models",
      "language": "Python",
      "github": {
        "stars": 5098,
        "forks": 411,
        "openIssues": 74,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-01-09T15:01:22Z"
      }
    },
    {
      "repo": "genmoai/mochi",
      "description": "The best OSS video generation models, created by Genmo",
      "language": "Python",
      "github": {
        "stars": 3746,
        "forks": 494,
        "openIssues": 60,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T17:19:13Z"
      }
    },
    {
      "repo": "Lightricks/LTX-Video",
      "description": "Official repository for LTX-Video",
      "language": "Python",
      "github": {
        "stars": 11056,
        "forks": 1164,
        "openIssues": 101,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-01-05T22:37:07Z"
      }
    },
    {
      "repo": "zai-org/CogVideo",
      "description": "text and image to video generation: CogVideoX (2024) and CogVideo (ICLR 2023)",
      "language": "Python",
      "github": {
        "stars": 13067,
        "forks": 1365,
        "openIssues": 115,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-11-04T11:19:04Z"
      }
    },
    {
      "repo": "Wan-Video/Wan2.1",
      "description": "Wan: Open and Advanced Large-Scale Video Generative Models",
      "language": "Python",
      "github": {
        "stars": 17122,
        "forks": 3727,
        "openIssues": 386,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-03-05T09:38:07Z"
      }
    },
    {
      "repo": "huggingface/diffusers",
      "description": "🤗 Diffusers: State-of-the-art diffusion models for image, video, and audio generation in PyTorch.",
      "language": "Python",
      "github": {
        "stars": 34695,
        "forks": 7380,
        "openIssues": 1476,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T14:42:43Z"
      }
    },
    {
      "repo": "LaurieWired/GhidraMCP",
      "description": "MCP Server for Ghidra",
      "language": "Java",
      "github": {
        "stars": 10728,
        "forks": 1108,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-06-23T04:18:18Z"
      }
    },
    {
      "repo": "undefined-ui/second-brain-os",
      "description": "An AI second brain that maintains itself. Full guide, starter vault, agent skills and scripts for a self-organizing knowledge base in Claude Code and Obsidian.",
      "language": "HTML",
      "github": {
        "stars": 1017,
        "forks": 163,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-07T19:16:09Z"
      }
    },
    {
      "repo": "gh1mau/masta-cve-2026-48907",
      "description": "cve-2026-48907 scanner",
      "language": "Python",
      "github": {
        "stars": 64,
        "forks": 12,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-06-27T05:25:46Z"
      }
    },
    {
      "repo": "JustExecution/HTF_indicator",
      "description": "Designed for traders who rely on multi-timeframe analysis and ICT/Smart Money concepts, HTF SUITE provides institutional market context without requiring multiple indicators.",
      "language": null,
      "github": {
        "stars": 122,
        "forks": 46,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-17T06:36:15Z"
      }
    },
    {
      "repo": "boykopovar/AnyPS5",
      "description": "Tool for automatic PS5 executables porting to Linux and Windows",
      "language": "C++",
      "github": {
        "stars": 15910,
        "forks": 1256,
        "openIssues": 554,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T22:46:53Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-5.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "LuxAlgo/PineTS",
      "description": "Run Pine Script® anywhere. PineTS is an open-source transpiler and runtime that brings Pine Script® logic to Node.js and the browser with 1:1 syntax compatibility. Reliably write, port, and run indicators or strategies on your own infrastructure.",
      "language": "TypeScript",
      "github": {
        "stars": 848,
        "forks": 193,
        "openIssues": 68,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T22:50:47Z"
      }
    },
    {
      "repo": "XHToken/Spark-X2.5",
      "description": "Spark-x2.5 open model series. Pushing the Limits of Agentic Capabilities in On-Device Models",
      "language": null,
      "github": {
        "stars": 682,
        "forks": 87,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T08:13:26Z"
      }
    },
    {
      "repo": "smicallef/spiderfoot",
      "description": "SpiderFoot automates OSINT for threat intelligence and mapping your attack surface.",
      "language": "Python",
      "github": {
        "stars": 23193,
        "forks": 3715,
        "openIssues": 329,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-04-13T19:43:06Z"
      }
    },
    {
      "repo": "MISP/MISP",
      "description": "MISP (core software) - Open Source Threat Intelligence and Sharing Platform",
      "language": "PHP",
      "github": {
        "stars": 6583,
        "forks": 1646,
        "openIssues": 2947,
        "archived": false,
        "disabled": false,
        "defaultBranch": "2.5",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-07T19:03:27Z"
      }
    },
    {
      "repo": "mitre-attack/attack-stix-data",
      "description": "STIX data representing MITRE ATT&CK",
      "language": "Python",
      "github": {
        "stars": 690,
        "forks": 147,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-05T22:57:21Z"
      }
    },
    {
      "repo": "OISF/suricata",
      "description": "Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine developed by the OISF and the Suricata community.",
      "language": "C",
      "github": {
        "stars": 6714,
        "forks": 1780,
        "openIssues": 91,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T15:31:08Z"
      }
    },
    {
      "repo": "zeek/zeek",
      "description": "Zeek is a powerful network analysis framework that is much different from the typical IDS you may know.",
      "language": "C++",
      "github": {
        "stars": 8084,
        "forks": 1433,
        "openIssues": 260,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T21:42:41Z"
      }
    },
    {
      "repo": "VirusTotal/yara",
      "description": "The pattern matching swiss knife",
      "language": "C",
      "github": {
        "stars": 9931,
        "forks": 1586,
        "openIssues": 169,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-23T09:48:49Z"
      }
    },
    {
      "repo": "SigmaHQ/sigma",
      "description": "Main Sigma Rule Repository",
      "language": "Python",
      "github": {
        "stars": 11192,
        "forks": 2839,
        "openIssues": 254,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-06T11:26:20Z"
      }
    },
    {
      "repo": "iamlukethedev/Herald-OS",
      "description": "An agent-native operating system, with Hermes Agent as the interface. Independent project, not affiliated with Nous Research.",
      "language": "TypeScript",
      "github": {
        "stars": 266,
        "forks": 37,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:11:58Z"
      }
    },
    {
      "repo": "openai/math",
      "description": null,
      "language": "Lean",
      "github": {
        "stars": 12136,
        "forks": 1263,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T05:20:00Z"
      }
    },
    {
      "repo": "Quincunx33/Ai-jailbreak",
      "description": "A collection of jailbreak prompts and exploit techniques for local and frontier AI models, with modern methods for Qwen3.5, Gemma 4, Llama 4, Kimi K3, GPT-OSS, GPT-5.x, Gemini 3.x and Grok 4.x. For red-teaming and AI safety research only.",
      "language": "JavaScript",
      "github": {
        "stars": 383,
        "forks": 68,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T14:59:44Z"
      }
    },
    {
      "repo": "fxraptor-alpha/pinescript-indicators",
      "description": "This repository consists of different trading model pine script indicators.",
      "language": null,
      "github": {
        "stars": 111,
        "forks": 42,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-06T11:42:04Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-6.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "cantolab/open-source-fractal",
      "description": "Open Source Fractal Indicator by CantoLab",
      "language": null,
      "github": {
        "stars": 173,
        "forks": 58,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-25T21:23:05Z"
      }
    },
    {
      "repo": "ict2023trader/Indicators",
      "description": null,
      "language": null,
      "github": {
        "stars": 60,
        "forks": 28,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T18:52:49Z"
      }
    },
    {
      "repo": "modal-labs/modal-examples",
      "description": "Examples of programs built using Modal",
      "language": "Python",
      "github": {
        "stars": 1276,
        "forks": 322,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:06:11Z"
      }
    },
    {
      "repo": "taskflow/taskflow",
      "description": "A General-purpose Task-parallel Programming System in C++",
      "language": "C++",
      "github": {
        "stars": 12198,
        "forks": 1413,
        "openIssues": 41,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-28T18:41:31Z"
      }
    },
    {
      "repo": "ray-project/ray",
      "description": "Ray is an AI compute engine. Ray consists of a core distributed runtime and a set of AI Libraries for accelerating ML workloads.",
      "language": "Python",
      "github": {
        "stars": 43993,
        "forks": 8121,
        "openIssues": 3556,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:23:55Z"
      }
    },
    {
      "repo": "justcallmekoko/ESP32Marauder",
      "description": "A suite of WiFi/Bluetooth offensive and defensive tools for the ESP32",
      "language": "C++",
      "github": {
        "stars": 12650,
        "forks": 1523,
        "openIssues": 332,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-10-08T22:09:49Z"
      }
    },
    {
      "repo": "trufflesecurity/trufflehog",
      "description": "Find, verify, and analyze leaked credentials",
      "language": "Go",
      "github": {
        "stars": 28369,
        "forks": 2623,
        "openIssues": 560,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T17:28:48Z"
      }
    },
    {
      "repo": "mitmproxy/mitmproxy",
      "description": "An interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers.",
      "language": "Python",
      "github": {
        "stars": 45349,
        "forks": 4774,
        "openIssues": 490,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T22:18:35Z"
      }
    },
    {
      "repo": "apache/tika",
      "description": "The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types (such as PPT, XLS, and PDF).",
      "language": "Java",
      "github": {
        "stars": 4090,
        "forks": 1005,
        "openIssues": 58,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:08:29Z"
      }
    },
    {
      "repo": "jina-ai/reader",
      "description": "Convert any URL to an LLM-friendly input with a simple prefix https://r.jina.ai/",
      "language": "TypeScript",
      "github": {
        "stars": 12127,
        "forks": 892,
        "openIssues": 34,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-05-22T02:56:46Z"
      }
    },
    {
      "repo": "datalab-to/marker",
      "description": "Convert PDF to markdown + JSON quickly with high accuracy",
      "language": "Python",
      "github": {
        "stars": 40292,
        "forks": 2913,
        "openIssues": 477,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T09:53:02Z"
      }
    },
    {
      "repo": "Unstructured-IO/unstructured",
      "description": "Convert documents to structured data effortlessly. Unstructured is open-source ETL solution for transforming complex documents into clean, structured formats for language models.  Visit our website to learn more about our enterprise grade Platform product for production grade workflows, partitioning, enrichments, chunking and embedding.",
      "language": "HTML",
      "github": {
        "stars": 15549,
        "forks": 1351,
        "openIssues": 336,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T00:03:37Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2-metadata-7.json
````json
{
  "capturedAt": "2026-10-09",
  "source": "GitHub REST API",
  "repositories": [
    {
      "repo": "rbrus/laya-as-judge",
      "description": "JEV's alike open-source alternative Laya-MLX used as a \"LLM-as-a-judge\"",
      "language": "Python",
      "github": {
        "stars": 17,
        "forks": 1,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-26T08:15:03Z"
      }
    },
    {
      "repo": "github/github-mcp-server",
      "description": "GitHub's official MCP Server",
      "language": "Go",
      "github": {
        "stars": 33454,
        "forks": 5111,
        "openIssues": 346,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T16:25:41Z"
      }
    },
    {
      "repo": "oraios/serena",
      "description": "A powerful MCP toolkit for coding, providing semantic retrieval and editing capabilities  - the IDE for your agent",
      "language": "Python",
      "github": {
        "stars": 30109,
        "forks": 2049,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T22:37:55Z"
      }
    },
    {
      "repo": "emilk/egui",
      "description": "egui: an easy-to-use immediate mode GUI in Rust that runs on both web and native",
      "language": "Rust",
      "github": {
        "stars": 31045,
        "forks": 2173,
        "openIssues": 1033,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T15:38:15Z"
      }
    },
    {
      "repo": "liquidslr/system-design-notes",
      "description": "Notes of the book System Desgin Interview - An Insider's Guide",
      "language": null,
      "github": {
        "stars": 24645,
        "forks": 4603,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-08-12T22:22:21Z"
      }
    },
    {
      "repo": "storytold/artcraft",
      "description": "ArtCraft is an intentional crafting engine for artists, designers, and filmmakers",
      "language": "Rust",
      "github": {
        "stars": 8048,
        "forks": 1135,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-07T00:56:15Z"
      }
    },
    {
      "repo": "EpicGames/raddebugger",
      "description": "A native, user-mode, multi-process, graphical debugger.",
      "language": "C",
      "github": {
        "stars": 8121,
        "forks": 391,
        "openIssues": 316,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-07T20:56:17Z"
      }
    },
    {
      "repo": "OpenByteInc/QuantDinger",
      "description": "Open-source AI Trading OS, agent trading, and vibe trading, with Jev System One integration. Research, build Python strategies, backtest, and paper/live trade across crypto, stocks, and forex. Launch your own multi-tenant trading SaaS with built-in user management, billing, payments, and settlement.",
      "language": "Python",
      "github": {
        "stars": 12566,
        "forks": 2547,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T21:14:39Z"
      }
    },
    {
      "repo": "go-gitea/gitea",
      "description": "Git with a cup of tea! Painless self-hosted all-in-one software development service, including Git hosting, code review, team collaboration, package registry and CI/CD",
      "language": "Go",
      "github": {
        "stars": 58373,
        "forks": 7234,
        "openIssues": 2347,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:15:36Z"
      }
    },
    {
      "repo": "reviewdog/reviewdog",
      "description": "🐶 Automated code review tool integrated with any code analysis tools regardless of programming language",
      "language": "Go",
      "github": {
        "stars": 9649,
        "forks": 503,
        "openIssues": 131,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:26:07Z"
      }
    },
    {
      "repo": "kargulstudio/sales-crm",
      "description": null,
      "language": "TypeScript",
      "github": {
        "stars": 1658,
        "forks": 360,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-06T06:42:03Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-2.json
````json
{
  "date": "2026-10-09",
  "source": "GitHub Stars screenshots (9), batch 2",
  "summary": {
    "raw": 95,
    "unique": 95,
    "alreadyInCatalog": 9,
    "newlyAdmitted": 86,
    "catalogBefore": 435,
    "catalogAfter": 521
  },
  "admitted": [
    "1N3/Sn1per",
    "aarora4/Awesome-Prediction-Market-Tools",
    "AILab-CVC/VideoCrafter",
    "apache/tika",
    "boykopovar/AnyPS5",
    "caddyserver/caddy",
    "caiovicentino/polymarket-mcp-server",
    "cantolab/open-source-fractal",
    "cloudflare/cloudflare-os",
    "ComposioHQ/composio",
    "datalab-to/marker",
    "deepseek-ai/DeepGEMM",
    "Diolinux/PhotoGIMP",
    "DuarteSantos8/openGym",
    "earthtojake/text-to-cad",
    "elder-plinius/T3MP3ST",
    "emilk/egui",
    "ent0n29/polybot",
    "EpicGames/raddebugger",
    "evan-kolberg/prediction-market-backtesting",
    "fxraptor-alpha/pinescript-indicators",
    "genmoai/mochi",
    "gh1mau/masta-cve-2026-48907",
    "github/github-mcp-server",
    "go-gitea/gitea",
    "google-deepmind/mujoco",
    "guoyww/AnimateDiff",
    "huggingface/diffusers",
    "huggingface/lerobot",
    "iamlukethedev/Herald-OS",
    "ict2023trader/Indicators",
    "isaac-sim/IsaacLab",
    "jina-ai/reader",
    "justcallmekoko/ESP32Marauder",
    "JustExecution/HTF_indicator",
    "kargulstudio/sales-crm",
    "LaurieWired/GhidraMCP",
    "lfnovo/esperanto",
    "lfnovo/open-notebook",
    "Lightricks/LTX-Video",
    "liquidslr/system-design-notes",
    "localsend/localsend",
    "LuxAlgo/PineTS",
    "mastra-ai/mastra",
    "meituan-longcat/LongCat-Video",
    "michael-denyer/pstack-claude",
    "MISP/MISP",
    "mitmproxy/mitmproxy",
    "mitre-attack/attack-stix-data",
    "modal-labs/modal-examples",
    "morluto/rea",
    "OISF/suricata",
    "open-rmf/rmf",
    "openai/math",
    "OpenByteInc/QuantDinger",
    "OpenCut-app/OpenCut",
    "openvla/openvla",
    "oraios/serena",
    "osquery/osquery",
    "pingdotgg/t3code",
    "Quincunx33/Ai-jailbreak",
    "rawfilejson/awesome-osint-arsenal",
    "ray-project/ray",
    "rbrus/laya-as-judge",
    "rehan-remade/universal-modder",
    "reviewdog/reviewdog",
    "RickdeJager/stegseek",
    "ros2/ros2",
    "SigmaHQ/sigma",
    "SII-WANGZJ/Polymarket_data",
    "smicallef/spiderfoot",
    "storytold/artcraft",
    "Stremio/stremio-web",
    "taskflow/taskflow",
    "tester-army/e2e",
    "topoteretes/cognee",
    "trufflesecurity/trufflehog",
    "undefined-ui/second-brain-os",
    "Unstructured-IO/unstructured",
    "Velocidex/velociraptor",
    "VirusTotal/yara",
    "Wan-Video/Wan2.1",
    "XHToken/Spark-X2.5",
    "yangyuan-zhen/PolyWeather",
    "zai-org/CogVideo",
    "zeek/zeek"
  ],
  "metadataFiles": [
    "reports/star-import-2026-10-09-batch-2-metadata-1.json",
    "reports/star-import-2026-10-09-batch-2-metadata-2.json",
    "reports/star-import-2026-10-09-batch-2-metadata-3.json",
    "reports/star-import-2026-10-09-batch-2-metadata-4.json",
    "reports/star-import-2026-10-09-batch-2-metadata-5.json",
    "reports/star-import-2026-10-09-batch-2-metadata-6.json",
    "reports/star-import-2026-10-09-batch-2-metadata-7.json"
  ],
  "manualCorrections": [
    {
      "from": "karqulstudio/sales-crm",
      "to": "kargulstudio/sales-crm"
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-3-metadata-1.json
````json
{
  "source": "GitHub REST repository metadata for user screenshot batch 3",
  "retrievedAt": "2026-10-09",
  "repositories": [
    {
      "repo": "metabase/metabase",
      "description": "The easy-to-use open source Business Intelligence and Embedded Analytics tool that lets everyone work with data :bar_chart:",
      "language": "Clojure",
      "github": {
        "stars": 49584,
        "forks": 6889,
        "openIssues": 4560,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:34:57Z"
      }
    },
    {
      "repo": "evidence-dev/evidence",
      "description": "Business intelligence as code: build fast, interactive data visualizations in SQL and markdown",
      "language": "TypeScript",
      "github": {
        "stars": 6989,
        "forks": 428,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T19:49:20Z"
      }
    },
    {
      "repo": "sinaptik-ai/pandas-ai",
      "description": "Chat with your database or your datalake (SQL, CSV, parquet). PandasAI makes data analysis conversational using LLMs and RAG.",
      "language": "Python",
      "github": {
        "stars": 23860,
        "forks": 2342,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2025-10-28T10:02:13Z"
      }
    },
    {
      "repo": "apache/datafusion",
      "description": "Apache DataFusion SQL Query Engine",
      "language": "Rust",
      "github": {
        "stars": 9417,
        "forks": 2482,
        "openIssues": 2374,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T02:59:07Z"
      }
    },
    {
      "repo": "pola-rs/polars",
      "description": "Extremely fast Query Engine for DataFrames, written in Rust",
      "language": "Rust",
      "github": {
        "stars": 40021,
        "forks": 3158,
        "openIssues": 2956,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T14:41:35Z"
      }
    },
    {
      "repo": "duckdb/duckdb",
      "description": "DuckDB is an analytical in-process SQL database management system",
      "language": "C++",
      "github": {
        "stars": 41995,
        "forks": 3887,
        "openIssues": 1066,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v2.0-cyanoptera",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:00:14Z"
      }
    },
    {
      "repo": "eosphoros-ai/DB-GPT",
      "description": "open-source agentic AI data assistant for the next generation of AI + Data products.",
      "language": "Python",
      "github": {
        "stars": 20093,
        "forks": 2958,
        "openIssues": 450,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T13:43:25Z"
      }
    },
    {
      "repo": "yifanfeng97/Hyper-Extract",
      "description": "Hypergraph is more powerful. Transform unstructured text into structured knowledge with LLMs. Graphs, hypergraphs, and spatio-temporal extractions — with one command.",
      "language": "Python",
      "github": {
        "stars": 4142,
        "forks": 473,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-29T13:33:32Z"
      }
    },
    {
      "repo": "Jakeschincariol/arena-skill",
      "description": "When Claude keeps giving you bad answers, make 100 versions of it fight to the death. Same task, 100 different strategies, a bracket, one answer left. Free Claude Code skill.",
      "language": "Python",
      "github": {
        "stars": 374,
        "forks": 52,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T13:20:07Z"
      }
    },
    {
      "repo": "quarto-dev/quarto-cli",
      "description": "Open-source scientific and technical publishing system built on Pandoc.",
      "language": "JavaScript",
      "github": {
        "stars": 6065,
        "forks": 464,
        "openIssues": 1896,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T16:35:35Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-3-metadata-2.json
````json
{
  "source": "GitHub REST repository metadata for user screenshot batch 3",
  "retrievedAt": "2026-10-09",
  "repositories": [
    {
      "repo": "apache/superset",
      "description": "Apache Superset is a Data Visualization and Data Exploration Platform",
      "language": "Python",
      "github": {
        "stars": 75082,
        "forks": 18439,
        "openIssues": 568,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:19:45Z"
      }
    },
    {
      "repo": "Kanaries/pygwalker",
      "description": "PyGWalker: Turn your dataframe into an interactive UI for visual analysis",
      "language": "Python",
      "github": {
        "stars": 15979,
        "forks": 890,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-05T19:19:19Z"
      }
    },
    {
      "repo": "Dataherald/dataherald",
      "description": "Interact with your SQL database, Natural Language to SQL using LLMs",
      "language": "Python",
      "github": {
        "stars": 3649,
        "forks": 263,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-07-24T17:37:41Z"
      }
    },
    {
      "repo": "open-metadata/OpenMetadata",
      "description": "The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building trusted data context and business semantics for humans, AI assistants, and agents.",
      "language": "TypeScript",
      "github": {
        "stars": 15420,
        "forks": 2436,
        "openIssues": 957,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:07:08Z"
      }
    },
    {
      "repo": "sodadata/soda-core",
      "description": "Data Contracts engine for the modern data stack. https://www.soda.io",
      "language": "Python",
      "github": {
        "stars": 2435,
        "forks": 288,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T20:50:19Z"
      }
    },
    {
      "repo": "fivetran/great_expectations",
      "description": "Always know what to expect from your data.",
      "language": "Python",
      "github": {
        "stars": 11867,
        "forks": 1871,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T09:28:46Z"
      }
    },
    {
      "repo": "dlt-hub/dlt",
      "description": "data load tool (dlt) is an open source Python library that makes data loading easy 🛠️ ",
      "language": "Python",
      "github": {
        "stars": 5945,
        "forks": 618,
        "openIssues": 454,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T16:24:37Z"
      }
    },
    {
      "repo": "airbytehq/airbyte",
      "description": "Open-source data movement for ELT pipelines and AI agents — from APIs, databases & files to warehouses, lakes, and AI applications. Both self-hosted and Cloud.",
      "language": "Python",
      "github": {
        "stars": 22194,
        "forks": 5393,
        "openIssues": 2583,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:29:22Z"
      }
    },
    {
      "repo": "defog-ai/sqlcoder",
      "description": "SoTA LLM for converting natural language questions to SQL queries",
      "language": "Jupyter Notebook",
      "github": {
        "stars": 4049,
        "forks": 272,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-05-23T03:06:26Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-3-reviewed.json
````json
{
  "date": "2026-10-09",
  "source": "GitHub API snapshots + selected screenshot import; review applies to catalog admission, not a grant of reuse rights",
  "repositories": [
    {
      "repo": "airbytehq/airbyte",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 22194,
        "forks": 5393,
        "openIssues": 2583,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:29:22Z"
      },
      "catalogEntry": {
        "repo": "airbytehq/airbyte",
        "score": 7.8,
        "tier": "audit",
        "category": "Synchronisation de sources de données",
        "domain": "data_ml",
        "capabilities": [
          "elt",
          "connectors",
          "data-ingestion"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "server"
        ],
        "resourceLevel": "high",
        "integrationComplexity": "high",
        "costModel": "mixed",
        "github": {
          "stars": 22194,
          "forks": 5393,
          "openIssues": 2583,
          "archived": false,
          "disabled": false,
          "defaultBranch": "master",
          "license": "NOASSERTION",
          "pushedAt": "2026-10-09T02:29:22Z"
        },
        "bestFor": [
          "Synchroniser des bases, fichiers et API vers des entrepôts et outils IA"
        ],
        "avoidWhen": [
          "Supposer que toutes les fonctionnalités et licences Cloud sont ouvertes"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "apache/datafusion",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 9417,
        "forks": 2482,
        "openIssues": 2374,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T02:59:07Z"
      },
      "catalogEntry": {
        "repo": "apache/datafusion",
        "score": 8.6,
        "tier": "specialized",
        "category": "Moteur SQL analytique embarquable",
        "domain": "data_ml",
        "capabilities": [
          "sql",
          "query-engine",
          "rust"
        ],
        "languages": [
          "rust"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "high",
        "costModel": "open-source",
        "github": {
          "stars": 9417,
          "forks": 2482,
          "openIssues": 2374,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "Apache-2.0",
          "pushedAt": "2026-10-09T02:59:07Z"
        },
        "bestFor": [
          "Intégrer un moteur de requêtes analytiques rapide en Rust"
        ],
        "avoidWhen": [
          "Rechercher une interface graphique de BI prête à utiliser"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "apache/superset",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 75082,
        "forks": 18439,
        "openIssues": 568,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:19:45Z"
      },
      "catalogEntry": {
        "repo": "apache/superset",
        "score": 8.6,
        "tier": "specialized",
        "category": "Exploration et visualisation SQL",
        "domain": "data_ml",
        "capabilities": [
          "dashboards",
          "sql",
          "data-visualization"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "server"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "high",
        "costModel": "open-source",
        "github": {
          "stars": 75082,
          "forks": 18439,
          "openIssues": 568,
          "archived": false,
          "disabled": false,
          "defaultBranch": "master",
          "license": "Apache-2.0",
          "pushedAt": "2026-10-09T03:19:45Z"
        },
        "bestFor": [
          "Créer des graphiques, rapports et tableaux de bord sur des sources SQL"
        ],
        "avoidWhen": [
          "Besoin d'une bibliothèque embarquée légère côté navigateur uniquement"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "Dataherald/dataherald",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 3649,
        "forks": 263,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-07-24T17:37:41Z"
      },
      "catalogEntry": {
        "repo": "Dataherald/dataherald",
        "score": 7.5,
        "tier": "audit",
        "category": "Génération de requêtes SQL par IA",
        "domain": "data_ml",
        "capabilities": [
          "nl-to-sql",
          "llm",
          "sql"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 3649,
          "forks": 263,
          "openIssues": 21,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "Apache-2.0",
          "pushedAt": "2024-07-24T17:37:41Z"
        },
        "bestFor": [
          "Expérimenter l'interrogation de bases SQL par langage naturel"
        ],
        "avoidWhen": [
          "Production sans audit de sécurité SQL ni contrôle de maintenance"
        ],
        "guidanceSource": "curated",
        "lifecycle": "reference"
      }
    },
    {
      "repo": "defog-ai/sqlcoder",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 4049,
        "forks": 272,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-05-23T03:06:26Z"
      },
      "catalogEntry": {
        "repo": "defog-ai/sqlcoder",
        "score": 7.4,
        "tier": "audit",
        "category": "Modèle de génération SQL",
        "domain": "data_ml",
        "capabilities": [
          "nl-to-sql",
          "llm",
          "text-to-sql"
        ],
        "languages": [
          "jupyter notebook"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "high",
        "integrationComplexity": "high",
        "costModel": "open-source",
        "github": {
          "stars": 4049,
          "forks": 272,
          "openIssues": 0,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "Apache-2.0",
          "pushedAt": "2024-05-23T03:06:26Z"
        },
        "bestFor": [
          "Évaluer des modèles de génération de SQL depuis le langage naturel"
        ],
        "avoidWhen": [
          "Déployer des requêtes générées sur une base réelle sans revue ni garde-fous"
        ],
        "guidanceSource": "curated",
        "lifecycle": "reference"
      }
    },
    {
      "repo": "dlt-hub/dlt",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 5945,
        "forks": 618,
        "openIssues": 454,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T16:24:37Z"
      },
      "catalogEntry": {
        "repo": "dlt-hub/dlt",
        "score": 8.5,
        "tier": "specialized",
        "category": "Ingestion de données Python",
        "domain": "data_ml",
        "capabilities": [
          "elt",
          "data-ingestion",
          "pipelines"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "low",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 5945,
          "forks": 618,
          "openIssues": 454,
          "archived": false,
          "disabled": false,
          "defaultBranch": "devel",
          "license": "Apache-2.0",
          "pushedAt": "2026-10-08T16:24:37Z"
        },
        "bestFor": [
          "Charger et normaliser des données API ou fichiers dans un entrepôt"
        ],
        "avoidWhen": [
          "Orchestration complexe non couverte sans outil complémentaire"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "duckdb/duckdb",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 41995,
        "forks": 3887,
        "openIssues": 1066,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v2.0-cyanoptera",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:00:14Z"
      },
      "catalogEntry": {
        "repo": "duckdb/duckdb",
        "score": 8.8,
        "tier": "specialized",
        "category": "Base SQL analytique embarquée",
        "domain": "data_ml",
        "capabilities": [
          "database",
          "sql",
          "analytics"
        ],
        "languages": [
          "c++"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "low",
        "integrationComplexity": "low",
        "costModel": "open-source",
        "github": {
          "stars": 41995,
          "forks": 3887,
          "openIssues": 1066,
          "archived": false,
          "disabled": false,
          "defaultBranch": "v2.0-cyanoptera",
          "license": "MIT",
          "pushedAt": "2026-10-09T00:00:14Z"
        },
        "bestFor": [
          "Exécuter des analyses SQL locales et sur des fichiers Parquet ou CSV"
        ],
        "avoidWhen": [
          "Héberger une base OLTP multi-utilisateurs avec beaucoup d'écritures concurrentes"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "eosphoros-ai/DB-GPT",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 20093,
        "forks": 2958,
        "openIssues": 450,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T13:43:25Z"
      },
      "catalogEntry": {
        "repo": "eosphoros-ai/DB-GPT",
        "score": 8.3,
        "tier": "specialized",
        "category": "Assistant IA pour bases de données",
        "domain": "data_ml",
        "capabilities": [
          "database",
          "llm",
          "nl-to-sql",
          "agents"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "high",
        "integrationComplexity": "high",
        "costModel": "open-source",
        "github": {
          "stars": 20093,
          "forks": 2958,
          "openIssues": 450,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "MIT",
          "pushedAt": "2026-10-04T13:43:25Z"
        },
        "bestFor": [
          "Construire un assistant de données capable de raisonner et interroger des bases SQL"
        ],
        "avoidWhen": [
          "Permettre à un LLM d'exécuter des requêtes non contrôlées sur une base de production"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "evidence-dev/evidence",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 6989,
        "forks": 428,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T19:49:20Z"
      },
      "catalogEntry": {
        "repo": "evidence-dev/evidence",
        "score": 8.4,
        "tier": "specialized",
        "category": "BI as code",
        "domain": "data_ml",
        "capabilities": [
          "business-intelligence",
          "dashboards",
          "sql",
          "markdown"
        ],
        "languages": [
          "typescript"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "low",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 6989,
          "forks": 428,
          "openIssues": 15,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "MIT",
          "pushedAt": "2026-10-08T19:49:20Z"
        },
        "bestFor": [
          "Construire des tableaux de bord versionnés à partir de SQL et Markdown"
        ],
        "avoidWhen": [
          "Exiger une interface BI entièrement sans code"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "fivetran/great_expectations",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 11867,
        "forks": 1871,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T09:28:46Z"
      },
      "catalogEntry": {
        "repo": "fivetran/great_expectations",
        "score": 8.5,
        "tier": "specialized",
        "category": "Tests de qualité des données",
        "domain": "data_ml",
        "capabilities": [
          "data-quality",
          "validation",
          "testing"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 11867,
          "forks": 1871,
          "openIssues": 47,
          "archived": false,
          "disabled": false,
          "defaultBranch": "develop",
          "license": "Apache-2.0",
          "pushedAt": "2026-10-08T09:28:46Z"
        },
        "bestFor": [
          "Définir et exécuter des assertions sur les jeux de données et les pipelines"
        ],
        "avoidWhen": [
          "Substituer des assertions aux validations métier ou statistiques"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "Jakeschincariol/arena-skill",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 374,
        "forks": 52,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T13:20:07Z"
      },
      "catalogEntry": {
        "repo": "Jakeschincariol/arena-skill",
        "score": 8,
        "tier": "specialized",
        "category": "Évaluation comparative d'agents IA",
        "domain": "ai_agents",
        "capabilities": [
          "agent-evaluation",
          "planning",
          "benchmarking"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": "partial",
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 374,
          "forks": 52,
          "openIssues": 3,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "MIT",
          "pushedAt": "2026-09-27T13:20:07Z"
        },
        "bestFor": [
          "Comparer plusieurs stratégies de résolution par agents sur une même tâche"
        ],
        "avoidWhen": [
          "Consommer des appels LLM coûteux sans budget et critères de jugement"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "Kanaries/pygwalker",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 15979,
        "forks": 890,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-05T19:19:19Z"
      },
      "catalogEntry": {
        "repo": "Kanaries/pygwalker",
        "score": 8.4,
        "tier": "specialized",
        "category": "Visualisation interactive de DataFrames",
        "domain": "data_ml",
        "capabilities": [
          "data-visualization",
          "dataframes",
          "exploration"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "low",
        "costModel": "open-source",
        "github": {
          "stars": 15979,
          "forks": 890,
          "openIssues": 69,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "Apache-2.0",
          "pushedAt": "2026-09-05T19:19:19Z"
        },
        "bestFor": [
          "Explorer visuellement des tableaux Python dans une interface interactive"
        ],
        "avoidWhen": [
          "Recherche exclusive de visualisations statiques pour un pipeline headless"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "metabase/metabase",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 49584,
        "forks": 6889,
        "openIssues": 4560,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:34:57Z"
      },
      "catalogEntry": {
        "repo": "metabase/metabase",
        "score": 7.7,
        "tier": "audit",
        "category": "BI et tableaux de bord",
        "domain": "data_ml",
        "capabilities": [
          "business-intelligence",
          "dashboards",
          "sql"
        ],
        "languages": [
          "clojure"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "server"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "high",
        "costModel": "mixed",
        "github": {
          "stars": 49584,
          "forks": 6889,
          "openIssues": 4560,
          "archived": false,
          "disabled": false,
          "defaultBranch": "master",
          "license": "NOASSERTION",
          "pushedAt": "2026-10-09T02:34:57Z"
        },
        "bestFor": [
          "Mettre à disposition des tableaux de bord métier et des analyses SQL"
        ],
        "avoidWhen": [
          "Réutiliser le code sans examiner les licences communautaires et commerciales"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "open-metadata/OpenMetadata",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 15420,
        "forks": 2436,
        "openIssues": 957,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:07:08Z"
      },
      "catalogEntry": {
        "repo": "open-metadata/OpenMetadata",
        "score": 8.6,
        "tier": "specialized",
        "category": "Catalogue et gouvernance de données",
        "domain": "data_ml",
        "capabilities": [
          "data-catalog",
          "governance",
          "metadata"
        ],
        "languages": [
          "typescript"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "server"
        ],
        "resourceLevel": "high",
        "integrationComplexity": "high",
        "costModel": "open-source",
        "github": {
          "stars": 15420,
          "forks": 2436,
          "openIssues": 957,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "Apache-2.0",
          "pushedAt": "2026-10-09T03:07:08Z"
        },
        "bestFor": [
          "Inventorier les actifs de données, lignages et règles de gouvernance"
        ],
        "avoidWhen": [
          "Déploiement d'une plateforme lourde pour quelques fichiers locaux"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "pola-rs/polars",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 40021,
        "forks": 3158,
        "openIssues": 2956,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T14:41:35Z"
      },
      "catalogEntry": {
        "repo": "pola-rs/polars",
        "score": 8.8,
        "tier": "specialized",
        "category": "Analyse de DataFrames hautes performances",
        "domain": "data_ml",
        "capabilities": [
          "dataframes",
          "sql",
          "performance"
        ],
        "languages": [
          "rust"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "open-source",
        "github": {
          "stars": 40021,
          "forks": 3158,
          "openIssues": 2956,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "MIT",
          "pushedAt": "2026-10-08T14:41:35Z"
        },
        "bestFor": [
          "Transformer et analyser des tables volumineuses avec un moteur DataFrame rapide"
        ],
        "avoidWhen": [
          "Avoir besoin uniquement de requêtes SQL simples sans traitement tabulaire"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "quarto-dev/quarto-cli",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 6065,
        "forks": 464,
        "openIssues": 1896,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T16:35:35Z"
      },
      "catalogEntry": {
        "repo": "quarto-dev/quarto-cli",
        "score": 7.8,
        "tier": "audit",
        "category": "Publication scientifique reproductible",
        "domain": "productivity",
        "capabilities": [
          "documentation",
          "publishing",
          "markdown"
        ],
        "languages": [
          "javascript"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "low",
        "integrationComplexity": "medium",
        "costModel": "unknown",
        "github": {
          "stars": 6065,
          "forks": 464,
          "openIssues": 1896,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "NOASSERTION",
          "pushedAt": "2026-10-08T16:35:35Z"
        },
        "bestFor": [
          "Publier des rapports techniques, notebooks et documents reproductibles"
        ],
        "avoidWhen": [
          "Réutiliser des composants sans vérification de leur licence exacte"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "sinaptik-ai/pandas-ai",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 23860,
        "forks": 2342,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2025-10-28T10:02:13Z"
      },
      "catalogEntry": {
        "repo": "sinaptik-ai/pandas-ai",
        "score": 7.5,
        "tier": "audit",
        "category": "Analyse de données en langage naturel",
        "domain": "data_ml",
        "capabilities": [
          "nl-to-sql",
          "llm",
          "dataframes"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": "partial",
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
        "costModel": "unknown",
        "github": {
          "stars": 23860,
          "forks": 2342,
          "openIssues": 23,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "NOASSERTION",
          "pushedAt": "2025-10-28T10:02:13Z"
        },
        "bestFor": [
          "Explorer des données SQL, CSV ou Parquet avec des requêtes conversationnelles"
        ],
        "avoidWhen": [
          "Fournir un accès non contrôlé à des données personnelles ou confidentielles"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "sodadata/soda-core",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 2435,
        "forks": 288,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T20:50:19Z"
      },
      "catalogEntry": {
        "repo": "sodadata/soda-core",
        "score": 7.6,
        "tier": "audit",
        "category": "Contrats et qualité des données",
        "domain": "data_ml",
        "capabilities": [
          "data-quality",
          "validation",
          "data-contracts"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "low",
        "integrationComplexity": "medium",
        "costModel": "unknown",
        "github": {
          "stars": 2435,
          "forks": 288,
          "openIssues": 211,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "NOASSERTION",
          "pushedAt": "2026-10-08T20:50:19Z"
        },
        "bestFor": [
          "Contrôler la qualité des données et les contrats des pipelines"
        ],
        "avoidWhen": [
          "Réutiliser des composants sous licence incertaine sans vérification"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    },
    {
      "repo": "yifanfeng97/Hyper-Extract",
      "reviewed": true,
      "reviewScope": "identity, metadata and conservative catalog admission; unresolved license retained as audit",
      "github": {
        "stars": 4142,
        "forks": 473,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-29T13:33:32Z"
      },
      "catalogEntry": {
        "repo": "yifanfeng97/Hyper-Extract",
        "score": 7.4,
        "tier": "audit",
        "category": "Extraction de connaissances structurées",
        "domain": "data_ml",
        "capabilities": [
          "knowledge-extraction",
          "llm",
          "knowledge-graph"
        ],
        "languages": [
          "python"
        ],
        "platforms": [
          "cross-platform"
        ],
        "selfHosted": true,
        "runtime": [
          "local"
        ],
        "resourceLevel": "medium",
        "integrationComplexity": "high",
        "costModel": "unknown",
        "github": {
          "stars": 4142,
          "forks": 473,
          "openIssues": 5,
          "archived": false,
          "disabled": false,
          "defaultBranch": "main",
          "license": "NOASSERTION",
          "pushedAt": "2026-09-29T13:33:32Z"
        },
        "bestFor": [
          "Transformer des documents non structurés en graphes et hypergraphes de connaissances"
        ],
        "avoidWhen": [
          "Traitement de documents sensibles sans isoler les services d'inférence"
        ],
        "guidanceSource": "curated",
        "lifecycle": "active"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-batch-3.json
````json
{
  "date": "2026-10-09",
  "source": "Two GitHub Stars screenshots",
  "summary": {
    "raw": 24,
    "unique": 24,
    "alreadyInCatalog": 5,
    "newlyAdmitted": 19,
    "catalogBefore": 521,
    "catalogAfter": 540
  },
  "alreadyCataloged": [
    "pytest-dev/pytest",
    "github/github-mcp-server",
    "oraios/serena",
    "emilk/egui",
    "liquidslr/system-design-notes"
  ],
  "newlyAdmitted": [
    "airbytehq/airbyte",
    "apache/datafusion",
    "apache/superset",
    "Dataherald/dataherald",
    "defog-ai/sqlcoder",
    "dlt-hub/dlt",
    "duckdb/duckdb",
    "eosphoros-ai/DB-GPT",
    "evidence-dev/evidence",
    "fivetran/great_expectations",
    "Jakeschincariol/arena-skill",
    "Kanaries/pygwalker",
    "metabase/metabase",
    "open-metadata/OpenMetadata",
    "pola-rs/polars",
    "quarto-dev/quarto-cli",
    "sinaptik-ai/pandas-ai",
    "sodadata/soda-core",
    "yifanfeng97/Hyper-Extract"
  ],
  "auditRequired": [
    {
      "repo": "airbytehq/airbyte",
      "reason": "GitHub does not resolve a standard SPDX license"
    },
    {
      "repo": "Dataherald/dataherald",
      "reason": "Repository has not been updated in over two years"
    },
    {
      "repo": "defog-ai/sqlcoder",
      "reason": "Repository has not been updated in over two years"
    },
    {
      "repo": "metabase/metabase",
      "reason": "GitHub does not resolve a standard SPDX license"
    },
    {
      "repo": "quarto-dev/quarto-cli",
      "reason": "GitHub does not resolve a standard SPDX license"
    },
    {
      "repo": "sinaptik-ai/pandas-ai",
      "reason": "GitHub does not resolve a standard SPDX license"
    },
    {
      "repo": "sodadata/soda-core",
      "reason": "GitHub does not resolve a standard SPDX license"
    },
    {
      "repo": "yifanfeng97/Hyper-Extract",
      "reason": "GitHub does not resolve a standard SPDX license"
    }
  ],
  "provenance": {
    "manifest": "imports/github-stars-2026-10-09-batch-3.json",
    "metadata": [
      "reports/star-import-2026-10-09-batch-3-metadata-1.json",
      "reports/star-import-2026-10-09-batch-3-metadata-2.json"
    ],
    "reviewed": "reports/star-import-2026-10-09-batch-3-reviewed.json"
  }
}
````

## File: reports/star-import-2026-10-09-metadata-1.json
````json
{
  "source": "GitHub REST repository metadata for screenshot admission",
  "repositories": [
    {
      "repo": "2Retr0/GodotOceanWaves",
      "description": "FFT-based ocean-wave rendering, implemented in Godot",
      "language": "C#",
      "github": {
        "stars": 3304,
        "forks": 197,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-04-29T17:17:08Z"
      }
    },
    {
      "repo": "owncloud/android",
      "description": ":phone: The ownCloud Android App",
      "language": "Kotlin",
      "github": {
        "stars": 4172,
        "forks": 3083,
        "openIssues": 206,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T03:11:03Z"
      }
    },
    {
      "repo": "shadcn-ui/lint",
      "description": "An agent-first linter for Tailwind design systems. Write design system rules that agents can verify.",
      "language": "TypeScript",
      "github": {
        "stars": 3137,
        "forks": 62,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:58:39Z"
      }
    },
    {
      "repo": "arnegiacomo/fugleramme",
      "description": "Bird frame for Raspberry Pi or your homelab - real-time bird detection by audio, fully local AI, rendered as real, hand-cut 1800s bird illustrations. On an e-ink panel, a TV, or any screen.",
      "language": "Python",
      "github": {
        "stars": 3594,
        "forks": 113,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T17:24:02Z"
      }
    },
    {
      "repo": "elliothux/open-compute",
      "description": "Self-hosted Cloudflare Workers-compatible platform with Workers、KV、D1、R2、DO、Queues、Workflows、Cron、Cache、Images、Vectorize、AI Search、Artifacts、Static Assets、Service Bindings、Dynamic Workers、LogTail、Gateway in one Rust binary.",
      "language": "Rust",
      "github": {
        "stars": 1776,
        "forks": 65,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T18:58:00Z"
      }
    },
    {
      "repo": "chubbyguan/chubbyskills",
      "description": "把中文全渠道内容（抖音 / B站 / 小红书 / 公众号 / X / 播客）采集进个人知识库的 14 个 AI Skill：图文存图、视频转文字稿、字幕优先免 GPU、RSS/YouTube 订阅调度与每日情报简报，附带知识库 MCP server。｜ Ingest Chinese content into your personal knowledge base — image/video routing, subtitle-first transcription, feed subscriptions with daily digests, and a KB MCP server.",
      "language": "Python",
      "github": {
        "stars": 1203,
        "forks": 147,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T09:43:23Z"
      }
    },
    {
      "repo": "togg53192-cmd/jailbreaks",
      "description": "LIST OF ALL MY JAILBREAKS",
      "language": null,
      "github": {
        "stars": 2619,
        "forks": 431,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-08T19:55:45Z"
      }
    },
    {
      "repo": "jamwithai/production-agentic-rag-course",
      "description": null,
      "language": "Python",
      "github": {
        "stars": 9679,
        "forks": 2103,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-06-05T07:23:49Z"
      }
    },
    {
      "repo": "daytonaio/daytona",
      "description": "Daytona is a Secure and Elastic Infrastructure for Running AI-Generated Code",
      "language": null,
      "github": {
        "stars": 71596,
        "forks": 5646,
        "openIssues": 458,
        "archived": true,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-07-24T07:12:07Z"
      }
    },
    {
      "repo": "getzep/graphiti",
      "description": "Build Real-Time Knowledge Graphs for AI Agents",
      "language": "Python",
      "github": {
        "stars": 31569,
        "forks": 3242,
        "openIssues": 462,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-07T19:12:47Z"
      }
    },
    {
      "repo": "huggingface/smolagents",
      "description": "🤗 smolagents: a barebones library for agents that think in code.",
      "language": "Python",
      "github": {
        "stars": 29742,
        "forks": 3051,
        "openIssues": 881,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T18:35:07Z"
      }
    },
    {
      "repo": "OffGridPete/Fieldwatch",
      "description": "Receive-only Wi-Fi and Bluetooth LE observer for Android. MIT.",
      "language": "Kotlin",
      "github": {
        "stars": 2824,
        "forks": 336,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-06T16:25:56Z"
      }
    },
    {
      "repo": "D4Vinci/Scrapling",
      "description": "🕷️ An adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl! Don't be shy, join here: https://discord.gg/EMgGbDceNQ and follow here for daily tips and tricks: https://x.com/Scrapling_dev",
      "language": "Python",
      "github": {
        "stars": 86388,
        "forks": 8858,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-08T20:28:21Z"
      }
    },
    {
      "repo": "whaleyxbt/patchright-enhanced",
      "description": "Browser automation toolkit for QA, monitoring and internal workflows",
      "language": "TypeScript",
      "github": {
        "stars": 486,
        "forks": 89,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-06T14:52:34Z"
      }
    },
    {
      "repo": "Ignitetechnologies/Mindmap",
      "description": "This repository will contain many mindmaps for cyber security technologies, methodologies, courses, and certifications in a tree structure to give brief details about them",
      "language": null,
      "github": {
        "stars": 9348,
        "forks": 1826,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-07-21T15:47:21Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-metadata-2.json
````json
{
  "source": "GitHub REST repository metadata for screenshot admission",
  "repositories": [
    {
      "repo": "JoasASantos/Offensive-Security-AI-Models",
      "description": "Uncensored AI models or those fine-tuned for cybersecurity tasks.",
      "language": null,
      "github": {
        "stars": 646,
        "forks": 75,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-28T14:34:47Z"
      }
    },
    {
      "repo": "letta-ai/letta-code",
      "description": "Stateful agents that are like people, with memory, identity, and the ability to learn and adapt",
      "language": "TypeScript",
      "github": {
        "stars": 3550,
        "forks": 430,
        "openIssues": 501,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:15:10Z"
      }
    },
    {
      "repo": "InfinityLoop1308/PipePipe",
      "description": "An open-source Android app to let you browse YouTube and other services freely. ",
      "language": "Shell",
      "github": {
        "stars": 6918,
        "forks": 246,
        "openIssues": 170,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-26T08:12:59Z"
      }
    },
    {
      "repo": "agentverse-os/AgentVerse-OS",
      "description": "Personal cloud OS for a developer and their AI agents on a single server. One-command install on Ubuntu, then everything in the browser: a windowed desktop, isolated workspaces with VS Code, Claude Code and Codex, a store of 944 self-hosted apps, backups and updates. Access only via Tailscale, nothing exposed to the internet. Rust core, Svelte UI.",
      "language": "Rust",
      "github": {
        "stars": 977,
        "forks": 26,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T11:34:49Z"
      }
    },
    {
      "repo": "yejy53/Editable-Design",
      "description": "Agent-driven creation of editable, tastefully crafted visual artifacts.",
      "language": "Python",
      "github": {
        "stars": 1155,
        "forks": 80,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-29T09:59:55Z"
      }
    },
    {
      "repo": "pizza-bot-app/pizza-bot",
      "description": "A local-first inbox for long-running AI agents, built with DeepAgents and LangGraph.",
      "language": "TypeScript",
      "github": {
        "stars": 460,
        "forks": 45,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T21:50:33Z"
      }
    },
    {
      "repo": "anmolkapil/plexo",
      "description": "Speed up downloads by combining multiple network connections in parallel",
      "language": "TypeScript",
      "github": {
        "stars": 1497,
        "forks": 130,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T18:44:57Z"
      }
    },
    {
      "repo": "vinnylarouge/jevlike",
      "description": null,
      "language": "Python",
      "github": {
        "stars": 1352,
        "forks": 118,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T18:12:53Z"
      }
    },
    {
      "repo": "Antseed/openclaw-channel-antseed",
      "description": "AntSeed P2P network channel for OpenClaw — provide AI agent services on the decentralized network",
      "language": "TypeScript",
      "github": {
        "stars": 4,
        "forks": 0,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-02-28T20:09:24Z"
      }
    },
    {
      "repo": "Antseed/AIPs",
      "description": "AntSeed Improvement Proposals (AIPs) — propose and standardize changes to the AntSeed protocol, contracts, interfaces, and economics",
      "language": "JavaScript",
      "github": {
        "stars": 5,
        "forks": 3,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC0-1.0",
        "pushedAt": "2026-10-04T05:38:14Z"
      }
    },
    {
      "repo": "Antseed/antseed",
      "description": "AntSeed P2P AI Network - An open market for AI inference. No gatekeepers.",
      "language": "TypeScript",
      "github": {
        "stars": 109,
        "forks": 37,
        "openIssues": 111,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-09T01:04:09Z"
      }
    },
    {
      "repo": "Effect-TS/effect",
      "description": "Build production-ready applications in TypeScript",
      "language": "TypeScript",
      "github": {
        "stars": 17176,
        "forks": 843,
        "openIssues": 243,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T23:59:51Z"
      }
    },
    {
      "repo": "colbymchenry/codegraph",
      "description": "Pre-indexed code knowledge graph, auto syncs on code changes, for Claude Code, Codex, Gemini, Cursor, OpenCode, AntiGravity, Kiro, CoPilot, and Hermes Agent — fewer tokens, fewer tool calls, 100% local",
      "language": "C",
      "github": {
        "stars": 73508,
        "forks": 4731,
        "openIssues": 527,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-07T16:34:38Z"
      }
    },
    {
      "repo": "google/skills",
      "description": "Agent Skills for Google products and technologies",
      "language": "Python",
      "github": {
        "stars": 21061,
        "forks": 1756,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:12:41Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09-metadata-3.json
````json
{
  "source": "GitHub REST repository metadata for screenshot admission",
  "repositories": [
    {
      "repo": "NVIDIA/OpenShell",
      "description": "OpenShell is the safe, private runtime for autonomous AI agents.",
      "language": "Rust",
      "github": {
        "stars": 15480,
        "forks": 1743,
        "openIssues": 576,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:24:52Z"
      }
    },
    {
      "repo": "JuliusBrussee/caveman",
      "description": "🪨 why use many token when few token do trick. Viral skill + proxy for coding agents that cuts 65% of tokens by talking like a caveman.",
      "language": "Go",
      "github": {
        "stars": 110586,
        "forks": 6404,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T13:28:29Z"
      }
    },
    {
      "repo": "Epix-Incorporated/Adonis",
      "description": "Roblox Server Administration System",
      "language": "Luau",
      "github": {
        "stars": 508,
        "forks": 237,
        "openIssues": 65,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-07T19:34:32Z"
      }
    },
    {
      "repo": "roblox-ts/roblox-ts",
      "description": "A TypeScript-to-Luau Compiler for Roblox",
      "language": "TypeScript",
      "github": {
        "stars": 1311,
        "forks": 178,
        "openIssues": 135,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:03:05Z"
      }
    },
    {
      "repo": "axstin/rbxfpsunlocker",
      "description": "FPS Unlocker for Roblox",
      "language": "C++",
      "github": {
        "stars": 2226,
        "forks": 878,
        "openIssues": 78,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-06-21T18:43:29Z"
      }
    },
    {
      "repo": "lihanyu81/polymarket_lp_tool",
      "description": "polymarket_lp_tool",
      "language": "Python",
      "github": {
        "stars": 559,
        "forks": 98,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-05-06T05:41:52Z"
      }
    },
    {
      "repo": "HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits",
      "description": "Rust trading bots for prediction markets — Polymarket, Kalshi, Limitless. Copy Trading is production-ready; nine more strategies in development on the same execution core. Dry-run by default, self-custody, MIT. Polymarket trading bot Polymarket copy trading bot Polymarket arbitrage trading bot ",
      "language": "Rust",
      "github": {
        "stars": 472,
        "forks": 127,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-07T11:44:40Z"
      }
    },
    {
      "repo": "recogardtech/AutoPilotPM",
      "description": "Open-source autonomous trading system powered by AI, built to monitor and trade across 1,000+ markets including Polymarket, Kalshi, Binance, Hyperliquid, Solana DEXs and multiple EVM networks. Finds opportunities, places trades in real time and handles risk automatically",
      "language": "TypeScript",
      "github": {
        "stars": 33,
        "forks": 9,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:01:24Z"
      }
    },
    {
      "repo": "evidentlyai/evidently",
      "description": "Evidently is ​​an open-source ML and LLM observability framework. Evaluate, test, and monitor any AI-powered system or data pipeline. From tabular data to Gen AI. 100+ metrics.",
      "language": "Jupyter Notebook",
      "github": {
        "stars": 7978,
        "forks": 947,
        "openIssues": 328,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-29T08:32:43Z"
      }
    },
    {
      "repo": "Giskard-AI/giskard-oss",
      "description": "🐢 Open-Source Evaluation & Testing library for LLM Agents",
      "language": "Python",
      "github": {
        "stars": 5879,
        "forks": 547,
        "openIssues": 70,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T07:10:15Z"
      }
    },
    {
      "repo": "truera/trulens",
      "description": "Evaluation and Tracking for LLM Experiments and AI Agents",
      "language": "Python",
      "github": {
        "stars": 3594,
        "forks": 360,
        "openIssues": 96,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:17:07Z"
      }
    },
    {
      "repo": "UKGovernmentBEIS/inspect_ai",
      "description": "Inspect: A framework for large language model evaluations",
      "language": "Python",
      "github": {
        "stars": 2962,
        "forks": 791,
        "openIssues": 375,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:16:04Z"
      }
    },
    {
      "repo": "comet-ml/opik",
      "description": "Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards.",
      "language": "Python",
      "github": {
        "stars": 22464,
        "forks": 1847,
        "openIssues": 198,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:08:08Z"
      }
    },
    {
      "repo": "vibrantlabsai/ragas",
      "description": "Supercharge Your LLM Application Evaluations 🚀",
      "language": "Python",
      "github": {
        "stars": 15967,
        "forks": 1750,
        "openIssues": 626,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-02-24T07:47:19Z"
      }
    }
  ]
}
````

## File: reports/star-import-2026-10-09.json
````json
{
  "date": "2026-10-09",
  "source": "GitHub Stars screenshots",
  "summary": {
    "raw": 97,
    "previouslyImported": 48,
    "newVsPreviousImports": 49,
    "alreadyInCuratedCatalog": 5,
    "newlyAdmitted": 43,
    "requiresReview": 1,
    "catalogBefore": 392,
    "catalogAfter": 435
  },
  "notAdmitted": [
    {
      "repo": "myschwarz/openrig",
      "reason": "GitHub repository API returned 404; identity could not be verified"
    }
  ],
  "previouslyCataloged": [
    "e2b-dev/E2B",
    "getsentry/sentry",
    "confident-ai/deepeval",
    "openai/evals",
    "Arize-ai/phoenix"
  ],
  "newlyAdmitted": [
    "2Retr0/GodotOceanWaves",
    "owncloud/android",
    "shadcn-ui/lint",
    "arnegiacomo/fugleramme",
    "elliothux/open-compute",
    "chubbyguan/chubbyskills",
    "togg53192-cmd/jailbreaks",
    "jamwithai/production-agentic-rag-course",
    "daytonaio/daytona",
    "getzep/graphiti",
    "huggingface/smolagents",
    "OffGridPete/Fieldwatch",
    "D4Vinci/Scrapling",
    "whaleyxbt/patchright-enhanced",
    "Ignitetechnologies/Mindmap",
    "JoasASantos/Offensive-Security-AI-Models",
    "letta-ai/letta-code",
    "InfinityLoop1308/PipePipe",
    "agentverse-os/AgentVerse-OS",
    "yejy53/Editable-Design",
    "pizza-bot-app/pizza-bot",
    "anmolkapil/plexo",
    "vinnylarouge/jevlike",
    "Antseed/openclaw-channel-antseed",
    "Antseed/AIPs",
    "Antseed/antseed",
    "Effect-TS/effect",
    "colbymchenry/codegraph",
    "google/skills",
    "NVIDIA/OpenShell",
    "JuliusBrussee/caveman",
    "Epix-Incorporated/Adonis",
    "roblox-ts/roblox-ts",
    "axstin/rbxfpsunlocker",
    "lihanyu81/polymarket_lp_tool",
    "HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits",
    "recogardtech/AutoPilotPM",
    "evidentlyai/evidently",
    "Giskard-AI/giskard-oss",
    "truera/trulens",
    "UKGovernmentBEIS/inspect_ai",
    "comet-ml/opik",
    "vibrantlabsai/ragas"
  ],
  "provenance": {
    "manifest": "imports/github-stars-2026-10-09.json",
    "metadata": [
      "reports/star-import-2026-10-09-metadata-1.json",
      "reports/star-import-2026-10-09-metadata-2.json",
      "reports/star-import-2026-10-09-metadata-3.json"
    ]
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

## File: schemas/replacement-report.schema.json
````json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Report","type":"object","required":["threshold","findings","repositories"],"properties":{"threshold":{"type":"number","minimum":0,"maximum":100},"findings":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Finding","type":"object","required":["repo","health","qualityScore","domain","suggestedReplacements"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]},"suggestedReplacements":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Candidate","type":"object","required":["repo","replacementScore","health","qualityScore","domain"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"replacementScore":{"type":"number","minimum":0},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]}},"additionalProperties":false}}},"additionalProperties":false}}},"additionalProperties":false}
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
code = f"archived-{lifecycle or 'audit'}-retained"
label = lifecycle or "audit"
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
def main()
⋮----
parser = argparse.ArgumentParser(description="Audit catalog maintenance debt.")
⋮----
args = parser.parse_args()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
report = analyze(repos, stale_days=args.stale_days)
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

## File: scripts/recommend.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
STACKS = ROOT / "stacks.json"
HISTORY = ROOT / "history.json"
⋮----
DOMAIN_ALIASES = {
TIER_BONUS = {"core": 1.0, "recommended": 0.6, "specialized": 0.25, "audit": -0.4}
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
def activity_adjustment(r)
⋮----
gh = r.get("github")
⋮----
pushed = gh.get("pushedAt")
⋮----
dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
days = max(0, (datetime.now(timezone.utc) - dt).days)
⋮----
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
def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps)
⋮----
caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
⋮----
rtoks = tokens(" ".join([
lexical = len(qtokens & rtoks) / max(1, len(qtokens))
cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
domain_match = 1.0 if requested_domains and r.get("domain") in requested_domains else 0.0
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
⋮----
matched_caps = sorted(required_caps & caps)
⋮----
matched_terms = sorted(qtokens & (tokens(r.get("repo", "")) | caps | best))
⋮----
def choose_stack(stacks, qtokens, domains)
⋮----
stoks = tokens(st.get("name", "") + " " + st.get("goal", "") + " " + " ".join(st.get("notes", [])))
score = 2*len(qtokens & stoks) + (3 if st.get("domain") in domains else 0)
⋮----
def infer_alternatives(source, repos, top=3)
⋮----
candidates = []
⋮----
result = replacement_score(source, candidate)
⋮----
def infer_complements(source, stacks, repo_by_name, top=4)
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
def resolve_relations(source, repos, stacks, repo_by_name)
⋮----
explicit_alternatives = source.get("alternatives", [])
explicit_complements = source.get("complements", [])
alternatives = explicit_alternatives or infer_alternatives(source, repos)
complements = explicit_complements or infer_complements(source, stacks, repo_by_name)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
⋮----
args = ap.parse_args()
⋮----
repo_by_name = {r["repo"]: r for r in repos}
qtokens = tokens(args.query)
domains = set(args.domain) or infer_domains(qtokens)
⋮----
ranked = []
filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "audit":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}
⋮----
gh = r.get("github", {})
⋮----
s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
⋮----
top = []
⋮----
relations = resolve_relations(r, repos, stacks, repo_by_name)
⋮----
result = {
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
path = item.get("path")
⋮----
payload = fetch_contents(repo, path=path, ref=default_branch, token=token)
⋮----
text = _decode_content(payload)
⋮----
detected = detect_license_text(text)
⋮----
# Some curated lists and documentation repositories state their license
# only in the README. Use this as a secondary signal, never as a guess.
readmes = []
⋮----
payload = fetch_contents(repo, path=item.get("path"), ref=default_branch, token=token)
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
name = r["repo"]
⋮----
raw = fetch(name, token)
fresh = metadata(raw)
⋮----
detected = fallback_license(name, raw.get("default_branch"), token)
⋮----
current_github = r.get("github")
current_license = current_github.get("license") if isinstance(current_github, dict) else None
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
# Local Markdown links from README must point to repository files/directories.
⋮----
local=target.split("#",1)[0]
⋮----
spec=importlib.util.spec_from_file_location("evaluation",ROOT/"scripts"/"evaluate_candidates.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
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

## File: scripts/test_json_contracts.py
````python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/"scripts"/"validate_json_contract.py"
SCHEMAS=ROOT/"schemas"
⋮----
required_schemas={
⋮----
spec=importlib.util.spec_from_file_location("contract_validator",VALIDATOR)
validator=importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
⋮----
samples={
⋮----
schema=json.loads((SCHEMAS/schema_name).read_text())
errors=validator.validate(data,schema)
⋮----
data=json.loads((ROOT/data_name).read_text())
⋮----
catalog_schema=json.loads((ROOT/"catalog.schema.json").read_text())
catalog=json.loads((ROOT/"catalog.json").read_text())
errors=validator.validate(catalog,catalog_schema)
⋮----
unsupported={"type":"object","unevaluatedProperties":False}
errors=validator.validate({},unsupported)
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

## File: scripts/test_recommend.py
````python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "recommend.py"
⋮----
def run(*args)
⋮----
out = subprocess.check_output([sys.executable, str(SCRIPT), *args, "--json"], text=True)
⋮----
cases = [
⋮----
data = run(query, "--top", "5")
domains = set(data["inferredDomains"])
⋮----
strict = run("android mobile", "--platform", "android", "--require-all-caps", "--cap", "mobile")
⋮----
high_threshold = run("ai agent", "--min-score", "1000")
⋮----
default_audit = run("ponytail agent", "--top", "20")
⋮----
with_audit = run("ponytail agent", "--top", "20", "--include-audit")
⋮----
spec = importlib.util.spec_from_file_location("recommend", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
base = {
qtokens = mod.tokens("specialized phrase")
curated = dict(base, guidanceSource="curated")
inferred = dict(base, guidanceSource="inferred")
⋮----
source = {
candidate = {
audit_candidate = dict(candidate, repo="x/audit", tier="audit")
⋮----
stack_repo = dict(candidate, repo="x/stack-tool", capabilities=["cache"])
repo_by_name = {r["repo"]: r for r in [source, stack_repo]}
stacks = [{"name":"Backend Stack","repos":["x/source","x/stack-tool"]}]
⋮----
curated_rel = dict(source, alternatives=["x/manual"], complements=["x/manual-comp"])
resolved = mod.resolve_relations(curated_rel, [curated_rel, candidate], stacks, repo_by_name)
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
def test_metadata_refresh_uses_license_fallback()
⋮----
def test_metadata_refresh_preserves_verified_license_when_github_is_inconclusive()
⋮----
def test_server_error_remains_fatal()
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
valid_tiers = {"core","recommended","specialized","audit"}
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

## File: AGENTS.md
````markdown
# Repository agent instructions

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

Repository-specific rules:
- Preserve existing architecture and public interfaces unless the task requires a change.
- Prefer the smallest coherent change.
- Prefer targeted tests from `.ai/brain/selected-tests.json`; expand validation when impact is ambiguous or targeted tests fail.
- Treat hotset/context packets and graph shards as routing hints, not authoritative source.
- Verify reference/dependency/impact/AST hits against authoritative source before editing.
- Treat security signals and static graph edges as heuristics, not proof.
- Never reproduce suspected secret values.
- Update manual project-state sections when status, blockers, or next priority materially changes.
- Maintain `.ai/session-state.json` for substantial multi-turn work so a later "Continue" can resume without reconstructing the repository.
````

## File: cache-health-history.json
````json
{
  "schemaVersion": 1,
  "points": [
    {
      "date": "2026-09-16",
      "status": "degraded",
      "logicalRequests": 180,
      "apiCallAvoidanceRate": 0.0,
      "bodyReuseRate": 0.0,
      "networkFetchRate": 0.8833,
      "staleFallbackRate": 0.0,
      "candidateSeverity": "degraded",
      "alertState": "watch",
      "issueAction": "open"
    },
    {
      "date": "2026-09-20",
      "status": "watch",
      "logicalRequests": 180,
      "apiCallAvoidanceRate": 0.4944,
      "bodyReuseRate": 0.4944,
      "networkFetchRate": 0.4,
      "staleFallbackRate": 0.0,
      "candidateSeverity": "watch",
      "alertState": "watch",
      "issueAction": "open"
    },
    {
      "date": "2026-09-21",
      "status": "healthy",
      "logicalRequests": 180,
      "apiCallAvoidanceRate": 0.8944,
      "bodyReuseRate": 0.8944,
      "networkFetchRate": 0.0,
      "staleFallbackRate": 0.0,
      "candidateSeverity": "healthy",
      "alertState": "watch",
      "issueAction": "open"
    },
    {
      "date": "2026-09-28",
      "status": "healthy",
      "logicalRequests": 180,
      "apiCallAvoidanceRate": 0.7167,
      "bodyReuseRate": 0.7167,
      "networkFetchRate": 0.1778,
      "staleFallbackRate": 0.0,
      "candidateSeverity": "healthy",
      "alertState": "healthy",
      "issueAction": "close"
    },
    {
      "date": "2026-10-05",
      "status": "degraded",
      "logicalRequests": 180,
      "apiCallAvoidanceRate": 0.0111,
      "bodyReuseRate": 0.0111,
      "networkFetchRate": 0.8889,
      "staleFallbackRate": 0.0,
      "candidateSeverity": "degraded",
      "alertState": "watch",
      "issueAction": "hold"
    }
  ]
}
````

## File: catalog.json
````json
{
  "schemaVersion": 1,
  "selectionPolicy": {
    "coreMin": 9.5,
    "recommendedMin": 9,
    "specializedMin": 8
  },
  "repositories": [
    {
      "repo": "lobehub/lobehub",
      "score": 9.2,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 82982,
        "forks": 15957,
        "openIssues": 1032,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "LobeHub Community License",
        "pushedAt": "2026-10-05T11:12:15Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "harry0703/MoneyPrinterTurbo",
      "score": 8.2,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 128532,
        "forks": 20102,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T06:48:17Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "hiyouga/LlamaFactory",
      "score": 9.5,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 75315,
        "forks": 9227,
        "openIssues": 1171,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-28T09:10:59Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "low-resource environments",
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Skyvern-AI/skyvern",
      "score": 9.3,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 23133,
        "forks": 2185,
        "openIssues": 274,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T09:09:27Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "BasedHardware/omi",
      "score": 8.4,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13632,
        "forks": 2566,
        "openIssues": 1614,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:25:04Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "OpenHands/OpenHands",
      "score": 9.7,
      "tier": "core",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "alternatives": [
        "anomalyco/opencode",
        "Aider-AI/aider"
      ],
      "complements": [
        "microsoft/playwright",
        "e2b-dev/E2B",
        "langfuse/langfuse"
      ],
      "bestFor": [
        "autonomous software tasks",
        "repo-level changes"
      ],
      "avoidWhen": [
        "very lightweight edits"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 90017,
        "forks": 11900,
        "openIssues": 954,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:18:59Z"
      }
    },
    {
      "repo": "danielmiessler/Fabric",
      "score": 9.1,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 44157,
        "forks": 4294,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:07:09Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ollama/ollama",
      "score": 9.8,
      "tier": "core",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "alternatives": [
        "mudler/LocalAI"
      ],
      "complements": [
        "BerriAI/litellm",
        "danny-avila/LibreChat"
      ],
      "bestFor": [
        "local model serving",
        "offline inference"
      ],
      "avoidWhen": [
        "very large models on constrained hardware"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 182217,
        "forks": 18103,
        "openIssues": 4169,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T23:16:41Z"
      }
    },
    {
      "repo": "khoj-ai/khoj",
      "score": 8.8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 37559,
        "forks": 2497,
        "openIssues": 165,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-08-02T01:55:40Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "modelcontextprotocol/servers",
      "score": 9.7,
      "tier": "core",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "alternatives": [],
      "complements": [
        "ChromeDevTools/chrome-devtools-mcp",
        "doobidoo/mcp-memory-service"
      ],
      "bestFor": [
        "MCP integrations",
        "tool connectivity"
      ],
      "avoidWhen": [
        "no tool integration needed"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 91010,
        "forks": 11754,
        "openIssues": 490,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T05:59:16Z"
      }
    },
    {
      "repo": "browser-use/browser-use",
      "score": 9.6,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "web-retrieval"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "web",
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 117166,
        "forks": 12931,
        "openIssues": 539,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T00:06:08Z"
      },
      "bestFor": [
        "agentic workflows",
        "browser and web retrieval"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mksglu/context-mode",
      "score": 8.5,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25438,
        "forks": 1822,
        "openIssues": 332,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:14:53Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "mattpocock/skills",
      "score": 8.8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 276592,
        "forks": 23179,
        "openIssues": 548,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:17:21Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "DietrichGebert/ponytail",
      "score": 7.5,
      "tier": "audit",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 155490,
        "forks": 8360,
        "openIssues": 64,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:09:14Z"
      }
    },
    {
      "repo": "affaan-m/ECC",
      "score": 7.6,
      "tier": "audit",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 273261,
        "forks": 40784,
        "openIssues": 347,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T04:55:16Z"
      }
    },
    {
      "repo": "THU-MAIC/OpenMAIC",
      "score": 8.3,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39969,
        "forks": 6185,
        "openIssues": 182,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:44:35Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "diegosouzapw/OmniRoute",
      "score": 8.2,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73152,
        "forks": 10488,
        "openIssues": 699,
        "archived": false,
        "disabled": false,
        "defaultBranch": "release/v3.8.52",
        "license": "MIT",
        "pushedAt": "2026-10-02T18:26:57Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "obra/superpowers",
      "score": 9,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 295439,
        "forks": 26393,
        "openIssues": 308,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T02:37:47Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ayghri/i-have-adhd",
      "score": 7,
      "tier": "audit",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 53776,
        "forks": 3086,
        "openIssues": 81,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T16:44:46Z"
      }
    },
    {
      "repo": "p-e-w/heretic",
      "score": 8.7,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 33272,
        "forks": 3726,
        "openIssues": 93,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-04T12:01:40Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "deepseek-ai/deepseek-harness",
      "score": 9.6,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 243710,
        "forks": 29204,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-03T06:02:48Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "msitarzewski/agency-agents",
      "score": 8.6,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 156920,
        "forks": 25329,
        "openIssues": 160,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T21:17:44Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Alishahryar1/free-claude-code",
      "score": 8.2,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 56690,
        "forks": 9065,
        "openIssues": 310,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T05:45:07Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vercel-labs/agent-browser",
      "score": 9.1,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "web-retrieval"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "web",
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 43529,
        "forks": 2939,
        "openIssues": 830,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-03T06:28:26Z"
      },
      "bestFor": [
        "agentic workflows",
        "browser and web retrieval"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ultraworkers/claw-code",
      "score": 8.3,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 195214,
        "forks": 108207,
        "openIssues": 48,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-16T06:18:45Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "666ghj/MiroFish",
      "score": 8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 76216,
        "forks": 11663,
        "openIssues": 129,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-01T18:28:51Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "punkpeye/awesome-mcp-servers",
      "score": 9.3,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 95827,
        "forks": 17110,
        "openIssues": 2947,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T02:12:17Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Shubhamsaboo/awesome-llm-apps",
      "score": 9.2,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 140742,
        "forks": 20685,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-30T20:31:22Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "pascalorg/editor",
      "score": 8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 24628,
        "forks": 3045,
        "openIssues": 39,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T20:54:27Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "nashsu/llm_wiki",
      "score": 7.8,
      "tier": "audit",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 20213,
        "forks": 2289,
        "openIssues": 271,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "LGPL-3.0",
        "pushedAt": "2026-09-28T01:43:23Z"
      }
    },
    {
      "repo": "milind-soni/OpenMausBot",
      "score": 8.2,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4045,
        "forks": 694,
        "openIssues": 351,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:20:49Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "akitaonrails/ai-memory",
      "score": 8.5,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "memory"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8830,
        "forks": 614,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:20:06Z"
      },
      "bestFor": [
        "agentic workflows",
        "agent memory and context retention"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "volcengine/OpenViking",
      "score": 8.8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39221,
        "forks": 3088,
        "openIssues": 761,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T11:15:50Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "anomalyco/opencode",
      "score": 9.8,
      "tier": "core",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "alternatives": [
        "OpenHands/OpenHands",
        "Aider-AI/aider"
      ],
      "complements": [
        "BerriAI/litellm",
        "mem0ai/mem0",
        "langfuse/langfuse"
      ],
      "bestFor": [
        "autonomous coding",
        "terminal workflows"
      ],
      "avoidWhen": [
        "GUI-first workflows"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 211807,
        "forks": 28177,
        "openIssues": 6273,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:25:21Z"
      }
    },
    {
      "repo": "ruvnet/ruflo",
      "score": 8.9,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 73889,
        "forks": 8781,
        "openIssues": 1088,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:32:17Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "NousResearch/hermes-agent",
      "score": 9,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 251300,
        "forks": 53960,
        "openIssues": 48061,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:19:51Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ChromeDevTools/chrome-devtools-mcp",
      "score": 9.5,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 52974,
        "forks": 5659,
        "openIssues": 120,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T04:24:31Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "heygen-com/hyperframes",
      "score": 8.6,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 56998,
        "forks": 5109,
        "openIssues": 165,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:21:55Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "danny-avila/LibreChat",
      "score": 9.4,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45293,
        "forks": 9283,
        "openIssues": 837,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:15:07Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "f/prompts.chat",
      "score": 8.6,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 172058,
        "forks": 22030,
        "openIssues": 84,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T08:12:28Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Aider-AI/aider",
      "score": 9.6,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49373,
        "forks": 5032,
        "openIssues": 1910,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-05-22T14:02:20Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "plandex-ai/plandex",
      "score": 8.8,
      "tier": "specialized",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15689,
        "forks": 1177,
        "openIssues": 66,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-10-03T21:49:58Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "langchain-ai/langgraph",
      "score": 9.6,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 42731,
        "forks": 7263,
        "openIssues": 822,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T08:53:37Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "microsoft/autogen",
      "score": 9.4,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 61255,
        "forks": 9278,
        "openIssues": 1100,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-04-15T11:59:09Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "crewAIInc/crewAI",
      "score": 9.2,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 59354,
        "forks": 8647,
        "openIssues": 545,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:15:42Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "google/adk-python",
      "score": 9.3,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python",
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 21705,
        "forks": 4101,
        "openIssues": 449,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T09:07:51Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "camel-ai/camel",
      "score": 9,
      "tier": "recommended",
      "category": "Agents / IA / développement",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 17809,
        "forks": 2106,
        "openIssues": 529,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-30T04:46:03Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "public-apis/public-apis",
      "score": 9.4,
      "tier": "recommended",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "api-directory",
        "data-sources"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 486152,
        "forks": 53743,
        "openIssues": 2016,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T04:32:07Z"
      },
      "bestFor": [
        "API discovery and reference",
        "data-source discovery"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "lissy93/web-check",
      "score": 8.8,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "web-diagnostics",
        "osint"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35009,
        "forks": 2873,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:58:07Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "trimstray/the-book-of-secret-knowledge",
      "score": 9,
      "tier": "recommended",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "memory"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 247990,
        "forks": 14452,
        "openIssues": 171,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-11-19T14:00:38Z"
      },
      "bestFor": [
        "knowledge retention and reference workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bmrf/tron",
      "score": 7.7,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "automation"
      ],
      "languages": [
        "batchfile"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6586,
        "forks": 416,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-03T19:35:35Z"
      }
    },
    {
      "repo": "ReVanced/revanced-manager",
      "score": 8.7,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "android",
        "patch-management"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 29720,
        "forks": 1159,
        "openIssues": 204,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-07-29T18:18:23Z"
      },
      "bestFor": [
        "android workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "sudoguy/tiktokpy",
      "score": 7.3,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "social-media-automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 876,
        "forks": 165,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-28T22:58:31Z"
      }
    },
    {
      "repo": "simonfarah/tiktok-bot",
      "score": 6.8,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "social-media-automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 918,
        "forks": 291,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-03-08T20:44:11Z"
      }
    },
    {
      "repo": "freeCodeCamp/freeCodeCamp",
      "score": 9.6,
      "tier": "core",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "learning",
        "software-engineering"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 456770,
        "forks": 48269,
        "openIssues": 199,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T10:50:19Z"
      },
      "bestFor": [
        "structured web-development learning",
        "hands-on programming exercises",
        "self-paced software-engineering study"
      ],
      "avoidWhen": [
        "advanced framework-specific production reference",
        "formal accredited coursework"
      ]
    },
    {
      "repo": "autoscrape-labs/pydoll",
      "score": 8.8,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "web-retrieval"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7107,
        "forks": 409,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-29T14:44:04Z"
      },
      "bestFor": [
        "browser and web retrieval"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "xai-org/x-algorithm",
      "score": 8.4,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "ranking",
        "recommendation-systems"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 33505,
        "forks": 5434,
        "openIssues": 118,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-03T03:26:57Z"
      },
      "bestFor": [
        "ranking workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "cathrynlavery/diagram-design",
      "score": 8.9,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "diagrams",
        "architecture"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 43379,
        "forks": 2799,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T04:11:15Z"
      },
      "bestFor": [
        "technical diagrams",
        "software architecture diagrams"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "sdmg15/Best-websites-a-programmer-should-visit",
      "score": 8.3,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "learning",
        "developer-resources"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 76234,
        "forks": 8589,
        "openIssues": 1002,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2025-09-16T18:34:24Z"
      },
      "bestFor": [
        "historical curated developer-resource index"
      ],
      "avoidWhen": [
        "current developer recommendations",
        "actively maintained resource discovery"
      ],
      "alternatives": [
        "freeCodeCamp/freeCodeCamp",
        "ruanyf/weekly"
      ],
      "lifecycle": "reference"
    },
    {
      "repo": "ChrisTitusTech/winutil",
      "score": 9.2,
      "tier": "recommended",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "windows-automation",
        "system-tuning"
      ],
      "languages": [
        "powershell"
      ],
      "platforms": [
        "windows"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 63636,
        "forks": 3714,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T15:37:19Z"
      },
      "bestFor": [
        "Windows administration automation",
        "Windows system tuning"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "harry2141985/Google-Collab-Notebooks",
      "score": 7.8,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "notebooks",
        "cloud-compute"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 65,
        "forks": 42,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-04-06T10:21:50Z"
      }
    },
    {
      "repo": "browserbase/stagehand",
      "score": 9.2,
      "tier": "recommended",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "web-retrieval"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25533,
        "forks": 1753,
        "openIssues": 378,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T16:24:31Z"
      },
      "bestFor": [
        "browser and web retrieval"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "qdrant/qdrant",
      "score": 9.5,
      "tier": "core",
      "category": "Mémoire / RAG / bases vectorielles",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "alternatives": [
        "chroma-core/chroma",
        "milvus-io/milvus"
      ],
      "complements": [
        "deepset-ai/haystack",
        "mem0ai/mem0"
      ],
      "bestFor": [
        "vector search",
        "RAG"
      ],
      "avoidWhen": [
        "tiny in-memory prototypes"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 34934,
        "forks": 2725,
        "openIssues": 747,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:14:23Z"
      }
    },
    {
      "repo": "chroma-core/chroma",
      "score": 9.2,
      "tier": "recommended",
      "category": "Mémoire / RAG / bases vectorielles",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 29440,
        "forks": 2546,
        "openIssues": 912,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T02:01:27Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "vector search and embedding retrieval"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "milvus-io/milvus",
      "score": 9.3,
      "tier": "recommended",
      "category": "Mémoire / RAG / bases vectorielles",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 46315,
        "forks": 4276,
        "openIssues": 1387,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T03:49:37Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "vector search and embedding retrieval"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "deepset-ai/haystack",
      "score": 9.1,
      "tier": "recommended",
      "category": "Mémoire / RAG / bases vectorielles",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 26654,
        "forks": 3237,
        "openIssues": 154,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:25:05Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "vector search and embedding retrieval"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "squidfunk/mkdocs-material",
      "score": 9.7,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "documentation",
        "docs-site"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 27540,
        "forks": 4146,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-02T08:04:22Z"
      },
      "bestFor": [
        "technical documentation",
        "documentation websites"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mkdocs/mkdocs",
      "score": 9.4,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "documentation",
        "docs-site"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 22493,
        "forks": 2655,
        "openIssues": 192,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-2-Clause",
        "pushedAt": "2025-10-20T13:17:06Z"
      },
      "bestFor": [
        "technical documentation",
        "documentation websites"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "facebook/docusaurus",
      "score": 9.6,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "documentation",
        "docs-site"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 66399,
        "forks": 10054,
        "openIssues": 416,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T20:35:04Z"
      },
      "bestFor": [
        "technical documentation",
        "documentation websites"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "withastro/starlight",
      "score": 9.3,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "documentation",
        "docs-site"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9361,
        "forks": 1054,
        "openIssues": 30,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T13:32:24Z"
      },
      "bestFor": [
        "technical documentation",
        "documentation websites"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "swagger-api/swagger-ui",
      "score": 9.6,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "api-documentation",
        "openapi"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 29029,
        "forks": 9253,
        "openIssues": 1141,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T09:22:12Z"
      },
      "bestFor": [
        "API documentation",
        "OpenAPI workflows"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Redocly/redoc",
      "score": 9.3,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "api-documentation",
        "openapi"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25941,
        "forks": 2401,
        "openIssues": 448,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T08:25:32Z"
      },
      "bestFor": [
        "API documentation",
        "OpenAPI workflows"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mermaid-js/mermaid",
      "score": 9.8,
      "tier": "core",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "diagrams",
        "architecture",
        "documentation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 90541,
        "forks": 9324,
        "openIssues": 1849,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:29:31Z"
      },
      "bestFor": [
        "text-to-diagram documentation",
        "architecture diagrams in Markdown",
        "version-controlled technical diagrams"
      ],
      "avoidWhen": [
        "pixel-perfect illustration",
        "interactive CAD-style editing"
      ]
    },
    {
      "repo": "plantuml/plantuml",
      "score": 9.5,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "diagrams",
        "architecture",
        "documentation"
      ],
      "languages": [
        "java"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13354,
        "forks": 1235,
        "openIssues": 595,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "LGPL-3.0",
        "pushedAt": "2026-10-05T01:03:19Z"
      },
      "bestFor": [
        "technical diagrams",
        "software architecture diagrams",
        "technical documentation"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "plantuml-stdlib/C4-PlantUML",
      "score": 9.2,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "diagrams",
        "architecture",
        "documentation"
      ],
      "languages": [
        "plantuml"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7427,
        "forks": 1170,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-26T14:58:27Z"
      },
      "bestFor": [
        "technical diagrams",
        "software architecture diagrams",
        "technical documentation"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "thomvaill/log4brains",
      "score": 8.8,
      "tier": "specialized",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "adr",
        "architecture",
        "documentation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1599,
        "forks": 111,
        "openIssues": 57,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2024-12-17T16:51:30Z"
      },
      "bestFor": [
        "software architecture diagrams",
        "technical documentation"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "orhun/git-cliff",
      "score": 9.3,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "changelog",
        "release-automation"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12282,
        "forks": 332,
        "openIssues": 118,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T23:39:10Z"
      },
      "bestFor": [
        "changelog automation",
        "release automation"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "conventional-changelog/conventional-changelog",
      "score": 9.1,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "changelog",
        "release-automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8514,
        "forks": 739,
        "openIssues": 30,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "ISC",
        "pushedAt": "2026-10-05T11:17:02Z"
      },
      "bestFor": [
        "changelog automation",
        "release automation"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "postgres/postgres",
      "score": 9.8,
      "tier": "core",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "database",
        "sql",
        "relational-database"
      ],
      "alternatives": [],
      "complements": [
        "redis/redis",
        "prisma/prisma",
        "drizzle-team/drizzle-orm"
      ],
      "bestFor": [
        "transactional data",
        "general-purpose relational storage"
      ],
      "avoidWhen": [
        "pure cache or ephemeral state"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 22284,
        "forks": 5930,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "PostgreSQL",
        "pushedAt": "2026-10-05T11:25:06Z"
      },
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "redis/redis",
      "score": 9.6,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "cache",
        "database",
        "messaging"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 76597,
        "forks": 24836,
        "openIssues": 3002,
        "archived": false,
        "disabled": false,
        "defaultBranch": "unstable",
        "license": "RSAL-2.0 / SSPL-1.0 / AGPL-3.0",
        "pushedAt": "2026-09-30T12:02:11Z"
      },
      "bestFor": [
        "application caching",
        "application data persistence",
        "messaging systems"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "supabase/supabase",
      "score": 9.8,
      "tier": "core",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "backend-as-a-service",
        "database",
        "auth",
        "storage"
      ],
      "alternatives": [
        "appwrite/appwrite",
        "pocketbase/pocketbase"
      ],
      "complements": [
        "postgres/postgres",
        "vercel/next.js"
      ],
      "bestFor": [
        "rapid full-stack backends",
        "auth + DB + storage"
      ],
      "avoidWhen": [
        "highly custom backend architecture"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 111104,
        "forks": 15834,
        "openIssues": 1144,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:19:49Z"
      }
    },
    {
      "repo": "appwrite/appwrite",
      "score": 9.4,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "backend-as-a-service",
        "auth",
        "database",
        "storage"
      ],
      "languages": [
        "php"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 57570,
        "forks": 5762,
        "openIssues": 718,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T11:20:34Z"
      },
      "bestFor": [
        "backend-as-a-service applications",
        "authentication and identity",
        "application data persistence"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "pocketbase/pocketbase",
      "score": 9.4,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "backend-as-a-service",
        "database",
        "auth"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 61276,
        "forks": 3724,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-02T08:39:50Z"
      },
      "bestFor": [
        "backend-as-a-service applications",
        "application data persistence",
        "authentication and identity"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "prisma/prisma",
      "score": 9.5,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "orm",
        "database",
        "typescript"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 47693,
        "forks": 2546,
        "openIssues": 2764,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:09:45Z"
      },
      "bestFor": [
        "database ORM workflows",
        "application data persistence",
        "TypeScript application development"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "drizzle-team/drizzle-orm",
      "score": 9.5,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "orm",
        "database",
        "typescript"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35955,
        "forks": 1694,
        "openIssues": 2103,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T22:49:15Z"
      },
      "bestFor": [
        "database ORM workflows",
        "application data persistence",
        "TypeScript application development"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "fastapi/fastapi",
      "score": 9.8,
      "tier": "core",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "api",
        "python",
        "backend"
      ],
      "alternatives": [
        "nestjs/nest"
      ],
      "complements": [
        "postgres/postgres",
        "redis/redis",
        "supabase/supabase"
      ],
      "bestFor": [
        "Python APIs",
        "AI backends"
      ],
      "avoidWhen": [
        "TypeScript-only backend teams"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 102817,
        "forks": 9990,
        "openIssues": 84,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-02T11:36:38Z"
      }
    },
    {
      "repo": "nestjs/nest",
      "score": 9.6,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "api",
        "typescript",
        "backend"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 76788,
        "forks": 8573,
        "openIssues": 48,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:53:37Z"
      },
      "bestFor": [
        "TypeScript application development",
        "backend services"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "trpc/trpc",
      "score": 9.4,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "api",
        "typescript",
        "rpc"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 40689,
        "forks": 1700,
        "openIssues": 223,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T02:10:04Z"
      },
      "bestFor": [
        "TypeScript application development"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "graphql/graphql-js",
      "score": 9.4,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "graphql",
        "api"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 20345,
        "forks": 2113,
        "openIssues": 103,
        "archived": false,
        "disabled": false,
        "defaultBranch": "17.x.x",
        "license": "MIT",
        "pushedAt": "2026-09-28T15:37:21Z"
      },
      "bestFor": [
        "GraphQL APIs"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "apollographql/apollo-server",
      "score": 9.1,
      "tier": "recommended",
      "category": "Backend / API / données",
      "domain": "backend",
      "capabilities": [
        "graphql",
        "api",
        "backend"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13950,
        "forks": 2003,
        "openIssues": 89,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T23:24:08Z"
      },
      "bestFor": [
        "GraphQL APIs",
        "backend services"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "keycloak/keycloak",
      "score": 9.5,
      "tier": "recommended",
      "category": "Authentification / identité",
      "domain": "backend",
      "capabilities": [
        "auth",
        "identity",
        "sso"
      ],
      "languages": [
        "java"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 37140,
        "forks": 9010,
        "openIssues": 3230,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:02:20Z"
      },
      "bestFor": [
        "authentication and identity"
      ],
      "avoidWhen": [
        "projects requiring minimal setup and operational complexity",
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ory/kratos",
      "score": 9.2,
      "tier": "recommended",
      "category": "Authentification / identité",
      "domain": "backend",
      "capabilities": [
        "auth",
        "identity"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13907,
        "forks": 1189,
        "openIssues": 233,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-07-29T09:30:37Z"
      },
      "bestFor": [
        "authentication and identity"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "seaweedfs/seaweedfs",
      "score": 9.2,
      "tier": "recommended",
      "category": "Stockage objet / distribué",
      "domain": "backend",
      "capabilities": [
        "object-storage",
        "distributed-storage"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35250,
        "forks": 3038,
        "openIssues": 769,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:45:46Z"
      },
      "bestFor": [
        "object storage",
        "distributed storage systems"
      ],
      "avoidWhen": [
        "frontend-only UI work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "facebook/react",
      "score": 9.8,
      "tier": "core",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui",
        "frontend",
        "component-framework"
      ],
      "alternatives": [
        "flutter/flutter"
      ],
      "complements": [
        "vercel/next.js",
        "vitejs/vite",
        "shadcn-ui/ui"
      ],
      "bestFor": [
        "web UI",
        "component systems"
      ],
      "avoidWhen": [
        "native-only mobile apps"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 250901,
        "forks": 51437,
        "openIssues": 1414,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T21:13:55Z"
      }
    },
    {
      "repo": "vercel/next.js",
      "score": 9.8,
      "tier": "core",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "frontend",
        "fullstack",
        "ssr"
      ],
      "alternatives": [
        "vitejs/vite"
      ],
      "complements": [
        "facebook/react",
        "shadcn-ui/ui",
        "supabase/supabase"
      ],
      "bestFor": [
        "full-stack React web apps",
        "SSR"
      ],
      "avoidWhen": [
        "simple static SPA with minimal server needs"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 143185,
        "forks": 33970,
        "openIssues": 3545,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:53:16Z"
      }
    },
    {
      "repo": "vitejs/vite",
      "score": 9.7,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "frontend-build",
        "bundler"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 83153,
        "forks": 8824,
        "openIssues": 773,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:59:06Z"
      },
      "bestFor": [
        "frontend build pipelines",
        "JavaScript bundling"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "tailwindlabs/tailwindcss",
      "score": 9.7,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "css",
        "design-system"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 97772,
        "forks": 7533,
        "openIssues": 94,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-25T19:32:43Z"
      },
      "bestFor": [
        "frontend styling systems",
        "design systems"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "shadcn-ui/ui",
      "score": 9.8,
      "tier": "core",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-components",
        "design-system",
        "accessibility"
      ],
      "alternatives": [
        "mui/material-ui",
        "chakra-ui/chakra-ui"
      ],
      "complements": [
        "tailwindlabs/tailwindcss",
        "facebook/react"
      ],
      "bestFor": [
        "customizable React UI systems"
      ],
      "avoidWhen": [
        "teams wanting a fully opinionated component library"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 125131,
        "forks": 12212,
        "openIssues": 1802,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:44:32Z"
      }
    },
    {
      "repo": "mui/material-ui",
      "score": 9.5,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-components",
        "design-system"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 99131,
        "forks": 32507,
        "openIssues": 1474,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:11:20Z"
      },
      "bestFor": [
        "reusable UI component systems",
        "design systems"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "chakra-ui/chakra-ui",
      "score": 9.1,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-components",
        "design-system",
        "accessibility"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 40676,
        "forks": 3648,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-24T06:11:42Z"
      },
      "bestFor": [
        "reusable UI component systems",
        "design systems",
        "accessibility testing and remediation"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "microsoft/fluentui",
      "score": 9.1,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-components",
        "design-system"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 20310,
        "forks": 2941,
        "openIssues": 813,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:17:51Z"
      },
      "bestFor": [
        "reusable UI component systems",
        "design systems"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "storybookjs/storybook",
      "score": 9.7,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-components",
        "visual-testing",
        "documentation"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 91201,
        "forks": 10474,
        "openIssues": 1881,
        "archived": false,
        "disabled": false,
        "defaultBranch": "next",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:07:52Z"
      },
      "bestFor": [
        "reusable UI component systems",
        "technical documentation"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "motiondivision/motion",
      "score": 9.7,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "ui-animation",
        "frontend"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 33835,
        "forks": 1387,
        "openIssues": 106,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:52:36Z"
      },
      "bestFor": [
        "frontend application development"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "pmndrs/react-three-fiber",
      "score": 9.3,
      "tier": "recommended",
      "category": "Frontend / UI / design systems",
      "domain": "web_frontend",
      "capabilities": [
        "3d",
        "webgl",
        "react"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32732,
        "forks": 2005,
        "openIssues": 14,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:51:18Z"
      },
      "bestFor": [
        "3D application development",
        "WebGL rendering",
        "React application development"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "android/nowinandroid",
      "score": 9.7,
      "tier": "core",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 21880,
        "forks": 4655,
        "openIssues": 281,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:17:39Z"
      },
      "bestFor": [
        "modern Android architecture reference",
        "Jetpack Compose patterns",
        "reference app structure and testing"
      ],
      "avoidWhen": [
        "small production dependency needs",
        "cross-platform application development"
      ]
    },
    {
      "repo": "JetBrains/compose-multiplatform",
      "score": 9.6,
      "tier": "recommended",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 19404,
        "forks": 1431,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-03T03:10:17Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "flutter/flutter",
      "score": 9.7,
      "tier": "recommended",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin",
        "dart"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 179345,
        "forks": 33083,
        "openIssues": 13292,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T10:57:47Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "facebook/react-native",
      "score": 9.7,
      "tier": "core",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "typescript",
        "javascript",
        "java",
        "kotlin"
      ],
      "platforms": [
        "android",
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 126795,
        "forks": 25300,
        "openIssues": 1122,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:48:43Z"
      },
      "bestFor": [
        "cross-platform mobile applications",
        "shared JavaScript or TypeScript mobile UI",
        "native-module integration"
      ],
      "avoidWhen": [
        "pure native-only Android or iOS apps",
        "web-only frontends"
      ]
    },
    {
      "repo": "expo/expo",
      "score": 9.7,
      "tier": "core",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin",
        "typescript",
        "javascript"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 52570,
        "forks": 14378,
        "openIssues": 860,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:14:05Z"
      },
      "bestFor": [
        "React Native app delivery",
        "managed cross-platform mobile workflows",
        "rapid Android and iOS iteration"
      ],
      "avoidWhen": [
        "fully native-only mobile architecture",
        "minimal runtime dependency footprints"
      ]
    },
    {
      "repo": "appium/appium",
      "score": 9.5,
      "tier": "recommended",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 22044,
        "forks": 6290,
        "openIssues": 50,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:14:41Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "wix/Detox",
      "score": 9.2,
      "tier": "recommended",
      "category": "Mobile / Android / multiplateforme",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12033,
        "forks": 1909,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:34:09Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "GoogleChrome/lighthouse",
      "score": 9.8,
      "tier": "core",
      "category": "UX / accessibilité / qualité frontend",
      "domain": "web_frontend",
      "capabilities": [
        "performance-audit",
        "accessibility",
        "seo"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 30855,
        "forks": 9758,
        "openIssues": 469,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T12:06:06Z"
      },
      "bestFor": [
        "web performance audits",
        "accessibility and SEO diagnostics",
        "CI quality gates for web pages"
      ],
      "avoidWhen": [
        "native mobile profiling",
        "deep backend performance analysis"
      ]
    },
    {
      "repo": "dequelabs/axe-core",
      "score": 9.7,
      "tier": "recommended",
      "category": "UX / accessibilité / qualité frontend",
      "domain": "web_frontend",
      "capabilities": [
        "accessibility",
        "testing"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7596,
        "forks": 953,
        "openIssues": 434,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MPL-2.0",
        "pushedAt": "2026-10-02T16:02:31Z"
      },
      "bestFor": [
        "accessibility testing and remediation",
        "automated testing"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "dagger/dagger",
      "score": 9.6,
      "tier": "core",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "ci-cd",
        "pipelines",
        "containers"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 16315,
        "forks": 933,
        "openIssues": 217,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T07:08:57Z"
      },
      "bestFor": [
        "portable CI pipelines",
        "containerized build automation",
        "CI/CD logic as code"
      ],
      "avoidWhen": [
        "very simple static CI jobs",
        "environments without container support"
      ]
    },
    {
      "repo": "nektos/act",
      "score": 9.4,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "github-actions",
        "local-ci"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 72214,
        "forks": 2055,
        "openIssues": 385,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-09T22:50:11Z"
      },
      "bestFor": [
        "GitHub Actions workflows",
        "local CI validation"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "earthly/earthly",
      "score": 9.1,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "build-system",
        "ci-cd",
        "containers"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12052,
        "forks": 461,
        "openIssues": 744,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MPL-2.0",
        "pushedAt": "2025-10-23T20:10:46Z"
      },
      "bestFor": [
        "build automation",
        "CI/CD pipelines",
        "container workflows"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "docker/compose",
      "score": 9.7,
      "tier": "core",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "containers",
        "orchestration"
      ],
      "alternatives": [
        "podman-container-tools/podman"
      ],
      "complements": [
        "dagger/dagger",
        "prometheus/prometheus"
      ],
      "bestFor": [
        "local multi-service stacks"
      ],
      "avoidWhen": [
        "large-scale cluster orchestration"
      ],
      "languages": [
        "kotlin"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 38285,
        "forks": 5850,
        "openIssues": 90,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T15:37:02Z"
      }
    },
    {
      "repo": "podman-container-tools/podman",
      "score": 9.5,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "containers",
        "runtime"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32996,
        "forks": 3398,
        "openIssues": 1024,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T19:24:12Z"
      },
      "bestFor": [
        "container workflows",
        "container runtime operations"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "kubernetes/kubernetes",
      "score": 9.6,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "containers",
        "orchestration"
      ],
      "alternatives": [],
      "complements": [
        "helm/helm",
        "argoproj/argo-cd",
        "prometheus/prometheus"
      ],
      "bestFor": [
        "cluster orchestration",
        "production scale"
      ],
      "avoidWhen": [
        "small single-host deployments"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 128294,
        "forks": 46084,
        "openIssues": 3170,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:06:37Z"
      }
    },
    {
      "repo": "helm/helm",
      "score": 9.4,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "kubernetes",
        "package-management"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 30304,
        "forks": 7826,
        "openIssues": 487,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T21:34:53Z"
      },
      "bestFor": [
        "Kubernetes operations"
      ],
      "avoidWhen": [
        "low-resource environments",
        "projects requiring minimal setup and operational complexity"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "opentofu/opentofu",
      "score": 9.5,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "iac",
        "infrastructure"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 30387,
        "forks": 1386,
        "openIssues": 328,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MPL-2.0",
        "pushedAt": "2026-10-02T19:40:24Z"
      },
      "bestFor": [
        "infrastructure as code",
        "infrastructure management"
      ],
      "avoidWhen": [
        "projects requiring minimal setup and operational complexity",
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "hashicorp/terraform",
      "score": 9.2,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "iac",
        "infrastructure"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 49829,
        "forks": 10639,
        "openIssues": 1938,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BUSL-1.1",
        "pushedAt": "2026-10-05T11:15:56Z"
      },
      "bestFor": [
        "infrastructure as code",
        "infrastructure management"
      ],
      "avoidWhen": [
        "projects requiring minimal setup and operational complexity",
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ansible/ansible",
      "score": 9.4,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "configuration-management",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 70860,
        "forks": 24343,
        "openIssues": 868,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-02T21:01:26Z"
      },
      "bestFor": [
        "workflow automation"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "argoproj/argo-cd",
      "score": 9.5,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "gitops",
        "deployment",
        "kubernetes"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 24327,
        "forks": 7911,
        "openIssues": 4416,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T09:48:20Z"
      },
      "bestFor": [
        "application deployment",
        "Kubernetes operations"
      ],
      "avoidWhen": [
        "low-resource environments",
        "projects requiring minimal setup and operational complexity"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "fluxcd/flux2",
      "score": 9.2,
      "tier": "recommended",
      "category": "DevOps / CI-CD / infrastructure",
      "domain": "devops",
      "capabilities": [
        "gitops",
        "deployment",
        "kubernetes"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 8435,
        "forks": 792,
        "openIssues": 257,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-03T20:23:14Z"
      },
      "bestFor": [
        "application deployment",
        "Kubernetes operations"
      ],
      "avoidWhen": [
        "low-resource environments",
        "projects requiring minimal setup and operational complexity"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "prometheus/prometheus",
      "score": 9.7,
      "tier": "core",
      "category": "Monitoring / production / releases",
      "domain": "devops",
      "capabilities": [
        "observability"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 66366,
        "forks": 10893,
        "openIssues": 940,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:20:20Z"
      },
      "bestFor": [
        "metrics collection",
        "time-series monitoring",
        "cloud-native monitoring foundations"
      ],
      "avoidWhen": [
        "log storage",
        "full distributed tracing without complementary tooling"
      ]
    },
    {
      "repo": "grafana/grafana",
      "score": 9.7,
      "tier": "core",
      "category": "Monitoring / production / releases",
      "domain": "devops",
      "capabilities": [
        "observability"
      ],
      "alternatives": [],
      "complements": [
        "prometheus/prometheus",
        "getsentry/sentry"
      ],
      "bestFor": [
        "dashboards",
        "operational observability"
      ],
      "avoidWhen": [
        "no telemetry sources available"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 77085,
        "forks": 14819,
        "openIssues": 3280,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T11:21:52Z"
      }
    },
    {
      "repo": "getsentry/sentry",
      "score": 9.5,
      "tier": "recommended",
      "category": "Monitoring / production / releases",
      "domain": "devops",
      "capabilities": [
        "observability"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45471,
        "forks": 4908,
        "openIssues": 2293,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "FSL-1.1-Apache-2.0",
        "pushedAt": "2026-10-05T11:19:07Z"
      },
      "bestFor": [
        "monitoring and observability"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "semantic-release/semantic-release",
      "score": 9.2,
      "tier": "recommended",
      "category": "Monitoring / production / releases",
      "domain": "devops",
      "capabilities": [
        "observability"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 24086,
        "forks": 1809,
        "openIssues": 404,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-04T06:35:24Z"
      },
      "bestFor": [
        "monitoring and observability"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "release-it/release-it",
      "score": 8.9,
      "tier": "specialized",
      "category": "Monitoring / production / releases",
      "domain": "devops",
      "capabilities": [
        "observability"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9065,
        "forks": 574,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T06:47:25Z"
      },
      "bestFor": [
        "monitoring and observability"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "tree-sitter/tree-sitter",
      "score": 9.8,
      "tier": "core",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "ast",
        "parsing",
        "code-analysis"
      ],
      "alternatives": [
        "ast-grep/ast-grep"
      ],
      "complements": [
        "sourcegraph/zoekt",
        "semgrep/semgrep"
      ],
      "bestFor": [
        "AST parsing",
        "multi-language code intelligence"
      ],
      "avoidWhen": [
        "simple text search is sufficient"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 27124,
        "forks": 2935,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:31:53Z"
      }
    },
    {
      "repo": "semgrep/semgrep",
      "score": 9.6,
      "tier": "recommended",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "static-analysis",
        "security-scanning"
      ],
      "alternatives": [
        "github/codeql"
      ],
      "complements": [
        "tree-sitter/tree-sitter",
        "microsoft/playwright"
      ],
      "bestFor": [
        "fast static analysis",
        "policy checks"
      ],
      "avoidWhen": [
        "deep whole-program query analysis is required"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 16877,
        "forks": 1089,
        "openIssues": 943,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-2.1",
        "pushedAt": "2026-10-05T00:02:23Z"
      }
    },
    {
      "repo": "github/codeql",
      "score": 9.6,
      "tier": "recommended",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "static-analysis",
        "security-scanning"
      ],
      "languages": [
        "codeql"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10165,
        "forks": 2109,
        "openIssues": 1479,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:04:58Z"
      },
      "bestFor": [
        "static analysis",
        "security scanning"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ast-grep/ast-grep",
      "score": 9.5,
      "tier": "recommended",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "ast",
        "code-search",
        "refactoring"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 16121,
        "forks": 468,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:44:04Z"
      },
      "bestFor": [
        "AST-based code analysis",
        "code search and indexing",
        "large-scale code refactoring"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "sourcegraph/zoekt",
      "score": 9.2,
      "tier": "recommended",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "code-search",
        "indexing"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1948,
        "forks": 246,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-23T06:40:47Z"
      },
      "bestFor": [
        "code search and indexing"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "comby-tools/comby",
      "score": 8.7,
      "tier": "specialized",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "code-transformation",
        "refactoring"
      ],
      "languages": [
        "ocaml"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2680,
        "forks": 75,
        "openIssues": 86,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-06-08T07:27:09Z"
      },
      "bestFor": [
        "large-scale code refactoring"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "astral-sh/uv",
      "score": 9.7,
      "tier": "core",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "python",
        "package-management",
        "environment-management"
      ],
      "languages": [
        "python",
        "rust"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 90406,
        "forks": 3627,
        "openIssues": 2946,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:44:19Z"
      },
      "bestFor": [
        "Python dependency management",
        "fast virtual environments",
        "reproducible Python tooling"
      ],
      "avoidWhen": [
        "non-Python package management",
        "Conda-specific environment workflows"
      ]
    },
    {
      "repo": "benfred/py-spy",
      "score": 9,
      "tier": "recommended",
      "category": "Analyse de code / transformation / qualité",
      "domain": "software_engineering",
      "capabilities": [
        "profiling",
        "python"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15539,
        "forks": 552,
        "openIssues": 235,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T01:35:59Z"
      },
      "bestFor": [
        "performance profiling",
        "Python development"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "HypothesisWorks/hypothesis",
      "score": 9.5,
      "tier": "recommended",
      "category": "Tests génératifs / fuzzing",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9045,
        "forks": 686,
        "openIssues": 53,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MPL-2.0",
        "pushedAt": "2026-10-05T04:13:18Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "google/oss-fuzz",
      "score": 9.2,
      "tier": "recommended",
      "category": "Tests génératifs / fuzzing",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12694,
        "forks": 2913,
        "openIssues": 794,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T09:43:16Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "boxed/mutmut",
      "score": 8.8,
      "tier": "specialized",
      "category": "Tests génératifs / fuzzing",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1466,
        "forks": 179,
        "openIssues": 64,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-12T22:05:54Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "microsoft/playwright",
      "score": 9.8,
      "tier": "core",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "alternatives": [
        "appium/appium",
        "wix/Detox"
      ],
      "complements": [
        "storybookjs/storybook",
        "GoogleChrome/lighthouse"
      ],
      "bestFor": [
        "browser E2E",
        "cross-browser testing"
      ],
      "avoidWhen": [
        "native mobile-only testing"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 97108,
        "forks": 6547,
        "openIssues": 219,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:02:19Z"
      }
    },
    {
      "repo": "pytest-dev/pytest",
      "score": 9.7,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 14565,
        "forks": 3442,
        "openIssues": 858,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:33:22Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "astral-sh/ruff",
      "score": 9.7,
      "tier": "core",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 49911,
        "forks": 2474,
        "openIssues": 2197,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:00:37Z"
      },
      "bestFor": [
        "fast Python linting",
        "Python formatting and static checks",
        "CI code-quality enforcement"
      ],
      "avoidWhen": [
        "non-Python codebases",
        "semantic type checking"
      ]
    },
    {
      "repo": "langfuse/langfuse",
      "score": 9.6,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "observability",
        "code-quality"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35392,
        "forks": 3920,
        "openIssues": 1002,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:25:02Z"
      },
      "bestFor": [
        "monitoring and observability",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "promptfoo/promptfoo",
      "score": 9.6,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25714,
        "forks": 2439,
        "openIssues": 716,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:21:54Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "confident-ai/deepeval",
      "score": 9.4,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 18637,
        "forks": 2022,
        "openIssues": 705,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T07:44:31Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Arize-ai/phoenix",
      "score": 9.3,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11710,
        "forks": 1182,
        "openIssues": 1109,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Elastic-2.0",
        "pushedAt": "2026-10-04T14:38:21Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "EleutherAI/lm-evaluation-harness",
      "score": 9.3,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14130,
        "forks": 3640,
        "openIssues": 1119,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T10:51:06Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "openai/evals",
      "score": 8.8,
      "tier": "specialized",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 19552,
        "forks": 3104,
        "openIssues": 344,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-04-14T15:29:57Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "testcontainers/testcontainers-python",
      "score": 9,
      "tier": "recommended",
      "category": "Tests / évaluation / observabilité",
      "domain": "software_engineering",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2310,
        "forks": 389,
        "openIssues": 190,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T23:33:51Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "e2b-dev/E2B",
      "score": 9.5,
      "tier": "recommended",
      "category": "Sandboxing / exécution isolée",
      "domain": "software_engineering",
      "capabilities": [
        "sandbox",
        "code-execution"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14177,
        "forks": 1089,
        "openIssues": 96,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T07:16:56Z"
      },
      "bestFor": [
        "isolated code execution"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "firecracker-microvm/firecracker",
      "score": 9.4,
      "tier": "recommended",
      "category": "Sandboxing / exécution isolée",
      "domain": "devops",
      "capabilities": [
        "sandbox",
        "microvm",
        "isolation"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 37164,
        "forks": 2656,
        "openIssues": 94,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T13:45:21Z"
      },
      "bestFor": [
        "isolated code execution"
      ],
      "avoidWhen": [
        "projects requiring minimal setup and operational complexity",
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "motion-canvas/motion-canvas",
      "score": 9.5,
      "tier": "core",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "alternatives": [
        "svgdotjs/svg.js",
        "paperjs/paper.js"
      ],
      "complements": [
        "airbnb/lottie-web"
      ],
      "bestFor": [
        "programmatic vector animation",
        "TypeScript motion graphics"
      ],
      "avoidWhen": [
        "native mobile runtime-only playback"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 19233,
        "forks": 830,
        "openIssues": 174,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-02T20:01:32Z"
      }
    },
    {
      "repo": "svgdotjs/svg.js",
      "score": 9.3,
      "tier": "recommended",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11825,
        "forks": 1078,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-04T07:48:43Z"
      },
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "airbnb/lottie-web",
      "score": 9.1,
      "tier": "recommended",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "alternatives": [
        "rive-app/rive-android",
        "EsotericSoftware/spine-runtimes"
      ],
      "complements": [
        "motion-canvas/motion-canvas"
      ],
      "bestFor": [
        "vector animation playback on web"
      ],
      "avoidWhen": [
        "complex interactive state-machine animation"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32143,
        "forks": 2940,
        "openIssues": 857,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2025-09-01T09:01:31Z"
      }
    },
    {
      "repo": "paperjs/paper.js",
      "score": 8.9,
      "tier": "specialized",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15081,
        "forks": 1256,
        "openIssues": 430,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2024-07-23T00:58:54Z"
      },
      "lifecycle": "stable",
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "jonobr1/two.js",
      "score": 8.6,
      "tier": "specialized",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8664,
        "forks": 463,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "MIT",
        "pushedAt": "2026-09-29T00:27:18Z"
      },
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "rough-stuff/rough",
      "score": 8.4,
      "tier": "specialized",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 21233,
        "forks": 663,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-07-28T21:12:58Z"
      },
      "lifecycle": "stable",
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "maxwellito/vivus",
      "score": 8.1,
      "tier": "specialized",
      "category": "Graphisme vectoriel / animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15484,
        "forks": 1123,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2022-07-06T22:16:59Z"
      },
      "lifecycle": "stable",
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "CorentinJ/Real-Time-Voice-Cloning",
      "score": 8.3,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 60168,
        "forks": 9381,
        "openIssues": 177,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-03-09T10:31:58Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vega-org/vega-app",
      "score": 8.5,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "visualization",
        "graphics"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1495,
        "forks": 206,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:36:31Z"
      },
      "bestFor": [
        "visualization workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "RVC-Project/Retrieval-based-Voice-Conversion-WebUI",
      "score": 9,
      "tier": "recommended",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 38598,
        "forks": 5294,
        "openIssues": 584,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-04T07:47:32Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "camenduru/SMPLer-X-colab",
      "score": 7.8,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "3d-human",
        "colab"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 69,
        "forks": 4,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2024-03-03T16:36:55Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "external-terms"
    },
    {
      "repo": "deepfakes/faceswap",
      "score": 8.2,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "face-swap",
        "video"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 57567,
        "forks": 13457,
        "openIssues": 16,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-08-05T11:39:37Z"
      },
      "bestFor": [
        "video-generation workflows"
      ],
      "avoidWhen": [
        "low-resource environments",
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Tencent-Hunyuan/HunyuanVideo",
      "score": 9.3,
      "tier": "recommended",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "video"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12588,
        "forks": 1344,
        "openIssues": 186,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-06-29T09:33:50Z"
      },
      "bestFor": [
        "video-generation workflows"
      ],
      "avoidWhen": [
        "low-resource environments",
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "dream80/roop_colab",
      "score": 7.4,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "face-swap",
        "colab"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 901,
        "forks": 314,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2025-08-19T01:37:38Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "hacksider/Deep-Live-Cam",
      "score": 8.8,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "face-swap",
        "realtime-video"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 96913,
        "forks": 14120,
        "openIssues": 46,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T00:58:03Z"
      },
      "bestFor": [
        "face swap workflows"
      ],
      "avoidWhen": [
        "low-resource environments",
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "camenduru/dust3r-jupyter",
      "score": 8,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "3d-reconstruction",
        "notebooks"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 24,
        "forks": 1,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2024-03-03T13:43:09Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "historical DUSt3R Colab/Jupyter setup reference"
      ],
      "avoidWhen": [
        "current 3D reconstruction workflows",
        "maintained notebook environments"
      ],
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "RayVentura/ShortGPT",
      "score": 8,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8002,
        "forks": 1159,
        "openIssues": 86,
        "archived": false,
        "disabled": false,
        "defaultBranch": "stable",
        "license": "MIT",
        "pushedAt": "2025-02-10T19:33:18Z"
      },
      "bestFor": [
        "workflow automation"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "FujiwaraChoki/MoneyPrinterV2",
      "score": 8.1,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32039,
        "forks": 3443,
        "openIssues": 92,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-15T22:35:17Z"
      },
      "bestFor": [
        "workflow automation"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "FujiwaraChoki/MoneyPrinter",
      "score": 7.8,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14024,
        "forks": 1823,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-03-26T22:17:17Z"
      }
    },
    {
      "repo": "KRTirtho/spotube",
      "score": 8.6,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "music",
        "streaming-client"
      ],
      "languages": [
        "dart"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49619,
        "forks": 2323,
        "openIssues": 867,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-02T14:57:54Z"
      },
      "bestFor": [
        "music workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ali-vilab/AnyDoor",
      "score": 8.5,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "object-insertion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4241,
        "forks": 371,
        "openIssues": 64,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2024-04-08T06:31:26Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "research reference for object insertion"
      ],
      "avoidWhen": [
        "new production image-editing pipelines",
        "actively maintained image models"
      ]
    },
    {
      "repo": "facefusion/facefusion",
      "score": 8.9,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "face-swap",
        "video"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 30137,
        "forks": 4922,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "OpenRAIL-AS",
        "pushedAt": "2026-10-05T09:30:07Z"
      },
      "bestFor": [
        "video-generation workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "SociallyIneptWeeb/AICoverGen",
      "score": 7.8,
      "tier": "audit",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "voice-conversion",
        "music"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1445,
        "forks": 362,
        "openIssues": 96,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-02-15T08:09:40Z"
      }
    },
    {
      "repo": "debpalash/VoiceStudio",
      "score": 8,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 53414,
        "forks": 5954,
        "openIssues": 60,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T09:47:38Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "comfyanonymous/ComfyUI",
      "score": 9.7,
      "tier": "core",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "workflow",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 136138,
        "forks": 16143,
        "openIssues": 5059,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-05T04:16:59Z"
      },
      "bestFor": [
        "node-based diffusion workflows",
        "local image-generation pipelines",
        "reproducible generative-media graphs"
      ],
      "avoidWhen": [
        "low-resource devices",
        "simple one-shot API-only image generation"
      ]
    },
    {
      "repo": "invoke-ai/InvokeAI",
      "score": 9.1,
      "tier": "recommended",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 28345,
        "forks": 2986,
        "openIssues": 408,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:22:29Z"
      },
      "bestFor": [
        "image-generation workflows",
        "diffusion-model workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mudler/LocalAI",
      "score": 9.3,
      "tier": "recommended",
      "category": "Infrastructure IA locale",
      "domain": "devops",
      "capabilities": [
        "local-inference",
        "model-serving"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49392,
        "forks": 4483,
        "openIssues": 189,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:25:29Z"
      },
      "bestFor": [
        "local inference workflows"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "swisskyrepo/PayloadsAllTheThings",
      "score": 9.5,
      "tier": "recommended",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 81481,
        "forks": 17435,
        "openIssues": 36,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-27T07:52:21Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "megadose/holehe",
      "score": 8.5,
      "tier": "audit",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15088,
        "forks": 1943,
        "openIssues": 117,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2024-09-10T20:24:32Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy OSINT workflow reference"
      ],
      "avoidWhen": [
        "fresh provider coverage",
        "production OSINT automation"
      ]
    },
    {
      "repo": "usestrix/strix",
      "score": 9,
      "tier": "recommended",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 66564,
        "forks": 7306,
        "openIssues": 436,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T02:37:22Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "0x4m4/hexstrike-ai",
      "score": 8.8,
      "tier": "specialized",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12392,
        "forks": 2524,
        "openIssues": 114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-03T14:33:09Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "CVEProject/cvelistV5",
      "score": 9.4,
      "tier": "recommended",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3030,
        "forks": 651,
        "openIssues": 51,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-05T11:24:53Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "bilawalsidhu/gods-eye-view",
      "score": 7.8,
      "tier": "audit",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 47697,
        "forks": 9727,
        "openIssues": 294,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:17:10Z"
      }
    },
    {
      "repo": "duty1g/x64dbg-mcp-server",
      "score": 8.4,
      "tier": "specialized",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "zig"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2192,
        "forks": 223,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T07:13:53Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Narasimha1997/fake-sms",
      "score": 6.8,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "productivity",
      "capabilities": [
        "messaging",
        "simulation"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2793,
        "forks": 186,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-2.0",
        "pushedAt": "2023-08-01T15:34:41Z"
      }
    },
    {
      "repo": "massgravel/Microsoft-Activation-Scripts",
      "score": 8.6,
      "tier": "specialized",
      "category": "Autres favoris visibles",
      "domain": "productivity",
      "capabilities": [
        "windows",
        "activation"
      ],
      "languages": [
        "batchfile"
      ],
      "platforms": [
        "windows"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 193402,
        "forks": 18350,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-10T22:33:44Z"
      },
      "bestFor": [
        "windows workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "friuns2/BlackFriday-GPTs-Prompts",
      "score": 7.2,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "prompt-library"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 9792,
        "forks": 1386,
        "openIssues": 222,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-03-18T02:09:18Z"
      }
    },
    {
      "repo": "charlesbel/Microsoft-Rewards-Farmer",
      "score": 7.5,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1137,
        "forks": 311,
        "openIssues": 104,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-08-05T01:55:49Z"
      },
      "bestFor": [
        "legacy Microsoft Rewards automation reference"
      ],
      "avoidWhen": [
        "actively maintained automation",
        "account-safe production use"
      ],
      "lifecycle": "legacy"
    },
    {
      "repo": "lllyasviel/Paints-UNDO",
      "score": 9,
      "tier": "recommended",
      "category": "Autres favoris visibles",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "image-editing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4062,
        "forks": 395,
        "openIssues": 70,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-08-13T22:11:05Z"
      },
      "bestFor": [
        "image-generation workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bleedline/aimoneyhunter",
      "score": 7,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "automation"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 18224,
        "forks": 1766,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2025-10-20T00:24:54Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "LargeWorldModel/LWM",
      "score": 8.7,
      "tier": "specialized",
      "category": "Autres favoris visibles",
      "domain": "ai_media",
      "capabilities": [
        "multimodal",
        "world-model"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7426,
        "forks": 562,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-10-19T03:27:38Z"
      },
      "bestFor": [
        "multimodal workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "teacat/chaturbate-dvr",
      "score": 6.5,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "video-recording"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 261,
        "forks": 64,
        "openIssues": 20,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2025-11-03T00:34:43Z"
      },
      "bestFor": [
        "legacy stream-recording reference"
      ],
      "avoidWhen": [
        "new deployments",
        "actively maintained recording tooling"
      ],
      "lifecycle": "legacy"
    },
    {
      "repo": "GuallaGang508/SMSBotBypass",
      "score": 5.5,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "messaging",
        "automation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 511,
        "forks": 134,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2024-06-27T21:58:30Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "Cyb0r9/SocialBox",
      "score": 6.2,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "cybersecurity",
      "capabilities": [
        "osint",
        "social-media"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2060,
        "forks": 543,
        "openIssues": 87,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2023-11-09T06:20:39Z"
      }
    },
    {
      "repo": "Ha3MrX/InstaBrute",
      "score": 5.8,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "cybersecurity",
      "capabilities": [
        "credential-testing",
        "social-media"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1559,
        "forks": 292,
        "openIssues": 62,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-06-10T19:03:50Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "GH05T-HUNTER5/GH05T-INSTA",
      "score": 5.5,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "social-media",
        "automation"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 851,
        "forks": 158,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GH05T-HUNTER5 Software License",
        "pushedAt": "2024-07-20T06:09:18Z"
      },
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "ShadowHackrs/Gmail-infinity",
      "score": 5.8,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "other",
      "capabilities": [
        "email",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1033,
        "forks": 232,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-16T21:16:57Z"
      },
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "custom-restrictive"
    },
    {
      "repo": "alsk1992/CloddsBot",
      "score": 6.8,
      "tier": "audit",
      "category": "Trading / AI agents",
      "domain": "trading",
      "capabilities": [
        "trading",
        "automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2892,
        "forks": 338,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T19:37:29Z"
      },
      "roles": [
        "alpha",
        "execution",
        "portfolio",
        "risk"
      ]
    },
    {
      "repo": "BloodOnTop/Stealerium",
      "score": 4,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "cybersecurity",
      "capabilities": [
        "malware-research"
      ],
      "languages": [
        "c#"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 94,
        "forks": 35,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2023-08-18T14:18:01Z"
      }
    },
    {
      "repo": "QuantConnect/Lean",
      "score": 9.9,
      "tier": "core",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest",
        "execution",
        "portfolio",
        "xauusd"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "execution",
        "risk",
        "code-quality",
        "backtest",
        "portfolio",
        "xauusd"
      ],
      "alternatives": [
        "nautechsystems/nautilus_trader",
        "polakowo/vectorbt"
      ],
      "complements": [
        "OpenBB-finance/OpenBB",
        "ranaroussi/quantstats",
        "dcajasn/Riskfolio-Lib"
      ],
      "bestFor": [
        "multi-asset backtesting",
        "live trading"
      ],
      "avoidWhen": [
        "ultra-light exploratory notebooks"
      ],
      "languages": [
        "c++",
        "c#"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 21861,
        "forks": 5282,
        "openIssues": 260,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T20:57:46Z"
      }
    },
    {
      "repo": "nautechsystems/nautilus_trader",
      "score": 9.8,
      "tier": "core",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest",
        "execution",
        "microstructure"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "execution",
        "code-quality",
        "backtest",
        "microstructure"
      ],
      "alternatives": [
        "QuantConnect/Lean",
        "freqtrade/freqtrade"
      ],
      "complements": [
        "OpenBB-finance/OpenBB",
        "ranaroussi/quantstats"
      ],
      "bestFor": [
        "event-driven trading",
        "execution realism"
      ],
      "avoidWhen": [
        "very simple strategy research"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 29626,
        "forks": 3925,
        "openIssues": 153,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-3.0",
        "pushedAt": "2026-10-05T08:06:02Z"
      }
    },
    {
      "repo": "polakowo/vectorbt",
      "score": 9.7,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest",
        "alpha",
        "risk",
        "portfolio"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "memory",
        "backtesting",
        "risk",
        "vector-animation",
        "code-quality",
        "backtest",
        "alpha",
        "portfolio"
      ],
      "alternatives": [
        "kernc/backtesting.py",
        "QuantConnect/Lean"
      ],
      "complements": [
        "optuna/optuna",
        "ranaroussi/quantstats"
      ],
      "bestFor": [
        "fast vectorized research",
        "parameter sweeps"
      ],
      "avoidWhen": [
        "high-fidelity event-driven execution simulation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9274,
        "forks": 1184,
        "openIssues": 139,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-26T11:27:49Z"
      }
    },
    {
      "repo": "microsoft/qlib",
      "score": 9.7,
      "tier": "core",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "backtest"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "machine-learning",
        "code-quality",
        "alpha",
        "ml",
        "backtest"
      ],
      "alternatives": [
        "AI4Finance-Foundation/FinRL"
      ],
      "complements": [
        "dmlc/xgboost",
        "catboost/catboost",
        "shap/shap"
      ],
      "bestFor": [
        "quant ML research",
        "alpha modeling"
      ],
      "avoidWhen": [
        "manual discretionary-only trading"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49146,
        "forks": 7763,
        "openIssues": 487,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-22T05:57:23Z"
      }
    },
    {
      "repo": "ccxt/ccxt",
      "score": 9.7,
      "tier": "core",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "data",
        "execution"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "execution",
        "market-data",
        "code-quality",
        "data"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 44251,
        "forks": 8872,
        "openIssues": 714,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:27:02Z"
      },
      "bestFor": [
        "multi-exchange crypto market data",
        "normalized exchange APIs",
        "crypto execution integrations"
      ],
      "avoidWhen": [
        "broker-specific low-latency execution",
        "non-crypto-only trading stacks"
      ]
    },
    {
      "repo": "freqtrade/freqtrade",
      "score": 9.6,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest",
        "execution",
        "alpha",
        "risk"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "execution",
        "risk",
        "code-quality",
        "backtest",
        "alpha"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 55035,
        "forks": 11380,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-05T05:03:12Z"
      },
      "bestFor": [
        "strategy backtesting",
        "trading execution systems",
        "risk analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "hummingbot/hummingbot",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "execution",
        "microstructure"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "execution",
        "code-quality",
        "microstructure"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 20303,
        "forks": 4977,
        "openIssues": 180,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-28T10:50:41Z"
      },
      "bestFor": [
        "strategy backtesting",
        "trading execution systems",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "AI4Finance-Foundation/FinRL",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "portfolio"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "risk",
        "machine-learning",
        "code-quality",
        "alpha",
        "ml",
        "portfolio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 16554,
        "forks": 3538,
        "openIssues": 308,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-28T23:32:46Z"
      },
      "bestFor": [
        "strategy backtesting",
        "risk analysis",
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "kernc/backtesting.py",
      "score": 9.3,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "code-quality",
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9010,
        "forks": 1543,
        "openIssues": 93,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-08-05T12:39:16Z"
      },
      "bestFor": [
        "strategy backtesting",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vnpy/vnpy",
      "score": 9.3,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "execution",
        "backtest"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "execution",
        "code-quality",
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45699,
        "forks": 12499,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T01:06:17Z"
      },
      "bestFor": [
        "strategy backtesting",
        "trading execution systems",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "TA-Lib/ta-lib-python",
      "score": 9.2,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "alpha"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "code-quality",
        "alpha"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 12266,
        "forks": 2003,
        "openIssues": 134,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-2-Clause",
        "pushedAt": "2026-09-21T16:37:09Z"
      },
      "bestFor": [
        "strategy backtesting",
        "code-quality automation",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ranaroussi/yfinance",
      "score": 9.1,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "data",
        "macro"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "market-data",
        "code-quality",
        "data",
        "macro"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 25431,
        "forks": 3434,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T12:26:33Z"
      },
      "bestFor": [
        "strategy backtesting",
        "market-data ingestion",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "stefan-jansen/machine-learning-for-trading",
      "score": 9.1,
      "tier": "recommended",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "backtest"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "backtesting",
        "machine-learning",
        "code-quality",
        "alpha",
        "ml",
        "backtest"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 21225,
        "forks": 5677,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T13:24:46Z"
      },
      "bestFor": [
        "strategy backtesting",
        "machine-learning workflows",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "pmorissette/bt",
      "score": 8.9,
      "tier": "specialized",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest",
        "portfolio"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "backtesting",
        "risk",
        "code-quality",
        "backtest",
        "portfolio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2993,
        "forks": 500,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-03T22:55:37Z"
      },
      "bestFor": [
        "strategy backtesting",
        "risk analysis",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mementum/backtrader",
      "score": 8.7,
      "tier": "audit",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "backtesting",
        "code-quality",
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 23394,
        "forks": 5297,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2024-08-19T17:47:36Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy Backtrader projects",
        "historical event-driven backtesting reference"
      ],
      "avoidWhen": [
        "new trading systems",
        "actively maintained backtesting framework"
      ],
      "alternatives": [
        "kernc/backtesting.py",
        "polakowo/vectorbt",
        "QuantConnect/Lean"
      ]
    },
    {
      "repo": "quantopian/zipline",
      "score": 8.3,
      "tier": "audit",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "backtest"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "backtesting",
        "code-quality",
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 20136,
        "forks": 5046,
        "openIssues": 367,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2024-02-13T08:02:51Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy Quantopian Zipline code",
        "historical Zipline API reference"
      ],
      "avoidWhen": [
        "new backtesting projects",
        "modern Python environments"
      ],
      "alternatives": [
        "stefan-jansen/zipline-reloaded",
        "QuantConnect/Lean",
        "kernc/backtesting.py"
      ]
    },
    {
      "repo": "hudson-and-thames/mlfinlab",
      "score": 8.2,
      "tier": "audit",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "roles": [
        "alpha",
        "risk",
        "microstructure"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "backtesting",
        "risk",
        "machine-learning",
        "code-quality",
        "alpha",
        "microstructure"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4935,
        "forks": 1291,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Hudson & Thames Proprietary License",
        "pushedAt": "2023-10-02T03:05:19Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy financial-ML research reference"
      ],
      "avoidWhen": [
        "new production research pipelines",
        "actively maintained open-source financial ML"
      ],
      "alternatives": [
        "microsoft/qlib",
        "skfolio/skfolio",
        "polakowo/vectorbt"
      ],
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "skfolio/skfolio",
      "score": 9.7,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "portfolio",
        "risk",
        "backtest"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "backtesting",
        "risk",
        "code-quality",
        "portfolio",
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2460,
        "forks": 266,
        "openIssues": 35,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-03T14:31:59Z"
      },
      "bestFor": [
        "strategy backtesting",
        "risk analysis",
        "code-quality automation"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "PyPortfolio/PyPortfolioOpt",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "portfolio",
        "risk"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "risk",
        "portfolio"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6073,
        "forks": 1176,
        "openIssues": 117,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-07T21:18:14Z"
      },
      "bestFor": [
        "risk analysis",
        "portfolio construction and analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "dcajasn/Riskfolio-Lib",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "portfolio",
        "risk"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "risk",
        "portfolio"
      ],
      "alternatives": [
        "PyPortfolio/PyPortfolioOpt",
        "skfolio/skfolio"
      ],
      "complements": [
        "ranaroussi/quantstats"
      ],
      "bestFor": [
        "portfolio risk optimization",
        "risk parity"
      ],
      "avoidWhen": [
        "single-position strategies without allocation needs"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4533,
        "forks": 718,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-04T20:35:18Z"
      }
    },
    {
      "repo": "ranaroussi/quantstats",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "risk",
        "performance"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "risk",
        "performance"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 7677,
        "forks": 1246,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-27T19:40:19Z"
      },
      "bestFor": [
        "risk analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "statsmodels/statsmodels",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "alpha",
        "regime",
        "macro"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "alpha",
        "regime",
        "macro"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11671,
        "forks": 3616,
        "openIssues": 2798,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T11:12:05Z"
      },
      "bestFor": [
        "quantitative alpha research",
        "market regime analysis",
        "macroeconomic analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bashtage/arch",
      "score": 9.2,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "risk",
        "regime",
        "volatility"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "risk",
        "regime",
        "volatility"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1586,
        "forks": 297,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T08:00:31Z"
      },
      "bestFor": [
        "risk analysis",
        "market regime analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "optuna/optuna",
      "score": 9.6,
      "tier": "recommended",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "alpha",
        "optimization",
        "ml"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "machine-learning",
        "optimization",
        "alpha",
        "ml"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14886,
        "forks": 1408,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-30T07:26:24Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "optimization workflows",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "hyperopt/hyperopt",
      "score": 8.8,
      "tier": "specialized",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "alpha",
        "optimization",
        "ml"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "machine-learning",
        "optimization",
        "alpha",
        "ml"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7595,
        "forks": 1074,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-28T22:18:00Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "optimization workflows",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "stefan-jansen/alphalens-reloaded",
      "score": 8.9,
      "tier": "specialized",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "alpha",
        "performance"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "alpha",
        "performance"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 662,
        "forks": 150,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-12-15T04:03:16Z"
      },
      "bestFor": [
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "quantopian/pyfolio",
      "score": 8.4,
      "tier": "audit",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "roles": [
        "risk",
        "performance"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "risk",
        "performance"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6423,
        "forks": 1896,
        "openIssues": 166,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2023-12-23T06:14:58Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy Pyfolio notebooks",
        "historical portfolio tear-sheet reference"
      ],
      "avoidWhen": [
        "new portfolio analytics",
        "actively maintained performance reporting"
      ],
      "alternatives": [
        "stefan-jansen/pyfolio-reloaded",
        "ranaroussi/quantstats",
        "skfolio/skfolio"
      ]
    },
    {
      "repo": "unit8co/darts",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "regime",
        "ml",
        "forecasting"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "regime",
        "ml",
        "forecasting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9533,
        "forks": 1048,
        "openIssues": 232,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-30T14:57:15Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "market regime analysis",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "sktime/sktime",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "regime",
        "ml",
        "forecasting"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "regime",
        "ml",
        "forecasting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10055,
        "forks": 2415,
        "openIssues": 2583,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-04T18:17:21Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "market regime analysis",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Nixtla/neuralforecast",
      "score": 9.3,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "regime",
        "ml",
        "forecasting"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "regime",
        "ml",
        "forecasting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4276,
        "forks": 510,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T05:25:33Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "market regime analysis",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "facebookresearch/Kats",
      "score": 9,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "regime",
        "forecasting"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "regime",
        "forecasting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6474,
        "forks": 633,
        "openIssues": 66,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-01T04:07:53Z"
      },
      "bestFor": [
        "market regime analysis",
        "forecasting models"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "blue-yonder/tsfresh",
      "score": 9.2,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "feature-engineering"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "ml",
        "feature-engineering"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9462,
        "forks": 1290,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-06T01:28:19Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "quantitative alpha research",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "akfamily/akshare",
      "score": 9,
      "tier": "recommended",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "data",
        "macro"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "market-data",
        "data",
        "macro"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 22827,
        "forks": 3530,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T07:23:31Z"
      },
      "bestFor": [
        "market-data ingestion",
        "data pipelines",
        "macroeconomic analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vollib/py_vollib",
      "score": 8.5,
      "tier": "specialized",
      "category": "Trading / microstructure / séries temporelles / exécution",
      "domain": "trading",
      "roles": [
        "derivatives",
        "volatility"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "derivatives",
        "volatility"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 437,
        "forks": 95,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-05-29T02:58:13Z"
      },
      "bestFor": [
        "derivatives workflows"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "OpenBB-finance/OpenBB",
      "score": 9.7,
      "tier": "recommended",
      "category": "Trading / Gold XAUUSD / macro / diagnostic",
      "domain": "trading",
      "roles": [
        "data",
        "macro",
        "xauusd"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "market-data",
        "data",
        "macro",
        "xauusd"
      ],
      "alternatives": [
        "ranaroussi/yfinance",
        "akfamily/akshare"
      ],
      "complements": [
        "microsoft/qlib",
        "QuantConnect/Lean"
      ],
      "bestFor": [
        "financial data research",
        "macro workflows"
      ],
      "avoidWhen": [
        "single-source minimal data ingestion"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73854,
        "forks": 7636,
        "openIssues": 86,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T04:55:27Z"
      }
    },
    {
      "repo": "plotly/plotly.py",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / Gold XAUUSD / macro / diagnostic",
      "domain": "trading",
      "roles": [
        "diagnostic",
        "xauusd"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "diagnostic",
        "xauusd"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 18823,
        "forks": 2858,
        "openIssues": 728,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T05:26:46Z"
      },
      "bestFor": [
        "diagnostics and analysis",
        "XAUUSD trading research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "matplotlib/mplfinance",
      "score": 9.1,
      "tier": "recommended",
      "category": "Trading / Gold XAUUSD / macro / diagnostic",
      "domain": "trading",
      "roles": [
        "diagnostic",
        "xauusd"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "diagnostic",
        "xauusd"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4439,
        "forks": 678,
        "openIssues": 177,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Matplotlib",
        "pushedAt": "2024-08-08T17:23:11Z"
      },
      "lifecycle": "stable",
      "bestFor": [
        "diagnostics and analysis",
        "XAUUSD trading research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "scikit-learn/scikit-learn",
      "score": 9.8,
      "tier": "core",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "regime"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "ml",
        "regime"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 67470,
        "forks": 27477,
        "openIssues": 2154,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T09:13:53Z"
      },
      "bestFor": [
        "classical machine-learning pipelines",
        "tabular modeling and evaluation",
        "feature preprocessing and model selection"
      ],
      "avoidWhen": [
        "deep neural-network training",
        "distributed GPU-first workloads"
      ]
    },
    {
      "repo": "dmlc/xgboost",
      "score": 9.7,
      "tier": "core",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "ml"
      ],
      "alternatives": [
        "catboost/catboost"
      ],
      "complements": [
        "shap/shap",
        "optuna/optuna"
      ],
      "bestFor": [
        "tabular alpha models",
        "nonlinear feature interactions"
      ],
      "avoidWhen": [
        "tiny datasets with unstable labels"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 28827,
        "forks": 8925,
        "openIssues": 449,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T13:56:26Z"
      }
    },
    {
      "repo": "catboost/catboost",
      "score": 9.6,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "ml"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9134,
        "forks": 1344,
        "openIssues": 734,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:45:28Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "quantitative alpha research",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "shap/shap",
      "score": 9.6,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "feature-selection"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "ml",
        "feature-selection"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25793,
        "forks": 3760,
        "openIssues": 987,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T18:10:00Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "quantitative alpha research",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "anyoptimization/pymoo",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "optimization",
        "portfolio",
        "risk"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "risk",
        "machine-learning",
        "optimization",
        "portfolio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2968,
        "forks": 482,
        "openIssues": 14,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-07-07T01:34:50Z"
      },
      "bestFor": [
        "risk analysis",
        "machine-learning workflows",
        "optimization workflows"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "DEAP/deap",
      "score": 9.2,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "optimization",
        "alpha"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "optimization",
        "alpha"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6445,
        "forks": 1164,
        "openIssues": 286,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "LGPL-3.0",
        "pushedAt": "2026-04-17T20:59:38Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "optimization workflows",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "tslearn-team/tslearn",
      "score": 9.1,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "regime",
        "ml"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "regime",
        "ml"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3183,
        "forks": 391,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-2-Clause",
        "pushedAt": "2026-10-05T09:33:19Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "market regime analysis",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "hmmlearn/hmmlearn",
      "score": 9,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "regime",
        "ml"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "regime",
        "ml"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3434,
        "forks": 756,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2024-10-31T09:14:35Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "market regime analysis",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "feature-engine/feature_engine",
      "score": 9,
      "tier": "recommended",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "alpha",
        "feature-engineering"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "machine-learning",
        "alpha",
        "feature-engineering"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2287,
        "forks": 379,
        "openIssues": 112,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-19T11:20:06Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "scikit-learn-contrib/imbalanced-learn",
      "score": 8.8,
      "tier": "specialized",
      "category": "Trading / alpha discovery / régimes / ML",
      "domain": "trading",
      "roles": [
        "ml",
        "alpha"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "machine-learning",
        "ml",
        "alpha"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7126,
        "forks": 1374,
        "openIssues": 103,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-06-29T16:33:16Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "machine-learning experiments",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "pykalman/pykalman",
      "score": 9,
      "tier": "recommended",
      "category": "Trading / ensembles / allocation dynamique / regime switching",
      "domain": "trading",
      "roles": [
        "regime",
        "filtering",
        "xauusd"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "regime",
        "filtering",
        "xauusd"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1337,
        "forks": 402,
        "openIssues": 85,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-04-20T19:22:17Z"
      },
      "bestFor": [
        "market regime analysis",
        "XAUUSD trading research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "blader/humanizer",
      "score": 9.1,
      "tier": "recommended",
      "category": "AI / agent skills",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 54067,
        "forks": 4296,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-28T05:55:12Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "freestylefly/awesome-gpt-image-2",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / image generation",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "prompt-library"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 33949,
        "forks": 3243,
        "openIssues": 34,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T09:56:12Z"
      },
      "bestFor": [
        "image-generation workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "cursor/plugins",
      "score": 9.1,
      "tier": "recommended",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9867,
        "forks": 929,
        "openIssues": 189,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:36:15Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file"
    },
    {
      "repo": "tt-a1i/archify",
      "score": 9.2,
      "tier": "recommended",
      "category": "Architecture / diagrams",
      "domain": "software_engineering",
      "capabilities": [
        "architecture",
        "diagrams",
        "agent-skill"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 77805,
        "forks": 5228,
        "openIssues": 199,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:10:38Z"
      },
      "bestFor": [
        "architecture workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bluscreenofjeff/Red-Team-Infrastructure-Wiki",
      "score": 8.8,
      "tier": "specialized",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4539,
        "forks": 907,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2025-10-01T17:10:58Z"
      },
      "bestFor": [
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "PurpleAILAB/Decepticon",
      "score": 9.1,
      "tier": "recommended",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 5662,
        "forks": 1067,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:16:17Z"
      },
      "bestFor": [
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "yeyintminthuhtut/Awesome-Red-Teaming",
      "score": 8.8,
      "tier": "audit",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8118,
        "forks": 1754,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2023-12-28T18:10:52Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "historical red-team resource collection"
      ],
      "avoidWhen": [
        "current tooling discovery",
        "time-sensitive offensive-security references"
      ]
    },
    {
      "repo": "A-poc/RedTeam-Tools",
      "score": 8.9,
      "tier": "specialized",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9804,
        "forks": 1313,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-04-18T09:27:42Z"
      },
      "bestFor": [
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "infosecn1nja/Red-Teaming-Toolkit",
      "score": 9,
      "tier": "recommended",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10762,
        "forks": 2376,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-05-07T23:44:01Z"
      },
      "bestFor": [
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "redcanaryco/atomic-red-team",
      "score": 9.6,
      "tier": "core",
      "category": "Cybersecurity / red team",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "alternatives": [],
      "complements": [
        "github/codeql",
        "semgrep/semgrep"
      ],
      "bestFor": [
        "authorized detection validation",
        "defensive testing"
      ],
      "avoidWhen": [
        "unauthorized environments"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12608,
        "forks": 3229,
        "openIssues": 35,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:12:53Z"
      }
    },
    {
      "repo": "enaqx/awesome-pentest",
      "score": 9.2,
      "tier": "recommended",
      "category": "Cybersecurity / pentest",
      "domain": "cybersecurity",
      "capabilities": [
        "code-quality",
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 27346,
        "forks": 4972,
        "openIssues": 134,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-07-25T12:15:45Z"
      },
      "bestFor": [
        "code-quality automation",
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file"
    },
    {
      "repo": "GreyDGL/PentestGPT",
      "score": 9.2,
      "tier": "recommended",
      "category": "Cybersecurity / pentest AI",
      "domain": "cybersecurity",
      "capabilities": [
        "code-quality",
        "security-testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15737,
        "forks": 2741,
        "openIssues": 87,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-14T12:58:31Z"
      },
      "bestFor": [
        "code-quality automation",
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vxcontrol/pentagi",
      "score": 9.4,
      "tier": "recommended",
      "category": "Cybersecurity / pentest AI",
      "domain": "cybersecurity",
      "capabilities": [
        "code-quality",
        "security-testing"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25256,
        "forks": 3244,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:59:49Z"
      },
      "bestFor": [
        "code-quality automation",
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "SnailSploit/Claude-Red",
      "score": 8.9,
      "tier": "specialized",
      "category": "Cybersecurity / agent skills",
      "domain": "cybersecurity",
      "capabilities": [
        "agent",
        "security-testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7270,
        "forks": 950,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T23:46:22Z"
      },
      "bestFor": [
        "agentic workflows",
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "asgeirtj/system_prompts_leaks",
      "score": 8.7,
      "tier": "specialized",
      "category": "AI / prompt research",
      "domain": "ai_agents",
      "capabilities": [
        "prompt-research",
        "system-prompts"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 68928,
        "forks": 11198,
        "openIssues": 56,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC0-1.0",
        "pushedAt": "2026-10-05T11:21:51Z"
      },
      "bestFor": [
        "prompt research workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "headroomlabs-ai/headroom",
      "score": 9.3,
      "tier": "recommended",
      "category": "AI / context optimization",
      "domain": "ai_agents",
      "capabilities": [
        "machine-learning",
        "optimization"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 74439,
        "forks": 5762,
        "openIssues": 447,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T03:48:29Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "optimization workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "langchain-ai/langchain",
      "score": 9.6,
      "tier": "recommended",
      "category": "AI / agent frameworks",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 147460,
        "forks": 24708,
        "openIssues": 618,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T08:41:46Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "microsoft/markitdown",
      "score": 9.5,
      "tier": "recommended",
      "category": "Documents / conversion",
      "domain": "software_engineering",
      "capabilities": [
        "document-conversion",
        "markdown"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 188541,
        "forks": 13959,
        "openIssues": 666,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T03:59:52Z"
      },
      "bestFor": [
        "document conversion workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "langgenius/dify",
      "score": 9.6,
      "tier": "recommended",
      "category": "AI / agent platforms",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 157865,
        "forks": 24909,
        "openIssues": 1024,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Modified Apache-2.0",
        "pushedAt": "2026-10-05T11:10:19Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "firebase/flutterfire",
      "score": 9.4,
      "tier": "recommended",
      "category": "Mobile / Flutter",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "dart"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9260,
        "forks": 4123,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-05T04:10:19Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Solido/awesome-flutter",
      "score": 8.9,
      "tier": "specialized",
      "category": "Mobile / Flutter",
      "domain": "mobile",
      "capabilities": [
        "mobile"
      ],
      "languages": [
        "dart"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 61416,
        "forks": 6924,
        "openIssues": 38,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "CC0-1.0",
        "pushedAt": "2026-09-03T04:34:54Z"
      },
      "bestFor": [
        "mobile application development"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file"
    },
    {
      "repo": "AgriciDaniel/claude-obsidian",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / knowledge",
      "domain": "ai_memory",
      "capabilities": [
        "memory"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15355,
        "forks": 1531,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-10T17:44:23Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "kepano/obsidian-skills",
      "score": 9,
      "tier": "recommended",
      "category": "AI / agent skills",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49157,
        "forks": 3489,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T14:43:57Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "blaCCkHatHacEEkr/PENTESTING-BIBLE",
      "score": 8.8,
      "tier": "audit",
      "category": "Cybersecurity / pentest",
      "domain": "cybersecurity",
      "capabilities": [
        "code-quality",
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13976,
        "forks": 2465,
        "openIssues": 28,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2023-04-03T07:40:28Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "historical pentesting reference collection"
      ],
      "avoidWhen": [
        "current toolchains",
        "time-sensitive vulnerability research"
      ]
    },
    {
      "repo": "mem0ai/mem0",
      "score": 9.7,
      "tier": "core",
      "category": "AI / memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory"
      ],
      "alternatives": [
        "thedotmack/claude-mem",
        "doobidoo/mcp-memory-service",
        "akitaonrails/ai-memory"
      ],
      "complements": [
        "langchain-ai/langgraph",
        "crewAIInc/crewAI"
      ],
      "bestFor": [
        "persistent agent memory"
      ],
      "avoidWhen": [
        "stateless short-lived agents"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 66586,
        "forks": 7851,
        "openIssues": 786,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T04:18:38Z"
      }
    },
    {
      "repo": "thedotmack/claude-mem",
      "score": 9.5,
      "tier": "core",
      "category": "AI / memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 96351,
        "forks": 8505,
        "openIssues": 88,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:17:15Z"
      },
      "bestFor": [
        "persistent context for Claude coding workflows",
        "cross-session project memory",
        "retrieving prior coding context"
      ],
      "avoidWhen": [
        "stateless sessions",
        "non-Claude agent stacks"
      ]
    },
    {
      "repo": "academic/awesome-datascience",
      "score": 9,
      "tier": "recommended",
      "category": "Data science",
      "domain": "data_ml",
      "capabilities": [
        "market-data"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 30108,
        "forks": 6661,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "live",
        "license": "MIT",
        "pushedAt": "2026-10-02T20:20:58Z"
      },
      "bestFor": [
        "market-data ingestion"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "DeusData/codebase-memory-mcp",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / code memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "market-data"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45799,
        "forks": 3767,
        "openIssues": 638,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T05:38:28Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "usememos/memos",
      "score": 9.2,
      "tier": "recommended",
      "category": "Knowledge / notes",
      "domain": "ai_memory",
      "capabilities": [
        "memory"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 63536,
        "forks": 4811,
        "openIssues": 98,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T22:17:54Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bytedance/UI-TARS-desktop",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / computer use",
      "domain": "ai_agents",
      "capabilities": [
        "computer-use",
        "desktop-agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39202,
        "forks": 3971,
        "openIssues": 503,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-24T06:48:56Z"
      },
      "bestFor": [
        "computer use workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "animate-css/animate.css",
      "score": 9.4,
      "tier": "recommended",
      "category": "Frontend / animation",
      "domain": "graphics",
      "capabilities": [
        "vector-animation"
      ],
      "languages": [
        "css"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 82850,
        "forks": 15877,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Hippocratic-2.1",
        "pushedAt": "2024-07-29T19:34:21Z"
      },
      "lifecycle": "stable",
      "bestFor": [
        "vector animation"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "microsoft/magentic-ui",
      "score": 9.3,
      "tier": "recommended",
      "category": "AI / computer use",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10087,
        "forks": 1018,
        "openIssues": 20,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-23T23:43:21Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "microsoft/ai-agents-for-beginners",
      "score": 9.1,
      "tier": "recommended",
      "category": "AI / agent learning",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "machine-learning"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 76471,
        "forks": 25128,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T06:16:49Z"
      },
      "bestFor": [
        "agentic workflows",
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "FlowiseAI/Flowise",
      "score": 9.5,
      "tier": "audit",
      "category": "AI / agent platforms",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 55483,
        "forks": 25064,
        "openIssues": 1040,
        "archived": true,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-08-13T12:38:19Z"
      },
      "bestFor": [
        "legacy Flowise deployments",
        "migration reference for visual agent workflows"
      ],
      "avoidWhen": [
        "new production deployments",
        "actively maintained visual agent builder"
      ],
      "alternatives": [
        "langflow-ai/langflow",
        "langgenius/dify"
      ],
      "lifecycle": "legacy"
    },
    {
      "repo": "BerriAI/litellm",
      "score": 9.7,
      "tier": "core",
      "category": "AI / model routing",
      "domain": "ai_agents",
      "capabilities": [
        "model-routing",
        "llm-gateway",
        "observability"
      ],
      "alternatives": [
        "diegosouzapw/OmniRoute"
      ],
      "complements": [
        "ollama/ollama",
        "langfuse/langfuse"
      ],
      "bestFor": [
        "multi-provider LLM routing",
        "cost and fallback control"
      ],
      "avoidWhen": [
        "single-provider minimal stacks"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 60144,
        "forks": 12030,
        "openIssues": 5195,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:26:29Z"
      }
    },
    {
      "repo": "bytedance/deer-flow",
      "score": 9.5,
      "tier": "recommended",
      "category": "AI / agent frameworks",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 83399,
        "forks": 11583,
        "openIssues": 904,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:06:17Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "lettier/3d-game-shaders-for-beginners",
      "score": 9.2,
      "tier": "audit",
      "category": "Graphics / shaders",
      "domain": "graphics",
      "capabilities": [
        "rendering",
        "game-development"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 19939,
        "forks": 1482,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2023-06-25T21:58:57Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "learning classic real-time shader techniques"
      ],
      "avoidWhen": [
        "current engine-specific shader APIs",
        "actively maintained rendering examples"
      ],
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "partial"
    },
    {
      "repo": "Donchitos/Claude-Code-Game-Studios",
      "score": 9.1,
      "tier": "recommended",
      "category": "Game development / agents",
      "domain": "game_dev",
      "capabilities": [
        "agent",
        "mobile",
        "game-development"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "android",
        "ios",
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25754,
        "forks": 3661,
        "openIssues": 61,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-29T12:55:08Z"
      },
      "bestFor": [
        "agentic workflows",
        "game development"
      ],
      "avoidWhen": [
        "non-game application development"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "godotengine/godot",
      "score": 9.8,
      "tier": "core",
      "category": "Game development",
      "domain": "game_dev",
      "capabilities": [
        "game-development"
      ],
      "alternatives": [
        "libgdx/libgdx"
      ],
      "complements": [
        "heroiclabs/nakama",
        "Calinou/awesome-godot"
      ],
      "bestFor": [
        "2D/3D games",
        "cross-platform game development"
      ],
      "avoidWhen": [
        "web-only non-game apps"
      ],
      "languages": [
        "go",
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 118136,
        "forks": 26949,
        "openIssues": 18924,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:56:04Z"
      }
    },
    {
      "repo": "libgdx/libgdx",
      "score": 9.3,
      "tier": "recommended",
      "category": "Game development",
      "domain": "game_dev",
      "capabilities": [
        "game-development"
      ],
      "languages": [
        "java"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 25421,
        "forks": 6521,
        "openIssues": 344,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-24T03:13:51Z"
      },
      "bestFor": [
        "game development"
      ],
      "avoidWhen": [
        "non-game application development"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "google/filament",
      "score": 9.6,
      "tier": "core",
      "category": "Graphics / rendering",
      "domain": "graphics",
      "capabilities": [
        "rendering"
      ],
      "alternatives": [
        "pmndrs/react-three-fiber"
      ],
      "complements": [
        "godotengine/godot"
      ],
      "bestFor": [
        "real-time rendering",
        "mobile/desktop 3D"
      ],
      "avoidWhen": [
        "simple 2D UI"
      ],
      "languages": [
        "rust",
        "go",
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 20563,
        "forks": 2272,
        "openIssues": 222,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T07:23:09Z"
      }
    },
    {
      "repo": "soxoj/maigret",
      "score": 9.1,
      "tier": "recommended",
      "category": "OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 38322,
        "forks": 3016,
        "openIssues": 60,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:58:30Z"
      },
      "bestFor": [
        "open-source intelligence research"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "sherlock-project/sherlock",
      "score": 9.5,
      "tier": "core",
      "category": "OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
      ],
      "alternatives": [
        "soxoj/maigret"
      ],
      "complements": [],
      "bestFor": [
        "OSINT username enumeration"
      ],
      "avoidWhen": [
        "identity claims require high-confidence attribution"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 93256,
        "forks": 11010,
        "openIssues": 356,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T05:31:58Z"
      }
    },
    {
      "repo": "payloadcms/payload",
      "score": 9.5,
      "tier": "recommended",
      "category": "Web development / CMS",
      "domain": "web_frontend",
      "capabilities": [
        "cms",
        "backend",
        "typescript"
      ],
      "languages": [
        "typescript",
        "javascript"
      ],
      "platforms": [
        "web",
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45096,
        "forks": 4256,
        "openIssues": 1268,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:54:32Z"
      },
      "bestFor": [
        "backend services",
        "TypeScript application development"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "danielmiessler/SecLists",
      "score": 9.7,
      "tier": "core",
      "category": "Cybersecurity / resources",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "php"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73939,
        "forks": 25140,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:17:11Z"
      },
      "bestFor": [
        "authorized security-testing wordlists",
        "fuzzing dictionaries and payload lists",
        "reproducible pentest input collections"
      ],
      "avoidWhen": [
        "standalone vulnerability validation",
        "non-security workloads"
      ]
    },
    {
      "repo": "infoslack/awesome-web-hacking",
      "score": 8.9,
      "tier": "specialized",
      "category": "Cybersecurity / web",
      "domain": "cybersecurity",
      "capabilities": [
        "security-testing"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "web",
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7286,
        "forks": 1365,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-18T02:51:45Z"
      },
      "bestFor": [
        "authorized security testing"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "rapid7/metasploit-framework",
      "score": 9.7,
      "tier": "core",
      "category": "Cybersecurity / pentest",
      "domain": "cybersecurity",
      "capabilities": [
        "code-quality",
        "security-testing"
      ],
      "languages": [
        "ruby"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 39094,
        "forks": 14983,
        "openIssues": 616,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T01:27:54Z"
      },
      "bestFor": [
        "authorized exploit validation",
        "penetration-testing labs",
        "reproducible security module workflows"
      ],
      "avoidWhen": [
        "non-security automation",
        "environments where custom minimal tooling is required"
      ]
    },
    {
      "repo": "huggingface/transformers",
      "score": 9.9,
      "tier": "core",
      "category": "AI / ML",
      "domain": "data_ml",
      "capabilities": [
        "machine-learning"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 166963,
        "forks": 34752,
        "openIssues": 2373,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:40:35Z"
      },
      "bestFor": [
        "pretrained transformer model inference",
        "fine-tuning NLP, vision, and audio models",
        "model ecosystem interoperability"
      ],
      "avoidWhen": [
        "small dependency-light inference",
        "very low-resource deployments"
      ]
    },
    {
      "repo": "jihe520/MathModelAgent",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / research agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6175,
        "forks": 450,
        "openIssues": 43,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-03T07:04:06Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "custom-restrictive"
    },
    {
      "repo": "alibaba/open-code-review",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / code review",
      "domain": "ai_agents",
      "capabilities": [
        "code-quality"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 43796,
        "forks": 3155,
        "openIssues": 276,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T06:43:52Z"
      },
      "bestFor": [
        "code-quality automation"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "multimodal-art-projection/YuE",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / audio",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10835,
        "forks": 1240,
        "openIssues": 38,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T00:32:42Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "calesthio/OpenMontage",
      "score": 9.3,
      "tier": "recommended",
      "category": "AI / video",
      "domain": "ai_media",
      "capabilities": [
        "video"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 63525,
        "forks": 8085,
        "openIssues": 354,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-03T16:28:55Z"
      },
      "bestFor": [
        "video-generation workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "tech-leads-club/agent-skills",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / agent skills",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7029,
        "forks": 558,
        "openIssues": 34,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-09-20T12:37:19Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "EsotericSoftware/spine-runtimes",
      "score": 9.3,
      "tier": "recommended",
      "category": "Graphics / vector animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation",
        "rendering"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 5309,
        "forks": 3140,
        "openIssues": 82,
        "archived": false,
        "disabled": false,
        "defaultBranch": "4.3",
        "license": "Spine Runtimes License",
        "pushedAt": "2026-09-30T22:11:28Z"
      },
      "bestFor": [
        "vector animation",
        "graphics rendering"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "online-ml/river",
      "score": 9.3,
      "tier": "recommended",
      "category": "ML / online learning",
      "domain": "data_ml",
      "capabilities": [
        "machine-learning",
        "vector-animation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6119,
        "forks": 832,
        "openIssues": 79,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-02T13:59:50Z"
      },
      "bestFor": [
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "airbnb/lottie-ios",
      "score": 9.3,
      "tier": "recommended",
      "category": "Graphics / vector animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation",
        "rendering",
        "mobile"
      ],
      "languages": [
        "swift"
      ],
      "platforms": [
        "android",
        "ios"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 26893,
        "forks": 3839,
        "openIssues": 45,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-28T12:55:28Z"
      },
      "bestFor": [
        "vector animation",
        "graphics rendering",
        "mobile application development"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "airbnb/lottie-android",
      "score": 9.4,
      "tier": "recommended",
      "category": "Graphics / vector animation",
      "domain": "graphics",
      "capabilities": [
        "memory",
        "vector-animation",
        "rendering",
        "mobile"
      ],
      "languages": [
        "java",
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35736,
        "forks": 5423,
        "openIssues": 76,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-02-15T22:03:57Z"
      },
      "bestFor": [
        "vector animation",
        "graphics rendering",
        "mobile application development"
      ],
      "avoidWhen": [
        "non-visual workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Calinou/awesome-godot",
      "score": 9,
      "tier": "recommended",
      "category": "Game development",
      "domain": "game_dev",
      "capabilities": [
        "game-development"
      ],
      "languages": [
        "go",
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 10843,
        "forks": 592,
        "openIssues": 77,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-09-12T21:34:34Z"
      },
      "bestFor": [
        "game development"
      ],
      "avoidWhen": [
        "low-resource environments",
        "non-game application development"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "heroiclabs/nakama",
      "score": 9.4,
      "tier": "recommended",
      "category": "Game development / backend",
      "domain": "game_dev",
      "capabilities": [
        "game-development"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13471,
        "forks": 1501,
        "openIssues": 120,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-28T11:20:40Z"
      },
      "bestFor": [
        "game development"
      ],
      "avoidWhen": [
        "non-game application development"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "unclecode/crawl4ai",
      "score": 9.6,
      "tier": "recommended",
      "category": "AI / web retrieval",
      "domain": "ai_agents",
      "capabilities": [
        "web-retrieval"
      ],
      "alternatives": [
        "firecrawl/firecrawl"
      ],
      "complements": [
        "langchain-ai/langchain",
        "langgenius/dify"
      ],
      "bestFor": [
        "self-hosted crawling",
        "structured extraction"
      ],
      "avoidWhen": [
        "managed API preferred"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 84769,
        "forks": 8777,
        "openIssues": 231,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:26:42Z"
      }
    },
    {
      "repo": "firecrawl/firecrawl",
      "score": 9.8,
      "tier": "core",
      "category": "AI / web retrieval",
      "domain": "ai_agents",
      "capabilities": [
        "web-retrieval"
      ],
      "alternatives": [
        "unclecode/crawl4ai"
      ],
      "complements": [
        "browser-use/browser-use",
        "microsoft/playwright"
      ],
      "bestFor": [
        "web extraction",
        "LLM-ready web data"
      ],
      "avoidWhen": [
        "pure browser interaction without extraction"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 188745,
        "forks": 10027,
        "openIssues": 525,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-04T15:03:46Z"
      }
    },
    {
      "repo": "jo-inc/camoufox-browser",
      "score": 9,
      "tier": "recommended",
      "category": "AI / browser automation",
      "domain": "ai_agents",
      "capabilities": [
        "web-retrieval"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11432,
        "forks": 1145,
        "openIssues": 154,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T02:38:56Z"
      },
      "bestFor": [
        "browser and web retrieval"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "AgriciDaniel/claude-ads",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / marketing agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9719,
        "forks": 1440,
        "openIssues": 25,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T21:05:04Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Open-LLM-VTuber/Open-LLM-VTuber",
      "score": 9.1,
      "tier": "recommended",
      "category": "AI / voice avatars",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13983,
        "forks": 1674,
        "openIssues": 158,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-15T07:18:04Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "HKUDS/Vibe-Trading",
      "score": 9.3,
      "tier": "recommended",
      "category": "Trading / AI agents",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "data"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "agent",
        "market-data",
        "machine-learning",
        "alpha",
        "ml",
        "data"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 34747,
        "forks": 5638,
        "openIssues": 35,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T09:22:45Z"
      },
      "bestFor": [
        "agentic workflows",
        "market-data ingestion",
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "The-Swarm-Corporation/AutoHedge",
      "score": 8.9,
      "tier": "specialized",
      "category": "Trading / AI agents",
      "domain": "trading",
      "roles": [
        "alpha",
        "risk",
        "execution"
      ],
      "agentSuitability": "medium",
      "capabilities": [
        "agent",
        "execution",
        "risk",
        "alpha"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6234,
        "forks": 897,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-11T05:44:09Z"
      },
      "bestFor": [
        "agentic workflows",
        "trading execution systems",
        "risk analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "OpenBMB/VoxCPM",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / speech",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 38321,
        "forks": 4332,
        "openIssues": 130,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-30T03:52:48Z"
      },
      "bestFor": [
        "speech and audio processing"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Fincept-Corporation/FinceptTerminal",
      "score": 9.4,
      "tier": "recommended",
      "category": "Trading / data / macro",
      "domain": "trading",
      "roles": [
        "data",
        "macro",
        "diagnostic"
      ],
      "agentSuitability": "medium-high",
      "capabilities": [
        "market-data",
        "data",
        "macro",
        "diagnostic"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32196,
        "forks": 4550,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-01T08:59:02Z"
      },
      "bestFor": [
        "market-data ingestion",
        "data pipelines",
        "macroeconomic analysis"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "TauricResearch/TradingAgents",
      "score": 9.5,
      "tier": "recommended",
      "category": "Trading / AI agents",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "portfolio",
        "risk"
      ],
      "agentSuitability": "high",
      "capabilities": [
        "agent",
        "risk",
        "machine-learning",
        "alpha",
        "ml",
        "portfolio"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 109816,
        "forks": 21111,
        "openIssues": 85,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-03T21:30:10Z"
      },
      "bestFor": [
        "agentic workflows",
        "risk analysis",
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ever-co/ever-gauzy",
      "score": 8.8,
      "tier": "specialized",
      "category": "Business / ERP",
      "domain": "productivity",
      "capabilities": [
        "erp",
        "crm",
        "business-automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8171,
        "forks": 1202,
        "openIssues": 462,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-05T11:24:51Z"
      },
      "bestFor": [
        "erp workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "kyegomez/awesome-multi-agent-papers",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / multi-agent research",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "developer-resources"
      ],
      "languages": [
        "tex"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1696,
        "forks": 164,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-23T16:56:23Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "doobidoo/mcp-memory-service",
      "score": 9,
      "tier": "recommended",
      "category": "AI / memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1984,
        "forks": 340,
        "openIssues": 25,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T05:25:21Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "agentic workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "alphaXiv/OpenResearch",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / research agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "research"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6582,
        "forks": 418,
        "openIssues": 68,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:44:31Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "inkscape/inkscape",
      "score": 9.4,
      "tier": "audit",
      "category": "Graphics / vector design",
      "domain": "graphics",
      "capabilities": [
        "vector-graphics",
        "design"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3987,
        "forks": 294,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2022-03-03T20:52:00Z"
      },
      "lifecycle": "reference",
      "bestFor": [
        "historical GitHub mirror reference for Inkscape"
      ],
      "avoidWhen": [
        "tracking current Inkscape development",
        "using GitHub as the canonical upstream"
      ],
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "rive-app/rive-android",
      "score": 8.9,
      "tier": "specialized",
      "category": "Mobile / animation",
      "domain": "mobile",
      "capabilities": [
        "animation",
        "graphics"
      ],
      "languages": [
        "kotlin"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 542,
        "forks": 66,
        "openIssues": 101,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T04:43:40Z"
      },
      "bestFor": [
        "animation workflows"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "plattysoft/Leonids",
      "score": 8.5,
      "tier": "audit",
      "category": "Mobile / particle effects",
      "domain": "mobile",
      "capabilities": [
        "particles",
        "graphics"
      ],
      "languages": [
        "java"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2279,
        "forks": 395,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2021-02-24T07:55:47Z"
      },
      "lifecycle": "legacy",
      "bestFor": [
        "legacy Android particle-effect implementations"
      ],
      "avoidWhen": [
        "modern Android UI stacks",
        "actively maintained graphics libraries"
      ]
    },
    {
      "repo": "DanielMartinus/Konfetti",
      "score": 8.6,
      "tier": "specialized",
      "category": "Mobile / particle effects",
      "domain": "mobile",
      "capabilities": [
        "particles",
        "graphics"
      ],
      "languages": [
        "kotlin"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3392,
        "forks": 311,
        "openIssues": 27,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "ISC",
        "pushedAt": "2025-08-21T10:03:22Z"
      },
      "bestFor": [
        "particle effects"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ruvnet/RuView",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / computer vision",
      "domain": "data_ml",
      "capabilities": [
        "computer-vision",
        "agent"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 96461,
        "forks": 12703,
        "openIssues": 430,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:40:41Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "rlaope/oh-my-hermes",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3156,
        "forks": 243,
        "openIssues": 14,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:51:01Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "stablyai/orca",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 85380,
        "forks": 5495,
        "openIssues": 7622,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:26:46Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Panniantong/Agent-Reach",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / web agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "web-search"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 91381,
        "forks": 8026,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:16:24Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "trailhq/Graft",
      "score": 8.8,
      "tier": "specialized",
      "category": "Software engineering / code context",
      "domain": "software_engineering",
      "capabilities": [
        "coding",
        "code-analysis"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9581,
        "forks": 882,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T19:00:50Z"
      },
      "bestFor": [
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "opensandbox-group/OpenSandbox",
      "score": 9,
      "tier": "recommended",
      "category": "Software engineering / agent sandbox",
      "domain": "software_engineering",
      "capabilities": [
        "sandbox",
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15672,
        "forks": 1443,
        "openIssues": 140,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-01T02:21:12Z"
      },
      "bestFor": [
        "isolated code execution",
        "agentic workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "jo-inc/camofox-browser",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / browser automation",
      "domain": "ai_agents",
      "capabilities": [
        "browser-automation",
        "agent"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11432,
        "forks": 1145,
        "openIssues": 154,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T02:38:56Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "roboflow/supervision",
      "score": 9.3,
      "tier": "recommended",
      "category": "Data / computer vision",
      "domain": "data_ml",
      "capabilities": [
        "computer-vision",
        "data"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 51123,
        "forks": 4867,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:04:22Z"
      },
      "bestFor": [
        "data pipelines"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "anthropics/claude-code",
      "score": 9.8,
      "tier": "core",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 149456,
        "forks": 25546,
        "openIssues": 14219,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Anthropic Commercial Terms",
        "pushedAt": "2026-10-05T01:04:13Z"
      },
      "bestFor": [
        "repository-level coding tasks",
        "terminal-driven code editing",
        "agentic debugging and refactoring"
      ],
      "avoidWhen": [
        "offline-only workflows",
        "tasks that do not need an autonomous coding agent"
      ],
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "NationalSecurityAgency/ghidra",
      "score": 9.5,
      "tier": "recommended",
      "category": "Cybersecurity / reverse engineering",
      "domain": "cybersecurity",
      "capabilities": [
        "reverse-engineering",
        "binary-analysis"
      ],
      "languages": [
        "java"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 80691,
        "forks": 8975,
        "openIssues": 1985,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T08:44:38Z"
      },
      "bestFor": [
        "reverse engineering workflows"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ankitects/anki",
      "score": 9.2,
      "tier": "recommended",
      "category": "Productivity / learning",
      "domain": "productivity",
      "capabilities": [
        "spaced-repetition",
        "learning"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 31768,
        "forks": 3300,
        "openIssues": 573,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:49:00Z"
      },
      "bestFor": [
        "spaced repetition workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "anthropics/knowledge-work-plugins",
      "score": 9,
      "tier": "recommended",
      "category": "AI / knowledge work",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "knowledge-work"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 26118,
        "forks": 3056,
        "openIssues": 125,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T07:55:53Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "jamiepine/voicebox",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / voice",
      "domain": "ai_media",
      "capabilities": [
        "audio",
        "voice"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 56403,
        "forks": 7028,
        "openIssues": 673,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T23:26:30Z"
      },
      "bestFor": [
        "audio workflows"
      ],
      "avoidWhen": [
        "non-generative media workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "JustVugg/colibri",
      "score": 8.7,
      "tier": "specialized",
      "category": "AI / local inference",
      "domain": "data_ml",
      "capabilities": [
        "inference",
        "edge-ai"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39658,
        "forks": 4346,
        "openIssues": 105,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:17:28Z"
      },
      "bestFor": [
        "inference workflows"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "cloudflare/security-audit-skill",
      "score": 9,
      "tier": "recommended",
      "category": "Cybersecurity / agent auditing",
      "domain": "cybersecurity",
      "capabilities": [
        "security-audit",
        "agent"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 24560,
        "forks": 1453,
        "openIssues": 54,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T19:29:02Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "CarterPerez-dev/Cybersecurity-Projects",
      "score": 8.6,
      "tier": "specialized",
      "category": "Cybersecurity / learning",
      "domain": "cybersecurity",
      "capabilities": [
        "security-learning",
        "developer-resources"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 7857,
        "forks": 1146,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-02T09:57:24Z"
      },
      "bestFor": [
        "security learning workflows"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "block/buzz",
      "score": 8.7,
      "tier": "specialized",
      "category": "Productivity / communication",
      "domain": "productivity",
      "capabilities": [
        "communication"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 35555,
        "forks": 4702,
        "openIssues": 3619,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T20:59:22Z"
      },
      "bestFor": [
        "communication workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Lakr233/vphone-cli",
      "score": 8.7,
      "tier": "specialized",
      "category": "Mobile / automation",
      "domain": "mobile",
      "capabilities": [
        "mobile-automation",
        "cli"
      ],
      "languages": [
        "swift"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14888,
        "forks": 1762,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:14:27Z"
      },
      "bestFor": [
        "mobile automation workflows"
      ],
      "avoidWhen": [
        "web-only applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Tencent/WeKnora",
      "score": 9.1,
      "tier": "recommended",
      "category": "AI / RAG / knowledge",
      "domain": "data_ml",
      "capabilities": [
        "rag",
        "knowledge-base"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 32102,
        "forks": 4278,
        "openIssues": 659,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-01T11:57:46Z"
      },
      "bestFor": [
        "retrieval-augmented generation"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Tencent/BrowserSkill",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / browser automation",
      "domain": "ai_agents",
      "capabilities": [
        "browser-automation",
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8152,
        "forks": 584,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T04:52:55Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "openai/codex",
      "score": 9.8,
      "tier": "core",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 127896,
        "forks": 20029,
        "openIssues": 20690,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:16:20Z"
      },
      "bestFor": [
        "agentic repository coding",
        "terminal-driven implementation tasks",
        "automated code editing and debugging"
      ],
      "avoidWhen": [
        "offline-only workflows",
        "tasks that do not require codebase modification"
      ]
    },
    {
      "repo": "cline/cline",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 69873,
        "forks": 7604,
        "openIssues": 1598,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T09:13:45Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "addyosmani/agent-skills",
      "score": 9,
      "tier": "recommended",
      "category": "AI / agent skills",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "developer-resources"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 101366,
        "forks": 10628,
        "openIssues": 121,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T18:21:11Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "virattt/ai-hedge-fund",
      "score": 9.2,
      "tier": "recommended",
      "category": "Trading / AI agents",
      "domain": "trading",
      "roles": [
        "alpha",
        "ml",
        "risk"
      ],
      "capabilities": [
        "agent",
        "alpha",
        "ml",
        "risk"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 63850,
        "forks": 11223,
        "openIssues": 177,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-02T14:19:04Z"
      },
      "bestFor": [
        "agentic workflows",
        "quantitative alpha research",
        "machine-learning experiments"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "cactus-compute/needle",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / edge inference",
      "domain": "data_ml",
      "capabilities": [
        "inference",
        "edge-ai"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13245,
        "forks": 894,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T20:44:20Z"
      },
      "bestFor": [
        "inference workflows"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ruanyf/weekly",
      "score": 8.8,
      "tier": "specialized",
      "category": "Productivity / developer resources",
      "domain": "productivity",
      "capabilities": [
        "developer-resources"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 105183,
        "forks": 4476,
        "openIssues": 9364,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-09-19T11:38:43Z"
      },
      "bestFor": [
        "developer resources workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "docling-project/docling",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / document processing",
      "domain": "data_ml",
      "capabilities": [
        "document-processing",
        "rag"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 68398,
        "forks": 5002,
        "openIssues": 1000,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:51:48Z"
      },
      "bestFor": [
        "retrieval-augmented generation"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Open-Dev-Society/OpenStock",
      "score": 8.8,
      "tier": "specialized",
      "category": "Trading / market data",
      "domain": "trading",
      "roles": [
        "data",
        "alpha"
      ],
      "capabilities": [
        "market-data",
        "data",
        "alpha"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 19671,
        "forks": 2413,
        "openIssues": 37,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-01T15:54:43Z"
      },
      "bestFor": [
        "market-data ingestion",
        "data pipelines",
        "quantitative alpha research"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "kaiiyer/awesome-vulnerable",
      "score": 8.6,
      "tier": "specialized",
      "category": "Cybersecurity / vulnerable labs",
      "domain": "cybersecurity",
      "capabilities": [
        "penetration-testing",
        "security-learning"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1399,
        "forks": 228,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-06-22T17:46:43Z"
      },
      "bestFor": [
        "penetration testing workflows"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "latent-spaces/brag",
      "score": 8.8,
      "tier": "specialized",
      "category": "AI / launch automation",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 13589,
        "forks": 962,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-01T16:24:38Z"
      },
      "bestFor": [
        "agentic workflows",
        "workflow automation"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ahmedkhaleel2004/gitdiagram",
      "score": 9,
      "tier": "recommended",
      "category": "Software engineering / visualization",
      "domain": "software_engineering",
      "capabilities": [
        "code-analysis",
        "visualization"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 17854,
        "forks": 1366,
        "openIssues": 45,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T19:29:31Z"
      },
      "bestFor": [
        "code analysis workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "tradesdontlie/tradingview-mcp",
      "score": 8.9,
      "tier": "specialized",
      "category": "Trading / chart analysis",
      "domain": "trading",
      "roles": [
        "data",
        "diagnostic"
      ],
      "capabilities": [
        "market-data",
        "diagnostic",
        "mcp"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6715,
        "forks": 2801,
        "openIssues": 266,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-28T17:28:37Z"
      },
      "bestFor": [
        "market-data ingestion",
        "diagnostics and analysis",
        "data pipelines"
      ],
      "avoidWhen": [
        "non-financial applications"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "supermemoryai/supermemory",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 31080,
        "forks": 2734,
        "openIssues": 97,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T00:28:29Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "agentic workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Fission-AI/OpenSpec",
      "score": 9.2,
      "tier": "recommended",
      "category": "Software engineering / spec-driven development",
      "domain": "software_engineering",
      "capabilities": [
        "spec-driven-development",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 71060,
        "forks": 4871,
        "openIssues": 189,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T01:47:11Z"
      },
      "bestFor": [
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "earendil-works/pi",
      "score": 9,
      "tier": "recommended",
      "category": "AI / agent toolkit",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 112570,
        "forks": 14280,
        "openIssues": 261,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:12:11Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "n8n-io/n8n",
      "score": 9.5,
      "tier": "core",
      "category": "Productivity / automation",
      "domain": "productivity",
      "capabilities": [
        "automation",
        "workflow"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 206693,
        "forks": 61006,
        "openIssues": 1114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Sustainable Use License",
        "pushedAt": "2026-10-05T11:24:23Z"
      },
      "bestFor": [
        "self-hosted workflow automation",
        "API and service orchestration",
        "low-code business automations"
      ],
      "avoidWhen": [
        "hard real-time processing",
        "ultra-light embedded automation"
      ],
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "mindsdb/mindsdb",
      "score": 9.3,
      "tier": "recommended",
      "category": "AI / data agents",
      "domain": "data_ml",
      "capabilities": [
        "machine-learning",
        "agent",
        "data"
      ],
      "languages": [
        "makefile"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39776,
        "forks": 6243,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T21:37:33Z"
      },
      "bestFor": [
        "machine-learning workflows",
        "agentic workflows",
        "data pipelines"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "RSSNext/Folo",
      "score": 8.9,
      "tier": "specialized",
      "category": "Productivity / RSS",
      "domain": "productivity",
      "capabilities": [
        "rss",
        "information-management"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39055,
        "forks": 2133,
        "openIssues": 122,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-04T12:25:12Z"
      },
      "bestFor": [
        "rss workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "MemPalace/mempalace",
      "score": 8.9,
      "tier": "specialized",
      "category": "AI / memory",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 59409,
        "forks": 7560,
        "openIssues": 777,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-10-03T14:07:52Z"
      },
      "bestFor": [
        "retrieval and persistent-memory workflows",
        "agentic workflows"
      ],
      "avoidWhen": [
        "stateless applications with no retrieval or memory needs"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "infiniflow/ragflow",
      "score": 9.3,
      "tier": "recommended",
      "category": "AI / RAG",
      "domain": "data_ml",
      "capabilities": [
        "rag",
        "agent",
        "document-processing"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 91685,
        "forks": 10890,
        "openIssues": 1615,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T14:51:58Z"
      },
      "bestFor": [
        "retrieval-augmented generation",
        "agentic workflows"
      ],
      "avoidWhen": [
        "deterministic non-ML tasks"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Mafifrizi/ARES",
      "score": 8.8,
      "tier": "specialized",
      "category": "Cybersecurity / red teaming",
      "domain": "cybersecurity",
      "capabilities": [
        "red-team",
        "security-audit",
        "agent"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 589,
        "forks": 103,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-01T23:21:17Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "non-security workloads"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "vercel-labs/json-render",
      "score": 9,
      "tier": "recommended",
      "category": "Web / generative UI",
      "domain": "web_frontend",
      "capabilities": [
        "generative-ui",
        "agent-ui"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 18495,
        "forks": 984,
        "openIssues": 135,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T06:51:42Z"
      },
      "bestFor": [
        "generative ui workflows"
      ],
      "avoidWhen": [
        "backend-only services"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "higgsfield-ai/higgsfield",
      "score": 8.8,
      "tier": "specialized",
      "category": "Data / ML infrastructure",
      "domain": "data_ml",
      "capabilities": [
        "machine-learning",
        "gpu-orchestration",
        "distributed-training"
      ],
      "languages": [
        "jupyter-notebook"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 5866,
        "forks": 1054,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T02:46:36Z"
      },
      "bestFor": [
        "machine-learning workflows"
      ],
      "avoidWhen": [
        "low-resource environments",
        "projects requiring minimal setup and operational complexity"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mihail911/modern-software-dev-assignments",
      "score": 8.3,
      "tier": "specialized",
      "category": "Software engineering / learning",
      "domain": "software_engineering",
      "capabilities": [
        "software-engineering",
        "learning-resources"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 5073,
        "forks": 1092,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-09-28T18:09:31Z"
      },
      "bestFor": [
        "software engineering workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file",
      "licenseStatus": "not-found"
    },
    {
      "repo": "paperless-ngx/paperless-ngx",
      "score": 9.3,
      "tier": "recommended",
      "category": "Productivity / document management",
      "domain": "productivity",
      "capabilities": [
        "document-management",
        "ocr",
        "archive"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 46289,
        "forks": 3205,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-05T03:53:43Z"
      },
      "bestFor": [
        "document management workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "anthropics/financial-services",
      "score": 9,
      "tier": "recommended",
      "category": "AI / financial services",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "finance"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 38745,
        "forks": 5556,
        "openIssues": 230,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-21T21:10:41Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "trycua/cua",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / computer use",
      "domain": "ai_agents",
      "capabilities": [
        "computer-use",
        "agent",
        "automation"
      ],
      "languages": [
        "html"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 28101,
        "forks": 1993,
        "openIssues": 1039,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:21:13Z"
      },
      "bestFor": [
        "agentic workflows",
        "workflow automation"
      ],
      "avoidWhen": [
        "low-resource environments",
        "projects requiring minimal setup and operational complexity"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Graphify-Labs/graphify",
      "score": 9.5,
      "tier": "recommended",
      "category": "Software engineering / code intelligence",
      "domain": "software_engineering",
      "capabilities": [
        "code-intelligence",
        "knowledge-graph",
        "agent-context"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 123909,
        "forks": 11955,
        "openIssues": 1527,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v8",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T21:28:20Z"
      },
      "bestFor": [
        "code intelligence workflows"
      ],
      "avoidWhen": [
        "non-development workflows"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "cookiy-ai/user-research-skill",
      "score": 8.5,
      "tier": "specialized",
      "category": "Productivity / user research",
      "domain": "productivity",
      "capabilities": [
        "agent-skill",
        "user-research"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 1563,
        "forks": 65,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-19T11:20:36Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "199-biotechnologies/claude-deep-research-skill",
      "score": 8.6,
      "tier": "specialized",
      "category": "AI / research agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent-skill",
        "deep-research",
        "source-validation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 1167,
        "forks": 124,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-04-11T22:18:08Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "no-root-license-file"
    },
    {
      "repo": "mvanhorn/last30days-skill",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / web research",
      "domain": "ai_agents",
      "capabilities": [
        "agent-skill",
        "web-research",
        "social-research"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 63541,
        "forks": 5534,
        "openIssues": 164,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T18:44:09Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "ZeroPointRepo/youtube-skills",
      "score": 8.4,
      "tier": "specialized",
      "category": "AI / media research",
      "domain": "ai_agents",
      "capabilities": [
        "agent-skill",
        "youtube",
        "transcripts"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 1012,
        "forks": 111,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-29T23:05:52Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "bevibing/tutor-skills",
      "score": 8.4,
      "tier": "specialized",
      "category": "Productivity / learning",
      "domain": "productivity",
      "capabilities": [
        "agent-skill",
        "study-tools",
        "obsidian"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 1320,
        "forks": 124,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-02-28T14:41:09Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Paramchoudhary/ResumeSkills",
      "score": 8.5,
      "tier": "specialized",
      "category": "Productivity / career",
      "domain": "productivity",
      "capabilities": [
        "agent-skill",
        "resume",
        "job-search"
      ],
      "languages": [
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 2551,
        "forks": 215,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-06-19T07:20:29Z"
      },
      "bestFor": [
        "agent skill workflows"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "career-ops-hq/career-ops",
      "score": 9.2,
      "tier": "recommended",
      "category": "Productivity / career automation",
      "domain": "productivity",
      "capabilities": [
        "agent",
        "job-search",
        "resume",
        "automation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73505,
        "forks": 13809,
        "openIssues": 402,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T05:11:11Z"
      },
      "bestFor": [
        "agentic workflows",
        "workflow automation"
      ],
      "avoidWhen": [
        "specialized low-level systems work"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "Dokploy/dokploy",
      "score": 9.2,
      "tier": "recommended",
      "category": "DevOps / deployment platform",
      "domain": "devops",
      "capabilities": [
        "deployment",
        "paas",
        "self-hosting"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "linux"
      ],
      "selfHosted": true,
      "runtime": [
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 37660,
        "forks": 3045,
        "openIssues": 756,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "Apache-2.0 with proprietary components",
        "pushedAt": "2026-10-01T14:35:33Z"
      },
      "bestFor": [
        "application deployment"
      ],
      "avoidWhen": [
        "local-only scripts with no deployment or operations needs"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "CopilotKit/CopilotKit",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / agent UI",
      "domain": "ai_agents",
      "capabilities": [
        "agent-ui",
        "generative-ui",
        "agent"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "web",
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 37747,
        "forks": 4698,
        "openIssues": 297,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T11:19:55Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "unslothai/unsloth",
      "score": 9.6,
      "tier": "core",
      "category": "Data / local model training",
      "domain": "data_ml",
      "capabilities": [
        "llm-training",
        "fine-tuning",
        "local-models"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 77207,
        "forks": 7113,
        "openIssues": 919,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:22:34Z"
      },
      "bestFor": [
        "efficient LLM fine-tuning",
        "local model-training optimization",
        "LoRA and QLoRA workflows"
      ],
      "avoidWhen": [
        "CPU-only low-memory machines",
        "non-LLM machine-learning workloads"
      ]
    },
    {
      "repo": "aaif-goose/goose",
      "score": 9.4,
      "tier": "recommended",
      "category": "AI / coding agents",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "coding",
        "tool-use"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 54949,
        "forks": 6362,
        "openIssues": 431,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T11:18:48Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks",
        "tool-using agent workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "code-yeongyu/oh-my-openagent",
      "score": 9.2,
      "tier": "recommended",
      "category": "AI / agent orchestration",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "orchestration",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 69805,
        "forks": 5746,
        "openIssues": 1134,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "Sustainable Use License",
        "pushedAt": "2026-10-05T08:25:56Z"
      },
      "bestFor": [
        "agentic workflows",
        "agentic coding tasks"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred",
      "licenseEvidence": "verified-file"
    },
    {
      "repo": "agno-agi/agno",
      "score": 9.5,
      "tier": "recommended",
      "category": "AI / agent platform",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "agent-platform",
        "orchestration"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 42557,
        "forks": 6099,
        "openIssues": 1812,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T10:21:18Z"
      },
      "bestFor": [
        "agentic workflows"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "mindsdb/mindshub",
      "score": 9,
      "tier": "recommended",
      "category": "AI / model workspace",
      "domain": "ai_agents",
      "capabilities": [
        "model-workspace",
        "agent",
        "automation"
      ],
      "languages": [
        "makefile"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39776,
        "forks": 6243,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T21:37:33Z"
      },
      "bestFor": [
        "agentic workflows",
        "workflow automation"
      ],
      "avoidWhen": [
        "simple deterministic scripts without agent orchestration"
      ],
      "guidanceSource": "inferred"
    },
    {
      "repo": "langflow-ai/langflow",
      "score": 9.6,
      "tier": "recommended",
      "category": "AI / agent platforms",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "workflow",
        "visual-builder",
        "mcp-server"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "bestFor": [
        "visual AI agent workflows",
        "self-hosted agent orchestration",
        "deploying workflows as APIs or MCP servers"
      ],
      "avoidWhen": [
        "minimal headless-only agent runtime",
        "very low-resource environments"
      ],
      "alternatives": [
        "langgenius/dify",
        "FlowiseAI/Flowise"
      ],
      "complements": [
        "modelcontextprotocol/servers"
      ],
      "github": {
        "stars": 155501,
        "forks": 10180,
        "openIssues": 1205,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T04:48:57Z"
      }
    },
    {
      "repo": "stefan-jansen/zipline-reloaded",
      "score": 8.9,
      "tier": "specialized",
      "category": "Trading / quant / backtesting",
      "domain": "trading",
      "capabilities": [
        "backtesting",
        "code-quality",
        "backtest"
      ],
      "roles": [
        "backtest"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "lifecycle": "active",
      "bestFor": [
        "maintained Zipline-compatible backtesting",
        "event-driven Python strategy research"
      ],
      "avoidWhen": [
        "ultra-low-latency execution",
        "non-Python trading stacks"
      ],
      "alternatives": [
        "QuantConnect/Lean",
        "kernc/backtesting.py",
        "quantopian/zipline"
      ],
      "complements": [
        "ranaroussi/yfinance",
        "stefan-jansen/pyfolio-reloaded"
      ],
      "github": {
        "stars": 1952,
        "forks": 331,
        "openIssues": 48,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-01-06T13:01:54Z"
      }
    },
    {
      "repo": "stefan-jansen/pyfolio-reloaded",
      "score": 8.8,
      "tier": "specialized",
      "category": "Trading / optimisation du rendement et du risque",
      "domain": "trading",
      "capabilities": [
        "risk",
        "performance"
      ],
      "roles": [
        "performance",
        "risk"
      ],
      "languages": [
        "python",
        "jupyter notebook"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local",
        "self-hosted"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "lifecycle": "active",
      "bestFor": [
        "portfolio tear sheets",
        "Python risk and performance analytics"
      ],
      "avoidWhen": [
        "full execution engines",
        "non-Python analytics stacks"
      ],
      "alternatives": [
        "ranaroussi/quantstats",
        "quantopian/pyfolio"
      ],
      "complements": [
        "stefan-jansen/zipline-reloaded",
        "skfolio/skfolio"
      ],
      "github": {
        "stars": 616,
        "forks": 175,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-12-15T11:02:30Z"
      }
    },
    {
      "repo": "2Retr0/GodotOceanWaves",
      "score": 8.5,
      "tier": "specialized",
      "category": "Godot / effets d'eau",
      "domain": "game_dev",
      "capabilities": [
        "rendering",
        "game-development"
      ],
      "languages": [
        "csharp"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3304,
        "forks": 197,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-04-29T17:17:08Z"
      },
      "bestFor": [
        "Godot ocean FFT shaders"
      ],
      "avoidWhen": [
        "non-Godot projects"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "agentverse-os/AgentVerse-OS",
      "score": 8.2,
      "tier": "specialized",
      "category": "Espaces de travail IA / serveur",
      "domain": "devops",
      "capabilities": [
        "self-hosted",
        "sandbox",
        "agent"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 977,
        "forks": 26,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-04T11:34:49Z"
      },
      "bestFor": [
        "single-server agent workspaces"
      ],
      "avoidWhen": [
        "teams requiring a managed enterprise cloud"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "anmolkapil/plexo",
      "score": 8,
      "tier": "specialized",
      "category": "Téléchargements / outils réseau",
      "domain": "software_engineering",
      "capabilities": [
        "network-downloads",
        "automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1497,
        "forks": 130,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T18:44:57Z"
      },
      "bestFor": [
        "parallel connection downloads"
      ],
      "avoidWhen": [
        "applications not handling file transfers"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "Antseed/AIPs",
      "score": 6.5,
      "tier": "audit",
      "category": "Spécifications protocole AntSeed",
      "domain": "other",
      "capabilities": [
        "documentation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 5,
        "forks": 3,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC0-1.0",
        "pushedAt": "2026-10-04T05:38:14Z"
      },
      "bestFor": [
        "AntSeed protocol design references"
      ],
      "avoidWhen": [
        "general-purpose AI deployment"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "Antseed/antseed",
      "score": 7.2,
      "tier": "audit",
      "category": "Réseau P2P d'inférence IA",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "networking"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 109,
        "forks": 37,
        "openIssues": 111,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-10-09T01:04:09Z"
      },
      "bestFor": [
        "experimental peer-to-peer inference architecture"
      ],
      "avoidWhen": [
        "verified secure production inference"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "Antseed/openclaw-channel-antseed",
      "score": 6.5,
      "tier": "audit",
      "category": "Réseaux d'agents expérimentaux",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "networking"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 4,
        "forks": 0,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-02-28T20:09:24Z"
      },
      "bestFor": [
        "experimental OpenClaw channel integration"
      ],
      "avoidWhen": [
        "production-critical infrastructure"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "arnegiacomo/fugleramme",
      "score": 8.1,
      "tier": "specialized",
      "category": "Vision et audio local",
      "domain": "ai_media",
      "capabilities": [
        "voice-audio",
        "rendering",
        "local-models"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3594,
        "forks": 113,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T17:24:02Z"
      },
      "bestFor": [
        "local bird-audio recognition and e-ink displays"
      ],
      "avoidWhen": [
        "general-purpose image generation"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "axstin/rbxfpsunlocker",
      "score": 6,
      "tier": "audit",
      "category": "Roblox / utilitaire historique",
      "domain": "game_dev",
      "capabilities": [
        "performance"
      ],
      "languages": [
        "cpp"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2226,
        "forks": 878,
        "openIssues": 78,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-06-21T18:43:29Z"
      },
      "bestFor": [
        "historical Roblox FPS unlocker reference"
      ],
      "avoidWhen": [
        "modern actively maintained Roblox tooling"
      ],
      "guidanceSource": "curated",
      "lifecycle": "legacy"
    },
    {
      "repo": "chubbyguan/chubbyskills",
      "score": 8.1,
      "tier": "specialized",
      "category": "Collecte et recherche personnelle",
      "domain": "productivity",
      "capabilities": [
        "automation",
        "mcp-server",
        "knowledge-base"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1203,
        "forks": 147,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T09:43:23Z"
      },
      "bestFor": [
        "Chinese-language content ingestion and knowledge bases"
      ],
      "avoidWhen": [
        "English-only content pipelines"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "colbymchenry/codegraph",
      "score": 9.4,
      "tier": "recommended",
      "category": "Indexation de code / graphes",
      "domain": "software_engineering",
      "capabilities": [
        "code-search",
        "knowledge-graph",
        "memory"
      ],
      "languages": [
        "c"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73508,
        "forks": 4731,
        "openIssues": 527,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-07T16:34:38Z"
      },
      "bestFor": [
        "local codebase graph indexing for coding agents"
      ],
      "avoidWhen": [
        "tiny single-file repositories"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "comet-ml/opik",
      "score": 9.1,
      "tier": "recommended",
      "category": "Observabilité et évaluation LLM",
      "domain": "data_ml",
      "capabilities": [
        "observability",
        "testing",
        "rag"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 22464,
        "forks": 1847,
        "openIssues": 198,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:08:08Z"
      },
      "bestFor": [
        "LLM traces and RAG evaluation"
      ],
      "avoidWhen": [
        "simple applications without model tracing"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "D4Vinci/Scrapling",
      "score": 9.1,
      "tier": "recommended",
      "category": "Extraction Web / automatisation",
      "domain": "software_engineering",
      "capabilities": [
        "web-retrieval",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 86388,
        "forks": 8858,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-08T20:28:21Z"
      },
      "bestFor": [
        "adaptive web extraction and crawling"
      ],
      "avoidWhen": [
        "sites where collection is unauthorized"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "daytonaio/daytona",
      "score": 6.4,
      "tier": "audit",
      "category": "Sandboxing / exécution isolée",
      "domain": "software_engineering",
      "capabilities": [
        "sandbox",
        "code-execution"
      ],
      "languages": [],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 71596,
        "forks": 5646,
        "openIssues": 458,
        "archived": true,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-07-24T07:12:07Z"
      },
      "bestFor": [
        "historical sandbox infrastructure reference"
      ],
      "avoidWhen": [
        "new production deployments requiring active maintenance"
      ],
      "guidanceSource": "curated",
      "lifecycle": "legacy"
    },
    {
      "repo": "Effect-TS/effect",
      "score": 9.3,
      "tier": "recommended",
      "category": "TypeScript / programmation fiable",
      "domain": "software_engineering",
      "capabilities": [
        "typescript",
        "backend",
        "testing"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 17176,
        "forks": 843,
        "openIssues": 243,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T23:59:51Z"
      },
      "bestFor": [
        "typed effect systems for TypeScript"
      ],
      "avoidWhen": [
        "small scripts without structured effect needs"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "elliothux/open-compute",
      "score": 8.3,
      "tier": "specialized",
      "category": "Cloudflare-compatible self hosting",
      "domain": "devops",
      "capabilities": [
        "infrastructure",
        "self-hosted",
        "runtime"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 1776,
        "forks": 65,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T18:58:00Z"
      },
      "bestFor": [
        "self-hosted Workers-compatible infrastructure"
      ],
      "avoidWhen": [
        "managed Cloudflare-only deployments"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "Epix-Incorporated/Adonis",
      "score": 8.1,
      "tier": "specialized",
      "category": "Roblox / administration serveur",
      "domain": "game_dev",
      "capabilities": [
        "game-development",
        "server-administration"
      ],
      "languages": [
        "luau"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 508,
        "forks": 237,
        "openIssues": 65,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-07T19:34:32Z"
      },
      "bestFor": [
        "Roblox server administration workflows"
      ],
      "avoidWhen": [
        "non-Roblox games"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "evidentlyai/evidently",
      "score": 9.1,
      "tier": "recommended",
      "category": "Évaluation et surveillance ML/LLM",
      "domain": "data_ml",
      "capabilities": [
        "machine-learning",
        "observability",
        "testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 7978,
        "forks": 947,
        "openIssues": 328,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-29T08:32:43Z"
      },
      "bestFor": [
        "ML data and LLM monitoring"
      ],
      "avoidWhen": [
        "applications without quality or drift metrics"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "getzep/graphiti",
      "score": 9.3,
      "tier": "recommended",
      "category": "Graphes de connaissance / mémoire IA",
      "domain": "ai_memory",
      "capabilities": [
        "memory",
        "knowledge-graph",
        "rag"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 31569,
        "forks": 3242,
        "openIssues": 462,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-07T19:12:47Z"
      },
      "bestFor": [
        "real-time knowledge graphs for agents"
      ],
      "avoidWhen": [
        "stateless agents with no long-term knowledge"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "Giskard-AI/giskard-oss",
      "score": 9.1,
      "tier": "recommended",
      "category": "Tests et évaluation d'agents IA",
      "domain": "data_ml",
      "capabilities": [
        "testing",
        "agent",
        "diagnostic"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 5879,
        "forks": 547,
        "openIssues": 70,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T07:10:15Z"
      },
      "bestFor": [
        "evaluating LLM agents and application behavior"
      ],
      "avoidWhen": [
        "projects without LLM evaluation requirements"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "google/skills",
      "score": 9.1,
      "tier": "recommended",
      "category": "Bibliothèque de compétences IA",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "tool-use",
        "documentation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 21061,
        "forks": 1756,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:12:41Z"
      },
      "bestFor": [
        "agent skills for Google products"
      ],
      "avoidWhen": [
        "tools unrelated to Google ecosystems"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits",
      "score": 8,
      "tier": "specialized",
      "category": "Marchés prédictifs / outils de trading",
      "domain": "trading",
      "capabilities": [
        "execution",
        "automation",
        "risk"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 472,
        "forks": 127,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-07T11:44:40Z"
      },
      "bestFor": [
        "researching prediction-market execution"
      ],
      "avoidWhen": [
        "unreviewed or unauthorized live trading"
      ],
      "guidanceSource": "curated",
      "roles": [
        "execution"
      ]
    },
    {
      "repo": "huggingface/smolagents",
      "score": 9.2,
      "tier": "recommended",
      "category": "Agents légers / outils",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "tool-use",
        "coding"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 29742,
        "forks": 3051,
        "openIssues": 881,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T18:35:07Z"
      },
      "bestFor": [
        "minimal code-oriented AI agents"
      ],
      "avoidWhen": [
        "heavy enterprise orchestration with extensive controls"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "Ignitetechnologies/Mindmap",
      "score": 8,
      "tier": "specialized",
      "category": "Ressources pédagogiques cybersécurité",
      "domain": "cybersecurity",
      "capabilities": [
        "documentation",
        "security-testing"
      ],
      "languages": [],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "unknown",
      "github": {
        "stars": 9348,
        "forks": 1826,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-07-21T15:47:21Z"
      },
      "bestFor": [
        "cybersecurity learning mind maps"
      ],
      "avoidWhen": [
        "runtime security scanning"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "InfinityLoop1308/PipePipe",
      "score": 8.3,
      "tier": "specialized",
      "category": "Client Android multimédia",
      "domain": "mobile",
      "capabilities": [
        "mobile",
        "video"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6918,
        "forks": 246,
        "openIssues": 170,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-26T08:12:59Z"
      },
      "bestFor": [
        "reference for open-source Android video clients"
      ],
      "avoidWhen": [
        "browser-only applications"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "jamwithai/production-agentic-rag-course",
      "score": 8.4,
      "tier": "specialized",
      "category": "Formation RAG agentique",
      "domain": "ai_agents",
      "capabilities": [
        "rag",
        "agent",
        "documentation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 9679,
        "forks": 2103,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-06-05T07:23:49Z"
      },
      "bestFor": [
        "learning production agentic RAG workflows"
      ],
      "avoidWhen": [
        "projects needing maintained turnkey production software"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "JoasASantos/Offensive-Security-AI-Models",
      "score": 6.9,
      "tier": "audit",
      "category": "Références modèles de sécurité IA",
      "domain": "cybersecurity",
      "capabilities": [
        "documentation",
        "security-testing"
      ],
      "languages": [],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "unknown",
      "github": {
        "stars": 646,
        "forks": 75,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-28T14:34:47Z"
      },
      "bestFor": [
        "researching security-focused model listings"
      ],
      "avoidWhen": [
        "unreviewed model deployment or unauthorized use"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "JuliusBrussee/caveman",
      "score": 8,
      "tier": "specialized",
      "category": "Optimisation contexte LLM",
      "domain": "software_engineering",
      "capabilities": [
        "coding",
        "optimization"
      ],
      "languages": [
        "go"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 110586,
        "forks": 6404,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T13:28:29Z"
      },
      "bestFor": [
        "testing concise coding-agent communication"
      ],
      "avoidWhen": [
        "work requiring complete uncompressed context"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "letta-ai/letta-code",
      "score": 8.8,
      "tier": "specialized",
      "category": "Agents à mémoire persistante",
      "domain": "ai_memory",
      "capabilities": [
        "agent",
        "memory",
        "coding"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3550,
        "forks": 430,
        "openIssues": 501,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:15:10Z"
      },
      "bestFor": [
        "stateful coding agents with persistent context"
      ],
      "avoidWhen": [
        "one-shot stateless code edits"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "lihanyu81/polymarket_lp_tool",
      "score": 6.8,
      "tier": "audit",
      "category": "Marchés prédictifs / liquidité",
      "domain": "trading",
      "capabilities": [
        "market-data"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 559,
        "forks": 98,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-05-06T05:41:52Z"
      },
      "bestFor": [
        "reviewing prediction-market liquidity tools"
      ],
      "avoidWhen": [
        "live money execution without code and legal review"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference",
      "roles": [
        "execution"
      ]
    },
    {
      "repo": "NVIDIA/OpenShell",
      "score": 9.2,
      "tier": "recommended",
      "category": "Exécution privée / isolation agents",
      "domain": "ai_agents",
      "capabilities": [
        "sandbox",
        "agent",
        "runtime"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15480,
        "forks": 1743,
        "openIssues": 576,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:24:52Z"
      },
      "bestFor": [
        "private agent runtimes with isolation"
      ],
      "avoidWhen": [
        "tasks with no agent execution"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "OffGridPete/Fieldwatch",
      "score": 8.1,
      "tier": "specialized",
      "category": "Android / observation radio passive",
      "domain": "cybersecurity",
      "capabilities": [
        "mobile",
        "wireless-monitoring"
      ],
      "languages": [
        "kotlin"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 2824,
        "forks": 336,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-06T16:25:56Z"
      },
      "bestFor": [
        "receive-only Wi-Fi and BLE observation on Android"
      ],
      "avoidWhen": [
        "active penetration testing or packet injection"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "owncloud/android",
      "score": 8.4,
      "tier": "specialized",
      "category": "Android / synchronisation",
      "domain": "mobile",
      "capabilities": [
        "mobile",
        "sync"
      ],
      "languages": [
        "kotlin"
      ],
      "platforms": [
        "android"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4172,
        "forks": 3083,
        "openIssues": 206,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T03:11:03Z"
      },
      "bestFor": [
        "ownCloud Android client architecture"
      ],
      "avoidWhen": [
        "projects unrelated to ownCloud"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "pizza-bot-app/pizza-bot",
      "score": 8.1,
      "tier": "specialized",
      "category": "Coordination d'agents longue durée",
      "domain": "ai_agents",
      "capabilities": [
        "agent",
        "memory",
        "workflow"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 460,
        "forks": 45,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-05T21:50:33Z"
      },
      "bestFor": [
        "local-first inboxes for long-running agents"
      ],
      "avoidWhen": [
        "simple single-call LLM tasks"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "recogardtech/AutoPilotPM",
      "score": 6.7,
      "tier": "audit",
      "category": "Trading automatisé expérimental",
      "domain": "trading",
      "capabilities": [
        "execution",
        "agent",
        "automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 33,
        "forks": 9,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T10:01:24Z"
      },
      "bestFor": [
        "experimental multi-market automation reference"
      ],
      "avoidWhen": [
        "production trading without extensive testing"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference",
      "roles": [
        "execution"
      ]
    },
    {
      "repo": "roblox-ts/roblox-ts",
      "score": 8.8,
      "tier": "specialized",
      "category": "Roblox / TypeScript vers Luau",
      "domain": "game_dev",
      "capabilities": [
        "game-development",
        "typescript",
        "build-system"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1311,
        "forks": 178,
        "openIssues": 135,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-05T06:03:05Z"
      },
      "bestFor": [
        "TypeScript development targeting Roblox Luau"
      ],
      "avoidWhen": [
        "Roblox scripts written only in Lua"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "shadcn-ui/lint",
      "score": 9.1,
      "tier": "recommended",
      "category": "Design systems / lint",
      "domain": "web_frontend",
      "capabilities": [
        "design-system",
        "static-analysis",
        "css"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3137,
        "forks": 62,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T07:58:39Z"
      },
      "bestFor": [
        "Tailwind design-system linting"
      ],
      "avoidWhen": [
        "applications without Tailwind"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "togg53192-cmd/jailbreaks",
      "score": 6.1,
      "tier": "audit",
      "category": "Sécurité / ressources de référence",
      "domain": "cybersecurity",
      "capabilities": [
        "documentation"
      ],
      "languages": [],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "unknown",
      "github": {
        "stars": 2619,
        "forks": 431,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-08T19:55:45Z"
      },
      "bestFor": [
        "reference collection for prompt-injection research"
      ],
      "avoidWhen": [
        "production AI policy bypasses"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "truera/trulens",
      "score": 8.8,
      "tier": "specialized",
      "category": "Évaluation / traçabilité LLM",
      "domain": "data_ml",
      "capabilities": [
        "testing",
        "observability",
        "rag"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 3594,
        "forks": 360,
        "openIssues": 96,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:17:07Z"
      },
      "bestFor": [
        "LLM experiment evaluation and tracing"
      ],
      "avoidWhen": [
        "non-LLM web analytics"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "UKGovernmentBEIS/inspect_ai",
      "score": 9,
      "tier": "recommended",
      "category": "Évaluation de modèles LLM",
      "domain": "data_ml",
      "capabilities": [
        "testing",
        "machine-learning"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 2962,
        "forks": 791,
        "openIssues": 375,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:16:04Z"
      },
      "bestFor": [
        "repeatable evaluations of large language models"
      ],
      "avoidWhen": [
        "applications without model evaluation needs"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "vibrantlabsai/ragas",
      "score": 8.7,
      "tier": "specialized",
      "category": "Évaluation des systèmes RAG",
      "domain": "data_ml",
      "capabilities": [
        "rag",
        "testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 15967,
        "forks": 1750,
        "openIssues": 626,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-02-24T07:47:19Z"
      },
      "bestFor": [
        "RAG quality assessments and evaluation"
      ],
      "avoidWhen": [
        "non-RAG or non-LLM systems"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "vinnylarouge/jevlike",
      "score": 6,
      "tier": "audit",
      "category": "Projet non documenté",
      "domain": "other",
      "capabilities": [
        "documentation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": false,
      "runtime": [],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 1352,
        "forks": 118,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T18:12:53Z"
      },
      "bestFor": [
        "manual source review before reuse"
      ],
      "avoidWhen": [
        "selection based on absent README description"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "whaleyxbt/patchright-enhanced",
      "score": 7.2,
      "tier": "audit",
      "category": "Automatisation navigateur / QA",
      "domain": "software_engineering",
      "capabilities": [
        "automation",
        "testing"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 486,
        "forks": 89,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-06T14:52:34Z"
      },
      "bestFor": [
        "researching browser QA and monitoring workflows"
      ],
      "avoidWhen": [
        "production use before licensing and provenance checks"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "yejy53/Editable-Design",
      "score": 8.1,
      "tier": "specialized",
      "category": "Graphisme génératif éditable",
      "domain": "graphics",
      "capabilities": [
        "design-system",
        "rendering"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1155,
        "forks": 80,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-29T09:59:55Z"
      },
      "bestFor": [
        "editable AI-generated design artifacts"
      ],
      "avoidWhen": [
        "purely non-visual automation"
      ],
      "guidanceSource": "curated"
    },
    {
      "repo": "1N3/Sn1per",
      "score": 7.2,
      "tier": "audit",
      "category": "OSINT et reconnaissance autorisée",
      "domain": "cybersecurity",
      "capabilities": [
        "osint",
        "recon"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 11393,
        "forks": 2210,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-07-04T21:10:21Z"
      },
      "bestFor": [
        "Collecter et corréler des données publiques sur un périmètre autorisé"
      ],
      "avoidWhen": [
        "Reconnaissance non autorisée ou non cadrée"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "aarora4/Awesome-Prediction-Market-Tools",
      "score": 7.2,
      "tier": "audit",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 767,
        "forks": 268,
        "openIssues": 147,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T03:03:02Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "AILab-CVC/VideoCrafter",
      "score": 7.2,
      "tier": "audit",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 5098,
        "forks": 411,
        "openIssues": 74,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-01-09T15:01:22Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "apache/tika",
      "score": 8.2,
      "tier": "specialized",
      "category": "Extraction et structuration de documents",
      "domain": "data_ml",
      "capabilities": [
        "document-processing",
        "extraction"
      ],
      "languages": [
        "java"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 4090,
        "forks": 1005,
        "openIssues": 58,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:08:29Z"
      },
      "bestFor": [
        "Extraire le contenu de documents pour la recherche et l'IA"
      ],
      "avoidWhen": [
        "Documents sensibles sans contrôles de confidentialité"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "boykopovar/AnyPS5",
      "score": 8.2,
      "tier": "specialized",
      "category": "Outils de compatibilité PS5",
      "domain": "game_dev",
      "capabilities": [
        "playstation",
        "porting"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 15910,
        "forks": 1256,
        "openIssues": 554,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T22:46:53Z"
      },
      "bestFor": [
        "Étudier les outils de portage pour exécutables PS5 détenus légalement"
      ],
      "avoidWhen": [
        "Distribution non autorisée de logiciels et contenus protégés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "caddyserver/caddy",
      "score": 8.2,
      "tier": "specialized",
      "category": "Serveur HTTP et reverse proxy",
      "domain": "backend",
      "capabilities": [
        "web-server",
        "https"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 77554,
        "forks": 5102,
        "openIssues": 287,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T04:02:21Z"
      },
      "bestFor": [
        "Déployer un reverse proxy HTTPS et servir des applications web"
      ],
      "avoidWhen": [
        "Environnements sans accès aux ports ou configuration réseau"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "caiovicentino/polymarket-mcp-server",
      "score": 8.2,
      "tier": "specialized",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 689,
        "forks": 143,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:04:03Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "cantolab/open-source-fractal",
      "score": 8.2,
      "tier": "specialized",
      "category": "Indicateurs et scripts TradingView",
      "domain": "trading",
      "capabilities": [
        "technical-analysis",
        "indicators"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 173,
        "forks": 58,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-25T21:23:05Z"
      },
      "bestFor": [
        "Analyser les marchés avec des indicateurs techniques"
      ],
      "avoidWhen": [
        "Décisions d'investissement prises sur un indicateur isolé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "regime"
      ]
    },
    {
      "repo": "cloudflare/cloudflare-os",
      "score": 8.2,
      "tier": "specialized",
      "category": "Espace de travail d'agents IA",
      "domain": "ai_agents",
      "capabilities": [
        "agents",
        "workspace"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": "partial",
      "runtime": [
        "cloud"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 11285,
        "forks": 1346,
        "openIssues": 132,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T22:40:55Z"
      },
      "bestFor": [
        "Construire des espaces de travail et des flux pour agents IA"
      ],
      "avoidWhen": [
        "Fonctionnement totalement hors ligne sans adaptation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "ComposioHQ/composio",
      "score": 8.2,
      "tier": "specialized",
      "category": "Espace de travail d'agents IA",
      "domain": "ai_agents",
      "capabilities": [
        "agents",
        "workspace"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": "partial",
      "runtime": [
        "cloud"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 30474,
        "forks": 4848,
        "openIssues": 110,
        "archived": false,
        "disabled": false,
        "defaultBranch": "next",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:09:09Z"
      },
      "bestFor": [
        "Construire des espaces de travail et des flux pour agents IA"
      ],
      "avoidWhen": [
        "Fonctionnement totalement hors ligne sans adaptation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "datalab-to/marker",
      "score": 8.2,
      "tier": "specialized",
      "category": "Extraction et structuration de documents",
      "domain": "data_ml",
      "capabilities": [
        "document-processing",
        "extraction"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 40292,
        "forks": 2913,
        "openIssues": 477,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-02T09:53:02Z"
      },
      "bestFor": [
        "Extraire le contenu de documents pour la recherche et l'IA"
      ],
      "avoidWhen": [
        "Documents sensibles sans contrôles de confidentialité"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "deepseek-ai/DeepGEMM",
      "score": 8.2,
      "tier": "specialized",
      "category": "Optimisation GPU pour ML",
      "domain": "data_ml",
      "capabilities": [
        "gpu",
        "performance"
      ],
      "languages": [
        "cuda"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 8880,
        "forks": 1396,
        "openIssues": 151,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-30T01:48:05Z"
      },
      "bestFor": [
        "Optimiser des calculs de réseaux neuronaux sur GPU"
      ],
      "avoidWhen": [
        "Machines sans accélérateur compatible"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Diolinux/PhotoGIMP",
      "score": 8.2,
      "tier": "specialized",
      "category": "Retouche et création graphique",
      "domain": "graphics",
      "capabilities": [
        "image-editing",
        "graphics"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 18328,
        "forks": 745,
        "openIssues": 43,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-27T05:10:17Z"
      },
      "bestFor": [
        "Retoucher et produire des visuels avec des outils graphiques"
      ],
      "avoidWhen": [
        "Flux exigeant des logiciels propriétaires non compatibles"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "DuarteSantos8/openGym",
      "score": 8.2,
      "tier": "specialized",
      "category": "Suivi sportif autonome",
      "domain": "productivity",
      "capabilities": [
        "self-hosted",
        "tracking"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8039,
        "forks": 1024,
        "openIssues": 152,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T13:32:09Z"
      },
      "bestFor": [
        "Suivre les entraînements sur un service auto-hébergé"
      ],
      "avoidWhen": [
        "Besoin d'une application sans maintenance serveur"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "earthtojake/text-to-cad",
      "score": 8.2,
      "tier": "specialized",
      "category": "Conception CAD par langage naturel",
      "domain": "graphics",
      "capabilities": [
        "cad",
        "agent-tools"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 18479,
        "forks": 1834,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:16:19Z"
      },
      "bestFor": [
        "Produire et itérer des modèles de conception assistée par ordinateur"
      ],
      "avoidWhen": [
        "Production industrielle sans validation géométrique"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "elder-plinius/T3MP3ST",
      "score": 8.2,
      "tier": "specialized",
      "category": "Plateforme de red team en laboratoire",
      "domain": "cybersecurity",
      "capabilities": [
        "red-team",
        "automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 6452,
        "forks": 1331,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-08T16:37:44Z"
      },
      "bestFor": [
        "Conduire des tests de sécurité en laboratoire ou sur périmètre autorisé"
      ],
      "avoidWhen": [
        "Opérations offensives sans consentement explicite"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "emilk/egui",
      "score": 8.2,
      "tier": "specialized",
      "category": "Interfaces graphiques Rust",
      "domain": "web_frontend",
      "capabilities": [
        "gui",
        "rust"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 31045,
        "forks": 2173,
        "openIssues": 1033,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T15:38:15Z"
      },
      "bestFor": [
        "Construire des interfaces natives ou web en Rust"
      ],
      "avoidWhen": [
        "Interfaces conçues exclusivement pour l'écosystème JavaScript"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "ent0n29/polybot",
      "score": 8.2,
      "tier": "specialized",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [
        "java"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 1019,
        "forks": 176,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-02-20T23:34:32Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "EpicGames/raddebugger",
      "score": 8.2,
      "tier": "specialized",
      "category": "Débogage graphique et natif",
      "domain": "game_dev",
      "capabilities": [
        "debugging",
        "profiling"
      ],
      "languages": [
        "c"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8121,
        "forks": 391,
        "openIssues": 316,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-07T20:56:17Z"
      },
      "bestFor": [
        "Diagnostiquer des applications et moteurs natifs"
      ],
      "avoidWhen": [
        "Débogage de binaires sans accès autorisé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "evan-kolberg/prediction-market-backtesting",
      "score": 7.2,
      "tier": "audit",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 1211,
        "forks": 196,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v4.1-alpha",
        "license": "NOASSERTION",
        "pushedAt": "2026-05-16T21:24:47Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "fxraptor-alpha/pinescript-indicators",
      "score": 7.2,
      "tier": "audit",
      "category": "Indicateurs et scripts TradingView",
      "domain": "trading",
      "capabilities": [
        "technical-analysis",
        "indicators"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 111,
        "forks": 42,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-06T11:42:04Z"
      },
      "bestFor": [
        "Analyser les marchés avec des indicateurs techniques"
      ],
      "avoidWhen": [
        "Décisions d'investissement prises sur un indicateur isolé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "regime"
      ]
    },
    {
      "repo": "genmoai/mochi",
      "score": 8.2,
      "tier": "specialized",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 3746,
        "forks": 494,
        "openIssues": 60,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T17:19:13Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "gh1mau/masta-cve-2026-48907",
      "score": 7.2,
      "tier": "audit",
      "category": "Recherche sur CVE",
      "domain": "cybersecurity",
      "capabilities": [
        "cve",
        "vulnerability-research"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 64,
        "forks": 12,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-06-27T05:25:46Z"
      },
      "bestFor": [
        "Examiner de manière reproductible un bulletin de vulnérabilité"
      ],
      "avoidWhen": [
        "Utilisation en production sans validation du code et du périmètre"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "github/github-mcp-server",
      "score": 8.2,
      "tier": "specialized",
      "category": "Intégration GitHub pour agents",
      "domain": "software_engineering",
      "capabilities": [
        "mcp",
        "github"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 33454,
        "forks": 5111,
        "openIssues": 346,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T16:25:41Z"
      },
      "bestFor": [
        "Piloter des opérations de développement GitHub depuis des agents"
      ],
      "avoidWhen": [
        "Tokens sur-privilégiés ou actions non relues"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "go-gitea/gitea",
      "score": 8.2,
      "tier": "specialized",
      "category": "Hébergement Git auto-administré",
      "domain": "devops",
      "capabilities": [
        "git-hosting",
        "ci"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 58373,
        "forks": 7234,
        "openIssues": 2347,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:15:36Z"
      },
      "bestFor": [
        "Héberger des dépôts et workflows Git sur une instance personnelle"
      ],
      "avoidWhen": [
        "Exploitation d'un service public sans plan de sécurité et sauvegarde"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "google-deepmind/mujoco",
      "score": 8.2,
      "tier": "specialized",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 15528,
        "forks": 1815,
        "openIssues": 292,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T20:33:34Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "guoyww/AnimateDiff",
      "score": 8.2,
      "tier": "specialized",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 12274,
        "forks": 1101,
        "openIssues": 319,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-07-31T01:14:15Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "huggingface/diffusers",
      "score": 8.2,
      "tier": "specialized",
      "category": "Modèles de diffusion multimodaux",
      "domain": "ai_media",
      "capabilities": [
        "diffusion",
        "image-generation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 34695,
        "forks": 7380,
        "openIssues": 1476,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T14:42:43Z"
      },
      "bestFor": [
        "Développer une chaîne de génération d'images et de vidéos"
      ],
      "avoidWhen": [
        "Applications sans inférence multimodale"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "huggingface/lerobot",
      "score": 8.2,
      "tier": "specialized",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 28017,
        "forks": 5839,
        "openIssues": 966,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T21:24:14Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "iamlukethedev/Herald-OS",
      "score": 8.2,
      "tier": "specialized",
      "category": "Système de travail piloté par agents",
      "domain": "ai_agents",
      "capabilities": [
        "agents",
        "workflow"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 266,
        "forks": 37,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:11:58Z"
      },
      "bestFor": [
        "Organiser un environnement de travail orienté agents"
      ],
      "avoidWhen": [
        "Confiance implicite dans les actions d'agents non supervisés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "ict2023trader/Indicators",
      "score": 7.2,
      "tier": "audit",
      "category": "Indicateurs et scripts TradingView",
      "domain": "trading",
      "capabilities": [
        "technical-analysis",
        "indicators"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 60,
        "forks": 28,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T18:52:49Z"
      },
      "bestFor": [
        "Analyser les marchés avec des indicateurs techniques"
      ],
      "avoidWhen": [
        "Décisions d'investissement prises sur un indicateur isolé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "regime"
      ]
    },
    {
      "repo": "isaac-sim/IsaacLab",
      "score": 8.2,
      "tier": "specialized",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 8299,
        "forks": 3940,
        "openIssues": 364,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-10-09T00:55:55Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "jina-ai/reader",
      "score": 8.2,
      "tier": "specialized",
      "category": "Extraction et structuration de documents",
      "domain": "data_ml",
      "capabilities": [
        "document-processing",
        "extraction"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12127,
        "forks": 892,
        "openIssues": 34,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-05-22T02:56:46Z"
      },
      "bestFor": [
        "Extraire le contenu de documents pour la recherche et l'IA"
      ],
      "avoidWhen": [
        "Documents sensibles sans contrôles de confidentialité"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "justcallmekoko/ESP32Marauder",
      "score": 7.2,
      "tier": "audit",
      "category": "Audit des objets connectés autorisés",
      "domain": "cybersecurity",
      "capabilities": [
        "iot",
        "wifi"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 12650,
        "forks": 1523,
        "openIssues": 332,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-10-08T22:09:49Z"
      },
      "bestFor": [
        "Effectuer des audits sans fil en laboratoire autorisé"
      ],
      "avoidWhen": [
        "Accès à des réseaux non autorisés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "JustExecution/HTF_indicator",
      "score": 8.2,
      "tier": "specialized",
      "category": "Indicateurs et scripts TradingView",
      "domain": "trading",
      "capabilities": [
        "technical-analysis",
        "indicators"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 122,
        "forks": 46,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-17T06:36:15Z"
      },
      "bestFor": [
        "Analyser les marchés avec des indicateurs techniques"
      ],
      "avoidWhen": [
        "Décisions d'investissement prises sur un indicateur isolé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "regime"
      ]
    },
    {
      "repo": "kargulstudio/sales-crm",
      "score": 7.2,
      "tier": "audit",
      "category": "CRM commercial",
      "domain": "productivity",
      "capabilities": [
        "crm",
        "web-app"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1658,
        "forks": 360,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-06T06:42:03Z"
      },
      "bestFor": [
        "Gérer les contacts et opportunités commerciales"
      ],
      "avoidWhen": [
        "Déploiement sans contrôle des données clients"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "LaurieWired/GhidraMCP",
      "score": 8.2,
      "tier": "specialized",
      "category": "Rétro-ingénierie assistée par IA",
      "domain": "cybersecurity",
      "capabilities": [
        "reverse-engineering",
        "analysis"
      ],
      "languages": [
        "java"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 10728,
        "forks": 1108,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-06-23T04:18:18Z"
      },
      "bestFor": [
        "Analyser des logiciels autorisés avec des outils de rétro-ingénierie"
      ],
      "avoidWhen": [
        "Analyse de logiciels tiers hors cadre légal ou contractuel"
      ],
      "guidanceSource": "curated",
      "lifecycle": "stable"
    },
    {
      "repo": "lfnovo/esperanto",
      "score": 8.2,
      "tier": "specialized",
      "category": "Interface unifiée de modèles IA",
      "domain": "ai_agents",
      "capabilities": [
        "model-routing",
        "api"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 220,
        "forks": 53,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-03T21:12:50Z"
      },
      "bestFor": [
        "Intégrer plusieurs fournisseurs de modèles derrière une interface"
      ],
      "avoidWhen": [
        "Usage exigeant un modèle exclusivement local"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "lfnovo/open-notebook",
      "score": 8.2,
      "tier": "specialized",
      "category": "Carnet de recherche IA",
      "domain": "productivity",
      "capabilities": [
        "notebook",
        "document-analysis"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 39969,
        "forks": 4628,
        "openIssues": 153,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T02:29:31Z"
      },
      "bestFor": [
        "Organiser des sources et interroger un carnet de recherche IA"
      ],
      "avoidWhen": [
        "Données sensibles sur fournisseur non maîtrisé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Lightricks/LTX-Video",
      "score": 8.2,
      "tier": "specialized",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 11056,
        "forks": 1164,
        "openIssues": 101,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-01-05T22:37:07Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "liquidslr/system-design-notes",
      "score": 7.2,
      "tier": "audit",
      "category": "Documentation d'architecture logicielle",
      "domain": "software_engineering",
      "capabilities": [
        "system-design",
        "documentation"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 24645,
        "forks": 4603,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-08-12T22:22:21Z"
      },
      "bestFor": [
        "Préparer des choix d'architecture et entretiens système"
      ],
      "avoidWhen": [
        "Utiliser une référence théorique comme preuve de performance"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "localsend/localsend",
      "score": 8.2,
      "tier": "specialized",
      "category": "Transfert de fichiers local",
      "domain": "mobile",
      "capabilities": [
        "file-transfer",
        "networking"
      ],
      "languages": [
        "dart"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 93704,
        "forks": 5231,
        "openIssues": 1008,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-07T23:01:53Z"
      },
      "bestFor": [
        "Partager des fichiers entre appareils sur le réseau local"
      ],
      "avoidWhen": [
        "Réseaux non fiables sans contrôle de sécurité"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "LuxAlgo/PineTS",
      "score": 8.2,
      "tier": "specialized",
      "category": "Indicateurs et scripts TradingView",
      "domain": "trading",
      "capabilities": [
        "technical-analysis",
        "indicators"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 848,
        "forks": 193,
        "openIssues": 68,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T22:50:47Z"
      },
      "bestFor": [
        "Analyser les marchés avec des indicateurs techniques"
      ],
      "avoidWhen": [
        "Décisions d'investissement prises sur un indicateur isolé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "regime"
      ]
    },
    {
      "repo": "mastra-ai/mastra",
      "score": 7.2,
      "tier": "audit",
      "category": "Espace de travail d'agents IA",
      "domain": "ai_agents",
      "capabilities": [
        "agents",
        "workspace"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 28649,
        "forks": 2943,
        "openIssues": 566,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T01:27:59Z"
      },
      "bestFor": [
        "Construire des espaces de travail et des flux pour agents IA"
      ],
      "avoidWhen": [
        "Fonctionnement totalement hors ligne sans adaptation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "meituan-longcat/LongCat-Video",
      "score": 7.2,
      "tier": "audit",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 9110,
        "forks": 1585,
        "openIssues": 82,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-27T02:51:41Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "michael-denyer/pstack-claude",
      "score": 8.2,
      "tier": "specialized",
      "category": "Agents de programmation et workflows",
      "domain": "software_engineering",
      "capabilities": [
        "coding-agents",
        "automation"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1652,
        "forks": 176,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T21:45:55Z"
      },
      "bestFor": [
        "Orchestrer des tâches de développement assistées par IA"
      ],
      "avoidWhen": [
        "Intégration sans revue des changements générés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "MISP/MISP",
      "score": 8.2,
      "tier": "specialized",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "php"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 6583,
        "forks": 1646,
        "openIssues": 2947,
        "archived": false,
        "disabled": false,
        "defaultBranch": "2.5",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-07T19:03:27Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "mitmproxy/mitmproxy",
      "score": 8.2,
      "tier": "specialized",
      "category": "Inspection du trafic HTTP",
      "domain": "cybersecurity",
      "capabilities": [
        "proxy",
        "http"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 45349,
        "forks": 4774,
        "openIssues": 490,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-05T22:18:35Z"
      },
      "bestFor": [
        "Diagnostiquer les échanges HTTP(S) dans un périmètre de test"
      ],
      "avoidWhen": [
        "Interception non consentie du trafic"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "mitre-attack/attack-stix-data",
      "score": 7.2,
      "tier": "audit",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 690,
        "forks": 147,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-05T22:57:21Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "modal-labs/modal-examples",
      "score": 8.2,
      "tier": "specialized",
      "category": "Exécution isolée et cloud",
      "domain": "devops",
      "capabilities": [
        "sandbox",
        "serverless"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": "partial",
      "runtime": [
        "cloud"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 1276,
        "forks": 322,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:06:11Z"
      },
      "bestFor": [
        "Exécuter des charges de calcul isolées ou hébergées"
      ],
      "avoidWhen": [
        "Déploiement sans suivi des coûts ni isolation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "morluto/rea",
      "score": 8.2,
      "tier": "specialized",
      "category": "Rétro-ingénierie assistée par IA",
      "domain": "cybersecurity",
      "capabilities": [
        "reverse-engineering",
        "analysis"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 27007,
        "forks": 3066,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:29:24Z"
      },
      "bestFor": [
        "Analyser des logiciels autorisés avec des outils de rétro-ingénierie"
      ],
      "avoidWhen": [
        "Analyse de logiciels tiers hors cadre légal ou contractuel"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "OISF/suricata",
      "score": 8.2,
      "tier": "specialized",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "c"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 6714,
        "forks": 1780,
        "openIssues": 91,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T15:31:08Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "open-rmf/rmf",
      "score": 8.2,
      "tier": "specialized",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 445,
        "forks": 90,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-08-25T01:22:32Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "openai/math",
      "score": 7.2,
      "tier": "audit",
      "category": "Bibliothèque formelle mathématique",
      "domain": "software_engineering",
      "capabilities": [
        "formal-verification",
        "mathematics"
      ],
      "languages": [
        "lean"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 12136,
        "forks": 1263,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T05:20:00Z"
      },
      "bestFor": [
        "Utiliser des preuves formelles et des mathématiques en Lean"
      ],
      "avoidWhen": [
        "Développement sans besoin de vérification formelle"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "OpenByteInc/QuantDinger",
      "score": 8.2,
      "tier": "specialized",
      "category": "Trading algorithmique multi-actifs",
      "domain": "trading",
      "capabilities": [
        "backtesting",
        "execution"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 12566,
        "forks": 2547,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-06T21:14:39Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies de trading automatisées"
      ],
      "avoidWhen": [
        "Exécution réelle sans backtesting et limites de risque"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "OpenCut-app/OpenCut",
      "score": 8.2,
      "tier": "specialized",
      "category": "Montage vidéo et création multimédia",
      "domain": "ai_media",
      "capabilities": [
        "video-editing",
        "rendering"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 93251,
        "forks": 9153,
        "openIssues": 375,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-24T09:24:44Z"
      },
      "bestFor": [
        "Créer et monter des vidéos dans une interface open source"
      ],
      "avoidWhen": [
        "Traitement multimédia sans vérification du rendu final"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "openvla/openvla",
      "score": 8.2,
      "tier": "specialized",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 7124,
        "forks": 854,
        "openIssues": 118,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-03-23T23:41:01Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "stable"
    },
    {
      "repo": "oraios/serena",
      "score": 7.2,
      "tier": "audit",
      "category": "Navigation sémantique du code",
      "domain": "software_engineering",
      "capabilities": [
        "code-search",
        "refactoring"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 30109,
        "forks": 2049,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T22:37:55Z"
      },
      "bestFor": [
        "Naviguer et éditer des projets via des outils sémantiques"
      ],
      "avoidWhen": [
        "Éditions sans tests ou revues de diff"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "osquery/osquery",
      "score": 7.2,
      "tier": "audit",
      "category": "Visibilité endpoint et threat hunting",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-hunting",
        "forensics"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 23629,
        "forks": 2610,
        "openIssues": 591,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T01:06:29Z"
      },
      "bestFor": [
        "Analyser les hôtes et les événements de sécurité"
      ],
      "avoidWhen": [
        "Collecte de télémétrie sans autorisation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "pingdotgg/t3code",
      "score": 7.2,
      "tier": "audit",
      "category": "Agents de programmation et workflows",
      "domain": "software_engineering",
      "capabilities": [
        "coding-agents",
        "automation"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 26414,
        "forks": 6870,
        "openIssues": 2831,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-09T01:31:05Z"
      },
      "bestFor": [
        "Orchestrer des tâches de développement assistées par IA"
      ],
      "avoidWhen": [
        "Intégration sans revue des changements générés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Quincunx33/Ai-jailbreak",
      "score": 7.2,
      "tier": "audit",
      "category": "Évaluation de prompts adversariaux",
      "domain": "cybersecurity",
      "capabilities": [
        "red-team",
        "prompt-testing"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 383,
        "forks": 68,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-10-07T14:59:44Z"
      },
      "bestFor": [
        "Auditer la robustesse des modèles dans un environnement autorisé"
      ],
      "avoidWhen": [
        "Utilisation non encadrée de techniques de contournement"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "rawfilejson/awesome-osint-arsenal",
      "score": 8.2,
      "tier": "specialized",
      "category": "OSINT et reconnaissance autorisée",
      "domain": "cybersecurity",
      "capabilities": [
        "osint",
        "recon"
      ],
      "languages": [
        "shell"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3204,
        "forks": 477,
        "openIssues": 12,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-29T03:14:19Z"
      },
      "bestFor": [
        "Collecter et corréler des données publiques sur un périmètre autorisé"
      ],
      "avoidWhen": [
        "Reconnaissance non autorisée ou non cadrée"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "ray-project/ray",
      "score": 8.2,
      "tier": "specialized",
      "category": "Orchestration des tâches parallèles",
      "domain": "software_engineering",
      "capabilities": [
        "task-scheduling",
        "concurrency"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 43993,
        "forks": 8121,
        "openIssues": 3556,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:23:55Z"
      },
      "bestFor": [
        "Orchestrer des tâches et dépendances de calcul"
      ],
      "avoidWhen": [
        "Applications sans parallélisme à gérer"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "rbrus/laya-as-judge",
      "score": 8.2,
      "tier": "specialized",
      "category": "Évaluation des réponses LLM",
      "domain": "ai_agents",
      "capabilities": [
        "llm-evaluation",
        "testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 17,
        "forks": 1,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-26T08:15:03Z"
      },
      "bestFor": [
        "Construire et comparer des pipelines de jugement par LLM"
      ],
      "avoidWhen": [
        "Substitution des évaluations humaines critiques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "rehan-remade/universal-modder",
      "score": 8.2,
      "tier": "specialized",
      "category": "Modding de jeux par agents IA",
      "domain": "game_dev",
      "capabilities": [
        "game-modding",
        "automation"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 5656,
        "forks": 530,
        "openIssues": 41,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T23:19:15Z"
      },
      "bestFor": [
        "Modifier et tester des contenus de jeu assistés par agent"
      ],
      "avoidWhen": [
        "Jeux sans autorisation de modification"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "reviewdog/reviewdog",
      "score": 8.2,
      "tier": "specialized",
      "category": "Revue automatisée du code",
      "domain": "software_engineering",
      "capabilities": [
        "code-review",
        "lint"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 9649,
        "forks": 503,
        "openIssues": 131,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:26:07Z"
      },
      "bestFor": [
        "Intégrer des vérifications statiques dans les pull requests"
      ],
      "avoidWhen": [
        "Remplacer entièrement les tests fonctionnels par un linter"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "RickdeJager/stegseek",
      "score": 8.2,
      "tier": "specialized",
      "category": "Stéganographie et analyse forensique",
      "domain": "cybersecurity",
      "capabilities": [
        "forensics",
        "steganography"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 1332,
        "forks": 136,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-2.0",
        "pushedAt": "2023-10-10T12:20:59Z"
      },
      "bestFor": [
        "Investiguer des supports et artefacts dans un laboratoire autorisé"
      ],
      "avoidWhen": [
        "Tentatives de récupération non autorisées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "ros2/ros2",
      "score": 7.2,
      "tier": "audit",
      "category": "Robotique et apprentissage robotique",
      "domain": "data_ml",
      "capabilities": [
        "robotics",
        "simulation"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 6136,
        "forks": 963,
        "openIssues": 151,
        "archived": false,
        "disabled": false,
        "defaultBranch": "rolling",
        "license": null,
        "pushedAt": "2026-10-07T13:51:04Z"
      },
      "bestFor": [
        "Simuler et entraîner des systèmes robotiques"
      ],
      "avoidWhen": [
        "Projet sans besoins robotiques ni matériel adapté"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "SigmaHQ/sigma",
      "score": 7.2,
      "tier": "audit",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 11192,
        "forks": 2839,
        "openIssues": 254,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-06T11:26:20Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "SII-WANGZJ/Polymarket_data",
      "score": 8.2,
      "tier": "specialized",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 858,
        "forks": 121,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-01-01T13:17:37Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "smicallef/spiderfoot",
      "score": 8.2,
      "tier": "specialized",
      "category": "OSINT et reconnaissance autorisée",
      "domain": "cybersecurity",
      "capabilities": [
        "osint",
        "recon"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 23193,
        "forks": 3715,
        "openIssues": 329,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-04-13T19:43:06Z"
      },
      "bestFor": [
        "Collecter et corréler des données publiques sur un périmètre autorisé"
      ],
      "avoidWhen": [
        "Reconnaissance non autorisée ou non cadrée"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "storytold/artcraft",
      "score": 7.2,
      "tier": "audit",
      "category": "Création visuelle artistique",
      "domain": "graphics",
      "capabilities": [
        "creative-tools",
        "rendering"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 8048,
        "forks": 1135,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-07T00:56:15Z"
      },
      "bestFor": [
        "Produire des visuels et récits assistés par logiciel"
      ],
      "avoidWhen": [
        "Utilisation sans vérification des droits sur les médias"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Stremio/stremio-web",
      "score": 8.2,
      "tier": "specialized",
      "category": "Interface de lecture multimédia",
      "domain": "ai_media",
      "capabilities": [
        "streaming",
        "web-ui"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 14447,
        "forks": 1643,
        "openIssues": 67,
        "archived": false,
        "disabled": false,
        "defaultBranch": "development",
        "license": "GPL-2.0",
        "pushedAt": "2026-10-08T14:16:34Z"
      },
      "bestFor": [
        "Développer une interface web de lecture multimédia"
      ],
      "avoidWhen": [
        "Usage sans respect des droits sur les contenus"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "taskflow/taskflow",
      "score": 7.2,
      "tier": "audit",
      "category": "Orchestration des tâches parallèles",
      "domain": "software_engineering",
      "capabilities": [
        "task-scheduling",
        "concurrency"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 12198,
        "forks": 1413,
        "openIssues": 41,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-28T18:41:31Z"
      },
      "bestFor": [
        "Orchestrer des tâches et dépendances de calcul"
      ],
      "avoidWhen": [
        "Applications sans parallélisme à gérer"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "tester-army/e2e",
      "score": 8.2,
      "tier": "specialized",
      "category": "Tests end-to-end",
      "domain": "software_engineering",
      "capabilities": [
        "testing",
        "e2e"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 8182,
        "forks": 383,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T22:06:20Z"
      },
      "bestFor": [
        "Automatiser les tests fonctionnels des applications web et mobiles"
      ],
      "avoidWhen": [
        "Utilisation comme substitut à des tests d'intégration ciblés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "topoteretes/cognee",
      "score": 8.2,
      "tier": "specialized",
      "category": "Mémoire pour agents IA",
      "domain": "ai_memory",
      "capabilities": [
        "agent-memory",
        "knowledge-graph"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 31763,
        "forks": 3275,
        "openIssues": 569,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T01:22:39Z"
      },
      "bestFor": [
        "Maintenir un contexte et une mémoire exploitable pour agents IA"
      ],
      "avoidWhen": [
        "Traitement de données confidentielles sans contrôle d'accès"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "trufflesecurity/trufflehog",
      "score": 8.2,
      "tier": "specialized",
      "category": "Détection des secrets",
      "domain": "cybersecurity",
      "capabilities": [
        "secret-scanning",
        "security"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 28369,
        "forks": 2623,
        "openIssues": 560,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-10-08T17:28:48Z"
      },
      "bestFor": [
        "Détecter des identifiants exposés dans des dépôts et journaux"
      ],
      "avoidWhen": [
        "Scan de ressources dont l'accès n'est pas autorisé"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "undefined-ui/second-brain-os",
      "score": 8.2,
      "tier": "specialized",
      "category": "Système de travail piloté par agents",
      "domain": "ai_agents",
      "capabilities": [
        "agents",
        "workflow"
      ],
      "languages": [
        "html"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 1017,
        "forks": 163,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-07T19:16:09Z"
      },
      "bestFor": [
        "Organiser un environnement de travail orienté agents"
      ],
      "avoidWhen": [
        "Confiance implicite dans les actions d'agents non supervisés"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Unstructured-IO/unstructured",
      "score": 8.2,
      "tier": "specialized",
      "category": "Extraction et structuration de documents",
      "domain": "data_ml",
      "capabilities": [
        "document-processing",
        "extraction"
      ],
      "languages": [
        "html"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 15549,
        "forks": 1351,
        "openIssues": 336,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T00:03:37Z"
      },
      "bestFor": [
        "Extraire le contenu de documents pour la recherche et l'IA"
      ],
      "avoidWhen": [
        "Documents sensibles sans contrôles de confidentialité"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Velocidex/velociraptor",
      "score": 7.2,
      "tier": "audit",
      "category": "Visibilité endpoint et threat hunting",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-hunting",
        "forensics"
      ],
      "languages": [
        "go"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 4312,
        "forks": 661,
        "openIssues": 77,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-07T11:34:46Z"
      },
      "bestFor": [
        "Analyser les hôtes et les événements de sécurité"
      ],
      "avoidWhen": [
        "Collecte de télémétrie sans autorisation"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "VirusTotal/yara",
      "score": 8.2,
      "tier": "specialized",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "c"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 9931,
        "forks": 1586,
        "openIssues": 169,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-23T09:48:49Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Wan-Video/Wan2.1",
      "score": 8.2,
      "tier": "specialized",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 17122,
        "forks": 3727,
        "openIssues": 386,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-03-05T09:38:07Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "XHToken/Spark-X2.5",
      "score": 8.2,
      "tier": "specialized",
      "category": "Modèle d'IA local",
      "domain": "data_ml",
      "capabilities": [
        "on-device",
        "model-inference"
      ],
      "languages": [],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 682,
        "forks": 87,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T08:13:26Z"
      },
      "bestFor": [
        "Évaluer les capacités de modèles exécutés sur l'appareil"
      ],
      "avoidWhen": [
        "Appareils sans mémoire ou puissance suffisante"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "yangyuan-zhen/PolyWeather",
      "score": 8.2,
      "tier": "specialized",
      "category": "Marchés prédictifs et Polymarket",
      "domain": "trading",
      "capabilities": [
        "prediction-markets",
        "backtesting"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 316,
        "forks": 73,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T17:25:12Z"
      },
      "bestFor": [
        "Étudier et tester des stratégies pour les marchés prédictifs"
      ],
      "avoidWhen": [
        "Exécution réelle sans validation des risques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active",
      "roles": [
        "alpha",
        "backtest",
        "risk",
        "execution"
      ]
    },
    {
      "repo": "zai-org/CogVideo",
      "score": 8.2,
      "tier": "specialized",
      "category": "Génération vidéo par IA",
      "domain": "ai_media",
      "capabilities": [
        "video-generation",
        "diffusion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 13067,
        "forks": 1365,
        "openIssues": 115,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-11-04T11:19:04Z"
      },
      "bestFor": [
        "Expérimenter la génération et l'animation vidéo par IA"
      ],
      "avoidWhen": [
        "Exécution sur matériel à ressources limitées"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "zeek/zeek",
      "score": 7.2,
      "tier": "audit",
      "category": "Threat intelligence et détection",
      "domain": "cybersecurity",
      "capabilities": [
        "threat-intelligence",
        "detection"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 8084,
        "forks": 1433,
        "openIssues": 260,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T21:42:41Z"
      },
      "bestFor": [
        "Corréler des indicateurs de compromission et détecter des menaces"
      ],
      "avoidWhen": [
        "Déploiement de règles non validées en production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "airbytehq/airbyte",
      "score": 7.8,
      "tier": "audit",
      "category": "Synchronisation de sources de données",
      "domain": "data_ml",
      "capabilities": [
        "elt",
        "connectors",
        "data-ingestion"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "server"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "mixed",
      "github": {
        "stars": 22194,
        "forks": 5393,
        "openIssues": 2583,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:29:22Z"
      },
      "bestFor": [
        "Synchroniser des bases, fichiers et API vers des entrepôts et outils IA"
      ],
      "avoidWhen": [
        "Supposer que toutes les fonctionnalités et licences Cloud sont ouvertes"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "apache/datafusion",
      "score": 8.6,
      "tier": "specialized",
      "category": "Moteur SQL analytique embarquable",
      "domain": "data_ml",
      "capabilities": [
        "sql",
        "query-engine",
        "rust"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 9417,
        "forks": 2482,
        "openIssues": 2374,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T02:59:07Z"
      },
      "bestFor": [
        "Intégrer un moteur de requêtes analytiques rapide en Rust"
      ],
      "avoidWhen": [
        "Rechercher une interface graphique de BI prête à utiliser"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "apache/superset",
      "score": 8.6,
      "tier": "specialized",
      "category": "Exploration et visualisation SQL",
      "domain": "data_ml",
      "capabilities": [
        "dashboards",
        "sql",
        "data-visualization"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "server"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 75082,
        "forks": 18439,
        "openIssues": 568,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:19:45Z"
      },
      "bestFor": [
        "Créer des graphiques, rapports et tableaux de bord sur des sources SQL"
      ],
      "avoidWhen": [
        "Besoin d'une bibliothèque embarquée légère côté navigateur uniquement"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Dataherald/dataherald",
      "score": 7.5,
      "tier": "audit",
      "category": "Génération de requêtes SQL par IA",
      "domain": "data_ml",
      "capabilities": [
        "nl-to-sql",
        "llm",
        "sql"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 3649,
        "forks": 263,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-07-24T17:37:41Z"
      },
      "bestFor": [
        "Expérimenter l'interrogation de bases SQL par langage naturel"
      ],
      "avoidWhen": [
        "Production sans audit de sécurité SQL ni contrôle de maintenance"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "defog-ai/sqlcoder",
      "score": 7.4,
      "tier": "audit",
      "category": "Modèle de génération SQL",
      "domain": "data_ml",
      "capabilities": [
        "nl-to-sql",
        "llm",
        "text-to-sql"
      ],
      "languages": [
        "jupyter notebook"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 4049,
        "forks": 272,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-05-23T03:06:26Z"
      },
      "bestFor": [
        "Évaluer des modèles de génération de SQL depuis le langage naturel"
      ],
      "avoidWhen": [
        "Déployer des requêtes générées sur une base réelle sans revue ni garde-fous"
      ],
      "guidanceSource": "curated",
      "lifecycle": "reference"
    },
    {
      "repo": "dlt-hub/dlt",
      "score": 8.5,
      "tier": "specialized",
      "category": "Ingestion de données Python",
      "domain": "data_ml",
      "capabilities": [
        "elt",
        "data-ingestion",
        "pipelines"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 5945,
        "forks": 618,
        "openIssues": 454,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T16:24:37Z"
      },
      "bestFor": [
        "Charger et normaliser des données API ou fichiers dans un entrepôt"
      ],
      "avoidWhen": [
        "Orchestration complexe non couverte sans outil complémentaire"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "duckdb/duckdb",
      "score": 8.8,
      "tier": "specialized",
      "category": "Base SQL analytique embarquée",
      "domain": "data_ml",
      "capabilities": [
        "database",
        "sql",
        "analytics"
      ],
      "languages": [
        "c++"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 41995,
        "forks": 3887,
        "openIssues": 1066,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v2.0-cyanoptera",
        "license": "MIT",
        "pushedAt": "2026-10-09T00:00:14Z"
      },
      "bestFor": [
        "Exécuter des analyses SQL locales et sur des fichiers Parquet ou CSV"
      ],
      "avoidWhen": [
        "Héberger une base OLTP multi-utilisateurs avec beaucoup d'écritures concurrentes"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "eosphoros-ai/DB-GPT",
      "score": 8.3,
      "tier": "specialized",
      "category": "Assistant IA pour bases de données",
      "domain": "data_ml",
      "capabilities": [
        "database",
        "llm",
        "nl-to-sql",
        "agents"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 20093,
        "forks": 2958,
        "openIssues": 450,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-04T13:43:25Z"
      },
      "bestFor": [
        "Construire un assistant de données capable de raisonner et interroger des bases SQL"
      ],
      "avoidWhen": [
        "Permettre à un LLM d'exécuter des requêtes non contrôlées sur une base de production"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "evidence-dev/evidence",
      "score": 8.4,
      "tier": "specialized",
      "category": "BI as code",
      "domain": "data_ml",
      "capabilities": [
        "business-intelligence",
        "dashboards",
        "sql",
        "markdown"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 6989,
        "forks": 428,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T19:49:20Z"
      },
      "bestFor": [
        "Construire des tableaux de bord versionnés à partir de SQL et Markdown"
      ],
      "avoidWhen": [
        "Exiger une interface BI entièrement sans code"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "fivetran/great_expectations",
      "score": 8.5,
      "tier": "specialized",
      "category": "Tests de qualité des données",
      "domain": "data_ml",
      "capabilities": [
        "data-quality",
        "validation",
        "testing"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 11867,
        "forks": 1871,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-08T09:28:46Z"
      },
      "bestFor": [
        "Définir et exécuter des assertions sur les jeux de données et les pipelines"
      ],
      "avoidWhen": [
        "Substituer des assertions aux validations métier ou statistiques"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Jakeschincariol/arena-skill",
      "score": 8,
      "tier": "specialized",
      "category": "Évaluation comparative d'agents IA",
      "domain": "ai_agents",
      "capabilities": [
        "agent-evaluation",
        "planning",
        "benchmarking"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": "partial",
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 374,
        "forks": 52,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-27T13:20:07Z"
      },
      "bestFor": [
        "Comparer plusieurs stratégies de résolution par agents sur une même tâche"
      ],
      "avoidWhen": [
        "Consommer des appels LLM coûteux sans budget et critères de jugement"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "Kanaries/pygwalker",
      "score": 8.4,
      "tier": "specialized",
      "category": "Visualisation interactive de DataFrames",
      "domain": "data_ml",
      "capabilities": [
        "data-visualization",
        "dataframes",
        "exploration"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 15979,
        "forks": 890,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-05T19:19:19Z"
      },
      "bestFor": [
        "Explorer visuellement des tableaux Python dans une interface interactive"
      ],
      "avoidWhen": [
        "Recherche exclusive de visualisations statiques pour un pipeline headless"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "metabase/metabase",
      "score": 7.7,
      "tier": "audit",
      "category": "BI et tableaux de bord",
      "domain": "data_ml",
      "capabilities": [
        "business-intelligence",
        "dashboards",
        "sql"
      ],
      "languages": [
        "clojure"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "server"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "mixed",
      "github": {
        "stars": 49584,
        "forks": 6889,
        "openIssues": 4560,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-09T02:34:57Z"
      },
      "bestFor": [
        "Mettre à disposition des tableaux de bord métier et des analyses SQL"
      ],
      "avoidWhen": [
        "Réutiliser le code sans examiner les licences communautaires et commerciales"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "open-metadata/OpenMetadata",
      "score": 8.6,
      "tier": "specialized",
      "category": "Catalogue et gouvernance de données",
      "domain": "data_ml",
      "capabilities": [
        "data-catalog",
        "governance",
        "metadata"
      ],
      "languages": [
        "typescript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "server"
      ],
      "resourceLevel": "high",
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 15420,
        "forks": 2436,
        "openIssues": 957,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-10-09T03:07:08Z"
      },
      "bestFor": [
        "Inventorier les actifs de données, lignages et règles de gouvernance"
      ],
      "avoidWhen": [
        "Déploiement d'une plateforme lourde pour quelques fichiers locaux"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "pola-rs/polars",
      "score": 8.8,
      "tier": "specialized",
      "category": "Analyse de DataFrames hautes performances",
      "domain": "data_ml",
      "capabilities": [
        "dataframes",
        "sql",
        "performance"
      ],
      "languages": [
        "rust"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 40021,
        "forks": 3158,
        "openIssues": 2956,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-10-08T14:41:35Z"
      },
      "bestFor": [
        "Transformer et analyser des tables volumineuses avec un moteur DataFrame rapide"
      ],
      "avoidWhen": [
        "Avoir besoin uniquement de requêtes SQL simples sans traitement tabulaire"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "quarto-dev/quarto-cli",
      "score": 7.8,
      "tier": "audit",
      "category": "Publication scientifique reproductible",
      "domain": "productivity",
      "capabilities": [
        "documentation",
        "publishing",
        "markdown"
      ],
      "languages": [
        "javascript"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 6065,
        "forks": 464,
        "openIssues": 1896,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T16:35:35Z"
      },
      "bestFor": [
        "Publier des rapports techniques, notebooks et documents reproductibles"
      ],
      "avoidWhen": [
        "Réutiliser des composants sans vérification de leur licence exacte"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "sinaptik-ai/pandas-ai",
      "score": 7.5,
      "tier": "audit",
      "category": "Analyse de données en langage naturel",
      "domain": "data_ml",
      "capabilities": [
        "nl-to-sql",
        "llm",
        "dataframes"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": "partial",
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 23860,
        "forks": 2342,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2025-10-28T10:02:13Z"
      },
      "bestFor": [
        "Explorer des données SQL, CSV ou Parquet avec des requêtes conversationnelles"
      ],
      "avoidWhen": [
        "Fournir un accès non contrôlé à des données personnelles ou confidentielles"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "sodadata/soda-core",
      "score": 7.6,
      "tier": "audit",
      "category": "Contrats et qualité des données",
      "domain": "data_ml",
      "capabilities": [
        "data-quality",
        "validation",
        "data-contracts"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "unknown",
      "github": {
        "stars": 2435,
        "forks": 288,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-10-08T20:50:19Z"
      },
      "bestFor": [
        "Contrôler la qualité des données et les contrats des pipelines"
      ],
      "avoidWhen": [
        "Réutiliser des composants sous licence incertaine sans vérification"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    },
    {
      "repo": "yifanfeng97/Hyper-Extract",
      "score": 7.4,
      "tier": "audit",
      "category": "Extraction de connaissances structurées",
      "domain": "data_ml",
      "capabilities": [
        "knowledge-extraction",
        "llm",
        "knowledge-graph"
      ],
      "languages": [
        "python"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": true,
      "runtime": [
        "local"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "high",
      "costModel": "unknown",
      "github": {
        "stars": 4142,
        "forks": 473,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-29T13:33:32Z"
      },
      "bestFor": [
        "Transformer des documents non structurés en graphes et hypergraphes de connaissances"
      ],
      "avoidWhen": [
        "Traitement de documents sensibles sans isoler les services d'inférence"
      ],
      "guidanceSource": "curated",
      "lifecycle": "active"
    }
  ],
  "metadata": {
    "githubRefreshedAt": "2026-10-05T11:27:17.097321Z",
    "githubRefreshFailures": []
  }
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
              "audit"
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

## File: discovery-memory.json
````json
{
  "schemaVersion": 1,
  "candidates": {
    "obsproject/obs-studio": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 76988,
        "pushedAt": "2026-10-04T01:39:14Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "bradtraversy/design-resources-for-developers": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 66947,
        "pushedAt": "2026-05-24T10:07:48Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "hesreallyhim/awesome-claude-code": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 54130,
        "pushedAt": "2026-09-16T03:11:54Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "Genesis-Embodied-AI/genesis-world": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 30022,
        "pushedAt": "2026-10-05T09:45:19Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "dipakkr/A-to-Z-Resources-for-Students": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 22260,
        "pushedAt": "2026-06-17T14:00:26Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "Unity-Technologies/ml-agents": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 19719,
        "pushedAt": "2026-09-29T13:32:59Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "Robbyant/lingbot-map": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 17220,
        "pushedAt": "2026-09-08T06:31:41Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "PavelDoGreat/WebGL-Fluid-Simulation": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16690,
        "pushedAt": "2024-11-12T13:29:23Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "OpenRCT2/OpenRCT2": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16323,
        "pushedAt": "2026-10-05T04:10:59Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "budtmo/docker-android": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 15937,
        "pushedAt": "2026-10-02T11:20:25Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "public-api-lists/public-api-lists": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 15826,
        "pushedAt": "2026-09-14T07:19:57Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "bulletphysics/bullet3": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 14764,
        "pushedAt": "2025-10-22T02:13:14Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "ytisf/theZoo": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 13440,
        "pushedAt": "2026-09-14T06:47:21Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "alicevision/Meshroom": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 12992,
        "pushedAt": "2026-10-05T10:10:20Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "jrouwe/JoltPhysics": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11662,
        "pushedAt": "2026-10-04T20:43:44Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "horsicq/Detect-It-Easy": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11629,
        "pushedAt": "2026-10-04T18:29:07Z",
        "targets": [
          [
            "capability",
            "binary-analysis"
          ],
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "OffcierCia/DeFi-Developer-Road-Map": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 10831,
        "pushedAt": "2026-08-16T23:17:39Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "o3de/o3de": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 9727,
        "pushedAt": "2026-10-02T18:49:18Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "VAST-AI-Research/TripoSR": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 7013,
        "pushedAt": "2026-06-04T07:11:09Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "openMVG/openMVG": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6564,
        "pushedAt": "2026-08-30T17:24:15Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "cnr-isti-vclab/meshlab": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5849,
        "pushedAt": "2026-08-25T20:38:52Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "ArthurBrussee/brush": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5135,
        "pushedAt": "2026-10-03T14:48:28Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "testcontainers/testcontainers-go": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 4978,
        "pushedAt": "2026-09-10T07:56:21Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "miroslavpejic85/mirotalk": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 4764,
        "pushedAt": "2026-10-05T10:43:52Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "royshil/obs-backgroundremoval": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 4546,
        "pushedAt": "2026-09-10T07:54:29Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "ihmily/StreamCap": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 4261,
        "pushedAt": "2026-09-01T23:06:47Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "kevoreilly/CAPEv2": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 3551,
        "pushedAt": "2026-10-03T15:03:30Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "vladmandic/human": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 3300,
        "pushedAt": "2025-12-13T09:49:12Z",
        "targets": [
          [
            "capability",
            "3d-human"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "anonfaded/FadCam": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 2772,
        "pushedAt": "2026-09-15T15:57:19Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "taojy123/KeymouseGo": {
      "fingerprint": {
        "decision": "accept",
        "score": 97.9,
        "stars": 10602,
        "pushedAt": "2026-06-07T08:09:08Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "NVlabs/instant-ngp": {
      "fingerprint": {
        "decision": "accept",
        "score": 97.7,
        "stars": 17568,
        "pushedAt": "2026-02-02T12:32:34Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "rednaga/APKiD": {
      "fingerprint": {
        "decision": "accept",
        "score": 97.5,
        "stars": 2574,
        "pushedAt": "2026-09-02T18:55:19Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "vxunderground/MalwareSourceCode": {
      "fingerprint": {
        "decision": "accept",
        "score": 96.9,
        "stars": 18756,
        "pushedAt": "2026-05-30T07:11:00Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-28T10:54:14.739184Z"
    },
    "pedramamini/awesome-yara": {
      "fingerprint": {
        "decision": "accept",
        "score": 93.4,
        "stars": 4283,
        "pushedAt": "2026-06-15T19:57:31Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "nuysoft/Mock": {
      "fingerprint": {
        "decision": "accept",
        "score": 88.4,
        "stars": 19571,
        "pushedAt": "2024-03-15T01:53:57Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "cporter202/API-mega-list": {
      "fingerprint": {
        "decision": "accept",
        "score": 88.3,
        "stars": 7624,
        "pushedAt": "2026-07-23T19:20:07Z",
        "targets": [
          [
            "capability",
            "api-directory"
          ],
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "rshipp/awesome-malware-analysis": {
      "fingerprint": {
        "decision": "accept",
        "score": 87.7,
        "stars": 14250,
        "pushedAt": "2024-06-07T05:09:47Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "yfeng95/PRNet": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.6,
        "stars": 5018,
        "pushedAt": "2022-07-25T23:50:26Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "thebuggeddev/anatomy": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.6,
        "stars": 3277,
        "pushedAt": "2026-08-09T12:36:20Z",
        "targets": [
          [
            "capability",
            "3d-human"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "nerfstudio-project/nerfstudio": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.6,
        "stars": 12043,
        "pushedAt": "2025-07-29T02:30:55Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "mezod/awesome-indie": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.1,
        "stars": 11790,
        "pushedAt": "2024-06-12T21:23:53Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "muaz-khan/RecordRTC": {
      "fingerprint": {
        "decision": "accept",
        "score": 83.4,
        "stars": 6921,
        "pushedAt": "2024-05-13T00:39:07Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "engineerapart/TheRemoteFreelancer": {
      "fingerprint": {
        "decision": "accept",
        "score": 83.3,
        "stars": 7576,
        "pushedAt": "2024-09-09T16:24:35Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "fudan-generative-vision/champ": {
      "fingerprint": {
        "decision": "accept",
        "score": 83.2,
        "stars": 4265,
        "pushedAt": "2024-07-10T07:53:06Z",
        "targets": [
          [
            "capability",
            "3d-human"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "mortenjust/androidtool-mac": {
      "fingerprint": {
        "decision": "accept",
        "score": 81.9,
        "stars": 5413,
        "pushedAt": "2023-03-16T03:28:28Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "dypsilon/frontend-dev-bookmarks": {
      "fingerprint": {
        "decision": "review",
        "score": 73.5,
        "stars": 47515,
        "pushedAt": "2024-05-21T10:56:58Z",
        "targets": [
          [
            "capability",
            "developer-resources"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "ange-yaghi/engine-sim": {
      "fingerprint": {
        "decision": "review",
        "score": 73.0,
        "stars": 9572,
        "pushedAt": "2024-06-17T11:35:26Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "CalebFenton/simplify": {
      "fingerprint": {
        "decision": "review",
        "score": 71.2,
        "stars": 4668,
        "pushedAt": "2022-04-30T12:20:33Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "timzhang642/3D-Machine-Learning": {
      "fingerprint": {
        "decision": "review",
        "score": 70.3,
        "stars": 10203,
        "pushedAt": "2024-07-04T19:13:09Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "bee-san/pyWhat": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 7321,
        "pushedAt": "2026-10-05T09:39:08Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "donnemartin/system-design-primer": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 373222,
        "pushedAt": "2026-09-15T01:10:09Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "clash-verge-rev/clash-verge-rev": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 149304,
        "pushedAt": "2026-10-05T06:19:33Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "nextlevelbuilder/ui-ux-pro-max-skill": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 133141,
        "pushedAt": "2026-10-03T16:05:26Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "rustdesk/rustdesk": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 125161,
        "pushedAt": "2026-10-05T10:54:20Z",
        "targets": [
          [
            "capability",
            "android"
          ],
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "VoltAgent/awesome-design-md": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 119612,
        "pushedAt": "2026-10-05T07:34:34Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "ant-design/ant-design": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 99683,
        "pushedAt": "2026-10-05T07:17:17Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "nexu-io/open-design": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 99487,
        "pushedAt": "2026-10-05T01:37:31Z",
        "targets": [
          [
            "capability",
            "cli"
          ],
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "iluwatar/java-design-patterns": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 94757,
        "pushedAt": "2026-10-04T18:45:15Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "ByteByteGoHq/system-design-101": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 89502,
        "pushedAt": "2025-04-04T17:30:30Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-21T09:56:15.822202Z"
    },
    "GraphiteEditor/Graphite": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 27433,
        "pushedAt": "2026-10-04T08:47:04Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "rawgraphs/rawgraphs-app": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 9033,
        "pushedAt": "2026-08-24T11:02:18Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "visioncortex/vtracer": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 7207,
        "pushedAt": "2026-10-02T12:34:01Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "ecomfe/zrender": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6308,
        "pushedAt": "2026-09-06T14:41:51Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "PixiEditor/PixiEditor": {
      "fingerprint": {
        "decision": "accept",
        "score": 98.9,
        "stars": 8088,
        "pushedAt": "2026-10-02T16:54:35Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "mbrlabs/Lorien": {
      "fingerprint": {
        "decision": "review",
        "score": 75.4,
        "stars": 6834,
        "pushedAt": "2025-09-22T21:29:46Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "exyte/Macaw": {
      "fingerprint": {
        "decision": "accept",
        "score": 81.2,
        "stars": 6048,
        "pushedAt": "2024-02-07T13:37:26Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    },
    "Leonxlnx/taste-skill": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 92702,
        "pushedAt": "2026-09-26T09:01:50Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-10-05T11:28:25.552928Z"
    }
  }
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

Automated discovery is advisory. It can find, score, remember, and surface candidates, but it does **not** edit `catalog.json` to add a repository. Human review remains the admission boundary.
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
        "OpenBB-finance/OpenBB",
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
