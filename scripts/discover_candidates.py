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
DEFAULT_SEARCH_STALE_MAX_HOURS=168
DEFAULT_METADATA_STALE_MAX_HOURS=2160

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

def _cache_entry(cache, url):
    entry=cache.get("entries",{}).get(url) if isinstance(cache,dict) else None
    if not isinstance(entry,dict): return None
    fetched=entry.get("fetchedAt")
    if not isinstance(fetched,(int,float)): return None
    return entry

def _headers_dict(headers):
    if headers is None: return {}
    try: return dict(headers.items())
    except AttributeError: return dict(headers)

def _header_value(headers, name):
    wanted=name.lower()
    for key,value in (headers or {}).items():
        if str(key).lower()==wanted: return value
    return None

def cache_get(cache, url, ttl_seconds, now=None):
    now=time.time() if now is None else now
    entry=_cache_entry(cache,url)
    if entry is None or now-entry["fetchedAt"]>ttl_seconds: return None
    return entry.get("data"), entry.get("headers",{})

def cache_get_stale(cache, url, max_age_seconds, now=None):
    if max_age_seconds<=0: return None
    now=time.time() if now is None else now
    entry=_cache_entry(cache,url)
    if entry is None: return None
    age=max(0,now-entry["fetchedAt"])
    if age>max_age_seconds: return None
    return entry.get("data"), entry.get("headers",{})

def cache_put(cache, url, data, headers, now=None):
    now=time.time() if now is None else now
    cache.setdefault("schemaVersion",CACHE_SCHEMA_VERSION)
    cache.setdefault("entries",{})[url]={"fetchedAt":now,"data":data,"headers":_headers_dict(headers)}

def _api_result(data, headers, source, return_source):
    return (data,headers,source) if return_source else (data,headers)

def _stale_result(cache, url, stale_max_seconds, now, return_source):
    stale=cache_get_stale(cache,url,stale_max_seconds,now) if cache is not None else None
    if stale is None: return None
    return _api_result(stale[0],stale[1],"stale-cache",return_source)

def _conditional_headers(headers, cache, url):
    result=dict(headers or {})
    entry=_cache_entry(cache,url)
    if entry is None: return result
    etag=_header_value(entry.get("headers",{}),"etag")
    if etag and not _header_value(result,"if-none-match"):
        result["If-None-Match"]=etag
    return result

def _not_modified_result(cache, url, response_headers, now, return_source):
    entry=_cache_entry(cache,url)
    if entry is None: return None
    merged_headers=dict(entry.get("headers",{}) or {})
    merged_headers.update(_headers_dict(response_headers))
    data=entry.get("data")
    cache_put(cache,url,data,merged_headers,now)
    return _api_result(data,merged_headers,"not-modified",return_source)

def api_json(url, headers, attempts=4, cache=None, ttl_seconds=0, stale_max_seconds=0, now=None, return_source=False):
    if cache is not None and ttl_seconds>0:
        hit=cache_get(cache,url,ttl_seconds,now)
        if hit is not None:
            return _api_result(hit[0],hit[1],"fresh-cache",return_source)
    request_headers=_conditional_headers(headers,cache,url) if cache is not None and ttl_seconds>0 else dict(headers or {})
    last=None
    for attempt in range(attempts):
        try:
            with urlopen(Request(url,headers=request_headers),timeout=20) as res:
                data=json.load(res)
                response_headers=_headers_dict(res.headers)
                if cache is not None and ttl_seconds>0:
                    cache_put(cache,url,data,response_headers,now)
                return _api_result(data,response_headers,"network",return_source)
        except HTTPError as e:
            last=e
            if e.code==304:
                not_modified=_not_modified_result(cache,url,e.headers,now,return_source)
                if not_modified is not None: return not_modified
                raise
            transient=e.code in (403,429,500,502,503,504)
            if not transient: raise
            if attempt==attempts-1:
                stale=_stale_result(cache,url,stale_max_seconds,now,return_source)
                if stale is not None: return stale
                raise
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
            if attempt==attempts-1:
                stale=_stale_result(cache,url,stale_max_seconds,now,return_source)
                if stale is not None: return stale
                raise
            time.sleep(min(30,2**attempt)+random.random())
    raise last

def fetch(query, token=None, per_page=10, cache=None, ttl_seconds=0, stale_max_seconds=0, return_source=False):
    params=urlencode({"q":query,"sort":"stars","order":"desc","per_page":per_page})
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    data,_,source=api_json(
        f"{API}?{params}",headers,cache=cache,ttl_seconds=ttl_seconds,
        stale_max_seconds=stale_max_seconds,return_source=True,
    )
    return (data,source) if return_source else data

