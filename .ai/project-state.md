# Project state

Status: active

## Working
- GitHub Stars are reconciled automatically into `catalog.json` at audit tier, preserving atomic validation and failure artifacts.
- Public portfolio scanning and recommendation reporting work; private-repository workflows run independently without publishing private project details.
- Catalog contains 942 entries on 2026-10-16; the current validation and Repository standards workflows have passed.
- Per-target single-flight dispatch and same-origin authenticated redirects have been merged (#80 and #81).
- Portfolio execution remains subject to strict worker capacity, deduplication, and UTC launch caps.

## Broken / blockers
- Public Stars API access does not guarantee discovery of inaccessible private stars; no total-private-stars completeness claim is made.
- Production-OS inventory has four unresolved historical v2 integrations (last report on 2026-10-16). No automatic integration was launched in that scan because one UTC-day launch slot had already been consumed.
- Dispatched work has not been established as functional until the target receives a real tested change and passes its own CI. Review Production-OS worker failures rather than increasing launch budgets.
- The 2026-10-09 Repository standards map-size failure is historical; later Repository standards workflow runs passed on 2026-10-16.

## Latest verified improvements (2026-10-16)
- PRs #90-#93 merged: strict Production-OS launch receipts; development-side Roblox Studio MCP classification; upstream TypeScript metadata correction; exclusion of catalog-declared substitute game engines from Roblox recommendations.
- Live discovery after PR #91 reported 38/38 accessible public repositories inspected, 15 with reviewable suggestions, 2 projects with native matches and 4 native candidates. The four historical v2 failures remained unresolved; no new integration was confirmed.
- Verify actual worker outputs and target-side CI before counting any Production-OS handoff as completed.

## New verified results (2026-10-16)
- PRs #100–#103 merged: redacted failure artifacts on API outages, daily operator diagnosis, Hermes/OpenCode catalog matching, and targeted read-only failure inventory.
- Production-OS PR #276 is live on Render and exposes opaque project IDs only to explicitly opted-in operators; default inventory remains redacted.
- Operator diagnosis [run 38965266598](https://github.com/dbrckk/star-list/actions/runs/38965266598) succeeded with 4/4 v2 task details. All remain `capacity_exhausted`, 1/3 attempts, zero commits, zero PRs and no target CI evidence.
- AI Dev Server PR #331 protects Production-OS and GitHub publishing credentials from Hermes/OpenCode subprocesses. This does not demonstrate available model inference capacity.

## Verified diagnosis and fleet safety (2026-10-17)
- PRs #105 and #106 merged: prevent new autonomous launches after terminal v3 failure and inspect failed v2/v3 tasks independently with an operator-only read endpoint.
- [Operator diagnosis run 39016621939](https://github.com/dbrckk/star-list/actions/runs/39016621939) passed with **4/4 historical v2 and 1/1 terminal v3 task details**. All five failures are `capacity_exhausted`, 1/3 attempts, zero commits/PRs and no target CI evidence.
- [Public portfolio report #61](https://github.com/dbrckk/star-list/issues/61) on 2026-10-17: 38/38 public repos inspected, 14 with reviewable suggestions, two targets with four native candidates; dispatch paused due final v3 failure, no new launch.
- Last verified private workflows for `Finders` and `tube`: scheduled runs 2026-10-16 passed. Current-day cadence is not asserted until a newer run completes.
- Hermes/OpenCode are already registered and security-filtered in AI Dev Server; their installation alone does not provide verified free inference capacity.

## Current priority
1. **Restore usable free AI execution capacity.** Operator diagnosis on 2026-10-16 verified that all four unresolved v2 jobs failed with `capacity_exhausted`, exactly 1/3 attempts each, without commits, PRs or target CI. See `docs/PORTFOLIO_CAPACITY_RECOVERY.md`.
2. Verify a real ready provider and worker before bounded v3 recovery; never increase or bypass the UTC/fleet and per-target launch caps to mask unavailable capacity.
3. Requalify current native candidates before retries (currently Ai-trading and vibecheck-android). Require real source edits, review and target CI before counting success.
4. Preserve daily public/private scans, Stars reconciliation, credential isolation and fail-closed diagnostics.

## Validation
- 2026-10-16: `Validate catalog`, `Portfolio discovery live smoke`, `Sync GitHub Stars` and `Repository standards` successful in relevant runs.
- Successful live smoke checks include read-only public discovery, offline single-flight dispatch, and authenticated redirect restrictions.
- Catalog identity uniqueness and schema remain enforced by the existing validation workflow.

## Last verified
- 2026-10-17 (942 catalog entries at the last checkpoint; 38/38 public repos inspected; four historical v2 and one final v3 integration failure; no target source delivery verified).

<!-- AUTO:START -->
## Automatic repository state

Generated: 2026-10-17T08:30:03Z

### Git
- Branch: `main`
- Head: `06e057565b69`
- Commit date: 2026-10-17T04:29:53-04:00
- Commit: docs(portfolio): document verified free model alternatives and conservative preflight (#108)
- Tracked files: 279

### Recently changed files
- `docs/PORTFOLIO_CAPACITY_RECOVERY.md`
- `.github/workflows/portfolio-scan-smoke.yml`
- `docs/PORTFOLIO_FAILURE_DIAGNOSTICS.md`
- `scripts/portfolio_failure_diagnostics.py`
- `docs/DAILY_PORTFOLIO_INTEGRATION.md`
- `scripts/portfolio_daily.py`

### Project signals
- No common build descriptor detected

> Generated by dbrckk/repo-standards. Keep manual priorities and blockers outside the AUTO markers.
<!-- AUTO:END -->
