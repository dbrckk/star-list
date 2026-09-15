#!/usr/bin/env python3
"""Classify discovery-cache efficiency and render an actionable health report."""
import argparse
import json
from pathlib import Path


def _ratio(value, total):
    return (value / total) if total else 0.0


def analyze(stats):
    logical=max(0,int(stats.get("logicalRequests",0) or 0))
    fresh=max(0,int(stats.get("freshCacheHits",0) or 0))
    not_modified=max(0,int(stats.get("notModifiedHits",0) or 0))
    stale=max(0,int(stats.get("staleFallbacks",0) or 0))
    network=max(0,int(stats.get("networkFetches",0) or 0))
    avoidance=float(stats.get("apiCallAvoidanceRate",_ratio(fresh,logical)) or 0.0)
    body_reuse=float(stats.get("bodyReuseRate",_ratio(fresh+not_modified+stale,logical)) or 0.0)
    network_ratio=_ratio(network,logical)
    stale_ratio=_ratio(stale,logical)

    findings=[]
    severe=False
    if logical>=5 and (avoidance<0.20 or body_reuse<0.50):
        findings.append("low-cache-efficiency")
    if logical>=5 and network_ratio>=0.65 and avoidance<0.10:
        findings.append("high-network-dependence")
        severe=True
    if logical>=5 and stale_ratio>=0.15:
        findings.append("excessive-stale-fallbacks")
        severe=True

    status="degraded" if severe else "watch" if findings else "healthy"
    return {
        "status":status,
        "findings":findings,
        "metrics":{
            "logicalRequests":logical,
            "freshCacheHits":fresh,
            "notModifiedHits":not_modified,
            "staleFallbacks":stale,
            "networkFetches":network,
            "apiCallAvoidanceRate":round(avoidance,4),
            "bodyReuseRate":round(body_reuse,4),
            "networkFetchRate":round(network_ratio,4),
            "staleFallbackRate":round(stale_ratio,4),
        },
    }


def render_markdown(report):
    m=report["metrics"]
    lines=[
        "<!-- star-list-cache-health -->",
        "# Discovery cache health",
        "",
        f"Status: **{report['status']}**",
        "",
        f"- Logical requests: {m['logicalRequests']}",
        f"- Fresh cache hits: {m['freshCacheHits']}",
        f"- 304 revalidations: {m['notModifiedHits']}",
        f"- Stale fallbacks: {m['staleFallbacks']}",
        f"- Network fetches: {m['networkFetches']}",
        f"- API call avoidance: {m['apiCallAvoidanceRate']:.1%}",
        f"- Body reuse: {m['bodyReuseRate']:.1%}",
        f"- Network fetch rate: {m['networkFetchRate']:.1%}",
        f"- Stale fallback rate: {m['staleFallbackRate']:.1%}",
    ]
    if report["findings"]:
        lines += ["", "## Findings"] + [f"- `{x}`" for x in report["findings"]]
    return "\n".join(lines)+"\n"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("discovery_report",type=Path)
    ap.add_argument("--markdown-output",type=Path)
    args=ap.parse_args()
    data=json.loads(args.discovery_report.read_text())
    report=analyze(data.get("cacheStats",{}))
    if args.markdown_output:
        args.markdown_output.write_text(render_markdown(report))
    print(json.dumps(report,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
