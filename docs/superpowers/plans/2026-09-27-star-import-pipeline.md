# GitHub Star Import Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic CLI that loads screenshot-derived GitHub star imports, normalizes identities, deduplicates them against each other and `catalog.json`, safely classifies only high-confidence candidates, reports ambiguous entries, and validates any proposed catalog write.

**Architecture:** Keep ingestion logic in one focused Python module with a thin CLI entry point and a standalone test script matching the repository's existing script-based test style. Local normalization/deduplication is authoritative; optional enrichment is separate from the deterministic core. Writes are atomic and occur only after existing validators accept the candidate catalog.

**Tech Stack:** Python 3 standard library; existing JSON catalog and validation scripts.

**Spec:** `docs/superpowers/specs/2026-09-27-star-import-pipeline-design.md`

## Global Constraints

- Preserve existing catalog schema and records unless integration adds a genuinely new, sufficiently classified repository.
- Raw `imports/` files remain provenance inputs.
- Core normalization/deduplication requires no paid service, secret, or network access.
- Never fabricate required metadata; unresolved candidates go to `needs_review`.
- Repeated ingestion of the same inputs is idempotent.
- Existing catalog validation remains the final write gate.

## Review Focus

- Mixed-case repository names must compare case-insensitively without losing display casing.
- GitHub URLs with `.git`, trailing slash, query/fragment, or nested paths must not produce ambiguous identities.
- One malformed import record must be reported with provenance rather than silently becoming a repository.
- Cross-batch duplicates must retain all contributing source filenames in the report.
- Validation failure must leave the authoritative catalog byte-for-byte unchanged.

---

### Task 1: Normalization and import loading

**Files:**
- Create: `scripts/star_import_pipeline.py`
- Create: `scripts/test_star_import_pipeline.py`

**Interfaces:**
- Produces: `normalize_repo_identity(value: str) -> tuple[str, str]`, `load_imports(paths: list[Path]) -> tuple[list[dict], list[dict]]`.

- [ ] Write failing tests for owner/repo, GitHub URL variants, malformed/nested URLs, and malformed import records with source provenance.
- [ ] Run `python scripts/test_star_import_pipeline.py` and verify RED because the module/functions do not exist.
- [ ] Implement the two interfaces using only the standard library.
- [ ] Run `python scripts/test_star_import_pipeline.py` and verify GREEN.

### Task 2: Deduplication and catalog partitioning

**Files:**
- Modify: `scripts/star_import_pipeline.py`
- Modify: `scripts/test_star_import_pipeline.py`

**Interfaces:**
- Consumes: normalized records from Task 1.
- Produces: `partition_candidates(records: list[dict], catalog: dict) -> dict` with `new`, `already_cataloged`, and `duplicate_import` collections.

- [ ] Add failing tests for case-insensitive catalog matches, cross-batch duplicates, source aggregation, and deterministic first-seen display identity.
- [ ] Run test script and verify RED.
- [ ] Implement deterministic partitioning.
- [ ] Run test script and verify GREEN.

### Task 3: Safe classification and report generation

**Files:**
- Modify: `scripts/star_import_pipeline.py`
- Modify: `scripts/test_star_import_pipeline.py`

**Interfaces:**
- Produces: `classify_candidate(candidate: dict, metadata: dict | None = None) -> dict`, `build_report(partition: dict, malformed: list[dict], import_files: list[str]) -> dict`.

- [ ] Add failing tests proving insufficient metadata becomes `needs_review`, no required catalog metadata is fabricated, and report counts/provenance are deterministic.
- [ ] Run test script and verify RED.
- [ ] Implement conservative classification and JSON/Markdown report rendering.
- [ ] Run test script and verify GREEN.

### Task 4: Atomic integration and validation gate

**Files:**
- Modify: `scripts/star_import_pipeline.py`
- Modify: `scripts/test_star_import_pipeline.py`

**Interfaces:**
- Produces: `integrate_catalog(catalog: dict, accepted: list[dict]) -> dict`, `validate_candidate_catalog(candidate: dict, root: Path) -> tuple[bool, str]`, and atomic write helper.

- [ ] Add failing tests for idempotence, deterministic ordering, preservation of existing records, and no write on failed validation.
- [ ] Run test script and verify RED.
- [ ] Implement integration through a temporary catalog and existing validators; replace `catalog.json` only after validation succeeds.
- [ ] Run test script and verify GREEN.

### Task 5: CLI and production migration report

**Files:**
- Modify: `scripts/star_import_pipeline.py`
- Modify: `scripts/test_star_import_pipeline.py`
- Create: `reports/star-import-2026-09-27.json`
- Create: `reports/star-import-2026-09-27.md`

**Interfaces:**
- CLI: `python scripts/star_import_pipeline.py [IMPORT ...] [--catalog PATH] [--report-json PATH] [--report-md PATH] [--write]`.

- [ ] Add failing CLI tests for dry-run default, explicit report paths, and write gating.
- [ ] Run test script and verify RED.
- [ ] Implement CLI.
- [ ] Run the CLI against all four September 27 import files in dry-run mode and create deterministic reports.
- [ ] Run `python scripts/test_star_import_pipeline.py`, `python scripts/validate_catalog.py`, and `python scripts/test_catalog_quality.py`; all must exit 0.
- [ ] Re-run the dry-run command and verify the generated report is stable.
