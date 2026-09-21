#!/usr/bin/env python3
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "catalog.json").read_text())
errors, warnings = [], []
valid_domains = {"ai_agents","ai_memory","ai_media","software_engineering","web_frontend","backend","mobile","graphics","game_dev","trading","cybersecurity","data_ml","devops","productivity","other"}
valid_roles = {"data","alpha","regime","backtest","risk","execution","portfolio","xauusd","macro","ml","microstructure","performance","volatility","optimization","forecasting","feature-engineering","derivatives","diagnostic","feature-selection","filtering"}
valid_tiers = {"core","recommended","specialized","audit"}
valid_levels = {"low","medium","high"}
valid_lifecycles = {"active","stable","reference","legacy"}
valid_guidance_sources = {"curated","inferred"}
seen = set()
repos = data.get("repositories", [])

if not isinstance(repos, list) or not repos:
    errors.append("catalog.repositories must be a non-empty list")

for i, r in enumerate(repos):
    name = r.get("repo", "")
    prefix = name or f"entry[{i}]"
    if not re.match(r"^[^/\s]+/[^/\s]+$", name):
        errors.append(f"{prefix}: invalid repo")
    if name in seen:
        errors.append(f"{prefix}: duplicate repo")
    seen.add(name)

    score = r.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 10:
        errors.append(f"{prefix}: score must be numeric in [0,10]")
        score = -1

    tier = r.get("tier")
    if tier not in valid_tiers:
        errors.append(f"{prefix}: invalid tier {tier}")
    if tier == "core" and score < 9.5: errors.append(f"{prefix}: core requires score >= 9.5")
    if tier == "recommended" and score < 9.0: errors.append(f"{prefix}: recommended requires score >= 9.0")
    if tier == "specialized" and score < 8.0: errors.append(f"{prefix}: specialized requires score >= 8.0")
    if tier in {"core", "recommended"}:
        if not r.get("bestFor"):
            errors.append(f"{prefix}: {tier} repositories require bestFor guidance")
        if not r.get("avoidWhen"):
            errors.append(f"{prefix}: {tier} repositories require avoidWhen guidance")

    domain = r.get("domain")
    if domain not in valid_domains:
        errors.append(f"{prefix}: invalid domain {domain}")

    lifecycle = r.get("lifecycle")
    if lifecycle is not None and lifecycle not in valid_lifecycles:
        errors.append(f"{prefix}: invalid lifecycle {lifecycle}")
    guidance_source = r.get("guidanceSource")
    if guidance_source is not None and guidance_source not in valid_guidance_sources:
        errors.append(f"{prefix}: invalid guidanceSource {guidance_source}")

    for field in ("capabilities","roles","bestFor","avoidWhen","alternatives","complements","languages","platforms"):
        value = r.get(field, [])
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            errors.append(f"{prefix}: {field} must be a list of non-empty strings")
        elif len(value) != len(set(value)):
            warnings.append(f"{prefix}: duplicate values in {field}")

    for field in ("resourceLevel","integrationComplexity"):
        if r.get(field) not in valid_levels:
            errors.append(f"{prefix}: invalid {field} {r.get(field)}")
    self_hosted = r.get("selfHosted")
    if not isinstance(self_hosted, bool):
        warnings.append(f"{prefix}: selfHosted metadata is unknown or non-boolean")

    gh = r.get("github")
    if gh is not None:
        if not isinstance(gh, dict):
            errors.append(f"{prefix}: github metadata must be an object")
        else:
            for field in ("stars", "forks", "openIssues"):
                value = gh.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    errors.append(f"{prefix}: github.{field} must be a non-negative integer")
            for field in ("archived", "disabled"):
                if not isinstance(gh.get(field), bool):
                    errors.append(f"{prefix}: github.{field} must be boolean")
            if not isinstance(gh.get("defaultBranch"), str) or not gh.get("defaultBranch"):
                errors.append(f"{prefix}: github.defaultBranch must be a non-empty string")
            if gh.get("license") is not None and not isinstance(gh.get("license"), str):
                errors.append(f"{prefix}: github.license must be string or null")
            if gh.get("pushedAt") is not None and not isinstance(gh.get("pushedAt"), str):
                errors.append(f"{prefix}: github.pushedAt must be string or null")

    if domain == "trading":
        roles = set(r.get("roles", []))
        bad = roles - valid_roles
        if not roles: warnings.append(f"{prefix}: trading repo missing roles metadata")
        if bad: errors.append(f"{prefix}: unknown roles {sorted(bad)}")

# Relationship integrity: known catalog repos only, no self-links.
for r in repos:
    name = r.get("repo", "")
    for field in ("alternatives","complements"):
        for target in r.get(field, []):
            if target == name:
                errors.append(f"{name}: {field} contains self-reference")
            elif target not in seen:
                warnings.append(f"{name}: {field} references uncatalogued repo {target}")

counts = Counter(r.get("domain") for r in repos)
if warnings:
    print("WARNINGS:")
    print("\n".join(sorted(set(warnings))))
if errors:
    print("ERRORS:")
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(seen)} repositories | {len(counts)} domains | {len(set(warnings))} warnings")
