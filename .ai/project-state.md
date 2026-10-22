# Project state

Status: active

## Working
- GitHub Stars are reconciled automatically into `catalog.json` at audit tier, preserving atomic validation and failure artifacts.
- Public portfolio scanning and recommendation reporting work; private-repository workflows run independently without publishing private project details.
- Catalog contains 980 entries at the verified 2026-10-18 checkpoint; the latest real Stars sync enumerated 846 accessible public favorites (830 previously cataloged, 16 admitted), and the catalog-quality issue reports 847/980 permanent GitHub IDs verified.
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

## Verified operational checkpoint (2026-10-18)
- [Star-list PR #113](https://github.com/dbrckk/star-list/pull/113): Production-OS integration-launch POSTs are never retried after ambiguous transport failure. The complete catalog CI and portfolio smoke passed.
- [PR #114](https://github.com/dbrckk/star-list/pull/114), [PR #115](https://github.com/dbrckk/star-list/pull/115) and [PR #116](https://github.com/dbrckk/star-list/pull/116) published automatic catalog quality audits on catalog changes, fixed the built-in GitHub-token event suppression with a reusable workflow, and added daily reconciliation. A real [Stars sync run #39118687501](https://github.com/dbrckk/star-list/actions/runs/39118687501) admitted one new favorite and completed its audit job; the issue then reported 961 catalog entries and zero review-grade findings.
- [Stars sync run #39121356632](https://github.com/dbrckk/star-list/actions/runs/39121356632) confirmed 827 accessible public stars, 827 cataloged, zero missing. This cannot attest inaccessible private favorites.
- Public discovery [issue #61](https://github.com/dbrckk/star-list/issues/61) covers 38/38 accessible public repositories; the separate private `Finders` and `tube` scans also passed on October 18. Four failed v2 and one terminal failed v3 integrations remain under the capacity-exhaustion safety hold. The [diagnostic workflow #39113139237](https://github.com/dbrckk/star-list/actions/runs/39113139237) checked all five failure task details.
- AI Dev Server PRs #337-#342 improved provider capacity guards, free-model failovers, Godot implementation token preservation and model-call ceilings. A passing CI workflow is not a completed, deployed, target-side integration.

## Verified post-admission and delivery improvements (2026-10-18)

- [Star-list PR #117](https://github.com/dbrckk/star-list/pull/117) merged as `a47f644`: reject stale quality issue publication if `main` advanced, and preserve evidence on failure. Exact PR-head and post-merge catalog validation, audit and repository standards passed.
- [Star-list PR #118](https://github.com/dbrckk/star-list/pull/118) merged as `ccce7e6`: weekly metadata refresh no longer publishes a pre-commit catalog snapshot. It rebases with bounded retries against concurrent Star admissions and calls the central SHA-guarded audit after a successful remote commit. Exact PR-head and post-merge catalog validation and repository standards passed; the next real weekly maintenance execution remains an independent operational check.
- [AI Dev Server PR #345](https://github.com/dbrckk/ai-dev-server/pull/345) (`bc046bf`) and [#346](https://github.com/dbrckk/ai-dev-server/pull/346) (`0736910`) merged: direct autonomous GitHub PR creation uses draft review state, and the Jumpy review canary requires independent exact published-SHA confirmation before declaring completion. Each passed seven required CI workflows on its exact PR head. The long-running post-merge mobile/multi-engine CI for the combined `main` remained in progress at the last check.
- Four historical v2 and one terminal v3 portfolio integration failure remain capacity-exhausted. No **new** real target-side OSS integration with exact-SHA draft PR and matching target CI has been verified. Do not confuse previous marker-file canaries or a small provider probe with that missing acceptance evidence.

## Public Stars identity backfill and security validation (2026-10-18)

- [PR #121](https://github.com/dbrckk/star-list/pull/121) merged: fail closed on a recycled GitHub `owner/name` with a different permanent ID, and reject mixed-ID pagination snapshots.
- [PR #122](https://github.com/dbrckk/star-list/pull/122) merged: weekly metadata refresh now captures numeric permanent GitHub IDs from the API responses it already makes and uses same-origin authenticated transport. This is not proof the weekly job has run since merging.
- [PR #123](https://github.com/dbrckk/star-list/pull/123) merged: authenticated candidate-discovery requests are restricted to the GitHub API host and use the shared cross-origin redirect protection.
- [PR #124](https://github.com/dbrckk/star-list/pull/124) merged: hourly Stars admission reuses the *full, timestamp-verified* public Stars snapshot to enrich legacy IDs without extra GitHub requests. A real [sync run #39136146189](https://github.com/dbrckk/star-list/actions/runs/39136146189) succeeded, admitted `github/opensource.guide` and populated **572 additional existing IDs**; the automatically chained issue audit succeeded.
- [PR #125](https://github.com/dbrckk/star-list/pull/125) merged: the [catalog quality issue #32](https://github.com/dbrckk/star-list/issues/32) now separately reports **829/962 verified permanent GitHub IDs** and **133 remaining name-only entries**, with 0 review-grade and 411 informational quality findings. [Audit workflow #39136539206](https://github.com/dbrckk/star-list/actions/runs/39136539206) passed.
- The subsequent [Stars run #39136471679](https://github.com/dbrckk/star-list/actions/runs/39136471679) checked **828/828 accessible public favorites**, 0 missing, 9 pages. This remains a public-accessible count only, not a statement about inaccessible private favorites.
- No portfolio integration is counted as delivered from these catalog/identity changes. The earlier four terminal v2 failures and one v3 failure remain under the Production-OS global dispatch stop; positive coding-provider capacity, real target code changes, draft PR head identity and target CI remain required.

## Verified portfolio-wide Skill Issue discovery (2026-10-18)

- [Star-list PR #131](https://github.com/dbrckk/star-list/pull/131) merged as `24e56f2`: add [Skill Issue](https://skill-issue.in/) as the 11th website resource, curate seven upstream GitHub skill references, match by domain and concrete repository metadata, and provide opt-in `--skills` recommendations. Skills are advisory-only and never auto-installed or sent to Production-OS.
- Exact PR-head `Validate catalog` and `Portfolio discovery live smoke` succeeded. Post-merge [Validate catalog](https://github.com/dbrckk/star-list/actions/runs/39154817166), [Repository standards](https://github.com/dbrckk/star-list/actions/runs/39154817913) and [Daily portfolio](https://github.com/dbrckk/star-list/actions/runs/39154817150) all succeeded.
- The live [public daily issue #61](https://github.com/dbrckk/star-list/issues/61) shows **41/41** public projects inspected and linked to the directory; **5** projects had **6** targeted skill recommendations; **0** new integrations launched. The two private per-repo workflows also use the shared `star-list/main` scanner, but their next runs must be observed separately before claiming live private adoption.
- [Repo-standards PR #12](https://github.com/dbrckk/repo-standards/pull/12) merged as `f2e6a2e`: shared AGENTS and repo-excellence guidance now considers relevant Skill Issue sources with full license/code review. Consumers pinned to the prior standards commit will not automatically update.
- Next: audit original `SKILL.md` and any invoked scripts at pinned revisions for each project before integrating or granting credentials. Neither directory listing nor working discovery guarantees installed, invoked or useful skills.

## Skill Issue rollout verified on 2026-10-18 (current)

- [Star-list PR #133](https://github.com/dbrckk/star-list/pull/133), merged `2e7a23a`: grew the **review-only** Skill Issue catalog from 7 to **19** curated references, each with an upstream `SKILL.md` path confirmed at a pinned commit. All exact-head catalog CI and live portfolio smoke checks passed, as did post-merge catalog validation, repository standards and public discovery.
- [PR #134](https://github.com/dbrckk/star-list/pull/134), merged `33777af`: only allowlisted framework names in structured `package.json` dependencies enrich advisory skill matching. README/package scripts and unrelated packages do not become matching evidence. The normal catalog recommender and Production-OS integration policy are unchanged. Exact-head validation and live smoke plus post-merge catalog/standards/public portfolio runs succeeded.
- [Actual post-merge public report #61](https://github.com/dbrckk/star-list/issues/61) generated 2026-10-18 21:32 UTC: **42/42** public repositories analyzed, Skill Issue linked for all **42**, and **8** projects with targeted pinned skill references, up from 5 immediately before manifest matching. Five native catalog-library suggestions over three projects remain merely candidate matches; **0 integration launches**, with global terminal-v3 capacity hold intact.
- [Real Stars run #39164085442](https://github.com/dbrckk/star-list/actions/runs/39164085442) inspected **846** accessible public favorites, recognized **830** existing and admitted **16**. [Catalog quality issue #32](https://github.com/dbrckk/star-list/issues/32) reports **980 repositories**, **847** verified permanent IDs, **133** name-only/unverified and **zero** review-grade findings. Private/inaccessible favorite coverage is not inferred.
- Only upstream file **existence and immutable source identity** were verified. The 19 SKILL.md bodies, bundled scripts, permissions and licenses have *not* been security audited or installed. Applying any skill to a target still requires independent source/terms review and target-side evidence.

## Verified native Skill Issue extension (2026-10-18)

- [Star-list PR #136](https://github.com/dbrckk/star-list/pull/136) merged as `a08aaed`: added pinned official Flutter and specialized Godot SKILL.md references. Strict root `pubspec.yaml` Flutter SDK dependency and GitHub's primary GDScript language now qualify review-only advice. Polyglot repositories can expose their separate React/Flutter frameworks without changing the existing repository integration ranker; duplicate manifest GETs are avoided. Exact-head catalog CI and read-only [portfolio smoke #39172713463](https://github.com/dbrckk/star-list/actions/runs/39172713463) passed, with **42/42** public repos inspected and **12** with targeted suggestions, up from 8.
- [PR #137](https://github.com/dbrckk/star-list/pull/137) merged as `112eae0`: added pinned sources from Google's `android/skills` (Compose performance, Play policy) and MIT `MSayib/roblox-dev-skill`. The matcher now supports pinned safe root SKILL.md files, distinguishes Luau from Lua and requires specific Compose labels rather than treating all Android projects as Compose. Exact-head catalog and [portfolio smoke #39173189524](https://github.com/dbrckk/star-list/actions/runs/39173189524) passed.
- All three post-merge jobs on `112eae0` succeeded: [Validate catalog #39173301348](https://github.com/dbrckk/star-list/actions/runs/39173301348), [Repository standards #39173302198](https://github.com/dbrckk/star-list/actions/runs/39173302198) and [daily portfolio #39173301377](https://github.com/dbrckk/star-list/actions/runs/39173301377). [Public issue #61](https://github.com/dbrckk/star-list/issues/61) was updated: **42/42** scanned, **42** Skill Issue directory references, **13** targets with **21** tailored skill suggestions; **zero** new Production-OS integrations. The catalog now includes **25** immutable-source-pinned skill references (19 original directory matches and six complementary platform-specific sources).
- **All 25 SKILL.md bodies and any referenced scripts remain unreviewed and uninstalled.** GitHub file existence and commit identity are not a security audit or evidence of target-side usage. The prior 4 v2 + 1 terminal v3 capacity failures and fleet-wide autonomous dispatch hold remain unchanged.

## Current priority
1. **Restore usable free AI execution capacity.** 2026-10-18 diagnosis verified 4 v2 and 1 failed final v3, all `capacity_exhausted`, with no delivered commit, reviewable PR or target CI. See `docs/PORTFOLIO_CAPACITY_RECOVERY.md`.
2. Qualify one zero-cost provider/model route with authenticated quota and a successful small inference probe before any operator-approved recovery; the final-v3 fleet stop is intentionally in effect. Do not reset markers, bypass caps or raise budgets.
3. Requalify current native candidates before retries (currently Ai-trading and vibecheck-android). Require real source edits, review and target CI before counting success.
4. Preserve daily public/private scans, Stars reconciliation, credential isolation and fail-closed diagnostics.

## Validation
- 2026-10-17: `Validate catalog`, `Repository standards` and `Sync GitHub Stars` have verified successful runs; prior `Portfolio discovery live smoke` and authenticated operator diagnosis also passed.
- Successful live smoke checks include read-only public discovery, offline single-flight dispatch, and authenticated redirect restrictions.
- Catalog identity uniqueness and schema remain enforced by the existing validation workflow.

## Last verified
- 2026-10-18 (980 catalog entries, 846 accessible public Stars reconciled in the latest verified admission; 847/980 permanent GitHub IDs verified and 133 name-only; 42/42 public projects scanned with 13 receiving 21 curated skill references; private-scanner success was last separately verified on October 18; zero new Production-OS integrations and terminal-v3 fleet stop remain in place).

## Verified 2026-10-21: per-project decisions for every catalogued source

- [PR #160](https://github.com/dbrckk/star-list/pull/160) merged as `aba361d`: consider relevant curated GitHub sources even when the automatic-dispatch admission gates exclude them. Sources with audit-only tiers, missing licenses, high integration complexity or insufficient score become review-only with explicit blockers; native dispatch gates remain intact. Exact-head Validate catalog and real public portfolio smoke passed.
- [PR #163](https://github.com/dbrckk/star-list/pull/163) merged as `65ae30f`: added [FastH3 Omni collection](https://huggingface.co/collections/FastVideo/fasth3-omni) as the 22nd website, referencing licensed and hardware-heavy video+audio models, not free unattended inference. Each active target's `source_assessment` now records a decision and reason for **every** GitHub catalog entry and curated website. A missing identity is a scan failure, and mutating dispatch is blocked.
- [Real post-merge workflow #39644170090](https://github.com/dbrckk/star-list/actions/runs/39644170090) succeeded; [public issue #61](https://github.com/dbrckk/star-list/issues/61) confirms **42/42** public projects and **42 complete per-source inventories**, **42,966 GitHub repository assessments (1,023 × 42)** and **924 website assessments (22 × 42)**. There were **216** GitHub matches (80 requiring policy review and 24 native-mode), **52** web references and **zero** new Production-OS dispatches. Post-merge Validate catalog and Repository standards also passed.
- Interpret "scan" precisely: this is a complete local metadata/relevance evaluation for every registered source, *not* fetching all third-party website pages, downloading model weights, executing SKILL.md files, or running 42,000 network requests. Hosted resources never become automatic dependencies.
- **Outstanding:** the earlier Production-OS integration fleet hold remains (four unresolved v2, one terminal v3). Restore genuinely available inference/worker capacity and prove exactly one licensed real target code change with reviewed PR and passing exact-SHA CI before resuming unattended launches. Do not claim that catalog recommendations have already been integrated.

<!-- AUTO:START -->
## Automatic repository state

Generated: 2026-10-22T12:21:06Z

### Git
- Branch: `main`
- Head: `c69ef2fdbe93`
- Commit date: 2026-10-22T08:20:55-04:00
- Commit: feat(discovery): expand evidence-backed generic source routing (#180)
- Tracked files: 304

### Recently changed files
- `.github/workflows/validate.yml`
- `RECOMMENDER.md`
- `scripts/catalog_domain_evidence.py`
- `scripts/portfolio_daily.py`
- `scripts/recommend.py`
- `scripts/report_domain_coverage.py`
- `scripts/test_other_domain_expansion.py`
- `scripts/test_catalog_domain_evidence.py`
- `.github/workflows/portfolio-scan-smoke.yml`
- `catalog.json`
- `catalog.schema.json`
- `scripts/admit_github_stars.py`
- `scripts/audit_catalog_quality.py`
- `scripts/infer_selection_guidance.py`
- `scripts/test_auto_stars_admission.py`
- `scripts/test_catalog_quality.py`
- `scripts/test_full_catalog_availability.py`
- `scripts/test_recommend.py`
- `scripts/test_verify_catalog_evidence.py`
- `scripts/validate_catalog.py`

### Project signals
- No common build descriptor detected

> Generated by dbrckk/repo-standards. Keep manual priorities and blockers outside the AUTO markers.
<!-- AUTO:END -->

## Verified checkpoint (2026-10-20, canonical identity and trends)

- [PR #148](https://github.com/dbrckk/star-list/pull/148) merged as `883ccf0`: updated three GitHub transfer names to canonical `prisma/orm`, `react/react`, and `react/react-native`, attached exact permanent IDs and rewired three inbound catalog relationships without dropping curation. The exact-head PR, [post-merge catalog validation](https://github.com/dbrckk/star-list/actions/runs/39483152224), [quality audit](https://github.com/dbrckk/star-list/actions/runs/39483152219), [Stars sync](https://github.com/dbrckk/star-list/actions/runs/39483152255), and [repository standards](https://github.com/dbrckk/star-list/actions/runs/39483154277) all passed.
- [PR #149](https://github.com/dbrckk/star-list/pull/149) merged as `42f59c5`: preserved the six historical data points per transferred repository under canonical keys and relabeled their prior health baselines with unchanged measurements; exact-head and [post-merge catalog](https://github.com/dbrckk/star-list/actions/runs/39483704311) and [standards](https://github.com/dbrckk/star-list/actions/runs/39483706050) checks passed.
- Fresh [quality issue #32](https://github.com/dbrckk/star-list/issues/32) confirms **1,013 total** catalog entries, **1,006 permanent GitHub IDs**, **7 unverified**: six deliberate duplicate/alias candidates with a canonical catalog row, plus inaccessible `Scottcjn/Rustchain`. Open [review issue #146](https://github.com/dbrckk/star-list/issues/146) tracks the remaining ambiguous cases. Do not auto-delete aliases or fabricate the last unavailable ID.
- [Real Stars sync #39483152255](https://github.com/dbrckk/star-list/actions/runs/39483152255) checked **879 accessible public Stars in nine API pages**, all 879 already cataloged, zero newly admitted and zero missing. This cannot prove coverage of inaccessible private Stars. The public [portfolio issue #61](https://github.com/dbrckk/star-list/issues/61) still reports 42/42 targets scanned and no confirmed new integrations.
- [Skill Issue source audit #39460419322](https://github.com/dbrckk/star-list/actions/runs/39460419322) passed for 25 pinned files (accessibility check only, not permission to execute). The fleet integration freeze stays in effect: four historical v2 failures and one terminal v3 failure require real provider capacity proof and operator review before any dispatch resumes.

Next priority: reconcile the six duplicates using immutable identities and curation-preserving reference migration, investigate Rustchain without guessing, then validate on the latest Stars scan and catalog audit. In parallel, restore Production-OS usable provider capacity before attempting a single compatible, licensed, exact-SHA target integration.

## Verified 2026-10-21: exhaustive discovery, worker publisher and GitHub CI

- [Star List PR #152](https://github.com/dbrckk/star-list/pull/152) merged as `1e822fb`. The live [portfolio workflow #39628513425](https://github.com/dbrckk/star-list/actions/runs/39628513425) succeeded: all **42/42 public targets** inspected, **106** qualified GitHub suggestions (including **14** native-mode matches across three projects), and **20** relevant website references. Full results are preserved in the artifact, not truncated to 3 GitHub / 2 websites / 2 skills. The [persistent issue #61](https://github.com/dbrckk/star-list/issues/61) shows the bounded preview. Relevant free/licensed-source discovery is distinct from adoption; private repositories retain isolated scans.
- The user-supplied `https://jupiterthewarlock.com/gameartstyle/` is recorded in `websites.json` as a separate, **unverified, reference-only** 14th website. Its live availability and media rights have not been independently verified. This does not authorize asset copying.
- [Production-OS model-authored source commit `06be764`](https://github.com/dbrckk/star-list/commit/06be764d654aa3ef2e3069d846df2f1583f81ef9) corrected `scripts/validate_websites.py` MCP `www.` handling. Automatic [trusted handoff #39622262664](https://github.com/dbrckk/star-list/actions/runs/39622262664) **failed correctly** because generic publisher changed unrelated executable file mode without changing blob. The offending branch's mode was repaired explicitly (new exact SHA `a1ac230`), then [PR #153](https://github.com/dbrckk/star-list/pull/153) passed target CI and merged as `2e0ff4a`. **Manual recovery does not certify autonomous retry success.**
- [AI Dev Server PR #370](https://github.com/dbrckk/ai-dev-server/pull/370) merged as `bc82897` after successful exact-commit jobs in all seven workflow groups (worker integration, security, resilience, Python CI, full Flutter/mobile and multi-engine). Generic Git publication now preserves original executable file modes from exact parent Git tree rather than forcing `100644`. Post-merge workflow completion and a fresh end-to-end worker handoff are separate verification steps.
- [Star List PR #155](https://github.com/dbrckk/star-list/pull/155) merged as `b42c4de`. Monolithic Repomix map exceeded its 1,500,000-byte threshold; excluding large structured snapshots **only from the generated architecture map** reduced it from **1,506,885** to **335,601 bytes**. Post-merge Repository standards and Validate catalog both passed. Actual catalog data remains tracked and scanned.
- **Outstanding:** [portfolio issue #61](https://github.com/dbrckk/star-list/issues/61) still shows **0 new integrations dispatched**, with **4 historical v2 failures and one terminal v3** requiring operator capacity verification; the safety stop has intentionally **not** been bypassed. Until a fresh, authorized Production-OS worker genuinely makes a licensed, compatible target edit with exact-SHA draft PR and target CI, describe automatic integration fleet as **still paused**, despite successful focused source-delivery evidence.

Next: independently validate repeatability of new publisher; inspect/read the existing terminal-v3 task and verified provider capacity before authorizing a bounded fleet resumption. Preserve GitHub credential isolation and never execute unreviewed Skill Issue scripts or gallery assets.
