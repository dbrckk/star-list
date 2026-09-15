#!/usr/bin/env python3
"""Analyze catalog coverage and surface functional blind spots."""
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
from health_score import health_score

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"catalog.json"

def analyze(repos, min_domain=3, min_capability=2):
    domains=Counter(r.get("domain","other") for r in repos)
    caps=Counter(c for r in repos for c in r.get("capabilities",[]))
    healthy_domains=Counter()
    healthy_caps=Counter()
    by_domain=defaultdict(list)
    for r in repos:
        h=health_score(r)
        usable=h["status"] not in {"inactive","weak"} if h["score"] is not None else True
        if usable:
            healthy_domains[r.get("domain","other")]+=1
            for c in r.get("capabilities",[]): healthy_caps[c]+=1
        by_domain[r.get("domain","other")].append(r)

    domain_gaps=[]
    for domain,count in sorted(domains.items()):
        healthy=healthy_domains[domain]
        if count < min_domain or healthy < min_domain:
            domain_gaps.append({"domain":domain,"total":count,"healthy":healthy,
                                "deficit":max(0,min_domain-healthy),"severity":"critical" if healthy==0 else "warning"})
    capability_gaps=[]
    for cap,count in sorted(caps.items()):
        healthy=healthy_caps[cap]
        if count < min_capability or healthy < min_capability:
            capability_gaps.append({"capability":cap,"total":count,"healthy":healthy,
                                    "deficit":max(0,min_capability-healthy),"severity":"critical" if healthy==0 else "warning"})
    concentration=[]
    for domain,items in sorted(by_domain.items()):
        total=len(items)
        top_tier=sum(r.get("tier") in {"core","recommended"} for r in items)
        if total and top_tier==0:
            concentration.append({"domain":domain,"repositories":total,"issue":"no-core-or-recommended"})
    return {"policy":{"minHealthyPerDomain":min_domain,"minHealthyPerCapability":min_capability},
            "domainGaps":domain_gaps,"capabilityGaps":capability_gaps,"qualityGaps":concentration,
            "summary":{"domains":len(domains),"capabilities":len(caps),"domainGaps":len(domain_gaps),
                       "capabilityGaps":len(capability_gaps),"qualityGaps":len(concentration)}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--min-domain",type=int,default=3)
    ap.add_argument("--min-capability",type=int,default=2)
    args=ap.parse_args()
    if args.min_domain<1 or args.min_capability<1: ap.error("minimum coverage must be >= 1")
    repos=json.loads(CATALOG.read_text()).get("repositories",[])
    print(json.dumps(analyze(repos,args.min_domain,args.min_capability),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
