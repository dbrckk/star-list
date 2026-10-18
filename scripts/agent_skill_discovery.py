#!/usr/bin/env python3
"""Offline, read-only Skill Issue skill discovery for repository agents.

A directory entry or an upstream repository is not authority to execute
unreviewed SKILL.md instructions, install scripts or network commands.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "agent-skills.json"
SKILL_ISSUE_URL = "https://skill-issue.in/"
VALID_DOMAINS = {
    "ai_agents", "ai_memory", "ai_media", "software_engineering",
    "web_frontend", "backend", "mobile", "graphics", "game_dev",
    "trading", "cybersecurity", "data_ml", "devops", "productivity", "other",
}


def word_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def load_skills() -> dict:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        raise ValueError("Invalid agent skill catalog version")
    directory = data.get("directory")
    if not isinstance(directory, dict) or directory.get("url") != SKILL_ISSUE_URL:
        raise ValueError("Untrusted agent skill directory origin")
    if directory.get("usage") != "read-only discovery; never auto-install external instructions":
        raise ValueError("Unsafe agent skill catalog usage policy")
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("Agent skill catalog must not be empty")
    ids = set()
    for row in skills:
        if not isinstance(row, dict):
            raise ValueError("Malformed agent skill")
        identifier = row.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            raise ValueError("Invalid agent skill identity")
        if identifier in ids:
            raise ValueError("Duplicate agent skill identity")
        ids.add(identifier)
        name = row.get("name")
        description = row.get("description")
        if not isinstance(name, str) or not name.strip() or not isinstance(description, str) or not description.strip():
            raise ValueError("Missing agent skill description")
        repo = row.get("sourceRepository")
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ValueError("Invalid agent skill source repository")
        expected = "https://github.com/" + repo
        if row.get("sourceUrl") != expected:
            raise ValueError("Untrusted agent skill source URL")
        url = urlsplit(expected)
        if url.scheme != "https" or url.hostname != "github.com":
            raise ValueError("Invalid agent skill source domain")
        # The exact SKILL.md path is independently confirmed on a pinned
        # upstream revision, rather than delegating review to a mutable repo root.
        source_commit, source_path = row.get("sourceCommit"), row.get("sourcePath")
        if not isinstance(source_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
            raise ValueError("Agent skill source must pin an exact Git commit")
        if not isinstance(source_path, str) or not re.fullmatch(
                r"(?:[a-zA-Z0-9_.-]+/)+SKILL[.]md", source_path
        ) or any(segment in ("", ".", "..") for segment in source_path.split("/")):
            raise ValueError("Agent skill source must pin a safe SKILL.md path")
        domains, tags, languages = (row.get("domains"), row.get("tags"), row.get("languages"))
        if not isinstance(domains, list) or not domains or any(x not in VALID_DOMAINS for x in domains) or len(domains) != len(set(domains)):
            raise ValueError("Invalid agent skill domains")
        if not isinstance(tags, list) or not tags or any(not isinstance(x, str) or not re.fullmatch(r"[a-z0-9-]+", x) for x in tags):
            raise ValueError("Invalid agent skill discovery tags")
        if len(tags) != len(set(tags)):
            raise ValueError("Duplicate agent skill discovery tags")
        if not isinstance(languages, list) or any(not isinstance(x, str) or not x.strip() for x in languages):
            raise ValueError("Invalid agent skill languages")
        if (row.get("verification") != "upstream-repository-exists"
                or row.get("integrationEligible") is not False
                or row.get("skillCodeReviewed") is not False):
            raise ValueError("Unreviewed skill cannot be automatically installed or executed")
    return data


def recommend_skills(
    terms: set[str], domains: set[str], *, language: str = "", limit: int = 2,
) -> list[dict]:
    """Rank skill *references* by declared domain and concrete repo labels.

    Never treat broad README prose as verified compatibility and never return
    shell installers or instructions for agent execution.
    """
    source = load_skills()
    if limit < 1:
        return []
    words = set().union(*(word_set(term) for term in terms))
    selected = []
    for item in source["skills"]:
        matched_domains = sorted(set(item["domains"]) & domains)
        matched_tags = sorted(set(item["tags"]) & words)
        if not matched_domains or not matched_tags:
            continue
        languages = {x.casefold() for x in item["languages"]}
        if languages and language.casefold() not in languages:
            # An explicit relevant framework term is stronger evidence than
            # GitHub's single primary language, but general domain is not.
            explicit = {"react", "nextjs", "remotion"} & set(matched_tags)
            if not explicit:
                continue
        score = 8 * len(matched_domains) + 5 * len(matched_tags)
        selected.append((score, item, matched_domains, matched_tags))
    selected.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [{
        "id": item["id"],
        "name": item["name"],
        "sourceRepository": item["sourceRepository"],
        "url": item["sourceUrl"],
        "skillFileUrl": (
            item["sourceUrl"] + "/blob/" + item["sourceCommit"] + "/" + item["sourcePath"]
        ),
        "sourceCommit": item["sourceCommit"],
        "sourcePath": item["sourcePath"],
        "directoryUrl": SKILL_ISSUE_URL,
        "summary": item["description"],
        "selectionScore": score,
        "why": {"domains": domain_hits, "tags": tag_hits},
        "reviewRequired": True,
        "integrationEligible": False,
        "installCommand": None,
    } for score, item, domain_hits, tag_hits in selected[:limit]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Search local curated skills by topic")
    parser.add_argument("--domain", action="append", choices=sorted(VALID_DOMAINS), default=[])
    parser.add_argument("--language", default="")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.top < 1 or args.top > 20:
        parser.error("--top must be between 1 and 20")
    catalog = load_skills()
    matched = recommend_skills(word_set(args.query), set(args.domain), language=args.language, limit=args.top)
    output = {
        "directory": SKILL_ISSUE_URL, "discoveryOnly": True,
        "totalCuratedSkills": len(catalog["skills"]), "recommendations": matched,
        "automaticInstallation": False,
    }
    if args.as_json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Skill Issue: {SKILL_ISSUE_URL} | {len(catalog['skills'])} reviewed source links (skill code not audited)")
        for item in matched:
            print(f"- {item['name']}: {item['url']} | review before use")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
