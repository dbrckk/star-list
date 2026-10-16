## Read-only failure diagnosis (public targets only)

To inspect unresolved managed integrations without an operator-token leak, run
the **Diagnose failed star-list integrations** GitHub Actions workflow. Its
operator-authenticated query reads Production-OS's problem inbox but writes
only a strict allowlist of public repositories, enum-valued failure
categories/statuses and boolean delivery indicators. Raw goals, worker
messages, internal IDs, URLs, private-repository identities, token values,
and provider traces never appear in artifacts or action logs.

The query is bounded to 200 problem projects and refuses an incomplete page.
The report separately marks `coverage_complete` based on the four publicly
verified unresolved v2 targets (Ai-trading, vibecheck-android,
viral-android-game, xbow-perso). Missing entries are **not** treated as
successful recovery; the workflow exits nonzero. The diagnostic cannot prove
successful code integration. Confirm changed source, PR, target CI and actual
runtime before marking any job done.

The workflow runs on a trusted main-branch change to itself or the diagnosis
script and also supports authenticated manual dispatch. It never launches,
retries, modifies or approves a managed project. No paid service is required.

For each failed v2 task, the operator workflow now also reads the project-specific
workflow result (at most four additional GETs). It inspects failed/blocked task
results in memory for allowlisted categories, retry-exhaustion status and task
counts. No raw task result, project ID, job key or workflow payload is emitted.
`details_complete` must be true for all four verified failed v2 targets;
otherwise the workflow exits nonzero while preserving partial safe evidence.
