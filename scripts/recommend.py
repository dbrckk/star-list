#!/usr/bin/env python3
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path
from health_score import health_score

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
LEVEL = {"low": 0, "medium": 1, "high": 2}

def norm(s):
    return re.sub(r"[^a-z0-9+.#_-]+", " ", (s or "").lower()).strip()

def tokens(s):
    return {t for t in norm(s).split() if len(t) > 1}

def load():
    data = json.loads(CATALOG.read_text())
    stacks = json.loads(STACKS.read_text()) if STACKS.exists() else {"stacks": []}
    return data["repositories"], stacks.get("stacks", [])

def infer_domains(qtokens):
    return {DOMAIN_ALIASES[t] for t in qtokens if t in DOMAIN_ALIASES}

def activity_adjustment(r):
    gh = r.get("github")
    if not isinstance(gh, dict):
        return 0.0, None
    if gh.get("archived") or gh.get("disabled"):
        return -30.0, "inactive"
    pushed = gh.get("pushedAt")
    if not pushed:
        return 0.0, None
    try:
        dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        days = max(0, (datetime.now(timezone.utc) - dt).days)
    except (ValueError, TypeError):
        return 0.0, None
    if days <= 90: return 5.0, "active<=90d"
    if days <= 365: return 2.0, "active<=1y"
    if days <= 730: return -3.0, "stale>1y"
    return -8.0, "stale>2y"

def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps):
    caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
    if excluded_caps and caps & excluded_caps:
        return None
    rtoks = tokens(" ".join([
        r.get("repo", ""), r.get("category", ""), r.get("domain", ""),
        " ".join(caps), " ".join(r.get("bestFor", []))
    ]))
    lexical = len(qtokens & rtoks) / max(1, len(qtokens))
    cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
    domain_match = 1.0 if requested_domains and r.get("domain") in requested_domains else 0.0
    quality = max(0.0, min(1.0, r.get("score", 0) / 10.0))
    tier = TIER_BONUS.get(r.get("tier"), 0.0)
    best_for = tokens(" ".join(r.get("bestFor", [])))
    best_match = len(qtokens & best_for) / max(1, len(qtokens)) if best_for else 0.0
    s = 34*cap_match + 22*domain_match + 18*lexical + 12*best_match + 10*quality + 4*max(0.0, tier)
    if not required_caps:
        s += 12*lexical
    avoid = tokens(" ".join(r.get("avoidWhen", [])))
    if qtokens & avoid:
        s -= 18
    activity, _ = activity_adjustment(r)
    s += activity
    health = health_score(r)
    if health["score"] is not None:
        s += 6.0 * (health["score"] / 100.0)
    return round(s, 3)

def explain_repo(r, qtokens, domains, required_caps):
    caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
    best = tokens(" ".join(r.get("bestFor", [])))
    reasons = []
    if domains and r.get("domain") in domains:
        reasons.append("domain:" + r["domain"])
    matched_caps = sorted(required_caps & caps)
    if matched_caps:
        reasons.append("capabilities:" + ",".join(matched_caps))
    matched_terms = sorted(qtokens & (tokens(r.get("repo", "")) | caps | best))
    if matched_terms:
        reasons.append("terms:" + ",".join(matched_terms[:6]))
    if r.get("tier") in {"core", "recommended"}:
        reasons.append("tier:" + r["tier"])
    _, activity_reason = activity_adjustment(r)
    if activity_reason:
        reasons.append("activity:" + activity_reason)
    return reasons[:4]

def choose_stack(stacks, qtokens, domains):
    best, best_score = None, -1
    for st in stacks:
        stoks = tokens(st.get("name", "") + " " + st.get("goal", "") + " " + " ".join(st.get("notes", [])))
        score = 2*len(qtokens & stoks) + (3 if st.get("domain") in domains else 0)
        if score > best_score:
            best_score, best = score, st
    return best if best_score > 0 else None

