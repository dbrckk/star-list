#!/usr/bin/env python3
"""Suppress unchanged reviewed/rejected candidates while preserving meaningful changes."""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path

def fingerprint(r):
    return {"decision":r.get("decision"),"score":r.get("evaluationScore"),"stars":r.get("stars"),
            "pushedAt":r.get("pushedAt"),"targets":sorted((x.get("kind"),x.get("target")) for x in r.get("matchedTargets",[]))}

def apply(data,memory,score_delta=5.0):
    known=memory.setdefault("candidates",{})
    visible=[]; suppressed=0
    now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    for r in data.get("repositories",[]):
        name=r["repo"]; fp=fingerprint(r); old=known.get(name)
        changed=True
        if old:
            oldfp=old.get("fingerprint",{})
            score_changed=abs(float(fp.get("score") or 0)-float(oldfp.get("score") or 0))>=score_delta
            changed=(fp.get("decision")!=oldfp.get("decision") or fp.get("pushedAt")!=oldfp.get("pushedAt")
                     or fp.get("targets")!=oldfp.get("targets") or score_changed)
        if changed or r.get("decision")=="accept": visible.append(r)
        else: suppressed+=1
        known[name]={"fingerprint":fp,"lastSeenAt":now}
    return {**data,"repositories":visible,"candidates":len(visible),"suppressedUnchanged":suppressed},memory

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("memory",type=Path)
    ap.add_argument("--output",type=Path); ap.add_argument("--write-memory",action="store_true"); ap.add_argument("--score-delta",type=float,default=5.0)
    args=ap.parse_args()
    data=json.loads(args.evaluated.read_text()); memory=json.loads(args.memory.read_text()) if args.memory.exists() else {"schemaVersion":1,"candidates":{}}
    filtered,memory=apply(data,memory,args.score_delta)
    text=json.dumps(filtered,indent=2,ensure_ascii=False)+"\n"
    if args.output: args.output.write_text(text)
    else: print(text,end="")
    if args.write_memory: args.memory.write_text(json.dumps(memory,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__": main()