def enrich(repo, token=None, cache=None, ttl_seconds=0, stale_max_seconds=0):
    headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"]=f"Bearer {token}"
    stale_endpoints=[]
    data,_,source=api_json(
        REPO_API.format(repo),headers,cache=cache,ttl_seconds=ttl_seconds,
        stale_max_seconds=stale_max_seconds,return_source=True,
    )
    if source=="stale-cache": stale_endpoints.append("repository")
    out={"topics":data.get("topics",[]),"watchers":data.get("subscribers_count",0),
         "size":data.get("size"),"openIssues":data.get("open_issues_count",0),
         "createdAt":data.get("created_at"),"homepage":data.get("homepage"),
         "hasDiscussions":data.get("has_discussions",False)}
    for key,path in (("latestRelease","releases/latest"),("contributors","contributors?per_page=1&anon=true")):
        try:
            payload,response_headers,source=api_json(
                f"{REPO_API.format(repo)}/{path}",headers,cache=cache,ttl_seconds=ttl_seconds,
                stale_max_seconds=stale_max_seconds,return_source=True,
            )
            if source=="stale-cache": stale_endpoints.append(key)
            if key=="latestRelease": out[key]={"tag":payload.get("tag_name"),"publishedAt":payload.get("published_at")}
            else:
                link=response_headers.get("Link","")
                import re
                m=re.search(r'[?&]page=(\\d+)>; rel="last"',link)
                out[key]=int(m.group(1)) if m else len(payload)
        except Exception: out[key]=None
    if stale_endpoints:
        out["metadataStale"]=True
        out["staleEndpoints"]=stale_endpoints
    return out

def score(item, priority):
    stars=max(0,item.get("stargazers_count",0)); forks=max(0,item.get("forks_count",0))
    popularity=min(25,5*math.log10(stars+1)); ecosystem=min(15,4*math.log10(forks+1))
    metadata=5 if item.get("license") else 2
    return round(min(100, 0.45*priority + popularity + ecosystem + metadata),1)

def discover(watchlist, known, token=None, per_query=10, cache=None, search_ttl_seconds=0, metadata_ttl_seconds=0,
             search_stale_max_seconds=0, metadata_stale_max_seconds=0):
    candidates={}
    errors=[]
    stale_sources=[]
    for target in watchlist.get("watchlist",[]):
        try:
            data,source=fetch(
                target["query"],token,per_query,cache,search_ttl_seconds,
                search_stale_max_seconds,return_source=True,
            )
            if source=="stale-cache":
                stale_sources.append({"kind":"search","target":target["target"]})
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
        try:
            enriched=enrich(row["repo"],token,cache,metadata_ttl_seconds,metadata_stale_max_seconds)
            row.update(enriched)
            if enriched.get("metadataStale"):
                stale_sources.append({"kind":"metadata","repo":row["repo"],"endpoints":enriched.get("staleEndpoints",[])})
        except Exception as e: row["enrichmentError"]=str(e)
        time.sleep(0.1)
    return {"candidates":len(rows),"repositories":rows,"errors":errors,"staleSources":stale_sources}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("watchlist",type=Path); ap.add_argument("catalog",type=Path)
    ap.add_argument("--per-query",type=int,default=10); ap.add_argument("--top",type=int,default=50)
    ap.add_argument("--cache",type=Path)
    ap.add_argument("--search-cache-ttl-hours",type=float,default=DEFAULT_SEARCH_CACHE_TTL_HOURS)
    ap.add_argument("--metadata-cache-ttl-hours",type=float,default=DEFAULT_METADATA_CACHE_TTL_HOURS)
    ap.add_argument("--search-stale-max-hours",type=float,default=DEFAULT_SEARCH_STALE_MAX_HOURS)
    ap.add_argument("--metadata-stale-max-hours",type=float,default=DEFAULT_METADATA_STALE_MAX_HOURS)
    args=ap.parse_args()
    if not 1<=args.per_query<=100: ap.error("--per-query must be in [1,100]")
    if args.top<1: ap.error("--top must be >= 1")
    ttls=(args.search_cache_ttl_hours,args.metadata_cache_ttl_hours,args.search_stale_max_hours,args.metadata_stale_max_hours)
    if any(x<0 for x in ttls): ap.error("cache TTL and stale fallback windows must be >= 0")
    known={r["repo"] for r in json.loads(args.catalog.read_text()).get("repositories",[])}
    cache=load_cache(args.cache) if args.cache else None
    result=discover(
        json.loads(args.watchlist.read_text()),known,os.environ.get("GITHUB_TOKEN"),args.per_query,cache,
        args.search_cache_ttl_hours*3600,args.metadata_cache_ttl_hours*3600,
        args.search_stale_max_hours*3600,args.metadata_stale_max_hours*3600,
    )
    result["repositories"]=result["repositories"][:args.top]; result["candidates"]=len(result["repositories"])
    if args.cache: save_cache(args.cache,cache)
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
