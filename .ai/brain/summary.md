# Repo Brain

- Index mode: incremental
- Files indexed: 62
- Files reparsed this run: 4
- Symbols: 280
- Internal import edges: 37
- Impacted files: 7
- Selected tests: 3

## Languages
- python: 62 files

## Highest-density symbol files
- scripts/portfolio_daily.py: 26 symbols
- scripts/discover_candidates.py: 23 symbols
- scripts/recommend.py: 20 symbols
- scripts/update_cache_health_history.py: 19 symbols
- scripts/test_refresh_github_metadata.py: 16 symbols
- scripts/evaluate_candidates.py: 12 symbols
- scripts/refresh_github_metadata.py: 12 symbols
- scripts/star_import_pipeline.py: 11 symbols
- scripts/sync_github_stars.py: 10 symbols
- scripts/test_sync_github_stars.py: 10 symbols
- scripts/verify_catalog_evidence.py: 9 symbols
- scripts/portfolio_failure_diagnostics.py: 8 symbols
- scripts/test_verify_catalog_evidence.py: 8 symbols
- scripts/admit_github_stars.py: 7 symbols
- scripts/filter_discovery_memory.py: 7 symbols
- scripts/test_discovery_cache_stats.py: 7 symbols
- scripts/update_history.py: 7 symbols
- scripts/audit_agent_skill_sources.py: 6 symbols
- scripts/audit_catalog_quality.py: 5 symbols
- scripts/agent_skill_discovery.py: 4 symbols

## Agent routing
- Read impact.json first after project/change context.
- Use selected-tests.json before broad validation.
- Search lookup.json for symbol routing; ast-grep enrichment may provide exact ranges.
- Verify source before editing.

## ast-grep enrichment
- ast-grep outline: available
- AST index mode: incremental
- AST files reparsed this run: 4
- outline files retained: 62
- top-level items retained: 1176
- direct members retained: 11
- symbol shards: 25
- route named symbols via ast-routing.json, then fetch one ast-symbols/<initial>.json shard

