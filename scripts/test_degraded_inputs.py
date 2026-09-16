#!/usr/bin/env python3
"""Regression tests for degraded, malformed, empty, and large pipeline inputs."""
import importlib.util
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOW=datetime(2026,9,15,tzinfo=timezone.utc)


def load(name):
    path=ROOT/"scripts"/f"{name}.py"
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


evaluation=load("evaluate_candidates")
health=load("health_score")
memory=load("filter_discovery_memory")
history=load("update_history")
cache_history=load("update_cache_health_history")

# Malformed candidate metadata must degrade to conservative defaults, not crash.
bad={
    "repo":"broken/types",
    "description":None,
    "language":None,
    "discoveryScore":"not-a-number",
    "stars":"oops",
    "watchers":"",
    "forks":None,
    "openIssues":"NaN",
    "contributors":"unknown",
    "topics":None,
    "matchedTargets":None,
    "latestRelease":"broken",
    "pushedAt":123,
    "createdAt":{},
    "hasDiscussions":"unknown",
}
result=evaluation.evaluate(bad,NOW)
assert result["decision"]=="reject"
assert 0.0<=result["evaluationScore"]<=100.0
assert all(0.0<=v<=100.0 for v in result["scoreBreakdown"].values())

# Sorting and volume must tolerate numeric strings and malformed rows.
rows=[]
for i in range(1000):
    rows.append({
        "repo":f"bulk/repo-{i:04d}",
        "discoveryScore":"60",
        "stars":str(i),
        "watchers":"0",
        "forks":"0",
        "openIssues":"0",
        "topics":[],
        "matchedTargets":[],
    })
rows.append(bad)
bulk=evaluation.evaluate_all({"repositories":rows},NOW)
assert bulk["candidates"]==1001
assert sum(bulk["counts"].values())==1001
assert evaluation.evaluate_all({"repositories":[]},NOW)["candidates"]==0

# Health scoring must tolerate corrupt scalar metadata conservatively.
h=health.health_score({
    "score":"invalid",
    "github":{"stars":"invalid","forks":None,"archived":False,"disabled":False,"pushedAt":123},
},NOW)
assert h["status"] in {"weak","watch","healthy"}
assert 0.0<=h["score"]<=100.0

# Discovery memory must survive malformed historical fingerprints and targets.
row={"repo":"broken/memory","decision":"review","evaluationScore":"bad","stars":"bad","pushedAt":None,"matchedTargets":None}
old={"schemaVersion":1,"candidates":{"broken/memory":{"fingerprint":{"decision":"review","score":"also-bad","stars":None,"pushedAt":None,"targets":[]}}}}
filtered,updated=memory.apply({"repositories":[row]},old)
assert filtered["candidates"]==0
assert filtered["suppressedUnchanged"]==1
assert "broken/memory" in updated["candidates"]

# Persistent memory/history files are caches/state: corrupt JSON or wrong shapes reset safely.
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    bad_memory=td/"memory.json"; bad_memory.write_text("{not-json")
    bad_history=td/"history.json"; bad_history.write_text("[]")
    assert memory.load_memory(bad_memory)==memory.empty_memory()
    assert history.load_history(bad_history)==history.empty_history()

# In-memory malformed history shapes must also recover.
updated_history=history.update(
    {"schemaVersion":1,"repositories":[]},
    {"repositories":[{"repo":"a/x","github":{"stars":1,"forks":0}}]},
    {"repositories":[]},
    now=NOW,
)
assert isinstance(updated_history["repositories"],dict)
assert "a/x" in updated_history["repositories"]

# Cache-health report metrics may be absent or malformed without killing persistence.
point=cache_history.point_from_report({"status":"watch","metrics":{"logicalRequests":"bad","networkFetchRate":"bad"}},"2026-09-15")
assert point["logicalRequests"]==0
assert point["networkFetchRate"]==0.0

print("OK: degraded-input robustness tests passed")
