#!/usr/bin/env python3
"""Render replacement and health-drift reports as one stable GitHub issue body."""
import argparse, json
from pathlib import Path

def render(report, drift=None):
    rows = report.get("repositories", [])
    drift = drift or {"repositories": [], "findings": 0}
    drifts = drift.get("repositories", [])
    lines = [
        "## Automated repository health review", "",
        f"Replacement review: **{len(rows)}** repositories. Significant health drift: **{len(drifts)}** repositories.", "",
    ]
    if drifts:
        lines += [
            "### Recent health deterioration", "",
            "| Repository | Previous | Current | Delta | Status change |",
            "|---|---:|---:|---:|---|",
        ]
        for x in drifts:
            lines.append(f"| {x['repo']} | {x['previousScore']} | {x['currentScore']} | {x['delta']} | {x.get('previousStatus')} -> {x.get('currentStatus')} |")
        lines.append("")
    if rows:
        lines += [
            "### Replacement candidates", "",
            "| Repository | Health | Status | Best replacement | Replacement score |",
            "|---|---:|---|---|---:|",
        ]
        for row in rows:
            h=row.get("health",{}); repl=row.get("suggestedReplacements",[]); best=repl[0] if repl else None
            lines.append(f"| {row['repo']} | {h.get('score','n/a')} | {h.get('status','unknown')} | {best['repo'] if best else 'none'} | {best.get('replacementScore') if best else 'n/a'} |")
        lines += ["", "### Replacement details", ""]
        for row in rows:
            h=row.get("health",{}); reasons=", ".join(h.get("reasons",[])) or "health threshold"
            lines.append(f"#### {row['repo']}")
            lines.append(f"- Health: **{h.get('score')}** ({h.get('status')}); reason: {reasons}.")
            repl=row.get("suggestedReplacements",[])
            lines.append("- Candidates: " + ("; ".join(f"{x['repo']} (fit {x['replacementScore']}, health {x['health'].get('score')})" for x in repl) if repl else "none found in the current catalog."))
            lines.append("")
    lines += ["This report is advisory. No repository is automatically removed or replaced.", "", "<!-- star-list-health-review -->"]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("report",type=Path)
    ap.add_argument("--drift",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    drift=json.loads(args.drift.read_text()) if args.drift else None
    body=render(json.loads(args.report.read_text()),drift)
    if args.output: args.output.write_text(body+"\n")
    else: print(body)

if __name__=="__main__":
    main()
