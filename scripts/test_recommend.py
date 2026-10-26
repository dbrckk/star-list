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

# External sites are advisory references, never installable GitHub repositories.
websites_catalog = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))
sites = websites_catalog["websites"]
# Curated website references are additive; new resources must not break
# the existing GitHub recommendation contract or require exact-size snapshots.
assert len(sites) >= 11
assert any(site["id"] == "skill-issue" and site["type"] == "agent-skills-directory" for site in sites)
assert len({site["id"] for site in sites}) == len(sites)
assert len({site["url"].lower().rstrip("/") for site in sites}) == len(sites)
assert all(site["url"].startswith("https://") for site in sites)
assert all(site["reuse"] for site in sites)
assert next(site for site in sites if site["id"] == "recent-design")["originalUrl"] == "https://godly.website/"
baseline_web_query = run("3d scroll animation website", "--top", "4")
with_web_query = run("3d scroll animation website", "--top", "4", "--websites", "--top-websites", "30")
assert baseline_web_query["recommendations"] == with_web_query["recommendations"]
assert "websiteRecommendations" not in baseline_web_query
assert "skillDiscovery" not in baseline_web_query
with_skills_query = run("mobile ui design", "--top", "4", "--skills")
without_skills_query = run("mobile ui design", "--top", "4")
assert with_skills_query["recommendations"] == without_skills_query["recommendations"]
assert with_skills_query["skillDiscovery"]["directory"] == "https://skill-issue.in/"
assert with_skills_query["skillDiscovery"]["automaticInstallation"] is False
assert all(s["reviewRequired"] and not s["integrationEligible"] and s["installCommand"] is None
           for s in with_skills_query["skillDiscovery"]["recommendations"])
assert all(s["skillFileUrl"].startswith(s["url"] + "/blob/" + s["sourceCommit"] + "/")
           and len(s["sourceCommit"]) == 40
           and (s["sourcePath"] == "SKILL.md" or s["sourcePath"].endswith("/SKILL.md"))
           for s in with_skills_query["skillDiscovery"]["recommendations"])
# Newly verified upstream files must be selectable without changing the normal
# GitHub recommendation contract, and no skill can be silently installed.
from agent_skill_discovery import recommend_skills, word_set
roblox_skills = recommend_skills(word_set("roblox luau studio"), {"game_dev"}, limit=20)
assert any(s["id"] == "roblox-luau-development" and s["sourcePath"] == "SKILL.md"
           and s["skillFileUrl"].endswith("/SKILL.md") for s in roblox_skills)
compose_skills = recommend_skills(word_set("compose jetpack"), {"mobile"}, language="Kotlin", limit=20)
assert any(s["id"] == "android-compose-performance" for s in compose_skills)
assert not any(s["id"] == "android-compose-performance" for s in
               recommend_skills(word_set("android mobile"), {"mobile"}, language="Kotlin", limit=20))
assert any(s["id"] == "android-play-policy-insights" for s in
           recommend_skills(word_set("android play policy"), {"mobile"}, language="Kotlin", limit=20))
assert all(s["reviewRequired"] and s["integrationEligible"] is False
           and s["installCommand"] is None
           for s in roblox_skills + compose_skills)
assert any(s["id"] == "react-native-architecture" for s in
           run("react native mobile", "--skills", "--language", "typescript")
           ["skillDiscovery"]["recommendations"])
assert {row["id"] for row in with_web_query["websiteRecommendations"]} >= {"scrolltide", "threejs", "shadertoy"}
assert all(not row["integrationEligible"] for row in with_web_query["websiteRecommendations"])
assert all(row["url"].startswith("https://") for row in with_web_query["websiteRecommendations"])
assert run("xauusd trading execution", "--websites")["websiteRecommendations"] == []
all_sites = run("xauusd trading execution", "--websites", "--rank-all-websites", "--top-websites", "200")
assert len(all_sites["websiteRecommendations"]) == len(sites)
assert all_sites["websiteDiagnostics"]["catalogSize"] == len(sites)
assert all_sites["websiteDiagnostics"]["rankAll"] is True
assert any(x["selectionScore"] == 0 for x in all_sites["websiteRecommendations"])
assert all(x["integrationEligible"] is False for x in all_sites["websiteRecommendations"])
assert any(row["id"] == "60fps" for row in run("mobile ui motion animation", "--websites")["websiteRecommendations"])

# SoPilot is an opt-in Chrome/X/SEO marketing service, not a general-purpose
# AI coder, video renderer, retail discount data feed or installable library.
sopilot_id = "sopilot"
sopilot = next(x for x in sites if x["id"] == sopilot_id)
assert sum(x["id"] == sopilot_id for x in sites) == 1
assert sopilot["url"] == "https://sopilot.net/"
assert sopilot["type"] == "marketing-automation-service"
assert sopilot["reuse"] == "hosted-service"
assert sopilot["domains"] == ["marketing"]
assert sopilot["portfolioRequiredSignals"]
assert not sopilot.get("portfolioBaselineDomains")
assert sopilot_id in {x["id"] for x in run(
    "social media marketing SEO campaign", "--websites", "--top-websites", "40"
)["websiteRecommendations"]}
from recommend import infer_domains
assert "marketing" in infer_domains({"seo", "campaign"})
assert "marketing" not in infer_domains({"promo", "discount", "food", "game", "video"})
from portfolio_daily import website_references_for_project
# Six screenshot-supplied sources are independent, specialist research entries.
animation_ids = {
    "sakugabooru", "shot-cafe", "posemy-art",
    "niwatoliver-costume-atlas", "youmind-video-prompts", "carat-ai-media",
}
assert animation_ids <= {site["id"] for site in sites}
assert all(sum(site["id"] == identity for site in sites) == 1 for identity in animation_ids)
assert next(site for site in sites if site["id"] == "sakugabooru")["originalUrl"] == (
    "https://sakugabooru.com/"
)
assert next(site for site in sites if site["id"] == "youmind-video-prompts")["url"] == (
    "https://youmind.com/prompts/video/anime"
)
assert next(site for site in sites if site["id"] == "niwatoliver-costume-atlas")["url"] == (
    "https://costume.tools.niwatoliver.dev/"
)
for site in sites:
    if site["id"] in animation_ids:
        assert site.get("portfolioRequiredSignals") and not site.get("portfolioBaselineDomains")
        assert site["reuse"] in {"reference-only", "license-per-item", "hosted-service"}
