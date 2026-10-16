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
# This O(1)-query index replaces the global production inbox, which eagerly
# materializes hundreds of unrelated project statuses before search filtering.
# Only an authenticated operator receives per-project diagnostic IDs.
ENDPOINT = (
    "https://production-os1.onrender.com/v1/managed-projects/integration-inventory"
    "?include_project_ids=1"
)
TRACKING = re.compile(r"(?<![a-z0-9])starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])")
CATEGORIES = (
    ("preview-cycle-limit", r"godot_preview_cycle_budget_exhausted|preview.cycle.budget.exhausted"),
    ("worker-capacity-exhausted", r"capacity_exhausted|capacity.exhausted|no.compatible.worker|worker.capacity.exhausted"),
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


def task_failure_evidence(detail: object) -> dict:
    """Summarize failed workflow tasks without exposing source text or identifiers."""
    workflow = detail.get("current_workflow") if isinstance(detail, dict) else None
    tasks = workflow.get("tasks") if isinstance(workflow, dict) else None
    if not isinstance(tasks, list):
        return {"details_checked": False, "failed_task_count": 0,
                "retry_budget_exhausted": None, "failure_category": "unknown"}
    failed = [task for task in tasks if isinstance(task, dict)
              and task.get("status") in {"failed", "blocked", "cancelled"}]
    # A terminal project without any terminal task is missing evidence, not
    # proof that a deep task diagnosis has succeeded.
    if not failed:
        return {"details_checked": False, "failed_task_count": 0,
                "retry_budget_exhausted": None, "failure_category": "unknown"}
    category = "unknown"
    for task in reversed(failed):
        result = task.get("result")
        if not isinstance(result, dict):
            continue
        fields = [result.get(key) for key in (
            "summary", "message", "error", "reason", "failure_reason",
            "ai_dev_server_status", "error_code", "status",
        )]
        evidence = result.get("evidence")
        if isinstance(evidence, dict):
            fields.extend(evidence.get(key) for key in (
                "error", "message", "reason", "failure_reason", "error_code",
                "next_stage", "pipeline_status", "blocked_reason",
            ))
        # All raw fields are classified in memory only; none are persisted.
        description = " ".join(value[:1000] for value in fields if isinstance(value, str))
        category = failure_category({"summary": description})
        if category != "unknown":
            break
    final = failed[-1] if failed else {}
    attempts = final.get("attempts")
    budget = final.get("max_attempts")
    exhausted = (attempts >= budget if type(attempts) is int
                 and type(budget) is int and budget > 0 else None)
    result = final.get("result") if isinstance(final.get("result"), dict) else {}
    evidence = result.get("evidence") if isinstance(result.get("evidence"), dict) else {}
    known_result_keys = (
        "summary", "message", "error", "reason", "failure_reason",
        "ai_dev_server_status", "error_code", "status", "evidence",
    )
    known_evidence_keys = (
        "error", "message", "reason", "failure_reason",
        "error_code", "next_stage", "pipeline_status", "blocked_reason",
    )
    return {
        "details_checked": True,
        "failed_task_count": min(100, len(failed)),
        "task_attempts": min(100, attempts) if type(attempts) is int and attempts >= 0 else None,
        "task_max_attempts": min(100, budget) if type(budget) is int and budget > 0 else None,
        "retry_budget_exhausted": exhausted,
        "failure_category": category,
        "result_fields_present": [k for k in known_result_keys if k in result],
        "evidence_fields_present": [k for k in known_evidence_keys if k in evidence],
        "worker_result_status": safe_state(
            result.get("ai_dev_server_status"),
            frozenset({"blocked", "capacity_exhausted", "failed", "succeeded",
                       "success", "unavailable", "running", "unknown"}),
        ),
        "pipeline_status": safe_state(
            evidence.get("pipeline_status"),
            frozenset({"blocked", "capacity_exhausted", "failed", "succeeded",
                       "running", "ready", "pending", "unknown"}),
        ),
    }


def add_deep_task_diagnostics(result: dict, inbox: object, token: str) -> dict:
    """Fetch each public failed v2 project individually with operator privileges.

    Internal project IDs are used only in the request path, never in output.
    A missing/mismatched detail makes the diagnosis incomplete, not successful.
    """
    if not isinstance(inbox, dict):
        raise RuntimeError("invalid private diagnostic inbox")
    items = inbox.get("items")
    if not isinstance(items, list):
        raise RuntimeError("missing private diagnostic rows")
    selected = {}
    ambiguous_targets = set()
    for item in items:
        record = safe_public_failure(item)
        if record is None or record["tracking_version"] != "v2":
            continue
        target = record["target"]
        if target in selected:
            ambiguous_targets.add(target)
        else:
            selected[target] = item
    checked = 0
    for record in result["failures"]:
        if record["tracking_version"] != "v2":
            continue
        # Never attribute one project/task result to a different historical
        # v2 candidate merely because the repository name is the same.
        if record["target"] in ambiguous_targets:
            record["details_checked"] = False
            continue
        item = selected.get(record["target"])
        identifier = item.get("project_id") if isinstance(item, dict) else None
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-f0-9]{32}", identifier):
            record["details_checked"] = False
            continue
        try:
            response = request_json(
                "https://production-os1.onrender.com/v1/managed-projects/" + identifier,
                token, max_attempts=1,
            )
            project = response.get("project") if isinstance(response, dict) else None
            if not isinstance(project, dict):
                raise RuntimeError("missing project detail")
            if str(project.get("repository") or "").lower() != record["target"]:
                raise RuntimeError("project identity mismatch")
            raw_goal = str(project.get("final_goal") or "")
            expected_goal = str(item.get("final_goal") or "")
            actual = TRACKING.search(raw_goal)
            expected = TRACKING.search(expected_goal)
            if actual is None or expected is None or actual.group() != expected.group():
                raise RuntimeError("project tracking marker mismatch")
            if project.get("status") != "NEEDS_ATTENTION":
                raise RuntimeError("project state changed during diagnosis")
            deeper = task_failure_evidence(project)
            record["details_checked"] = deeper["details_checked"] is True
            if not record["details_checked"]:
                continue
            for key in (
                "failed_task_count", "task_attempts", "task_max_attempts",
                "retry_budget_exhausted", "result_fields_present",
                "evidence_fields_present", "worker_result_status", "pipeline_status",
            ):
                record[key] = deeper[key]
            if record["failure_category"] == "unknown":
                record["failure_category"] = deeper["failure_category"]
            checked += 1
        except (RuntimeError, ValueError, TypeError, KeyError):
            record["details_checked"] = False
    result["details_checked_v2"] = checked
    result["details_complete"] = (
        result["coverage_complete"] and checked == len(PUBLIC_FAILED_TARGETS)
    )
    return result


