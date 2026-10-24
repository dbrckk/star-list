#!/usr/bin/env python3
import argparse, json, re
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from health_score import health_score
from find_replacements import replacement_score
from agent_skill_discovery import SKILL_ISSUE_URL, recommend_skills, word_set
from catalog_domain_evidence import (
    advisory_domain_evidence, reviewed_readme_task_terms
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
STACKS = ROOT / "stacks.json"
HISTORY = ROOT / "history.json"
WEBSITES = ROOT / "websites.json"

DOMAIN_ALIASES = {
    "ai": "ai_agents", "agent": "ai_agents", "agents": "ai_agents",
    "memory": "ai_memory", "rag": "ai_memory",
    "media": "ai_media", "image": "ai_media", "audio": "ai_media", "video": "ai_media",
    "code": "software_engineering", "coding": "software_engineering", "dev": "software_engineering",
    "frontend": "web_frontend", "web": "web_frontend",
    "backend": "backend", "api": "backend",
    "android": "mobile", "mobile": "mobile", "flutter": "mobile",
    "graphics": "graphics", "vector": "graphics", "animation": "graphics", "3d": "graphics",
    "game": "game_dev", "gaming": "game_dev", "roblox": "game_dev",
    "godot": "game_dev", "luau": "game_dev",
    "trading": "trading", "quant": "trading", "xauusd": "trading", "gold": "trading",
    "security": "cybersecurity", "cyber": "cybersecurity", "pentest": "cybersecurity", "osint": "cybersecurity",
    "ml": "data_ml", "data": "data_ml",
    "devops": "devops", "infra": "devops", "ci": "devops",
    "esp32": "embedded_iot", "esp8266": "embedded_iot", "arduino": "embedded_iot",
    "firmware": "embedded_iot", "iot": "embedded_iot", "embedded": "embedded_iot",
    "microcontroller": "embedded_iot", "drone": "embedded_iot", "robotics": "embedded_iot",
    "education": "education", "curriculum": "education", "teaching": "education",
    "learning": "education", "school": "education",
    "automation": "productivity", "productivity": "productivity",
    "marketing": "marketing", "seo": "marketing", "outreach": "marketing",
    "campaign": "marketing", "campaigns": "marketing", "social": "marketing",
    "social-media": "marketing",
    "writing": "writing", "rewrite": "writing", "rewriting": "writing",
    "paraphrase": "writing", "paraphrasing": "writing",
    "copywriting": "writing", "editorial": "writing",
    "newsletter": "writing", "proofreading": "writing",
    "essay": "writing", "blog": "writing", "emails": "writing",
}
TIER_BONUS = {"core": 1.0, "recommended": 0.6, "specialized": 0.25, "indexed": -0.4}
LEVEL = {"low": 0, "medium": 1, "high": 2}
GUIDANCE_WEIGHT = {"curated": 1.0, "inferred": 0.55}
SPECIALIZED_INFERRED_WEIGHT = 0.35

def norm(s):
    return re.sub(r"[^a-z0-9+.#_-]+", " ", (s or "").lower()).strip()

def tokens(s):
    return {t for t in norm(s).split() if len(t) > 1}

def load():
    data = json.loads(CATALOG.read_text())
    stacks = json.loads(STACKS.read_text()) if STACKS.exists() else {"stacks": []}
    return data["repositories"], stacks.get("stacks", [])

def infer_domains(qtokens):
    domains = {DOMAIN_ALIASES[t] for t in qtokens if t in DOMAIN_ALIASES}
    # "AI" alone is generic. In an explicitly media, graphics, marketing, or
    # writing task, it should not add a spurious coding-agent domain.
    explicit_agents = {"agent", "agents", "coding", "code", "dev"}
    if ("ai" in qtokens and len(domains) > 1
            and not qtokens.intersection(explicit_agents)):
        domains.discard("ai_agents")
    return domains


# Generic connective words in curator prose are not evidence that a website
# applies to a project (e.g. "and" in both a TTS description and art guidance).
WEBSITE_MATCH_STOPWORDS = frozenset(
    "a an and are as at be by for from in into is its of on or our the their "
    "these this to using via was were with your".split()
)


def website_review_gates(site):
    """Stable, auditable reasons a curated web resource needs separate review.

    These are discovery metadata only, not install instructions or a grant of
    commercial image/model rights. All web resources remain non-executable.
    """
    gates = []
    resource_type = site.get("type")
    reuse = site.get("reuse")
    if resource_type == "model-checkpoint":
        gates.append("model-runtime-and-device-review")
        gates.append("model-license-and-attribution-review")
    elif resource_type == "model-collection":
        gates.append("per-model-license-and-compute-review")
    elif resource_type == "model-hub":
        gates.append("per-item-license-and-provider-review")
    if site.get("sourceLicenseTag") in {"other", "unknown"}:
        gates.append("unverified-hub-license-tag")
    if site.get("safetyRisk") == "reduced-refusal":
        gates.append("reduced-refusal-public-safety-review")
    # Rewriting output is never guaranteed to retain names, dates, numbers,
    # quotations, formatting or source language. Label these constraints
    # independently from a licence or hosted compute review.
    if resource_type == "model-checkpoint" and "text-rewriting" in set(site.get("tags") or []):
        gates.append("factual-and-format-preservation-review")
        gates.append("source-and-target-language-review")
        gates.append("human-editor-approval-before-publication")
    if resource_type == "marketing-automation-service":
        gates.append("platform-anti-spam-and-account-policy-review")
        gates.append("manual-publication-and-consent-required")
    if resource_type in {"animation-reference-library", "film-stills-library"}:
        gates.append("copyrighted-reference-no-production-reuse")
    if resource_type == "costume-history-atlas":
        gates.append("verify-per-image-public-domain-or-cc0-provenance")
        gates.append("creator-submitted-design-rights-review")
    if resource_type == "3d-pose-reference-tool":
        gates.append("pose-export-format-and-rights-review")
    if resource_type == "3d-asset-dataset":
        gates.extend([
            "asset-level-license-and-attribution-review",
            "3d-mesh-texture-and-target-engine-review",
            "individual-download-hash-and-file-safety-review",
        ])
    if resource_type == "codebase-prompt-generator":
        gates.extend([
            "public-prompt-visibility-and-sensitive-input-review",
            "generated-prompt-accuracy-and-source-code-review",
            "untrusted-repository-and-website-prompt-injection-review",
            "upstream-code-and-website-reuse-rights-review",
        ])
    if resource_type == "prompt-template-library":
        gates.append("prompt-creator-rights-and-instruction-safety-review")
    if resource_type == "ai-media-generator":
        gates.append("generated-output-licence-and-subject-consent-review")
        gates.append("human-approved-inference-and-compute-costs")
    if reuse == "hosted-service":
        gates.append("hosted-terms-privacy-and-cost-review")
    elif reuse in {"licensed-material", "license-per-item", "reference-only"}:
        gates.append("third-party-reuse-rights-review")
    return gates


def recommend_websites(qtokens, domains, limit=5, include_unmatched=False):
    """Rank non-GitHub references separately from code integration candidates.

    This remains advisory: no site can be auto-dispatched as a dependency.
    Repository-specific hard filters have no meaning for inspiration pages.
    """
    data = json.loads(WEBSITES.read_text(encoding="utf-8"))
    ranked = []
    for site in data["websites"]:
        site_domains = set(site["domains"])
        matched_domains = sorted(site_domains & domains)
        baseline_domains = sorted(set(site.get("portfolioBaselineDomains", [])) & domains)
        matched_tags = sorted(qtokens & set(site["tags"]))
        matched_text = sorted((qtokens & tokens(
            site["name"] + " " + " ".join(site["bestFor"])
        )) - WEBSITE_MATCH_STOPWORDS)
        if not include_unmatched and not matched_domains and not matched_tags and not matched_text:
            continue
        score = (12 * len(matched_domains) + 10 * len(matched_tags)
                 + 4 * len(matched_text))
        ranked.append((score, site, matched_domains, matched_tags, matched_text, baseline_domains))
    ranked.sort(key=lambda row: (-row[0], row[1]["name"].lower()))
    return [
        {
            "id": site["id"], "name": site["name"], "url": site["url"],
            "type": site["type"], "access": site["access"],
            "reuse": site["reuse"], "caution": site["caution"],
            "bestFor": site["bestFor"],
            "portfolioRequiredSignals": site.get("portfolioRequiredSignals", []),
            **({"supportedLanguages": site["supportedLanguages"]}
               if site.get("supportedLanguages") else {}),
            "reviewGates": website_review_gates(site),
            **({"sourceLicenseTag": site["sourceLicenseTag"]}
               if site.get("sourceLicenseTag") else {}),
            **({"upstreamModel": site["upstreamModel"]}
               if site.get("upstreamModel") else {}),
            **({"safetyRisk": site["safetyRisk"]}
               if site.get("safetyRisk") else {}),
            # A verified documentation endpoint is reference metadata only;
            # the recommender never connects or authorizes paid MCP tools.
            **({"mcpEndpoint": site["mcpEndpoint"]} if site.get("mcpEndpoint") else {}),
            "selectionScore": score,
            "why": {"domains": domain_hits, "tags": tag_hits, "terms": text_hits,
                    "portfolioBaselineDomains": baseline_hits},
            "integrationEligible": False,
        }
        for score, site, domain_hits, tag_hits, text_hits, baseline_hits in (ranked if limit is None else ranked[:limit])
    ]

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

@lru_cache(maxsize=8192)
def trend_adjustment(repo_name):
    if not HISTORY.exists(): return 0.0, None
    try:
        pts=json.loads(HISTORY.read_text()).get("repositories",{}).get(repo_name,[])
    except (OSError,json.JSONDecodeError): return 0.0, None
    if len(pts)<2: return 0.0, None
    recent=pts[-5:] if len(pts)>=5 else pts
    first,last=recent[0],recent[-1]
    try:
        days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
    except (ValueError,TypeError,KeyError):
        days=max(1,7*(len(recent)-1))
    def delta(k):
        a,b=first.get(k),last.get(k)
        return b-a if isinstance(a,(int,float)) and isinstance(b,(int,float)) else None
    hd,sd,fd=delta("health"),delta("stars"),delta("forks")
    stars_week=(sd*7/days) if sd is not None else 0.0
    forks_week=(fd*7/days) if fd is not None else 0.0
    momentum=max(-3.0,min(3.0, stars_week/50.0)) + max(-1.0,min(1.0, forks_week/10.0))
    if hd is not None:
        momentum += max(-4.0,min(4.0,hd/2.5))
    momentum=round(max(-6.0,min(6.0,momentum)),3)
    reason="declining" if momentum<=-2 else "improving" if momentum>=2 else "growing" if momentum>0.5 else "stable"
    return momentum, reason

def guidance_weight(r):
    source = r.get("guidanceSource")
    if source == "inferred" and r.get("tier") == "specialized":
        return SPECIALIZED_INFERRED_WEIGHT
    return GUIDANCE_WEIGHT.get(source, 1.0)


def ranking_review_gates(r):
    """Rank everything, but expose the reasons an entry requires review."""
    gates = []
    gh = r.get("github")
    if isinstance(gh, dict):
        if gh.get("archived"):
            gates.append("archived")
        if gh.get("disabled"):
            gates.append("disabled")
    return gates


def metadata_review_gates(r):
    """Report factual gaps without guessing about hosting or licensing."""
    gates = []
    gh = r.get("github")
    if not isinstance(gh, dict) or not gh:
        gates.append("github-metadata-unavailable")
    elif str(gh.get("license") or "").strip().upper() in {"", "NOASSERTION"}:
        gates.append("license-unresolved")
    if not isinstance(r.get("selfHosted"), bool):
        gates.append("self-hosting-unverified")
    return gates


def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps):
    caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
    if excluded_caps and caps & excluded_caps:
        return None
    rtoks = tokens(" ".join([
        r.get("repo", ""), r.get("category", ""), r.get("domain", ""),
        " ".join(caps)
    ]))
    # Exact task tokens from manually reviewed upstream README blobs improve
    # only advisory relevance. They do not elevate tier or integration trust.
    rtoks |= tokens(" ".join(reviewed_readme_task_terms(r)))
    lexical = len(qtokens & rtoks) / max(1, len(qtokens))
    cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
    domain_evidence = advisory_domain_evidence(r)
    domain_match = 1.0 if requested_domains and requested_domains & domain_evidence.keys() else 0.0
    quality = max(0.0, min(1.0, r.get("score", 0) / 10.0))
    tier = TIER_BONUS.get(r.get("tier"), 0.0)
    best_for = tokens(" ".join(r.get("bestFor", [])))
    best_match = len(qtokens & best_for) / max(1, len(qtokens)) if best_for else 0.0
    guidance = guidance_weight(r)
    s = 34*cap_match + 22*domain_match + 18*lexical + 12*guidance*best_match + 10*quality + 4*max(0.0, tier)
    if not required_caps:
        s += 12*lexical
    avoid = tokens(" ".join(r.get("avoidWhen", [])))
    if qtokens & avoid:
        s -= 18 * guidance
    activity, _ = activity_adjustment(r)
    s += activity
    health = health_score(r)
    if health["score"] is not None:
        s += 6.0 * (health["score"] / 100.0)
    trend, _ = trend_adjustment(r["repo"])
    s += trend
    return round(s, 3)

