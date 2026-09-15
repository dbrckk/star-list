#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"analyze_coverage.py"
spec=importlib.util.spec_from_file_location("coverage",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
repos=[
 {"repo":"a/one","domain":"backend","tier":"recommended","capabilities":["api"],"score":9.2},
 {"repo":"a/two","domain":"backend","tier":"specialized","capabilities":["api"],"score":8.5},
 {"repo":"b/one","domain":"mobile","tier":"specialized","capabilities":["mobile"],"score":8.5},
]
r=mod.analyze(repos,min_domain=2,min_capability=2)
assert any(x["domain"]=="mobile" for x in r["domainGaps"])
assert not any(x["domain"]=="backend" for x in r["domainGaps"])
assert any(x["capability"]=="mobile" for x in r["capabilityGaps"])
assert any(x["domain"]=="mobile" for x in r["qualityGaps"])
print("OK: coverage analysis tests passed")