def main():
    ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
    ap.add_argument("query", help="Natural-language task/query")
    ap.add_argument("--cap", action="append", default=[], help="Desired capability; repeatable")
    ap.add_argument("--require-all-caps", action="store_true", help="Reject repositories missing any --cap capability")
    ap.add_argument("--exclude-cap", action="append", default=[], help="Excluded capability; repeatable")
    ap.add_argument("--domain", action="append", default=[], help="Force a domain; repeatable")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=0.0, help="Minimum selection score")
    ap.add_argument("--platform", action="append", default=[], help="Required platform; repeatable")
    ap.add_argument("--language", action="append", default=[], help="Required language; repeatable")
    ap.add_argument("--self-hosted", action="store_true", help="Require self-hosted/local-friendly repositories")
    ap.add_argument("--include-archived", action="store_true", help="Allow archived/disabled repositories")
    ap.add_argument("--max-resource", choices=["low","medium","high"], default="high")
    ap.add_argument("--max-complexity", choices=["low","medium","high"], default="high")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    if args.top < 1:
        ap.error("--top must be >= 1")
    if args.min_score < 0:
        ap.error("--min-score must be >= 0")

    repos, stacks = load()
    qtokens = tokens(args.query)
    domains = set(args.domain) or infer_domains(qtokens)
    required_caps, excluded_caps = set(args.cap), set(args.exclude_cap)
    ranked = []
    filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}

    for r in repos:
        caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
        if args.platform and not set(args.platform).issubset(set(r.get("platforms", []))):
            filtered["platform"] += 1; continue
        if args.language and not set(args.language).issubset(set(r.get("languages", []))):
            filtered["language"] += 1; continue
        if args.self_hosted and r.get("selfHosted") is not True:
            filtered["selfHosted"] += 1; continue
        gh = r.get("github", {})
        if not args.include_archived and isinstance(gh, dict) and (gh.get("archived") or gh.get("disabled")):
            filtered["inactive"] += 1; continue
        if LEVEL.get(r.get("resourceLevel","medium"),1) > LEVEL[args.max_resource]:
            filtered["resource"] += 1; continue
        if LEVEL.get(r.get("integrationComplexity","medium"),1) > LEVEL[args.max_complexity]:
            filtered["complexity"] += 1; continue
        if args.require_all_caps and not required_caps.issubset(caps):
            filtered["capability"] += 1; continue
        s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
        if s is None:
            filtered["excluded"] += 1; continue
        if s < args.min_score or s <= 0:
            filtered["minScore"] += 1; continue
        ranked.append((s, r))

    ranked.sort(key=lambda x: (-x[0], -x[1].get("score", 0), x[1]["repo"].lower()))
    top = []
    for s, r in ranked[:args.top]:
        top.append({
            "repo": r["repo"], "selectionScore": s, "qualityScore": r.get("score"),
            "tier": r.get("tier"), "domain": r.get("domain"),
            "capabilities": r.get("capabilities", []), "bestFor": r.get("bestFor", []),
            "avoidWhen": r.get("avoidWhen", []), "alternatives": r.get("alternatives", []),
            "complements": r.get("complements", []), "languages": r.get("languages", []),
            "platforms": r.get("platforms", []), "selfHosted": r.get("selfHosted"),
            "resourceLevel": r.get("resourceLevel"), "integrationComplexity": r.get("integrationComplexity"),
            "why": explain_repo(r, qtokens, domains, required_caps),
            "health": health_score(r),
        })

    result = {
        "query": args.query, "inferredDomains": sorted(domains),
        "requiredCapabilities": sorted(required_caps), "recommendations": top,
        "constraints": {"platforms":args.platform, "languages":args.language, "selfHosted":args.self_hosted,
                        "maxResource":args.max_resource, "maxComplexity":args.max_complexity,
                        "requireAllCapabilities":args.require_all_caps, "minScore":args.min_score, "includeArchived":args.include_archived},
        "diagnostics": {"catalogSize":len(repos), "eligible":len(ranked), "returned":len(top), "filtered":filtered},
        "recommendedStack": choose_stack(stacks, qtokens, domains),
    }
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Query: {args.query}")
        if domains: print("Domains:", ", ".join(sorted(domains)))
        for i, item in enumerate(top, 1):
            print(f"{i}. {item['repo']} | selection={item['selectionScore']:.1f} | quality={item['qualityScore']}/10 | {item['tier']}")
            if item["why"]: print("   why:", "; ".join(item["why"]))
            if item["bestFor"]: print("   bestFor:", "; ".join(item["bestFor"][:3]))
            if item["complements"]: print("   complements:", ", ".join(item["complements"][:4]))
        if result["recommendedStack"]:
            st = result["recommendedStack"]
            print(f"\nSuggested stack: {st['name']}")
            print(" + ".join(st.get("repos", [])))
        print(f"\nEligible: {len(ranked)}/{len(repos)} | returned: {len(top)}")

if __name__ == "__main__":
    main()
