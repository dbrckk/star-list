#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_cache_health_history.py"
spec = importlib.util.spec_from_file_location("cache_history", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

history={"schemaVersion":1,"points":[
    {"date":"2026-09-01","apiCallAvoidanceRate":0.75,"bodyReuseRate":0.85,"networkFetchRate":0.25,"staleFallbackRate":0.00,"status":"healthy"},
    {"date":"2026-09-08","apiCallAvoidanceRate":0.55,"bodyReuseRate":0.70,"networkFetchRate":0.40,"staleFallbackRate":0.00,"status":"healthy"},
]}
current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.32,"bodyReuseRate":0.55,"networkFetchRate":0.60,"staleFallbackRate":0.05}}
updated,trend=mod.update(history,current,date="2026-09-15",max_points=26)
assert len(updated["points"])==3
assert trend["direction"]=="declining"
assert "declining-cache-efficiency" in trend["findings"]
assert "rising-network-dependence" in trend["findings"]
assert trend["apiCallAvoidanceDelta"]==-0.43
assert trend["networkFetchDelta"]==0.35

for i in range(40):
    updated,_=mod.update(updated,current,date=f"2026-10-{(i%28)+1:02d}",max_points=26)
assert len(updated["points"])==26

print("OK: cache health history tests passed")
