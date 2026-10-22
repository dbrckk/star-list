#!/usr/bin/env python3
"""Offline proof: drift checks preserve original source facts and identity."""
import json
from pathlib import Path
from check_readme_evidence_freshness import check, inspect

ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/"catalog-readme-evidence.json").read_text())["sources"]
known=records[0]
def repo(name, token=None):
    return {"id":known["githubRepositoryId"]}
def content(name, path="", token=None):
    return {"sha":known["blobSha"]}
base=inspect(known,repo,content)
assert base["status"]=="unchanged",base
assert base["currentBlobSha"]==known["blobSha"]
assert inspect(known,repo,lambda *args,**kw:{"sha":"f"*40})["status"]=="review-outdated"
assert inspect(known,lambda *args,**kw:{"id":known["githubRepositoryId"]+1},
               content)["status"]=="repository-identity-changed"
assert inspect(known,repo,lambda *args,**kw:{})["status"]=="readme-unavailable"
def failed(*args,**kwargs):
    raise RuntimeError("GitHub rate limited")
assert inspect(known,failed,content)["status"]=="api-error"
reports=check([known],1,0,repo,content)
assert reports["counts"]["unchanged"]==1
assert reports["catalogOrIntegrationChanged"] is False
assert reports["inspected"]==1
assert reports["totalSources"]==1
assert reports["findings"][0]["repo"]==known["repository"]
try:
    check(records,10,999,repo,content)
except ValueError:
    pass
else:
    raise AssertionError("Invalid batch accepted")
print("OK: upstream SHA drift, failed API, identity transfer and no-write guards")
