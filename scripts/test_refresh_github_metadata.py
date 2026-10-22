#!/usr/bin/env python3
"""Regression tests for resilient GitHub metadata refresh behavior."""
import base64
import json
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError

import refresh_github_metadata as refresh


def http_error(repo, code, message):
    return HTTPError(
        f"https://api.github.com/repos/{repo}",
        code,
        message,
        hdrs=None,
        fp=None,
    )


def run_main(args):
    old_argv = sys.argv
    try:
        sys.argv = ["refresh_github_metadata.py", *args]
        refresh.main()
    finally:
        sys.argv = old_argv


def test_missing_repo_is_recorded_but_nonfatal():
    with tempfile.TemporaryDirectory() as tmp:
        catalog = Path(tmp) / "catalog.json"
        catalog.write_text(json.dumps({
            "metadata": {},
            "repositories": [
                {"repo": "live/repo", "github": {"stars": 1}, "languages": ["unknown"]},
                {"repo": "gone/repo", "github": {"stars": 9}},
            ],
        }))

        old_catalog, old_fetch = refresh.CATALOG, refresh.fetch
        try:
            refresh.CATALOG = catalog

            def fake_fetch(repo, token=None, retries=2):
                if repo == "gone/repo":
                    raise http_error(repo, 404, "Not Found")
                return {
                    "id": 424242,
                    "stargazers_count": 42,
                    "forks_count": 3,
                    "open_issues_count": 1,
                    "archived": False,
                    "disabled": False,
                    "default_branch": "main",
                    "license": {"spdx_id": "MIT"},
                    "pushed_at": "2026-09-15T12:00:00Z",
                    "language": "Python",
                }

            refresh.fetch = fake_fetch
            run_main(["--write"])
        finally:
            refresh.CATALOG, refresh.fetch = old_catalog, old_fetch

        written = json.loads(catalog.read_text())
        live, gone = written["repositories"]
        assert live["github"]["stars"] == 42
        assert live["githubRepositoryId"] == 424242
        assert live["languages"] == ["python"]
        assert gone["github"] == {"stars": 9}, "missing repos must keep their last known metadata"
        assert written["metadata"]["githubRefreshFailures"] == [
            {"repo": "gone/repo", "error": "HTTP Error 404: Not Found"}
        ]
        assert written["metadata"]["githubRefreshedAt"].endswith("Z")


def test_license_signature_detection():
    assert refresh.detect_license_text("""MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software...
""") == "MIT"
    assert refresh.detect_license_text("""Apache License
Version 2.0, January 2004
""") == "Apache-2.0"
    assert refresh.detect_license_text("""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
""") == "GPL-3.0"
    assert refresh.detect_license_text("""Mozilla Public License Version 2.0
""") == "MPL-2.0"
    assert refresh.detect_license_text("This work is licensed under a Creative Commons Attribution 4.0 International License.") == "CC-BY-4.0"
    assert refresh.detect_license_text("To the extent possible under law, Example Author has waived all copyright and related or neighboring rights to this work.") == "CC0-1.0"
    assert refresh.detect_license_text("## License\nMIT") == "MIT"
    assert refresh.detect_license_text("custom proprietary terms") is None
    # Bare words and README snippets must not grant repo-wide reuse rights.
    assert refresh.strict_root_license("## License\\nMIT") is None
    assert refresh.strict_root_license(
        "Portions of this software are licensed as follows: MIT for other files. "
        "Permission is hereby granted, free of charge, to any person obtaining a copy "
        "of this software, to deal in the Software without restriction."
    ) is None
    assert refresh.strict_root_license(
        "MIT License\\nPermission is hereby granted, free of charge, to any person obtaining a copy "
        "of this software, to deal in the Software without restriction."
    ) == "MIT"



def test_license_fallback_reads_root_license_file():
    original = refresh.fetch_contents
    try:
        def fake_contents(repo, path="", ref=None, token=None, retries=2):
            if not path:
                return [
                    {"type": "file", "name": "README.md", "path": "README.md"},
                    {"type": "file", "name": "LICENSE", "path": "LICENSE"},
                ]
            assert path == "LICENSE"
            content = base64.b64encode(
                b"MIT License\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software, to deal in the Software without restriction."
            ).decode()
            return {"type": "file", "name": "LICENSE", "path": "LICENSE", "content": content}
        refresh.fetch_contents = fake_contents
        assert refresh.fallback_license("x/repo", "main") == "MIT"
    finally:
        refresh.fetch_contents = original


