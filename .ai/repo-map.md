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
valid_lifecycles = {"active","stable","reference","legacy"}
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
        "stars": 82681,
        "forks": 15900,
        "openIssues": 943,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T17:54:56Z"
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
        "stars": 124842,
        "forks": 19346,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:57:25Z"
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
        "stars": 74926,
        "forks": 9178,
        "openIssues": 1155,
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
        "stars": 23043,
        "forks": 2167,
        "openIssues": 247,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T00:51:42Z"
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
        "stars": 13520,
        "forks": 2443,
        "openIssues": 1199,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:12:30Z"
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
        "stars": 88634,
        "forks": 11660,
        "openIssues": 867,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T11:40:44Z"
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
        "stars": 44020,
        "forks": 4272,
        "openIssues": 72,
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
        "stars": 181317,
        "forks": 17944,
        "openIssues": 4045,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T20:41:40Z"
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
        "stars": 37435,
        "forks": 2489,
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
        "stars": 90500,
        "forks": 11668,
        "openIssues": 550,
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
        "stars": 115527,
        "forks": 12711,
        "openIssues": 459,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T22:34:42Z"
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
        "stars": 23758,
        "forks": 1715,
        "openIssues": 264,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T12:05:59Z"
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
        "stars": 266374,
        "forks": 22490,
        "openIssues": 505,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T10:12:48Z"
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
        "stars": 142973,
        "forks": 7669,
        "openIssues": 287,
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
        "stars": 263552,
        "forks": 39438,
        "openIssues": 206,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:26:52Z"
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
        "stars": 38168,
        "forks": 5988,
        "openIssues": 228,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:14:20Z"
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
        "stars": 68549,
        "forks": 9701,
        "openIssues": 518,
        "archived": false,
        "disabled": false,
        "defaultBranch": "release/v3.8.51",
        "license": "MIT",
        "pushedAt": "2026-09-19T08:30:04Z"
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
        "stars": 289173,
        "forks": 25876,
        "openIssues": 374,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:43:04Z"
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
        "stars": 49138,
        "forks": 2849,
        "openIssues": 69,
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
        "stars": 31954,
        "forks": 3589,
        "openIssues": 85,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-19T02:38:32Z"
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
        "stars": 231100,
        "forks": 27702,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-17T13:30:15Z"
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
        "stars": 153732,
        "forks": 24800,
        "openIssues": 156,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:58:53Z"
      }
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
        "stars": 55554,
        "forks": 8888,
        "openIssues": 396,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-21T02:44:42Z"
      }
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
        "stars": 42926,
        "forks": 2880,
        "openIssues": 793,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T22:18:42Z"
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
        "stars": 195273,
        "forks": 108481,
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
        "stars": 74126,
        "forks": 11406,
        "openIssues": 145,
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
        "stars": 95337,
        "forks": 16400,
        "openIssues": 2360,
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
        "stars": 139136,
        "forks": 20453,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:48:37Z"
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
        "stars": 24169,
        "forks": 3007,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T21:06:05Z"
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
        "stars": 19798,
        "forks": 2234,
        "openIssues": 286,
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
        "stars": 3185,
        "forks": 554,
        "openIssues": 283,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T19:00:23Z"
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
        "stars": 7298,
        "forks": 501,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:06:15Z"
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
        "stars": 38187,
        "forks": 2965,
        "openIssues": 707,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T13:30:05Z"
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
        "stars": 208842,
        "forks": 27501,
        "openIssues": 6007,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:49:04Z"
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
        "stars": 72919,
        "forks": 8656,
        "openIssues": 1002,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T14:59:45Z"
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
        "stars": 247437,
        "forks": 52041,
        "openIssues": 43305,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:13:47Z"
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
        "stars": 52364,
        "forks": 4326,
        "openIssues": 123,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:18:04Z"
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
        "stars": 51906,
        "forks": 4727,
        "openIssues": 196,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T19:12:22Z"
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
        "stars": 44473,
        "forks": 9135,
        "openIssues": 772,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:02:19Z"
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
        "stars": 170833,
        "forks": 21949,
        "openIssues": 78,
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
        "stars": 49084,
        "forks": 4982,
        "openIssues": 1884,
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
        "stars": 15647,
        "forks": 1172,
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
        "stars": 42020,
        "forks": 7093,
        "openIssues": 810,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:19:47Z"
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
        "stars": 61079,
        "forks": 9238,
        "openIssues": 1086,
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
        "stars": 58822,
        "forks": 8522,
        "openIssues": 429,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:11:01Z"
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
        "stars": 21581,
        "forks": 4040,
        "openIssues": 535,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T05:53:39Z"
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
        "stars": 17747,
        "forks": 2082,
        "openIssues": 488,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T04:56:23Z"
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
        "python"
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
        "stars": 481862,
        "forks": 53212,
        "openIssues": 1950,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-18T19:39:43Z"
      }
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
        "stars": 34882,
        "forks": 2861,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T21:08:24Z"
      }
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
        "stars": 244920,
        "forks": 14362,
        "openIssues": 171,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-11-19T14:00:38Z"
      }
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
        "stars": 6571,
        "forks": 416,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-09T17:39:58Z"
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
        "stars": 29592,
        "forks": 1154,
        "openIssues": 193,
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
        "stars": 877,
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
        "stars": 913,
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
        "stars": 455848,
        "forks": 46869,
        "openIssues": 213,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T15:48:25Z"
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
        "stars": 7090,
        "forks": 406,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T18:29:37Z"
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
        "stars": 33297,
        "forks": 5405,
        "openIssues": 113,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T23:55:40Z"
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
        "stars": 41525,
        "forks": 2664,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T17:47:52Z"
      }
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
        "stars": 76261,
        "forks": 8583,
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
        "stars": 62914,
        "forks": 3688,
        "openIssues": 34,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T23:16:16Z"
      }
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
        "stars": 24637,
        "forks": 1702,
        "openIssues": 395,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T01:49:28Z"
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
        "stars": 34711,
        "forks": 2688,
        "openIssues": 741,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T19:08:36Z"
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
        "stars": 29338,
        "forks": 2524,
        "openIssues": 879,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T23:12:37Z"
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
        "stars": 46175,
        "forks": 4257,
        "openIssues": 1438,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T14:27:36Z"
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
        "stars": 26563,
        "forks": 3155,
        "openIssues": 183,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T02:18:02Z"
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
        "stars": 27467,
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
        "stars": 22453,
        "forks": 2647,
        "openIssues": 190,
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
        "stars": 66303,
        "forks": 10039,
        "openIssues": 400,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T20:35:06Z"
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
        "stars": 9271,
        "forks": 1039,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T10:01:55Z"
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
        "stars": 29013,
        "forks": 9257,
        "openIssues": 1130,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T11:54:20Z"
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
        "stars": 25916,
        "forks": 2396,
        "openIssues": 446,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T13:06:23Z"
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
        "stars": 90324,
        "forks": 9273,
        "openIssues": 1793,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-09-18T10:41:27Z"
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
        "machine-learning"
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
        "stars": 13325,
        "forks": 1237,
        "openIssues": 588,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "LGPL-3.0",
        "pushedAt": "2026-09-20T17:56:41Z"
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
        "stars": 7409,
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
        "stars": 1593,
        "forks": 110,
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
        "stars": 12248,
        "forks": 327,
        "openIssues": 114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T23:39:10Z"
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
        "stars": 8511,
        "forks": 741,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "ISC",
        "pushedAt": "2026-09-20T05:10:50Z"
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
        "stars": 22162,
        "forks": 5922,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T05:17:27Z"
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
        "stars": 76421,
        "forks": 24814,
        "openIssues": 2959,
        "archived": false,
        "disabled": false,
        "defaultBranch": "unstable",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T07:21:25Z"
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
        "stars": 110415,
        "forks": 14448,
        "openIssues": 1143,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T17:08:05Z"
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
        "stars": 57424,
        "forks": 5732,
        "openIssues": 994,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T19:13:43Z"
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
        "stars": 61116,
        "forks": 3693,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-17T22:29:46Z"
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
        "stars": 47640,
        "forks": 2539,
        "openIssues": 2649,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T20:00:41Z"
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
        "stars": 35837,
        "forks": 1637,
        "openIssues": 2042,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T06:22:02Z"
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
        "stars": 102485,
        "forks": 9916,
        "openIssues": 83,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-18T21:24:37Z"
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
        "stars": 76690,
        "forks": 8556,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:56:39Z"
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
        "stars": 40627,
        "forks": 1679,
        "openIssues": 199,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T08:05:27Z"
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
        "stars": 20346,
        "forks": 2113,
        "openIssues": 98,
        "archived": false,
        "disabled": false,
        "defaultBranch": "17.x.x",
        "license": "MIT",
        "pushedAt": "2026-09-17T21:04:22Z"
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
        "stars": 13953,
        "forks": 2005,
        "openIssues": 88,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:07:37Z"
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
        "stars": 36885,
        "forks": 8945,
        "openIssues": 3269,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T03:09:56Z"
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
        "stars": 13883,
        "forks": 1186,
        "openIssues": 228,
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
        "stars": 34853,
        "forks": 3004,
        "openIssues": 770,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T08:15:13Z"
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
        "stars": 250608,
        "forks": 51380,
        "openIssues": 1381,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T09:18:04Z"
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
        "stars": 142395,
        "forks": 32529,
        "openIssues": 3462,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:40:38Z"
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
        "stars": 82913,
        "forks": 8758,
        "openIssues": 788,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T21:41:28Z"
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
        "stars": 97636,
        "forks": 6211,
        "openIssues": 74,
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
        "stars": 124255,
        "forks": 10842,
        "openIssues": 1852,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T16:46:35Z"
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
        "stars": 99066,
        "forks": 32524,
        "openIssues": 1475,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T01:35:55Z"
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
        "stars": 40658,
        "forks": 3646,
        "openIssues": 14,
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
        "stars": 20283,
        "forks": 2932,
        "openIssues": 817,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-18T10:44:27Z"
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
        "stars": 91107,
        "forks": 10455,
        "openIssues": 1850,
        "archived": false,
        "disabled": false,
        "defaultBranch": "next",
        "license": "MIT",
        "pushedAt": "2026-09-20T01:05:17Z"
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
        "stars": 33666,
        "forks": 1364,
        "openIssues": 112,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T17:39:36Z"
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
        "stars": 32393,
        "forks": 1975,
        "openIssues": 76,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-16T09:36:08Z"
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
        "stars": 21829,
        "forks": 4640,
        "openIssues": 281,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:20:03Z"
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
        "stars": 19375,
        "forks": 1428,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T03:17:13Z"
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
        "stars": 179023,
        "forks": 31753,
        "openIssues": 13250,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T10:58:46Z"
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
        "stars": 126670,
        "forks": 25281,
        "openIssues": 1153,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:57:13Z"
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
        "stars": 52353,
        "forks": 14103,
        "openIssues": 901,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:09:08Z"
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
        "stars": 21990,
        "forks": 6288,
        "openIssues": 46,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:49:25Z"
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
        "stars": 12027,
        "forks": 1911,
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
        "stars": 30796,
        "forks": 9764,
        "openIssues": 464,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T12:06:48Z"
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
        "stars": 7536,
        "forks": 936,
        "openIssues": 439,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MPL-2.0",
        "pushedAt": "2026-09-18T18:02:42Z"
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
        "stars": 16276,
        "forks": 924,
        "openIssues": 202,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T02:53:50Z"
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
        "stars": 72066,
        "forks": 2039,
        "openIssues": 381,
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
        "stars": 12048,
        "forks": 458,
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
        "stars": 38202,
        "forks": 5826,
        "openIssues": 107,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T14:21:57Z"
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
        "stars": 32900,
        "forks": 3381,
        "openIssues": 1033,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T19:27:59Z"
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
        "stars": 127856,
        "forks": 44741,
        "openIssues": 3086,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T03:13:59Z"
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
        "stars": 30263,
        "forks": 7789,
        "openIssues": 467,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-17T22:12:56Z"
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
        "stars": 30237,
        "forks": 1373,
        "openIssues": 327,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MPL-2.0",
        "pushedAt": "2026-09-18T15:10:12Z"
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
        "stars": 49699,
        "forks": 10627,
        "openIssues": 1927,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-18T18:44:41Z"
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
        "stars": 70750,
        "forks": 24334,
        "openIssues": 836,
        "archived": false,
        "disabled": false,
        "defaultBranch": "devel",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-18T18:12:11Z"
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
        "stars": 24205,
        "forks": 7861,
        "openIssues": 4359,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T14:27:40Z"
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
        "stars": 8418,
        "forks": 785,
        "openIssues": 257,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T12:34:42Z"
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
        "stars": 66143,
        "forks": 10846,
        "openIssues": 904,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T15:19:50Z"
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
        "stars": 76819,
        "forks": 14762,
        "openIssues": 3297,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T15:49:10Z"
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
        "stars": 44811,
        "forks": 4858,
        "openIssues": 2301,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T12:22:25Z"
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
        "stars": 24051,
        "forks": 1809,
        "openIssues": 406,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:59:10Z"
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
        "stars": 9062,
        "forks": 573,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T06:47:25Z"
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
        "stars": 26999,
        "forks": 2906,
        "openIssues": 113,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T05:25:00Z"
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
        "stars": 16704,
        "forks": 1063,
        "openIssues": 927,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-2.1",
        "pushedAt": "2026-09-18T00:02:40Z"
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
        "stars": 10109,
        "forks": 2091,
        "openIssues": 1471,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T16:53:07Z"
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
        "stars": 15972,
        "forks": 454,
        "openIssues": 68,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T04:53:38Z"
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
        "stars": 1915,
        "forks": 242,
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
        "stars": 90016,
        "forks": 3598,
        "openIssues": 2903,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:54:15Z"
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
        "stars": 15506,
        "forks": 547,
        "openIssues": 244,
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
        "stars": 8997,
        "forks": 675,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T00:08:57Z"
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
        "stars": 12661,
        "forks": 2903,
        "openIssues": 759,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T20:03:29Z"
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
        "forks": 172,
        "openIssues": 57,
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
        "stars": 96411,
        "forks": 6472,
        "openIssues": 219,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T01:47:13Z"
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
        "stars": 14519,
        "forks": 3391,
        "openIssues": 826,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T00:45:42Z"
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
        "stars": 49706,
        "forks": 2424,
        "openIssues": 2190,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:27:34Z"
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
        "stars": 34855,
        "forks": 3820,
        "openIssues": 931,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T17:32:19Z"
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
        "stars": 25312,
        "forks": 2347,
        "openIssues": 636,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:32:00Z"
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
        "stars": 18356,
        "forks": 1959,
        "openIssues": 629,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T16:48:03Z"
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
        "stars": 11549,
        "forks": 1143,
        "openIssues": 1028,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T13:31:32Z"
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
        "stars": 14036,
        "forks": 3578,
        "openIssues": 1002,
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
        "stars": 19486,
        "forks": 3092,
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
        "stars": 2299,
        "forks": 386,
        "openIssues": 182,
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
        "stars": 13892,
        "forks": 1041,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T19:05:44Z"
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
        "stars": 36835,
        "forks": 2641,
        "openIssues": 100,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T17:22:22Z"
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
        "stars": 19135,
        "forks": 821,
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
        "stars": 11827,
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
        "stars": 32112,
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
        "stars": 15078,
        "forks": 1256,
        "openIssues": 430,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "NOASSERTION",
        "pushedAt": "2024-07-23T00:58:54Z"
      },
      "lifecycle": "stable"
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
        "stars": 8661,
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
        "stars": 21189,
        "forks": 663,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2024-07-28T21:12:58Z"
      },
      "lifecycle": "stable"
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
        "stars": 15480,
        "forks": 1121,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2022-07-06T22:16:59Z"
      },
      "lifecycle": "stable"
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
        "stars": 60142,
        "forks": 9382,
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
        "stars": 1324,
        "forks": 187,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T09:11:17Z"
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
        "stars": 38396,
        "forks": 5274,
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
        "stars": 57557,
        "forks": 13469,
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
        "stars": 12549,
        "forks": 1330,
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
        "stars": 96741,
        "forks": 14116,
        "openIssues": 49,
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
      ]
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
        "stars": 7965,
        "forks": 1151,
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
        "stars": 31934,
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
        "stars": 13981,
        "forks": 1820,
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
        "stars": 49302,
        "forks": 2301,
        "openIssues": 865,
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
        "stars": 4240,
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
        "stars": 29966,
        "forks": 4888,
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
        "stars": 1441,
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
        "stars": 33470,
        "forks": 3957,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T18:51:38Z"
      }
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
        "stars": 134094,
        "forks": 15883,
        "openIssues": 4896,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-20T17:32:01Z"
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
        "stars": 28251,
        "forks": 2977,
        "openIssues": 370,
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
        "stars": 49192,
        "forks": 4458,
        "openIssues": 156,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:39:06Z"
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
        "stars": 80998,
        "forks": 17387,
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
        "stars": 14957,
        "forks": 1915,
        "openIssues": 119,
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
        "stars": 63848,
        "forks": 6983,
        "openIssues": 399,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T03:10:17Z"
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
        "stars": 12002,
        "forks": 2459,
        "openIssues": 112,
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
        "stars": 3001,
        "forks": 645,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-20T18:48:33Z"
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
        "stars": 39376,
        "forks": 7966,
        "openIssues": 225,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-17T00:37:30Z"
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
        "stars": 2026,
        "forks": 205,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T13:02:00Z"
      }
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
        "stars": 2794,
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
        "stars": 191358,
        "forks": 18198,
        "openIssues": 9,
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
        "stars": 9777,
        "forks": 1387,
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
        "stars": 1136,
        "forks": 310,
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
        "stars": 4067,
        "forks": 394,
        "openIssues": 70,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-08-13T22:11:05Z"
      }
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
        "stars": 18162,
        "forks": 1762,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2025-10-20T00:24:54Z"
      }
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
        "stars": 7428,
        "forks": 563,
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
        "forks": 63,
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
        "stars": 510,
        "forks": 135,
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
        "stars": 2054,
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
        "stars": 1547,
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
        "stars": 1009,
        "forks": 227,
        "openIssues": 11,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-16T21:16:57Z"
      }
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
        "stars": 2808,
        "forks": 342,
        "openIssues": 32,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T19:38:27Z"
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
        "stars": 21701,
        "forks": 5253,
        "openIssues": 254,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T22:51:33Z"
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
        "stars": 29202,
        "forks": 3855,
        "openIssues": 126,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "LGPL-3.0",
        "pushedAt": "2026-09-20T19:13:24Z"
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
        "stars": 9137,
        "forks": 1172,
        "openIssues": 139,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-17T20:38:03Z"
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
        "stars": 48692,
        "forks": 7708,
        "openIssues": 480,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-17T16:40:12Z"
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
        "stars": 44074,
        "forks": 8849,
        "openIssues": 693,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T12:48:58Z"
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
        "stars": 54600,
        "forks": 11324,
        "openIssues": 30,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-19T11:07:05Z"
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
        "stars": 20098,
        "forks": 4949,
        "openIssues": 163,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T12:13:41Z"
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
        "stars": 16358,
        "forks": 3511,
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
        "stars": 8978,
        "forks": 1533,
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
        "stars": 45460,
        "forks": 12480,
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
        "stars": 12247,
        "forks": 2002,
        "openIssues": 136,
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
        "stars": 25298,
        "forks": 3422,
        "openIssues": 104,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-17T11:23:15Z"
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
        "stars": 20951,
        "forks": 5627,
        "openIssues": 1,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:55:21Z"
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
        "stars": 2989,
        "forks": 501,
        "openIssues": 15,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:34:50Z"
      }
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
        "stars": 23290,
        "forks": 5285,
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
        "stars": 20101,
        "forks": 5046,
        "openIssues": 368,
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
        "stars": 4925,
        "forks": 1289,
        "openIssues": 49,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
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
      ]
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
        "stars": 2418,
        "forks": 256,
        "openIssues": 41,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T14:42:11Z"
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
        "stars": 6045,
        "forks": 1169,
        "openIssues": 115,
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
        "stars": 4503,
        "forks": 710,
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
        "stars": 7646,
        "forks": 1235,
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
        "stars": 11637,
        "forks": 3601,
        "openIssues": 2822,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-17T18:12:40Z"
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
        "stars": 1572,
        "forks": 292,
        "openIssues": 51,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T13:06:59Z"
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
        "stars": 14820,
        "forks": 1391,
        "openIssues": 21,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-18T04:50:13Z"
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
        "stars": 7597,
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
        "stars": 652,
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
        "stars": 6422,
        "forks": 1894,
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
        "stars": 9520,
        "forks": 1044,
        "openIssues": 220,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T12:44:08Z"
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
        "stars": 10025,
        "forks": 2375,
        "openIssues": 2488,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T19:06:18Z"
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
        "stars": 4275,
        "forks": 505,
        "openIssues": 16,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T17:53:50Z"
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
        "stars": 6471,
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
        "stars": 9424,
        "forks": 1284,
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
        "stars": 22661,
        "forks": 3515,
        "openIssues": 0,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T15:00:24Z"
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
        "stars": 73298,
        "forks": 7584,
        "openIssues": 114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-19T21:44:06Z"
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
        "stars": 18794,
        "forks": 2848,
        "openIssues": 714,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T22:49:13Z"
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
        "stars": 4433,
        "forks": 678,
        "openIssues": 176,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2024-08-08T17:23:11Z"
      },
      "lifecycle": "stable"
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
        "stars": 67329,
        "forks": 27427,
        "openIssues": 2162,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-19T19:07:47Z"
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
        "stars": 28780,
        "forks": 8901,
        "openIssues": 436,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T17:41:51Z"
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
        "stars": 9110,
        "forks": 1335,
        "openIssues": 724,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T15:13:31Z"
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
        "stars": 25765,
        "forks": 3750,
        "openIssues": 989,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T15:15:34Z"
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
        "stars": 2961,
        "forks": 480,
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
        "stars": 6438,
        "forks": 1161,
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
        "stars": 3179,
        "forks": 385,
        "openIssues": 81,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-2-Clause",
        "pushedAt": "2026-09-18T01:30:29Z"
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
        "stars": 3425,
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
        "stars": 2281,
        "forks": 372,
        "openIssues": 104,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-19T11:20:06Z"
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
        "forks": 1368,
        "openIssues": 94,
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
        "stars": 1332,
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
        "stars": 50583,
        "forks": 4069,
        "openIssues": 22,
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
        "stars": 32986,
        "forks": 3180,
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
        "stars": 8226,
        "forks": 758,
        "openIssues": 136,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-20T08:34:24Z"
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
        "stars": 68152,
        "forks": 4557,
        "openIssues": 140,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:17:02Z"
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
        "stars": 4529,
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
        "stars": 5561,
        "forks": 1054,
        "openIssues": 3,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T15:12:49Z"
      }
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
        "stars": 8101,
        "forks": 1755,
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
        "stars": 9739,
        "forks": 1300,
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
        "stars": 10725,
        "forks": 2376,
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
        "stars": 12564,
        "forks": 3219,
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
        "stars": 27249,
        "forks": 4951,
        "openIssues": 120,
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
        "forks": 2708,
        "openIssues": 84,
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
        "stars": 24787,
        "forks": 3194,
        "openIssues": 71,
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
        "stars": 6468,
        "forks": 844,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T23:46:22Z"
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
        "stars": 67853,
        "forks": 11027,
        "openIssues": 55,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "CC0-1.0",
        "pushedAt": "2026-09-20T03:22:38Z"
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
        "stars": 73241,
        "forks": 5634,
        "openIssues": 692,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T19:07:21Z"
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
        "stars": 146742,
        "forks": 24539,
        "openIssues": 536,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:54:54Z"
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
        "stars": 185915,
        "forks": 13688,
        "openIssues": 695,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T17:23:11Z"
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
        "stars": 156605,
        "forks": 24693,
        "openIssues": 1080,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T18:46:19Z"
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
        "stars": 9259,
        "forks": 4121,
        "openIssues": 76,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-16T20:44:44Z"
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
        "stars": 61255,
        "forks": 6917,
        "openIssues": 27,
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
        "stars": 15105,
        "forks": 1502,
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
        "stars": 48649,
        "forks": 3467,
        "openIssues": 73,
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
        "stars": 13967,
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
        "stars": 65716,
        "forks": 7717,
        "openIssues": 761,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T01:14:39Z"
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
        "stars": 94332,
        "forks": 8330,
        "openIssues": 237,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:13:09Z"
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
        "stars": 30032,
        "forks": 6638,
        "openIssues": 8,
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
        "stars": 43901,
        "forks": 3579,
        "openIssues": 592,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:34:33Z"
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
        "stars": 63192,
        "forks": 4772,
        "openIssues": 65,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:19:50Z"
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
        "stars": 39059,
        "forks": 3957,
        "openIssues": 448,
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
        "stars": 82807,
        "forks": 15891,
        "openIssues": 80,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2024-07-29T19:34:21Z"
      },
      "lifecycle": "stable"
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
        "stars": 10090,
        "forks": 1013,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T02:29:51Z"
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
        "stars": 75240,
        "forks": 24784,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T06:16:49Z"
      }
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
        "stars": 55469,
        "forks": 25033,
        "openIssues": 1040,
        "archived": true,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
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
        "stars": 59237,
        "forks": 11614,
        "openIssues": 5207,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T19:12:16Z"
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
        "stars": 82754,
        "forks": 11432,
        "openIssues": 884,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T14:42:23Z"
      }
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
        "stars": 19913,
        "forks": 1479,
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
      ]
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
        "stars": 25282,
        "forks": 3610,
        "openIssues": 59,
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
        "stars": 117514,
        "forks": 26814,
        "openIssues": 18910,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:51:56Z"
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
        "stars": 25404,
        "forks": 6526,
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
        "stars": 20513,
        "forks": 2264,
        "openIssues": 213,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T05:38:44Z"
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
        "stars": 37852,
        "forks": 2977,
        "openIssues": 63,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T13:54:06Z"
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
        "stars": 92258,
        "forks": 10876,
        "openIssues": 350,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T05:16:20Z"
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
        "stars": 44844,
        "forks": 4177,
        "openIssues": 1163,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T20:50:43Z"
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
        "stars": 73636,
        "forks": 25125,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:16:48Z"
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
        "stars": 7271,
        "forks": 1361,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-18T02:51:45Z"
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
        "stars": 39033,
        "forks": 14971,
        "openIssues": 614,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-17T16:01:43Z"
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
        "stars": 166452,
        "forks": 34643,
        "openIssues": 2426,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T17:34:58Z"
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
        "stars": 5774,
        "forks": 434,
        "openIssues": 42,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-20T14:30:01Z"
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
        "stars": 38300,
        "forks": 2730,
        "openIssues": 265,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T07:57:28Z"
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
        "stars": 9897,
        "forks": 1107,
        "openIssues": 33,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T14:04:43Z"
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
        "stars": 60400,
        "forks": 7653,
        "openIssues": 329,
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
        "stars": 6533,
        "forks": 537,
        "openIssues": 26,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T12:37:19Z"
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
        "stars": 5298,
        "forks": 3137,
        "openIssues": 82,
        "archived": false,
        "disabled": false,
        "defaultBranch": "4.3",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-17T18:23:31Z"
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
        "stars": 6105,
        "forks": 824,
        "openIssues": 71,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "BSD-3-Clause",
        "pushedAt": "2026-09-20T13:42:26Z"
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
        "stars": 26881,
        "forks": 3840,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T18:03:13Z"
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
        "stars": 35724,
        "forks": 5427,
        "openIssues": 74,
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
        "stars": 10772,
        "forks": 587,
        "openIssues": 72,
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
        "stars": 13362,
        "forks": 1494,
        "openIssues": 118,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T19:29:13Z"
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
        "stars": 83962,
        "forks": 8687,
        "openIssues": 201,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T07:00:43Z"
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
        "stars": 182535,
        "forks": 9863,
        "openIssues": 641,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T19:10:23Z"
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
        "stars": 11115,
        "forks": 1098,
        "openIssues": 91,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-19T15:49:13Z"
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
        "stars": 9439,
        "forks": 1392,
        "openIssues": 19,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T21:06:40Z"
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
        "stars": 13854,
        "forks": 1653,
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
        "stars": 33733,
        "forks": 5500,
        "openIssues": 54,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T17:10:12Z"
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
        "stars": 6159,
        "forks": 888,
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
        "stars": 37827,
        "forks": 4293,
        "openIssues": 124,
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
        "stars": 31848,
        "forks": 4519,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-19T12:41:43Z"
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
        "stars": 107763,
        "forks": 20622,
        "openIssues": 161,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T05:43:45Z"
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
        "stars": 7807,
        "forks": 1159,
        "openIssues": 464,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T18:58:28Z"
      }
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
        "stars": 1684,
        "forks": 160,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-08-20T19:37:51Z"
      }
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
        "stars": 1952,
        "forks": 321,
        "openIssues": 22,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T11:52:53Z"
      }
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
        "stars": 5445,
        "forks": 335,
        "openIssues": 54,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T08:15:15Z"
      }
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
        "stars": 3934,
        "forks": 291,
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
      ]
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
        "stars": 538,
        "forks": 66,
        "openIssues": 102,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-20T00:00:37Z"
      }
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
        "stars": 3390,
        "forks": 312,
        "openIssues": 27,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "ISC",
        "pushedAt": "2025-08-21T10:03:22Z"
      }
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
        "stars": 94561,
        "forks": 12519,
        "openIssues": 743,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:16:47Z"
      }
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
        "stars": 2818,
        "forks": 208,
        "openIssues": 35,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T15:41:59Z"
      }
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
        "stars": 73431,
        "forks": 4807,
        "openIssues": 6311,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T19:13:32Z"
      }
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
        "stars": 83791,
        "forks": 7345,
        "openIssues": 155,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-15T16:16:24Z"
      }
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
        "stars": 8802,
        "forks": 804,
        "openIssues": 181,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T15:27:38Z"
      }
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
        "stars": 15429,
        "forks": 1415,
        "openIssues": 135,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T15:44:46Z"
      }
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
        "stars": 11115,
        "forks": 1098,
        "openIssues": 91,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-09-19T15:49:13Z"
      }
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
        "stars": 50952,
        "forks": 4849,
        "openIssues": 72,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-09-19T01:53:17Z"
      }
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
        "stars": 147027,
        "forks": 24032,
        "openIssues": 12285,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-09-20T16:24:05Z"
      },
      "bestFor": [
        "repository-level coding tasks",
        "terminal-driven code editing",
        "agentic debugging and refactoring"
      ],
      "avoidWhen": [
        "offline-only workflows",
        "tasks that do not need an autonomous coding agent"
      ]
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
        "stars": 79155,
        "forks": 8772,
        "openIssues": 1964,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T10:01:09Z"
      }
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
        "stars": 31361,
        "forks": 3248,
        "openIssues": 530,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-19T01:46:47Z"
      }
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
        "stars": 25271,
        "forks": 3007,
        "openIssues": 89,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T07:30:27Z"
      }
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
        "stars": 55316,
        "forks": 6903,
        "openIssues": 702,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-09T00:03:42Z"
      }
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
        "stars": 36565,
        "forks": 3890,
        "openIssues": 148,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T15:56:11Z"
      }
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
        "stars": 17825,
        "forks": 990,
        "openIssues": 44,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-14T19:29:02Z"
      }
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
        "stars": 7128,
        "forks": 1040,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-18T18:10:57Z"
      }
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
        "stars": 33738,
        "forks": 4434,
        "openIssues": 3627,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T19:09:45Z"
      }
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
        "stars": 14069,
        "forks": 1661,
        "openIssues": 39,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T14:05:30Z"
      }
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
        "stars": 27925,
        "forks": 3754,
        "openIssues": 627,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T16:05:12Z"
      }
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
        "stars": 6015,
        "forks": 429,
        "openIssues": 59,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T12:54:38Z"
      }
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
        "stars": 125501,
        "forks": 19504,
        "openIssues": 17998,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:27:11Z"
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
        "stars": 68876,
        "forks": 7460,
        "openIssues": 1391,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T18:14:09Z"
      }
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
        "stars": 97584,
        "forks": 10289,
        "openIssues": 116,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T03:32:22Z"
      }
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
        "stars": 63618,
        "forks": 11152,
        "openIssues": 165,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T14:54:26Z"
      }
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
        "stars": 11869,
        "forks": 764,
        "openIssues": 29,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T16:02:04Z"
      }
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
        "stars": 103648,
        "forks": 4434,
        "openIssues": 9148,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2026-09-19T11:38:43Z"
      }
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
        "stars": 67407,
        "forks": 4860,
        "openIssues": 942,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T10:12:27Z"
      }
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
        "stars": 16670,
        "forks": 2131,
        "openIssues": 30,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-19T13:13:19Z"
      }
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
        "stars": 1394,
        "forks": 228,
        "openIssues": 2,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "MIT",
        "pushedAt": "2026-06-22T17:46:43Z"
      }
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
        "stars": 6100,
        "forks": 388,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T16:21:37Z"
      }
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
        "stars": 16754,
        "forks": 1276,
        "openIssues": 40,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T09:57:54Z"
      }
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
        "stars": 6582,
        "forks": 2732,
        "openIssues": 260,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "NOASSERTION",
        "pushedAt": "2026-07-28T17:28:37Z"
      }
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
        "stars": 30680,
        "forks": 2678,
        "openIssues": 114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T05:42:08Z"
      }
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
        "stars": 69663,
        "forks": 4772,
        "openIssues": 241,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-18T23:23:30Z"
      }
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
        "stars": 107689,
        "forks": 13609,
        "openIssues": 213,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T16:03:24Z"
      }
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
        "stars": 205465,
        "forks": 60806,
        "openIssues": 1179,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T17:43:19Z"
      },
      "bestFor": [
        "self-hosted workflow automation",
        "API and service orchestration",
        "low-code business automations"
      ],
      "avoidWhen": [
        "hard real-time processing",
        "ultra-light embedded automation"
      ]
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
        "stars": 39759,
        "forks": 6242,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T21:37:33Z"
      }
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
        "stars": 38996,
        "forks": 2126,
        "openIssues": 398,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "AGPL-3.0",
        "pushedAt": "2026-09-20T07:09:04Z"
      }
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
        "stars": 59190,
        "forks": 7563,
        "openIssues": 744,
        "archived": false,
        "disabled": false,
        "defaultBranch": "develop",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:03:11Z"
      }
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
        "stars": 91064,
        "forks": 10791,
        "openIssues": 1465,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T13:31:09Z"
      }
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
        "stars": 326,
        "forks": 51,
        "openIssues": 8,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:13:09Z"
      }
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
        "stars": 17183,
        "forks": 913,
        "openIssues": 109,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T18:53:03Z"
      }
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
        "stars": 5288,
        "forks": 945,
        "openIssues": 13,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-14T02:46:36Z"
      }
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
        "stars": 4507,
        "forks": 1009,
        "openIssues": 31,
        "archived": false,
        "disabled": false,
        "defaultBranch": "master",
        "license": null,
        "pushedAt": "2025-11-10T17:06:44Z"
      }
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
        "stars": 45479,
        "forks": 3140,
        "openIssues": 10,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "GPL-3.0",
        "pushedAt": "2026-09-20T17:09:05Z"
      }
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
        "stars": 35296,
        "forks": 5245,
        "openIssues": 210,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-18T23:48:56Z"
      }
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
        "stars": 25056,
        "forks": 1723,
        "openIssues": 1027,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T17:59:13Z"
      }
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
        "stars": 119844,
        "forks": 11588,
        "openIssues": 1400,
        "archived": false,
        "disabled": false,
        "defaultBranch": "v8",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T17:53:37Z"
      }
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
        "stars": 1553,
        "forks": 63,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-08-19T11:20:36Z"
      }
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
        "stars": 1051,
        "forks": 116,
        "openIssues": 9,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": null,
        "pushedAt": "2026-04-11T22:18:08Z"
      }
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
        "stars": 62414,
        "forks": 5440,
        "openIssues": 114,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:43:56Z"
      }
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
        "stars": 895,
        "forks": 88,
        "openIssues": 4,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T09:23:39Z"
      }
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
        "stars": 1161,
        "forks": 100,
        "openIssues": 7,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-02-28T14:41:09Z"
      }
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
        "stars": 2380,
        "forks": 202,
        "openIssues": 5,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-06-19T07:20:29Z"
      }
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
        "stars": 72249,
        "forks": 13602,
        "openIssues": 545,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-19T18:21:38Z"
      }
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
        "stars": 37403,
        "forks": 2984,
        "openIssues": 711,
        "archived": false,
        "disabled": false,
        "defaultBranch": "canary",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-18T09:12:43Z"
      }
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
        "stars": 37433,
        "forks": 4645,
        "openIssues": 287,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-20T18:56:24Z"
      }
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
        "stars": 76488,
        "forks": 6990,
        "openIssues": 1249,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T17:51:56Z"
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
        "stars": 54499,
        "forks": 6281,
        "openIssues": 400,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-19T18:33:03Z"
      }
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
        "stars": 69226,
        "forks": 5706,
        "openIssues": 1057,
        "archived": false,
        "disabled": false,
        "defaultBranch": "dev",
        "license": "NOASSERTION",
        "pushedAt": "2026-09-20T18:27:38Z"
      }
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
        "stars": 42269,
        "forks": 5971,
        "openIssues": 1559,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2026-09-20T19:01:05Z"
      }
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
        "stars": 39759,
        "forks": 6242,
        "openIssues": 6,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-16T21:37:33Z"
      }
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
        "stars": 155076,
        "forks": 10122,
        "openIssues": 1125,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "MIT",
        "pushedAt": "2026-09-21T07:26:04Z"
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
        "stars": 1941,
        "forks": 330,
        "openIssues": 44,
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
        "forks": 173,
        "openIssues": 17,
        "archived": false,
        "disabled": false,
        "defaultBranch": "main",
        "license": "Apache-2.0",
        "pushedAt": "2025-12-15T11:02:30Z"
      }
    }
  ],
  "metadata": {
    "githubRefreshedAt": "2026-09-20T19:16:02.340872Z",
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
        "stars": 76453,
        "pushedAt": "2026-09-19T01:02:49Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 29971,
        "pushedAt": "2026-09-16T23:19:18Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 19695,
        "pushedAt": "2026-09-17T19:34:51Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "Robbyant/lingbot-map": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 17094,
        "pushedAt": "2026-09-08T06:31:41Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "PavelDoGreat/WebGL-Fluid-Simulation": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16649,
        "pushedAt": "2024-11-12T13:29:23Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "OpenRCT2/OpenRCT2": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 16240,
        "pushedAt": "2026-09-20T16:48:02Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "budtmo/docker-android": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 15873,
        "pushedAt": "2026-09-18T07:25:19Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 14734,
        "pushedAt": "2025-10-22T02:13:14Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "ytisf/theZoo": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 13400,
        "pushedAt": "2026-09-14T06:47:21Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "alicevision/Meshroom": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 12972,
        "pushedAt": "2026-09-18T15:16:27Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "jrouwe/JoltPhysics": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11566,
        "pushedAt": "2026-09-20T09:55:16Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "horsicq/Detect-It-Easy": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 11564,
        "pushedAt": "2026-09-20T17:24:14Z",
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 9696,
        "pushedAt": "2026-09-20T01:20:53Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "VAST-AI-Research/TripoSR": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6966,
        "pushedAt": "2026-06-04T07:11:09Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "cnr-isti-vclab/meshlab": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5839,
        "pushedAt": "2026-08-25T20:38:52Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "ArthurBrussee/brush": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 5090,
        "pushedAt": "2026-09-20T12:58:50Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 4746,
        "pushedAt": "2026-09-20T18:47:46Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 3518,
        "pushedAt": "2026-09-18T21:48:23Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 10570,
        "pushedAt": "2026-06-07T08:09:08Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "NVlabs/instant-ngp": {
      "fingerprint": {
        "decision": "accept",
        "score": 97.7,
        "stars": 17557,
        "pushedAt": "2026-02-02T12:32:34Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 18743,
        "pushedAt": "2026-05-30T07:11:00Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "pedramamini/awesome-yara": {
      "fingerprint": {
        "decision": "accept",
        "score": 93.4,
        "stars": 4274,
        "pushedAt": "2026-06-15T19:57:31Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "nuysoft/Mock": {
      "fingerprint": {
        "decision": "accept",
        "score": 88.4,
        "stars": 19572,
        "pushedAt": "2024-03-15T01:53:57Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 14206,
        "pushedAt": "2024-06-07T05:09:47Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "yfeng95/PRNet": {
      "fingerprint": {
        "decision": "accept",
        "score": 85.6,
        "stars": 5015,
        "pushedAt": "2022-07-25T23:50:26Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 12011,
        "pushedAt": "2025-07-29T02:30:55Z",
        "targets": [
          [
            "capability",
            "3d-reconstruction"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 6919,
        "pushedAt": "2024-05-13T00:39:07Z",
        "targets": [
          [
            "capability",
            "video-recording"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 4261,
        "pushedAt": "2024-07-10T07:53:06Z",
        "targets": [
          [
            "capability",
            "3d-human"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
        "stars": 9556,
        "pushedAt": "2024-06-17T11:35:26Z",
        "targets": [
          [
            "capability",
            "simulation"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "CalebFenton/simplify": {
      "fingerprint": {
        "decision": "review",
        "score": 71.2,
        "stars": 4665,
        "pushedAt": "2022-04-30T12:20:33Z",
        "targets": [
          [
            "capability",
            "malware-research"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "donnemartin/system-design-primer": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 370929,
        "pushedAt": "2026-09-15T01:10:09Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "clash-verge-rev/clash-verge-rev": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 145725,
        "pushedAt": "2026-09-20T14:10:35Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "nextlevelbuilder/ui-ux-pro-max-skill": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 129298,
        "pushedAt": "2026-09-19T00:58:38Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "rustdesk/rustdesk": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 124077,
        "pushedAt": "2026-09-20T10:21:15Z",
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "VoltAgent/awesome-design-md": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 116839,
        "pushedAt": "2026-07-31T12:32:42Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "ant-design/ant-design": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 99565,
        "pushedAt": "2026-09-20T16:02:38Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "nexu-io/open-design": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 97270,
        "pushedAt": "2026-09-20T18:17:06Z",
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "iluwatar/java-design-patterns": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 94708,
        "pushedAt": "2026-09-13T06:53:54Z",
        "targets": [
          [
            "capability",
            "design"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "GraphiteEditor/Graphite": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 27300,
        "pushedAt": "2026-09-20T14:30:22Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "rawgraphs/rawgraphs-app": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 9031,
        "pushedAt": "2026-08-24T11:02:18Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "visioncortex/vtracer": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 7078,
        "pushedAt": "2026-09-20T11:40:49Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "ecomfe/zrender": {
      "fingerprint": {
        "decision": "accept",
        "score": 100,
        "stars": 6307,
        "pushedAt": "2026-09-06T14:41:51Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "PixiEditor/PixiEditor": {
      "fingerprint": {
        "decision": "accept",
        "score": 98.9,
        "stars": 8047,
        "pushedAt": "2026-09-18T14:55:26Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "mbrlabs/Lorien": {
      "fingerprint": {
        "decision": "accept",
        "score": 88.4,
        "stars": 6802,
        "pushedAt": "2025-09-22T21:29:46Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
    },
    "exyte/Macaw": {
      "fingerprint": {
        "decision": "accept",
        "score": 81.2,
        "stars": 6045,
        "pushedAt": "2024-02-07T13:37:26Z",
        "targets": [
          [
            "capability",
            "vector-graphics"
          ]
        ]
      },
      "lastSeenAt": "2026-09-20T19:16:55.893619Z"
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
