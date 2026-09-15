#!/usr/bin/env python3
"""Render actionable discovery candidates as a stable GitHub issue."""
import argparse,json
from pathlib import Path

def render(data,limit=20):
    rows=[x for x in data.get("repositories",[]) if x.get("decision") in {"accept","review"}][:limit]
    counts=data.get("counts",{})
    lines=["## Discovery candidates","",f"Evaluated **{data.get('candidates',0)}** candidates: **{counts.get('accept',0)} accept**, **{counts.get('review',0)} review**, **{counts.get('reject',0)} reject**.",""]
    if rows:
        lines += ["| Decision | Repository | Score | Stars | Activity age | Gaps |","|---|---|---:|---:|---:|---|"]
        for x in rows:
            targets=", ".join(f"{m.get('kind')}:{m.get('target')}" for m in x.get("matchedTargets",[]))
            url=x.get("url") or ""
            repo=f"[{x['repo']}]({url})" if url else x["repo"]
            lines.append(f"| **{x['decision']}** | {repo} | {x.get('evaluationScore')} | {x.get('stars',0)} | {x.get('ageDays','n/a')}d | {targets} |")
        lines += ["","### Evaluation notes",""]
        for x in rows: lines.append(f"- **{x['repo']}** — {', '.join(x.get('reasons',[])) or 'no additional signals'}")
    else: lines += ["No candidates currently meet the accept or review thresholds."]
    lines += ["","Candidates are never added to the catalog automatically.","","<!-- star-list-discovery-candidates -->"]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("--output",type=Path); ap.add_argument("--limit",type=int,default=20)
    args=ap.parse_args(); body=render(json.loads(args.evaluated.read_text()),args.limit)
    if args.output: args.output.write_text(body+"\n")
    else: print(body)

if __name__=="__main__": main()
