#!/usr/bin/env python3
"""Evidence-only advisory routing for catalog entries whose domain is unknown.

Neither text clues nor GitHub descriptions authorize installation or execution.
Keep named/curated domains authoritative and do not overwrite catalog metadata.
"""
import re

# Only explicit technical capabilities or unambiguous *task phrases* qualify.
# Generic words ("AI", "agent", "web", "app", "automation") never qualify alone.
CAPABILITY_DOMAIN_SIGNALS = {
    "ai_media": {
        "text2music", "text-to-music", "text-to-video", "text-to-image",
        "video-generation", "video-recording", "video-editing", "text2video",
        "image-generation", "voice-audio", "audio-generation", "voice-cloning",
        "speech-synthesis", "tts", "music-generation", "diffusion",
    },
    "ai_agents": {
        "mcp", "agent-sdk", "coding-agent", "agent-runtime", "agent-framework",
        "llm-agent", "multi-agent", "agent-orchestration",
    },
    "game_dev": {
        "godot", "roblox", "luau", "unity", "unreal", "game-development",
        "game-engine", "gameplay", "game-assets",
    },
    "graphics": {
        "3d-modeling", "rigging", "shader", "shaders", "texture-generation",
        "vector-animation", "svg", "blender", "3d-rendering", "motion-capture",
    },
    "mobile": {
        "android", "android-sdk", "ios", "jetpack-compose", "flutter",
        "mobile-development", "android-app",
    },
    "cybersecurity": {
        "pentest", "penetration-testing", "security-scanning", "osint",
        "vulnerability-scanning", "cve", "rce", "redteam", "red-team",
        "bug-bounty", "security-testing",
    },
    "trading": {
        "backtesting", "backtest", "quantitative-trading", "trading",
        "market-data", "forex", "xauusd", "stock-trading",
    },
    "web_frontend": {
        "react", "vue", "svelte", "frontend", "webgl", "ui-components",
        "css", "tailwind", "nextjs",
    },
    "backend": {
        "database", "orm", "graphql", "backend", "postgresql",
        "fastapi", "supabase",
    },
    "devops": {
        "kubernetes", "docker", "ci-cd", "infrastructure-as-code",
        "observability", "terraform",
    },
    "software_engineering": {
        "code-search", "static-analysis", "refactoring", "test-runner",
        "code-review", "code-quality", "repository-analysis",
    },
    "ai_memory": {
        "rag", "vector-database", "vector-search", "retrieval-augmented-generation",
        "embeddings",
    },
    "data_ml": {
        "fine-tuning", "llm-training", "machine-learning", "ml-training",
        "dataset-analysis",
    },
}
# A title/description is *less* trustworthy than a structured capability.
# Match task-specific phrases, never freeform single-topic descriptions.
DESCRIPTION_DOMAIN_PHRASES = {
    "ai_media": (
        "music generation", "video generation", "image generation", "video editing",
        "video editor", "audio processing", "speech synthesis", "voice cloning",
        "short drama", "text to video", "text to image", "text to music",
        "generate video", "generate music", "generate images", "video production",
    ),
    "ai_agents": (
        "agent sdk", "agent framework", "agent orchestration", "mcp server",
        "model context protocol", "coding agent", "autonomous coding",
    ),
    "game_dev": (
        "godot plugin", "godot engine", "roblox studio", "luau scripting",
        "game engine", "game development", "unity game",
    ),
    "graphics": (
        "3d modeling", "3d rendering", "shader effects", "skeletal animation",
        "motion capture", "vector animation", "3d model",
    ),
    "mobile": (
        "android application", "android sdk", "ios application", "flutter application",
        "android app", "mobile app",
    ),
    "cybersecurity": (
        "penetration testing", "vulnerability scanning", "bug bounty",
        "security testing", "red team", "remote code execution",
        "offensive security",
    ),
    "trading": (
        "trading bot", "backtesting framework", "market data",
        "stock trading", "crypto trading", "forex trading",
    ),
    "web_frontend": (
        "frontend framework", "react components", "vue components",
        "web ui", "website builder",
    ),
    "backend": (
        "database server", "postgresql database", "backend service",
        "api server", "graph ql", "graphql api",
    ),
    "devops": (
        "infrastructure as code", "kubernetes deployment", "docker orchestration",
        "ci cd pipeline", "continuous integration",
    ),
    "software_engineering": (
        "static code analysis", "code search", "code refactoring", "automated testing",
        "repository analysis",
    ),
    "ai_memory": (
        "retrieval augmented generation", "vector database", "semantic search",
        "agent memory",
    ),
    "data_ml": (
        "machine learning", "model fine tuning", "model training",
        "dataset analysis",
    ),
}


def _normalized(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def advisory_domain_evidence(item):
    """Return {domain: supporting evidence strings}, for advisory routing only."""
    domain = item.get("domain")
    if isinstance(domain, str) and domain not in ("other", "unknown", ""):
        return {domain: ["catalog-domain"]}
    caps = {str(v).strip().casefold() for v in (
        (item.get("capabilities") or []) + (item.get("roles") or [])
    ) if isinstance(v, str)}
    # Structured capability labels may be overly broad or inaccurate. The
    # result is therefore advisory even if the label is an exact match.
    description = _normalized(" ".join(
        str(v)[:400] for v in (item.get("bestFor") or [])[:3] if isinstance(v, str)
    ))
    evidence = {}
    for name, signals in CAPABILITY_DOMAIN_SIGNALS.items():
        hits = sorted(caps & signals)
        if hits:
            evidence[name] = ["capability:" + h for h in hits[:3]]
    for name, phrases in DESCRIPTION_DOMAIN_PHRASES.items():
        matches = [s for s in phrases if re.search(
            r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", description
        )]
        if matches:
            evidence.setdefault(name, [])
            evidence[name].extend("description:" + m for m in sorted(matches)[:2])
    return evidence
