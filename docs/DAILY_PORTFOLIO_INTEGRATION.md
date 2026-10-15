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
   configured, submits at most **3** new tasks per day to the existing
   `Production-OS` managed-project API.
7. Uses a stable request ID derived from target + upstream repo, so retries
   of the same suggestion cannot produce duplicate managed projects.
8. Production-OS / ai-dev-server must actually inspect, implement and verify
   the integration in the target. A suggestion or queued task is NOT a
   completed integration. The managed project must produce a functional
   change and pass target CI before merge or deployment.

## Configuration

For **public** GitHub repositories, no extra GitHub secret is needed;
`GITHUB_TOKEN` supports reading the public portfolio and writing the
star-list review issue.

Private repositories are **never** written to the public star-list review issue.\nThe two known private projects (`Finders`, `tube`) use repository-scoped\ndaily workflows and retain their reports as private Actions artifacts.\nEach private workflow scans only its own repository using its local\n`GITHUB_TOKEN` and the public star-list catalog; no shared portfolio PAT\nis necessary.\n\nFor **actual autonomous integrations**, configure a star-list Actions
repository secret:

- `PRODUCTION_OS_OPERATOR_TOKEN`: valid Production-OS **operator** API
  token. Store only as a GitHub Actions secret, never commit or paste it.
- The workflow sends this token **only** to
  `https://production-os1.onrender.com`, over HTTPS.
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
- Exclude generic words and incompatible game engines from matching. Single-term
  suggestions must match a technical capability or use case. Cross-language
  adapter suggestions remain visible in the report, but are **never** sent to
  autonomous integration without a separate compatibility assessment.
- Even native-language suggestions are only hypotheses: a managed worker must
  reject reference projects, non-integrable toolchains and dependencies that
  cannot be used and validated in the existing target.
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
as a successful complete scan. Unselected catalog matches remain available
for later review; not every third-party project is safe or useful to install.
