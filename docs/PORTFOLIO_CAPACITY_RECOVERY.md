# Production-OS portfolio integrations: capacity-exhaustion recovery

## Evidence and status (2026-10-16)

The [operator-only diagnostic run](https://github.com/dbrckk/star-list/actions/runs/38954955707)
inspected the **actual persisted worker tasks** for four public targets.
All four v2 integrations ended with both
`worker_result_status=capacity_exhausted` and
`pipeline_status=capacity_exhausted`.

| Target | Attempts | Max attempts | Failed tasks | Commits | PR/CI evidence |
| --- | ---: | ---: | ---: | ---: | --- |
| `dbrckk/Ai-trading` | 1 | 3 | 1 | 0 | None |
| `dbrckk/vibecheck-android` | 1 | 3 | 1 | 0 | None |
| `dbrckk/viral-android-game` | 1 | 3 | 1 | 0 | None |
| `dbrckk/xbow-perso` | 1 | 3 | 1 | 0 | None |

A worker-capacity failure is **not** proof of an incompatible upstream
dependency, a successful patch, or exhausted workflow retry counts.
The [public daily review](https://github.com/dbrckk/star-list/issues/61)
continues to show these historical attempts as unresolved.

The Render service `production-os1` deployed successfully on October 16;
that server deployment alone does **not** establish downstream AI model
capacity or successful worker execution.

## What to check before a recovery

1. Inspect `dbrckk/ai-dev-server` provider health, token availability,
   active provider cooldowns and the worker's actual capacity snapshot.
   The worker code in `studio/production_os_worker.py` can constrain
   the requested task envelope by **authenticated, available** Omniroute
   tokens. A positive service health check or a registered worker does not
   prove that the model provider can accept an inference request.
2. Establish **positive, usable free capacity** for the relevant code
   task. If the provider reports exhausted capacity or rejects inference,
   do not blindly restart the same 90,000-token integration; restore a
   qualified free model/provider route or defer execution.
3. Verify the available worker really has the required capabilities and
   that Production-OS can dispatch the target-specific work.
   The [Production-OS Actions Worker](https://github.com/dbrckk/ai-dev-server/actions/workflows/production-os-actions-worker.yml)
   provides operational evidence. Its historical failed-job counts must
   not be mistaken for fresh jobs waiting in the queue.
4. Run a **read-only** star-list portfolio scan and requalify each candidate
   on actual language, environment, license and use case. Currently only
   `Ai-trading` and `vibecheck-android` have native-mode candidates in
   the public scan. The other historical failures should not be restarted
   simply to raise the completed count.
5. Only after capacity is proven, use the existing bounded, idempotent
   higher-version recovery path. Preserve the one-launch-per-UTC-day rule
   while unresolved failures exist, global worker caps and per-target
   single-flight safety. Do not forcibly reset existing project states.
6. Require a real reviewable source change, appropriate target build/CI,
   and evidence that the new component is used. Neither an accepted
   Production-OS launch nor an improved worker status alone is completion.

## Safe observability

The workflow
[Diagnose failed star-list integrations](https://github.com/dbrckk/star-list/actions/workflows/portfolio-failure-diagnostics.yml)
uses an operator-only read endpoint. Its retained artifacts contain only
public repository names and strict diagnostics categories, counts and enums.
Never publish raw task results, model logs, source instructions, credentials,
private-repository identities or internal project/job identifiers.

This playbook does not raise token limits, require a paid provider, deploy an
application or authorize automatic merging.
