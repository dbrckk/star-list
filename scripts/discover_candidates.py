#!/usr/bin/env python3
"""Execute discovery watchlist against GitHub Search API and rank novel candidates."""
import argparse, json, math, os, time, random
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API="https://api.github.com/search/repositories"
REPO_API="https://api.github.com/repos/{}"
CACHE_SCHEMA_VERSION=1
DEFAULT_SEARCH_CACHE_TTL_HOURS=24
DEFAULT_METADATA_CACHE_TTL_HOURS=336

def empty_cache():
    return {"schemaVersion": CACHE_SCHEMA_VERSION, "entries": {}}

def load_cache(path):
    if path is None or not path.exists(): return empty_cache()
    try:
        data=json.loads(path.read_text())
    except (OSError,json.JSONDecodeError):
        return empty_cache()
    if not isinstance(data,dict) or not isinstance(data.get("entries"),dict):
        return empty_cache()
    data["schemaVersion"]=CACHE_SCHEMA_VERSION
    return data

def save_cache(path, cache):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(cache,indent=2,ensure_ascii=False)+"\n")
    tmp.replace(path)

def cache_get(cache, url, ttl_seconds, now=None):
    now=time.time() if now is None else now
    entry=cache.get("entries",{}).get(url)
    if not isinstance(entry,dict): return None
    fetched=entry.get("fetchedAt")
    if not isinstance(fetched,(int,float)) or now-fetched>ttl_seconds: return None
    return entry.get("data"), entry.get("headers",{})

def cache_put(cache, url, data, headers, now=None):
    now=time.time() if now is None else now
    cache.setdefault("schemaVersion",CACHE_SCHEMA_VERSION)
    cache.setdefault("entries",{})[url]={"fetchedAt":now,"data":data,"headers":dict(headers or {})}

def api_json(url, headers, attempts=4, cache=None, ttl_seconds=0, now=None):
    if cache is not None and ttl_seconds>0:
        hit=cache_get(cache,url,ttl_seconds,now)
        if hit is not None: return hit
    last=None
    for attempt in range(attempts):
        try:
            with urlopen(Request(url,headers=headers),timeout=20) as res:
                data=json.load(res)
                response_headers=dict(res.headers.items())
                if cache is not None and ttl_seconds>0:
                    cache_put(cache,url,data,response_headers,now)
                return data,response_headers
        except HTTPError as e:
            last=e
            if e.code not in (403,429,500,502,503,504) or attempt==attempts-1: raise
            retry=e.headers.get("Retry-After")
            reset=e.headers.get("X-RateLimit-Reset")
            if retry:
                wait=min(60,float(retry))
            elif reset:
                wait=max(1,min(60,float(reset)-time.time()))
            else:
                wait=min(30,2**attempt)
            time.sleep(wait + random.random())
        except (TimeoutError,OSError) as e:
            last=e
            if attempt==attempts-1: raise
            time.sleep(min(30,2**attempt)+random.random())
    raise last

def fetch(query, token=None, per_page=10, cache=None, ttl_seconds=0):
    params=urlencode({"q":query,"sort":"stars","order":"desc","per_page":per_page})
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    data,_=api_json(f"{API}?{params}",headers,cache=cache,ttl_seconds=ttl_seconds)
    return data

def enrich(repo, token=None, cache=None, ttl_seconds=0):
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    data,_=api_json(REPO_API.format(repo),headers,cache=cache,ttl_seconds=ttl_seconds)
    out={"topics":data.get("topics",[]),"watchers":data.get("subscribers_count",0),
         "size":data.get("size"),"openIssues":data.get("open_issues_count",0),
         "createdAt":data.get("created_at"),"homepage":data.get("homepage"),
         "hasDiscussions":data.get("has_discussions",False)}
    for key,path in (("latestRelease","releases/latest"),("contributors","contributors?per_page=1&anon=true")):
        try:
            payload,response_headers=api_json(f"{REPO_API.format(repo)}/{path}",headers,cache=cache,ttl_seconds=ttl_seconds)
            if key=="latestRelease": out[key]={"tag":payload.get("tag_name"),"publishedAt":payload.get("published_at")}
            else:
                link=response_headers.get("Link","")
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

def discover(watchlist, known, token=None, per_query=10, cache=None, search_ttl_seconds=0, metadata_ttl_seconds=0):
    candidates={}
    errors=[]
    for target in watchlist.get("watchlist",[]):
        try:
            data=fetch(target["query"],token,per_query,cache,search_ttl_seconds)
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
        try: row.update(enrich(row["repo"],token,cache,metadata_ttl_seconds))
        except Exception as e: row["enrichmentError"]=str(e)
        time.sleep(0.1)
    return {"candidates":len(rows),"repositories":rows,"errors":errors}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("watchlist",type=Path); ap.add_argument("catalog",type=Path)
    ap.add_argument("--per-query",type=int,default=10); ap.add_argument("--top",type=int,default=50)
    ap.add_argument("--cache",type=Path)
    ap.add_argument("--search-cache-ttl-hours",type=float,default=DEFAULT_SEARCH_CACHE_TTL_HOURS)
    ap.add_argument("--metadata-cache-ttl-hours",type=float,default=DEFAULT_METADATA_CACHE_TTL_HOURS)
    args=ap.parse_args()
    if not 1<=args.per_query<=100: ap.error("--per-query must be in [1,100]")
    if args.top<1: ap.error("--top must be >= 1")
    if args.search_cache_ttl_hours<0 or args.metadata_cache_ttl_hours<0: ap.error("cache TTLs must be >= 0")
    known={r["repo"] for r in json.loads(args.catalog.read_text()).get("repositories",[])}
    cache=load_cache(args.cache) if args.cache else None
    result=discover(
        json.loads(args.watchlist.read_text()),known,os.environ.get("GITHUB_TOKEN"),args.per_query,cache,
        args.search_cache_ttl_hours*3600,args.metadata_cache_ttl_hours*3600
    )
    result["repositories"]=result["repositories"][:args.top]; result["candidates"]=len(result["repositories"])
    if args.cache: save_cache(args.cache,cache)
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
