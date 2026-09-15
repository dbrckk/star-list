#!/usr/bin/env python3
"""Evaluate discovered repositories into accept/review/reject buckets."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ACCEPT_THRESHOLD=80.0
REVIEW_THRESHOLD=55.0

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

def _bounded(value):
    return round(max(0.0,min(100.0,float(value))),1)

def decision_for_score(score):
    score=float(score)
    if score>=ACCEPT_THRESHOLD: return "accept"
    if score>=REVIEW_THRESHOLD: return "review"
    return "reject"

def evaluation_confidence(repo):
    release=repo.get("latestRelease")
    signals=(
        bool(repo.get("pushedAt")),
        bool(repo.get("createdAt")),
        bool(repo.get("license")),
        isinstance(release,dict) and bool(release.get("publishedAt")),
        isinstance(repo.get("contributors"),int),
        isinstance(repo.get("watchers"),int),
        isinstance(repo.get("forks"),int),
        isinstance(repo.get("openIssues"),int),
        isinstance(repo.get("hasDiscussions"),bool),
        isinstance(repo.get("topics"),list) and bool(repo.get("topics")),
    )
    coverage=sum(signals)/len(signals)
    if coverage>=0.8: return "high"
    if coverage>=0.5: return "medium"
    return "low"

def score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues):
    fit_score=fit*65+min(20,topic_hits*10)+min(15,max(0,len(matches)-1)*7.5)

    if days is None: activity=0
    elif days<=90: activity=70
    elif days<=365: activity=55
    elif days<=730: activity=35
    else: activity=10
    if release_days is not None and release_days<=180: activity+=30
    elif release_days is not None and release_days<=365: activity+=15

    if stars>=5000: adoption=55
    elif stars>=1000: adoption=45
    elif stars>=500: adoption=35
    elif stars>=100: adoption=25
    elif stars>=20: adoption=10
    else: adoption=0
    if watchers>=100: adoption+=20
    elif watchers>=20: adoption+=10
    elif watchers>=5: adoption+=5
    fork_ratio=forks/max(1,stars) if stars else 0.0
    if stars and fork_ratio>=0.05: adoption+=25
    elif stars and fork_ratio>=0.01: adoption+=15
    elif forks>0: adoption+=5

    maturity=25 if repo.get("license") else 0
    if created_days is not None and created_days>=730: maturity+=25
    elif created_days is not None and created_days>=365: maturity+=15
    elif created_days is not None and created_days>=90: maturity+=10
    if isinstance(contributors,int) and contributors>=20: maturity+=30
    elif isinstance(contributors,int) and contributors>=5: maturity+=20
    elif isinstance(contributors,int) and contributors>=2: maturity+=10
    if repo.get("hasDiscussions"): maturity+=20

    maintenance=50
    if isinstance(contributors,int) and contributors>=20: maintenance+=15
    elif isinstance(contributors,int) and contributors<=1 and stars>=500: maintenance-=20
    if stars>=500:
        issue_ratio=open_issues/max(1,stars)
        if issue_ratio<0.02: maintenance+=20
        elif issue_ratio>0.20: maintenance-=20
        if fork_ratio>=0.05: maintenance+=15
        elif fork_ratio<0.005: maintenance-=15

    return {
        "fit":_bounded(fit_score),
        "activity":_bounded(activity),
        "adoption":_bounded(adoption),
        "maturity":_bounded(maturity),
        "maintenance":_bounded(maintenance),
    }

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
    stars=max(0,int(repo.get("stars",0)))
    contributors=repo.get("contributors")
    if isinstance(contributors,int) and contributors>=20: score+=4; reasons.append("broad-contributor-base")
    elif isinstance(contributors,int) and contributors<=1 and stars>=500: score-=4; reasons.append("single-contributor-risk")
    topics={str(x).lower() for x in repo.get("topics",[])}
    target_words={w for m in repo.get("matchedTargets",[]) for w in str(m.get("target","")).lower().replace("_","-").split("-") if w}
    topic_hits=len(topics & target_words)
    if topic_hits: score+=min(6,2*topic_hits); reasons.append("topic-fit")
    matches=repo.get("matchedTargets",[])
    if len(matches)>=2: score+=min(10,3*(len(matches)-1)); reasons.append("multi-gap-fit")
    if stars<100: score-=10; reasons.append("low-adoption")
    watchers=max(0,int(repo.get("watchers",0) or 0))
    if watchers>=100: score+=2; reasons.append("strong-watchers")
    forks=max(0,int(repo.get("forks",0)))
    open_issues=max(0,int(repo.get("openIssues",0) or 0))
    if stars>=500:
        issue_ratio=open_issues/max(1,stars)
        if issue_ratio>0.20: score-=5; reasons.append("high-open-issue-load")
        elif issue_ratio<0.02: score+=2; reasons.append("controlled-issue-load")
    if repo.get("hasDiscussions"): score+=1; reasons.append("community-discussions")
    if stars>=500 and forks/max(1,stars)>=0.05: score+=4; reasons.append("healthy-fork-ratio")
    elif stars>=500 and forks/max(1,stars)<0.005: score-=3; reasons.append("low-fork-ratio")
    score=round(max(0,min(100,score)),1)
    confidence=evaluation_confidence(repo)
    decision=decision_for_score(score)
    if confidence=="low" and decision=="accept":
        decision="review"
        reasons.append("low-confidence-cap")
    breakdown=score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues)
    return {"evaluationScore":score,"decision":decision,"ageDays":days,"repositoryAgeDays":created_days,"releaseAgeDays":release_days,"textFit":round(fit,3),"openIssueRatio":round(open_issues/max(1,stars),4) if stars else None,"scoreBreakdown":breakdown,"evaluationConfidence":confidence,"reasons":reasons}

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