def explain_repo(r, qtokens, domains, required_caps):
    caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
    best = tokens(" ".join(r.get("bestFor", [])))
    reasons = []
    matched_domains = sorted(domains & advisory_domain_evidence(r).keys())
    if matched_domains:
        if r.get("domain") in matched_domains:
            reasons.append("domain:" + r["domain"])
        else:
            reasons.append("advisory-domain:" + ",".join(matched_domains[:2]))
    matched_caps = sorted(required_caps & caps)
    if matched_caps:
        reasons.append("capabilities:" + ",".join(matched_caps))
    matched_terms = sorted(qtokens & (tokens(r.get("repo", "")) | caps | best))
    if matched_terms:
        reasons.append("terms:" + ",".join(matched_terms[:6]))
    if r.get("tier") in {"core", "recommended"}:
        reasons.append("tier:" + r["tier"])
    if r.get("guidanceSource") == "inferred":
        reasons.append("guidance:inferred")
    _, activity_reason = activity_adjustment(r)
    if activity_reason:
        reasons.append("activity:" + activity_reason)
    _, trend_reason = trend_adjustment(r["repo"])
    if trend_reason and trend_reason != "stable": reasons.append("trend:" + trend_reason)
    return reasons[:4]

# Generic words can occur in unrelated stacks. They cannot establish a fit
# on their own (e.g. "AI video" must not select a coding-agent stack).
STACK_GENERIC_TERMS = frozenset(
    "ai agent agents app apps tool tools dev software production project "
    "projects system systems workflow workflows modern high quality using with "
    "and for research validation".split()
)


