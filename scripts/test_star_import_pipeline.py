#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path

from star_import_pipeline import (
    build_report,
    classify_candidate,
    integrate_catalog,
    load_imports,
    normalize_repo_identity,
    partition_candidates,
    write_catalog_if_valid,
)

# Normalization
assert normalize_repo_identity("OpenAI/Codex") == ("openai/codex", "OpenAI/Codex")
assert normalize_repo_identity("https://github.com/OpenAI/Codex.git/") == ("openai/codex", "OpenAI/Codex")
assert normalize_repo_identity("https://github.com/OpenAI/Codex?tab=readme#top") == ("openai/codex", "OpenAI/Codex")
for bad in ("", "codex", "a/b/c", "https://gitlab.com/a/b", "https://github.com/a/b/issues/1"):
    try:
        normalize_repo_identity(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"expected invalid identity: {bad}")

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    p1 = root / "one.json"
    p2 = root / "two.json"
    p1.write_text(json.dumps({"repositories": ["OpenAI/Codex", "bad"]}))
    p2.write_text(json.dumps({"repositories": ["openai/codex", "Anthropic/Claude-Code"]}))
    records, malformed = load_imports([p1, p2])
    assert len(records) == 3
    assert malformed == [{"source": str(p1), "value": "bad", "error": "invalid GitHub repository identity"}]

    catalog = {"repositories": [{"repo": "OPENAI/CODEX", "score": 9.5}]}
    partition = partition_candidates(records, catalog)
    assert [x["repo"] for x in partition["already_cataloged"]] == ["OpenAI/Codex"]
    assert [x["repo"] for x in partition["new"]] == ["Anthropic/Claude-Code"]
    assert len(partition["duplicate_import"]) == 1
    assert partition["duplicate_import"][0]["sources"] == [str(p1), str(p2)]

    candidate = partition["new"][0]
    classified = classify_candidate(candidate)
    assert classified["status"] == "needs_review"
    assert "catalogEntry" not in classified

    report = build_report(partition, malformed, [str(p1), str(p2)])
    assert report["summary"] == {
        "rawRecords": 3,
        "uniqueNormalized": 2,
        "duplicateImports": 1,
        "alreadyCataloged": 1,
        "newCandidates": 1,
        "needsReview": 1,
        "malformed": 1,
    }

# Integration preserves existing records, sorts only additions deterministically, and is idempotent.
base = {"schemaVersion": 1, "repositories": [{"repo": "z/existing", "score": 8.0}]}
accepted = [
    {"repo": "b/new", "score": 8.0, "tier": "specialized"},
    {"repo": "A/new", "score": 8.0, "tier": "specialized"},
]
once = integrate_catalog(base, accepted)
twice = integrate_catalog(once, accepted)
assert base["repositories"] == [{"repo": "z/existing", "score": 8.0}]
assert [x["repo"] for x in once["repositories"]] == ["z/existing", "A/new", "b/new"]
assert once == twice

# Failed validation never replaces the authoritative catalog.
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    catalog_path = root / "catalog.json"
    original = json.dumps(base, indent=2) + "\n"
    catalog_path.write_text(original)
    ok, output = write_catalog_if_valid(once, catalog_path, validator=lambda _: (False, "boom"))
    assert ok is False
    assert "boom" in output
    assert catalog_path.read_text() == original

print("OK: star import pipeline tests passed")
