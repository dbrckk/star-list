# Fifteen MCP servers from the Hermes Agent screenshot

Source: user-provided social-media screenshot (28 October 2026). These are **distinct GitHub repositories**, not new website-directory records. GitHub star totals in the screenshot are a snapshot, not a stable order or an endorsement.

At ingestion: **8 already indexed**, **7 newly registered** in [`catalog.json`](catalog.json). The original 8 were recategorized where needed. All 15 are tracked by the normal daily portfolio catalog scan.

| # | Repository | Function | Main review requirement |
|---|---|---|---|
| 1 | [Context7](https://github.com/upstash/context7) | Documentation retrieval | Version-aware library docs; verify provenance and API changes |
| 2 | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Browser debugging | Inspect Chrome pages and performance; never attach sensitive tabs |
| 3 | [Codebase Memory MCP](https://github.com/DeusData/codebase-memory-mcp) | Repository navigation | Local code knowledge; review index scope and privacy |
| 4 | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Web UI verification | MCP browser interactions; honor third-party website policies |
| 5 | [GitHub MCP Server](https://github.com/github/github-mcp-server) | GitHub operations | GitHub repo/PR/actions access; least-privilege token, review writes |
| 6 | [Context Mode](https://github.com/mksglu/context-mode) | Agent context | Reduce wasted agent context; confirm filtered content not hiding errors |
| 7 | [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) | 3D production | Generate or edit Blender scenes; inspect agent-supplied Python |
| 8 | [Code Review Graph](https://github.com/tirth8205/code-review-graph) | PR quality | Graph-based code impact and review; verify findings against source |
| 9 | [Serena](https://github.com/oraios/serena) | Code editing | Symbol-aware code search/refactoring; review diffs |
| 10 | [n8n-MCP](https://github.com/czlonkowski/n8n-mcp) | Workflow authoring | Discover n8n nodes and automation designs; instance/auth required for writes |
| 11 | [MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox) | Databases | Audited DB queries; restrict SQL/data scope and write permissions |
| 12 | [Xiaohongshu MCP](https://github.com/xpzouying/xiaohongshu-mcp) | Platform-specific | Social-platform adapter; cookies, ToS and no unauthorized posting/scraping |
| 13 | [Framelink Figma Context MCP](https://github.com/GLips/Figma-Context-MCP) | UI design | Authorized Figma design metadata; keep API keys secure |
| 14 | [Unity MCP](https://github.com/CoplayDev/unity-mcp) | Unity production | Control Unity editor; not compatible with Godot/Roblox runtime |
| 15 | [Apify MCP Server](https://github.com/apify/apify-mcp-server) | Authorized extraction | Access paid/hosted Apify Actors where site terms allow; control costs |

## Operational boundary

- A match is a **recommendation to review an MCP adapter**, never permission to install or embed its repository in an app. Every screenshot entry is explicitly listed in `EXTERNAL_MCP_SERVERS` and receives `adapter-review` or a stricter mode from the portfolio audit.
- An MCP tool can read files, execute browser/code/Blender operations, interact with GitHub and external APIs, or modify databases; all such operations require explicit target permissions and a reviewed configuration.
- Assign separate tokens and least-privilege scopes. Never put secrets, long-lived session cookies or database passwords into catalog metadata or commits.
- Paid hosted actors, remote inference, platform automation and publication require consent and budget checks. The source code licence **does not override a platform's terms of service**.
- Unity MCP requires a Unity Editor; Blender MCP requires desktop Blender. Neither is an automatic Godot/Roblox replacement. On Android-only environments, use a separately authorized desktop/cloud development host rather than claiming native mobile support.
- Newly added entries have independently checked canonical repositories and root licence files. GitHub star/fork/issue snapshots are intentionally not invented when API metadata is unavailable; health scores will remain `unknown` for those entries until an authenticated metadata refresh.

Example curated discovery: `python scripts/recommend.py "MCP code review memory context browser" --json`. For portfolio-specific advisory matches run `scripts/portfolio_daily.py` via the existing GitHub Actions workflow.
