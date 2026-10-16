# Daily star-list integration for the full GitHub portfolio

Source of truth: `dbrckk/star-list/catalog.json`.

The workflow `.github/workflows/daily-portfolio-integration.yml` runs daily
at **03:37 UTC** and is also available through **Actions > Daily portfolio
star-list integration > Run workflow**. GitHub Actions schedules can be delayed
or skipped by GitHub, so "daily" is a configured cadence, not a real-time SLA.

## What it does

1. Enumerates **every accessible** repository owned by `dbrckk`,
   with pagination and duplicate removal. Includes `star-list` itself.
2. Inspects its GitHub metadata, README and one supported dependency manifest
   without downloading/executing third-party code.
3. Compares its actual profile with all catalog candidates.
4. Rejects audit-tier, archived, unsupported-license, paid, low-quality and
   high-complexity candidates before deciding that an integration is eligible.
5. Records each scanned target, including those with **no useful match**, in
   `portfolio-daily.json`, `portfolio-daily.md`, a retained Actions artifact
   and an updated GitHub issue.
6. If a qualified suggestion exists and a Production-OS **operator** secret is
   configured, submits up to **3** new tasks per scan (never more than 3 active
   portfolio integrations at once) to the existing managed-project API.
   Earlier high-budget failures reduce this to at most one launch per UTC day.
   A given target may receive at most **one** newly submitted integration per
   scanner run. Targets with existing `ACTIVE` or `REVIEW_REQUIRED` work
   receive no additional candidate until that work is resolved.
7. Uses stable tracking IDs derived from target + upstream repo, so repeat
   scans cannot create duplicate projects. A failed v1 may receive one bounded
   v2 retry; a failed v2 may receive one bounded **v3** retry for the **same**
   candidate. Any prior v3 marker permanently blocks additional automatic
   retries for that candidate. Failed targets stay quarantined from unrelated
   candidate launches until reviewed. Once that exact candidate's v3 recovery
   reaches `DONE`, its superseded v2 failure no longer counts as unresolved
   or blocks unrelated qualified tools. An active, failed, or review-pending
   v3 recovery does not clear the quarantine. If the previous v2 tool is
   now classified as reference-only or otherwise not native-eligible, or has
   already received its one v3 attempt, the target is no longer quarantined
   against *different* qualified native tools. Its historical failure remains
   visible and the global one-launch-per-UTC-day limit still applies.
8. Production-OS / ai-dev-server must actually inspect, implement and verify
   the integration in the target. A suggestion or queued task is NOT a
   completed integration. The managed project must produce a functional
   change and pass target CI before merge or deployment.

## Configuration

For **public** GitHub repositories, no extra GitHub secret is needed;
`GITHUB_TOKEN` supports reading the public portfolio and writing the
star-list review issue.

Private repositories are **never** written to the public star-list review issue.
The two known private projects (`Finders`, `tube`) use repository-scoped
daily workflows and retain their reports as private Actions artifacts.
Each private workflow scans only its own repository using its local
`GITHUB_TOKEN` and the public star-list catalog; no shared portfolio PAT
is necessary.

For **actual autonomous integrations**, configure a star-list Actions
repository secret:

- `PRODUCTION_OS_OPERATOR_TOKEN`: valid Production-OS **operator** API
  token. Store only as a GitHub Actions secret, never commit or paste it.
- The workflow sends this token **only** to
  `https://production-os1.onrender.com`, over HTTPS. Authenticated API requests
  reject redirects to other origins or insecure protocols, rather than
  forwarding bearer credentials to a new destination.
- Production-OS must be deployed, ready, and have an authenticated, qualified
  `ai-dev-server` worker with access to the target repositories and a working
  inference provider. Check worker status and actual PR/CI evidence there.

If the operator token is missing or Production-OS is unavailable, the scanner
still produces its report, but **does not claim** an integration has happened.
Transport or dispatch errors are recorded and the workflow fails visibly.

## Cost, load and promotion constraints

- Only open-source candidates with an eligible explicitly recognized SPDX
  license are considered. Verify upstream files and redistribution terms at
  implementation time; metadata alone is insufficient.
- Max 3 managed-project launches per daily run and up to three qualified candidates per
  target. All accessible repositories are still inspected on each run.
- If any v2 high-budget integration needs attention, **quarantine its target**
  from further automatic attempts and admit **at most one different project
  per UTC day**, only when no other portfolio integration is active. This
  avoids permanently freezing the entire portfolio while also preventing
  runaway retries or repeated work from push/schedule dispatches. Missing
  creation timestamps are treated conservatively as same-day launches.
