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

## Final v3 recovery evidence (2026-10-17)

The [authenticated operator diagnosis](https://github.com/dbrckk/star-list/actions/runs/39016621939)
verified **all five terminal v2/v3 task results**: the four earlier v2
failures and the new final v3 recovery for `dbrckk/Ai-trading`. All five
show `worker_result_status=capacity_exhausted` and
`pipeline_status=capacity_exhausted`, exactly **1/3** task attempts,
**zero** delivered commits, **zero** reviewable PRs and no CI evidence.
The v3 result is not a recovered integration. This is direct worker-task
evidence; it does not establish whether the limiting provider, model quota
or project envelope specifically caused the underlying shortage.

After [star-list PR #105](https://github.com/dbrckk/star-list/pull/105),
a terminal `v3 NEEDS_ATTENTION` is a fleet-wide **automatic launch stop**,
independent of the UTC daily limit. Repo discovery, Stars sync and read-only
failure diagnosis continue. The stop is intentional: do not raise the token
budget, reset tracking markers, manually relaunch the same v3, or circumvent
the safety gate until a real provider inference route and worker are positively
verified and the operator has reviewed the previous attempt.

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
   on actual language, environment, license and use case. The latest public scan shows
   only `Ai-trading` and `vibecheck-android` with native-mode candidates. The other historical failures should not be restarted
   simply to raise the completed count.
5. Only after capacity is proven, use the existing bounded, idempotent
   higher-version recovery path. Preserve the one-launch-per-UTC-day rule
   while unresolved failures exist, global worker caps and per-target
   single-flight safety. Do not forcibly reset existing project states.
6. Require a real reviewable source change, appropriate target build/CI,
   and evidence that the new component is used. Neither an accepted
   Production-OS launch nor an improved worker status alone is completion.

## Verified free inference routes to qualify (2026-10-17)

These are **candidates for capacity testing**, not verified Production-OS
workers or permission to resume failed v3 work. None has yet passed a
live, authenticated code-editing inference preflight in this environment.

| Provider | Free-plan evidence | Conditions and limits |
| --- | --- | --- |
| Cloudflare Workers AI | [Official pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/): 10,000 Neurons per day on Workers Free, resetting at 00:00 UTC | Free tier still fails after the allowance; neurons are **not** the same as tokens. Some high-end coding models now require Workers Paid or prepaid credits. Use a currently Free-eligible model (for example [GLM-4.7-Flash](https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/)) for a small qualified probe, not an assumed 90k-token job. |
| Pollinations | [Official authentication](https://gen.pollinations.ai/docs): OpenAI-compatible text API, user-scoped key required for generation | Public models have individual prices; only catalog models explicitly priced at zero can be assumed free at the Pollinations layer. A key can be valid but out of its allowance (`402 PAYMENT_REQUIRED`). Do not treat a publicly accessible model list as guaranteed free inference. |

For a free alternative, the safe evaluation sequence is:

1. Obtain a user-authorized, budget-constrained provider key and save it
   **only** as a masked repository/worker secret; never commit or print it.
   A provider's free plan is not a license to use paid models.
2. Query the chosen provider's *authenticated* quota/budget and its live
   eligible model list. Reject exhausted, paid-only or unknown-capacity routes.
3. Run one bounded, non-mutating inference probe with an explicit free eligible
   model, record only success/failure and redacted quota evidence, and confirm
   the worker's exact implementation task can use that provider.
4. Prefer short, verified source edits over oversized attempts. Preserve the
   existing project budget, fleet launch cap, per-target single-flight and
   final-v3 operator stop. Never automatically retry just because a provider
   claims a large theoretical monthly allocation.
5. Require target-side tested source changes and CI before reporting that any
   integration succeeded. A positive model probe alone is not completion.

Do not put Pollinations or Workers AI API keys, request URLs with credentials,
inference prompts, private repository identities or provider traces in public
star-list artifacts. This guide authorizes **diagnosis only**; resuming
Production-OS mutation still requires a separate operator decision.

## Safe observability

The workflow
[Diagnose failed star-list integrations](https://github.com/dbrckk/star-list/actions/workflows/portfolio-failure-diagnostics.yml)
uses an operator-only read endpoint. Its retained artifacts contain only
public repository names and strict diagnostics categories, counts and enums.
Never publish raw task results, model logs, source instructions, credentials,
private-repository identities or internal project/job identifiers.

This playbook does not raise token limits, require a paid provider, deploy an
application or authorize automatic merging.
