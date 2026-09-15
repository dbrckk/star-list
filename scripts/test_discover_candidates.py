#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"discover_candidates.py"
spec=importlib.util.spec_from_file_location("discover",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
item={"stargazers_count":10000,"forks_count":1000,"license":{"spdx_id":"MIT"}}
assert 0 < mod.score(item,100) <= 100
assert mod.score(item,100) > mod.score({"stargazers_count":10,"forks_count":1,"license":None},50)
print("OK: discovery candidate scoring tests passed")
