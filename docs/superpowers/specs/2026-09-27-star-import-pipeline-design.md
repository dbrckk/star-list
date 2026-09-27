# GitHub Star Import Pipeline Design

Date: 2026-09-27
Status: approved design

## Intent

Turn screenshot-derived GitHub star batches into a deterministic, repeatable ingestion flow for `star-list`. Preserve raw provenance, avoid duplicate work, integrate only normalized unique repositories, and keep the catalog valid and useful for downstream recommendation and project-selection workflows.

## Constraints

- Preserve the existing `catalog.json` schema and repository architecture unless a change is strictly required.
- Treat files under `imports/` as immutable provenance inputs after ingestion.
- Prefer deterministic local processing with no paid dependency.
- Do not require GitHub secrets for normalization, deduplication, or validation.
- Network enrichment, when used, must be optional and must not make core validation nondeterministic.
- Reuse the repository's existing catalog validation and quality checks.
- Keep changes small enough to review and test independently.

## Architecture

Add one ingestion command implemented as focused Python modules/scripts rather than embedding import logic in `catalog.json` maintenance by hand.

The pipeline has six stages:

1. **Load**: read one or more `imports/github-stars-*.json` files and preserve source-file provenance.
2. **Normalize**: canonicalize repository identifiers to lowercase-comparable `owner/repo` keys while retaining display casing and canonical GitHub URL fields where available.
3. **Deduplicate**: collapse duplicates both across input batches and against repositories already represented in `catalog.json`.
4. **Classify**: map genuinely new repositories onto the catalog's existing taxonomy using deterministic metadata/rules first. Ambiguous entries are surfaced for review rather than silently guessed.
5. **Integrate**: produce a stable proposed catalog update with deterministic ordering and no duplicate repository identity.
6. **Validate**: run schema/catalog validation plus quality checks and fail the operation if the resulting catalog violates existing invariants.

## Components

### Import loader

Responsibilities:
- Accept explicit import paths and a glob/default for pending GitHub-star imports.
- Validate each input's basic structure before processing.
- Attach source filename to each normalized candidate for traceability.
- Report malformed records with file and record location.

### Repository identity normalizer

Responsibilities:
- Derive a canonical identity key from repository full name or GitHub repository URL.
- Normalize URL variants, trailing slashes, and `.git` suffixes.
- Reject values that cannot unambiguously identify a GitHub `owner/repo` repository.
- Preserve original values for diagnostics.

Identity comparison is case-insensitive. The canonical comparison key is `owner/repo` in lowercase.

### Deduplicator

Responsibilities:
- Deduplicate candidates across all supplied import batches.
- Build an identity set from the existing catalog.
- Partition records into `already_cataloged`, `duplicate_import`, and `new`.
- Preserve every source batch contributing to a duplicate identity in the report.

### Classifier

Classification must follow the taxonomy already encoded by the catalog rather than inventing a parallel category system. Existing catalog examples and fields are authoritative.

The classifier may use deterministic signals available in import records and existing repository metadata. If evidence is insufficient for a required catalog field, the candidate is placed in `needs_review`; it must not receive fabricated metadata.

Project relevance may be recorded using existing catalog mechanisms for areas such as agent tooling, repository intelligence, Android, Godot/game development, security, AI/model tooling, deployment, and automation. This relevance is descriptive metadata, not a replacement taxonomy.

### Integrator

Responsibilities:
- Update only the catalog records that are genuinely new and sufficiently classified.
- Preserve existing records unchanged.
- Maintain deterministic ordering according to current catalog conventions.
- Support a dry-run/report mode before writing.
- Make repeated ingestion idempotent: running the same inputs twice produces no second catalog change.

### Report

Each run emits a concise machine-readable and human-readable summary containing:
- import files processed;
- total raw records;
- unique normalized repositories;
- duplicates within imports;
- repositories already in the catalog;
- newly integrated repositories;
- candidates requiring review;
- malformed/rejected records;
- validation results.

Generated reports must not become a second source of truth for catalog data.

## Data Flow

`imports/*.json` -> loader -> normalizer -> deduplicator -> classifier -> integrator -> temporary/proposed catalog -> existing validators -> `catalog.json`

Validation occurs before a write is considered successful. A failure leaves the authoritative catalog unchanged.

## Error Handling

- Invalid JSON: fail that run with the offending file identified.
- Malformed repository identity: reject the record and report it; never synthesize an identity.
- Duplicate input: collapse deterministically and report provenance.
- Existing catalog entry: skip without modifying the existing entry.
- Ambiguous classification: route to `needs_review` rather than guessing.
- Validation failure: do not accept the generated catalog update.
- Optional network metadata unavailable: continue with deterministic local data where possible; otherwise route affected candidates to review.

## Testing

Add focused tests covering:
- owner/repo and GitHub URL normalization;
- case-insensitive duplicate detection;
- duplicates spanning multiple import batches;
- detection of entries already in `catalog.json`;
- malformed input diagnostics;
- classification fallback to `needs_review`;
- idempotent repeated ingestion;
- deterministic output ordering;
- no catalog write on validation failure.

Then run the repository's existing `scripts/validate_catalog.py`, `scripts/test_catalog_quality.py`, and relevant quality audit checks. Any CI configured for the repository remains the final integration gate.

## Initial Migration

The four September 27 import files currently identified by repository state are the first production input set:

- `imports/github-stars-2026-09-27.json`
- `imports/github-stars-2026-09-27-batch-2.json`
- `imports/github-stars-2026-09-27-batch-3.json`
- `imports/github-stars-2026-09-27-batch-4.json`

The migration will process all four together so cross-batch duplicates are resolved before catalog integration.

## Success Criteria

- All four current batches can be processed by one command/workflow.
- Every valid repository has one canonical identity during ingestion.
- No duplicate repository is introduced into `catalog.json`.
- Existing catalog entries are not rewritten merely because they appear in a new import.
- Ambiguous data is reported instead of fabricated.
- Re-running the same imports is idempotent.
- Existing catalog validation and quality tests pass after integration.
- Future screenshot-derived batches can use the same pipeline without new one-off import code.
