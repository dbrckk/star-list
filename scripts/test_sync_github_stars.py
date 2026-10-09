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
assert "not" in rendered.lower() and "automatically" in rendered.lower()
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

# Corrupt/missing catalogs must not produce misleading lists.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    catalog = root / "catalog.json"
    catalog.write_text('{"repositories":[{"repo":"KNOWN/Repo"}]}', encoding="utf-8")
    assert mod.catalog_identities(catalog) == {"known/repo"}
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
