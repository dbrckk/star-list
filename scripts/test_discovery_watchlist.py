#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"build_discovery_watchlist.py"
spec=importlib.util.spec_from_file_location("watchlist",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
report={"policy":{"minHealthyPerDomain":3,"minHealthyPerCapability":2},
"domainGaps":[{"domain":"mobile","healthy":0,"deficit":3,"severity":"critical"}],
"capabilityGaps":[{"capability":"vector","healthy":1,"deficit":1,"severity":"warning"}],
"qualityGaps":[{"domain":"graphics","issue":"no-core-or-recommended"}]}
r=mod.build(report)
assert r["items"]==3
assert r["watchlist"][0]["target"]=="mobile"
assert "archived:false" in r["watchlist"][0]["query"]
assert all(r["watchlist"][i]["priority"]>=r["watchlist"][i+1]["priority"] for i in range(len(r["watchlist"])-1))
print("OK: discovery watchlist tests passed")