def inventory_diagnostic_inbox(payload: object) -> dict:
    """Convert a complete operator-only index into filtered-inbox structure.

    Never copy raw worker instructions into artifacts. The server itself
    redacts tracking goals; this in-memory conversion keeps only the fields
    needed to fetch the four public failed v2 project details.
    """
    if not isinstance(payload, dict) or payload.get("complete") is not True:
        raise RuntimeError("operator integration inventory unavailable")
    rows = payload.get("projects")
    total = payload.get("total_count")
    if (not isinstance(rows, list) or type(total) is not int
            or total != len(rows) or total > 10000
            or any(not isinstance(row, dict) for row in rows)):
        raise RuntimeError("operator integration inventory incomplete")
    items = []
    for row in rows:
        # An incomplete privileged index cannot prove absence of a job.
        if (not isinstance(row.get("repository"), str)
                or not isinstance(row.get("final_goal"), str)
                or not isinstance(row.get("status"), str)
                or not isinstance(row.get("project_id"), str)):
            raise RuntimeError("operator integration inventory missing identity")
        items.append({
            "repository": row["repository"],
            "status": row["status"],
            "final_goal": row["final_goal"],
            "project_id": row["project_id"],
        })
    return {
        "schema_version": "production-os/production-inbox/v1",
        "summary": {"matching": len(items)},
        "items": items,
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
    v2_targets = [row["target"] for row in rows if row["tracking_version"] == "v2"]
    found = set(v2_targets)
    # Multiple failed v2 candidates for one repository require an explicit
    # per-candidate reconciliation, not silent attribution by target alone.
    unique_v2_targets = len(v2_targets) == len(found)
    rows.sort(key=lambda r: (r["target"], r["tracking_version"]))
    return {
        "schema_version": "star-list/public-failure-diagnostics/v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "expected_public_v2_targets": len(PUBLIC_FAILED_TARGETS),
        "observed_public_v2_targets": len(found),
        "coverage_complete": found == PUBLIC_FAILED_TARGETS and unique_v2_targets,
        "failures": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("portfolio-failure-diagnostics.json"))
    args = parser.parse_args()
    # Always create a secret-free artifact, including when Render is sleeping,
    # an operator credential is missing, or an authenticated read times out.
    # The previous early-return behavior concealed why a diagnosis failed.
    result = {
        "schema_version": "star-list/public-failure-diagnostics/v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "expected_public_v2_targets": len(PUBLIC_FAILED_TARGETS),
        "observed_public_v2_targets": 0,
        "coverage_complete": False,
        "details_checked_v2": 0,
        "details_complete": False,
        "failures": [],
        "diagnostic_status": "unavailable",
    }
    token = os.environ.get("PRODUCTION_OS_OPERATOR_TOKEN", "")
    if not token:
        result["diagnostic_status"] = "missing-operator-token"
    else:
        stage = "inbox"
        try:
            inbox = inventory_diagnostic_inbox(
                request_json(ENDPOINT, token, max_attempts=1)
            )
            result = public_diagnostics(inbox)
            stage = "task-details"
            result = add_deep_task_diagnostics(result, inbox, token)
            result["diagnostic_status"] = (
                "complete" if result["coverage_complete"] and result["details_complete"]
                else "incomplete-task-evidence"
            )
        except (RuntimeError, ValueError, TypeError, KeyError):
            # Never echo network exception text or the private API response:
            # both can contain backend details or credential-bearing URLs.
            result["diagnostic_status"] = "unavailable-" + stage
            result.setdefault("details_checked_v2", 0)
            result.setdefault("details_complete", False)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # The log and artifact contain only allowlisted public names, enums and
    # counters. Unavailable and incomplete diagnoses still exit nonzero.
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["diagnostic_status"] == "complete" else 2


if __name__ == "__main__":
    sys.exit(main())