animation_queries = (
    ({"name": "anime-motion-studio", "description": "Anime animation choreography",
      "topics": ["sakuga"]},
     {"domains": ["game_dev", "graphics"]}, {"sakugabooru"}),
    ({"name": "cinematic-storyboard", "description": "Film camera framing and cinematic lighting",
      "topics": ["storyboard"]},
     {"domains": ["game_dev", "ai_media"]}, {"shot-cafe"}),
    ({"name": "3d-character-posing", "description": "3d character mannequin poses",
      "topics": ["rigging"]},
     {"domains": ["graphics", "game_dev"]}, {"posemy-art"}),
    ({"name": "historical-costume-design", "description": "Historical wardrobe dress fashion",
      "topics": ["costume"]},
     {"domains": ["graphics", "game_dev"]}, {"niwatoliver-costume-atlas"}),
    ({"name": "anime-video-generation", "description": "Animated anime video generation",
      "topics": ["video"]},
     {"domains": ["ai_media"]}, {"youmind-video-prompts", "carat-ai-media"}),
)
for project, project_profile, expected in animation_queries:
    audit = {}
    matched = website_references_for_project(project, project_profile, assessment=audit)
    refs = {site["id"]: site for site in matched}
    assert expected <= refs.keys(), (project, refs)
    for identity in expected:
        assert refs[identity]["integrationEligible"] is False
        assert refs[identity]["reviewGates"]
        assert audit[identity]["decision"] == "matched"
        assert audit[identity]["integrationEligible"] is False
        assert audit[identity]["reviewGates"] == refs[identity]["reviewGates"]
assert "copyrighted-reference-no-production-reuse" in next(
    row for row in website_references_for_project(
        {"name": "anime-motion", "description": "sakuga anime animated animation",
         "topics": ["sakuga"]}, {"domains": ["graphics"]}
    ) if row["id"] == "sakugabooru"
)["reviewGates"]
assert "verify-per-image-public-domain-or-cc0-provenance" in next(
    row for row in website_references_for_project(
        {"name": "costume-history", "description": "historical fashion dress",
         "topics": ["costume"]}, {"domains": ["graphics"]}
    ) if row["id"] == "niwatoliver-costume-atlas"
)["reviewGates"]
assert "human-approved-inference-and-compute-costs" in next(
    row for row in website_references_for_project(
        {"name": "anime-video", "description": "animated video generation",
         "topics": ["video"]}, {"domains": ["ai_media"]}
    ) if row["id"] == "carat-ai-media"
)["reviewGates"]
for unrelated_project, domains in (
    ({"name": "Jumpy", "description": None, "topics": []}, ["game_dev"]),
    ({"name": "asset-ledger", "description": "finance and trading",
      "topics": []}, []),
    ({"name": "TTS", "description": "Text to speech synthesis",
      "topics": []}, ["ai_media"]),
):
    rejected = website_references_for_project(
        unrelated_project, {"domains": domains, "terms": set()}
    )
    assert not animation_ids & {item["id"] for item in rejected}, unrelated_project
from validate_websites import check_websites as validate_visual_websites
import copy as animation_copy
animation_schema = json.loads((ROOT / "schemas/websites.schema.json").read_text(encoding="utf-8"))
unsafe_visual = animation_copy.deepcopy(websites_catalog)
copyrighted_site = next(x for x in unsafe_visual["websites"] if x["id"] == "sakugabooru")
copyrighted_site["reuse"] = "open-source-upstream"
assert validate_visual_websites(unsafe_visual, animation_schema)
copyrighted_site["reuse"] = "reference-only"
copyrighted_site["portfolioBaselineDomains"] = ["game_dev"]
assert validate_visual_websites(unsafe_visual, animation_schema)
copyrighted_site.pop("portfolioBaselineDomains")
hosted_generation = next(x for x in unsafe_visual["websites"] if x["id"] == "carat-ai-media")
hosted_generation["reuse"] = "open-source-upstream"
assert validate_visual_websites(unsafe_visual, animation_schema)
marketing_target = {
    "name": "social-campaign-studio", "description": None, "topics": ["seo", "marketing"]
}
marketing_matches = website_references_for_project(marketing_target, {"domains": [], "terms": set()})
sopilot_match = next(x for x in marketing_matches if x["id"] == sopilot_id)
assert sopilot_match["integrationEligible"] is False
assert {"platform-anti-spam-and-account-policy-review",
        "manual-publication-and-consent-required",
        "hosted-terms-privacy-and-cost-review"} <= set(sopilot_match["reviewGates"])
for unrelated in (
    {"name": "Promo-alimentaire", "description": "Retail discounts and coupons", "topics": []},
    {"name": "Jumpy", "description": "Godot jumping game", "topics": []},
    {"name": "monteur-video", "description": "Automatic HD video montage", "topics": []},
):
    assert sopilot_id not in {
        x["id"] for x in website_references_for_project(
            unrelated, {"domains": [], "terms": set()}
        )
    }, unrelated
