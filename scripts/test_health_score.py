#!/usr/bin/env python3
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "health_score.py"
spec = importlib.util.spec_from_file_location("health_score", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NOW = datetime(2026, 9, 15, tzinfo=timezone.utc)

active = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2026-09-10T00:00:00Z"}}
stale = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2023-01-01T00:00:00Z"}}
assert mod.health_score(active, NOW)["score"] > mod.health_score(stale, NOW)["score"]
assert mod.health_score({"github":{"archived":True}}, NOW)["status"] == "inactive"
assert mod.health_score({})["status"] == "unknown"
assert 0 <= mod.health_score(active, NOW)["score"] <= 100
print("OK: health score tests passed")
