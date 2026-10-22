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

### Dedicated game-production stacks

The catalog now contains two additional curated combinations alongside the
general-purpose **Game Production** stack:

- **Roblox Studio Agent Production** uses a Roblox/Luau knowledge base, an
  instrumented Studio playtest connector and an agent-assisted building
  workflow. Authoring requires Roblox Studio on a supported desktop; review
  third-party agent edits and AGPL-3.0 obligations before deployment.
- **Godot Gameplay and VFX** combines the Godot engine, official game
  demonstration projects and agent-assisted Godot tooling. Verify each
  shader, animation and gameplay feature in the real engine.

```bash
python scripts/recommend.py "roblox studio luau playtesting agent" --json
python scripts/recommend.py "godot gameplay shaders vfx" --json
```

These are **tool recommendations**, not runnable game templates or guarantees
of AAA-level output. As with all predefined stacks, the engine only shows a
stack when every member passes the requested hard constraints.

## External website references (opt-in)

Use [the 27-site directory](WEB_RESOURCES.md) to discover website
inspiration, React components, motion references, 3D/shader examples or
hosted builders alongside GitHub repositories.

```bash
python scripts/recommend.py "3d scroll animation website" --websites --top-websites 10
python scripts/recommend.py "react ui animation" --websites --json
python scripts/recommend.py "any topic" --websites --rank-all-websites --top-websites 200 --json
```

With `--websites`, JSON contains a separate `websiteRecommendations`
array with HTTPS links, type, free/freemium access expectations,
`reuse` guidance, and a relevance score. Every site is marked
`integrationEligible: false`: a web gallery or paid service must not
be dispatched as a GitHub dependency. The normal repository
`recommendations` and `recommendedStack` are unchanged.

`--rank-all-websites` also ranks websites with no matching signals (zero score).
Without that opt-in, unrelated sites remain hidden to avoid noisy results.
Every web resource is reference-only and never auto-integrated.

`--top-websites N` limits interactive CLI output (default 5); the daily portfolio scanner evaluates all curated sites without a top-N cap and admits sparse game-project baseline references as review-only. Specialist NPC, narrative and 3D providers require a project-metadata match.
Repository-only technical hard filters (such as `--language`, `--platform`
or `--self-hosted`) do not establish compatibility or code licensing
for these external reference pages.

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

## Complete catalog availability (default)

**Every GitHub entry is immediately discoverable and rankable.** The catalog
uses four score tiers: `core`, `recommended`, `specialized`, and `indexed`.
`indexed` means cataloged with automatically collected metadata; it is not an
approval queue. Newly imported GitHub Stars enter as `indexed` and are
searchable from admission. All items can be assessed by any portfolio project
without waiting for a manual tier promotion.

For an exhaustive, inspectable recommendation set:

```bash
python scripts/recommend.py "youtube video automation" --top 2000 --websites --rank-all-websites --top-websites 200 --json
```

Without explicit filters, `diagnostics.eligible` equals
`diagnostics.catalogSize`; `--top` only limits the number returned.
Task relevance and selection score do **not** certify runtime compatibility,
security, licence or quality.

The recommender exposes `availableForDiscovery: true` for each returned
GitHub entry. `rankingReviewGates` reports archived or disabled upstream
projects, and `metadataReviewGates` reports unresolved licence or hosting
details. `reviewRequired` marks factual follow-up needs, **not**
a hold on indexing, scanning or recommendations.
`automaticIntegrationApproved: false` means the recommender does not
authorize installation on its own. The production portfolio scanner evaluates
separate safeguards before any mutating integration.

Legacy `--include-audit`/`--exclude-audit` flags remain accepted as aliases
for `--include-indexed`/`--exclude-indexed`, respectively. They no longer
refer to an `audit` catalog tier. Users can explicitly filter by domain,
platform, language, costs, complexity or upstream activity without altering
default full-catalog coverage.

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
| `--min-score N` | Optional minimum selection score (no default threshold). |
| `--platform VALUE` | Required platform; repeatable. |
| `--language VALUE` | Required language; repeatable. |
| `--self-hosted` | Require `selfHosted: true`. |
| `--include-archived` | Explicitly confirm the default inclusive ranking. |
| `--exclude-archived` | Filter out archived or disabled repositories. |
| `--include-indexed` | Explicitly include indexed references (already default). |
| `--exclude-indexed` | Optional filter for indexed references (does not delete them). |
| `--rank-all-websites` | With `--websites`, rank every website, even zero-match entries. |
| `--max-resource low|medium|high` | Maximum resource level. |
| `--max-complexity low|medium|high` | Maximum integration complexity. |
| `--json` | Emit structured JSON instead of the human-readable ranking. |

