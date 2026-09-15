#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"

def main():
    repos = json.loads(CATALOG.read_text()).get("repositories", [])
    domains = Counter(r.get("domain", "other") for r in repos)
    tiers = Counter(r.get("tier", "unknown") for r in repos)
    languages = Counter(x for r in repos for x in r.get("languages", []))
    platforms = Counter(x for r in repos for x in r.get("platforms", []))
    capabilities = Counter(x for r in repos for x in r.get("capabilities", []))
    self_hosted = sum(r.get("selfHosted") is True for r in repos)
    scores = [r.get("score", 0) for r in repos if isinstance(r.get("score"), (int, float))]
    by_domain = defaultdict(list)
    for r in repos:
        by_domain[r.get("domain", "other")].append(r)

    report = {
        "repositories": len(repos),
        "averageScore": round(sum(scores) / len(scores), 3) if scores else 0,
        "selfHosted": self_hosted,
        "selfHostedPercent": round(100 * self_hosted / len(repos), 1) if repos else 0,
        "domains": dict(domains.most_common()),
        "tiers": dict(tiers.most_common()),
        "topLanguages": dict(languages.most_common(15)),
        "topPlatforms": dict(platforms.most_common(15)),
        "topCapabilities": dict(capabilities.most_common(20)),
        "domainLeaders": {
            domain: [
                {"repo": r["repo"], "score": r.get("score"), "tier": r.get("tier")}
                for r in sorted(items, key=lambda x: (-x.get("score", 0), x["repo"]))[:5]
            ]
            for domain, items in sorted(by_domain.items())
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
