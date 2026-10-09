#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from star_import_pipeline import (
    build_report,
    classify_candidate,
    integrate_catalog,
    load_imports,
    load_reviewed_metadata,
    normalize_repo_identity,
    partition_candidates,
    write_catalog_if_valid,
)

SCRIPT = Path(__file__).with_name("star_import_pipeline.py")

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
        "accepted": 0,
        "needsReview": 1,
        "malformed": 1,
        "malformedMetadata": 0,
    }

# A raw GitHub snapshot cannot approve itself. Approval is explicit and tied to GitHub evidence.
verified_github = {
    "stars": 10, "forks": 2, "openIssues": 0, "archived": False, "disabled": False,
    "defaultBranch": "main", "license": "MIT", "pushedAt": "2026-10-09T00:00:00Z",
}
new_entry = {
    "repo": "Anthropic/Claude-Code", "score": 8.0, "tier": "specialized",
    "category": "Coding agents", "domain": "software_engineering",
    "resourceLevel": "low", "integrationComplexity": "medium",
    "selfHosted": True, "github": verified_github,
}
reviewed = {"repo": "Anthropic/Claude-Code", "github": verified_github,
            "reviewed": True, "catalogEntry": new_entry}
assert classify_candidate(candidate, reviewed)["status"] == "accepted"
assert classify_candidate(candidate, {**reviewed, "reviewed": False})["status"] == "needs_review"
assert classify_candidate(candidate, {**reviewed, "github": {**verified_github, "stars": 999}})["status"] == "needs_review"
assert classify_candidate(candidate, {**reviewed, "repo": "other/repo"})["status"] == "needs_review"
assert classify_candidate(candidate, {**reviewed, "catalogEntry": {**new_entry, "repo": "other/repo"}})["status"] == "needs_review"
review_report = build_report(partition, malformed, ["batch"], {candidate["key"]: reviewed}, ["metadata"])
assert review_report["summary"]["accepted"] == 1
assert review_report["summary"]["needsReview"] == 0
assert review_report["newCandidates"][0]["catalogEntry"] == new_entry

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    a, b = root / "reviewed.json", root / "conflict.json"
    a.write_text(json.dumps({"repositories": [reviewed]}))
    b.write_text(json.dumps({"repositories": [{**reviewed, "reviewed": False}]}))
    md, errors = load_reviewed_metadata([a])
    assert not errors and md["anthropic/claude-code"] == reviewed
    _, errors = load_reviewed_metadata([a, b])
    assert len(errors) == 1 and "conflicting" in errors[0]["error"]
    a.write_text('{"repositories": [null, "bad"]}')
    _, errors = load_reviewed_metadata([a])
    assert len(errors) == 2

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

# CLI is dry-run by default, emits requested reports, and leaves catalog unchanged.
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    import_path = root / "stars.json"
    catalog_path = root / "catalog.json"
    report_json = root / "report.json"
    report_md = root / "report.md"
    import_path.write_text(json.dumps({"repositories": ["OpenAI/Codex", "New/Repo"]}))
    catalog_payload = {"schemaVersion": 1, "repositories": [{"repo": "openai/codex"}]}
    original = json.dumps(catalog_payload) + "\n"
    catalog_path.write_text(original)
    proc = subprocess.run([
        sys.executable, str(SCRIPT), str(import_path), "--catalog", str(catalog_path),
        "--report-json", str(report_json), "--report-md", str(report_md),
    ], text=True, capture_output=True)
    assert proc.returncode == 0, proc.stderr
    assert catalog_path.read_text() == original
    cli_report = json.loads(report_json.read_text())
    assert cli_report["summary"]["alreadyCataloged"] == 1
    assert cli_report["summary"]["newCandidates"] == 1
    assert "`New/Repo` — needs_review" in report_md.read_text()

# End-to-end CLI: importing needs human approval, accepts reviewed data, and stays idempotent.
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    scripts = root / "scripts"
    scripts.mkdir()
    for file_name in ("validate_catalog.py", "test_catalog_quality.py", "audit_catalog_quality.py"):
        import shutil
        shutil.copy2(Path(__file__).with_name(file_name), scripts / file_name)
    baseline = {**new_entry, "repo": "Existing/Project"}
    proposed = {**new_entry, "repo": "New/Project"}
    import_path, metadata_path, catalog_path = (
        root / "stars.json", root / "metadata.json", root / "catalog.json"
    )
    import_path.write_text(json.dumps({"repositories": ["New/Project"]}))
    catalog_path.write_text(json.dumps({"schemaVersion": 1, "repositories": [baseline]}))
    metadata_path.write_text(json.dumps({"repositories": [
        {"repo": "New/Project", "github": verified_github, "catalogEntry": proposed}
    ]}))
    args = [sys.executable, str(SCRIPT), str(import_path), "--catalog", str(catalog_path),
            "--metadata", str(metadata_path)]
    before = catalog_path.read_text()
    raw = subprocess.run(args + ["--write"], text=True, capture_output=True)
    assert raw.returncode == 2 and "no reviewed entries" in raw.stdout
    assert catalog_path.read_text() == before
    metadata_path.write_text(json.dumps({"repositories": [
        {"repo": "New/Project", "github": verified_github, "catalogEntry": proposed, "reviewed": True}
    ]}))
    success = subprocess.run(args + ["--write"], text=True, capture_output=True)
    assert success.returncode == 0, success.stdout + success.stderr
    merged = json.loads(catalog_path.read_text())
    assert [x["repo"] for x in merged["repositories"]] == ["Existing/Project", "New/Project"]
    new_before_repeat = catalog_path.read_text()
    repeat = subprocess.run(args + ["--write"], text=True, capture_output=True)
    assert repeat.returncode == 0 and catalog_path.read_text() == new_before_repeat
    metadata_path.write_text('{"repositories": [null]}')
    bad = subprocess.run(args + ["--write"], text=True, capture_output=True)
    assert bad.returncode == 2 and catalog_path.read_text() == new_before_repeat

print("OK: star import pipeline tests passed")
