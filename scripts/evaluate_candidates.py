#!/usr/bin/env python3
"""Evaluate discovered repositories into accept/review/reject buckets."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def age_days(value, now=None):
    if not value: return None
    try: dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    except (ValueError,TypeError): return None
    return max(0,((now or datetime.now(timezone.utc))-dt).days)

def text_fit(repo):
    text=((repo.get("repo") or "")+" "+(repo.get("description") or "")+" "+(repo.get("language") or "")).lower()
    targets=repo.get("matchedTargets",[])
    if not targets: return 0.0
    hits=0
    for m in targets:
        words=str(m.get("target","")).lower().replace("_"," ").replace("-"," ").split()
        if words and any(w in text for w in words): hits+=1
    return hits/max(1,len(targets))

def evaluate(repo, now=None):
    score=float(repo.get("discoveryScore",0))
    reasons=[]
    days=age_days(repo.get("pushedAt"),now)
    if days is None: score-=8; reasons.append("missing-activity-date")
    elif days<=90: score+=10; reasons.append("active<=90d")
    elif days<=365: score+=5; reasons.append("active<=1y")
    elif days>730: score-=20; reasons.append("stale>2y")
    elif days>365: score-=8; reasons.append("stale>1y")
    if repo.get("license"): score+=5; reasons.append("licensed")
    else: score-=10; reasons.append("license-missing")
    fit=text_fit(repo)
    if fit>=0.75: score+=8; reasons.append("strong-text-fit")
    elif fit==0: score-=6; reasons.append("weak-text-fit")
    created_days=age_days(repo.get("createdAt"),now)
    if created_days is not None and created_days>=730: score+=4; reasons.append("mature>=2y")
    elif created_days is not None and created_days<90: score-=3; reasons.append("very-new<90d")
    release=repo.get("latestRelease") or {}
    release_days=age_days(release.get("publishedAt"),now) if isinstance(release,dict) else None
    if release_days is not None and release_days<=180: score+=5; reasons.append("recent-release")
    contributors=repo.get("contributors")
    if isinstance(contributors,int) and contributors>=20: score+=4; reasons.append("broad-contributor-base")
    elif isinstance(contributors,int) and contributors<=1 and stars>=500: score-=4; reasons.append("single-contributor-risk")
    topics={str(x).lower() for x in repo.get("topics",[])}
    target_words={w for m in repo.get("matchedTargets",[]) for w in str(m.get("target","")).lower().replace("_","-").split("-") if w}
    topic_hits=len(topics & target_words)
    if topic_hits: score+=min(6,2*topic_hits); reasons.append("topic-fit")
    matches=repo.get("matchedTargets",[])
    if len(matches)>=2: score+=min(10,3*(len(matches)-1)); reasons.append("multi-gap-fit")
    stars=max(0,int(repo.get("stars",0)))
    if stars<100: score-=10; reasons.append("low-adoption")
    watchers=max(0,int(repo.get("watchers",0) or 0))
    if watchers>=100: score+=2; reasons.append("strong-watchers")
    forks=max(0,int(repo.get("forks",0)))
    if stars>=500 and forks/max(1,stars)>=0.05: score+=4; reasons.append("healthy-fork-ratio")
    elif stars>=500 and forks/max(1,stars)<0.005: score-=3; reasons.append("low-fork-ratio")
    score=round(max(0,min(100,score)),1)
    decision="accept" if score>=80 else "review" if score>=55 else "reject"
    return {"evaluationScore":score,"decision":decision,"ageDays":days,"repositoryAgeDays":created_days,"releaseAgeDays":release_days,"textFit":round(fit,3),"reasons":reasons}

def evaluate_all(data):
    rows=[]
    for r in data.get("repositories",[]):
        rows.append({**r,**evaluate(r)})
    rows.sort(key=lambda x:({"accept":0,"review":1,"reject":2}[x["decision"]],-x["evaluationScore"],-x.get("stars",0),x["repo"].lower()))
    counts={k:sum(x["decision"]==k for x in rows) for k in ("accept","review","reject")}
    return {"candidates":len(rows),"counts":counts,"repositories":rows,"errors":data.get("errors",[])}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidates",type=Path)
    args=ap.parse_args()
    print(json.dumps(evaluate_all(json.loads(args.candidates.read_text())),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
