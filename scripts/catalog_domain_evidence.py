#!/usr/bin/env python3
"""Evidence-only advisory routing for catalog entries whose domain is unknown.

Neither text clues nor GitHub descriptions authorize installation or execution.
Keep named/curated domains authoritative and do not overwrite catalog metadata.
"""
import re

# Only explicit technical capabilities or unambiguous *task phrases* qualify.
# Generic words ("AI", "agent", "web", "app", "automation") never qualify alone.
CAPABILITY_DOMAIN_SIGNALS = {
    "ai_media": {
        "text2music", "text-to-music", "text-to-video", "text-to-image",
        "video-generation", "video-recording", "video-editing", "text2video",
        "image-generation", "voice-audio", "audio-generation", "voice-cloning",
        "speech-synthesis", "tts", "music-generation", "diffusion",
        "lip-sync", "text-to-speech", "speech-recognition", "stt",
        "speech-to-text", "video-restoration", "video-transcription",
        "video-translation", "webcam", "video-workflows", "ai-video",
        "ffmpeg", "digital-human", "talking-head", "multimedia", "audio-editor",
        "image-to-video", "storyboard", "storyboarding", "manga-generation",
        "comic-generation", "music-video", "ocr", "audio-processing",
    },
    "ai_agents": {
        "mcp", "agent-sdk", "coding-agent", "agent-runtime", "agent-framework",
        "llm-agent", "multi-agent", "agent-orchestration",
        "mcp-server", "mcp-client", "ai-coding-agent",
        "agent-skills", "hermes-agent",
    },
    "game_dev": {
        "godot", "roblox", "luau", "unity", "unreal", "game-development",
        "game-engine", "gameplay", "game-assets", "games",
        "open-source-games", "game-developer", "game-development-tools",
    },
    "graphics": {
        "3d-modeling", "rigging", "shader", "shaders", "texture-generation",
        "vector-animation", "svg", "blender", "3d-rendering",
        "ui-design", "ux-design", "design-rules",
        "3d-animation", "motion-design", "colorization",
        "webgpu", "manga", "comics", "comic", "illustration",
    },
    "mobile": {
        "android", "android-sdk", "ios", "jetpack-compose", "flutter",
        "android-app", "swiftui", "ios-development",
    },
    "cybersecurity": {
        "pentest", "penetration-testing", "security-scanning", "osint",
        "vulnerability-scanning", "cve", "rce", "redteam", "red-team",
        "bug-bounty", "security-testing", "hardware-hacking",
        "binary-analysis", "instrumentation",
        "hacking-tool", "hacking-tools", "c2", "malware-analysis",
        "imsi-catcher",
    },
    "trading": {
        "backtesting", "backtest", "quantitative-trading", "trading",
        "market-data", "forex", "xauusd", "stock-trading",
        "financial-markets", "algorithmic-trading",
    },
    "web_frontend": {
        "react", "vue", "svelte", "frontend", "webgl", "ui-components",
        "css", "tailwind", "nextjs", "webgpu",
        "web-interface", "browser-extension", "chrome-extension",
    },
    "backend": {
        "database", "orm", "graphql", "backend", "postgresql",
        "fastapi", "supabase", "sqlite", "mysql", "serverless",
    },
    "devops": {
        "kubernetes", "docker", "ci-cd", "infrastructure-as-code",
        "observability", "terraform", "monitoring",
        "cloud-native", "cicd",
    },
    "software_engineering": {
        "code-search", "static-analysis", "refactoring", "test-runner",
        "code-review", "code-quality", "repository-analysis",
        "spec-driven", "spec-driven-development", "reverse-engineering",
        "ai-coding-agent", "performance-profiling",
        "claude-skills", "test-automation",
    },
    "ai_memory": {
        "rag", "vector-database", "vector-search", "retrieval-augmented-generation",
        "embeddings", "context-compression", "context-management",
        "agentmemory", "persistent-memory",
    },
    "data_ml": {
        "fine-tuning", "llm-training", "machine-learning", "ml-training",
        "dataset-analysis", "computer-vision", "vision-language-model",
        "edge-ai", "on-device-ai", "ml-inference", "multi-modal",
        "multimodal",
    },
    "embedded_iot": {
        "esp32", "esp8266", "esp-idf", "esp32-arduino", "arduino",
        "microcontroller", "firmware", "embedded", "embedded-systems",
        "iot", "iot-platform", "rtos", "freertos", "platformio",
        "raspberry-pi", "espressif", "drone", "quadcopter",
        "esp32-cam", "lora", "lorawan", "zigbee", "cnc",
        "stepper-motor", "robotics", "gpio", "esp32cam",
        "esp32-s3", "esp32c3", "esp32-c5",
    },
    "marketing": {
        "seo", "digital-marketing", "social-media", "copywriting",
        "serp", "geo", "email-template", "brand-kit", "flyer-maker",
    },
    "productivity": {
        "erp", "crm", "accounting", "task-management",
        "hrms", "asset-management", "point-of-sale", "procurement",
        "email", "email-template", "time-tracking", "token-usage",
        "job-search", "resume", "cv",
    },
    "writing": {
        "copywriting", "blog-writing", "novel-writing", "prompt-library",
        "storytelling", "prompt-engineering",
    },
}
# A title/description is *less* trustworthy than a structured capability.
# Match task-specific phrases, never freeform single-topic descriptions.
DESCRIPTION_DOMAIN_PHRASES = {
    "ai_media": (
        "music generation", "video generation", "image generation", "video editing",
        "video editor", "audio processing", "speech synthesis", "voice cloning",
        "short drama", "text to video", "text to image", "text to music",
        "generate video", "generate music", "generate images", "video production",
        "lip sync", "speech recognition", "video restoration", "video transcription",
        "subtitle generation", "audio editor", "audio video downloader",
        "digital human", "text to speech", "image to video",
        "voice synthesis", "manga creation", "comic creation",
        "line art colorization", "video analytics", "video workflow",
        "rigged character", "ai creative platform",
    ),
    "ai_agents": (
        "agent sdk", "agent framework", "agent orchestration", "mcp server",
        "model context protocol", "coding agent", "autonomous coding",
        "hermes agent", "agent skills", "agent tool",
        "managed employee",
    ),
    "game_dev": (
        "godot plugin", "godot engine", "roblox studio", "luau scripting",
        "game engine", "game development", "unity game",
        "open source games", "game dev",
    ),
    "graphics": (
        "3d modeling", "3d rendering", "shader effects", "skeletal animation",
        "skeletal motion capture", "motion capture animation",
        "vector animation", "3d model",
        "ui design", "design platform", "motion design",
        "3d character", "rigged character", "storyboard generation",
        "webgpu ocean", "visual effects",
    ),
    "mobile": (
        "android application", "android sdk", "ios application", "flutter application",
        "android app", "mobile app", "swiftui",
    ),
    "cybersecurity": (
        "penetration testing", "vulnerability scanning", "bug bounty",
        "security testing", "red team", "remote code execution",
        "offensive security", "hardware hacking",
        "binary analysis", "firmware analysis",
        "remote rce", "redteam toolkit", "cve exploit", "imsi catcher",
        "penetration tester",
    ),
    "trading": (
        "trading bot", "backtesting framework", "market data",
        "crypto trading", "forex trading", "financial markets",
        "foundation model for the language of financial markets",
    ),
    "web_frontend": (
        "frontend framework", "react components", "vue components",
        "web ui", "website builder", "webgpu renderer",
        "browser extension", "user interface components",
    ),
    "backend": (
        "database server", "postgresql database", "backend service",
        "graphql api", "sqlite backed", "database engine",
    ),
    "devops": (
        "infrastructure as code", "kubernetes deployment", "docker orchestration",
        "continuous integration", "deployment automation",
    ),
    "software_engineering": (
        "static code analysis", "code search", "code refactoring", "automated testing",
        "repository analysis", "spec driven development",
        "claude code skills", "memory leaks", "test automation",
        "code debugging", "reverse engineer anything",
        "context compression plugin",
    ),
    "ai_memory": (
        "retrieval augmented generation", "vector database", "semantic search",
        "agent memory", "persistent memory", "memory for ai coding agents",
        "context compression",
    ),
    "data_ml": (
        "machine learning", "model fine tuning", "model training",
        "dataset analysis", "inference framework", "inference repo",
        "computer vision", "edge ai", "vision language", "model inference",
    ),
    "embedded_iot": (
        "esp32", "esp8266", "esp idf", "arduino core",
        "microcontroller", "embedded systems", "embedded firmware",
        "quadcopter firmware", "firmware for", "rtos for esp32",
        "esp32 emulator", "drone firmware", "esp32 based",
        "sensor board", "robot cleaner", "esp32 bluetooth",
    ),
    "marketing": (
        "social media posts", "seo optimized", "serp rank",
        "email templates", "digital marketing", "flyer maker",
    ),
    "productivity": (
        "enterprise resource planning", "job search", "track token usage",
        "email templates", "application framework", "resume builder",
        "transactional mail",
    ),
    "writing": (
        "novel writing", "write blog", "long form seo", "blog content",
        "prompt library", "story writing",
    ),
}


