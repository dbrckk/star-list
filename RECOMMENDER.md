# Recommendation engine

Use `scripts/recommend.py` to rank repositories from `catalog.json` for a concrete task.

Examples:

```bash
python scripts/recommend.py "xauusd backtesting risk execution" --top 8
python scripts/recommend.py "android vector animation" --top 6
python scripts/recommend.py "autonomous coding agent memory observability" --top 8
python scripts/recommend.py "trading ml alpha" --cap machine-learning --cap alpha --json
```

The selection score combines:
- capability match
- domain match
- lexical/task match
- `bestFor` match
- repository quality score
- tier bonus
- `avoidWhen` penalties

This selection score is task-specific and is different from the repository quality score in `catalog.json`.

The engine also inspects `stacks.json` and returns the closest predefined stack when one matches the task.


## Constraint filters

The recommender can enforce technical constraints:

```bash
python scripts/recommend.py "android vector animation" --platform android --max-resource medium
python scripts/recommend.py "local coding agent" --self-hosted --max-complexity medium
python scripts/recommend.py "python trading backtest" --language python --cap backtesting --json
```

Supported filters:
- `--platform`
- `--language`
- `--self-hosted`
- `--max-resource low|medium|high`
- `--max-complexity low|medium|high`

These filters are applied before task scoring.
