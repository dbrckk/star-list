#!/usr/bin/env python3
"""Offline integration test for the discovery review pipeline."""
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
sys.path.insert(0,str(SCRIPTS))


def load(name):
    path=SCRIPTS/f"{name}.py"
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


coverage=load("analyze_coverage")
watchlists=load("build_discovery_watchlist")
discovery=load("discover_candidates")
evaluation=load("evaluate_candidates")
memory=load("filter_discovery_memory")
renderer=load("render_discovery_issue")

NOW=datetime(2026,9,15,tzinfo=timezone.utc)
catalog=[{
    "repo":"known/agent-core",
    "domain":"ai_agents",
    "tier":"recommended",
    "capabilities":["agents"],
    "score":9.4,
}]

report=coverage.analyze(catalog,min_domain=2,min_capability=2)
assert any(x["domain"]=="ai_agents" for x in report["domainGaps"])
assert any(x["capability"]=="agents" for x in report["capabilityGaps"])

watchlist=watchlists.build(report,max_items=10)
assert watchlist["items"]>=2

high={
    "full_name":"new/agent-grid",
    "html_url":"https://github.com/new/agent-grid",
    "description":"AI agents orchestration framework",
    "stargazers_count":20000,
    "forks_count":2000,
    "language":"Python",
    "license":{"spdx_id":"MIT"},
    "pushed_at":"2026-09-01T00:00:00Z",
    "archived":False,
    "disabled":False,
    "fork":False,
}
review={
    "full_name":"new/agent-helper",
    "html_url":"https://github.com/new/agent-helper",
    "description":"AI agents helper toolkit",
    "stargazers_count":100,
    "forks_count":1,
    "language":"Python",
    "license":None,
    "pushed_at":"2026-09-01T00:00:00Z",
    "archived":False,
    "disabled":False,
    "fork":False,
}


def fake_fetch(query,token=None,per_page=10,cache=None,ttl_seconds=0,stale_max_seconds=0,return_source=False,stats=None):
    payload={"items":[high,review]}
    return (payload,"fixture") if return_source else payload


def fake_enrich(repo,token=None,cache=None,ttl_seconds=0,stale_max_seconds=0,stats=None):
    if repo=="new/agent-grid":
        return {
            "topics":["ai","agents"],"watchers":250,"size":1200,"openIssues":25,
            "createdAt":"2020-01-01T00:00:00Z","homepage":None,"hasDiscussions":True,
            "latestRelease":{"tag":"v2.0.0","publishedAt":"2026-08-15T00:00:00Z"},"contributors":40,
        }
    return {
        "topics":["ai","agents"],"watchers":5,"size":300,"openIssues":8,
        "createdAt":"2025-01-01T00:00:00Z","homepage":None,"hasDiscussions":False,
        "latestRelease":{"tag":"v0.9.0","publishedAt":"2026-07-01T00:00:00Z"},"contributors":3,
    }


discovery.fetch=fake_fetch
discovery.enrich=fake_enrich
discovery.time.sleep=lambda _seconds: None

discovered=discovery.discover(watchlist,{"known/agent-core"},per_query=5)
assert discovered["candidates"]==2
assert discovered["errors"]==[]
assert all(len(row["matchedTargets"])>=2 for row in discovered["repositories"])

evaluated=evaluation.evaluate_all(discovered,NOW)
assert evaluated["counts"]=={"accept":1,"review":1,"reject":0}
by_repo={row["repo"]:row for row in evaluated["repositories"]}
assert by_repo["new/agent-grid"]["evaluationConfidence"]=="high"
assert by_repo["new/agent-grid"]["decision"]=="accept"
assert by_repo["new/agent-helper"]["decision"]=="review"

state={"schemaVersion":1,"candidates":{}}
visible,state=memory.apply(evaluated,state)
assert visible["candidates"]==2 and visible["suppressedUnchanged"]==0
assert set(state["candidates"])=={"new/agent-grid","new/agent-helper"}

body=renderer.render(visible)
assert "new/agent-grid" in body and "new/agent-helper" in body
assert "<!-- star-list-discovery-candidates -->" in body
assert "score profile:" in body

visible_again,state=memory.apply(evaluated,state)
assert visible_again["candidates"]==1
assert visible_again["suppressedUnchanged"]==1
assert visible_again["repositories"][0]["repo"]=="new/agent-grid"

print("OK: offline discovery pipeline integration passed")
