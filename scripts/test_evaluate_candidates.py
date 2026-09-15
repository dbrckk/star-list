#!/usr/bin/env python3
import importlib.util
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"evaluate_candidates.py"
spec=importlib.util.spec_from_file_location("evaluate",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
strong={"repo":"a/ai-agents","description":"AI agents framework","language":"Python","discoveryScore":75,"stars":5000,"forks":500,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","createdAt":"2020-01-01T00:00:00Z","latestRelease":{"publishedAt":"2026-08-01T00:00:00Z"},"contributors":50,"watchers":200,"topics":["ai","agents"],"matchedTargets":[{"target":"ai"},{"target":"agents"}]}
weak={"repo":"b/y","description":"unrelated tool","language":"C","discoveryScore":50,"stars":20,"forks":0,"license":None,"pushedAt":"2020-01-01T00:00:00Z","matchedTargets":[{"target":"mobile"}]}
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW)
assert a["decision"]=="accept" and a["evaluationScore"]>=80
assert b["decision"]=="reject" and b["evaluationScore"]<55
assert a["evaluationScore"]>b["evaluationScore"]
assert a["textFit"]==1.0 and b["textFit"]==0.0
assert "mature>=2y" in a["reasons"] and "recent-release" in a["reasons"] and "broad-contributor-base" in a["reasons"]
print("OK: candidate evaluation tests passed")
