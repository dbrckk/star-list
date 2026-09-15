#!/usr/bin/env python3
"""Maintain bounded weekly repository history and derive trend signals."""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path

def update(history,catalog,health,max_points=26,now=None):
    now=(now or datetime.now(timezone.utc)).date().isoformat()
    hmap={x["repo"]:x for x in health.get("repositories",[])}
    store=history.setdefault("repositories",{})
    for r in catalog.get("repositories",[]):
        name=r["repo"]; gh=r.get("github",{}); h=hmap.get(name,{})
        point={"date":now,"health":h.get("score"),"status":h.get("status"),
               "stars":gh.get("stars"),"forks":gh.get("forks")}
        points=store.setdefault(name,[])
        if points and points[-1].get("date")==now: points[-1]=point
        else: points.append(point)
        store[name]=points[-max_points:]
    return history

def trends(history):
    rows=[]
    for repo,pts in history.get("repositories",{}).items():
        if len(pts)<2: continue
        first,last=pts[0],pts[-1]
        def delta(k):
            a,b=first.get(k),last.get(k)
            return round(b-a,1) if isinstance(a,(int,float)) and isinstance(b,(int,float)) else None
        hd,sd,fd=delta("health"),delta("stars"),delta("forks")
        direction="stable"
        if hd is not None and hd<=-10: direction="declining"
        elif hd is not None and hd>=10: direction="improving"
        elif sd is not None and sd>0: direction="growing"
        rows.append({"repo":repo,"points":len(pts),"healthDelta":hd,"starsDelta":sd,"forksDelta":fd,"trend":direction})
    rows.sort(key=lambda x:(x["trend"]!="declining",-(abs(x["healthDelta"] or 0)),x["repo"].lower()))
    return {"repositories":rows}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("history",type=Path); ap.add_argument("catalog",type=Path); ap.add_argument("health",type=Path)
    ap.add_argument("--max-points",type=int,default=26); ap.add_argument("--write",action="store_true"); ap.add_argument("--trends",type=Path)
    args=ap.parse_args()
    if args.max_points<2: ap.error("--max-points must be >= 2")
    history=json.loads(args.history.read_text()) if args.history.exists() else {"schemaVersion":1,"repositories":{}}
    history=update(history,json.loads(args.catalog.read_text()),json.loads(args.health.read_text()),args.max_points)
    if args.write: args.history.write_text(json.dumps(history,indent=2,ensure_ascii=False)+"\n")
    if args.trends: args.trends.write_text(json.dumps(trends(history),indent=2,ensure_ascii=False)+"\n")
    if not args.write and not args.trends: print(json.dumps(history,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
