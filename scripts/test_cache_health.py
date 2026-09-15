#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_cache_health.py"
spec = importlib.util.spec_from_file_location("cache_health", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

healthy = mod.analyze({
    "logicalRequests": 20,
    "freshCacheHits": 10,
    "notModifiedHits": 5,
    "staleFallbacks": 0,
    "networkFetches": 5,
    "apiCallAvoidanceRate": 0.5,
    "bodyReuseRate": 0.75,
})
assert healthy["status"] == "healthy"
assert healthy["findings"] == []

watch = mod.analyze({
    "logicalRequests": 20,
    "freshCacheHits": 3,
    "notModifiedHits": 2,
    "staleFallbacks": 1,
    "networkFetches": 14,
    "apiCallAvoidanceRate": 0.15,
    "bodyReuseRate": 0.30,
})
assert watch["status"] == "watch"
assert "low-cache-efficiency" in watch["findings"]

degraded = mod.analyze({
    "logicalRequests": 20,
    "freshCacheHits": 1,
    "notModifiedHits": 1,
    "staleFallbacks": 4,
    "networkFetches": 14,
    "apiCallAvoidanceRate": 0.05,
    "bodyReuseRate": 0.30,
})
assert degraded["status"] == "degraded"
assert "excessive-stale-fallbacks" in degraded["findings"]
assert "high-network-dependence" in degraded["findings"]

print("OK: cache health tests passed")
