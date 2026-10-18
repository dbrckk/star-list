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

### Implemented opt-in Cloudflare fallback — not yet activated (2026-10-17)

[AI Dev Server PR #335](https://github.com/dbrckk/ai-dev-server/pull/335)
is merged into `ai-dev-server/main` as commit
[`b0cd423`](https://github.com/dbrckk/ai-dev-server/commit/b0cd423262325cce3fdc13cfca294525154944f9).
Its exact PR head passed all **seven** GitHub checks: CI, validation,
Production-OS worker integration, fault injection, resilience, mobile build and
multi-engine benchmark. The merge only adds an **optional** free-eligible
`@cf/zai-org/glm-4.7-flash` route. It is disabled by default and does not
prove a live usable quota or completion of any portfolio integration.

To qualify this path, an operator first confirms a **Workers Free** account and
then configures the `dbrckk/ai-dev-server` Actions secret
`CLOUDFLARE_API_TOKEN` and Actions variables `CLOUDFLARE_ACCOUNT_ID`
(32 hexadecimal characters) and `STUDIO_CLOUDFLARE_FREE_TIER_ONLY=1`.
The Cloudflare token is excluded from third-party agent subprocesses. The
built-in fallback is injected only with these opt-in values, a default NVIDIA
base URL and an empty `STUDIO_PROVIDERS_JSON` override. The Workers Paid
plan is not a safe zero-cost substitute: over-quota usage can be billed.

Run the existing
[Production-OS Live Diagnostics](https://github.com/dbrckk/ai-dev-server/actions/workflows/production-os-live-diagnostics.yml)
only after confirming the free-plan settings; it probes a small actual
inference and operator access without changing a target. Record sanitized
results, then establish adequate provider/worker capacity and a small
reviewable coding delivery before any operator-approved portfolio recovery.
**Do not clear** the terminal-v3 global safety stop merely because the
diagnostic probe or an unrelated CI workflow passes. No Cloudflare account,
token, billing-plan confirmation or successful live inference has yet been
verified in this project.

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

## Verified delivery guards, not yet a recovered integration (2026-10-18)

Two AI Dev Server safety improvements have now merged independently:

- [PR #345](https://github.com/dbrckk/ai-dev-server/pull/345):
  directly created autonomous GitHub pull requests are **draft** by default,
  matching the existing trusted target-side handoff.
- [PR #346](https://github.com/dbrckk/ai-dev-server/pull/346):
  the Jumpy canary only reports delivery when GitHub confirms that the
  exact open target pull request points to the **published 40-character SHA**.
  A previously opened PR on the same branch or an accepted dispatch is not
  delivery proof.

Both PRs passed their seven required exact-head CI workflows before merge,
including Production-OS worker integration, multi-engine Godot and
mobile/Flutter checks. They do not reset historical failures, prove usable
provider quota, or certify an end-to-end **new** target source integration.

A successful **portfolio integration** must now have *all* of the following
independent evidence:

1. A scoped, open-source upstream candidate with verified license and
   runtime compatibility, not merely a high heuristic catalog score.
2. A target branch containing real source changes that actually use the
   component, not only a marker file, documentation or queued managed task.
3. A draft review PR whose target repository, branch and head SHA match the
   published source checkpoint; if confirmation fails, retain the checkpoint
   and report `blocked`, never `complete`.
4. Successful applicable target-side tests, build and runtime checks against
   that exact SHA, with artifacts or CI links for independent review.
5. Explicit review before merge or deployment. Source publication and
   a passing synthetic canary do not alone authorize fleet-wide resumption.

The [2026-10-18 operator diagnosis](https://github.com/dbrckk/star-list/actions/runs/39113139237)
still covered all **four historical v2 and one terminal v3** failures with
no verified target-side integration delivery. The automatic v3 fleet stop
remains active. A short model-completion smoke from the NVIDIA NIM route
may demonstrate isolated inference availability, but it is not durable free
capacity for the 90,000-token portfolio task envelope.

## Delivery acceptance gates (2026-10-18)

The Production-OS handoff must not be reported as a successful integration
merely because GitHub accepted a write or the worker returned a task receipt.
The merged [AI Dev Server PR #345](https://github.com/dbrckk/ai-dev-server/pull/345)
makes agent-created code-delivery PRs **draft by default**. The merged
[PR #346](https://github.com/dbrckk/ai-dev-server/pull/346) checks that the
target PR head is **exactly** the commit that was pushed; an unrelated branch
head or an out-of-date PR is not delivery evidence.

Before recording any catalog-to-target integration as complete, retain
all of the following evidence:

1. A positive authenticated provider-capacity check for the *actual* coding
   route, followed by a bounded worker execution. A short smoke probe alone
   does not establish sustained free quota.
2. A real source commit in the intended target repository, with an inspected
   diff implementing the selected licensed and compatible component. A
   generated proposal or no-op commit is insufficient.
3. A reviewable **draft** PR whose repository, base and head SHA match the
   intended target and the delivered source commit exactly. Do not
   auto-approve or auto-merge third-party integrations.
4. Passing relevant target-side tests, build and CI for the exact delivered
   SHA, plus evidence the integrated component is actually invoked by the
   application rather than merely declared as a dependency.
5. A recorded operator review of the earlier terminal v3 failure before
   any fleet-wide recovery. A successful isolated canary does not remove
   the existing global launch stop.

These gates are independent: CI on the orchestration repository is not
substitute evidence for CI on the modified target. Preserve failed attempts
and their original status rather than retroactively marking them DONE.

## Safe observability

The workflow
[Diagnose failed star-list integrations](https://github.com/dbrckk/star-list/actions/workflows/portfolio-failure-diagnostics.yml)
uses an operator-only read endpoint. Its retained artifacts contain only
public repository names and strict diagnostics categories, counts and enums.
Never publish raw task results, model logs, source instructions, credentials,
private-repository identities or internal project/job identifiers.

This playbook does not raise token limits, require a paid provider, deploy an
application or authorize automatic merging.