sopilot_decisions = {}
website_references_for_project(
    marketing_target, {"domains": [], "terms": set()}, assessment=sopilot_decisions
)
assert sopilot_decisions[sopilot_id]["decision"] == "matched"
assert sopilot_decisions[sopilot_id]["integrationEligible"] is False
assert "manual-publication-and-consent-required" in sopilot_decisions[sopilot_id]["reviewGates"]
retail_decisions = {}
website_references_for_project(
    {"name": "Promo-alimentaire", "description": "Discount coupons", "topics": []},
    {"domains": [], "terms": set()}, assessment=retail_decisions
)
assert retail_decisions[sopilot_id]["decision"] == "not-relevant"

# Humanizer is a 12B English/Chinese draft *completion* checkpoint, not a
# broadly compatible French-language chat agent or free hosted inference API.
humanizer_id = "jialinyyzz-humanizer-12b"
humanizer_model = next(x for x in sites if x["id"] == humanizer_id)
assert sum(x["id"] == humanizer_id for x in sites) == 1
assert humanizer_model["url"] == "https://huggingface.co/jialinyyzz/humanizer"
assert humanizer_model["type"] == "model-checkpoint"
assert humanizer_model["sourceLicenseTag"] == "apache-2.0"
assert humanizer_model["upstreamModel"] == "google/gemma-4-12B"
assert set(humanizer_model["supportedLanguages"]) == {"en", "zh"}
assert not humanizer_model.get("portfolioBaselineDomains")
assert humanizer_model["portfolioRequiredSignals"]
assert "writing" in infer_domains({"writing", "editorial"})
assert "writing" not in infer_domains({"video", "game", "code", "image", "text"})
writing_project = {
    "name": "newsletter-copywriting", "description": None, "topics": ["rewriting"]
}
writing_matches = website_references_for_project(
    writing_project, {"domains": [], "terms": set()}
)
humanizer_advice = next(x for x in writing_matches if x["id"] == humanizer_id)
assert humanizer_advice["integrationEligible"] is False
assert humanizer_advice["supportedLanguages"] == ["en", "zh"]
assert {"model-runtime-and-device-review",
        "model-license-and-attribution-review",
        "factual-and-format-preservation-review",
        "source-and-target-language-review",
        "human-editor-approval-before-publication"} <= set(humanizer_advice["reviewGates"])
assert humanizer_id in {x["id"] for x in run(
    "rewrite newsletter copywriting", "--websites", "--top-websites", "50"
)["websiteRecommendations"]}
writing_decisions = {}
website_references_for_project(
    writing_project, {"domains": [], "terms": set()}, assessment=writing_decisions
)
assert writing_decisions[humanizer_id]["decision"] == "matched"
assert "factual-and-format-preservation-review" in writing_decisions[humanizer_id]["reviewGates"]
for nonwriting in (
    {"name": "monteur-video", "description": "Automatic video editing", "topics": []},
    {"name": "TTS", "description": "Multilingual speech synthesis", "topics": []},
    {"name": "Jumpy", "description": "Godot game", "topics": []},
    {"name": "ai-agent", "description": "Autonomous coding agent", "topics": []},
    {"name": "Promo-alimentaire", "description": "Retail discount coupons", "topics": []},
):
    advice = website_references_for_project(
        nonwriting, {"domains": ["ai_media"] if nonwriting["name"] == "TTS" else [], "terms": set()}
    )
    assert humanizer_id not in {x["id"] for x in advice}, nonwriting
rejected_writing = {}
website_references_for_project(
    {"name": "Jumpy", "description": "Godot game", "topics": []},
    {"domains": ["game_dev"]}, assessment=rejected_writing
)
assert rejected_writing[humanizer_id]["decision"] == "not-relevant"
assert rejected_writing[humanizer_id]["integrationEligible"] is False

# Real regression: TTS was being shown game-art-style due to generic words
# such as "and" in both project metadata and curator descriptions.
tts_labels = "TTS a deep learning toolkit for Text-to-Speech battle-tested in research and production"
from recommend import recommend_websites, tokens
tts_sites = recommend_websites(tokens(tts_labels), {"ai_media"}, limit=30)
assert not any(s["id"] == "game-art-style" for s in tts_sites)
from portfolio_daily import website_references_for_project
tts_portfolio_sites = website_references_for_project(
    {"name": "TTS", "description": tts_labels, "topics": []},
    {"domains": ["ai_media"]},
)
assert not any(s["id"] == "game-art-style" for s in tts_portfolio_sites)
# Quantized checkpoints must be discoverable for visual projects, but a
# generic AI/media project (including speech) must not get an image generator.
gguf_id = "atomicchat-flux3-image-klein-gguf"
assert sum(x["id"] == gguf_id for x in sites) == 1, "Repeated URLs must not create duplicate entries"
gguf = next(x for x in sites if x["id"] == gguf_id)
assert gguf["sourceLicenseTag"] == "other"
assert gguf["upstreamModel"] == "black-forest-labs/flux-3-image-klein"
assert gguf["type"] == "model-checkpoint"
assert gguf["reuse"] == "licensed-material"
assert not gguf.get("portfolioBaselineDomains")
image_project = {"name": "asset-forge", "description": "Image-to-image sprite texture assets",
                 "topics": ["image-editing", "gguf"]}
image_profile = {"domains": ["ai_media", "graphics"]}
image_references = website_references_for_project(image_project, image_profile)
gguf_result = next(x for x in image_references if x["id"] == gguf_id)
assert gguf_result["integrationEligible"] is False
assert gguf_result["sourceLicenseTag"] == "other"
assert {"model-runtime-and-device-review", "model-license-and-attribution-review",
        "unverified-hub-license-tag"} <= set(gguf_result["reviewGates"])
