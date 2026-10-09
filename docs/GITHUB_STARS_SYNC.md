# Automatic GitHub Stars synchronization

star-list can check the public GitHub Stars of the account **dbrckk** without
sending screenshots or configuring any external service.

## Scheduled operation

[Sync GitHub Stars](../.github/workflows/sync-github-stars.yml) runs daily at
05:41 UTC, can be started manually in **GitHub → Actions → Sync GitHub Stars →
Run workflow**, and runs automatically whenever `catalog.json` changes on `main` (so the review issue is reconciled immediately after admissions).

It uses the built-in GITHUB_TOKEN (read access to the GitHub API; issues:write
only for its review issue). It requires **no personal access token and no paid
API**.

The workflow:
1. Executes the offline synchronization regression tests.
2. Fetches every accessible public Star for dbrckk (100 per page).
3. Compares normalized owner/repository names and recorded permanent GitHub IDs with catalog.json.
4. Generates an immutable-for-the-run JSON report, Markdown review, and a
   star-import compatible manifest as **GitHub Actions artifacts** (14 days).
5. Creates or updates **one** review issue if new repositories are found;
   closes the previous issue when no review is needed.

The catalog is **never** changed by this workflow. Only the existing,
explicitly human-reviewed admission path in
[scripts/star_import_pipeline.py](../scripts/star_import_pipeline.py) can write
new entries. The report is a discovery aid, not a software review, license
grant, or security assessment.

## Local execution

Python 3.12 standard library is sufficient for the synchronizer.

~~~bash
python scripts/test_sync_github_stars.py
python scripts/sync_github_stars.py --user dbrckk \
  --report-json star-sync-report.json \
  --report-md star-sync-review.md \
  --manifest star-sync-manifest.json
python scripts/validate_json_contract.py \
  schemas/star-sync-report.schema.json star-sync-report.json
~~~

For higher GitHub rate limits, optionally set GITHUB_TOKEN in your environment.
Do not put tokens in Git-tracked files. The default public endpoint can also
work without a token, subject to lower API limits.

To inspect the discovered names using the existing read-only import pipeline:

~~~bash
python scripts/star_import_pipeline.py star-sync-manifest.json \
  --report-json star-sync-import-report.json
~~~

Admitting a new entry still requires manually inspected and verified metadata,
an explicit reviewed=true entry and the existing validator.

## Failure behavior and limitations

- HTTP errors, malformed API data, exhausted retries and incomplete pagination
  **fail the run** instead of claiming the catalog is complete.
- The page limit defaults to 100 (up to 10,000 starred entries); reaching it
  while a next page exists fails closed. Increase --max-pages if needed.
- Only repositories visible through the GitHub account permissions used by
  the job are returned; it cannot inspect private repositories inaccessible to
  GITHUB_TOKEN. Stars removed from the account are not deleted from the catalog.
- For catalog entries with a verified `githubRepositoryId`, GitHub Stars are
  matched by that permanent ID even if the repository owner/name changes.
  Older catalog entries without an ID still fall back to case-insensitive names;
  their transfers may require a one-time identity review.
- GitHub's license field is only a metadata hint; model weights and bundled
  assets may use separate or more restrictive terms.
- The issue displays at most 50 new repositories; the artifact contains all
  results. A workflow failure does not update or close the previous issue.
- When Actions permissions are restricted, review issue publication can fail.
  The workflow must have issues:write; no admin or external connector is needed.

Tests run without any network, API keys, or dependency installation.
