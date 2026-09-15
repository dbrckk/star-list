#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"render_discovery_issue.py"
spec=importlib.util.spec_from_file_location("renderer",SCRIPT); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
data={"candidates":2,"counts":{"accept":1,"review":1,"reject":0},"repositories":[{"repo":"a/x","url":"https://github.com/a/x","decision":"accept","evaluationScore":90,"evaluationConfidence":"high","scoreBreakdown":{"fit":92.5,"activity":100.0,"adoption":75.0,"maturity":80.0,"maintenance":85.0},"stars":1000,"ageDays":5,"matchedTargets":[{"kind":"domain","target":"mobile"}],"reasons":["active<=90d"]}]}
body=mod.render(data)
assert "Discovery candidates" in body and "a/x" in body and "mobile" in body
assert "Confidence" in body and "high" in body
assert "fit=92.5" in body and "activity=100.0" in body and "maintenance=85.0" in body
assert "<!-- star-list-discovery-candidates -->" in body
print("OK: discovery issue renderer tests passed")
