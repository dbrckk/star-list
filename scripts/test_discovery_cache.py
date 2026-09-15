#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

cache = {"schemaVersion": 1, "entries": {}}
mod.cache_put(cache, "https://api.github.test/repos/a/x", {"ok": True}, {"Link": "next"}, now=1000)

fresh = mod.cache_get(cache, "https://api.github.test/repos/a/x", ttl_seconds=60, now=1030)
assert fresh == ({"ok": True}, {"Link": "next"})

expired = mod.cache_get(cache, "https://api.github.test/repos/a/x", ttl_seconds=60, now=1061)
assert expired is None

assert mod.cache_get(cache, "missing", ttl_seconds=60, now=1030) is None
print("OK: discovery cache tests passed")
