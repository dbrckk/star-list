#!/usr/bin/env python3
import importlib.util
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"update_history.py"
spec=importlib.util.spec_from_file_location("h",SCRIPT); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
cat={"repositories":[{"repo":"a/x","github":{"stars":100,"forks":10}}]}; health={"repositories":[{"repo":"a/x","score":80,"status":"healthy"}]}
hist={"schemaVersion":1,"repositories":{}}
h.update(hist,cat,health,3,datetime(2026,9,1,tzinfo=timezone.utc))
cat["repositories"][0]["github"]["stars"]=150; health["repositories"][0]["score"]=65
h.update(hist,cat,health,3,datetime(2026,9,8,tzinfo=timezone.utc))
t=h.trends(hist)["repositories"][0]; assert t["healthDelta"]==-15 and t["starsDelta"]==50 and t["trend"]=="declining"
print("OK: repository history tests passed")
