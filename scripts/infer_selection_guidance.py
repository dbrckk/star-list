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
    for cap in caps:
        if cap == "vector-animation":
            phrase = (
                "vector search and embedding retrieval"
                if repo.get("domain") == "ai_memory"
                else "vector animation"
            )
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


def enrich(repos, tier="recommended"):
    changed = 0
    for repo in repos:
        if repo.get("tier") != tier:
            continue
        missing_best = not repo.get("bestFor")
        missing_avoid = not repo.get("avoidWhen")
        if not (missing_best or missing_avoid):
            continue
        best, avoid = infer_guidance(repo)
        if missing_best:
            repo["bestFor"] = best
        if missing_avoid:
            repo["avoidWhen"] = avoid
        repo["guidanceSource"] = "inferred"
        changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description="Backfill deterministic selection guidance.")
    parser.add_argument("--tier", default="recommended", choices=["core","recommended","specialized","audit"])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    data = json.loads(CATALOG.read_text())
    changed = enrich(data.get("repositories", []), tier=args.tier)
    print(json.dumps({"tier": args.tier, "changed": changed}, indent=2))
    if args.write and changed:
        CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
