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
  --report-json star-admission-report.json \
  --dry-run
```

Remove `--dry-run` to validate and update the local catalog atomically.
The GitHub Actions workflow performs that write automatically.

## Limitations

- The built-in `GITHUB_TOKEN` reads public Stars, not necessarily private
  repositories or private Stars unavailable to this token.
- Previously cataloged entries remain after an unstar; the catalog is additive.
- Renamed/transferred repositories with known stable IDs are recognized as
  already present; legacy references may require a separate canonical rename.
- GitHub's license label is only metadata; model weights, assets and commercial
  usage may have separate restrictions.
- Auto-admitted entries retain the `audit` tier until deeper manual curation.
- A permission or branch policy preventing bot commits causes a visible workflow
  failure, not a false successful synchronization.

The synchronization uses Python 3.12 standard library and GitHub Actions.
