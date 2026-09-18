# Repo Brain

- Files indexed: 39
- Symbols: 130
- Internal import edges: 4

## Languages
- python: 39 files

## Highest-density symbol files
- scripts/discover_candidates.py: 22 symbols
- scripts/update_cache_health_history.py: 19 symbols
- scripts/evaluate_candidates.py: 12 symbols
- scripts/recommend.py: 11 symbols
- scripts/filter_discovery_memory.py: 7 symbols
- scripts/test_discovery_cache_stats.py: 7 symbols
- scripts/update_history.py: 7 symbols
- scripts/test_refresh_github_metadata.py: 5 symbols
- scripts/analyze_cache_health.py: 4 symbols
- scripts/find_replacements.py: 4 symbols
- scripts/health_score.py: 4 symbols
- scripts/refresh_github_metadata.py: 4 symbols
- scripts/validate_json_contract.py: 4 symbols
- scripts/detect_health_drift.py: 3 symbols
- scripts/render_discovery_issue.py: 3 symbols
- scripts/test_pipeline_integration.py: 3 symbols
- scripts/analyze_coverage.py: 2 symbols
- scripts/build_discovery_watchlist.py: 2 symbols
- scripts/render_health_issue.py: 2 symbols
- scripts/test_discovery_cache.py: 2 symbols

## Agent routing
- Search lookup.json first for direct symbol-to-file routing.
- Use symbols.json only when broader symbol metadata is needed.
- Use code-graph.json to inspect likely internal import relationships.
- Use imports.json when a changed file crosses module boundaries.
- Treat graph edges as static hints; verify source before editing.
