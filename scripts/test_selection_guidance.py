#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "infer_selection_guidance.py"
spec = importlib.util.spec_from_file_location("infer_selection_guidance", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

repos = [
    {
        "repo": "x/agent",
        "tier": "recommended",
        "domain": "ai_agents",
        "capabilities": ["agent", "web-retrieval"],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
    },
    {
        "repo": "x/vector-db",
        "tier": "recommended",
        "domain": "ai_memory",
        "capabilities": ["memory", "vector-animation"],
        "resourceLevel": "high",
        "integrationComplexity": "high",
    },
    {
        "repo": "x/curated",
        "tier": "recommended",
        "domain": "backend",
        "capabilities": ["database"],
        "bestFor": ["curated best"],
        "avoidWhen": ["curated avoid"],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
    },
    {
        "repo": "x/core",
        "tier": "core",
        "domain": "backend",
        "capabilities": ["database"],
        "resourceLevel": "medium",
        "integrationComplexity": "medium",
    },
]

changed = mod.enrich(repos)
assert changed == 2
assert repos[0]["bestFor"] == ["agentic workflows", "browser and web retrieval"]
assert repos[0]["avoidWhen"] == ["simple deterministic scripts without agent orchestration"]
assert repos[0]["guidanceSource"] == "inferred"
assert "vector search and embedding retrieval" in repos[1]["bestFor"]
assert "low-resource environments" in repos[1]["avoidWhen"]
assert "projects requiring minimal setup and operational complexity" in repos[1]["avoidWhen"]
assert repos[2]["bestFor"] == ["curated best"]
assert "guidanceSource" not in repos[2]
assert "bestFor" not in repos[3]
print("OK: selection guidance inference tests passed")
