#!/usr/bin/env python3
"""Operator-only, read-only diagnosis of failed public star-list integrations.

Do not copy worker goals, error messages, project IDs, job keys, private repos,
tokens or URLs from Production-OS into a public GitHub Actions artifact.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

from portfolio_daily import request_json

PUBLIC_FAILED_TARGETS = frozenset({
    "dbrckk/ai-trading",
    "dbrckk/vibecheck-android",
    "dbrckk/viral-android-game",
    "dbrckk/xbow-perso",
})
ENDPOINT = (
    "https://production-os1.onrender.com/v1/dashboard/productions"
    "?filter=problems&q=starlist-integration-v&limit=200"
)
TRACKING = re.compile(r"(?<![a-z0-9])starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])")
CATEGORIES = (
    ("provider-quota-or-token-budget", r"quota|rate.limit|429|token.{0,20}(?:budget|limit|exhaust)|(?:budget|limit).{0,20}token"),
    ("provider-unavailable-or-auth", r"provider|model.{0,25}(?:unavailable|fail)|401|403|unauthori[sz]|invalid.api.key"),
    ("network-or-timeout", r"timeout|timed.out|connect(?:ion)?.{0,20}(?:reset|refused|failed)|network|502|503|504"),
    ("tests-or-build-failed", r"pytest|test.{0,20}fail|build.{0,20}fail|compil|syntax.error|lint.{0,20}fail"),
    ("github-or-delivery-failed", r"git(?:hub)?.{0,20}(?:denied|failed|permission|conflict)|pull.request|push.{0,20}reject"),
    ("worker-or-execution-failed", r"worker|execution|stage.{0,20}fail|continuation.limit|task.{0,20}fail|traceback"),
    ("incompatible-tool", r"licen[cs]|incompatib|dependency.conflict|unsupported.runtime"),
)
WORKFLOW_STATES = frozenset({
    "failed", "cancelled", "blocked", "succeeded", "running",
    "queued", "pending", "ready", "unknown",
})
VALIDATION_STATES = frozenset({
    "pass", "passed", "success", "succeeded", "fail", "failed",
    "blocked", "skipped", "pending", "unknown",
})


def safe_state(raw: object, allowed: frozenset[str]) -> str:
    value = raw.strip().lower() if isinstance(raw, str) else ""
    return value if value in allowed else "unknown"


def failure_category(outcome: object) -> str:
    # Scan free text internally only; NEVER persist or print it.
    if not isinstance(outcome, dict):
        return "unknown"
    message = outcome.get("summary")
    if not isinstance(message, str):
        return "unknown"
    content = message[:8000].lower()
    for name, pattern in CATEGORIES:
        if re.search(pattern, content):
            return name
    return "unknown"


def safe_public_failure(item: object) -> dict | None:
    if not isinstance(item, dict):
        return None
    target = item.get("repository")
    if not isinstance(target, str) or target.lower() not in PUBLIC_FAILED_TARGETS:
        return None
    if item.get("status") != "NEEDS_ATTENTION":
        return None
    goal = item.get("final_goal")
    marker = TRACKING.search(goal) if isinstance(goal, str) else None
    if marker is None:
        return None
    outcome = item.get("outcome")
    outcome = outcome if isinstance(outcome, dict) else {}
    runtime = item.get("runtime")
    runtime = runtime if isinstance(runtime, dict) else {}
    commits = outcome.get("commit_shas")
    commits_count = min(20, len(commits)) if isinstance(commits, list) else 0
    return {
        "target": target.lower(),
        "tracking_version": "v" + marker.group(1),
        "status": "NEEDS_ATTENTION",
        "failure_category": failure_category(outcome),
        "workflow_status": safe_state(outcome.get("workflow_status"), WORKFLOW_STATES),
        "validation_status": safe_state(outcome.get("validation_status"), VALIDATION_STATES),
        "commit_count": commits_count,
        "pull_request_reported": isinstance(outcome.get("pull_request"), dict),
        "ci_reported": isinstance(outcome.get("ci"), dict),
        "runtime_phase": safe_state(
            runtime.get("phase"),
            frozenset({"needs_attention", "review_required", "done", "preparing",
                       "running", "queued", "claimed", "cancelling"}),
        ),
        "task_status": safe_state(runtime.get("task_status"), WORKFLOW_STATES),
    }


def public_diagnostics(payload: object) -> dict:
    if not isinstance(payload, dict) or payload.get("schema_version") != "production-os/production-inbox/v1":
        raise RuntimeError("invalid diagnostic response schema")
    summary = payload.get("summary")
    items = payload.get("items")
    if not isinstance(summary, dict) or not isinstance(items, list):
        raise RuntimeError("invalid diagnostic response structure")
    matching = summary.get("matching")
    if type(matching) is not int or matching < 0 or matching > len(items):
        raise RuntimeError("incomplete or invalid diagnostic page")
    rows = [record for item in items if (record := safe_public_failure(item)) is not None]
    # The public issue previously verified exactly these four unresolved v2 targets.
    found = {row["target"] for row in rows if row["tracking_version"] == "v2"}
    rows.sort(key=lambda r: (r["target"], r["tracking_version"]))
    return {
        "schema_version": "star-list/public-failure-diagnostics/v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "expected_public_v2_targets": len(PUBLIC_FAILED_TARGETS),
        "observed_public_v2_targets": len(found),
        "coverage_complete": found == PUBLIC_FAILED_TARGETS,
        "failures": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("portfolio-failure-diagnostics.json"))
    args = parser.parse_args()
    token = os.environ.get("PRODUCTION_OS_OPERATOR_TOKEN", "")
    if not token:
        print("operator diagnostic unavailable: missing configured secret", file=sys.stderr)
        return 2
    try:
        result = public_diagnostics(request_json(ENDPOINT, token))
    except (RuntimeError, ValueError, TypeError, KeyError):
        print("operator diagnostic unavailable: invalid or incomplete response", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # The log and artifact contain only strictly allowlisted public target names
    # and enumerated failure categories. Never show backend response bodies.
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["coverage_complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
