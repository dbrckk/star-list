#!/usr/bin/env python3
import importlib.util
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

stats = mod.empty_cache_stats()
cache = {"schemaVersion": 1, "entries": {}}

fresh_url = "https://api.github.test/fresh"
mod.cache_put(cache, fresh_url, {"ok": "fresh"}, {"ETag": '"fresh"'}, now=1000)
mod.api_json(fresh_url, {}, attempts=1, cache=cache, ttl_seconds=60, now=1030, stats=stats)

etag_url = "https://api.github.test/etag"
mod.cache_put(cache, etag_url, {"ok": "etag"}, {"ETag": '"v1"'}, now=1000)
real_urlopen = mod.urlopen

def not_modified(req, *args, **kwargs):
    raise HTTPError(req.full_url, 304, "Not Modified", {"ETag": '"v1"'}, None)

mod.urlopen = not_modified
try:
    mod.api_json(etag_url, {}, attempts=1, cache=cache, ttl_seconds=60, now=2000, stats=stats)
finally:
    mod.urlopen = real_urlopen

stale_url = "https://api.github.test/stale"
mod.cache_put(cache, stale_url, {"ok": "stale"}, {}, now=1000)

def offline(*args, **kwargs):
    raise OSError("offline")

mod.urlopen = offline
try:
    mod.api_json(
        stale_url, {}, attempts=1, cache=cache, ttl_seconds=60,
        stale_max_seconds=3600, now=2000, stats=stats,
    )
finally:
    mod.urlopen = real_urlopen

class Response:
    def __init__(self): self.headers = {"ETag": '"network"'}
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return b'{"ok":"network"}'

network_url = "https://api.github.test/network"
mod.urlopen = lambda *args, **kwargs: Response()
try:
    mod.api_json(network_url, {}, attempts=1, cache=cache, ttl_seconds=60, now=2000, stats=stats)
finally:
    mod.urlopen = real_urlopen

summary = mod.finalize_cache_stats(stats)
assert summary["logicalRequests"] == 4
assert summary["freshCacheHits"] == 1
assert summary["notModifiedHits"] == 1
assert summary["staleFallbacks"] == 1
assert summary["networkFetches"] == 1
assert summary["apiCallAvoidanceRate"] == 0.25
assert summary["bodyReuseRate"] == 0.75

print("OK: cache telemetry tests passed")
