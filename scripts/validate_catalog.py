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
    s=r.get("score",-1)
    tier=r.get("tier")
    if tier not in {"core","recommended","specialized","audit"}: errors.append(f"{r.get('repo')}: invalid tier {tier}")
    if tier=="core" and s<9.5: errors.append(f"{r.get('repo')}: core requires score >= 9.5")
    if tier=="recommended" and s<9.0: errors.append(f"{r.get('repo')}: recommended requires score >= 9.0")
    if tier=="specialized" and s<8.0: errors.append(f"{r.get('repo')}: specialized requires score >= 8.0")
    if r.get("domain")=="trading":
        roles=set(r.get("roles",[]))
        bad=roles-valid_roles
        if not roles: errors.append(f"{r.get('repo')}: trading repo missing roles")
        if bad: errors.append(f"{r.get('repo')}: unknown roles {sorted(bad)}")
if errors:
    print("\n".join(errors)); sys.exit(1)
print(f"OK: {len(seen)} repositories")
