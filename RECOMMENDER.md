# Recommendation engine

Use `scripts/recommend.py` to rank repositories from `catalog.json` for a concrete task.

## Examples

```bash
python scripts/recommend.py "xauusd backtesting risk execution" --top 8
python scripts/recommend.py "android vector animation" --top 6
python scripts/recommend.py "autonomous coding agent memory observability" --top 8
python scripts/recommend.py "trading ml alpha" --cap machine-learning --cap alpha --json
```

The recommender also inspects `stacks.json` and returns the closest predefined stack when one matches the task.

## Selection score

The selection score is task-specific. It is different from:

- the repository quality score stored in `catalog.json`;
- the health score produced by `scripts/health_score.py`;
- the discovery `evaluationScore` used to review newly found repositories.

The selection score combines:

- required capability match;
- inferred or forced domain match;
- lexical/task match;
- `bestFor` match;
- repository quality score;
- tier bonus;
- GitHub activity adjustment;
- repository health contribution;
- recent trend contribution from `history.json`;
- `avoidWhen` penalties.

If no `--cap` is supplied, lexical relevance receives extra weight.

## Constraint filters

The recommender can enforce technical constraints before scoring:

```bash
python scripts/recommend.py "android vector animation" --platform android --max-resource medium
python scripts/recommend.py "local coding agent" --self-hosted --max-complexity medium
python scripts/recommend.py "python trading backtest" --language python --cap backtesting --json
python scripts/recommend.py "security scanner" --domain cybersecurity --exclude-cap offensive
python scripts/recommend.py "agent runtime" --cap agents --cap memory --require-all-caps --min-score 40
```

Supported options:

| Option | Meaning |
| --- | --- |
| `--cap VALUE` | Desired capability; repeatable. |
| `--require-all-caps` | Reject repositories missing any requested capability. |
| `--exclude-cap VALUE` | Excluded capability; repeatable. |
| `--domain VALUE` | Force a domain instead of relying only on query inference; repeatable. |
| `--top N` | Maximum number of recommendations; default 5. |
| `--min-score N` | Minimum positive selection score. |
| `--platform VALUE` | Required platform; repeatable. |
| `--language VALUE` | Required language; repeatable. |
| `--self-hosted` | Require `selfHosted: true`. |
| `--include-archived` | Allow archived or disabled repositories. |
| `--max-resource low|medium|high` | Maximum resource level. |
| `--max-complexity low|medium|high` | Maximum integration complexity. |
| `--json` | Emit structured JSON instead of the human-readable ranking. |

Repeated platform/language filters are conjunctive: the repository must contain every requested value.

## Domain inference

When `--domain` is not provided, common query terms are mapped to catalog domains. Examples include `ai`/`agent`, `memory`/`rag`, `android`/`mobile`, `trading`/`quant`/`xauusd`, `security`/`pentest`, `ml`/`data`, and `devops`/`infra`.

Explicit `--domain` values replace inferred domains for that run.

## Output

Human-readable output includes the repository name, selection score, catalog quality score, tier, concise reasons, selected `bestFor` entries, complements, and an optional suggested stack.

JSON output additionally exposes inferred domains, requested capabilities, constraints, filter diagnostics, health information, and the recommended stack.

Example:

```bash
python scripts/recommend.py "local coding agent" --self-hosted --json
```

For the discovery candidate admission model, see `docs/DISCOVERY_SCORING.md`.
