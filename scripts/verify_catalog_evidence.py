#!/usr/bin/env python3
"""Evidence-based, read-only by default triage for uncertain catalog metadata.

GitHub is the only remote source. A verified root licence can be applied with
--apply, but deployment configuration files are never proof that a project
is fully self-hostable.
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import refresh_github_metadata as github

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN_LICENSE = (None, "", "NOASSERTION")
MAX_FILE_BYTES = 128 * 1024
LICENSE_STEMS = frozenset({"license", "licence", "copying"})
COMPOSE_FILES = frozenset({
    "compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.yaml",
})
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")



def root_files(payload):
    if not isinstance(payload, list):
        raise ValueError("GitHub root directory listing unavailable")
    files = {}
    for item in payload:
        if not isinstance(item, dict) or item.get("type") != "file":
            continue
        name = item.get("name")
        path = item.get("path")
        if (isinstance(name, str) and isinstance(path, str)
                and path == name and "/" not in path and len(path) < 150):
            files[name.lower()] = item
    return files


def is_license_file(name):
    stem = re.split(r"[._-]", name.lower(), maxsplit=1)[0]
    return stem in LICENSE_STEMS


def content_with_sha(payload):
    if not isinstance(payload, dict) or payload.get("type") not in (None, "file"):
        return None, None
    size = payload.get("size")
    if type(size) is int and (size < 0 or size > MAX_FILE_BYTES):
        return None, None
    sha = payload.get("sha")
    if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{40}", sha):
        return None, None
    encoded = payload.get("content")
    if not isinstance(encoded, str):
        return None, None
    try:
        raw = base64.b64decode(encoded, validate=False)
        if len(raw) > MAX_FILE_BYTES:
            return None, None
        actual_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if actual_sha != sha:
            return None, None
        text = raw.decode("utf-8")
    except (UnicodeError, ValueError, TypeError):
        return None, None
    return text, sha


def blob_evidence(name, sha):
    # Immutable blob reference, not a mutable default-branch page.
    return "https://api.github.com/repos/" + name + "/git/blobs/" + sha


def inspect_entry(entry, fetch_repo=github.fetch, fetch_content=github.fetch_contents, token=None):
    name = entry.get("repo")
    if not isinstance(name, str) or not REPO_RE.fullmatch(name):
        raise ValueError("Invalid repository identifier")
    gh = entry.get("github") or {}
    if not isinstance(gh, dict):
        raise ValueError("Invalid catalog GitHub metadata")
    raw = fetch_repo(name, token=token)
    if not isinstance(raw, dict):
        raise ValueError("GitHub repository response is not an object")
    expected_id = entry.get("githubRepositoryId")
    actual_id = raw.get("id")
    if type(actual_id) is not int or actual_id <= 0:
        raise ValueError("GitHub repository ID is unavailable")
    if expected_id is not None and expected_id != actual_id:
        raise ValueError("GitHub repository ID mismatch; possible transferred or reused slug")
    branch = raw.get("default_branch")
    if not isinstance(branch, str) or not branch:
        raise ValueError("GitHub default branch is unavailable")
    files = root_files(fetch_content(name, ref=branch, token=token))
    item = {
        "repository": name,
        "repositoryId": actual_id,
        "defaultBranch": branch,
        "license": {"status": "unverified", "value": None, "evidence": []},
        "hosting": {"status": "unverified", "evidence": []},
        "proposedLicense": None,
    }
    api_license = raw.get("license")
    api_spdx = api_license.get("spdx_id") if isinstance(api_license, dict) else None
    if api_spdx and api_spdx != "NOASSERTION":
        item["license"]["evidence"].append({
            "method": "github-repository-spdx", "value": api_spdx,
            "url": "https://api.github.com/repos/" + name + "/license",
        })
    strong = set()
    scoped = False
    for filename, file in sorted(files.items()):
        if not is_license_file(filename):
            continue
        if type(file.get("size")) is int and file["size"] > MAX_FILE_BYTES:
            continue
        payload = fetch_content(name, path=file["path"], ref=branch, token=token)
        content, sha = content_with_sha(payload)
        if content is None:
            continue
        if github.root_license_scope_warning(content):
            scoped = True
            item["license"]["evidence"].append({
                "method": "root-license-scope-warning", "value": "partial-or-mixed",
                "path": file["path"], "blobSha": sha, "url": blob_evidence(name, sha),
            })
            continue
        detected = github.strict_root_license(content)
        if detected:
            strong.add(detected)
            item["license"]["evidence"].append({
                "method": "root-license-signature", "value": detected,
                "path": file["path"], "blobSha": sha, "url": blob_evidence(name, sha),
            })
    if scoped:
        item["license"]["status"] = "scoped-licensing-review"
    elif len(strong) == 1:
        verified = next(iter(strong))
        if api_spdx not in (None, "", "NOASSERTION", verified):
            item["license"]["status"] = "conflict"
        else:
            item["license"]["status"] = "verified-root-file"
            item["license"]["value"] = verified
            # A previous restrictive/partial/external-terms review is not
            # invalidated by finding one apparently permissive root file.
            if (gh.get("license") in UNKNOWN_LICENSE
                    and entry.get("licenseStatus") not in ("partial", "custom-restrictive", "external-terms")
                    and not raw.get("archived") and not raw.get("disabled")):
                item["proposedLicense"] = verified
    elif len(strong) > 1:
        item["license"]["status"] = "conflict"
    elif api_spdx not in (None, "", "NOASSERTION"):
        item["license"]["status"] = "github-claim-only"
        item["license"]["value"] = api_spdx

    # Never infer selfHosted=True from root Docker files; report candidates
    # for human examination instead.
    for filename in COMPOSE_FILES:
        file = files.get(filename)
        if not file or (type(file.get("size")) is int and file["size"] > MAX_FILE_BYTES):
            continue
        payload = fetch_content(name, path=file["path"], ref=branch, token=token)
        content, sha = content_with_sha(payload)
        if content and re.search(r"(?m)^\s*services:\s*(?:#.*)?$", content) and re.search(
                r"(?m)^\s+(?:image|build):\s*\S", content):
            item["hosting"]["evidence"].append({
                "method": "compose-root-file", "path": file["path"],
                "blobSha": sha, "url": blob_evidence(name, sha),
            })
    if item["hosting"]["evidence"]:
        item["hosting"]["status"] = "deployment-file-present-review-required"
    return item


def requires_review(row):
    """Watch missing facts and inactive projects, without gating discovery."""
    gh = row.get("github")
    if not isinstance(gh, dict) or not gh:
        return True
    return (bool(gh.get("archived") or gh.get("disabled"))
            or gh.get("license") in UNKNOWN_LICENSE
            or type(row.get("selfHosted")) is not bool)


def select_entries(repos, limit, batch_index, selected_names):
    uncertain = [row for row in repos if requires_review(row)]
    if selected_names:
        by_name = {row.get("repo"): row for row in repos}
        missing = sorted(set(selected_names) - set(by_name))
        if missing:
            raise ValueError("Repository not present in catalog: " + ", ".join(missing))
        rows = [by_name[name] for name in selected_names]
    else:
        rows = sorted(uncertain, key=lambda x: x["repo"].lower())
        chunks = max(1, (len(rows) + limit - 1) // limit)
        if batch_index < 0 or batch_index >= chunks:
            raise ValueError("batch-index must be 0.." + str(chunks - 1))
        rows = rows[batch_index * limit:(batch_index + 1) * limit]
    return rows, len(uncertain)


def audit(repos, entries, total_uncertain, fetch_repo=github.fetch,
          fetch_content=github.fetch_contents, token=None, apply=False):
    results, errors, updates = [], [], []
    by_name = {x.get("repo"): x for x in repos}
    for entry in entries:
        try:
            result = inspect_entry(entry, fetch_repo, fetch_content, token)
            results.append(result)
            license_value = result.get("proposedLicense")
            if apply and license_value:
                current = by_name[result["repository"]]
                current["github"]["license"] = license_value
                current["licenseEvidence"] = "verified-file"
                current.pop("licenseStatus", None)
                updates.append({"repository": result["repository"], "license": license_value,
                                "evidence": next(x["url"] for x in result["license"]["evidence"]
                                                 if x["method"] == "root-license-signature")})
        except Exception as exc:
            # API failures and identity conflicts are never interpreted as
            # 'not licensed' or 'not self-hostable'.
            errors.append({"repository": entry.get("repo"), "error": str(exc)[:240]})
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "catalogSize": len(repos),
        "uncertainEntries": total_uncertain,
        "selected": len(entries),
        "inspected": len(results),
        "counts": {
            "verifiedRootLicenses": sum(x["license"]["status"] == "verified-root-file" for x in results),
            "scopedLicenses": sum(x["license"]["status"] == "scoped-licensing-review" for x in results),
            "githubClaimsOnly": sum(x["license"]["status"] == "github-claim-only" for x in results),
            "hostingCandidates": sum(bool(x["hosting"]["evidence"]) for x in results),
            "proposedLicenseUpdates": sum(bool(x["proposedLicense"]) for x in results),
            "appliedUpdates": len(updates),
            "errors": len(errors),
        },
        "results": results,
        "updates": updates,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description="Verify evidence for uncertain Star List metadata.")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--limit", type=int, default=15)
    parser.add_argument("--batch-index", type=int, default=0)
    parser.add_argument("--repo", action="append", default=[], help="Specific exact owner/repo (repeatable)")
    parser.add_argument("--report-out", type=Path, help="Save JSON audit report")
    parser.add_argument("--apply", action="store_true", help="Write verified root licences to catalog")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 100:
        parser.error("--limit must be between 1 and 100")
    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    repos = data["repositories"]
    try:
        entries, total_uncertain = select_entries(repos, args.limit, args.batch_index, args.repo)
    except ValueError as exc:
        parser.error(str(exc))
    result = audit(repos, entries, total_uncertain, token=os.environ.get("GITHUB_TOKEN"),
                   apply=args.apply)
    result["batchIndex"] = args.batch_index
    result["wroteCatalog"] = bool(args.apply and result["updates"] and not result["errors"])
    if result["wroteCatalog"]:
        # An interrupted process must never leave a partially written catalog.
        import tempfile
        with tempfile.NamedTemporaryFile("w", dir=args.catalog.parent, prefix=".catalog-evidence-",
                                         suffix=".tmp", encoding="utf-8", delete=False) as handle:
            handle.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            temporary_path = Path(handle.name)
        temporary_path.replace(args.catalog)
    elif args.apply and result["errors"]:
        # Fail closed; avoid partial catalog writes if even one source failed.
        result["counts"]["appliedUpdates"] = 0
        result["updates"] = []
        result["wroteCatalog"] = False
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.report_out:
        args.report_out.parent.mkdir(parents=True, exist_ok=True)
        args.report_out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    if result["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