assert gguf_result["upstreamModel"] == gguf["upstreamModel"]
assert gguf_id in {x["id"] for x in recommend_websites(
    tokens("flux gguf image generation editing"), {"ai_media"}, limit=None
)}
quiet_game = website_references_for_project(
    {"name": "Jumpy", "description": None, "topics": []}, {"domains": ["game_dev"]}
)
assert gguf_id not in {x["id"] for x in quiet_game}
assert gguf_id not in {x["id"] for x in tts_portfolio_sites}
assert gguf_id not in {x["id"] for x in website_references_for_project(
    {"name": "speech-service", "description": "Speech synthesis and podcasts", "topics": []},
    {"domains": ["ai_media"]}
)}
# Metadata decisions must cover the model even when it is rejected.
image_audit = {}
website_references_for_project(image_project, image_profile, assessment=image_audit)
assert image_audit[gguf_id]["decision"] == "matched"
speech_audit = {}
website_references_for_project(
    {"name": "speech-service", "description": "Voice generation", "topics": []},
    {"domains": ["ai_media"]}, assessment=speech_audit
)
assert speech_audit[gguf_id]["decision"] == "not-relevant"
assert speech_audit[gguf_id]["integrationEligible"] is False
# Advisory matching must work on real sparse repository identities.
# The native-code recommender still uses its stricter engine/domain profile.
sparse_assets = {"name": "asset-forge", "description": None, "topics": []}
sparse_asset_profile = {
    "domains": [],
    "terms": tokens("central visual asset production illustration sprites textures"),
}
sparse_asset_refs = website_references_for_project(sparse_assets, sparse_asset_profile)
assert gguf_id in {x["id"] for x in sparse_asset_refs}, sparse_asset_refs
assert all(not x["integrationEligible"] for x in sparse_asset_refs)
sparse_video_refs = website_references_for_project(
    {"name": "monteur-video", "description": None, "topics": []},
    {"domains": [], "terms": set()},
)
assert "fasth3-omni-collection" in {x["id"] for x in sparse_video_refs}, sparse_video_refs
assert gguf_id not in {x["id"] for x in sparse_video_refs}
finance_asset_refs = website_references_for_project(
    {"name": "asset-ledger", "description": None, "topics": []},
    {"domains": [], "terms": tokens("portfolio finance trades balance")},
)
assert gguf_id not in {x["id"] for x in finance_asset_refs}
# The general Hugging Face hub is an advisory discovery *directory*, not a
# blanket licence or a source of free unrestricted inference.
hf_hub_id = "hugging-face-hub"
minicpm_id = "minicpm-v-4-7-1b-heretic"
assert sum(site["id"] == hf_hub_id for site in sites) == 1
assert sum(site["id"] == minicpm_id for site in sites) == 1
hf_hub = next(site for site in sites if site["id"] == hf_hub_id)
assert hf_hub["type"] == "model-hub" and hf_hub["reuse"] == "reference-only"
assert hf_hub["url"] == "https://huggingface.co/"
assert not hf_hub.get("upstreamModel")
vlm = next(site for site in sites if site["id"] == minicpm_id)
assert vlm["sourceLicenseTag"] == "apache-2.0"
assert vlm["upstreamModel"] == "openbmb/MiniCPM-V-4.7-1B"
assert vlm["safetyRisk"] == "reduced-refusal"
assert "uncensored" not in str(vlm.get("bestFor", [])).lower()
assert vlm["type"] == "model-checkpoint"
assert not vlm.get("portfolioBaselineDomains")
# An OCR/vision project may lack GitHub topics or primary AI language; this
# case must NOT promote a model to a native code dependency.
vision_ref = website_references_for_project(
    {"name": "ocr-screenshot-reader", "description": None, "topics": []},
    {"domains": [], "terms": set()}
)
vlm_ref = next(x for x in vision_ref if x["id"] == minicpm_id)
assert vlm_ref["safetyRisk"] == "reduced-refusal"
assert "reduced-refusal-public-safety-review" in vlm_ref["reviewGates"]
assert "model-runtime-and-device-review" in vlm_ref["reviewGates"]
assert vlm_ref["sourceLicenseTag"] == "apache-2.0"
assert vlm_ref["integrationEligible"] is False
assert vlm_ref["upstreamModel"] == vlm["upstreamModel"]
assert hf_hub_id in {x["id"] for x in vision_ref}
# An AI agent can discover Hugging Face even without a particular model
# family or action signal; the exact abliterated checkpoint stays gated.
agent_refs = website_references_for_project(
    {"name": "ai-agent", "description": None, "topics": []},
    {"domains": ["ai_agents"], "terms": set()}
)
assert hf_hub_id in {x["id"] for x in agent_refs}
assert "per-item-license-and-provider-review" in next(
    x for x in agent_refs if x["id"] == hf_hub_id
)["reviewGates"]
assert minicpm_id not in {x["id"] for x in agent_refs}
assert minicpm_id not in {x["id"] for x in tts_portfolio_sites}
assert minicpm_id not in {x["id"] for x in sparse_asset_refs}
assert minicpm_id not in {x["id"] for x in quiet_game}
vision_decisions = {}
website_references_for_project(
    {"name": "ocr-screenshot-reader", "description": None, "topics": []},
    {"domains": [], "terms": set()}, assessment=vision_decisions
)
assert vision_decisions[minicpm_id]["decision"] == "matched"
assert "reduced-refusal-public-safety-review" in vision_decisions[minicpm_id]["reviewGates"]
assert vision_decisions[minicpm_id]["integrationEligible"] is False
# Game repositories often have sparse GitHub descriptions. Their actual
# game-development domain is sufficient to recommend art-direction research.
game_sites = website_references_for_project(
    {"name": "Jumpy", "description": None, "topics": []},
    {"domains": ["game_dev"]},
)
assert game_sites[0]["id"] == "game-art-style", game_sites
assert game_sites[0]["reuse"] == "reference-only"
assert game_sites[0]["integrationEligible"] is False
# PINOC is a user-authorized external MCP reference, not an automatically
# installed game dependency or a free unlimited generation provider.
pinoc_rows = run("3d rigging mocap animation blender", "--websites", "--top-websites", "20")["websiteRecommendations"]
pinoc = next(site for site in pinoc_rows if site["id"] == "viggle-pinoc-mcp")
assert pinoc["mcpEndpoint"] == "https://pinoc.mcp.viggle.ai/mcp"
assert pinoc["integrationEligible"] is False
assert pinoc["reuse"] == "hosted-service" and pinoc["access"] == "freemium"
assert next(site for site in sites if site["id"] == "viggle-pinoc-mcp")["originalUrl"] == "https://viggle.ai/pinoc/app/mcp"
motion_sites = website_references_for_project(
    {"name": "NPC Animation", "description": "3D mocap and rigged NPCs in Blender",
     "topics": ["rigging"]},
    {"domains": ["game_dev", "graphics"]},
)
assert [row["id"] for row in motion_sites[:2]] == ["game-art-style", "viggle-pinoc-mcp"], motion_sites
assert "jupiter-game-art-style" in {row["id"] for row in motion_sites}, motion_sites
assert all(site["id"] != "viggle-pinoc-mcp" for site in game_sites), game_sites
# Roblox is a named engine with possible 3D skeletal animations; the
# advisory PINOC reference must be discoverable without guessing from README.
roblox_sites = website_references_for_project(
    # Actual public GitHub metadata: no description, no topics, Lua language.
    {"name": "chaos-survival-roblox", "description": None, "topics": []},
    {"domains": ["game_dev"]},
)
assert [item["id"] for item in roblox_sites[:2]] == ["game-art-style", "viggle-pinoc-mcp"], roblox_sites
assert "jupiter-game-art-style" in {item["id"] for item in roblox_sites}, roblox_sites
assert all(item["integrationEligible"] is False for item in roblox_sites)
assert all(site["id"] != "viggle-pinoc-mcp" for site in tts_portfolio_sites), tts_portfolio_sites
from validate_websites import check_websites
import copy
website_schema = json.loads((ROOT / "schemas/websites.schema.json").read_text(encoding="utf-8"))
assert not check_websites(websites_catalog, website_schema)
unsafe_websites = copy.deepcopy(websites_catalog)
bad_pinoc = next(site for site in unsafe_websites["websites"] if site["id"] == "viggle-pinoc-mcp")
bad_pinoc["mcpEndpoint"] = "https://attacker.example/mcp"
assert check_websites(unsafe_websites, website_schema)
bad_pinoc["mcpEndpoint"] = "https://pinoc.mcp.viggle.ai/other"
assert check_websites(unsafe_websites, website_schema)
bad_model = copy.deepcopy(websites_catalog)
model_data = next(x for x in bad_model["websites"] if x["id"] == gguf_id)
model_data.pop("sourceLicenseTag")
assert check_websites(bad_model, website_schema)
model_data["sourceLicenseTag"] = "other"
model_data["portfolioBaselineDomains"] = ["ai_media"]
assert check_websites(bad_model, website_schema)
unsafe_vlm = copy.deepcopy(websites_catalog)
vlm_row = next(x for x in unsafe_vlm["websites"] if x["id"] == minicpm_id)
vlm_row.pop("safetyRisk")
assert check_websites(unsafe_vlm, website_schema)
vlm_row["safetyRisk"] = "reduced-refusal"
vlm_row["portfolioBaselineDomains"] = ["ai_media"]
assert check_websites(unsafe_vlm, website_schema)
unsafe_hf = copy.deepcopy(websites_catalog)
hf_row = next(x for x in unsafe_hf["websites"] if x["id"] == hf_hub_id)
hf_row["reuse"] = "open-source-upstream"
assert check_websites(unsafe_hf, website_schema)
unsafe_marketing = copy.deepcopy(websites_catalog)
unsafe_sopilot = next(x for x in unsafe_marketing["websites"] if x["id"] == sopilot_id)
unsafe_sopilot["portfolioBaselineDomains"] = ["marketing"]
assert check_websites(unsafe_marketing, website_schema)
unsafe_humanizer = copy.deepcopy(websites_catalog)
humanizer_row = next(x for x in unsafe_humanizer["websites"] if x["id"] == humanizer_id)
humanizer_row.pop("supportedLanguages")
assert check_websites(unsafe_humanizer, website_schema)
humanizer_row["supportedLanguages"] = ["en", "zh"]
humanizer_row["portfolioBaselineDomains"] = ["writing"]
assert check_websites(unsafe_humanizer, website_schema)
unsafe_sopilot.pop("portfolioBaselineDomains")
unsafe_sopilot["reuse"] = "open-source-upstream"
assert check_websites(unsafe_marketing, website_schema)
# HF model IDs commonly contain dots (MiniCPM-V-4.7), while
# dot-segment path traversal, queries and embedded credentials stay blocked.
from validate_websites import canonical_url
assert canonical_url("https://huggingface.co/saidutta69/MiniCPM-V-4.7-1B-heretic") == (
    "huggingface.co/saidutta69/MiniCPM-V-4.7-1B-heretic"
)
for unsafe_url in (
    "https://huggingface.co/../secret",
    "https://huggingface.co/a/./b",
    "https://huggingface.co/a..b",
    "https://huggingface.co/a//b",
    "https://huggingface.co/?download=1",
    "https://user:secret@huggingface.co/model",
):
    try:
        canonical_url(unsafe_url)
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe URL accepted: " + unsafe_url)

