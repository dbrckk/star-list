#!/usr/bin/env python3
import importlib.util
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"evaluate_candidates.py"
spec=importlib.util.spec_from_file_location("evaluate",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
strong={"repo":"a/ai-agents","description":"AI agents framework","language":"Python","discoveryScore":75,"stars":5000,"forks":500,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","createdAt":"2020-01-01T00:00:00Z","latestRelease":{"publishedAt":"2026-08-01T00:00:00Z"},"contributors":50,"watchers":200,"openIssues":20,"hasDiscussions":True,"topics":["ai","agents"],"matchedTargets":[{"target":"ai"},{"target":"agents"}]}
weak={"repo":"b/y","description":"unrelated tool","language":"C","discoveryScore":50,"stars":20,"forks":0,"license":None,"pushedAt":"2020-01-01T00:00:00Z","matchedTargets":[{"target":"mobile"}]}
sparse={"repo":"c/ai-tool","description":"AI tool","language":"Python","discoveryScore":60,"stars":100,"matchedTargets":[{"target":"ai"}]}
sparse_high={"repo":"c/high-score-ai","description":"AI framework","language":"Python","discoveryScore":100,"stars":100,"matchedTargets":[{"target":"ai"}]}
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW); c=mod.evaluate(sparse,NOW); d=mod.evaluate(sparse_high,NOW)
assert a["decision"]=="accept" and a["evaluationScore"]>=80
assert b["decision"]=="reject" and b["evaluationScore"]<55
assert a["evaluationScore"]>b["evaluationScore"]
assert a["textFit"]==1.0 and b["textFit"]==0.0
assert "mature>=2y" in a["reasons"] and "recent-release" in a["reasons"] and "broad-contributor-base" in a["reasons"]
assert "controlled-issue-load" in a["reasons"] and "community-discussions" in a["reasons"]
assert a["openIssueRatio"] == 0.004

components={"fit","activity","adoption","maturity","maintenance"}
assert set(a["scoreBreakdown"])==components
assert set(b["scoreBreakdown"])==components
assert all(0.0<=value<=100.0 for value in a["scoreBreakdown"].values())
assert a["scoreBreakdown"]["fit"]>b["scoreBreakdown"]["fit"]
assert a["scoreBreakdown"]["activity"]>b["scoreBreakdown"]["activity"]
assert a["scoreBreakdown"]["adoption"]>b["scoreBreakdown"]["adoption"]
assert a["scoreBreakdown"]["maturity"]>b["scoreBreakdown"]["maturity"]
assert a["scoreBreakdown"]["maintenance"]>=b["scoreBreakdown"]["maintenance"]
assert a["evaluationConfidence"]=="high"
assert c["evaluationConfidence"]=="low"
assert c["decision"]==mod.evaluate(sparse,NOW)["decision"]

# Low-confidence metadata can never produce automatic acceptance.
assert d["evaluationScore"]>=mod.ACCEPT_THRESHOLD
assert d["evaluationConfidence"]=="low"
assert d["decision"]=="review"
assert "low-confidence-cap" in d["reasons"]

# Decision boundaries are part of the public calibration contract.
assert hasattr(mod,"ACCEPT_THRESHOLD") and mod.ACCEPT_THRESHOLD==80.0
assert hasattr(mod,"REVIEW_THRESHOLD") and mod.REVIEW_THRESHOLD==55.0
assert hasattr(mod,"decision_for_score")
assert mod.decision_for_score(80.0)=="accept"
assert mod.decision_for_score(79.9)=="review"
assert mod.decision_for_score(55.0)=="review"
assert mod.decision_for_score(54.9)=="reject"

calibration_cases=[
    ({"repo":"cal/excellent-agent","description":"AI agents orchestration framework","language":"Python","discoveryScore":68,"stars":2500,"forks":200,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","createdAt":"2021-01-01T00:00:00Z","latestRelease":{"publishedAt":"2026-08-15T00:00:00Z"},"contributors":30,"watchers":150,"openIssues":20,"hasDiscussions":True,"topics":["ai","agents"],"matchedTargets":[{"target":"ai"},{"target":"agents"}]},"accept"),
    ({"repo":"cal/python-backtest","description":"Python backtesting toolkit","language":"Python","discoveryScore":48,"stars":350,"forks":20,"license":"Apache-2.0","pushedAt":"2026-04-01T00:00:00Z","createdAt":"2023-01-01T00:00:00Z","latestRelease":{"publishedAt":"2025-10-01T00:00:00Z"},"contributors":6,"watchers":15,"openIssues":25,"hasDiscussions":False,"topics":["backtesting"],"matchedTargets":[{"target":"backtesting"}]},"review"),
    ({"repo":"cal/mobile-ui","description":"mobile ui components","language":"Kotlin","discoveryScore":45,"stars":120,"forks":6,"license":"MIT","pushedAt":"2026-06-01T00:00:00Z","createdAt":"2025-01-01T00:00:00Z","contributors":3,"watchers":5,"openIssues":12,"hasDiscussions":False,"topics":["mobile"],"matchedTargets":[{"target":"mobile"}]},"review"),
    ({"repo":"cal/legacy","description":"legacy unrelated utility","language":"C","discoveryScore":58,"stars":40,"forks":0,"license":None,"pushedAt":"2022-01-01T00:00:00Z","createdAt":"2018-01-01T00:00:00Z","contributors":1,"watchers":0,"openIssues":50,"hasDiscussions":False,"topics":[],"matchedTargets":[{"target":"agents"}]},"reject"),
]
results=[mod.evaluate(repo,NOW) for repo,_ in calibration_cases]
for result,(_,expected) in zip(results,calibration_cases): assert result["decision"]==expected
assert results[0]["evaluationScore"]>results[1]["evaluationScore"]>results[2]["evaluationScore"]>results[3]["evaluationScore"]

print("OK: candidate evaluation tests passed")