def choose_stack(stacks, qtokens, domains, allowed_names=None):
    best, best_score = None, -1
    for st in stacks:
        if allowed_names is not None and not all(name in allowed_names for name in st.get("repos", [])):
            continue
        domain_match = st.get("domain") in domains
        if domains and st.get("domain") and not domain_match:
            continue
        title_terms = tokens(st.get("name", ""))
        goal_terms = tokens(st.get("goal", ""))
        significant = (qtokens & (title_terms | goal_terms)) - STACK_GENERIC_TERMS
        # Require a strong named match, or two independent task-specific
        # signals. Notes cannot be evidence: they often describe caveats,
        # alternatives or unrelated technologies.
        title_words = norm(st.get("name", "")).split()
        anchor = next((word for word in title_words if word not in STACK_GENERIC_TERMS), None)
        anchored = anchor is not None and anchor in qtokens
        if not anchored and len(significant) < 2:
            continue
        if not domain_match and st.get("domain") and len(significant) < 3:
            continue
        score = 4 * len(significant) + (3 if domain_match else 0) + (2 if anchored else 0)
        if score > best_score:
            best_score, best = score, st
    return best


def infer_alternatives(source, repos, top=3, allowed_names=None):
    candidates = []
    for candidate in repos:
        if candidate["repo"] == source["repo"]:
            continue
        if allowed_names is not None and candidate["repo"] not in allowed_names:
            continue
        result = replacement_score(source, candidate)
        if result is None:
            continue
        fit, candidate_health = result
        candidates.append((
            fit,
            candidate_health.get("score") or 0,
            candidate.get("score") or 0,
            candidate["repo"],
        ))
    candidates.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3].lower()))
    return [repo for _, _, _, repo in candidates[:top]]


