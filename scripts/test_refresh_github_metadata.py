#!/usr/bin/env python3
"""Regression tests for resilient GitHub metadata refresh behavior."""
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
        assert live["languages"] == ["python"]
        assert gone["github"] == {"stars": 9}, "missing repos must keep their last known metadata"
        assert written["metadata"]["githubRefreshFailures"] == [
            {"repo": "gone/repo", "error": "HTTP Error 404: Not Found"}
        ]
        assert written["metadata"]["githubRefreshedAt"].endswith("Z")


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


if __name__ == "__main__":
    test_missing_repo_is_recorded_but_nonfatal()
    test_server_error_remains_fatal()
    print("refresh metadata resilience tests passed")
