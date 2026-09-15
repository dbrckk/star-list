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

baseline_history={"schemaVersion":1,"points":[
    {"date":"2026-08-04","apiCallAvoidanceRate":0.72,"bodyReuseRate":0.82,"networkFetchRate":0.28,"staleFallbackRate":0.00,"status":"healthy"},
    {"date":"2026-08-11","apiCallAvoidanceRate":0.69,"bodyReuseRate":0.79,"networkFetchRate":0.31,"staleFallbackRate":0.00,"status":"healthy"},
    {"date":"2026-08-18","apiCallAvoidanceRate":0.71,"bodyReuseRate":0.81,"networkFetchRate":0.29,"staleFallbackRate":0.00,"status":"healthy"},
    {"date":"2026-08-25","apiCallAvoidanceRate":0.70,"bodyReuseRate":0.80,"networkFetchRate":0.30,"staleFallbackRate":0.00,"status":"healthy"},
    {"date":"2026-09-01","apiCallAvoidanceRate":0.73,"bodyReuseRate":0.83,"networkFetchRate":0.27,"staleFallbackRate":0.00,"status":"healthy"},
]}
baseline_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.48,"bodyReuseRate":0.58,"networkFetchRate":0.52,"staleFallbackRate":0.00}}
_,baseline_trend=mod.update(baseline_history,baseline_current,date="2026-09-08",max_points=26)
assert baseline_trend["adaptiveBaseline"]["sampleSize"]==5
assert baseline_trend["adaptiveBaseline"]["apiCallAvoidanceRate"]==0.71
assert baseline_trend["adaptiveBaseline"]["networkFetchRate"]==0.29
assert baseline_trend["adaptiveBaseline"]["status"]=="anomalous"
assert baseline_trend["adaptiveBaseline"]["confidence"]=="low"
assert baseline_trend["adaptiveBaseline"]["confidenceScore"]==0.625
assert baseline_trend["adaptiveSeverity"]=="watch"
assert "below-adaptive-cache-baseline" in baseline_trend["findings"]
assert "above-adaptive-network-baseline" in baseline_trend["findings"]
assert "below-adaptive-body-reuse-baseline" in baseline_trend["findings"]
assert baseline_trend["direction"]=="declining"

confidence_points=[]
for i in range(9):
    confidence_points.append({
        "date":f"2026-07-{i+1:02d}",
        "apiCallAvoidanceRate":0.70,
        "bodyReuseRate":0.80,
        "networkFetchRate":0.30,
        "staleFallbackRate":0.00,
        "status":"healthy",
    })
assert mod.adaptive_baseline(confidence_points[:5])["confidence"]=="low"
assert mod.adaptive_baseline(confidence_points[:7])["confidence"]=="medium"
assert mod.adaptive_baseline(confidence_points[:9])["confidence"]=="high"
assert mod.adaptive_baseline(confidence_points[:5])["confidenceScore"]==0.5
assert mod.adaptive_baseline(confidence_points[:7])["confidenceScore"]==0.75
assert mod.adaptive_baseline(confidence_points[:9])["confidenceScore"]==1.0
assert "Baseline confidence: **low** (62.5%)" in mod.render_markdown(baseline_trend)

high_history={"schemaVersion":1,"points":[]}
for i in range(8):
    high_history["points"].append({
        "date":f"2026-07-{i+1:02d}",
        "apiCallAvoidanceRate":0.70,
        "bodyReuseRate":0.80,
        "networkFetchRate":0.30,
        "staleFallbackRate":0.00,
        "status":"healthy",
    })
high_updated,high_trend=mod.update(high_history,baseline_current,date="2026-09-08",max_points=26)
assert high_trend["adaptiveBaseline"]["confidence"]=="high"
assert high_trend["adaptiveBaseline"]["status"]=="anomalous"
assert high_trend["adaptiveSeverity"]=="degraded"
assert "Adaptive severity: **degraded**" in mod.render_markdown(high_trend)

assert mod.hysteresis_state("healthy","degraded")=="watch"
assert mod.hysteresis_state("degraded","degraded")=="degraded"
assert mod.hysteresis_state("degraded","healthy")=="watch"
assert mod.hysteresis_state("healthy","healthy")=="healthy"
assert high_trend["candidateSeverity"]=="degraded"
assert high_trend["alertState"]=="watch"
assert high_updated["points"][-1]["candidateSeverity"]=="degraded"

high_updated,high_trend_2=mod.update(high_updated,baseline_current,date="2026-09-15",max_points=26)
assert high_trend_2["candidateSeverity"]=="degraded"
assert high_trend_2["alertState"]=="degraded"

healthy_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.70,"bodyReuseRate":0.80,"networkFetchRate":0.30,"staleFallbackRate":0.00}}
high_updated,recovery_1=mod.update(high_updated,healthy_current,date="2026-09-22",max_points=26)
assert recovery_1["candidateSeverity"]=="healthy"
assert recovery_1["alertState"]=="watch"
high_updated,recovery_2=mod.update(high_updated,healthy_current,date="2026-09-29",max_points=26)
assert recovery_2["candidateSeverity"]=="healthy"
assert recovery_2["alertState"]=="healthy"
assert "Alert state: **healthy**" in mod.render_markdown(recovery_2)

for i in range(40):
    updated,_=mod.update(updated,current,date=f"2026-10-{(i%28)+1:02d}",max_points=26)
assert len(updated["points"])==26

print("OK: cache health history tests passed")
