#!/usr/bin/env python3
"""Execute discovery watchlist against GitHub Search API and rank novel candidates."""
import argparse, json, math, os, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API="https://api.github.com/search/repositories"
REPO_API="https://api.github.com/repos/{}"

def fetch(query, token=None, per_page=10):
    params=urlencode({"q":query,"sort":"stars","order":"desc","per_page":per_page})
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    req=Request(f"{API}?{params}",headers=headers)
    with urlopen(req,timeout=20) as res: return json.load(res)

def enrich(repo, token=None):
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    req=Request(REPO_API.format(repo),headers=headers)
    with urlopen(req,timeout=20) as res:
        data=json.load(res)
    out={"topics":data.get("topics",[]),"watchers":data.get("subscribers_count",0),
         "size":data.get("size"),"openIssues":data.get("open_issues_count",0),
         "createdAt":data.get("created_at"),"homepage":data.get("homepage"),
         "hasDiscussions":data.get("has_discussions",False)}
    for key,path in (("latestRelease","releases/latest"),("contributors","contributors?per_page=1&anon=true")):
        try:
            with urlopen(Request(f"{REPO_API.format(repo)}/{path}",headers=headers),timeout=20) as extra:
                payload=json.load(extra)
                if key=="latestRelease": out[key]={"tag":payload.get("tag_name"),"publishedAt":payload.get("published_at")}
                else:
                    link=extra.headers.get("Link","")
                    import re
                    m=re.search(r'[?&]page=(\\d+)>; rel="last"',link)
                    out[key]=int(m.group(1)) if m else len(payload)
        except Exception: out[key]=None
    return out

def score(item, priority):
    stars=max(0,item.get("stargazers_count",0)); forks=max(0,item.get("forks_count",0))
    popularity=min(25,5*math.log10(stars+1)); ecosystem=min(15,4*math.log10(forks+1))
    metadata=5 if item.get("license") else 2
    return round(min(100, 0.45*priority + popularity + ecosystem + metadata),1)

def discover(watchlist, known, token=None, per_query=10):
    candidates={}
    errors=[]
    for target in watchlist.get("watchlist",[]):
        try:
            data=fetch(target["query"],token,per_query)
        except Exception as e:
            errors.append({"target":target["target"],"error":str(e)}); continue
        for item in data.get("items",[]):
            name=item.get("full_name")
            if not name or name in known or item.get("archived") or item.get("disabled") or item.get("fork"): continue
            row={"repo":name,"url":item.get("html_url"),"description":item.get("description"),
                 "stars":item.get("stargazers_count",0),"forks":item.get("forks_count",0),
                 "language":item.get("language"),"license":(item.get("license") or {}).get("spdx_id"),
                 "pushedAt":item.get("pushed_at"),"discoveryScore":score(item,target["priority"]),
                 "matchedTargets":[{"kind":target["kind"],"target":target["target"],"priority":target["priority"]}]}
            if name in candidates:
                candidates[name]["matchedTargets"].append(row["matchedTargets"][0])
                candidates[name]["discoveryScore"]=max(candidates[name]["discoveryScore"],row["discoveryScore"])
            else: candidates[name]=row
        time.sleep(0.2)
    rows=sorted(candidates.values(),key=lambda x:(-x["discoveryScore"],-x["stars"],x["repo"].lower()))
    for row in rows[:min(50,len(rows))]:
        try: row.update(enrich(row["repo"],token))
        except Exception as e: row["enrichmentError"]=str(e)
        time.sleep(0.1)
    return {"candidates":len(rows),"repositories":rows,"errors":errors}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("watchlist",type=Path); ap.add_argument("catalog",type=Path)
    ap.add_argument("--per-query",type=int,default=10); ap.add_argument("--top",type=int,default=50)
    args=ap.parse_args()
    if not 1<=args.per_query<=100: ap.error("--per-query must be in [1,100]")
    known={r["repo"] for r in json.loads(args.catalog.read_text()).get("repositories",[])}
    result=discover(json.loads(args.watchlist.read_text()),known,os.environ.get("GITHUB_TOKEN"),args.per_query)
    result["repositories"]=result["repositories"][:args.top]; result["candidates"]=len(result["repositories"])
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
