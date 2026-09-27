#!/usr/bin/env python3
"""Deterministic ingestion for screenshot-derived GitHub star manifests."""
from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def normalize_repo_identity(value: str) -> tuple[str, str]:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("invalid GitHub repository identity")
    raw = value.strip()
    if "://" in raw:
        parsed = urlsplit(raw)
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {"github.com", "www.github.com"}:
            raise ValueError("invalid GitHub repository identity")
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) != 2:
            raise ValueError("invalid GitHub repository identity")
        owner, name = parts
    else:
        parts = raw.split("/")
        if len(parts) != 2:
            raise ValueError("invalid GitHub repository identity")
        owner, name = parts
    name = name[:-4] if name.lower().endswith(".git") else name
    if not owner or not name or any(c.isspace() for c in owner + name):
        raise ValueError("invalid GitHub repository identity")
    display = f"{owner}/{name}"
    return display.lower(), display


def load_imports(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    records, malformed = [], []
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            malformed.append({"source": str(path), "value": None, "error": str(exc)})
            continue
        values = payload.get("repositories") if isinstance(payload, dict) else None
        if not isinstance(values, list):
            malformed.append({"source": str(path), "value": None, "error": "repositories must be a list"})
            continue
        for value in values:
            try:
                key, display = normalize_repo_identity(value)
            except (ValueError, TypeError):
                malformed.append({"source": str(path), "value": value, "error": "invalid GitHub repository identity"})
                continue
            records.append({"key": key, "repo": display, "source": str(path)})
    return records, malformed


def partition_candidates(records: list[dict], catalog: dict) -> dict:
    catalog_keys = {}
    for entry in catalog.get("repositories", []):
        try:
            key, _ = normalize_repo_identity(entry.get("repo", ""))
        except ValueError:
            continue
        catalog_keys[key] = entry.get("repo")
    first, sources, duplicate_keys = {}, {}, []
    for record in records:
        key = record["key"]
        sources.setdefault(key, [])
        if record["source"] not in sources[key]:
            sources[key].append(record["source"])
        if key not in first:
            first[key] = record
        elif key not in duplicate_keys:
            duplicate_keys.append(key)
    new, existing = [], []
    for key, record in first.items():
        item = {"key": key, "repo": record["repo"], "sources": sources[key]}
        (existing if key in catalog_keys else new).append(item)
    duplicates = [{"key": key, "repo": first[key]["repo"], "sources": sources[key]} for key in duplicate_keys]
    return {"raw_records": len(records), "new": new, "already_cataloged": existing, "duplicate_import": duplicates}


def classify_candidate(candidate: dict, metadata: dict | None = None) -> dict:
    result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])), "status": "needs_review"}
    if metadata and isinstance(metadata.get("catalogEntry"), dict):
        entry = copy.deepcopy(metadata["catalogEntry"])
        if entry.get("repo", "").lower() == candidate["key"]:
            result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])), "status": "accepted", "catalogEntry": entry}
    return result


def build_report(partition: dict, malformed: list[dict], import_files: list[str]) -> dict:
    classified = [classify_candidate(c) for c in partition["new"]]
    needs_review = [x for x in classified if x["status"] == "needs_review"]
    unique = len(partition["new"]) + len(partition["already_cataloged"])
    return {"importFiles": list(import_files), "summary": {"rawRecords": partition.get("raw_records", unique), "uniqueNormalized": unique, "duplicateImports": len(partition["duplicate_import"]), "alreadyCataloged": len(partition["already_cataloged"]), "newCandidates": len(partition["new"]), "needsReview": len(needs_review), "malformed": len(malformed)}, "alreadyCataloged": partition["already_cataloged"], "duplicateImports": partition["duplicate_import"], "newCandidates": classified, "malformed": malformed}


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = ["# GitHub Star Import Report", "", f"- Raw records: {s['rawRecords']}", f"- Unique normalized repositories: {s['uniqueNormalized']}", f"- Duplicate imports: {s['duplicateImports']}", f"- Already cataloged: {s['alreadyCataloged']}", f"- New candidates: {s['newCandidates']}", f"- Needs review: {s['needsReview']}", f"- Malformed: {s['malformed']}", "", "## New candidates", ""]
    lines.extend(f"- `{x['repo']}` — {x['status']}" for x in report["newCandidates"])
    return "\n".join(lines) + "\n"


def integrate_catalog(catalog: dict, accepted: list[dict]) -> dict:
    result = copy.deepcopy(catalog)
    entries = result.setdefault("repositories", [])
    seen = {str(x.get("repo", "")).lower() for x in entries}
    additions = []
    for entry in accepted:
        key = str(entry.get("repo", "")).lower()
        if key and key not in seen:
            additions.append(copy.deepcopy(entry))
            seen.add(key)
    entries.extend(sorted(additions, key=lambda x: x["repo"].lower()))
    return result


def validate_candidate_catalog(candidate: dict, root: Path) -> tuple[bool, str]:
    root = Path(root).resolve()
    with tempfile.TemporaryDirectory(prefix="star-list-validate-") as td:
        sandbox = Path(td) / "repo"
        shutil.copytree(root, sandbox, ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__", "*.pyc"))
        (sandbox / "catalog.json").write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        output = []
        for command in (["python", "scripts/validate_catalog.py"], ["python", "scripts/test_catalog_quality.py"]):
            proc = subprocess.run(command, cwd=sandbox, text=True, capture_output=True)
            output.append(proc.stdout + proc.stderr)
            if proc.returncode:
                return False, "".join(output)
        return True, "".join(output)


def write_catalog_if_valid(candidate: dict, catalog_path: Path, validator=None) -> tuple[bool, str]:
    catalog_path = Path(catalog_path)
    validator = validator or (lambda data: validate_candidate_catalog(data, catalog_path.parent))
    ok, output = validator(candidate)
    if not ok:
        return False, output
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{catalog_path.name}.", dir=catalog_path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(candidate, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp_name, catalog_path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return True, output


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("imports", nargs="*", type=Path)
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    paths = args.imports or sorted((ROOT / "imports").glob("github-stars-*.json"))
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    records, malformed = load_imports(paths)
    partition = partition_candidates(records, catalog)
    report = build_report(partition, malformed, [str(p) for p in paths])
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(payload, encoding="utf-8")
    if args.report_md:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(render_markdown(report), encoding="utf-8")
    if args.write:
        accepted = [x["catalogEntry"] for x in report["newCandidates"] if x["status"] == "accepted"]
        candidate = integrate_catalog(catalog, accepted)
        ok, output = write_catalog_if_valid(candidate, args.catalog)
        if not ok:
            print(output)
            return 1
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
