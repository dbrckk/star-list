#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/"scripts"/"validate_json_contract.py"
SCHEMAS=ROOT/"schemas"

required_schemas={
    "coverage-report.schema.json",
    "discovery-watchlist.schema.json",
    "discovery-candidates.schema.json",
    "discovery-evaluated.schema.json",
    "discovery-cache.schema.json",
    "discovery-memory.schema.json",
    "cache-health.schema.json",
    "cache-health-trend.schema.json",
    "cache-health-history.schema.json",
    "history.schema.json",
    "health-snapshot.schema.json",
    "health-drift.schema.json",
    "health-trends.schema.json",
    "replacement-report.schema.json",
    "catalog-stats.schema.json",
}

assert VALIDATOR.exists(), "missing JSON contract validator"
assert SCHEMAS.is_dir(), "missing schemas directory"
assert required_schemas <= {p.name for p in SCHEMAS.glob("*.schema.json")}, "missing pipeline schemas"

spec=importlib.util.spec_from_file_location("contract_validator",VALIDATOR)
validator=importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)

samples={
    "coverage-report.schema.json": {
        "policy":{"minHealthyPerDomain":3,"minHealthyPerCapability":2},
        "domainGaps":[],"capabilityGaps":[],"qualityGaps":[],
        "summary":{"domains":0,"capabilities":0,"domainGaps":0,"capabilityGaps":0,"qualityGaps":0},
    },
    "discovery-watchlist.schema.json": {"items":0,"watchlist":[]},
    "discovery-candidates.schema.json": {
        "candidates":0,"repositories":[],"errors":[],"staleSources":[],
        "cacheStats":{"logicalRequests":0,"freshCacheHits":0,"notModifiedHits":0,"staleFallbacks":0,"networkFetches":0,"apiCallAvoidanceRate":0.0,"bodyReuseRate":0.0},
    },
    "discovery-evaluated.schema.json": {
        "candidates":0,"counts":{"accept":0,"review":0,"reject":0},"repositories":[],"errors":[],"suppressedUnchanged":0,
    },
    "discovery-cache.schema.json": {"schemaVersion":1,"entries":{}},
    "discovery-memory.schema.json": {"schemaVersion":1,"candidates":{}},
    "cache-health.schema.json": {
        "status":"healthy","findings":[],"metrics":{"logicalRequests":0,"freshCacheHits":0,"notModifiedHits":0,"staleFallbacks":0,"networkFetches":0,"apiCallAvoidanceRate":0.0,"bodyReuseRate":0.0,"networkFetchRate":0.0,"staleFallbackRate":0.0},
    },
    "cache-health-trend.schema.json": {
        "direction":"insufficient-data","findings":[],"windowPoints":1,"apiCallAvoidanceDelta":None,"networkFetchDelta":None,
        "adaptiveBaseline":{"status":"insufficient-data","sampleSize":0,"threshold":0.2,"confidence":"insufficient-data","confidenceScore":0.0,"findings":[]},
        "adaptiveSeverity":"healthy","candidateSeverity":"healthy","alertState":"healthy","issueAction":"close",
    },
    "cache-health-history.schema.json": {"schemaVersion":1,"points":[]},
    "history.schema.json": {"schemaVersion":1,"repositories":{}},
    "health-snapshot.schema.json": {"repositories":[]},
    "health-drift.schema.json": {"dropThreshold":10.0,"findings":0,"repositories":[]},
    "health-trends.schema.json": {"repositories":[]},
    "replacement-report.schema.json": {"threshold":55.0,"findings":0,"repositories":[]},
    "catalog-stats.schema.json": {
        "repositories":0,"averageScore":0.0,"selfHosted":0,"selfHostedPercent":0.0,
        "domains":{},"tiers":{},"topLanguages":{},"topPlatforms":{},"topCapabilities":{},"domainLeaders":{},
    },
}

for schema_name,data in samples.items():
    schema=json.loads((SCHEMAS/schema_name).read_text())
    errors=validator.validate(data,schema)
    assert not errors, f"{schema_name}: {errors}"

for schema_name in required_schemas:
    schema=json.loads((SCHEMAS/schema_name).read_text())
    assert validator.validate({},schema), f"{schema_name} unexpectedly accepts empty object"

for data_name,schema_name in (
    ("discovery-cache.json","discovery-cache.schema.json"),
    ("discovery-memory.json","discovery-memory.schema.json"),
    ("cache-health-history.json","cache-health-history.schema.json"),
    ("history.json","history.schema.json"),
    ("health-snapshot.json","health-snapshot.schema.json"),
):
    data=json.loads((ROOT/data_name).read_text())
    schema=json.loads((SCHEMAS/schema_name).read_text())
    errors=validator.validate(data,schema)
    assert not errors, f"{data_name}: {errors}"

catalog_schema=json.loads((ROOT/"catalog.schema.json").read_text())
catalog=json.loads((ROOT/"catalog.json").read_text())
errors=validator.validate(catalog,catalog_schema)
assert not errors, f"catalog.json: {errors}"

unsupported={"type":"object","unevaluatedProperties":False}
errors=validator.validate({},unsupported)
assert errors and any("unsupported schema keyword" in error for error in errors), errors

print("OK: pipeline and catalog JSON contract tests passed")