strict = run("android mobile", "--platform", "android", "--require-all-caps", "--cap", "mobile")
for item in strict["recommendations"]:
    assert "android" in item["platforms"]
    assert "mobile" in set(item["capabilities"]), item["repo"]

high_threshold = run("ai agent", "--min-score", "1000")
assert high_threshold["recommendations"] == []
assert high_threshold["diagnostics"]["returned"] == 0

# All catalog records are ranked by default, including zero/negative scores,
# indexed entries, archived and disabled entries. Ranking is not approval.
default_audit = run("ponytail agent", "--top", "30")
assert default_audit["diagnostics"]["eligible"] == default_audit["diagnostics"]["catalogSize"]
assert default_audit["diagnostics"]["filtered"]["indexed"] == 0
assert default_audit["diagnostics"]["filtered"]["inactive"] == 0
assert default_audit["diagnostics"]["filtered"]["minScore"] == 0
assert default_audit["constraints"]["includeAudit"] is True
assert default_audit["constraints"]["includeArchived"] is True
assert default_audit["constraints"]["minScore"] is None
ponytail = next(item for item in default_audit["recommendations"]
               if item["repo"] == "DietrichGebert/ponytail")
assert ponytail["tier"] == "indexed"
assert ponytail["availableForDiscovery"] is True
assert ponytail["automaticIntegrationApproved"] is False
assert "indexed-unverified" not in ponytail["rankingReviewGates"]

