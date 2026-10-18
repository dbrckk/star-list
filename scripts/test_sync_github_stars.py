#!/usr/bin/env python3
"""Offline regression tests for public GitHub Stars synchronization."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request

SCRIPT = Path(__file__).with_name("sync_github_stars.py")
spec = importlib.util.spec_from_file_location("sync_github_stars", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def star(name, **overrides):
    item = {
        "full_name": name,
        "stargazers_count": 50,
        "language": "Python",
        "license": {"spdx_id": "MIT"},
        "archived": False,
        "disabled": False,
        "pushed_at": "2026-10-01T12:00:00Z",
    }
    item.update(overrides)
    return item


class Response:
    def __init__(self, payload, link=""):
        self.body = json.dumps(payload).encode("utf-8")
        self.headers = {"Link": link}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self.body


calls = []
def two_page_opener(request, timeout=20):
    calls.append(request)
    assert timeout == 20
    assert request.get_header("Authorization") == "Bearer testing-token"
    query = parse_qs(urlsplit(request.full_url).query)
    assert query["per_page"] == ["100"]
    if query["page"] == ["1"]:
        return Response(
            [star("Known/Repo"), star("New/Beta", archived=True, license=None)],
            '<https://api.github.com/users/dbrckk/starred?per_page=100&page=2>; rel="next"',
        )
    if query["page"] == ["2"]:
        return Response([star("new/beta"), star("New/Alpha")])
    raise AssertionError("unexpected page")


# Authenticated GitHub API redirects must not forward the workflow's token
# to an attacker-controlled host, downgrade to HTTP, or change port.
auth = Request(
    "https://api.github.com/users/dbrckk/starred?page=1",
    headers={"Authorization": "Bearer private-github-token"},
)
redirect = mod.SameOriginGitHubRedirect()
for unsafe in (
    "https://example.com/steal",
    "https://api.github.com.attacker.example/steal",
    "http://api.github.com/users/dbrckk/starred",
    "https://api.github.com:444/users/dbrckk/starred",
    "https://name:pass@api.github.com/users/dbrckk/starred",
):
    try:
        redirect.redirect_request(auth, None, 302, "Found", {}, unsafe)
    except RuntimeError:
        pass
    else:
        raise AssertionError("GitHub API auth redirect escaped approved origin")
same_origin = redirect.redirect_request(
    auth, None, 302, "Found", {},
    "https://api.github.com/users/dbrckk/starred?page=2",
)
assert same_origin.get_header("Authorization") == "Bearer private-github-token"
assert mod.api_stars.__defaults__[2].__self__ is mod.SAFE_GITHUB_HTTP
# The admission stage must use the same restricted transport by default.
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
import admit_github_stars as admission
import sync_github_stars as imported_sync
assert admission.get_repo.__defaults__[1].__self__ is imported_sync.SAFE_GITHUB_HTTP

items, pages, duplicates = mod.api_stars(
    "dbrckk", token="testing-token", opener=two_page_opener
)
assert pages == 2 and duplicates == 1 and len(calls) == 2
assert [r["repo"] for r in items] == ["Known/Repo", "New/Alpha", "New/Beta"]
assert items[2]["archived"] is True and items[2]["license"] is None

stamp = datetime(2026, 10, 9, tzinfo=timezone.utc)
report = mod.build_report("dbrckk", items, {"known/repo"}, pages, duplicates, now=stamp)
assert report["summary"] == {
    "starred": 3, "alreadyCataloged": 1, "new": 2, "pages": 2,
    "duplicateApiItems": 1,
}
assert [r["repo"] for r in report["newRepositories"]] == ["New/Alpha", "New/Beta"]
rendered = mod.render_issue(report, limit=1)
assert mod.ISSUE_MARKER in rendered and "New/Alpha" in rendered
assert "New/Beta" not in rendered and "Showing 1 of 2" in rendered
assert "automatically admitted" in rendered.lower() and "not approval" in rendered.lower()
assert "All accessible starred" in mod.render_issue(
    mod.build_report("dbrckk", items, {x["repo"].lower() for x in items}, pages)
)
assert "https://github.com/New/Alpha" in rendered

try:
    mod.api_stars("bad/user", opener=two_page_opener)
    raise AssertionError("invalid username allowed")
except ValueError:
    pass
try:
    mod.normalize_repo("not-a-name")
    raise AssertionError("invalid repository name allowed")
except ValueError:
    pass

# Never report the first N pages as complete when the API signals more pages.
try:
    mod.api_stars("dbrckk", opener=lambda _req, timeout=20: Response(
        [star("X/Y")], '<https://api.github.com/users/dbrckk/starred?page=2>; rel="next"'
    ), max_pages=1)
    raise AssertionError("truncated pagination accepted")
except RuntimeError as exc:
    assert "max-pages" in str(exc)

# Invalid API shapes and identities fail closed.
for payload in ({"message": "rate limited"}, [None], [star("../../../evil")]):
    try:
        mod.api_stars("dbrckk", opener=lambda _req, timeout=20: Response(payload))
        raise AssertionError("invalid API payload accepted")
    except RuntimeError:
        pass

try:
    mod.api_stars("dbrckk", opener=lambda _req, timeout=20: Response(
        [], '<https://api.github.com/users/dbrckk/starred?page=2>; rel="next"'
    ))
    raise AssertionError("empty linked page accepted")
except RuntimeError:
    pass

attempts = []
def rate_limited(request, timeout=20):
    attempts.append(request)
    if len(attempts) == 1:
        raise HTTPError(request.full_url, 429, "Too Many Requests", {"Retry-After": "0"}, None)
    return Response([star("X/Y")])
assert len(mod.api_stars("dbrckk", opener=rate_limited, sleeper=lambda _: None)[0]) == 1
assert len(attempts) == 2

for code in (403, 429):
    try:
        mod.api_stars("dbrckk", opener=lambda request, timeout=20: (
            (_ for _ in ()).throw(HTTPError(request.full_url, code, "err", {}, None))
        ), sleeper=lambda _: None)
        raise AssertionError("API error treated as valid snapshot")
    except RuntimeError as exc:
        assert str(code) in str(exc)

# GitHub repository ID is stable even when the owner/name changes.
transfer_api = [star("New-Owner/Project", id=338719962)]
transfer_items, transfer_pages, _ = mod.api_stars(
    "dbrckk",
    opener=lambda _req, timeout=20: Response(transfer_api)
)
assert transfer_items[0]["githubRepositoryId"] == 338719962
by_name_only = mod.build_report("dbrckk", transfer_items, {"old-owner/project"}, transfer_pages)
assert by_name_only["summary"]["new"] == 1
by_stable_id = mod.build_report(
    "dbrckk", transfer_items, {"old-owner/project"}, transfer_pages,
    catalog_ids={338719962}
)
assert by_stable_id["summary"]["new"] == 0

# The complete same-run manifest can backfill IDs for legacy catalog
# entries without refetching already known GitHub repositories. A real
# transfer keeps its ID and an actually new Star still uses one metadata GET.
known_report = {
    "username": "dbrckk", "schemaVersion": 1,
    "checkedAt": "2026-10-18T14:00:00Z",
    "summary": {"starred": 3, "alreadyCataloged": 2, "new": 1},
    "newRepositories": [{"repo": "Fresh/New", "githubRepositoryId": 303}],
}
known_manifest = {
    "source": "GitHub public Stars of dbrckk",
    "checkedAt": known_report["checkedAt"],
    "repositories": ["Existing/Legacy", "Transferred/Repo", "Fresh/New"],
    "identities": [
        {"repo": "Existing/Legacy", "githubRepositoryId": 101},
        {"repo": "Transferred/Repo", "githubRepositoryId": 202},
        {"repo": "Fresh/New", "githubRepositoryId": 303},
    ],
}
known_ids = admission.manifest_stable_ids(known_manifest, known_report)
assert known_ids == {
    "existing/legacy": 101, "transferred/repo": 202, "fresh/new": 303,
}
existing_catalog = {"repositories": [
    {"repo": "Existing/Legacy"},
    {"repo": "Old-Owner/Repo", "githubRepositoryId": 202},
]}
fetches = []
def fresh_metadata(repo):
    fetches.append(repo)
    return star(
        "Fresh/New", id=303, forks_count=0, open_issues_count=0,
        default_branch="main", topics=[], private=False,
    )
filled_catalog, filled_summary = admission.admit(
    existing_catalog, known_report["newRepositories"], fresh_metadata,
    known_star_ids=known_ids,
)
assert fetches == ["Fresh/New"]
assert filled_summary["admitted"] == 1
assert filled_summary["identityEnriched"] == 1
assert len(filled_catalog["repositories"]) == 3
assert filled_catalog["repositories"][0]["githubRepositoryId"] == 101
assert filled_catalog["repositories"][1]["githubRepositoryId"] == 202
assert filled_catalog["repositories"][2]["githubRepositoryId"] == 303
assert existing_catalog["repositories"][0].get("githubRepositoryId") is None

# The manifest and report are one atomic identity snapshot: even if counts
# happen to match, divergent timestamps, missing rows and switched IDs must
# fail before admitting or enriching anything.
for bad_manifest in (
    {**known_manifest, "checkedAt": "2026-10-17T14:00:00Z"},
    {**known_manifest, "identities": known_manifest["identities"][:-1]},
    {**known_manifest, "identities": [
        known_manifest["identities"][0],
        known_manifest["identities"][1],
        {"repo": "Fresh/New", "githubRepositoryId": 999},
    ]},
    {**known_manifest, "identities": [
        known_manifest["identities"][0],
        known_manifest["identities"][1],
        {"repo": "Fresh/New", "githubRepositoryId": 202},
    ]},
):
    try:
        admission.manifest_stable_ids(bad_manifest, known_report)
        raise AssertionError("inconsistent full Stars snapshot accepted")
    except RuntimeError:
        pass

# A deleted/recreated owner/name is a different repository even when
# its spelling is identical. Neither the sync report nor admission may
# silently count the new permanent ID as the old starred dependency.
recycled = [{"repo": "Known/Repo", "githubRepositoryId": 222}]
try:
    mod.build_report(
        "dbrckk", recycled, {"known/repo"}, 1,
        catalog_ids={111}, catalog_name_ids={"known/repo": 111},
    )
    raise AssertionError("recycled GitHub repository name treated as already cataloged")
except RuntimeError as exc:
    assert "identity conflict" in str(exc)
try:
    admission.admit(
        {"repositories": [{"repo": "Known/Repo", "githubRepositoryId": 111}]},
        recycled,
        lambda _repo: (_ for _ in ()).throw(AssertionError("metadata should not be fetched")),
    )
    raise AssertionError("recycled name bypassed admission identity checks")
except RuntimeError as exc:
    assert "identity conflict" in str(exc)
# A genuine transfer keeps the permanent ID and is still considered known.
assert admission.admit(
    {"repositories": [{"repo": "Known/Repo", "githubRepositoryId": 111}]},
    [{"repo": "NEW/Repo", "githubRepositoryId": 111}],
    lambda _repo: (_ for _ in ()).throw(AssertionError("transfer must not refetch")),
)[1]["alreadyCataloged"] == 1

# Duplicate API names/IDs that contradict each other can arise if a GitHub
# repository transfers while pagination is in progress. Abort and retry
# next hour rather than publishing a misleading completeness count.
for inconsistent in (
    [star("Known/Repo", id=111), star("known/repo", id=222)],
    [star("Known/Repo", id=111), star("Other/Repo", id=111)],
):
    try:
        mod.api_stars("dbrckk", opener=lambda _req, timeout=20: Response(inconsistent))
        raise AssertionError("inconsistent Stars API identities were accepted")
    except RuntimeError as exc:
        assert "repository" in str(exc).lower() and "ID" in str(exc)

for bad_id in (-1, 0, True, "12"):
    try:
        mod.api_stars("dbrckk", opener=lambda _req, timeout=20: Response(
            [star("Test/Repo", id=bad_id)]
        ))
        raise AssertionError("invalid GitHub ID accepted")
    except RuntimeError as exc:
        assert "repository ID" in str(exc)

# Corrupt/missing catalogs must not produce misleading lists.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    catalog = root / "catalog.json"
    catalog.write_text('{"repositories":[{"repo":"KNOWN/Repo"}]}', encoding="utf-8")
    assert mod.catalog_identities(catalog) == {"known/repo"}
    catalog.write_text('{"repositories":[{"repo":"OLD/Repo","githubRepositoryId":338719962}]}')
    assert mod.catalog_identities(catalog, include_ids=True) == (
        {"old/repo"}, {338719962}
    )
    assert mod.catalog_identities(catalog, include_name_ids=True) == (
        {"old/repo"}, {338719962}, {"old/repo": 338719962}
    )
    catalog.write_text('{"repositories":[{"repo":"X/Y","githubRepositoryId":42},{"repo":"Z/W","githubRepositoryId":42}]}')
    try:
        mod.catalog_identities(catalog, include_ids=True)
        raise AssertionError("duplicate permanent repository IDs accepted")
    except RuntimeError:
        pass
    catalog.write_text('{"repositories":[{"repo":"X/Y","githubRepositoryId":0}]}')
    try:
        mod.catalog_identities(catalog, include_ids=True)
        raise AssertionError("invalid permanent repository ID accepted")
    except RuntimeError:
        pass
    catalog.write_text('{"repositories":[{"repo":"X/Y"},{"repo":"x/y"}]}')
    try:
        mod.catalog_identities(catalog)
        raise AssertionError("catalog duplicates accepted")
    except RuntimeError:
        pass
    catalog.write_text('{invalid')
    try:
        mod.catalog_identities(catalog)
        raise AssertionError("corrupt catalog accepted")
    except RuntimeError:
        pass

# CLI creates a parseable manifest usable by existing star_import_pipeline.py,
# emits review files, and must never change the authoritative catalog.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    catalog, report_json, report_md, manifest = (
        root / "catalog.json", root / "report.json",
        root / "issue.md", root / "manifest.json"
    )
    catalog.write_text('{"schemaVersion":1,"repositories":[{"repo":"Known/Repo"}]}\n')
    original = catalog.read_bytes()
    original_api = mod.api_stars
    try:
        mod.api_stars = lambda *_args, **_kwargs: (items, 2, 1)
        with contextlib.redirect_stdout(io.StringIO()):
            status = mod.main([
                "--user", "dbrckk", "--catalog", str(catalog),
                "--report-json", str(report_json), "--report-md", str(report_md),
                "--manifest", str(manifest),
            ])
        assert status == 0 and catalog.read_bytes() == original
        assert json.loads(report_json.read_text())["summary"]["new"] == 2
        assert len(json.loads(manifest.read_text())["repositories"]) == 3
        assert "identities" in json.loads(manifest.read_text())
        assert len(json.loads(manifest.read_text())["identities"]) == 3
        assert "New/Alpha" in report_md.read_text()
        report_json.unlink()
        mod.api_stars = lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("offline"))
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                mod.main(["--catalog", str(catalog), "--report-json", str(report_json)])
                raise AssertionError("failed API run returned success")
            except SystemExit as exc:
                assert exc.code == 2
        assert not report_json.exists() and catalog.read_bytes() == original
    finally:
        mod.api_stars = original_api

print("OK: GitHub Stars sync pagination, validation and fail-closed tests passed")
