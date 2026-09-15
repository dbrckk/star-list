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
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW); c=mod.evaluate(sparse,NOW)
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

print("OK: candidate evaluation tests passed")
