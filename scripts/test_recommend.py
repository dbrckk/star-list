#!/usr/bin/env python3
import json, subprocess, sys
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "recommend.py"

def run(*args):
    out = subprocess.check_output([sys.executable, str(SCRIPT), *args, "--json"], text=True)
    return json.loads(out)

cases = [
    ("xauusd backtesting risk execution", {"trading"}),
    ("android vector animation", {"mobile", "graphics"}),
    ("autonomous coding agent memory observability", {"ai_agents", "ai_memory"}),
]
for query, expected_any in cases:
    data = run(query, "--top", "5")
    domains = set(data["inferredDomains"])
    assert domains & expected_any, (query, domains)
    assert data["recommendations"], query
    assert all("repo" in x and "selectionScore" in x and "why" in x for x in data["recommendations"])
    assert data["diagnostics"]["catalogSize"] >= data["diagnostics"]["eligible"] >= data["diagnostics"]["returned"]

strict = run("android mobile", "--platform", "android", "--require-all-caps", "--cap", "mobile")
for item in strict["recommendations"]:
    assert "android" in item["platforms"]
    assert "mobile" in set(item["capabilities"]), item["repo"]

high_threshold = run("ai agent", "--min-score", "1000")
assert high_threshold["recommendations"] == []
assert high_threshold["diagnostics"]["returned"] == 0

default_audit = run("ponytail agent", "--top", "20")
assert all(item["tier"] != "audit" for item in default_audit["recommendations"])
assert default_audit["diagnostics"]["filtered"]["audit"] > 0
assert default_audit["constraints"]["includeAudit"] is False

with_audit = run("ponytail agent", "--top", "20", "--include-audit")
assert any(item["repo"] == "DietrichGebert/ponytail" for item in with_audit["recommendations"])
assert with_audit["constraints"]["includeAudit"] is True

spec = importlib.util.spec_from_file_location("recommend", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
assert mod.activity_adjustment({"github":{"archived":True}})[0] == -30.0
assert mod.activity_adjustment({"github":{"disabled":True}})[0] == -30.0
assert mod.activity_adjustment({}) == (0.0, None)
assert mod.trend_adjustment("definitely/not-in-history")[0] == 0.0
assert -6.0 <= mod.trend_adjustment("definitely/not-in-history")[0] <= 6.0
assert mod.guidance_weight({"guidanceSource":"curated"}) == 1.0
assert mod.guidance_weight({"guidanceSource":"inferred"}) == 0.55
assert mod.guidance_weight({"guidanceSource":"inferred", "tier":"specialized"}) == 0.35
assert mod.guidance_weight({}) == 1.0

base = {
    "repo":"x/example", "category":"", "domain":"backend", "capabilities":[],
    "roles":[], "score":9.0, "tier":"recommended", "bestFor":["specialized phrase"],
    "avoidWhen":[], "github":None,
}
qtokens = mod.tokens("specialized phrase")
curated = dict(base, guidanceSource="curated")
inferred = dict(base, guidanceSource="inferred")
assert mod.score_repo(curated, qtokens, set(), set(), set()) > mod.score_repo(inferred, qtokens, set(), set(), set())

source = {
    "repo":"x/source", "domain":"backend", "capabilities":["database"], "roles":[],
    "platforms":["cross-platform"], "languages":["python"], "selfHosted":True,
    "score":8.5, "tier":"recommended",
    "github":{"archived":False,"disabled":False,"license":"MIT","stars":1000,"forks":100,"openIssues":5,"pushedAt":"2026-09-01T00:00:00Z"},
}
candidate = {
    "repo":"x/candidate", "domain":"backend", "capabilities":["database","orm"], "roles":[],
    "platforms":["cross-platform"], "languages":["python"], "selfHosted":True,
    "score":9.0, "tier":"recommended",
    "github":{"archived":False,"disabled":False,"license":"MIT","stars":2000,"forks":200,"openIssues":5,"pushedAt":"2026-09-01T00:00:00Z"},
}
audit_candidate = dict(candidate, repo="x/audit", tier="audit")
assert mod.infer_alternatives(source, [source, candidate, audit_candidate]) == ["x/candidate"]

stack_repo = dict(candidate, repo="x/stack-tool", capabilities=["cache"])
repo_by_name = {r["repo"]: r for r in [source, stack_repo]}
stacks = [{"name":"Backend Stack","repos":["x/source","x/stack-tool"]}]
assert mod.infer_complements(source, stacks, repo_by_name) == ["x/stack-tool"]

curated_rel = dict(source, alternatives=["x/manual"], complements=["x/manual-comp"])
resolved = mod.resolve_relations(curated_rel, [curated_rel, candidate], stacks, repo_by_name)
assert resolved["alternatives"] == ["x/manual"]
assert resolved["alternativesSource"] == "curated"
assert resolved["complements"] == ["x/manual-comp"]
assert resolved["complementsSource"] == "curated"

print("OK: recommendation engine smoke tests passed")