- **Per-target single-flight protection:** candidate ranking never triggers
  simultaneous modifications of the same target. All suggestions remain in
  the report; only submission is deferred until active/review-pending work
  is resolved. The guard also applies after a successful dispatch within the
  current run, not just to the previously fetched Production-OS inventory.
- **Fleet-level queue protection:** at most three active portfolio integrations
  may run across all scans. Failed v2 tasks are **quarantined**, not counted as
  indefinitely active workers; while any remain unresolved, dispatch requires
  an idle fleet and permits at most one new or v3 recovery task per UTC day.
  Daily scanning and recommendations continue when no launch slots are
  available. The daily quota is calculated from timezone-aware timestamps
  normalized to **UTC**, not the date prefix returned by Production-OS.
  The public review issue reports the remaining launch slots and, when the
  failure throttle applies, the number of earlier launches on that UTC date.
  The `dispatch_status` value distinguishes a genuinely enabled dispatcher
  from a saturated UTC quota, active worker capacity, a read-only scan,
  unavailable Production-OS inventory or an incomplete repository scan.
  The authenticated Production-OS inventory must declare itself
  complete, contain valid unique v1/v2/v3 markers, valid target identities,
  timezone-aware creation dates, and known lifecycle states
  (`ACTIVE`, `REVIEW_REQUIRED`, `NEEDS_ATTENTION`, `DONE`).
  Unknown status or malformed inventory **fails closed** before dispatch.
- A qualified v2 integration requests a bounded **90,000-token** envelope
  through Production-OS's operator-only dashboard API using the explicit
  `launch_profile: portfolio-integration` option. Ordinary dashboard
  launches retain their original 30,000-token default and ignore caller
  budget fields for backwards compatibility. These are token caps,
  not a guarantee of successful code delivery or of provider availability.
  No paid provider is added or selected by this scanner.
- Exclude generic words and incompatible game engines from matching. Single-term
  suggestions must match a technical capability or use case. Cross-language
  adapter suggestions remain visible in the report, but are **never** sent to
  autonomous integration without a separate compatibility assessment.
- Reference applications, demo repositories and code-example collections
  are marked `reference-review`, even when their language matches the
  target. They remain discoverable but **never** enter automated integration.
  This also applies to catalogs whose best-for text describes studying
  examples rather than installing a runtime component.
- Same-language matches must also share a **concrete named capability** with
  the target to qualify as `native`. Generic overlap such as `workflows`
  or `data` produces `capability-review` instead: visible in the review,
  but not automatically dispatched. Usable native libraries rank first.
- Even native-language suggestions are only hypotheses: a managed worker must
  reject non-integrable toolchains and dependencies that cannot be used and
  validated in the existing target.
- Do not interpret a high matching score as proof of compatibility. The worker
  must check dependency compatibility, licenses, security, test/build results,
  and actual use of the new tool in source/runtime.
- **No automatic merge or production deployment** from this workflow.
  Changes require the target's real CI and existing branch/review rules.
- The default catalog excludes audit-tier favorites from automatic handoff.
  They remain listed in star-list and can be evaluated separately.
- No credentials from upstream tools are downloaded or executed in discovery.
  README text is only weak discovery context, never a worker instruction.

## Manual CLI

From `star-list`, with Python 3.12 and a valid GitHub API token:

```bash
GITHUB_TOKEN=... python scripts/portfolio_daily.py \
  --owner dbrckk --max-dispatch 0 \
  --output portfolio-daily.json --markdown portfolio-daily.md
```

`--max-dispatch 0` performs a scan only. Without
`PRODUCTION_OS_OPERATOR_TOKEN`, the scanner is read-only as well.

For operational verification, check **all** of: latest scheduled workflow
conclusion, `summary.inspected == summary.discovered`, number of submitted
projects, resulting Production-OS task status, committed target change,
successful target CI, and observed runtime usage.

## Limits and failures

GitHub may delay a scheduled job; missing GitHub API permissions may prevent
private repository discovery. Files above the scan size limit and missing
manifests are not downloaded. An individual repository read failure is
recorded as `scan-failed` and makes the workflow fail; it is never reported
as a successful complete scan. **Fail closed:** if any target cannot be
inspected or the catalog/owner discovery fails, no Production-OS inventory
request or integration launch is attempted, even if other repositories have
qualified candidates. The JSON/Markdown report remains available for triage
and `dispatch_status` states why launches were blocked. Unselected catalog matches remain available
for later review; not every third-party project is safe or useful to install.
