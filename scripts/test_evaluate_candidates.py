#!/usr/bin/env python3
import importlib.util
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"evaluate_candidates.py"
spec=importlib.util.spec_from_file_location("evaluate",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
strong={"repo":"a/x","discoveryScore":75,"stars":5000,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","matchedTargets":[{"target":"ai"},{"target":"agents"}]}
weak={"repo":"b/y","discoveryScore":50,"stars":20,"license":None,"pushedAt":"2020-01-01T00:00:00Z","matchedTargets":[]}
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW)
assert a["decision"]=="accept" and a["evaluationScore"]>=80
assert b["decision"]=="reject" and b["evaluationScore"]<55
assert a["evaluationScore"]>b["evaluationScore"]
print("OK: candidate evaluation tests passed")
