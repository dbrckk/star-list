#!/usr/bin/env python3
"""Compare repository health snapshots and detect meaningful deterioration."""
import argparse, json
from pathlib import Path

def index(snapshot):
    rows = snapshot.get("repositories", snapshot if isinstance(snapshot, list) else [])
    return {r["repo"]: r for r in rows if isinstance(r, dict) and r.get("repo")}

def detect(previous, current, drop=10.0):
    old, new = index(previous), index(current)
    findings = []
    for repo, now in new.items():
        before = old.get(repo)
        if not before: continue
        a, b = before.get("score"), now.get("score")
        if not isinstance(a, (int,float)) or not isinstance(b, (int,float)): continue
        delta = round(b-a, 1)
        status_changed = before.get("status") != now.get("status")
        if delta <= -abs(drop) or (status_changed and now.get("status") in {"weak","inactive"}):
            findings.append({"repo":repo,"previousScore":a,"currentScore":b,"delta":delta,
                             "previousStatus":before.get("status"),"currentStatus":now.get("status")})
    findings.sort(key=lambda x:(x["delta"], x["repo"].lower()))
    return findings

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("previous", type=Path)
    ap.add_argument("current", type=Path)
    ap.add_argument("--drop", type=float, default=10.0)
    args=ap.parse_args()
    if args.drop <= 0: ap.error("--drop must be > 0")
    findings=detect(json.loads(args.previous.read_text()), json.loads(args.current.read_text()), args.drop)
    print(json.dumps({"dropThreshold":args.drop,"findings":len(findings),"repositories":findings},indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
