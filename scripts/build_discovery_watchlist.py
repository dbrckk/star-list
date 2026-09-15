#!/usr/bin/env python3
"""Turn coverage gaps into a deterministic GitHub discovery watchlist."""
import argparse, json
from pathlib import Path

def build(report, max_items=30):
    items=[]
    for x in report.get("domainGaps",[]):
        priority=100 if x.get("severity")=="critical" else 70
        priority += min(20, 5*int(x.get("deficit",0)))
        items.append({"kind":"domain","target":x["domain"],"priority":priority,
                      "query":f"{x['domain'].replace('_',' ')} stars:>100 archived:false",
                      "reason":f"healthy {x.get('healthy',0)}/{report.get('policy',{}).get('minHealthyPerDomain',3)}"})
    for x in report.get("capabilityGaps",[]):
        priority=95 if x.get("severity")=="critical" else 65
        priority += min(20, 5*int(x.get("deficit",0)))
        items.append({"kind":"capability","target":x["capability"],"priority":priority,
                      "query":f"{x['capability'].replace('_',' ')} stars:>100 archived:false",
                      "reason":f"healthy {x.get('healthy',0)}/{report.get('policy',{}).get('minHealthyPerCapability',2)}"})
    for x in report.get("qualityGaps",[]):
        items.append({"kind":"quality","target":x["domain"],"priority":60,
                      "query":f"{x['domain'].replace('_',' ')} stars:>500 archived:false",
                      "reason":x.get("issue","quality-gap")})
    dedup={}
    for x in items:
        key=(x["kind"],x["target"])
        if key not in dedup or x["priority"]>dedup[key]["priority"]: dedup[key]=x
    rows=sorted(dedup.values(),key=lambda x:(-x["priority"],x["kind"],x["target"]))[:max_items]
    return {"items":len(rows),"watchlist":rows}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("coverage",type=Path)
    ap.add_argument("--max-items",type=int,default=30)
    args=ap.parse_args()
    if args.max_items<1: ap.error("--max-items must be >= 1")
    print(json.dumps(build(json.loads(args.coverage.read_text()),args.max_items),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