def test_license_fallback_reads_readme_when_root_license_is_absent():
    original = refresh.fetch_contents
    try:
        def fake_contents(repo, path="", ref=None, token=None, retries=2):
            if not path:
                return [{"type": "file", "name": "README.md", "path": "README.md"}]
            content = base64.b64encode(
                b"## License\nThis work is licensed under a Creative Commons Attribution 4.0 International License."
            ).decode()
            return {"type": "file", "name": "README.md", "path": "README.md", "content": content}
        refresh.fetch_contents = fake_contents
        assert refresh.fallback_license("x/repo", "main") is None
    finally:
        refresh.fetch_contents = original


def test_license_fallback_rejects_conflicting_root_files():
    original = refresh.fetch_contents
    try:
        def fake_contents(repo, path="", ref=None, token=None, retries=2):
            if not path:
                return [
                    {"type": "file", "name": "LICENSE", "path": "LICENSE"},
                    {"type": "file", "name": "COPYING", "path": "COPYING"},
                ]
            content = (
                "MIT License\\nPermission is hereby granted, free of charge, to any person "
                "obtaining a copy of this software, to deal in the Software without restriction."
                if path == "LICENSE" else
                "GNU GENERAL PUBLIC LICENSE\\nVersion 3, 29 June 2007"
            )
            return {"type": "file", "content": base64.b64encode(content.encode()).decode()}
        refresh.fetch_contents = fake_contents
        assert refresh.fallback_license("x/repo", "main") is None
    finally:
        refresh.fetch_contents = original


def test_metadata_refresh_uses_license_fallback():
    with tempfile.TemporaryDirectory() as tmp:
        catalog = Path(tmp) / "catalog.json"
        catalog.write_text(json.dumps({
            "metadata": {},
            "repositories": [{"repo": "x/repo", "github": {}, "languages": ["python"]}],
        }))
        old_catalog, old_fetch, old_fallback = refresh.CATALOG, refresh.fetch, refresh.fallback_license
        try:
            refresh.CATALOG = catalog
            refresh.fetch = lambda repo, token=None, retries=2: {
                "stargazers_count": 10,
                "forks_count": 2,
                "open_issues_count": 1,
                "archived": False,
                "disabled": False,
                "default_branch": "main",
                "license": {"spdx_id": "NOASSERTION"},
                "pushed_at": "2026-09-20T00:00:00Z",
                "language": "Python",
            }
            refresh.fallback_license = lambda repo, default_branch, token=None: "MIT"
            run_main(["--write"])
        finally:
            refresh.CATALOG, refresh.fetch, refresh.fallback_license = old_catalog, old_fetch, old_fallback
        written = json.loads(catalog.read_text())
        assert written["repositories"][0]["github"]["license"] == "MIT"



def test_metadata_refresh_preserves_verified_license_when_github_is_inconclusive():
    with tempfile.TemporaryDirectory() as tmp:
        catalog = Path(tmp) / "catalog.json"
        catalog.write_text(json.dumps({
            "metadata": {},
            "repositories": [{
                "repo": "x/repo",
                "github": {"license": "Custom Verified License"},
                "languages": ["python"],
            }],
        }))
        old_catalog, old_fetch, old_fallback = refresh.CATALOG, refresh.fetch, refresh.fallback_license
        try:
            refresh.CATALOG = catalog
            refresh.fetch = lambda repo, token=None, retries=2: {
                "stargazers_count": 10,
                "forks_count": 2,
                "open_issues_count": 1,
                "archived": False,
                "disabled": False,
                "default_branch": "main",
                "license": {"spdx_id": "NOASSERTION"},
                "pushed_at": "2026-09-20T00:00:00Z",
                "language": "Python",
            }
            refresh.fallback_license = lambda repo, default_branch, token=None: None
            run_main(["--write"])
        finally:
            refresh.CATALOG, refresh.fetch, refresh.fallback_license = old_catalog, old_fetch, old_fallback
        written = json.loads(catalog.read_text())
        assert written["repositories"][0]["github"]["license"] == "Custom Verified License"


