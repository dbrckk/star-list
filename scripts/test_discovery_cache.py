#!/usr/bin/env python3
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

cache = {"schemaVersion": 1, "entries": {}}
url = "https://api.github.test/repos/a/x"
mod.cache_put(cache, url, {"ok": True}, {"Link": "next"}, now=1000)

fresh = mod.cache_get(cache, url, ttl_seconds=60, now=1030)
assert fresh == ({"ok": True}, {"Link": "next"})

expired = mod.cache_get(cache, url, ttl_seconds=60, now=1061)
assert expired is None
assert mod.cache_get(cache, "missing", ttl_seconds=60, now=1030) is None

cached_data, cached_headers = mod.api_json(url, {}, attempts=1, cache=cache, ttl_seconds=60, now=1030)
assert cached_data == {"ok": True}
assert cached_headers == {"Link": "next"}

# Expired data may be used only as a bounded fallback when GitHub/network is unavailable.
stale_url = "https://api.github.test/repos/stale/x"
mod.cache_put(cache, stale_url, {"stale": True}, {"ETag": "old"}, now=1000)
real_urlopen = mod.urlopen

def offline(*args, **kwargs):
    raise OSError("network unavailable")

mod.urlopen = offline
try:
    stale_data, stale_headers, source = mod.api_json(
        stale_url, {}, attempts=1, cache=cache, ttl_seconds=60,
        stale_max_seconds=3600, now=2000, return_source=True,
    )
    assert stale_data == {"stale": True}
    assert stale_headers == {"ETag": "old"}
    assert source == "stale-cache"

    too_old_failed = False
    try:
        mod.api_json(
            stale_url, {}, attempts=1, cache=cache, ttl_seconds=60,
            stale_max_seconds=300, now=2000, return_source=True,
        )
    except OSError:
        too_old_failed = True
    assert too_old_failed, "cache older than stale_max_seconds must not be used"
finally:
    mod.urlopen = real_urlopen

with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "cache.json"
    mod.save_cache(path, cache)
    loaded = mod.load_cache(path)
    assert loaded == cache
    assert mod.load_cache(Path(td) / "missing.json") == {"schemaVersion": 1, "entries": {}}

print("OK: discovery cache tests passed")
