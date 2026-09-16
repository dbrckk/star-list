#!/usr/bin/env python3
"""Suppress unchanged reviewed/rejected candidates while preserving meaningful changes."""
import argparse,json,math
from datetime import datetime,timezone
from pathlib import Path

SCHEMA_VERSION=1


def empty_memory():
    return {"schemaVersion":SCHEMA_VERSION,"candidates":{}}


def load_memory(path):
    if path is None or not path.exists(): return empty_memory()
    try:
        data=json.loads(path.read_text())
    except (OSError,json.JSONDecodeError):
        return empty_memory()
    if not isinstance(data,dict) or not isinstance(data.get("candidates"),dict):
        return empty_memory()
    candidates={str(name):entry for name,entry in data["candidates"].items() if isinstance(entry,dict)}
    return {"schemaVersion":SCHEMA_VERSION,"candidates":candidates}


def _number(value,default=0.0):
    if isinstance(value,bool): return default
    try: result=float(value)
    except (TypeError,ValueError): return default
    return result if math.isfinite(result) else default


def _targets(value):
    if not isinstance(value,list): return []
    return sorted((x.get("kind"),x.get("target")) for x in value if isinstance(x,dict))


def fingerprint(r):
    return {"decision":r.get("decision"),"score":r.get("evaluationScore"),"stars":r.get("stars"),
            "pushedAt":r.get("pushedAt"),"targets":_targets(r.get("matchedTargets",[]))}

def apply(data,memory,score_delta=5.0):
    if not isinstance(memory,dict): memory=empty_memory()
    known=memory.get("candidates")
    if not isinstance(known,dict):
        known={}
        memory={"schemaVersion":SCHEMA_VERSION,"candidates":known}
    else:
        memory["schemaVersion"]=SCHEMA_VERSION
    visible=[]; suppressed=0
    now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    repositories=data.get("repositories",[]) if isinstance(data,dict) else []
    for r in repositories if isinstance(repositories,list) else []:
        if not isinstance(r,dict): continue
        name=r.get("repo")
        if not isinstance(name,str) or not name: continue
        fp=fingerprint(r); old=known.get(name)
        changed=True
        if isinstance(old,dict):
            oldfp=old.get("fingerprint",{})
            if not isinstance(oldfp,dict): oldfp={}
            score_changed=abs(_number(fp.get("score"))-_number(oldfp.get("score")))>=score_delta
            changed=(fp.get("decision")!=oldfp.get("decision") or fp.get("pushedAt")!=oldfp.get("pushedAt")
                     or fp.get("targets")!=oldfp.get("targets") or score_changed)
        if changed or r.get("decision")=="accept": visible.append(r)
        else: suppressed+=1
        known[name]={"fingerprint":fp,"lastSeenAt":now}
    base=data if isinstance(data,dict) else {}
    return {**base,"repositories":visible,"candidates":len(visible),"suppressedUnchanged":suppressed},memory

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("memory",type=Path)
    ap.add_argument("--output",type=Path); ap.add_argument("--write-memory",action="store_true"); ap.add_argument("--score-delta",type=float,default=5.0)
    args=ap.parse_args()
    data=json.loads(args.evaluated.read_text()); memory=load_memory(args.memory)
    filtered,memory=apply(data,memory,args.score_delta)
    text=json.dumps(filtered,indent=2,ensure_ascii=False)+"\n"
    if args.output: args.output.write_text(text)
    else: print(text,end="")
    if args.write_memory: args.memory.write_text(json.dumps(memory,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__": main()