def test_server_error_remains_fatal():
    with tempfile.TemporaryDirectory() as tmp:
        catalog = Path(tmp) / "catalog.json"
        catalog.write_text(json.dumps({
            "metadata": {},
            "repositories": [{"repo": "broken/repo"}],
        }))

        old_catalog, old_fetch = refresh.CATALOG, refresh.fetch
        try:
            refresh.CATALOG = catalog
            refresh.fetch = lambda repo, token=None, retries=2: (_ for _ in ()).throw(
                http_error(repo, 500, "Server Error")
            )
            try:
                run_main(["--write"])
            except SystemExit as exc:
                assert exc.code == 1
            else:
                raise AssertionError("HTTP 500 must keep the refresh command failing")
        finally:
            refresh.CATALOG, refresh.fetch = old_catalog, old_fetch

    # Reusing an existing slug for a new GitHub ID must not silently change
    # the catalog's established permanent identity.
    with tempfile.TemporaryDirectory() as tmp:
        catalog = Path(tmp) / "catalog.json"
        catalog.write_text(json.dumps({
            "metadata": {},
            "repositories": [{
                "repo": "recycled/repo", "githubRepositoryId": 111,
                "github": {"stars": 7},
            }],
        }))
        old_catalog, old_fetch, old_fallback = (
            refresh.CATALOG, refresh.fetch, refresh.fallback_license,
        )
        try:
            refresh.CATALOG = catalog
            refresh.fetch = lambda repo, token=None, retries=2: {
                "id": 222, "stargazers_count": 11, "forks_count": 1,
                "open_issues_count": 0, "archived": False, "disabled": False,
                "default_branch": "main", "license": {"spdx_id": "MIT"},
                "pushed_at": "2026-10-18T00:00:00Z",
            }
            refresh.fallback_license = lambda *_args, **_kwargs: None
            try:
                run_main(["--write"])
            except SystemExit as exc:
                assert exc.code == 1
            else:
                raise AssertionError("recycled GitHub ID must fail refresh")
        finally:
            refresh.CATALOG, refresh.fetch, refresh.fallback_license = (
                old_catalog, old_fetch, old_fallback,
            )
        unchanged = json.loads(catalog.read_text())["repositories"][0]
        assert unchanged["githubRepositoryId"] == 111
        assert unchanged["github"] == {"stars": 7}

    # Metadata and license fallback requests must use the same authenticated
    # GitHub-only opener as Stars synchronization, never urlopen's default
    # unrestricted redirect handling.
    import sync_github_stars
    assert refresh.SAFE_GITHUB_HTTP is sync_github_stars.SAFE_GITHUB_HTTP
    class RejectingOpener:
        def open(self, request, timeout=20):
            assert request.get_header("Authorization") == "Bearer masked-token"
            assert request.full_url.startswith("https://api.github.com/")
            raise RuntimeError("Refusing cross-origin GitHub API redirect")
    previous_opener = refresh.SAFE_GITHUB_HTTP
    try:
        refresh.SAFE_GITHUB_HTTP = RejectingOpener()
        try:
            refresh._request_json(
                "https://api.github.com/repos/any/repository",
                token="masked-token", retries=0,
            )
        except RuntimeError as exc:
            assert "cross-origin" in str(exc)
        else:
            raise AssertionError("metadata fetch bypassed safe GitHub transport")
    finally:
        refresh.SAFE_GITHUB_HTTP = previous_opener


if __name__ == "__main__":
    test_missing_repo_is_recorded_but_nonfatal()
    test_license_signature_detection()
    test_license_fallback_reads_root_license_file()
    test_license_fallback_reads_readme_when_root_license_is_absent()
    test_license_fallback_rejects_conflicting_root_files()
    test_metadata_refresh_uses_license_fallback()
    test_metadata_refresh_preserves_verified_license_when_github_is_inconclusive()
    test_server_error_remains_fatal()
    print("refresh metadata resilience tests passed")
