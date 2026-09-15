#!/usr/bin/env python3
"""Render replacement-report.json as a stable GitHub issue body."""
import argparse, json
from pathlib import Path

def render(report):
    rows = report.get("repositories", [])
    lines = [
        "## Automated repository health review", "",
        f"Detected **{len(rows)}** repositories requiring review (threshold: **{report.get('threshold', 55)}**).", "",
        "| Repository | Health | Status | Best replacement | Replacement score |",
        "|---|---:|---|---|---:|",
    ]
    for row in rows:
        h = row.get("health", {})
        replacements = row.get("suggestedReplacements", [])
        best = replacements[0] if replacements else None
        best_name = best["repo"] if best else "none"
        best_score = best.get("replacementScore") if best else "n/a"
        lines.append(f"| {row['repo']} | {h.get('score', 'n/a')} | {h.get('status', 'unknown')} | {best_name} | {best_score} |")
    lines += ["", "### Details", ""]
    for row in rows:
        lines.append(f"#### {row['repo']}")
        h = row.get("health", {})
        reasons = ", ".join(h.get("reasons", [])) or "health threshold"
        lines.append(f"- Health: **{h.get('score')}** ({h.get('status')}); reason: {reasons}.")
        replacements = row.get("suggestedReplacements", [])
        if replacements:
            lines.append("- Candidates: " + "; ".join(
                f"{x['repo']} (fit {x['replacementScore']}, health {x['health'].get('score')})" for x in replacements
            ))
        else:
            lines.append("- Candidates: none found in the current catalog.")
        lines.append("")
    lines += ["This report is advisory. No repository is automatically removed or replaced.", "", "<!-- star-list-health-review -->"]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    body = render(json.loads(args.report.read_text()))
    if args.output: args.output.write_text(body + "\n")
    else: print(body)

if __name__ == "__main__":
    main()
