# Project state

Status: active

## Working
- GitHub Stars are reconciled automatically into `catalog.json` at audit tier, preserving atomic validation and failure artifacts.
- Public portfolio scanning and recommendation reporting work; private-repository workflows run independently without publishing private project details.
- Catalog contains 942 entries at the 2026-10-17 checkpoint; GitHub Stars sync, Validate catalog and Repository standards have successful verified runs.
- Per-target single-flight dispatch and same-origin authenticated redirects have been merged (#80 and #81).
- Portfolio execution remains subject to strict worker capacity, deduplication, and UTC launch caps.

## Broken / blockers
- Public Stars API access does not guarantee discovery of inaccessible private stars; no total-private-stars completeness claim is made.
- Production-OS has four unresolved v2 failures and one terminal v3 recovery failure, all `capacity_exhausted` in the 2026-10-17 operator diagnosis; autonomous launches are paused pending positive model-capacity proof and operator review.
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

## Provider and agent execution hardening (2026-10-17)
- Star-list [PR #108](https://github.com/dbrckk/star-list/pull/108) documents conservative Cloudflare Workers AI and Pollinations free-tier options and mandates positive authenticated capacity and a small non-mutating inference probe before retries.
- AI Dev Server [PR #333](https://github.com/dbrckk/ai-dev-server/pull/333) merged: provider keys inherited by Hermes/OpenCode/Codex cannot persist in subprocess stdout/stderr tails. The exact PR head ultimately passed **all seven** CI workflows including the mobile build.
- AI Dev Server [PR #334](https://github.com/dbrckk/ai-dev-server/pull/334) merged: Hermes uses documented one-shot JSONL terminal results and Codex must show `turn.completed`; zero-exit without proof is no longer success. Core CI, security/resilience and Production-OS integration checks passed on the reconciled PR head; additional long mobile/benchmark jobs were still in progress when last observed.
- [Star-list PR #111](https://github.com/dbrckk/star-list/pull/111) merged: trusted scheduled and hourly fallback scans now skip redundant full re-scans when a current UTC-day report was already published. Manual dispatch remains possible. The latest post-merge daily scan succeeded with 38/38 repositories and zero new integrations.
- [AI Dev Server PR #335](https://github.com/dbrckk/ai-dev-server/pull/335) merged as `b0cd423`: optional, opt-in Workers Free `@cf/zai-org/glm-4.7-flash` code-model fallback, with GitHub secret isolation from external coding agents. All seven exact-PR-head checks passed, including mobile and multi-engine CI. Fallback remains **disabled until a verified Workers Free account, scoped key and variables are configured**. No authenticated Cloudflare inference or sustained model capacity has been verified and terminal-v3 fleet stop remains active.
- [GitHub Stars run 39002112723](https://github.com/dbrckk/star-list/actions/runs/39002112723) on October 17 checked **804/804 accessible public favorites** (9 pages; no uncataloged stars). This does not verify inaccessible private stars. Public discovery continues at 38/38 with 14 projects showing suggestions; no integration is counted complete.

## Current priority
1. **Restore usable free AI execution capacity.** 2026-10-17 diagnosis verified 4 v2 and 1 failed final v3, all `capacity_exhausted`, with no delivered commit, reviewable PR or target CI. See `docs/PORTFOLIO_CAPACITY_RECOVERY.md`.
2. Qualify one zero-cost provider/model route with authenticated quota and a successful small inference probe before any operator-approved recovery; the final-v3 fleet stop is intentionally in effect. Do not reset markers, bypass caps or raise budgets.
3. Requalify current native candidates before retries (currently Ai-trading and vibecheck-android). Require real source edits, review and target CI before counting success.
4. Preserve daily public/private scans, Stars reconciliation, credential isolation and fail-closed diagnostics.

## Validation
- 2026-10-17: `Validate catalog`, `Repository standards` and `Sync GitHub Stars` have verified successful runs; prior `Portfolio discovery live smoke` and authenticated operator diagnosis also passed.
- Successful live smoke checks include read-only public discovery, offline single-flight dispatch, and authenticated redirect restrictions.
- Catalog identity uniqueness and schema remain enforced by the existing validation workflow.

## Last verified
- 2026-10-17 (942 catalog entries at the last checkpoint; 38/38 public repos inspected; four historical v2 and one final v3 integration failure; no target source delivery verified).

<!-- AUTO:START -->
## Automatic repository state

Generated: 2026-10-17T15:27:42Z

### Git
- Branch: `main`
- Head: `b5ee5bdaeee3`
- Commit date: 2026-10-17T11:27:33-04:00
- Commit: fix(portfolio): prevent duplicate Production-OS launch POSTs after uncertain responses (#113)
- Tracked files: 279

### Recently changed files
- `.github/workflows/portfolio-scan-smoke.yml`
- `docs/DAILY_PORTFOLIO_INTEGRATION.md`
- `scripts/portfolio_daily.py`
- `catalog.json`
- `docs/PORTFOLIO_CAPACITY_RECOVERY.md`
- `.github/workflows/daily-portfolio-integration.yml`

### Project signals
- No common build descriptor detected

> Generated by dbrckk/repo-standards. Keep manual priorities and blockers outside the AUTO markers.
<!-- AUTO:END -->