# Legacy positive flags continue to work. Explicit opt-out filters remain available.
with_audit = run("ponytail agent", "--top", "30", "--include-audit", "--include-archived")
assert with_audit["diagnostics"]["eligible"] == default_audit["diagnostics"]["eligible"]
without_audit = run("ponytail agent", "--top", "30", "--exclude-audit")
assert all(item["tier"] != "indexed" for item in without_audit["recommendations"])
assert without_audit["diagnostics"]["filtered"]["indexed"] > 0
assert without_audit["constraints"]["includeAudit"] is False
without_inactive = run("ponytail agent", "--top", "30", "--exclude-archived")
assert without_inactive["diagnostics"]["filtered"]["inactive"] > 0
assert without_inactive["constraints"]["includeArchived"] is False
# An impossible query still ranks every record; relevance is not an admission gate.
zero_relevance = run("qzxwvtr234567unknown", "--top", "5")
assert zero_relevance["diagnostics"]["eligible"] == zero_relevance["diagnostics"]["catalogSize"]
assert all("rankingReviewGates" in item for item in zero_relevance["recommendations"])


spec = importlib.util.spec_from_file_location("recommend", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Ranking preserves uncertain source facts without inventing missing values.
assert mod.metadata_review_gates({"github": {"license": "MIT"}, "selfHosted": True}) == []
assert mod.metadata_review_gates({"github": {"license": "NOASSERTION"}, "selfHosted": "unknown"}) == [
    "license-unresolved", "self-hosting-unverified"
]
assert mod.metadata_review_gates({"github": {"license": None}, "selfHosted": "partial"}) == [
    "license-unresolved", "self-hosting-unverified"
]
assert mod.metadata_review_gates({}) == [
    "github-metadata-unavailable", "self-hosting-unverified"
]
complete_rank = run("youtube cartoon video automation", "--top", "2000")
entire_catalog = mod.load()[0]
assert complete_rank["diagnostics"]["eligible"] == len(entire_catalog)
assert complete_rank["diagnostics"]["returned"] == len(entire_catalog)
metadata_counts = complete_rank["diagnostics"]["metadata"]
assert metadata_counts["unverifiedSelfHosting"] == sum(
    not isinstance(entry.get("selfHosted"), bool) for entry in entire_catalog
)
assert metadata_counts["unresolvedLicenses"] == sum(
    "license-unresolved" in mod.metadata_review_gates(entry) for entry in entire_catalog
)
assert metadata_counts["reviewRequired"] == sum(
    bool(mod.metadata_review_gates(entry) or mod.ranking_review_gates(entry)) for entry in entire_catalog
)
assert all(item["reviewRequired"] == bool(item["rankingReviewGates"] or item["metadataReviewGates"])
           for item in complete_rank["recommendations"])

# The first release previously suggested an unrelated Roblox stack for a
# faceless-YouTube task because generic words in stack notes matched.
stack_catalog = mod.load()[1]
for query in ("faceless youtube cartoon AI video voiceover thumbnails",
              "educational animated video content automatic captions narration"):
    assert mod.choose_stack(stack_catalog, mod.tokens(query),
                            mod.infer_domains(mod.tokens(query))) is None
assert mod.choose_stack(stack_catalog, mod.tokens("roblox studio luau playtesting"),
                        {"game_dev"})["name"] == "Roblox Studio Agent Production"
assert mod.choose_stack(stack_catalog, mod.tokens("godot gameplay shaders vfx"),
                        {"game_dev"})["name"] == "Godot Gameplay and VFX"
assert mod.choose_stack(stack_catalog, mod.tokens("android vector animation"),
                        {"graphics", "mobile"})["name"] == "Vector Animation Android"
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
audit_candidate = dict(candidate, repo="x/indexed", tier="indexed", score=8.0)
assert mod.infer_alternatives(source, [source, candidate, audit_candidate]) == ["x/candidate", "x/indexed"][:2]
assert "x/source" not in mod.infer_alternatives(source, [source, candidate, audit_candidate])

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

# Hard constraints must also apply to curated/inferred relations and suggested stacks.
assert mod.infer_domains(mod.tokens("AI video narration")) == {"ai_media"}
assert mod.infer_domains(mod.tokens("AI marketing")) == {"marketing"}
assert mod.infer_domains(mod.tokens("AI agent video")) == {"ai_agents", "ai_media"}
assert mod.infer_domains(mod.tokens("AI")) == {"ai_agents"}
assert mod.infer_domains(mod.tokens("Roblox Studio Luau")) == {"game_dev"}
assert mod.infer_domains(mod.tokens("Godot shaders")) == {"game_dev"}
assert mod.choose_stack(stacks, mod.tokens("backend"), {"backend"}, {"x/source"}) is None
assert mod.choose_stack(stacks, mod.tokens("backend"), {"backend"}, {"x/source", "x/stack-tool"})["name"] == "Backend Stack"

limited_rel = mod.resolve_relations(
    dict(source, alternatives=["x/audit", "x/candidate", "x/candidate", "x/source"],
         complements=["x/stack-tool", "x/audit"]),
    [source, candidate, audit_candidate],
    stacks,
    {**repo_by_name, "x/audit": audit_candidate, "x/candidate": candidate},
    {"x/source", "x/candidate"},
)
assert limited_rel["alternatives"] == ["x/candidate"], limited_rel
assert limited_rel["alternativesSource"] == "curated"
assert limited_rel["complements"] == []
assert limited_rel["complementsSource"] == "none"

fallback = mod.resolve_relations(
    dict(source, alternatives=["x/audit"], complements=["x/audit"]),
    [source, candidate, audit_candidate], stacks,
    {**repo_by_name, "x/audit": audit_candidate},
    {"x/source", "x/candidate"},
)
assert fallback["alternatives"] == ["x/candidate"] and fallback["alternativesSource"] == "inferred"
assert fallback["complements"] == [] and fallback["complementsSource"] == "none"

# Integration: returned relations must obey the same hard CLI filters as primary recommendations.
for results in (
    run("android vector animation", "--platform", "android", "--max-resource", "medium", "--top", "15"),
    run("python data", "--language", "python", "--max-complexity", "low", "--top", "15"),
):
    catalog_index = {entry["repo"]: entry for entry in mod.load()[0]}
    constraints = results["constraints"]
    for item in results["recommendations"]:
        for name in item["alternatives"] + item["complements"]:
            linked = catalog_index[name]
            assert linked["tier"] in {"core", "recommended", "specialized", "indexed"}
            assert not linked.get("github", {}).get("archived")
            assert all(p in linked.get("platforms", []) for p in constraints["platforms"])
            assert all(lang in linked.get("languages", []) for lang in constraints["languages"])
            assert mod.LEVEL.get(linked.get("resourceLevel", "medium"), 1) <= mod.LEVEL[constraints["maxResource"]]
            assert mod.LEVEL.get(linked.get("integrationComplexity", "medium"), 1) <= mod.LEVEL[constraints["maxComplexity"]]
    if results["recommendedStack"]:
        for member in results["recommendedStack"]["repos"]:
            linked = catalog_index[member]
            assert linked["tier"] in {"core", "recommended", "specialized", "indexed"}
            assert all(p in linked.get("platforms", []) for p in constraints["platforms"])
            assert all(lang in linked.get("languages", []) for lang in constraints["languages"])

# Scenario Labs 3D asset dataset is a licensed, per-file reviewed visual
# resource: match 3D game projects, reject unrelated coding/video tasks, and
# never silently download, import or dispatch model files as code.
scenario_id = "scenario-labs-3d-collection"
scenario = next(x for x in sites if x["id"] == scenario_id)
assert sum(x["id"] == scenario_id for x in sites) == 1
assert scenario["url"] == "https://huggingface.co/datasets/scenario-labs/3d-collection"
assert scenario["type"] == "3d-asset-dataset"
assert scenario["reuse"] == "licensed-material"
assert scenario["sourceLicenseTag"] == "cc-by-4.0"
assert scenario["portfolioRequiredSignals"] and not scenario.get("portfolioBaselineDomains")
scenario_query = run("roblox 3d glb models", "--websites", "--top-websites", "80")
scenario_ranked = next(x for x in scenario_query["websiteRecommendations"] if x["id"] == scenario_id)
assert scenario_ranked["integrationEligible"] is False
assert {"asset-level-license-and-attribution-review",
        "3d-mesh-texture-and-target-engine-review",
        "individual-download-hash-and-file-safety-review",
        "third-party-reuse-rights-review"} <= set(scenario_ranked["reviewGates"])
scenario_game = {"name": "chaos-survival", "description": "Roblox 3D arena meshes", "topics": ["game"]}
scenario_matches = website_references_for_project(scenario_game, {"domains": ["game_dev"], "terms": set()})
assert scenario_id in {x["id"] for x in scenario_matches}
scenario_assessment = {}
website_references_for_project(scenario_game, {"domains": ["game_dev"], "terms": set()}, assessment=scenario_assessment)
assert scenario_assessment[scenario_id]["decision"] == "matched"
assert scenario_assessment[scenario_id]["integrationEligible"] is False
for unrelated in (
    {"name": "TTS", "description": "AI speech synthesis", "topics": []},
    {"name": "production-os", "description": "Code automation agent", "topics": []},
    {"name": "promo-alimentaire", "description": "Food prices and offers", "topics": []},
):
    unrelated_assessment = {}
    sites_for_unrelated = website_references_for_project(
        unrelated, {"domains": ["ai_media"] if unrelated["name"] == "TTS" else [], "terms": set()},
        assessment=unrelated_assessment
    )
    assert scenario_id not in {x["id"] for x in sites_for_unrelated}, unrelated
    assert unrelated_assessment[scenario_id]["decision"] == "not-relevant", unrelated

# GitReverse is a hosted, review-only reverse-prompt helper, not an audit
# engine. Select it for explicit codebase/repository work, not every AI app.
gitreverse_id = "gitreverse"
gitreverse = next(s for s in sites if s["id"] == gitreverse_id)
assert sum(s["id"] == gitreverse_id for s in sites) == 1
assert gitreverse["url"] == "https://www.gitreverse.com/"
assert gitreverse["type"] == "codebase-prompt-generator"
assert gitreverse["reuse"] == "hosted-service" and gitreverse["access"] == "freemium"
assert gitreverse["portfolioRequiredSignals"] and not gitreverse.get("portfolioBaselineDomains")
matched_prompt = next(s for s in run(
    "coding agent github repository reverse engineering prompt",
    "--websites", "--top-websites", "100"
)["websiteRecommendations"] if s["id"] == gitreverse_id)
assert matched_prompt["integrationEligible"] is False
assert {"public-prompt-visibility-and-sensitive-input-review",
        "generated-prompt-accuracy-and-source-code-review",
        "untrusted-repository-and-website-prompt-injection-review",
        "upstream-code-and-website-reuse-rights-review",
        "hosted-terms-privacy-and-cost-review"} <= set(matched_prompt["reviewGates"])
prompt_project = {
    "name": "repo-onboarding-agent",
    "description": "Coding agent for public GitHub codebase analysis and prompt specifications",
    "topics": ["prompt-engineering"]
}
gitreverse_decisions = {}
prompt_refs = website_references_for_project(
    prompt_project, {"domains": ["ai_agents", "software_engineering"], "terms": set()},
    assessment=gitreverse_decisions
)
assert gitreverse_id in {site["id"] for site in prompt_refs}
assert gitreverse_decisions[gitreverse_id]["decision"] == "matched"
assert gitreverse_decisions[gitreverse_id]["integrationEligible"] is False
for unrelated in (
    {"name": "JumpyFrog", "description": "Godot jumping game", "topics": []},
    {"name": "monteur-video", "description": "Automated video montage", "topics": []},
    {"name": "production-os", "description": "Coding automation service", "topics": []},
):
    decisions = {}
    refs = website_references_for_project(
        unrelated, {"domains": ["software_engineering"] if unrelated["name"] == "production-os"
                    else ["game_dev"] if unrelated["name"] == "JumpyFrog" else ["ai_media"],
                    "terms": set()}, assessment=decisions
    )
    assert gitreverse_id not in {site["id"] for site in refs}, unrelated
    assert decisions[gitreverse_id]["decision"] == "not-relevant", unrelated
unsafe_reverse = animation_copy.deepcopy(websites_catalog)
reverse_site = next(s for s in unsafe_reverse["websites"] if s["id"] == gitreverse_id)
reverse_site["reuse"] = "open-source-upstream"
assert validate_visual_websites(unsafe_reverse, animation_schema)
reverse_site["reuse"] = "hosted-service"
reverse_site["portfolioBaselineDomains"] = ["software_engineering"]
assert validate_visual_websites(unsafe_reverse, animation_schema)

# Pixel VFX Forge: explicit 2D/FX evidence routes to a reviewed hosted
# visual editor; it is not a free commercial asset licence or code dependency.
pixel_forge_id = "scenario-pixel-vfx-forge"
pixel_forge = next(s for s in sites if s["id"] == pixel_forge_id)
assert sum(s["id"] == pixel_forge_id for s in sites) == 1
assert pixel_forge["url"] == "https://www.scenario.com/explorations/pixel-vfx-forge/"
assert pixel_forge["type"] == "pixel-vfx-editor"
assert pixel_forge["access"] == "free" and pixel_forge["reuse"] == "hosted-service"
assert pixel_forge["portfolioRequiredSignals"] and not pixel_forge.get("portfolioBaselineDomains")
pixel_query = run("godot pixel art 2d sprite vfx", "--websites", "--top-websites", "100")
pixel_advice = next(s for s in pixel_query["websiteRecommendations"] if s["id"] == pixel_forge_id)
assert pixel_advice["integrationEligible"] is False
assert {
    "pixel-vfx-export-commercial-licence-confirmation",
    "sprite-sheet-godot-import-animation-and-mobile-review",
    "external-agent-skill-archive-and-json-recipe-trust-review",
    "hosted-terms-privacy-and-cost-review",
} <= set(pixel_advice["reviewGates"])
for project, domains in (
    ({"name": "jumpy-frog", "description": "Godot jumping game", "topics": ["2d"]}, ["game_dev"]),
    ({"name": "pixel-effects", "description": "Pixel art sprite and vfx animation", "topics": []}, ["graphics"]),
):
    decisions = {}
    refs = website_references_for_project(project, {"domains": domains, "terms": set()}, assessment=decisions)
    matched = next(s for s in refs if s["id"] == pixel_forge_id)
    assert matched["integrationEligible"] is False
    assert decisions[pixel_forge_id]["decision"] == "matched"
    assert decisions[pixel_forge_id]["reviewGates"] == matched["reviewGates"]
for unrelated, domains in (
    ({"name": "generic-game", "description": "An online game", "topics": []}, ["game_dev"]),
    ({"name": "production-os", "description": "Software coding automation", "topics": []}, ["software_engineering"]),
    ({"name": "TTS", "description": "Audio speech generation", "topics": []}, ["ai_media"]),
    ({"name": "promo-alimentaire", "description": "Food coupons", "topics": []}, []),
):
    decisions = {}
    refs = website_references_for_project(unrelated, {"domains": domains, "terms": set()}, assessment=decisions)
    assert pixel_forge_id not in {s["id"] for s in refs}, unrelated
    assert decisions[pixel_forge_id]["decision"] == "not-relevant", unrelated
unsafe_pixel = animation_copy.deepcopy(websites_catalog)
unsafe_site = next(s for s in unsafe_pixel["websites"] if s["id"] == pixel_forge_id)
unsafe_site["reuse"] = "open-source-upstream"
assert validate_visual_websites(unsafe_pixel, animation_schema)
unsafe_site["reuse"] = "hosted-service"
unsafe_site["portfolioBaselineDomains"] = ["game_dev"]
assert validate_visual_websites(unsafe_pixel, animation_schema)

print("OK: recommendation engine smoke tests passed")
