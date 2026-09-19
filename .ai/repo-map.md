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
    refresh-metadata.yml
    semantic-refresh.yml
    validate.yml
.serena/
  project.yml
schemas/
  cache-health-history.schema.json
  cache-health-trend.schema.json
  cache-health.schema.json
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
  build_discovery_watchlist.py
  catalog_stats.py
  detect_health_drift.py
  discover_candidates.py
  evaluate_candidates.py
  filter_discovery_memory.py
  find_replacements.py
  health_score.py
  recommend.py
  refresh_github_metadata.py
  render_discovery_issue.py
  render_health_issue.py
  test_analyze_coverage.py
  test_cache_health_history.py
  test_cache_health.py
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
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
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
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Compile Python utilities
        run: python -m compileall -q scripts
      - name: Validate catalog
        run: python scripts/validate_catalog.py
      - name: Test GitHub metadata refresh resilience
        run: python scripts/test_refresh_github_metadata.py
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
def save_cache(path, cache)
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
now=time.time() if now is None else now
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
s = 34*cap_match + 22*domain_match + 18*lexical + 12*best_match + 10*quality + 4*max(0.0, tier)
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
def main()
⋮----
ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
⋮----
args = ap.parse_args()
⋮----
qtokens = tokens(args.query)
domains = set(args.domain) or infer_domains(qtokens)
⋮----
ranked = []
filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}
⋮----
gh = r.get("github", {})
⋮----
s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
⋮----
top = []
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
FIELDS = {
⋮----
def fetch(repo, token=None, retries=2)
⋮----
headers = {"Accept":"application/vnd.github+json","User-Agent":"star-list-metadata-refresh","X-GitHub-Api-Version":"2022-11-28"}
⋮----
req = Request(API.format(repo), headers=headers)
⋮----
def metadata(raw)
⋮----
out = {}
⋮----
lic = raw.get("license")
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
fresh = metadata(fetch(name, token))
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
spec = importlib.util.spec_from_file_location("recommend", SCRIPT)
mod = importlib.util.module_from_spec(spec)
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
def validate(value, schema, path="$")
⋮----
errors=[]
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
version: 17
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
    }
  ]
}
````