def infer_complements(source, stacks, repo_by_name, top=4, allowed_names=None):
    seen = set()
    complements = []
    for stack in stacks:
        members = stack.get("repos", [])
        if source["repo"] not in members:
            continue
        for name in members:
            if name == source["repo"] or name in seen:
                continue
            if allowed_names is not None and name not in allowed_names:
                continue
            candidate = repo_by_name.get(name)
            if not candidate:
                continue
            health = health_score(candidate)
            if health.get("status") in {"inactive", "weak"}:
                continue
            seen.add(name)
            complements.append(name)
            if len(complements) >= top:
                return complements
    return complements


def resolve_relations(source, repos, stacks, repo_by_name, allowed_names=None):
    # Curated links are suggestions, not exemptions from the user's constraints.
    def usable(names):
        seen = {source["repo"]}
        result = []
        for name in names:
            if name in seen or (allowed_names is not None and name not in allowed_names):
                continue
            seen.add(name)
            result.append(name)
        return result

    explicit_alternatives = usable(source.get("alternatives", []))
    explicit_complements = usable(source.get("complements", []))
    alternatives = explicit_alternatives or infer_alternatives(source, repos, allowed_names=allowed_names)
    complements = explicit_complements or infer_complements(source, stacks, repo_by_name, allowed_names=allowed_names)
    return {
        "alternatives": alternatives,
        "alternativesSource": "curated" if explicit_alternatives else ("inferred" if alternatives else "none"),
        "complements": complements,
        "complementsSource": "curated" if explicit_complements else ("inferred" if complements else "none"),
    }

