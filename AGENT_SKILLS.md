# Skill Issue: priority agent-skill discovery for every repository

The public [Skill Issue](https://skill-issue.in/) directory is a **search and
discovery reference** for reusable agent skills (design, frontend, backend,
motion/video, automation and other domains). It is not an installed agent, a
verified package registry, an executable dependency or an assurance of
copyright/security compliance.

The catalog lists its website once in [websites.json](websites.json) and a
curated set of **25** original skill source references in
[agent-skills.json](agent-skills.json). The initial 19 entries were
drawn from Skill Issue's visible listings; six additional specialized
Flutter/Godot/Android/Roblox references come from the official Flutter
and Android agent repositories and independently verified engine-specific
skill sources. All upstream SKILL.md
files are addressed at immutable Git commits, but their instructions and
supporting scripts remain unaudited.
Every entry now records its **exact `SKILL.md` path and a pinned Git commit**
where that file exists, so reviewers can inspect immutable source before any
decision. This verifies source identity and file existence, **not** the
safety or correctness of the SKILL.md instructions or bundled scripts.

## Make it useful throughout the portfolio

Every accessible repository reviewed by the existing public daily scan or
private per-repository workflow receives the **high-priority Skill Issue
directory** in its report, even when no individual skill qualifies. When
metadata strongly supports a match, the scanner also proposes **up to two**
specific skill sources. All results are advisory; neither GitHub Stars
synchronization nor Production-OS integration dispatch installs these skills.

The matching algorithm considers GitHub-owned project metadata
(repository name, description, topics, inferred domain and primary language)
and, for repositories with `package.json`, a **strict allowlist of exact
dependency names** (for example React, Expo, Next.js, Tailwind and Remotion).
Flutter guidance requires the exact `dependencies.flutter.sdk: flutter`
declaration in the root `pubspec.yaml` or matching project-owned Flutter
labels with the Dart language. GDScript skills can be qualified by GitHub's
primary GDScript language metadata. For mixed projects, the scanner checks
both root package manifests independently of the first detected project
manifest, without changing the existing integration-dependency ranking.
It does not tokenize untrusted README instructions, package install scripts or
arbitrary manifest text. Only skill recommendations use these new framework
hints; the existing catalog-dependency integration ranker and dispatch gate
are unchanged. Skill suggestions still require a matching domain and a
concrete label/framework match. Unknown projects see the general directory
without arbitrary skill installations.

Examples of curated source references (all direct skill-file links returned
by the CLI are revision-pinned):

| Skill | Source repository | Example fit |
| --- | --- | --- |
| UI UX Pro Max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Web, mobile and game UI design |
| Frontend Design | [anthropics/skills](https://github.com/anthropics/skills) | Frontend and visual design |
| Agent Browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Browser QA and automation |
| React Best Practices | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React/Next.js applications |
| Web Design Guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Web UI quality and accessibility |
| Remotion Best Practices | [remotion-dev/skills](https://github.com/remotion-dev/skills) | JS/TS video and animation pipelines |
| API Design Principles | [wshobson/agents](https://github.com/wshobson/agents) | Backend REST/GraphQL APIs |
| Design Taste Frontend | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Frontend art direction and visual review |
| Redesign Existing Projects | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Existing UI refinement |
| Image to Code | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Image-guided frontend |
| Design System Patterns | [wshobson/agents](https://github.com/wshobson/agents) | Reusable design tokens and component systems |
| React Native Architecture | [wshobson/agents](https://github.com/wshobson/agents) | JavaScript/TypeScript mobile apps |
| Accessibility Compliance | [wshobson/agents](https://github.com/wshobson/agents) | WCAG/UI quality |
| Auth Implementation Patterns | [wshobson/agents](https://github.com/wshobson/agents) | Backend authentication |
| OpenAPI Spec Generation | [wshobson/agents](https://github.com/wshobson/agents) | REST API documentation |
| Flutter Responsive Layout | [flutter/agent-plugins](https://github.com/flutter/agent-plugins) | Adaptive Flutter/Dart widget layouts |
| Flutter Layout Diagnostics | [flutter/agent-plugins](https://github.com/flutter/agent-plugins) | Debugging Flutter overflow and layout constraints |
| Godot GDScript 4.x | [shihabshahrier/Godot-Skill](https://github.com/shihabshahrier/Godot-Skill) | Typed scenes, signals and Godot 4 gameplay guidance |
| Jetpack Compose Performance | [android/skills](https://github.com/android/skills) | Verified Compose-specific UI performance review |
| Android Play Policy Insights | [android/skills](https://github.com/android/skills) | Google Play policy and data-safety review |
| Roblox Luau Development | [MSayib/roblox-dev-skill](https://github.com/MSayib/roblox-dev-skill) | Roblox Studio/Luau development patterns |

The other curated entries cover Next.js App Router, React state,
Tailwind design systems and responsive interfaces. Flutter, Godot, Android and Roblox sources complement Skill Issue rather
than implying those entries were listed by the Skill Issue directory.
Root-level `SKILL.md` entries are supported when pinned and validated.
Jetpack Compose optimization is not recommended merely because a project
uses Android; actual Compose evidence is required. Source paths are pinned
for auditability, **not for automated execution or installation**. Read and
audit the entire pinned instruction and scripts before considering adoption.

## Continuous verification of pinned sources

On 2026-10-20, all **25** source links currently in
[`agent-skills.json`](agent-skills.json) were directly retrieved at their
recorded immutable Git commits. This proves those files existed and were
accessible at that point, **not** that any instruction is safe, reviewed,
compatible or legally reusable.

The [daily metadata audit](.github/workflows/audit-agent-skill-sources.yml)
now rechecks each exact pinned `SKILL.md` path without executing or trusting
any remote instruction. It verifies only GitHub file metadata and preserves a
structured artifact. A missing/invalid reference opens or updates a GitHub
review issue; recovered links close it. Rate-limit, network and access failures
keep the scan explicitly **incomplete** and fail the workflow rather than
publishing a false clean report.

To validate the local contract without network access:

```bash
python scripts/audit_agent_skill_sources.py \
  --json-output /tmp/skill-sources.json
python scripts/validate_json_contract.py \
  schemas/agent-skill-source-audit.schema.json /tmp/skill-sources.json
```

To actually recheck upstream files, run
**Actions → Audit pinned Skill Issue sources → Run workflow**.
Source access evidence does not authorize auto-installation.

## Use from the repository

```bash
# Validate the local snapshot and find skill sources.
python scripts/agent_skill_discovery.py

# Select only framework-compatible, project-relevant suggestions.
python scripts/agent_skill_discovery.py "react frontend performance" --domain web_frontend --language TypeScript --json
python scripts/agent_skill_discovery.py "api backend rest" --domain backend --json

# Search both GitHub repositories and Skill Issue references for a task.
python scripts/recommend.py "react frontend performance" --language typescript --skills --json
python scripts/recommend.py "mobile ui design" --skills --websites --json
```

The `--skills` flag adds `skillDiscovery` separately from GitHub
`recommendations` and website `websiteRecommendations`. It never overrides
hard repository filters, alters the selected stack, downloads scripts or
contributes items to the Production-OS dispatch queue.

## Required security and compatibility review

1. Check that an original skill actually exists at the linked repository and
   that the applicable license permits the intended use. Repository-level
   license metadata alone may not cover every skill or third-party asset.
2. Review its full `SKILL.md`, referenced scripts, update hooks,
   dependencies and permissions at a **pinned commit**; reject prompt
   injection, credential harvesting, unsafe shell instructions and unbounded
   external-network access.
3. Install selectively in a sandbox or approved development environment, not
   blindly across all projects or on production servers. Never execute
   remote `curl | sh`, `npx` or plugin install commands merely because they
   are presented by the directory.
4. Run the relevant checks in the actual target repository and establish that
   the skill was invoked for its intended task and materially improved the
   workflow before retaining it. Do not alter production code or grant extra
   tokens/permissions just to satisfy a suggested skill.
5. Treat skill updates as new code that requires review. Keep the public
   portfolio report free of private repository source, credentials and other
   confidential task data.

The daily scanner stays **read-only for skills** and may run safely even while
Production-OS autonomous integration dispatch is halted due to insufficient
verified provider capacity.
