#!/usr/bin/env python3
"""Detect unhealthy catalog entries and rank safer in-catalog replacements."""
import argparse, json
from pathlib import Path
from health_score import health_score

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"

def overlap(a, b):
    a, b = set(a or []), set(b or [])
    return len(a & b) / max(1, len(a | b))

def replacement_score(source, candidate):
    if source["repo"] == candidate["repo"]:
        return None
    health = health_score(candidate)
    if health["score"] is None or health["status"] in {"inactive","weak"}:
        return None
    domain = 1.0 if source.get("domain") == candidate.get("domain") else 0.0
    caps = overlap(source.get("capabilities"), candidate.get("capabilities"))
    roles = overlap(source.get("roles"), candidate.get("roles"))
    platforms = overlap(source.get("platforms"), candidate.get("platforms"))
    languages = overlap(source.get("languages"), candidate.get("languages"))
    self_hosted = 1.0 if source.get("selfHosted") == candidate.get("selfHosted") else 0.0
    fit = 35*domain + 25*caps + 12*roles + 8*platforms + 5*languages + 5*self_hosted
    fit += 10 * (health["score"] / 100.0)
    return round(fit, 2), health

def analyze(repos, threshold=55, top=3):
    findings = []
    for source in repos:
        health = health_score(source)
        if health["score"] is None:
            continue
        if health["status"] not in {"inactive","weak"} and health["score"] >= threshold:
            continue
        candidates = []
        for candidate in repos:
            result = replacement_score(source, candidate)
            if result is None: continue
            score, candidate_health = result
            if candidate_health["score"] <= health["score"]: continue
            candidates.append({
                "repo":candidate["repo"], "replacementScore":score,
                "health":candidate_health, "qualityScore":candidate.get("score"),
                "domain":candidate.get("domain")
            })
        candidates.sort(key=lambda x:(-x["replacementScore"], -(x["health"]["score"] or 0), x["repo"].lower()))
        findings.append({
            "repo":source["repo"], "health":health, "qualityScore":source.get("score"),
            "domain":source.get("domain"), "suggestedReplacements":candidates[:top]
        })
    findings.sort(key=lambda x:(x["health"]["score"], x["repo"].lower()))
    return findings

def main():
    ap = argparse.ArgumentParser(description="Find catalog repositories that should be reviewed or replaced.")
    ap.add_argument("--threshold", type=float, default=55)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--fail-on-findings", action="store_true")
    args = ap.parse_args()
    if not 0 <= args.threshold <= 100: ap.error("--threshold must be in [0,100]")
    if args.top < 1: ap.error("--top must be >= 1")
    repos = json.loads(CATALOG.read_text()).get("repositories", [])
    findings = analyze(repos, args.threshold, args.top)
    print(json.dumps({"threshold":args.threshold,"findings":len(findings),"repositories":findings}, indent=2, ensure_ascii=False))
    if findings and args.fail_on_findings:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
