# Repo Brain

- Index mode: incremental
- Files indexed: 52
- Files reparsed this run: 1
- Symbols: 216
- Internal import edges: 10
- Impacted files: 1
- Selected tests: 0

## Languages
- python: 52 files

## Highest-density symbol files
- scripts/discover_candidates.py: 23 symbols
- scripts/portfolio_daily.py: 21 symbols
- scripts/update_cache_health_history.py: 19 symbols
- scripts/recommend.py: 16 symbols
- scripts/evaluate_candidates.py: 12 symbols
- scripts/test_refresh_github_metadata.py: 12 symbols
- scripts/star_import_pipeline.py: 11 symbols
- scripts/refresh_github_metadata.py: 10 symbols
- scripts/sync_github_stars.py: 8 symbols
- scripts/test_sync_github_stars.py: 8 symbols
- scripts/filter_discovery_memory.py: 7 symbols
- scripts/test_discovery_cache_stats.py: 7 symbols
- scripts/update_history.py: 7 symbols
- scripts/admit_github_stars.py: 6 symbols
- scripts/audit_catalog_quality.py: 5 symbols
- scripts/analyze_cache_health.py: 4 symbols
- scripts/find_replacements.py: 4 symbols
- scripts/health_score.py: 4 symbols
- scripts/infer_selection_guidance.py: 4 symbols
- scripts/validate_json_contract.py: 4 symbols

## Agent routing
- Read impact.json first after project/change context.
- Use selected-tests.json before broad validation.
- Search lookup.json for symbol routing; ast-grep enrichment may provide exact ranges.
- Verify source before editing.

## ast-grep enrichment
- ast-grep outline: available
- AST index mode: incremental
- AST files reparsed this run: 1
- outline files retained: 52
- top-level items retained: 841
- direct members retained: 9
- symbol shards: 24
- route named symbols via ast-routing.json, then fetch one ast-symbols/<initial>.json shard