def main():
    ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
    ap.add_argument("query", help="Natural-language task/query")
    ap.add_argument("--cap", action="append", default=[], help="Desired capability; repeatable")
    ap.add_argument("--require-all-caps", action="store_true", help="Reject repositories missing any --cap capability")
    ap.add_argument("--exclude-cap", action="append", default=[], help="Excluded capability; repeatable")
    ap.add_argument("--domain", action="append", default=[], help="Force a domain; repeatable")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=None, help="Optional score threshold; without it every catalog entry is rankable")
    ap.add_argument("--platform", action="append", default=[], help="Required platform; repeatable")
    ap.add_argument("--language", action="append", default=[], help="Required language; repeatable")
    ap.add_argument("--self-hosted", action="store_true", help="Require self-hosted/local-friendly repositories")
    archived_filter = ap.add_mutually_exclusive_group()
    archived_filter.add_argument("--include-archived", action="store_true", dest="include_archived",
                                 default=True, help="Include archived/disabled entries (default)")
    archived_filter.add_argument("--exclude-archived", action="store_false", dest="include_archived",
                                 help="Opt in to excluding archived/disabled entries")
    indexed_filter = ap.add_mutually_exclusive_group()
    indexed_filter.add_argument("--include-indexed", "--include-audit", action="store_true",
                                dest="include_indexed", default=True,
                                help="Include indexed references (default, including old --include-audit alias)")
    indexed_filter.add_argument("--exclude-indexed", "--exclude-audit", action="store_false",
                                dest="include_indexed",
                                help="Opt in to omitting indexed references; --exclude-audit is a legacy alias")
    ap.add_argument("--max-resource", choices=["low","medium","high"], default="high")
    ap.add_argument("--max-complexity", choices=["low","medium","high"], default="high")
    ap.add_argument("--websites", action="store_true", help="Include matching external web references separately from repositories")
    ap.add_argument("--rank-all-websites", action="store_true",
                    help="With --websites, rank unrelated sites with zero relevance too")
    ap.add_argument("--skills", action="store_true", help="Find curated agent-skill sources from Skill Issue (review-only)")
    ap.add_argument("--top-skills", type=int, default=3, help="Max matching agent-skill sources when --skills is active")
    ap.add_argument("--top-websites", type=int, default=5, help="Max external website references when --websites is active")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    if args.top < 1:
        ap.error("--top must be >= 1")
    if args.top_websites < 1:
        ap.error("--top-websites must be >= 1")
    if args.top_skills < 1 or args.top_skills > 20:
        ap.error("--top-skills must be between 1 and 20")
    if args.min_score is not None and args.min_score < 0:
        ap.error("--min-score must be >= 0")

    repos, stacks = load()
    repo_by_name = {r["repo"]: r for r in repos}
    qtokens = tokens(args.query)
    domains = set(args.domain) or infer_domains(qtokens)
    required_caps, excluded_caps = set(args.cap), set(args.exclude_cap)
    ranked = []
    relation_names = set()  # Advisory links may reference indexed sources; installation remains independently gated.
    filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "indexed":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}

    for r in repos:
        if r.get("tier") == "indexed" and not args.include_indexed:
            filtered["indexed"] += 1
            continue
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
        # Eligibility for related tools/stacks must obey the same hard constraints.
        if not (isinstance(gh, dict) and (gh.get("archived") or gh.get("disabled"))):
            relation_names.add(r["repo"])
        if args.min_score is not None and s < args.min_score:
            filtered["minScore"] += 1; continue
        ranked.append((s, r))

    ranked.sort(key=lambda x: (-x[0], -x[1].get("score", 0), x[1]["repo"].lower()))
    top = []
    for s, r in ranked[:args.top]:
        relations = resolve_relations(r, repos, stacks, repo_by_name, relation_names)
        top.append({
            "repo": r["repo"], "selectionScore": s, "qualityScore": r.get("score"),
            "tier": r.get("tier"), "domain": r.get("domain"),
            "advisoryDomains": advisory_domain_evidence(r),
            "domainReviewGates": (
                ["inferred-domain-needs-confirmation"]
                if r.get("domain") in {"other", "unknown", ""}
                and domains & advisory_domain_evidence(r).keys() else []
            ),
            "capabilities": r.get("capabilities", []), "bestFor": r.get("bestFor", []),
            "avoidWhen": r.get("avoidWhen", []),
            "alternatives": relations["alternatives"], "alternativesSource": relations["alternativesSource"],
            "complements": relations["complements"], "complementsSource": relations["complementsSource"],
            "languages": r.get("languages", []),
            "platforms": r.get("platforms", []), "selfHosted": r.get("selfHosted"),
            "resourceLevel": r.get("resourceLevel"), "integrationComplexity": r.get("integrationComplexity"),
            "guidanceSource": r.get("guidanceSource", "curated"),
            "why": explain_repo(r, qtokens, domains, required_caps),
            "health": health_score(r),
            "rankingReviewGates": ranking_review_gates(r),
            "metadataReviewGates": metadata_review_gates(r),
            "availableForDiscovery": True,
            "automaticIntegrationApproved": False,
            "reviewRequired": bool(
                ranking_review_gates(r) or metadata_review_gates(r) or
                (r.get("domain") in {"other", "unknown", ""}
                 and domains & advisory_domain_evidence(r).keys())
            ),
        })

    result = {
        "query": args.query, "inferredDomains": sorted(domains),
        "requiredCapabilities": sorted(required_caps), "recommendations": top,
        "constraints": {"platforms":args.platform, "languages":args.language, "selfHosted":args.self_hosted,
                        "maxResource":args.max_resource, "maxComplexity":args.max_complexity,
                        "requireAllCapabilities":args.require_all_caps, "minScore":args.min_score,
                        "includeArchived":args.include_archived, "includeIndexed":args.include_indexed, "includeAudit":args.include_indexed},
        "diagnostics": {
            "catalogSize": len(repos), "eligible": len(ranked), "returned": len(top),
            "filtered": filtered,
            "metadata": {
                "unverifiedSelfHosting": sum(bool("self-hosting-unverified" in metadata_review_gates(r)) for _, r in ranked),
                "unresolvedLicenses": sum(bool("license-unresolved" in metadata_review_gates(r)) for _, r in ranked),
                "reviewRequired": sum(bool(
                    ranking_review_gates(r) or metadata_review_gates(r) or
                    (r.get("domain") in {"other", "unknown", ""}
                     and domains & advisory_domain_evidence(r).keys())
                ) for _, r in ranked),
            },
        },
        "recommendedStack": choose_stack(stacks, qtokens, domains, relation_names),
    }
    if args.websites:
        result["websiteRecommendations"] = recommend_websites(
            qtokens, domains, args.top_websites, include_unmatched=args.rank_all_websites
        )
        result["websiteDiagnostics"] = {
            "catalogSize": len(json.loads(WEBSITES.read_text(encoding="utf-8"))["websites"]),
            "rankAll": args.rank_all_websites,
            "returned": len(result["websiteRecommendations"]),
        }
    if args.skills:
        result["skillDiscovery"] = {
            "directory": SKILL_ISSUE_URL, "priority": "high",
            "reviewRequired": True, "automaticInstallation": False,
            "recommendations": recommend_skills(
                word_set(args.query), domains,
                language=args.language[0] if args.language else "",
                limit=args.top_skills,
            ),
        }
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Query: {args.query}")
        if domains: print("Domains:", ", ".join(sorted(domains)))
        for i, item in enumerate(top, 1):
            print(f"{i}. {item['repo']} | selection={item['selectionScore']:.1f} | quality={item['qualityScore']}/10 | {item['tier']}")
            if item["why"]: print("   why:", "; ".join(item["why"]))
            all_gates = (item["rankingReviewGates"] + item["metadataReviewGates"]
                         + item["domainReviewGates"])
            if all_gates:
                print("   review required:", ", ".join(all_gates))
            if item["bestFor"]: print("   bestFor:", "; ".join(item["bestFor"][:3]))
            if item["complements"]: print("   complements:", ", ".join(item["complements"][:4]))
        if result["recommendedStack"]:
            st = result["recommendedStack"]
            print(f"\nSuggested stack: {st['name']}")
            print(" + ".join(st.get("repos", [])))
        if args.skills:
            print("\nAgent skills (Skill Issue; review sources and licenses before use):")
            print(" - Directory:", SKILL_ISSUE_URL)
            for skill in result["skillDiscovery"]["recommendations"]:
                print(" - " + skill["name"] + " | " + skill["url"] + " | review required")
        if args.websites and result["websiteRecommendations"]:
            print("\nWeb resources (references only; not GitHub repositories or automatic integrations):")
            for site in result["websiteRecommendations"]:
                print(f" - {site['name']} | {site['url']} | {site['type']} | {site['access']}")
                print("   use:", "; ".join(site["bestFor"][:2]))
                print("   reuse:", site["reuse"])
        print(f"\nEligible: {len(ranked)}/{len(repos)} | returned: {len(top)}")

if __name__ == "__main__":
    main()
