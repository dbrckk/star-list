#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "recommend.py"

cases = [
    ("xauusd backtesting risk execution", {"trading"}),
    ("android vector animation", {"mobile", "graphics"}),
    ("autonomous coding agent memory observability", {"ai_agents", "ai_memory"}),
]

for query, expected_any in cases:
    out = subprocess.check_output([sys.executable, str(SCRIPT), query, "--json", "--top", "5"], text=True)
    data = json.loads(out)
    domains = set(data["inferredDomains"])
    assert domains & expected_any, (query, domains)
    assert data["recommendations"], query
    assert all("repo" in x and "selectionScore" in x for x in data["recommendations"])

print("OK: recommendation engine smoke tests passed")
