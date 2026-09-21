#!/usr/bin/env python3
"""Audit catalog maintenance debt without mutating catalog.json."""
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
SEVERITY_ORDER = {"review": 0, "info": 1}


def _age_days(value, now):
    if not isinstance(value, str) or not value:
        return None
    try:
        pushed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if pushed.tzinfo is None:
        pushed = pushed.replace(tzinfo=timezone.utc)
    return max(0, (now - pushed.astimezone(timezone.utc)).days)


def analyze(repos, stale_days=730, now=None):
    if stale_days < 1:
        raise ValueError("stale_days must be >= 1")
    now = now or datetime.now(timezone.utc)
    findings = []
    guidance_fields = ("bestFor", "avoidWhen", "alternatives", "complements")

    def add(repo, severity, code, message):
        findings.append({
            "repo": repo,
            "severity": severity,
            "code": code,
            "message": message,
        })

    for entry in repos:
        name = entry.get("repo", "<unknown>")
        gh = entry.get("github")
        if not isinstance(gh, dict):
            add(name, "review", "missing-github-metadata", "GitHub metadata is missing.")
        else:
            tier = entry.get("tier")
            lifecycle = entry.get("lifecycle")
            if gh.get("archived") is True:
                if tier == "audit" or lifecycle in {"reference", "legacy"}:
                    code = f"archived-{lifecycle or 'audit'}-retained"
                    label = lifecycle or "audit"
                    add(
                        name,
                        "info",
                        code,
                        f"Repository is archived and intentionally retained as {label}.",
                    )
                else:
                    add(name, "review", "archived", "Repository is archived on GitHub.")
            if gh.get("disabled") is True:
                add(name, "review", "disabled", "Repository is disabled on GitHub.")

            age = _age_days(gh.get("pushedAt"), now)
            if age is not None and age >= stale_days and not gh.get("archived") and not gh.get("disabled"):
                if lifecycle in {"stable", "reference", "legacy"}:
                    add(
                        name,
                        "info",
                        f"stale-{lifecycle}",
                        f"No GitHub push for {age} days; classified as {lifecycle}.",
                    )
                elif tier == "audit":
                    add(
                        name,
                        "info",
                        "stale-audit-retained",
                        f"No GitHub push for {age} days; retained in the audit tier.",
                    )
                else:
                    add(
                        name,
                        "review",
                        "stale-over-threshold",
                        f"No GitHub push for {age} days (threshold: {stale_days}).",
                    )

            license_name = gh.get("license")
            if license_name in (None, "", "NOASSERTION"):
                add(name, "info", "license-unknown", "GitHub license metadata is unknown.")

        if not isinstance(entry.get("selfHosted"), bool):
            add(
                name,
                "info",
                "self-hosting-uncertain",
                "selfHosted is not a definitive boolean value.",
            )

    findings.sort(key=lambda row: (SEVERITY_ORDER[row["severity"]], row["repo"].lower(), row["code"]))
    severity_counts = Counter(row["severity"] for row in findings)
    code_counts = Counter(row["code"] for row in findings)
    guidance = {
        field: {
            "populated": sum(bool(entry.get(field)) for entry in repos),
            "missing": sum(not bool(entry.get(field)) for entry in repos),
        }
        for field in guidance_fields
    }

    return {
        "staleDays": stale_days,
        "repositories": len(repos),
        "summary": {
            "findings": len(findings),
            "review": severity_counts["review"],
            "info": severity_counts["info"],
            "byCode": dict(sorted(code_counts.items())),
        },
        "guidanceCoverage": guidance,
        "findings": findings,
    }


def render_markdown(report):
    summary = report["summary"]
    lines = [
        "<!-- star-list-catalog-quality -->",
        "# Catalog quality audit",
        "",
        f"- Repositories: **{report['repositories']}**",
        f"- Review findings: **{summary['review']}**",
        f"- Informational findings: **{summary['info']}**",
        f"- Staleness threshold: **{report['staleDays']} days**",
        "",
        "## Selection-guidance coverage",
        "",
        "| Field | Populated | Missing |",
        "| --- | ---: | ---: |",
    ]
    for field, values in report["guidanceCoverage"].items():
        lines.append(f"| `{field}` | {values['populated']} | {values['missing']} |")

    review = [row for row in report["findings"] if row["severity"] == "review"]
    info = [row for row in report["findings"] if row["severity"] == "info"]

    lines += ["", "## Review required", ""]
    if review:
        lines += ["| Repository | Code | Detail |", "| --- | --- | --- |"]
        for row in review:
            lines.append(f"| `{row['repo']}` | `{row['code']}` | {row['message']} |")
    else:
        lines.append("No review-level findings.")

    lines += ["", "## Informational debt", ""]
    if info:
        lines += ["| Repository | Code | Detail |", "| --- | --- | --- |"]
        for row in info:
            lines.append(f"| `{row['repo']}` | `{row['code']}` | {row['message']} |")
    else:
        lines.append("No informational findings.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Audit catalog maintenance debt.")
    parser.add_argument("--stale-days", type=int, default=730)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-review", action="store_true")
    args = parser.parse_args()
    if args.stale_days < 1:
        parser.error("--stale-days must be >= 1")

    repos = json.loads(CATALOG.read_text()).get("repositories", [])
    report = analyze(repos, stale_days=args.stale_days)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.markdown_output:
        args.markdown_output.write_text(render_markdown(report))
    if args.fail_on_review and report["summary"]["review"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
