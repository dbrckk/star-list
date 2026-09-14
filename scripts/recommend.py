#!/usr/bin/env python3
import argparse, json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
STACKS = ROOT / "stacks.json"

DOMAIN_ALIASES = {
    "ai": "ai_agents", "agent": "ai_agents", "agents": "ai_agents",
    "memory": "ai_memory", "rag": "ai_memory",
    "media": "ai_media", "image": "ai_media", "audio": "ai_media", "video": "ai_media",
    "code": "software_engineering", "coding": "software_engineering", "dev": "software_engineering",
    "frontend": "web_frontend", "web": "web_frontend",
    "backend": "backend", "api": "backend",
    "android": "mobile", "mobile": "mobile", "flutter": "mobile",
    "graphics": "graphics", "vector": "graphics", "animation": "graphics", "3d": "graphics",
    "game": "game_dev", "gaming": "game_dev",
    "trading": "trading", "quant": "trading", "xauusd": "trading", "gold": "trading",
    "security": "cybersecurity", "cyber": "cybersecurity", "pentest": "cybersecurity", "osint": "cybersecurity",
    "ml": "data_ml", "data": "data_ml",
    "devops": "devops", "infra": "devops", "ci": "devops",
    "automation": "productivity", "productivity": "productivity",
}

TIER_BONUS = {"core": 1.0, "recommended": 0.6, "specialized": 0.25, "audit": -0.4}

def norm(s):
    return re.sub(r"[^a-z0-9+.#_-]+", " ", (s or "").lower()).strip()

def tokens(s):
    return {t for t in norm(s).split() if len(t) > 1}

def load():
    data = json.loads(CATALOG.read_text())
    stacks = json.loads(STACKS.read_text()) if STACKS.exists() else {"stacks": []}
    return data["repositories"], stacks.get("stacks", [])

def infer_domains(qtokens):
    out = set()
    for tok in qtokens:
        if tok in DOMAIN_ALIASES:
            out.add(DOMAIN_ALIASES[tok])
    return out

def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps):
    caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
    text_fields = " ".join([
        r.get("repo", ""), r.get("category", ""), r.get("domain", ""),
        " ".join(caps), " ".join(r.get("bestFor", []))
    ])
    rtoks = tokens(text_fields)

    if excluded_caps and (caps & excluded_caps):
        return None

    lexical = len(qtokens & rtoks) / max(1, len(qtokens))
    cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
    domain_match = 1.0 if requested_domains and r.get("domain") in requested_domains else 0.0
    quality = max(0.0, min(1.0, r.get("score", 0) / 10.0))
    tier = TIER_BONUS.get(r.get("tier"), 0.0)

    best_for = tokens(" ".join(r.get("bestFor", [])))
    best_match = len(qtokens & best_for) / max(1, len(qtokens)) if best_for else 0.0

    # 0..100
    s = (
        34 * cap_match +
        22 * domain_match +
        18 * lexical +
        12 * best_match +
        10 * quality +
        4 * max(0.0, tier)
    )

    # If no explicit capabilities were requested, lexical/domain fit drives selection.
    if not required_caps:
        s += 12 * lexical

    # Penalize avoidWhen overlap.
    avoid = tokens(" ".join(r.get("avoidWhen", [])))
    if qtokens & avoid:
        s -= 18

    return round(s, 3)

def choose_stack(stacks, qtokens, domains):
    best = None
    best_score = -1
    for st in stacks:
        stoks = tokens(st.get("name", "") + " " + st.get("goal", "") + " " + " ".join(st.get("notes", [])))
        score = 2 * len(qtokens & stoks)
        if st.get("domain") in domains:
            score += 3
        if score > best_score:
            best_score, best = score, st
    return best if best_score > 0 else None

def main():
    ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
    ap.add_argument("query", help="Natural-language task/query")
    ap.add_argument("--cap", action="append", default=[], help="Required capability; repeatable")
    ap.add_argument("--exclude-cap", action="append", default=[], help="Excluded capability; repeatable")
    ap.add_argument("--domain", action="append", default=[], help="Force a domain; repeatable")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    repos, stacks = load()
    qtokens = tokens(args.query)
    domains = set(args.domain) or infer_domains(qtokens)
    required_caps = set(args.cap)
    excluded_caps = set(args.exclude_cap)

    ranked = []
    for r in repos:
        s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
        if s is not None and s > 0:
            ranked.append((s, r))
    ranked.sort(key=lambda x: (-x[0], -x[1].get("score", 0), x[1]["repo"].lower()))

    top = []
    for s, r in ranked[:args.top]:
        top.append({
            "repo": r["repo"],
            "selectionScore": s,
            "qualityScore": r.get("score"),
            "tier": r.get("tier"),
            "domain": r.get("domain"),
            "capabilities": r.get("capabilities", []),
            "bestFor": r.get("bestFor", []),
            "avoidWhen": r.get("avoidWhen", []),
            "alternatives": r.get("alternatives", []),
            "complements": r.get("complements", []),
        })

    result = {
        "query": args.query,
        "inferredDomains": sorted(domains),
        "requiredCapabilities": sorted(required_caps),
        "recommendations": top,
        "recommendedStack": choose_stack(stacks, qtokens, domains),
    }

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Query: {args.query}")
        if domains:
            print("Domains:", ", ".join(sorted(domains)))
        for i, item in enumerate(top, 1):
            print(f"{i}. {item['repo']} | selection={item['selectionScore']:.1f} | quality={item['qualityScore']}/10 | {item['tier']}")
            if item["bestFor"]:
                print("   bestFor:", "; ".join(item["bestFor"][:3]))
            if item["complements"]:
                print("   complements:", ", ".join(item["complements"][:4]))
        if result["recommendedStack"]:
            st = result["recommendedStack"]
            print(f"\nSuggested stack: {st['name']}")
            print(" + ".join(st.get("repos", [])))

if __name__ == "__main__":
    main()
