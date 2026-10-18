# Curated websites alongside GitHub repositories

The 10 sites below were contributed from a design-resource screenshot on
2026-10-18. They live in [`web-resources.json`](../web-resources.json),
**separately** from `catalog.json`, which remains a GitHub repository catalog.
The URLs and descriptions are manually curated. A site entry does not imply
its code, visuals, model weights, images or templates are open source.

| Website | Best use | Source usage |
| --- | --- | --- |
| [Scrolltide](https://www.scrolltide.co/) | Scroll-driven, cinematic 3D site prompts and templates | Paid; review the particular template license |
| [Awwwards](https://www.awwwards.com/) | Awarded web design and interaction inspiration | Reference only |
| [Recent (formerly Godly)](https://recent.design/) | Curated interfaces, branding, websites and motion | Reference only |
| [60fps](https://60fps.design/) | Mobile and web micro-interaction inspiration | Reference only |
| [21st.dev](https://21st.dev/) | React/Tailwind and shadcn-style UI components | Check each community component's license |
| [Aceternity UI](https://ui.aceternity.com/) | Animated React UI, heroes and backgrounds | Check Aceternity/item terms |
| [Magic UI](https://magicui.design/) | Animated React UI and landing-page components | Verify free vs premium licensing |
| [Three.js](https://threejs.org/) | 3D rendering documentation and open-source library | Core library MIT; check example assets |
| [Shadertoy](https://www.shadertoy.com/) | Interactive GLSL shader demos and experiments | Verify each shader author's rights |
| [Lovable](https://lovable.dev/) | Prompt-driven web and app prototypes | Hosted freemium builder, not a dependency |

The old `https://godly.website/` link now redirects to
`https://recent.design/`. Both are retained under one identity with an
alias to prevent duplicate records and keep old bookmarks discoverable.

## How to use this in star-list

Running the existing recommender now returns an additional **`webResources`**
field separate from `recommendations` (GitHub repositories) and
`recommendedStack` (compatible GitHub tool stacks):

```bash
python scripts/recommend.py "3d web shader animation" --json
python scripts/recommend.py "react tailwind animation components" --top-web 10 --json
python scripts/recommend.py "mobile ui motion animation" --json
python scripts/recommend.py "3d web" --no-web --json
```

Default: up to five website references. `--top-web N` changes the maximum;
`--top-web 0` or `--no-web` disables website suggestions. Website scoring
uses explicit topic, task and domain overlap. A broad domain alone does not
qualify a website. The repository recommender's existing hard filters,
GitHub rankings, stacks and default `recommendations` output are unchanged.

Website suggestions are **advisory and never automatically dispatched** to
Production-OS or counted as an integrated dependency. Every website record
has `autoIntegrate: false`. `usagePolicy` distinguishes inspiration-only
references from sites where copying particular source requires a separate
license review. The field `accessModel` is informational, **not** a promise
of unrestricted free access or an executable local component.

## Add additional sites safely

1. Check the actual canonical HTTPS website, redirects and intended use;
   keep old domains in `aliases` instead of adding duplicates.
2. Add one normalized record to `web-resources.json` with an honest access
   model, category, topic keywords and non-empty usage warnings.
3. Run both validators. URLs must be credential-free HTTPS locations and
   cannot be shared between records:

   ```bash
   python scripts/validate_json_contract.py schemas/web-resources.schema.json web-resources.json
   python scripts/validate_web_resources.py
   python scripts/test_recommend.py
   ```

4. Review the live site's terms and each component/asset license **before**
   introducing code into any project. Never interpret website discovery,
   subscriptions or gallery screenshots as a code reuse grant.

The website catalog requires no account, API token, crawler, paid provider,
background network request, or new Python dependency.
