# Changelog

All notable stable changes to `star-list` are recorded here.

## 1.0.0 - 2026-09-16

First stable release of the catalog and automation pipeline.

### Added

- Curated repository catalog with schema validation and task-oriented recommendation.
- Repository health scoring, trend history, replacement review, and advisory health issues.
- Coverage analysis, discovery watchlists, GitHub candidate discovery, deterministic admission evaluation, and discovery-memory suppression.
- Persistent discovery cache with ETag reuse, retry/backoff, stale fallback, telemetry, adaptive cache-health analysis, and issue lifecycle handling.
- JSON contracts for generated and persistent pipeline outputs.
- Deterministic offline end-to-end discovery integration testing.
- Candidate score explainability, calibrated `accept`/`review`/`reject` thresholds, metadata confidence, and the `low-confidence-cap` admission safeguard.
- Defensive handling for malformed candidate metadata, health inputs, discovery memory, repository history, and cache-health metrics.
- Public architecture, recommender, and discovery-scoring documentation.

### Release guarantees

- Discovery remains advisory: candidates are never inserted into `catalog.json` automatically.
- The validation workflow covers catalog validation, unit/component tests, JSON contracts, offline pipeline integration, degraded-input robustness, documentation consistency, and generated report contracts.
- The scheduled metadata workflow maintains repository metadata, health/history state, discovery state, cache health, and review issues.