def _normalized(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def advisory_domain_evidence(item):
    """Return {domain: supporting evidence strings}, for advisory routing only."""
    domain = item.get("domain")
    if isinstance(domain, str) and domain not in ("other", "unknown", ""):
        return {domain: ["catalog-domain"]}
    caps = {str(v).strip().casefold() for v in (
        (item.get("capabilities") or []) + (item.get("roles") or [])
    ) if isinstance(v, str)}
    # Structured capability labels may be overly broad or inaccurate. The
    # result is therefore advisory even if the label is an exact match.
    description = _normalized(" ".join(
        str(v)[:400] for v in (item.get("bestFor") or [])[:3] if isinstance(v, str)
    ))
    # Exact ecosystem tokens from the repository slug are robust enough for
    # advisory routing, but ambiguous brand/project names are not.
    slug = str(item.get("repo") or "").split("/")[-1]
    slug_terms = {x for x in re.split(r"[^a-z0-9]+", slug.lower()) if x}
    slug_source = slug.casefold()
    if re.search(r"(?<![a-z0-9])agent-sdk(?![a-z0-9])", slug_source):
        slug_terms.add("agent-sdk")
    specific_slug_technology = {
        "embedded_iot": {"esp32", "esp8266", "arduino", "microcontroller"},
        "graphics": {"webgpu"},
        "ai_media": {"ffmpeg", "wav2lip"},
        "cybersecurity": {"binwalk"},
        "devops": {"kubernetes"},
        "ai_agents": {"agent-sdk"},
    }
    evidence = {}
    for name, lexemes in specific_slug_technology.items():
        match = sorted(slug_terms & lexemes)
        if match:
            evidence[name] = ["repo-name:" + m for m in match[:2]]
    for name, signals in CAPABILITY_DOMAIN_SIGNALS.items():
        hits = sorted(caps & signals)
        if hits:
            evidence[name] = ["capability:" + h for h in hits[:3]]
    for name, phrases in DESCRIPTION_DOMAIN_PHRASES.items():
        matches = [s for s in phrases if re.search(
            r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", description
        )]
        if matches:
            evidence.setdefault(name, [])
            evidence[name].extend("description:" + m for m in sorted(matches)[:2])
    return evidence
