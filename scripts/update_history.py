#!/usr/bin/env python3
"""Maintain bounded weekly repository history and derive multi-window trend signals."""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path

SCHEMA_VERSION=1


def empty_history():
    return {"schemaVersion":SCHEMA_VERSION,"repositories":{}}


def load_history(path):
    if path is None or not path.exists(): return empty_history()
    try:
        data=json.loads(path.read_text())
    except (OSError,json.JSONDecodeError):
        return empty_history()
    if not isinstance(data,dict) or not isinstance(data.get("repositories"),dict):
        return empty_history()
    repositories={}
    for repo,points in data["repositories"].items():
        if not isinstance(repo,str) or not isinstance(points,list): continue
        repositories[repo]=[point for point in points if isinstance(point,dict)]
    return {"schemaVersion":SCHEMA_VERSION,"repositories":repositories}


def update(history,catalog,health,max_points=26,now=None):
    now=(now or datetime.now(timezone.utc)).date().isoformat()
    if not isinstance(history,dict): history=empty_history()
    store=history.get("repositories")
    if not isinstance(store,dict):
        store={}
        history={"schemaVersion":SCHEMA_VERSION,"repositories":store}
    else:
        history["schemaVersion"]=SCHEMA_VERSION
    health_rows=health.get("repositories",[]) if isinstance(health,dict) else []
    hmap={x.get("repo"):x for x in health_rows if isinstance(x,dict) and isinstance(x.get("repo"),str)} if isinstance(health_rows,list) else {}
    catalog_rows=catalog.get("repositories",[]) if isinstance(catalog,dict) else []
    for r in catalog_rows if isinstance(catalog_rows,list) else []:
        if not isinstance(r,dict): continue
        name=r.get("repo")
        if not isinstance(name,str) or not name: continue
        gh=r.get("github",{}); gh=gh if isinstance(gh,dict) else {}
        h=hmap.get(name,{})
        point={"date":now,"health":h.get("score"),"status":h.get("status"),"stars":gh.get("stars"),"forks":gh.get("forks")}
        points=store.get(name,[])
        points=[p for p in points if isinstance(p,dict)] if isinstance(points,list) else []
        if points and points[-1].get("date")==now: points[-1]=point
        else: points.append(point)
        store[name]=points[-max_points:]
    return history

def window_metrics(points,size):
    pts=points[-size:] if size else points
    if len(pts)<2: return None
    first,last=pts[0],pts[-1]
    try:
        days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
    except (ValueError,TypeError,KeyError): days=max(1,7*(len(pts)-1))
    def delta(k):
        a,b=first.get(k),last.get(k)
        return round(b-a,2) if isinstance(a,(int,float)) and isinstance(b,(int,float)) else None
    hd,sd,fd=delta("health"),delta("stars"),delta("forks")
    return {"points":len(pts),"days":days,"healthDelta":hd,"starsDelta":sd,"forksDelta":fd,
            "starsPerWeek":round(sd*7/days,2) if sd is not None else None,
            "forksPerWeek":round(fd*7/days,2) if fd is not None else None}

def trends(history):
    rows=[]
    repositories=history.get("repositories",{}) if isinstance(history,dict) else {}
    for repo,pts in repositories.items() if isinstance(repositories,dict) else []:
        if not isinstance(pts,list): continue
        pts=[p for p in pts if isinstance(p,dict)]
        if len(pts)<2: continue
        w1=window_metrics(pts,2); w4=window_metrics(pts,5); full=window_metrics(pts,None)
        recent=w4 or w1 or full
        hd=recent.get("healthDelta")
        direction="stable"
        if hd is not None and hd<=-10: direction="declining"
        elif hd is not None and hd>=10: direction="improving"
        elif (recent.get("starsPerWeek") or 0)>0: direction="growing"
        rows.append({"repo":repo,"trend":direction,"week":w1,"fourWeeks":w4,"full":full})
    rows.sort(key=lambda x:(x["trend"]!="declining",-abs((x["fourWeeks"] or x["week"] or x["full"]).get("healthDelta") or 0),x["repo"].lower()))
    return {"repositories":rows}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("history",type=Path); ap.add_argument("catalog",type=Path); ap.add_argument("health",type=Path)
    ap.add_argument("--max-points",type=int,default=26); ap.add_argument("--write",action="store_true"); ap.add_argument("--trends",type=Path)
    args=ap.parse_args()
    if args.max_points<2: ap.error("--max-points must be >= 2")
    history=load_history(args.history)
    history=update(history,json.loads(args.catalog.read_text()),json.loads(args.health.read_text()),args.max_points)
    if args.write: args.history.write_text(json.dumps(history,indent=2,ensure_ascii=False)+"\n")
    if args.trends: args.trends.write_text(json.dumps(trends(history),indent=2,ensure_ascii=False)+"\n")
    if not args.write and not args.trends: print(json.dumps(history,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
