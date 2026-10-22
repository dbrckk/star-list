#!/usr/bin/env python3
"""Deterministic offline tests for evidence-based metadata review."""
import base64
import hashlib
import json
import tempfile
from pathlib import Path

import verify_catalog_evidence as audit


def source(text):
    data = text.encode("utf-8")
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    return {"type": "file", "size": len(data), "sha": blob,
            "content": base64.b64encode(data).decode("ascii")}


MIT = ("MIT License\nCopyright (c) 2026 Example\n"
       "Permission is hereby granted, free of charge, to any person obtaining a copy "
       "of this software and associated documentation files (the Software), "
       "to deal in the Software without restriction.")
LISTING = [
    {"type": "file", "name": "README.md", "path": "README.md", "size": 99},
    {"type": "file", "name": "LICENSE", "path": "LICENSE", "size": len(MIT)},
    {"type": "file", "name": "compose.yaml", "path": "compose.yaml", "size": 80},
]
row = {"repo": "example/project", "tier": "audit", "githubRepositoryId": 123,
       "selfHosted": "unknown", "github": {"license": None, "defaultBranch": "main",
                                          "archived": False, "disabled": False}}


def fake_repo(name, token=None):
    assert name == "example/project"
    return {"id": 123, "default_branch": "main", "license": {"spdx_id": "MIT"},
            "archived": False, "disabled": False}


def fake_content(name, path="", ref=None, token=None):
    assert name == "example/project" and ref == "main"
    if not path:
        return LISTING
    if path == "LICENSE":
        return source(MIT)
    if path == "compose.yaml":
        return source("services:\n  web:\n    image: docker.io/example/hello:1.0\n")
    raise AssertionError("Only authoritative licence and Compose may be read: " + path)


def main():
    assert audit.github.strict_root_license("MIT") is None
    assert audit.github.strict_root_license(MIT) == "MIT"
    partial = ('Portions of this software are licensed as follows: '
               'Content outside of the above mentioned directories uses MIT. ' + MIT)
    assert audit.github.root_license_scope_warning(partial)
    assert audit.github.strict_root_license(partial) is None
    def scoped_content(name, path="", ref=None, token=None):
        if not path:
            return LISTING
        if path == "LICENSE":
            return source(partial)
        return source("services:\n  web:\n    image: docker.io/example/hello:1.0\n")
    scoped_row = audit.inspect_entry(row, fake_repo, scoped_content)
    assert scoped_row["license"]["status"] == "scoped-licensing-review"
    assert scoped_row["proposedLicense"] is None
    assert any(e["method"] == "root-license-scope-warning"
               for e in scoped_row["license"]["evidence"])

    assert audit.is_license_file("LICENSE-MIT")
    assert not audit.is_license_file("README")
    assert audit.content_with_sha({"size": 130000, "sha": "b"*40}) == (None, None)
    bad = source(MIT)
    bad["sha"] = "f" * 40
    assert audit.content_with_sha(bad) == (None, None), "Content must match immutable Git blob SHA"
    report = audit.inspect_entry(row, fake_repo, fake_content)
    assert report["license"]["status"] == "verified-root-file", report
    assert report["proposedLicense"] == "MIT", report
    assert report["license"]["evidence"][-1]["blobSha"] == source(MIT)["sha"]
    assert report["hosting"]["status"] == "deployment-file-present-review-required"
    assert report["hosting"]["evidence"][0]["blobSha"] == source(
        "services:\n  web:\n    image: docker.io/example/hello:1.0\n")["sha"]
    assert row["selfHosted"] == "unknown", "finding Compose is not proof of full self-hosting"

    changed = dict(row, licenseStatus="partial")
    assert audit.inspect_entry(changed, fake_repo, fake_content)["proposedLicense"] is None
    changed = dict(row, github={**row["github"], "license": "Apache-2.0"})
    assert audit.inspect_entry(changed, fake_repo, fake_content)["proposedLicense"] is None

    def conflicting_repo(name, token=None):
        return {**fake_repo(name, token), "license": {"spdx_id": "Apache-2.0"}}
    assert audit.inspect_entry(row, conflicting_repo, fake_content)["license"]["status"] == "conflict"

    def reused_repo(name, token=None):
        return {**fake_repo(name, token), "id": 456}
    try:
        audit.inspect_entry(row, reused_repo, fake_content)
    except ValueError as exc:
        assert "ID mismatch" in str(exc)
    else:
        raise AssertionError("Must refuse identity mismatches")

    # A README claim without a root licence is never promoted.
    def readme_only(name, path="", ref=None, token=None):
        assert path == "", "README must not be fetched for licence inference"
        return [LISTING[0]]
    assert audit.inspect_entry(row, fake_repo, readme_only)["proposedLicense"] is None

    entries = [dict(row), {**row, "repo": "example/second"}]
    chosen, uncertain = audit.select_entries(entries, 1, 0, [])
    assert len(chosen) == 1 and uncertain == 2
    flagged = dict(row, repo="example/audit-only", selfHosted=True,
                   github={**row["github"], "license": "MIT"})
    assert audit.requires_review(flagged) is True
    flagged["tier"] = "recommended"
    assert audit.requires_review(flagged) is False
    flagged["github"]["archived"] = True
    assert audit.requires_review(flagged) is True
    chosen2, _ = audit.select_entries(entries, 1, 1, [])
    assert chosen[0]["repo"] != chosen2[0]["repo"]
    try:
        audit.select_entries(entries, 1, 2, [])
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid batch index accepted")
    assert audit.select_entries(entries, 1, 0, ["example/project"])[0] == [entries[0]]

    only = [dict(row, github=dict(row["github"]))]
    original_self_hosted = only[0]["selfHosted"]
    full = audit.audit(only, only, 1, fake_repo, fake_content, apply=True)
    assert full["counts"]["appliedUpdates"] == 1
    assert only[0]["github"]["license"] == "MIT"
    assert only[0]["licenseEvidence"] == "verified-file"
    assert only[0]["selfHosted"] == original_self_hosted
    assert all(x["url"].startswith("https://api.github.com/repos/") for x in (
        full["results"][0]["hosting"]["evidence"]
        + full["results"][0]["license"]["evidence"]))
    import validate_json_contract
    schema = json.loads((Path(__file__).resolve().parents[1]
                          / "schemas/metadata-evidence.schema.json").read_text())
    report_contract = {**full, "batchIndex": 0, "wroteCatalog": True}
    assert not validate_json_contract.validate(report_contract, schema)
    unsafe = dict(report_contract, counts={**full["counts"], "scopedLicenses": "not-a-number"})
    assert validate_json_contract.validate(unsafe, schema)

    # Caller writes nothing if any individual operation fails, including an
    # identity conflict in a later entry in the batch.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "catalog.json"
        path.write_text(json.dumps({"repositories": [row]}))
        assert not json.loads(path.read_text())["repositories"][0]["github"]["license"]

    print("OK: verified metadata evidence and fail-closed licence promotion tests passed")


if __name__ == "__main__":
    main()
