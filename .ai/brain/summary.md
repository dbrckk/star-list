# Repo Brain

- Index mode: incremental
- Files indexed: 41
- Files reparsed this run: 1
- Symbols: 137
- Internal import edges: 4
- Impacted files: 1
- Selected tests: 0

## Languages
- python: 41 files

## Highest-density symbol files
- scripts/discover_candidates.py: 23 symbols
- scripts/update_cache_health_history.py: 19 symbols
- scripts/evaluate_candidates.py: 12 symbols
- scripts/recommend.py: 11 symbols
- scripts/filter_discovery_memory.py: 7 symbols
- scripts/test_discovery_cache_stats.py: 7 symbols
- scripts/update_history.py: 7 symbols
- scripts/audit_catalog_quality.py: 5 symbols
- scripts/refresh_github_metadata.py: 5 symbols
- scripts/test_refresh_github_metadata.py: 5 symbols
- scripts/analyze_cache_health.py: 4 symbols
- scripts/find_replacements.py: 4 symbols
- scripts/health_score.py: 4 symbols
- scripts/validate_json_contract.py: 4 symbols
- scripts/detect_health_drift.py: 3 symbols
- scripts/render_discovery_issue.py: 3 symbols
- scripts/test_pipeline_integration.py: 3 symbols
- scripts/analyze_coverage.py: 2 symbols
- scripts/build_discovery_watchlist.py: 2 symbols
- scripts/render_health_issue.py: 2 symbols

## Agent routing
- Read impact.json first after project/change context.
- Use selected-tests.json before broad validation.
- Search lookup.json for symbol routing; ast-grep enrichment may provide exact ranges.
- Verify source before editing.

## ast-grep enrichment
- ast-grep outline: available
- AST index mode: incremental
- AST files reparsed this run: 1
- outline files retained: 41
- top-level items retained: 540
- direct members retained: 4
- symbol shards: 22
- route named symbols via ast-routing.json, then fetch one ast-symbols/<initial>.json shard

