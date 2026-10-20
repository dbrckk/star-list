# Automatic GitHub Stars synchronization

The public GitHub Stars of **dbrckk** are synchronized into `catalog.json`
hourly at approximately **minute 11** (UTC), and the workflow can be launched using
**Actions → Sync GitHub Stars → Run workflow**.

## Admission policy

All accessible, publicly starred repositories are eligible for **automatic
catalog inclusion**, even when archived, inactive or missing clear license
terms. Admission does not mean the software has been verified or endorsed.

The workflow:
1. Fetches all accessible Stars (100 per page) and fails if pagination
   or API responses cannot be completed.
2. Reconciles case-insensitive repository names and permanent GitHub IDs
   to avoid duplicates and recognize transfers.
3. Fetches full GitHub metadata for each genuinely missing repository.
   It also retains the complete public Stars snapshot with permanent IDs,
   then **enriches old catalog entries from those already-fetched IDs**.
   No additional GitHub API call is needed for the identity backfill.
   The manifest timestamp, full list and new-Star review must agree before
   admission writes anything.
4. Generates a schema-compatible catalog entry with topic-based
   categorization, factual metadata and conservative defaults.
5. Assigns **`tier: audit`**, **`score: 6.0`** and inferred guidance to
   newly added entries. License and suitability remain unverified.
6. Validates the complete candidate catalog before atomic replacement.
7. Commits `catalog.json` to `main`, then closes the previous review issue
   when all accessible Stars have been accounted for.
8. Publishes synchronization and admission reports as Actions artifacts for
   14 days, including any partial diagnostic reports produced before a failed
   admission or validation run. An incomplete run is not marked successful.
9. When the catalog was actually pushed, invokes the existing catalog-quality
   audit as a reusable workflow. It reads the **current `main`** catalog,
   validates the complete audit and updates the public review issue. Empty
   hourly syncs do not run a redundant audit. The reusable job uses only
   repository `contents: read` and `issues: write` permissions.

   This explicit call is necessary because GitHub suppresses ordinary `push`
   workflow triggers for commits made using the built-in `GITHUB_TOKEN`.
   The catalog-quality workflow also reconciles once daily at 03:47 UTC,
   so a missed or interrupted admission audit cannot leave its issue stale
   indefinitely. Both routes read the latest `main` before publishing.
   If the default branch changes during an audit, the reporter re-fetches
   and rechecks it (up to three times). It refuses to overwrite the review
   issue with an older snapshot, retaining the audit artifact on failure.

The weekly **Refresh GitHub metadata** workflow also uses this same
validated audit publisher, but only after its own metadata/history push has
succeeded. It rebases non-destructively against new Stars admissions and fails
visibly on conflicts instead of publishing an audit from a local snapshot that
never reached `main`. Its other health/discovery issues are independent and
remain published by the maintenance workflow.

That refresh also captures GitHub's **permanent numeric repository IDs** in
existing catalog records when confirmed by the metadata response, without any
extra API calls. The refreshed IDs make subsequent Stars reconciliation
resistant to recycled owner/name slugs. Existing known IDs are immutable: if
GitHub reports a different ID or two catalog entries resolve to the same ID,
maintenance fails visibly rather than reassigning historical identities.
Unavailable repositories keep their previously recorded IDs unchanged.
The catalog-quality audit publishes **verified ID coverage** and the remaining
name-only count separately from license/maintenance findings. This makes
identity-enrichment progress measurable without claiming that inaccessible
or unverified repositories have been resolved.
The metadata reader shares the Stars sync's same-origin authenticated HTTPS
transport; redirected bearer credentials never go to another site.
The weekly discovery-candidate scanner uses this transport as well and
rejects any initially non-GitHub URL when a bearer token is supplied, before
consulting cached responses or issuing network requests.

If any repository cannot be verified, admission fails rather than committing
a partial catalog. Subsequent scheduled runs retry. No Star is silently
excluded because of its license, maturity, language or category.

## Manual/local commands

```bash
python scripts/sync_github_stars.py --user dbrckk \
  --report-json star-sync-report.json \
  --report-md star-sync-review.md \
  --manifest star-sync-manifest.json

python scripts/admit_github_stars.py \
  --sync-report star-sync-report.json \
  --manifest star-sync-manifest.json \
  --report-json star-admission-report.json \
  --dry-run
```

Remove `--dry-run` to validate and update the local catalog atomically.
The GitHub Actions workflow performs that write automatically.

## Permanent GitHub repository identity reconciliation

Legacy catalog entries can predate stable `githubRepositoryId` tracking.
A separate [weekly backfill workflow](../.github/workflows/backfill-github-ids.yml)
checks only missing identities against the public GitHub metadata API. On
October 20, 2026 the quality report showed **133 name-only entries** out
of **999**. The latest full metadata refresh recorded in `catalog.json`
was October 12, so the hourly Stars check alone cannot fill unrelated
curated repository IDs.

The backfill refuses to replace an existing ID, assign the same ID to two
catalog entries, or silently resolve an old slug into a transferred or
renamed repository. Missing/replaced names remain in the diagnostic artifact
for manual review. API outages fail before any catalog write. After a
validated non-force push, the same centralized quality audit is invoked
explicitly; this handles GitHub's suppression of bot-triggered push events.

Local offline inventory (no GitHub calls and no catalog changes):

```bash
python scripts/backfill_github_ids.py
```

To reconcile live metadata, run **Actions → Backfill permanent GitHub
repository IDs → Run workflow**. This process does not alter repo quality
scores, tiers, licenses, source code or project integration approvals.

## Limitations

- The built-in `GITHUB_TOKEN` reads public Stars, not necessarily private
  repositories or private Stars unavailable to this token.
- Previously cataloged entries remain after an unstar; the catalog is additive.
- Renamed/transferred repositories with known stable IDs are recognized as
  already present; legacy references may require a separate canonical rename.
- A GitHub owner/name slug may be recycled after deletion or transfer. If the
  current public Star reports a different permanent repository ID from a
  catalog entry with the same slug, syncing **fails visibly** instead of
  incorrectly marking the new repository as accounted for. A transfer that
  retains its permanent ID is still recognized. Ambiguous duplicate IDs across
  API pages also abort the snapshot; the next scheduled sync retries.
  Historic entries without a known stable ID cannot be verified by ID until
  separately enriched. The hourly public Stars snapshot now enriches matching
  legacy entries without refetching; the weekly metadata refresh can verify
  other accessible entries. Unreachable repos remain name-only until a reliable
  permanent ID is established.
- GitHub's license label is only metadata; model weights, assets and commercial
  usage may have separate restrictions.
- Auto-admitted entries retain the `audit` tier until deeper manual curation.
- A permission or branch policy preventing bot commits causes a visible workflow
  failure, not a false successful synchronization.

The synchronization uses Python 3.12 standard library and GitHub Actions.
