#!/usr/bin/env python3
"""Backfill conservative selection guidance from existing curated catalog metadata."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"

CAPABILITY_BEST_FOR = {
    "agent": "agentic workflows",
    "coding": "agentic coding tasks",
    "tool-use": "tool-using agent workflows",
    "web-retrieval": "browser and web retrieval",
    "machine-learning": "machine-learning workflows",
    "ml": "machine-learning experiments",
    "alpha": "quantitative alpha research",
    "memory": "retrieval and persistent-memory workflows",
    "backtesting": "strategy backtesting",
    "backtest": "strategy backtesting",
    "risk": "risk analysis",
    "regime": "market regime analysis",
    "mobile": "mobile application development",
    "market-data": "market-data ingestion",
    "data": "data pipelines",
    "documentation": "technical documentation",
    "docs-site": "documentation websites",
    "database": "application data persistence",
    "typescript": "TypeScript application development",
    "portfolio": "portfolio construction and analysis",
    "security-testing": "authorized security testing",
    "automation": "workflow automation",
    "voice-audio": "speech and audio processing",
    "osint": "open-source intelligence research",
    "macro": "macroeconomic analysis",
    "optimization": "optimization workflows",
    "forecasting": "forecasting models",
    "game-development": "game development",
    "backend": "backend services",
    "kubernetes": "Kubernetes operations",
    "deployment": "application deployment",
    "observability": "monitoring and observability",
    "sandbox": "isolated code execution",
    "execution": "trading execution systems",
    "diagnostic": "diagnostics and analysis",
    "xauusd": "XAUUSD trading research",
    "rendering": "graphics rendering",
    "rag": "retrieval-augmented generation",
    "api-documentation": "API documentation",
    "openapi": "OpenAPI workflows",
    "changelog": "changelog automation",
    "release-automation": "release automation",
    "backend-as-a-service": "backend-as-a-service applications",
    "orm": "database ORM workflows",
    "graphql": "GraphQL APIs",
    "auth": "authentication and identity",
    "ui-components": "reusable UI component systems",
    "design-system": "design systems",
    "css": "frontend styling systems",
    "frontend": "frontend application development",
    "frontend-build": "frontend build pipelines",
    "bundler": "JavaScript bundling",
    "static-analysis": "static analysis",
    "security-scanning": "security scanning",
    "cache": "application caching",
    "messaging": "messaging systems",
    "workflow": "workflow orchestration",
    "image-generation": "image-generation workflows",
    "diffusion": "diffusion-model workflows",
    "fine-tuning": "model fine-tuning",
    "llm-training": "LLM training",
    "local-models": "local model workflows",
    "api-directory": "API discovery and reference",
    "data-sources": "data-source discovery",
    "windows-automation": "Windows administration automation",
    "system-tuning": "Windows system tuning",
    "object-storage": "object storage",
    "distributed-storage": "distributed storage systems",
    "3d": "3D application development",
    "webgl": "WebGL rendering",
    "react": "React application development",
    "accessibility": "accessibility testing and remediation",
    "testing": "automated testing",
    "github-actions": "GitHub Actions workflows",
    "local-ci": "local CI validation",
    "build-system": "build automation",
    "ci-cd": "CI/CD pipelines",
    "containers": "container workflows",
    "runtime": "container runtime operations",
    "iac": "infrastructure as code",
    "infrastructure": "infrastructure management",
    "ast": "AST-based code analysis",
    "code-search": "code search and indexing",
    "refactoring": "large-scale code refactoring",
    "profiling": "performance profiling",
    "python": "Python development",
    "video": "video-generation workflows",
    "code-quality": "code-quality automation",
    "particles": "particle effects",
}

DOMAIN_AVOID_WHEN = {
    "ai_agents": "simple deterministic scripts without agent orchestration",
    "ai_memory": "stateless applications with no retrieval or memory needs",
    "ai_media": "non-generative media workflows",
    "software_engineering": "non-development workflows",
    "web_frontend": "backend-only services",
    "backend": "frontend-only UI work",
    "mobile": "web-only applications",
    "graphics": "non-visual workloads",
    "game_dev": "non-game application development",
    "trading": "non-financial applications",
    "cybersecurity": "non-security workloads",
    "data_ml": "deterministic non-ML tasks",
    "devops": "local-only scripts with no deployment or operations needs",
    "productivity": "specialized low-level systems work",
    "other": "tasks outside the repository's documented scope",
}


def _humanize(value):
    return value.replace("_", " ").replace("-", " ").strip()


def infer_guidance(repo):
    caps = list(dict.fromkeys(repo.get("capabilities", []) + repo.get("roles", [])))
    best = []
    domain = repo.get("domain")
    for cap in caps:
        if cap == "memory":
            if domain == "ai_memory":
                phrase = "retrieval and persistent-memory workflows"
            elif domain == "ai_agents":
                phrase = "agent memory and context retention"
            elif domain == "productivity":
                phrase = "knowledge retention and reference workflows"
            elif domain == "graphics":
                continue
            else:
                phrase = "stateful memory workflows"
        elif cap == "vector-animation":
            if domain == "ai_memory":
                phrase = "vector search and embedding retrieval"
            elif domain == "graphics":
                phrase = "vector animation"
            else:
                continue
        elif cap in {"market-data", "xauusd", "alpha", "risk", "regime", "backtesting", "backtest", "execution", "portfolio", "macro"} and domain not in {"trading", "data_ml"}:
            continue
        elif cap == "mobile" and domain == "game_dev":
            continue
        else:
            phrase = CAPABILITY_BEST_FOR.get(cap)
        if phrase and phrase not in best:
            best.append(phrase)
        if len(best) >= 3:
            break

    if not best and caps:
        best.append(_humanize(caps[0]) + " workflows")
    if not best:
        best.append(_humanize(repo.get("category", "general-purpose tooling")).lower())

    avoid = []
    if repo.get("resourceLevel") == "high":
        avoid.append("low-resource environments")
    if repo.get("integrationComplexity") == "high":
        avoid.append("projects requiring minimal setup and operational complexity")
    domain_avoid = DOMAIN_AVOID_WHEN.get(repo.get("domain"))
    if domain_avoid and domain_avoid not in avoid:
        avoid.append(domain_avoid)
    if not avoid:
        avoid.append("tasks outside the repository's documented scope")

    return best[:3], avoid[:2]


def enrich(repos, tier="recommended", refresh_inferred=False):
    changed = 0
    for repo in repos:
        if repo.get("tier") != tier:
            continue
        missing_best = not repo.get("bestFor")
        missing_avoid = not repo.get("avoidWhen")
        refresh = refresh_inferred and repo.get("guidanceSource") == "inferred"
        if not (missing_best or missing_avoid or refresh):
            continue
        best, avoid = infer_guidance(repo)
        if missing_best or refresh:
            repo["bestFor"] = best
        if missing_avoid or refresh:
            repo["avoidWhen"] = avoid
        repo["guidanceSource"] = "inferred"
        changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description="Backfill deterministic selection guidance.")
    parser.add_argument("--tier", default="recommended", choices=["core","recommended","specialized","audit"])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh-inferred", action="store_true")
    args = parser.parse_args()

    data = json.loads(CATALOG.read_text())
    changed = enrich(data.get("repositories", []), tier=args.tier, refresh_inferred=args.refresh_inferred)
    print(json.dumps({"tier": args.tier, "changed": changed}, indent=2))
    if args.write and changed:
        CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
