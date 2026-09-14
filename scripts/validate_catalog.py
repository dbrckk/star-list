#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
p=Path(__file__).resolve().parents[1]
data=json.loads((p/"catalog.json").read_text())
errors=[]
valid_domains={"ai_agents","ai_memory","ai_media","software_engineering","web_frontend","backend","mobile","graphics","game_dev","trading","cybersecurity","data_ml","devops","productivity","other"}
valid_roles={"data","alpha","regime","backtest","risk","execution","portfolio","xauusd","macro","ml","microstructure","performance","volatility","optimization","forecasting","feature-engineering","derivatives","diagnostic","feature-selection","filtering"}
seen=set()
for i,r in enumerate(data.get("repositories",[])):
    if not re.match(r"^[^/]+/[^/]+$",r.get("repo","")): errors.append(f"{i}: invalid repo")
    if r.get("repo") in seen: errors.append(f"{i}: duplicate {r['repo']}")
    seen.add(r.get("repo"))
    s=r.get("score",-1); expected="core" if s>=9.5 else "recommended" if s>=9 else "specialized" if s>=8 else "audit"
    if r.get("tier")!=expected: errors.append(f"{r.get('repo')}: tier should be {expected}")
    if r.get("domain")=="trading":
        roles=set(r.get("roles",[]))
        bad=roles-valid_roles
        if not roles: errors.append(f"{r.get('repo')}: trading repo missing roles")
        if bad: errors.append(f"{r.get('repo')}: unknown roles {sorted(bad)}")
if errors:
    print("\n".join(errors)); sys.exit(1)
print(f"OK: {len(seen)} repositories")
