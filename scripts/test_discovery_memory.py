#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"filter_discovery_memory.py"
spec=importlib.util.spec_from_file_location("m",SCRIPT); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
row={"repo":"a/x","decision":"review","evaluationScore":70,"stars":1000,"pushedAt":"2026-09-01","matchedTargets":[]}
data={"repositories":[row],"counts":{"accept":0,"review":1,"reject":0}}
first,mem=m.apply(data,{"schemaVersion":1,"candidates":{}}); assert first["candidates"]==1
second,mem=m.apply(data,mem); assert second["candidates"]==0 and second["suppressedUnchanged"]==1
changed={**row,"evaluationScore":76}; third,mem=m.apply({"repositories":[changed]},mem); assert third["candidates"]==1
print("OK: discovery memory tests passed")