## File: catalog.json
````json
{
  "schemaVersion": 1,
  "generatedFrom": "text/star-list.md",
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
        "stars": 82513,
        "forks": 15892,
        "openIssues": 950,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T05:57:17Z"
      }
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
        "stars": 124075,
        "forks": 19199,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T06:02:37Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 74798,
        "forks": 9164,
        "openIssues": 1154,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T08:09:48Z"
      }
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
        "stars": 23010,
        "forks": 2161,
        "openIssues": 243,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-16T05:40:32Z"
      }
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
        "stars": 13496,
        "forks": 2388,
        "openIssues": 1149,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:06:28Z"
      }
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
        "stars": 88073,
        "forks": 11557,
        "openIssues": 812,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:22:18Z"
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
        "stars": 43931,
        "forks": 4260,
        "openIssues": 71,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-07T19:17:46Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 181100,
        "forks": 17896,
        "openIssues": 4013,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T00:37:09Z"
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
        "stars": 37351,
        "forks": 2483,
        "openIssues": 150,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-08-02T01:55:40Z"
      }
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
        "stars": 90368,
        "forks": 11639,
        "openIssues": 536,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-03T01:42:26Z"
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
        "stars": 114753,
        "forks": 12620,
        "openIssues": 427,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T22:49:04Z"
      }
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
        "stars": 23123,
        "forks": 1671,
        "openIssues": 248,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-15T18:04:54Z"
      }
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
        "stars": 263017,
        "forks": 22184,
        "openIssues": 498,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T14:29:06Z"
      }
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
        "stars": 139603,
        "forks": 7502,
        "openIssues": 272,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T14:34:56Z"
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
        "stars": 259489,
        "forks": 38817,
        "openIssues": 211,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T19:33:00Z"
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
        "stars": 37185,
        "forks": 5865,
        "openIssues": 262,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:28:10Z"
      }
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
        "stars": 66699,
        "forks": 9362,
        "openIssues": 709,
        "archived": false,
        "disabled": false,
        "defaultBranch": "release/v3.8.51",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:55:43Z"
      }
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
        "stars": 287279,
        "forks": 25689,
        "openIssues": 367,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T18:42:08Z"
      }
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
        "stars": 46416,
        "forks": 2697,
        "openIssues": 66,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T20:56:47Z"
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
        "stars": 31519,
        "forks": 3523,
        "openIssues": 84,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-05T16:11:52Z"
      }
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
        "stars": 225728,
        "forks": 26886,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T04:51:11Z"
      }
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
        "stars": 152664,
        "forks": 24609,
        "openIssues": 146,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-12T16:57:21Z"
      }
    },
    {
      "repo": "Alisharvr1/free-claude-code",
      "score": 8.2,
      "tier": "specialized",
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
      "costModel": "open-source"
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
        "stars": 42657,
        "forks": 2858,
        "openIssues": 712,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:39:24Z"
      }
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
        "stars": 195250,
        "forks": 108528,
        "openIssues": 45,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-16T06:18:45Z"
      }
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
        "stars": 73672,
        "forks": 11321,
        "openIssues": 140,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-16T03:31:58Z"
      }
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
        "stars": 95063,
        "forks": 16196,
        "openIssues": 2131,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T23:17:39Z"
      }
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
        "stars": 138376,
        "forks": 20322,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T04:08:39Z"
      }
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
        "stars": 23965,
        "forks": 2972,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T17:54:19Z"
      }
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
        "stars": 19598,
        "forks": 2206,
        "openIssues": 270,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-25T06:42:02Z"
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
        "stars": 2934,
        "forks": 523,
        "openIssues": 243,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:49:56Z"
      }
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
        "stars": 6956,
        "forks": 465,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:16:20Z"
      }
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
        "stars": 37609,
        "forks": 2900,
        "openIssues": 743,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-16T05:59:49Z"
      }
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
        "stars": 207728,
        "forks": 27267,
        "openIssues": 5762,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:51:50Z"
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
        "stars": 72570,
        "forks": 8592,
        "openIssues": 965,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T04:22:59Z"
      }
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
        "stars": 245946,
        "forks": 51328,
        "openIssues": 43248,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:47:06Z"
      }
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
        "stars": 52080,
        "forks": 3812,
        "openIssues": 104,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T04:14:52Z"
      }
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
        "stars": 50472,
        "forks": 4606,
        "openIssues": 153,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:57:56Z"
      }
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
        "stars": 43953,
        "forks": 9037,
        "openIssues": 744,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:59:01Z"
      }
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
        "stars": 170441,
        "forks": 21918,
        "openIssues": 79,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-09T10:27:05Z"
      }
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
        "stars": 48983,
        "forks": 4951,
        "openIssues": 1869,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-05-22T14:02:20Z"
      }
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
        "stars": 15638,
        "forks": 1175,
        "openIssues": 62,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2025-10-03T21:49:58Z"
      }
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
        "stars": 41729,
        "forks": 7053,
        "openIssues": 790,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:04:25Z"
      }
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
        "stars": 61004,
        "forks": 9218,
        "openIssues": 1071,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-04-15T11:59:09Z"
      }
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
        "stars": 58633,
        "forks": 8471,
        "openIssues": 810,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T06:01:08Z"
      }
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
        "stars": 21548,
        "forks": 4012,
        "openIssues": 493,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:51:05Z"
      }
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
        "stars": 17726,
        "forks": 2080,
        "openIssues": 483,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T14:31:55Z"
      }
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
        "unknown"
      ],
      "platforms": [
        "cross-platform"
      ],
      "selfHosted": "partial",
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 480687,
        "forks": 53052,
        "openIssues": 1944,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T12:21:13Z"
      }
    },
    {
      "repo": "lisys93/web-check",
      "score": 8.8,
      "tier": "specialized",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
      "capabilities": [
        "web-diagnostics",
        "osint"
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
      "costModel": "open-source"
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
        "stars": 244031,
        "forks": 14338,
        "openIssues": 170,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-11-19T14:00:38Z"
      }
    },
    {
      "repo": "bnmf/tron",
      "score": 7.7,
      "tier": "audit",
      "category": "Automatisation / outils / données",
      "domain": "productivity",
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
      "costModel": "open-source"
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
        "stars": 29525,
        "forks": 1150,
        "openIssues": 194,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "GPL-3.0",
        "pushedAt": "2026-07-29T18:18:23Z"
      }
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
        "stars": 876,
        "forks": 165,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-14T22:15:44Z"
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
        "stars": 911,
        "forks": 288,
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
        "stars": 455537,
        "forks": 46361,
        "openIssues": 210,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T10:49:35Z"
      }
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
        "stars": 7086,
        "forks": 405,
        "openIssues": 23,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:31:58Z"
      }
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
        "stars": 33207,
        "forks": 5385,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:11:23Z"
      }
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
        "stars": 40294,
        "forks": 2565,
        "openIssues": 40,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T20:39:25Z"
      }
    },
    {
      "repo": "sdmg15/Best-websites-a-programmer-should-visit",
      "score": 8.3,
      "tier": "specialized",
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
        "stars": 76258,
        "forks": 8581,
        "openIssues": 1002,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2025-09-16T18:34:24Z"
      }
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
        "unknown"
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
        "stars": 62666,
        "forks": 3672,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T15:32:31Z"
      }
    },
    {
      "repo": "harry2141985/Google-Colab-Notebooks",
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
      "costModel": "open-source"
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
        "stars": 24296,
        "forks": 1685,
        "openIssues": 375,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T01:19:21Z"
      }
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
        "stars": 34585,
        "forks": 2677,
        "openIssues": 723,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T02:18:25Z"
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
        "stars": 29316,
        "forks": 2513,
        "openIssues": 859,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T23:39:38Z"
      }
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
        "stars": 46123,
        "forks": 4253,
        "openIssues": 1419,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:43:36Z"
      }
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
        "stars": 26518,
        "forks": 3144,
        "openIssues": 151,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:55:08Z"
      }
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
        "stars": 27446,
        "forks": 4149,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T15:34:06Z"
      }
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
        "stars": 22437,
        "forks": 2645,
        "openIssues": 189,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-2-Clause",
        "pushedAt": "2025-10-20T13:17:06Z"
      }
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
        "stars": 66250,
        "forks": 10028,
        "openIssues": 399,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T14:31:12Z"
      }
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
        "stars": 9240,
        "forks": 1038,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T21:19:20Z"
      }
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
        "stars": 29011,
        "forks": 9253,
        "openIssues": 1127,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T23:03:40Z"
      }
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
        "stars": 25910,
        "forks": 2397,
        "openIssues": 448,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T13:38:54Z"
      }
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
        "stars": 90260,
        "forks": 9261,
        "openIssues": 1785,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-09-15T12:39:28Z"
      }
    },
    {
      "repo": "plantuml/plantuml",
      "score": 9.5,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "machine-learning"
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
        "stars": 13317,
        "forks": 1236,
        "openIssues": 586,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "LGPL-3.0",
        "pushedAt": "2026-09-15T21:10:43Z"
      }
    },
    {
      "repo": "plantuml-stdlib/C4-PlantUML",
      "score": 9.2,
      "tier": "recommended",
      "category": "Documentation / architecture / API",
      "domain": "backend",
      "capabilities": [
        "machine-learning"
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
        "stars": 7407,
        "forks": 1169,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-26T14:58:27Z"
      }
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
        "stars": 1589,
        "forks": 111,
        "openIssues": 57,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "Apache-2.0",
        "pushedAt": "2024-12-17T16:51:30Z"
      }
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
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12239,
        "forks": 325,
        "openIssues": 116,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-13T21:28:12Z"
      }
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
        "stars": 8508,
        "forks": 741,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "ISC",
        "pushedAt": "2026-09-16T01:04:47Z"
      }
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
        "stars": 22115,
        "forks": 5913,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T01:57:58Z"
      }
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
        "stars": 76376,
        "forks": 24807,
        "openIssues": 2953,
        "archived": false,
        "disabled": false,
        "defaultBranch": "unstable",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T01:45:36Z"
      }
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
        "stars": 109349,
        "forks": 13923,
        "openIssues": 1159,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T04:48:59Z"
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
        "stars": 57371,
        "forks": 5721,
        "openIssues": 1011,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-16T05:23:11Z"
      }
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
        "stars": 61048,
        "forks": 3686,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T14:40:08Z"
      }
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
        "stars": 47608,
        "forks": 2537,
        "openIssues": 2631,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T19:09:42Z"
      }
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
        "stars": 35781,
        "forks": 1620,
        "openIssues": 2024,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:45:34Z"
      }
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
        "stars": 102357,
        "forks": 9890,
        "openIssues": 77,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-14T18:49:48Z"
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
        "stars": 76721,
        "forks": 8551,
        "openIssues": 27,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T00:52:17Z"
      }
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
        "stars": 40609,
        "forks": 1672,
        "openIssues": 195,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T19:23:57Z"
      }
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
        "stars": 20342,
        "forks": 2111,
        "openIssues": 99,
        "archived": false,
        "disabled": false,
        "defaultBranch": "17.x.x",
        "license": "MIT",
        "pushedAt": "2026-09-09T16:59:37Z"
      }
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
        "stars": 13952,
        "forks": 2006,
        "openIssues": 89,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:49:03Z"
      }
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
        "stars": 36797,
        "forks": 8934,
        "openIssues": 3290,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:06:59Z"
      }
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
        "stars": 13879,
        "forks": 1184,
        "openIssues": 224,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-07-29T09:30:37Z"
      }
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
        "stars": 34738,
        "forks": 3002,
        "openIssues": 764,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:42:18Z"
      }
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
        "stars": 250480,
        "forks": 51354,
        "openIssues": 1373,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:27:02Z"
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
        "stars": 142332,
        "forks": 32065,
        "openIssues": 3356,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:56:35Z"
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
        "stars": 82846,
        "forks": 8744,
        "openIssues": 775,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:50:49Z"
      }
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
        "stars": 97570,
        "forks": 5754,
        "openIssues": 71,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-08T17:15:40Z"
      }
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
        "stars": 123916,
        "forks": 10321,
        "openIssues": 1847,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-12T13:26:36Z"
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
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 99048,
        "forks": 32528,
        "openIssues": 1470,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:23:03Z"
      }
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
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 40642,
        "forks": 3645,
        "openIssues": 16,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T20:20:59Z"
      }
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
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 20274,
        "forks": 2931,
        "openIssues": 815,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-15T10:36:15Z"
      }
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
        "stars": 91069,
        "forks": 10451,
        "openIssues": 1849,
        "archived": false,
        "disabled": false,
        "defaultBranch": "next",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:55:47Z"
      }
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
        "stars": 33617,
        "forks": 1357,
        "openIssues": 112,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T14:58:08Z"
      }
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
        "stars": 32315,
        "forks": 1969,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-13T13:32:18Z"
      }
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
        "stars": 21813,
        "forks": 4635,
        "openIssues": 281,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T04:48:06Z"
      }
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
        "stars": 19362,
        "forks": 1426,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T16:31:24Z"
      }
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
        "stars": 178960,
        "forks": 31245,
        "openIssues": 13176,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-16T05:42:34Z"
      }
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
        "stars": 126625,
        "forks": 25248,
        "openIssues": 1148,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T23:46:37Z"
      }
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
        "stars": 52272,
        "forks": 13995,
        "openIssues": 863,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:36:20Z"
      }
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
        "stars": 21969,
        "forks": 6288,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T19:57:53Z"
      }
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
        "stars": 12026,
        "forks": 1910,
        "openIssues": 210,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-07T14:48:39Z"
      }
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
        "stars": 30774,
        "forks": 9764,
        "openIssues": 471,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T19:24:40Z"
      }
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
        "stars": 7512,
        "forks": 934,
        "openIssues": 446,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MPL-2.0",
        "pushedAt": "2026-09-15T22:13:03Z"
      }
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
        "stars": 16253,
        "forks": 923,
        "openIssues": 159,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:17:55Z"
      }
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
        "stars": 72008,
        "forks": 2033,
        "openIssues": 380,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-09T22:50:11Z"
      }
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
        "stars": 12048,
        "forks": 457,
        "openIssues": 744,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MPL-2.0",
        "pushedAt": "2025-10-23T20:10:46Z"
      }
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
        "stars": 38165,
        "forks": 5815,
        "openIssues": 101,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:54:39Z"
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
        "stars": 32878,
        "forks": 3375,
        "openIssues": 1058,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:41:09Z"
      }
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
        "stars": 127751,
        "forks": 44231,
        "openIssues": 3047,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:13:25Z"
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
        "stars": 30246,
        "forks": 7786,
        "openIssues": 461,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T21:34:29Z"
      }
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
        "stars": 30188,
        "forks": 1366,
        "openIssues": 323,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MPL-2.0",
        "pushedAt": "2026-09-16T00:59:51Z"
      }
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
        "stars": 49664,
        "forks": 10615,
        "openIssues": 1926,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-15T23:56:09Z"
      }
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
        "stars": 70694,
        "forks": 24331,
        "openIssues": 830,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-15T22:52:06Z"
      }
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
        "stars": 24164,
        "forks": 7847,
        "openIssues": 4361,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:13:49Z"
      }
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
        "stars": 8407,
        "forks": 783,
        "openIssues": 263,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T14:25:48Z"
      }
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
        "stars": 66084,
        "forks": 10839,
        "openIssues": 884,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:01:29Z"
      }
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
        "stars": 76766,
        "forks": 14746,
        "openIssues": 3297,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-16T04:30:53Z"
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
        "stars": 44778,
        "forks": 4850,
        "openIssues": 2291,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T04:41:14Z"
      }
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
        "stars": 24037,
        "forks": 1812,
        "openIssues": 406,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:28:42Z"
      }
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
        "stars": 9056,
        "forks": 573,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T11:19:07Z"
      }
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
        "stars": 26963,
        "forks": 2891,
        "openIssues": 109,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:27:17Z"
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
        "stars": 16658,
        "forks": 1057,
        "openIssues": 921,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-2.1",
        "pushedAt": "2026-09-16T00:02:23Z"
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
        "stars": 10093,
        "forks": 2083,
        "openIssues": 1463,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T00:34:08Z"
      }
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
        "stars": 15920,
        "forks": 452,
        "openIssues": 54,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:07:05Z"
      }
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
        "stars": 1897,
        "forks": 240,
        "openIssues": 20,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:51:18Z"
      }
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
        "stars": 2675,
        "forks": 74,
        "openIssues": 86,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-06-08T07:27:09Z"
      }
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
        "stars": 89864,
        "forks": 3584,
        "openIssues": 2902,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T02:07:14Z"
      }
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
        "stars": 15501,
        "forks": 545,
        "openIssues": 240,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-14T01:33:58Z"
      }
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
        "stars": 8971,
        "forks": 673,
        "openIssues": 43,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-14T18:58:21Z"
      }
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
        "stars": 12650,
        "forks": 2899,
        "openIssues": 763,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T21:53:43Z"
      }
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
        "stars": 1439,
        "forks": 172,
        "openIssues": 56,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-12T22:05:54Z"
      }
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
        "stars": 96197,
        "forks": 6444,
        "openIssues": 187,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:20:50Z"
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
        "stars": 14505,
        "forks": 3370,
        "openIssues": 807,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:50:51Z"
      }
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
        "stars": 49645,
        "forks": 2418,
        "openIssues": 2207,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T06:02:02Z"
      }
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
        "stars": 34669,
        "forks": 3776,
        "openIssues": 964,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T05:52:09Z"
      }
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
        "stars": 25155,
        "forks": 2314,
        "openIssues": 644,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T06:02:14Z"
      }
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
        "stars": 18287,
        "forks": 1934,
        "openIssues": 604,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T04:43:30Z"
      }
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
        "stars": 11478,
        "forks": 1131,
        "openIssues": 998,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T03:03:01Z"
      }
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
        "stars": 13996,
        "forks": 3565,
        "openIssues": 977,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T10:51:06Z"
      }
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
        "stars": 19464,
        "forks": 3089,
        "openIssues": 340,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-04-14T15:29:57Z"
      }
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
        "stars": 2296,
        "forks": 384,
        "openIssues": 179,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T23:33:51Z"
      }
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
        "stars": 13833,
        "forks": 1033,
        "openIssues": 61,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T11:56:39Z"
      }
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
        "stars": 36805,
        "forks": 2625,
        "openIssues": 99,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T22:51:44Z"
      }
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
        "stars": 19110,
        "forks": 818,
        "openIssues": 173,
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
        "stars": 11823,
        "forks": 1078,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-04T07:48:43Z"
      }
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
        "stars": 32099,
        "forks": 2942,
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
        "stars": 15078,
        "forks": 1257,
        "openIssues": 430,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "NOASSERTION",
        "pushedAt": "2024-07-23T00:58:54Z"
      }
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
        "stars": 8660,
        "forks": 463,
        "openIssues": 38,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "MIT",
        "pushedAt": "2026-09-15T04:36:20Z"
      }
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
        "stars": 21178,
        "forks": 664,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-07-28T21:12:58Z"
      }
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
        "stars": 15480,
        "forks": 1121,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2022-07-06T22:16:59Z"
      }
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
        "stars": 60140,
        "forks": 9381,
        "openIssues": 177,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-03-09T10:31:58Z"
      }
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
        "stars": 1317,
        "forks": 187,
        "openIssues": 20,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-10T09:52:51Z"
      }
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
        "stars": 38266,
        "forks": 5269,
        "openIssues": 575,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-04T07:47:32Z"
      }
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
        "stars": 69,
        "forks": 4,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2024-03-03T16:36:55Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 57551,
        "forks": 13472,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-08-05T11:39:37Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 12527,
        "forks": 1331,
        "openIssues": 185,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-06-29T09:33:50Z"
      }
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
        "stars": 900,
        "forks": 314,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2025-08-19T01:37:38Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 96668,
        "forks": 14102,
        "openIssues": 47,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-15T11:05:04Z"
      }
    },
    {
      "repo": "camenduru/dust3r-jupyter",
      "score": 8,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "3d-reconstruction",
        "notebooks"
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
        "stars": 24,
        "forks": 1,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2024-03-03T13:43:09Z"
      }
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
        "stars": 7951,
        "forks": 1149,
        "openIssues": 86,
        "archived": false,
        "disabled": false,
        "defaultBranch": "stable",
        "license": "MIT",
        "pushedAt": "2025-02-10T19:33:18Z"
      }
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
        "stars": 31900,
        "forks": 3443,
        "openIssues": 93,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-15T22:35:17Z"
      }
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
        "stars": 13970,
        "forks": 1812,
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
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 49201,
        "forks": 2290,
        "openIssues": 861,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-12T04:09:08Z"
      }
    },
    {
      "repo": "ali-vilab/AnyDoor",
      "score": 8.5,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "object-insertion"
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
        "stars": 4238,
        "forks": 371,
        "openIssues": 64,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2024-04-08T06:31:26Z"
      }
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
        "stars": 29919,
        "forks": 4882,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-14T08:48:04Z"
      }
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
        "stars": 1436,
        "forks": 360,
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
        "stars": 31298,
        "forks": 3723,
        "openIssues": 102,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-15T14:32:21Z"
      }
    },
    {
      "repo": "freestylfly/awesome-gpt-image-2",
      "score": 8.2,
      "tier": "specialized",
      "category": "Média / voix / vidéo",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
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
      "costModel": "open-source"
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 133443,
        "forks": 15785,
        "openIssues": 4880,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-16T05:56:17Z"
      }
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
        "stars": 28223,
        "forks": 2970,
        "openIssues": 372,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T12:27:03Z"
      }
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
        "stars": 49127,
        "forks": 4449,
        "openIssues": 166,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:05:42Z"
      }
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
        "stars": 80896,
        "forks": 17376,
        "openIssues": 36,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-27T07:52:21Z"
      }
    },
    {
      "repo": "megadose/holehe",
      "score": 8.5,
      "tier": "specialized",
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
        "stars": 14922,
        "forks": 1897,
        "openIssues": 117,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2024-09-10T20:24:32Z"
      }
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
        "stars": 62836,
        "forks": 6869,
        "openIssues": 388,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T22:07:49Z"
      }
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
        "stars": 11901,
        "forks": 2445,
        "openIssues": 110,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-08-03T14:33:09Z"
      }
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
        "stars": 2990,
        "forks": 645,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-16T06:01:44Z"
      }
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
        "stars": 35073,
        "forks": 7007,
        "openIssues": 168,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T03:31:53Z"
      }
    },
    {
      "repo": "dutly1/x64dbg-mcp-server",
      "score": 8.4,
      "tier": "specialized",
      "category": "Sécurité / OSINT",
      "domain": "cybersecurity",
      "capabilities": [
        "osint"
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
      "costModel": "open-source"
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
        "stars": 2793,
        "forks": 185,
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
        "unknown"
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
        "stars": 190785,
        "forks": 18158,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-10T22:33:44Z"
      }
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
        "stars": 9763,
        "forks": 1385,
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
        "stars": 1136,
        "forks": 310,
        "openIssues": 104,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-08-05T01:55:49Z"
      }
    },
    {
      "repo": "Illyasviel/Paints-UNDO",
      "score": 9,
      "tier": "recommended",
      "category": "Autres favoris visibles",
      "domain": "ai_media",
      "capabilities": [
        "image-generation",
        "image-editing"
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
      "costModel": "open-source"
    },
    {
      "repo": "bleeeline/aimoneyhunter",
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
      "costModel": "open-source"
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
        "stars": 7430,
        "forks": 562,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2024-10-19T03:27:38Z"
      }
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
        "stars": 260,
        "forks": 63,
        "openIssues": 20,
        "archived": true,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2025-11-03T00:34:43Z"
      }
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
        "stars": 507,
        "forks": 134,
        "openIssues": 24,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2024-06-27T21:58:30Z"
      }
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
        "stars": 2050,
        "forks": 541,
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
        "stars": 1544,
        "forks": 293,
        "openIssues": 62,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-06-10T19:03:50Z"
      }
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
        "stars": 850,
        "forks": 158,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2024-07-20T06:09:18Z"
      }
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
        "stars": 998,
        "forks": 222,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-07-09T11:18:52Z"
      }
    },
    {
      "repo": "alsk1992/CloddsBot",
      "score": 6.8,
      "tier": "audit",
      "category": "Autres favoris visibles",
      "domain": "trading",
      "capabilities": [
        "trading",
        "automation"
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
        "stars": 2746,
        "forks": 332,
        "openIssues": 28,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-12T03:58:12Z"
      }
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
        "stars": 21643,
        "forks": 5247,
        "openIssues": 255,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T22:44:30Z"
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
        "stars": 29002,
        "forks": 3796,
        "openIssues": 130,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-3.0",
        "pushedAt": "2026-09-16T03:45:33Z"
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
        "stars": 9099,
        "forks": 1169,
        "openIssues": 140,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-02T09:14:10Z"
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
        "stars": 48593,
        "forks": 7690,
        "openIssues": 477,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T03:18:42Z"
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
        "stars": 44007,
        "forks": 8835,
        "openIssues": 717,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T21:17:44Z"
      }
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
        "stars": 54432,
        "forks": 11288,
        "openIssues": 28,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-15T04:24:22Z"
      }
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
        "stars": 20020,
        "forks": 4925,
        "openIssues": 162,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T15:22:00Z"
      }
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
        "stars": 16293,
        "forks": 3503,
        "openIssues": 312,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-07-13T23:02:18Z"
      }
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
        "stars": 8964,
        "forks": 1534,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-08-05T12:39:16Z"
      }
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
        "stars": 45400,
        "forks": 12473,
        "openIssues": 25,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-13T06:36:50Z"
      }
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
        "stars": 12246,
        "forks": 2003,
        "openIssues": 137,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-2-Clause",
        "pushedAt": "2026-09-15T18:45:16Z"
      }
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
      "selfHosted": "partial",
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 25255,
        "forks": 3419,
        "openIssues": 105,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-13T13:00:38Z"
      }
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
        "stars": 20910,
        "forks": 5615,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:14:51Z"
      }
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
        "stars": 2983,
        "forks": 501,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T03:55:37Z"
      }
    },
    {
      "repo": "mementum/backtrader",
      "score": 8.7,
      "tier": "specialized",
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
        "stars": 23259,
        "forks": 5280,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2024-08-19T17:47:36Z"
      }
    },
    {
      "repo": "quantopian/zipline",
      "score": 8.3,
      "tier": "specialized",
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
        "stars": 20098,
        "forks": 5049,
        "openIssues": 368,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2024-02-13T08:02:51Z"
      }
    },
    {
      "repo": "hudson-and-thames/mlfinlab",
      "score": 8.2,
      "tier": "specialized",
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
        "stars": 4922,
        "forks": 1285,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2023-10-02T03:05:19Z"
      }
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
        "stars": 2403,
        "forks": 252,
        "openIssues": 35,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T22:05:56Z"
      }
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
        "stars": 6028,
        "forks": 1168,
        "openIssues": 113,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-07T21:18:14Z"
      }
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
        "stars": 4497,
        "forks": 708,
        "openIssues": 20,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-08-18T17:08:34Z"
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
      "resourceLevel": "low",
      "integrationComplexity": "low",
      "costModel": "open-source",
      "github": {
        "stars": 7638,
        "forks": 1234,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-07-20T14:12:56Z"
      }
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
        "stars": 11622,
        "forks": 3592,
        "openIssues": 2817,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T12:50:06Z"
      }
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
        "stars": 1568,
        "forks": 291,
        "openIssues": 51,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-14T05:01:57Z"
      }
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
        "stars": 14799,
        "forks": 1386,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-11T01:45:23Z"
      }
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
        "stars": 7595,
        "forks": 1076,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-14T21:42:02Z"
      }
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
        "stars": 650,
        "forks": 145,
        "openIssues": 14,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-12-15T04:03:16Z"
      }
    },
    {
      "repo": "quantopian/pyfolio",
      "score": 8.4,
      "tier": "specialized",
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
        "stars": 6421,
        "forks": 1894,
        "openIssues": 166,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2023-12-23T06:14:58Z"
      }
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
        "stars": 9521,
        "forks": 1043,
        "openIssues": 231,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-07T11:18:12Z"
      }
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
        "stars": 10017,
        "forks": 2360,
        "openIssues": 2478,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T22:55:08Z"
      }
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
        "stars": 4273,
        "forks": 504,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T14:10:43Z"
      }
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
        "stars": 6470,
        "forks": 635,
        "openIssues": 66,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-19T01:26:53Z"
      }
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
        "stars": 9424,
        "forks": 1283,
        "openIssues": 74,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-06T01:28:19Z"
      }
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
        "stars": 22598,
        "forks": 3509,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T04:16:55Z"
      }
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
        "stars": 434,
        "forks": 94,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-05-29T02:58:13Z"
      }
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
      "selfHosted": "partial",
      "runtime": [
        "local",
        "external-services"
      ],
      "resourceLevel": "medium",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73053,
        "forks": 7557,
        "openIssues": 116,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-14T20:20:53Z"
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
        "stars": 18785,
        "forks": 2844,
        "openIssues": 711,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T21:35:57Z"
      }
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
        "stars": 4432,
        "forks": 678,
        "openIssues": 176,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2024-08-08T17:23:11Z"
      }
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
        "stars": 67265,
        "forks": 27405,
        "openIssues": 2163,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-14T23:49:53Z"
      }
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
        "stars": 28766,
        "forks": 8896,
        "openIssues": 435,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T10:58:05Z"
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
        "stars": 9101,
        "forks": 1334,
        "openIssues": 722,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:17:33Z"
      }
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
        "stars": 25760,
        "forks": 3750,
        "openIssues": 989,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T21:18:04Z"
      }
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
        "stars": 2957,
        "forks": 481,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-07-07T01:34:50Z"
      }
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
        "stars": 6439,
        "forks": 1162,
        "openIssues": 281,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "LGPL-3.0",
        "pushedAt": "2026-04-17T20:59:38Z"
      }
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
        "stars": 3177,
        "forks": 384,
        "openIssues": 82,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-2-Clause",
        "pushedAt": "2026-09-12T15:48:15Z"
      }
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
        "stars": 3424,
        "forks": 755,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2024-10-31T09:14:35Z"
      }
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
        "stars": 2280,
        "forks": 370,
        "openIssues": 93,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T17:21:34Z"
      }
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
        "stars": 7121,
        "forks": 1365,
        "openIssues": 90,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-06-29T16:33:16Z"
      }
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
        "stars": 1331,
        "forks": 403,
        "openIssues": 85,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-04-20T19:22:17Z"
      }
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
        "stars": 48754,
        "forks": 3958,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-06T20:26:10Z"
      }
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
        "stars": 32159,
        "forks": 3095,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-11T13:41:32Z"
      }
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
        "stars": 7949,
        "forks": 707,
        "openIssues": 128,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-15T13:58:56Z"
      }
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
        "stars": 63922,
        "forks": 4240,
        "openIssues": 176,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:44:57Z"
      }
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
        "stars": 4526,
        "forks": 907,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2025-10-01T17:10:58Z"
      }
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
        "stars": 5518,
        "forks": 1048,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-08-30T13:22:58Z"
      }
    },
    {
      "repo": "yeyintminthuhtut/Awesome-Red-Teaming",
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
        "stars": 8093,
        "forks": 1754,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2023-12-28T18:10:52Z"
      }
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
        "stars": 9721,
        "forks": 1302,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-04-18T09:27:42Z"
      }
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
        "stars": 10716,
        "forks": 2373,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-05-07T23:44:01Z"
      }
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
        "stars": 12544,
        "forks": 3212,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-14T11:11:59Z"
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
        "stars": 27204,
        "forks": 4947,
        "openIssues": 119,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-07-25T12:15:45Z"
      }
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
        "stars": 15482,
        "forks": 2693,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-07-14T12:58:31Z"
      }
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
        "stars": 24520,
        "forks": 3139,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-10T05:45:01Z"
      }
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
        "stars": 5458,
        "forks": 707,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-30T11:02:24Z"
      }
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
        "stars": 67257,
        "forks": 10917,
        "openIssues": 54,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC0-1.0",
        "pushedAt": "2026-09-15T16:46:47Z"
      }
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
        "stars": 72358,
        "forks": 5545,
        "openIssues": 656,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T02:23:53Z"
      }
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
        "stars": 146422,
        "forks": 24478,
        "openIssues": 515,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T04:35:22Z"
      }
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
        "stars": 184527,
        "forks": 13597,
        "openIssues": 669,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T00:16:34Z"
      }
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
        "stars": 155893,
        "forks": 24623,
        "openIssues": 1066,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T03:43:04Z"
      }
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
        "stars": 9251,
        "forks": 4116,
        "openIssues": 75,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-15T21:03:29Z"
      }
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
        "stars": 61201,
        "forks": 6913,
        "openIssues": 25,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-09-03T04:34:54Z"
      }
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
        "stars": 14968,
        "forks": 1483,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-10T17:44:23Z"
      }
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
        "stars": 48400,
        "forks": 3447,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T14:43:57Z"
      }
    },
    {
      "repo": "blaCCkHatHacEEkr/PENTESTING-BIBLE",
      "score": 8.8,
      "tier": "specialized",
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
        "stars": 13965,
        "forks": 2464,
        "openIssues": 28,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2023-04-03T07:40:28Z"
      }
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
        "stars": 65372,
        "forks": 7662,
        "openIssues": 752,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T21:19:16Z"
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
        "stars": 93998,
        "forks": 8279,
        "openIssues": 191,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T01:00:29Z"
      }
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
        "stars": 29991,
        "forks": 6631,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "live",
        "license": "MIT",
        "pushedAt": "2026-09-09T16:27:56Z"
      }
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
        "stars": 43452,
        "forks": 3537,
        "openIssues": 590,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T02:32:40Z"
      }
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
        "stars": 63093,
        "forks": 4760,
        "openIssues": 69,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T01:32:09Z"
      }
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
        "stars": 39001,
        "forks": 3944,
        "openIssues": 445,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-11T03:56:20Z"
      }
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
        "stars": 82792,
        "forks": 15896,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2024-07-29T19:34:21Z"
      }
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
        "stars": 10091,
        "forks": 1014,
        "openIssues": 14,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-10T22:59:08Z"
      }
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
        "stars": 74823,
        "forks": 24673,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-10T17:41:19Z"
      }
    },
    {
      "repo": "FlowiseAI/Flowise",
      "score": 9.5,
      "tier": "recommended",
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
        "stars": 55466,
        "forks": 25022,
        "openIssues": 1040,
        "archived": true,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-13T12:38:19Z"
      }
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
        "stars": 58840,
        "forks": 11478,
        "openIssues": 5096,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T05:45:25Z"
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
        "stars": 82512,
        "forks": 11378,
        "openIssues": 907,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T14:22:13Z"
      }
    },
    {
      "repo": "lettier/3d-game-shaders-for-beginners",
      "score": 9.2,
      "tier": "recommended",
      "category": "Graphics / shaders",
      "domain": "graphics",
      "capabilities": [
        "rendering",
        "game-development"
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
        "stars": 19898,
        "forks": 1479,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2023-06-25T21:58:57Z"
      }
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
        "unknown"
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
        "stars": 25130,
        "forks": 3588,
        "openIssues": 60,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-21T23:33:07Z"
      }
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
        "stars": 117255,
        "forks": 26764,
        "openIssues": 18890,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T22:57:08Z"
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
        "stars": 25398,
        "forks": 6527,
        "openIssues": 337,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-09T08:20:10Z"
      }
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
        "stars": 20499,
        "forks": 2260,
        "openIssues": 221,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:41:02Z"
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
        "stars": 37601,
        "forks": 2939,
        "openIssues": 68,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T06:03:11Z"
      }
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
        "stars": 91637,
        "forks": 10790,
        "openIssues": 344,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T05:17:48Z"
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
        "stars": 44765,
        "forks": 4154,
        "openIssues": 1142,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:15:47Z"
      }
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
      "resourceLevel": "low",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 73544,
        "forks": 25115,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T11:16:16Z"
      }
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
        "stars": 7270,
        "forks": 1361,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-15T22:36:00Z"
      }
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
      "integrationComplexity": "high",
      "costModel": "open-source",
      "github": {
        "stars": 39015,
        "forks": 14971,
        "openIssues": 608,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-15T10:37:23Z"
      }
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
      "resourceLevel": "high",
      "integrationComplexity": "medium",
      "costModel": "open-source",
      "github": {
        "stars": 166220,
        "forks": 34591,
        "openIssues": 2436,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T05:51:17Z"
      }
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
        "stars": 5584,
        "forks": 417,
        "openIssues": 43,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-14T10:25:56Z"
      }
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
        "stars": 29286,
        "forks": 2080,
        "openIssues": 163,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-16T03:27:16Z"
      }
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
        "stars": 9068,
        "forks": 983,
        "openIssues": 25,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T10:31:07Z"
      }
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
        "stars": 59383,
        "forks": 7475,
        "openIssues": 322,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-06T05:02:34Z"
      }
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
        "stars": 6316,
        "forks": 525,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-12T15:29:58Z"
      }
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
        "stars": 5293,
        "forks": 3135,
        "openIssues": 81,
        "archived": false,
        "disabled": false,
        "defaultBranch": "4.3",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-16T00:14:28Z"
      }
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
        "stars": 6096,
        "forks": 820,
        "openIssues": 76,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-14T13:33:30Z"
      }
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
        "unknown"
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
        "stars": 26876,
        "forks": 3838,
        "openIssues": 45,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-02T17:51:00Z"
      }
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
        "stars": 35725,
        "forks": 5428,
        "openIssues": 73,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-02-15T22:03:57Z"
      }
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
        "stars": 10751,
        "forks": 586,
        "openIssues": 70,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "CC-BY-4.0",
        "pushedAt": "2026-09-12T21:34:34Z"
      }
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
        "stars": 13340,
        "forks": 1491,
        "openIssues": 123,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T16:37:08Z"
      }
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
        "stars": 83626,
        "forks": 8637,
        "openIssues": 197,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T16:13:39Z"
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
        "stars": 180989,
        "forks": 9815,
        "openIssues": 626,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-16T02:47:02Z"
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
        "stars": 11053,
        "forks": 1093,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-14T23:04:35Z"
      }
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
        "stars": 9309,
        "forks": 1377,
        "openIssues": 18,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-11T21:07:34Z"
      }
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
        "stars": 13778,
        "forks": 1645,
        "openIssues": 156,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-05-15T07:18:04Z"
      }
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
        "stars": 33522,
        "forks": 5467,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T17:30:34Z"
      }
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
        "stars": 6123,
        "forks": 885,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-05-11T05:44:09Z"
      }
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
        "stars": 37602,
        "forks": 4268,
        "openIssues": 120,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-02T12:12:35Z"
      }
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
        "stars": 31680,
        "forks": 4477,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-08T14:49:11Z"
      }
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
        "stars": 106794,
        "forks": 20400,
        "openIssues": 349,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-15T01:33:49Z"
      }
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
        "stars": 6857,
        "forks": 1055,
        "openIssues": 474,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-15T23:18:43Z"
      }
    }
  ],
  "metadata": {
    "githubRefreshedAt": "2026-09-16T06:04:07.801251Z",
    "githubRefreshFailures": [
      {
        "repo": "Alisharvr1/free-claude-code",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "lisys93/web-check",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "bnmf/tron",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "harry2141985/Google-Colab-Notebooks",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "freestylfly/awesome-gpt-image-2",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "dutly1/x64dbg-mcp-server",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "Illyasviel/Paints-UNDO",
        "error": "HTTP Error 404: Not Found"
      },
      {
        "repo": "bleeeline/aimoneyhunter",
        "error": "HTTP Error 404: Not Found"
      }
    ]
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
          }
        },
        "additionalProperties": false
      }
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
        "stars": 76263,
        "pushedAt": "2026-09-15T01:05:48Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 29952,
        "pushedAt": "2026-09-15T14:02:01Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 19677,
        "pushedAt": "2026-09-02T18:38:03Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "Robbyant/lingbot-map": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 17059,
        "pushedAt": "2026-09-08T06:31:41Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "PavelDoGreat/WebGL-Fluid-Simulation": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16637,
        "pushedAt": "2024-11-12T13:29:23Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "OpenRCT2/OpenRCT2": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16227,
        "pushedAt": "2026-09-16T04:06:01Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "budtmo/docker-android": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 15855,
        "pushedAt": "2026-09-11T06:29:51Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 14725,
        "pushedAt": "2025-10-22T02:13:14Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "ytisf/theZoo": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 13384,
        "pushedAt": "2026-09-14T06:47:21Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "alicevision/Meshroom": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 12965,
        "pushedAt": "2026-09-15T14:32:30Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "jrouwe/JoltPhysics": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11548,
        "pushedAt": "2026-09-15T20:06:02Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "horsicq/Detect-It-Easy": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11538,
        "pushedAt": "2026-09-16T05:51:34Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 9687,
        "pushedAt": "2026-09-14T21:07:32Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "VAST-AI-Research/TripoSR": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6958,
        "pushedAt": "2026-06-04T07:11:09Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "openMVG/openMVG": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6558,
        "pushedAt": "2026-08-30T17:24:15Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "cnr-isti-vclab/meshlab": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5830,
        "pushedAt": "2026-08-25T20:38:52Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "ArthurBrussee/brush": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5096,
        "pushedAt": "2026-09-15T21:55:59Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 4737,
        "pushedAt": "2026-09-11T07:49:10Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 4207,
        "pushedAt": "2026-09-01T23:06:47Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "kevoreilly/CAPEv2": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 3497,
        "pushedAt": "2026-09-15T01:23:02Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 10558,
        "pushedAt": "2026-06-07T08:09:08Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "NVlabs/instant-ngp": {
      "fingerprint": {
        "decision": "accept",
        "score": 97.7,
        "stars": 17550,
        "pushedAt": "2026-02-02T12:32:34Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 18729,
        "pushedAt": "2026-05-30T07:11:00Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "pedramamini/awesome-yara": {
      "fingerprint": {
        "decision": "accept",
        "score": 93.4,
        "stars": 4273,
        "pushedAt": "2026-06-15T19:57:31Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "nuysoft/Mock": {
      "fingerprint": {
        "decision": "accept",
        "score": 88.4,
        "stars": 19575,
        "pushedAt": "2024-03-15T01:53:57Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 14195,
        "pushedAt": "2024-06-07T05:09:47Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "yfeng95/PRNet": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.6,
        "stars": 5014,
        "pushedAt": "2022-07-25T23:50:26Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "score": 85.5,
        "stars": 12000,
        "pushedAt": "2025-07-29T02:30:55Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 6918,
        "pushedAt": "2024-05-13T00:39:07Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "score": 83.1,
        "stars": 4261,
        "pushedAt": "2024-07-10T07:53:06Z",
        "targets": [
          [
            "capability",
            "3d-human"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "mortenjust/androidtool-mac": {
      "fingerprint": {
        "decision": "accept",
        "score": 81.9,
        "stars": 5414,
        "pushedAt": "2023-03-16T03:28:28Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
        "stars": 9551,
        "pushedAt": "2024-06-17T11:35:26Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "CalebFenton/simplify": {
      "fingerprint": {
        "decision": "review",
        "score": 71.2,
        "stars": 4662,
        "pushedAt": "2022-04-30T12:20:33Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "timzhang642/3D-Machine-Learning": {
      "fingerprint": {
        "decision": "review",
        "score": 70.3,
        "stars": 10200,
        "pushedAt": "2024-07-04T19:13:09Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
    },
    "bee-san/pyWhat": {
      "fingerprint": {
        "decision": "review",
        "score": 69.9,
        "stars": 7322,
        "pushedAt": "2023-10-31T22:01:01Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-16T06:05:18.257533Z"
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
