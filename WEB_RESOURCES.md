# Web resources: design, animation, 3D and AI builders

The GitHub repository catalog in [`catalog.json`](catalog.json) is unchanged.
These **10 websites** are curated alongside it in [`websites.json`](websites.json);
they are not GitHub repositories, software licenses or automatically installable
libraries. Access plans, implementation rights and attribution are separate from
the ability to browse a page.

| Resource | Link | Main use | Access | Reuse policy |
| --- | --- | --- | --- | --- |
| Scrolltide | [scrolltide.co](https://www.scrolltide.co/) | Scroll-driven/3D website prompts and source templates | Freemium, mainly paid | Paid/licensed material; inspect the template terms |
| Awwwards | [awwwards.com](https://www.awwwards.com/) | Award-winning websites, visual benchmarks | Freemium | Inspiration only; third-party work |
| Recent (formerly Godly) | [recent.design](https://recent.design/) | Curated web, UI, branding and motion design | Free browsing | Inspiration only; original [godly.website](https://godly.website/) now redirects |
| 60fps | [60fps.design](https://60fps.design/) | Mobile/web UI animations and micro-interactions | Freemium | Inspiration only; do not reproduce assets without rights |
| 21st.dev | [21st.dev](https://21st.dev/) | React/Tailwind component discovery | Freemium | Check each community component's author/license |
| Aceternity UI | [ui.aceternity.com](https://ui.aceternity.com/) | Animated React + Tailwind components | Freemium | Review the Aceternity/third-party component terms |
| Magic UI | [magicui.design](https://magicui.design/) | Animated landing-page UI components | Freemium | Check source/component or premium template terms |
| Three.js | [threejs.org](https://threejs.org/) | JavaScript/WebGL/WebGPU 3D rendering | Free | Open-source core; independently license models/textures |
| Shadertoy | [shadertoy.com](https://www.shadertoy.com/) | GLSL shader experiments and visual effects | Free browsing | Creator-specific shader rights and performance review |
| Lovable | [lovable.dev](https://lovable.dev/) | AI-generated website/application prototypes | Freemium | Hosted service; check export/data/usage plans |

## Search repositories and relevant websites together

```bash
python scripts/recommend.py "3d scroll animation website" --websites --top-websites 10
python scripts/recommend.py "react animated ui components" --websites --json
python scripts/recommend.py "mobile ui motion animation" --websites --json
python scripts/validate_json_contract.py schemas/websites.schema.json websites.json
```

The opt-in `--websites` flag adds `websiteRecommendations` separately from
`recommendations` in JSON output. Its site scores are **relevance cues**, not
GitHub quality/security scores. All website results carry
`integrationEligible: false`. The normal GitHub repository ranking, strict
repository filters, stacks, Stars sync and Production-OS integration handoffs
remain unchanged.

`--top-websites` controls the number of references (default 5). The normal
repository `--platform`, `--language`, `--self-hosted`, license and similar
hard filters **do not certify web inspiration pages**. A site may be useful
for visual research without matching the project's runtime.

## Operating policy

- A link is not an open-source license. Verify individual component/shader
  licenses, source availability, third-party images, fonts and trademarks
  before any commercial reuse.
- Paid content remains paid; a free preview is not permission to scrape,
  bypass access controls or redistribute premium prompts/templates.
- No copying other websites verbatim without rights. Use galleries for design
  direction, then create original implementation and assets.
- Future website additions should use canonical HTTPS URLs, stable unique IDs,
  descriptive tags, access expectations and an explicit `reuse` policy.
  Validate against [`schemas/websites.schema.json`](schemas/websites.schema.json).
- Website entries are not auto-dispatched into target repositories. After
  selecting a compatible implementation, ordinary target CI, security review
  and the project's approval gates continue to apply.
