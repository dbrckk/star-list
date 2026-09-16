# Discovery scoring and admission

This document describes the candidate evaluation implemented by `scripts/evaluate_candidates.py`.

It is separate from the recommendation engine. The recommender ranks repositories already present in `catalog.json` for a user task. Discovery evaluation decides how newly found repositories should be surfaced for human review.

## Scores used by discovery

A discovered repository enters evaluation with a `discoveryScore` produced by `scripts/discover_candidates.py`.

`evaluate_candidates.py` starts from that value, applies deterministic bonuses and penalties, clamps the result to `0..100`, and returns it as `evaluationScore`.

The five values in `scoreBreakdown` — `fit`, `activity`, `adoption`, `maturity`, and `maintenance` — are diagnostic dimensions. They explain candidate quality from different angles, but they are **not averaged together to produce `evaluationScore`**.

## Admission thresholds

The current thresholds are defined in code as:

```python
ACCEPT_THRESHOLD = 80.0
REVIEW_THRESHOLD = 55.0
```

In documentation form:

- score >= `80` -> `accept`
- score >= `55` and < `80` -> `review`
- score < `55` -> `reject`

There is one additional safety rule: a candidate with `low` evaluation confidence cannot be automatically classified as `accept`. If its score reaches the accept range, the decision is changed to `review` and the reason `low-confidence-cap` is added.

## Evaluation score adjustments

The evaluator begins with `discoveryScore` and then applies the following signals.

| Signal | Adjustment |
| --- | ---: |
| Missing push/activity date | -8 |
| Pushed within 90 days | +10 |
| Pushed within 365 days | +5 |
| Last push > 365 days | -8 |
| Last push > 730 days | -20 |
| License present | +5 |
| License missing | -10 |
| Strong text fit (`textFit >= 0.75`) | +8 |
| Zero text fit | -6 |
| Repository age >= 2 years | +4 |
| Repository age < 90 days | -3 |
| Latest release <= 180 days | +5 |
| Contributors >= 20 | +4 |
| Contributors <= 1 with >= 500 stars | -4 |
| Matching topics | +2 each, capped at +6 |
| Multiple matched catalog gaps | +3 per extra match, capped at +10 |
| Stars < 100 | -10 |
| Watchers >= 100 | +2 |
| Open-issue ratio > 20% when stars >= 500 | -5 |
| Open-issue ratio < 2% when stars >= 500 | +2 |
| GitHub Discussions enabled | +1 |
| Fork/star ratio >= 5% when stars >= 500 | +4 |
| Fork/star ratio < 0.5% when stars >= 500 | -3 |

After all adjustments, `evaluationScore` is rounded to one decimal place and constrained to the inclusive `0..100` range.

## Text fit

`textFit` measures how many matched gap targets have at least one word present in the repository name, description, or language string.

A target such as `machine-learning` is normalized into words before comparison. The final value is a ratio from `0.0` to `1.0`.

## Evaluation confidence

Confidence measures metadata completeness, not repository quality.

The evaluator checks ten metadata signals:

1. push date;
2. creation date;
3. license;
4. latest release publication date;
5. contributor count;
6. watcher count;
7. fork count;
8. open-issue count;
9. Discussions availability;
10. non-empty topics.

Confidence is assigned from the fraction of available signals:

- at least 80% -> `high`
- at least 50% -> `medium`
- below 50% -> `low`

The `low-confidence-cap` rule prevents sparse metadata from creating an automatic `accept` decision solely because the numeric score is high.

## Diagnostic score breakdown

Each component is independently bounded to `0..100`.

### `fit`

`fit` combines:

- text fit: up to 65 points;
- topic overlap: up to 20 points;
- additional matched catalog gaps: up to 15 points.

### `activity`

Base push-recency points are:

| Push age | Points |
| --- | ---: |
| <= 90 days | 70 |
| <= 365 days | 55 |
| <= 730 days | 35 |
| > 730 days | 10 |
| Missing | 0 |

Release recency adds 30 points for a release within 180 days or 15 points for a release within 365 days.

### `adoption`

Star contribution:

| Stars | Points |
| --- | ---: |
| >= 5000 | 55 |
| >= 1000 | 45 |
| >= 500 | 35 |
| >= 100 | 25 |
| >= 20 | 10 |
| < 20 | 0 |

Watcher contribution is +20 for at least 100 watchers, +10 for at least 20, and +5 for at least 5.

Fork ratio contributes +25 at >= 5%, +15 at >= 1%, or +5 when there is at least one fork.

### `maturity`

`maturity` can receive points from:

- license presence: +25;
- repository age: +10 to +25;
- contributor count: +10 to +30;
- Discussions enabled: +20.

### `maintenance`

`maintenance` starts at 50 and adjusts for contributor breadth and, for repositories with at least 500 stars, issue and fork ratios.

It rewards a broad contributor base, low issue load, and healthy fork ratio, while penalizing single-contributor risk, high issue load, and very low fork ratio.

## Decision output

Each evaluated repository includes the discovery data plus fields such as:

```json
{
  "evaluationScore": 84.0,
  "decision": "accept",
  "evaluationConfidence": "high",
  "scoreBreakdown": {
    "fit": 85.0,
    "activity": 100.0,
    "adoption": 80.0,
    "maturity": 90.0,
    "maintenance": 85.0
  },
  "reasons": [
    "active<=90d",
    "licensed",
    "strong-text-fit"
  ]
}
```

The output contract is defined in `schemas/discovery-evaluated.schema.json`.

## Memory and review behavior

After evaluation, `scripts/filter_discovery_memory.py` fingerprints candidates so unchanged `review` and `reject` rows can be suppressed on later discovery runs. Accepted candidates remain visible.

The filtered result is rendered by `scripts/render_discovery_issue.py`. The renderer displays decision, repository, score, confidence, stars, activity age, matched gaps, reasons, and the five diagnostic score components.

No decision automatically modifies the main catalog. Candidate admission remains a human review step.