Repeated platform/language filters are conjunctive: the repository must contain every requested value.

### Distinguishing rankability from metadata trust

Every repository remains searchable even when some metadata is unknown. In JSON,
`metadataReviewGates` explains unresolved GitHub licence metadata or
`selfHosted` values such as `unknown` and `partial`; these are not silently
converted into `true` or `false`. The existing `rankingReviewGates` continue
to distinguish archived and disabled upstream projects. The `indexed`
tier itself is not a review blocker. `reviewRequired` is true if *either*
group reports an actual source-level finding.

`diagnostics.metadata` counts unverified self-hosting, unresolved licences
and entries requiring review across **all ranked results**, not just `--top`.
For detailed findings, run `python scripts/audit_catalog_quality.py`.

Stack selection now needs a recognizable name/task-specific match and
compatible domain. Generic shared words in a stack's warnings or usage notes
cannot make it a valid recommendation (for example, an AI/video task does
not imply a Roblox Studio or autonomous coding stack). Stack and relation
results are *advisory*, not proof of approved or safe integration.

### Evidence-based metadata verification

The catalog keeps original `unknown` / `partial` self-hosting values
rather than guessing. Use the bounded GitHub evidence auditor for individual
sources or rotating batches:

```bash
python scripts/verify_catalog_evidence.py --repo activepieces/activepieces --report-out /tmp/evidence.json
python scripts/verify_catalog_evidence.py --limit 15 --batch-index 0 --report-out /tmp/evidence.json
python scripts/validate_json_contract.py schemas/metadata-evidence.schema.json /tmp/evidence.json
```

The daily **Review uncertain catalog metadata** GitHub workflow selects a
rotating batch of sources with **missing or problematic factual metadata**
(archived/disabled, unresolved licences or unverified hosting). Being `indexed`
alone never places a project in an approval queue. This evidence report
does not block discovery, ranking or portfolio evaluation. Normal execution is **read-only**. The
auditor checks GitHub repository identity, records immutable Git blob hashes,
and validates root licence signatures. Explicitly scoped or mixed licensing
(e.g. a root MIT licence excluding enterprise directories) remains flagged
for review and cannot be automatically promoted.

A root Compose configuration produces a *deployment candidate*, not a
`selfHosted=true` assertion. It can require external paid infrastructure,
secrets, resources or non-open-source components. An unresolved GitHub SPDX
claim alone is insufficient to auto-approve a whole repository.

Only after reviewing the licences and report, an operator may opt in with
`--apply` to save a clearly verified root licence to `catalog.json`.
An ID mismatch or an API failure prevents writing the entire batch. The
auditor does not certify the licensing of every embedded component, and
GitHub rate-limit errors must be retried with an authorized API token.

### Constraint-safe relations and stacks

The same hard filters used for the main recommendations also apply to linked alternatives,
complementary tools and predefined stacks. A curated relationship cannot override a
requested platform, language, capability exclusion, self-hosting requirement, resource
limit or complexity limit. Audit/inactive entries remain outside inferred
links and predefined stacks, even while they appear in the full ranking.

- An ineligible curated link is removed. The engine can infer an eligible replacement when available.
- A predefined stack is only displayed when **all** of its component repositories are eligible.
  When no complete stack is compatible, `recommendedStack` is `null` in JSON output.
- `--min-score` determines which repositories appear as primary recommendations; related
  tools still honor the hard filters, but need not individually meet the query-specific
  relevance threshold.
- Audit/archived entries can be inspected in the primary ranking but remain
  excluded from inferred relations and predefined stacks. Ranking does not grant
  permission to install or reuse a dependency.

Domain inference also recognizes `roblox`, `godot` and `luau` as game-development queries.

## Domain inference

When `--domain` is not provided, common query terms are mapped to catalog domains. Examples include `ai`/`agent`, `memory`/`rag`, `android`/`mobile`, `trading`/`quant`/`xauusd`, `security`/`pentest`, `ml`/`data`, and `devops`/`infra`.

A generic "AI" token does not inject the coding-agent domain when
other specific domains (such as video, writing, or marketing) are detected,
unless the query explicitly mentions coding, development, or agents.

Explicit `--domain` values replace inferred domains for that run.

## Output

Human-readable output includes the repository name, selection score, catalog quality score, tier, concise reasons, selected `bestFor` entries, complements, and an optional suggested stack.

JSON output additionally exposes inferred domains, requested capabilities, constraints, filter diagnostics, health information, and the recommended stack.

Example:

```bash
python scripts/recommend.py "local coding agent" --self-hosted --json
```

For the discovery candidate admission model, see `docs/DISCOVERY_SCORING.md`.
