#!/usr/bin/env python3
"""Deterministic repository health scoring from catalog + refreshed GitHub metadata."""
import json, math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"

def age_days(pushed_at, now=None):
    if not pushed_at: return None
    try:
        dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    now = now or datetime.now(timezone.utc)
    return max(0, (now - dt).days)

def health_score(repo, now=None):
    gh = repo.get("github")
    if not isinstance(gh, dict):
        return {"score":None,"status":"unknown","reasons":["github-metadata-missing"]}
    if gh.get("archived") or gh.get("disabled"):
        return {"score":0.0,"status":"inactive","reasons":["archived-or-disabled"]}

    days = age_days(gh.get("pushedAt"), now)
    freshness = 35.0
    reasons = []
    if days is None:
        freshness = 12.0; reasons.append("push-date-missing")
    elif days <= 30: freshness = 35.0
    elif days <= 90: freshness = 32.0
    elif days <= 365: freshness = 25.0
    elif days <= 730: freshness = 14.0; reasons.append("stale-over-1y")
    else: freshness = 4.0; reasons.append("stale-over-2y")

    stars = max(0, gh.get("stars", 0))
    forks = max(0, gh.get("forks", 0))
    adoption = min(25.0, 5.0 * math.log10(stars + 1))
    ecosystem = min(15.0, 4.0 * math.log10(forks + 1))
    quality = max(0.0, min(20.0, 2.0 * float(repo.get("score", 0))))
    metadata = 5.0 if gh.get("license") else 2.0
    total = round(min(100.0, freshness + adoption + ecosystem + quality + metadata), 1)
    status = "healthy" if total >= 75 else "watch" if total >= 55 else "weak"
    return {"score":total,"status":status,"ageDays":days,"reasons":reasons}

def main():
    repos = json.loads(CATALOG.read_text()).get("repositories", [])
    rows = [{"repo":r["repo"], **health_score(r)} for r in repos]
    rows.sort(key=lambda x: (x["score"] is None, -(x["score"] or -1), x["repo"].lower()))
    print(json.dumps({"repositories":rows}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
