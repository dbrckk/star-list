#!/usr/bin/env python3
"""Persist bounded cache-health history and derive multi-week drift signals."""
import argparse
import json
from datetime import date as date_type
from pathlib import Path
from statistics import median

SCHEMA_VERSION=1
DEFAULT_MAX_POINTS=26
ADAPTIVE_MIN_SAMPLES=4
ADAPTIVE_MAX_SAMPLES=8
ADAPTIVE_THRESHOLD=0.20


def empty_history():
    return {"schemaVersion":SCHEMA_VERSION,"points":[]}


def load_history(path):
    if path is None or not path.exists(): return empty_history()
    try:
        data=json.loads(path.read_text())
    except (OSError,json.JSONDecodeError):
        return empty_history()
    if not isinstance(data,dict) or not isinstance(data.get("points"),list):
        return empty_history()
    return {"schemaVersion":SCHEMA_VERSION,"points":[p for p in data["points"] if isinstance(p,dict)]}


def save_history(path,history):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(history,indent=2,ensure_ascii=False)+"\n")
    tmp.replace(path)


def _metric(metrics,name):
    value=metrics.get(name,0.0)
    return round(float(value or 0.0),4)


def point_from_report(report,date):
    metrics=report.get("metrics",{}) if isinstance(report,dict) else {}
    return {
        "date":str(date),
        "status":report.get("status","unknown") if isinstance(report,dict) else "unknown",
        "logicalRequests":max(0,int(metrics.get("logicalRequests",0) or 0)),
        "apiCallAvoidanceRate":_metric(metrics,"apiCallAvoidanceRate"),
        "bodyReuseRate":_metric(metrics,"bodyReuseRate"),
        "networkFetchRate":_metric(metrics,"networkFetchRate"),
        "staleFallbackRate":_metric(metrics,"staleFallbackRate"),
    }


def _point_metric(point,name):
    return float(point.get(name,0.0) or 0.0)


def _baseline_confidence(sample_size):
    score=round(min(1.0,max(0.0,sample_size/ADAPTIVE_MAX_SAMPLES)),3)
    if sample_size<ADAPTIVE_MIN_SAMPLES:
        return "insufficient-data",score
    if sample_size>=ADAPTIVE_MAX_SAMPLES:
        return "high",score
    if sample_size>=6:
        return "medium",score
    return "low",score


def adaptive_baseline(points,min_samples=ADAPTIVE_MIN_SAMPLES,max_samples=ADAPTIVE_MAX_SAMPLES,threshold=ADAPTIVE_THRESHOLD):
    history=points[:-1][-max_samples:] if points else []
    confidence,confidence_score=_baseline_confidence(len(history))
    result={
        "status":"insufficient-data",
        "sampleSize":len(history),
        "threshold":threshold,
        "confidence":confidence,
        "confidenceScore":confidence_score,
        "findings":[],
    }
    if len(history)<min_samples or not points:
        return result

    current=points[-1]
    names=("apiCallAvoidanceRate","bodyReuseRate","networkFetchRate")
    baselines={name:round(float(median([_point_metric(p,name) for p in history])),4) for name in names}
    deltas={name:round(_point_metric(current,name)-baselines[name],4) for name in names}
    findings=[]
    if deltas["apiCallAvoidanceRate"]<=-threshold:
        findings.append("below-adaptive-cache-baseline")
    if deltas["networkFetchRate"]>=threshold:
        findings.append("above-adaptive-network-baseline")
    if deltas["bodyReuseRate"]<=-threshold:
        findings.append("below-adaptive-body-reuse-baseline")

    result.update(baselines)
    result["deltas"]={name:round(value,4) for name,value in deltas.items()}
    result["status"]="anomalous" if findings else "normal"
    result["findings"]=findings
    return result


def _adaptive_severity(adaptive):
    if adaptive.get("status")!="anomalous":
        return "healthy"
    return "watch" if adaptive.get("confidence")=="low" else "degraded"


def analyze_trend(points):
    adaptive=adaptive_baseline(points)
    adaptive_severity=_adaptive_severity(adaptive)
    recent=points[-3:]
    if len(recent)<3:
        return {"direction":"insufficient-data","findings":list(adaptive["findings"]),"windowPoints":len(recent),
                "apiCallAvoidanceDelta":None,"networkFetchDelta":None,"adaptiveBaseline":adaptive,
                "adaptiveSeverity":adaptive_severity}
    first,last=recent[0],recent[-1]
    avoidance=[_point_metric(p,"apiCallAvoidanceRate") for p in recent]
    network=[_point_metric(p,"networkFetchRate") for p in recent]
    body=[_point_metric(p,"bodyReuseRate") for p in recent]
    ad=round(avoidance[-1]-avoidance[0],4)
    nd=round(network[-1]-network[0],4)
    bd=round(body[-1]-body[0],4)
    findings=[]
    if avoidance[0]>avoidance[1]>avoidance[2] and ad<=-0.20:
        findings.append("declining-cache-efficiency")
    if network[0]<network[1]<network[2] and nd>=0.20:
        findings.append("rising-network-dependence")
    if body[0]>body[1]>body[2] and bd<=-0.20:
        findings.append("declining-body-reuse")
    for finding in adaptive["findings"]:
        if finding not in findings:
            findings.append(finding)
    direction="declining" if findings else "stable"
    if not findings and avoidance[0]<avoidance[1]<avoidance[2] and ad>=0.20 and network[0]>network[1]>network[2]:
        direction="improving"
    return {"direction":direction,"findings":findings,"windowPoints":3,
            "apiCallAvoidanceDelta":ad,"networkFetchDelta":nd,"bodyReuseDelta":bd,
            "fromDate":first.get("date"),"toDate":last.get("date"),"adaptiveBaseline":adaptive,
            "adaptiveSeverity":adaptive_severity}


def update(history,current,date=None,max_points=DEFAULT_MAX_POINTS):
    if max_points<1: raise ValueError("max_points must be >= 1")
    today=str(date or date_type.today().isoformat())
    base=history if isinstance(history,dict) else empty_history()
    points=[dict(p) for p in base.get("points",[]) if isinstance(p,dict) and p.get("date")]
    point=point_from_report(current,today)
    points=[p for p in points if p.get("date")!=today]
    points.append(point)
    points.sort(key=lambda p:str(p.get("date","")))
    points=points[-max_points:]
    updated={"schemaVersion":SCHEMA_VERSION,"points":points}
    return updated,analyze_trend(points)


def render_markdown(trend):
    lines=["## Multi-week trend", "", f"Direction: **{trend.get('direction','unknown')}**"]
    if trend.get("apiCallAvoidanceDelta") is not None:
        lines += [
            f"- API call avoidance delta: {trend['apiCallAvoidanceDelta']:+.1%}",
            f"- Network fetch delta: {trend['networkFetchDelta']:+.1%}",
            f"- Body reuse delta: {trend.get('bodyReuseDelta',0):+.1%}",
        ]
    adaptive=trend.get("adaptiveBaseline",{})
    if adaptive.get("sampleSize",0)>=ADAPTIVE_MIN_SAMPLES:
        deltas=adaptive.get("deltas",{})
        lines += [
            "",
            "### Adaptive baseline",
            f"Baseline samples: {adaptive['sampleSize']}",
            f"Baseline confidence: **{adaptive['confidence']}** ({adaptive['confidenceScore']:.1%})",
            f"Adaptive severity: **{trend.get('adaptiveSeverity','healthy')}**",
            f"- API call avoidance baseline: {adaptive['apiCallAvoidanceRate']:.1%} ({deltas.get('apiCallAvoidanceRate',0):+.1%})",
            f"- Body reuse baseline: {adaptive['bodyReuseRate']:.1%} ({deltas.get('bodyReuseRate',0):+.1%})",
            f"- Network fetch baseline: {adaptive['networkFetchRate']:.1%} ({deltas.get('networkFetchRate',0):+.1%})",
            f"- Baseline status: **{adaptive['status']}**",
        ]
    if trend.get("findings"):
        lines += ["", "### Trend findings"]+[f"- `{x}`" for x in trend["findings"]]
    return "\n".join(lines)+"\n"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("history",type=Path)
    ap.add_argument("current_report",type=Path)
    ap.add_argument("--write",action="store_true")
    ap.add_argument("--max-points",type=int,default=DEFAULT_MAX_POINTS)
    ap.add_argument("--trend-output",type=Path)
    ap.add_argument("--markdown-output",type=Path)
    args=ap.parse_args()
    if args.max_points<1: ap.error("--max-points must be >= 1")
    history=load_history(args.history)
    current=json.loads(args.current_report.read_text())
    updated,trend=update(history,current,max_points=args.max_points)
    if args.write: save_history(args.history,updated)
    if args.trend_output: args.trend_output.write_text(json.dumps(trend,indent=2,ensure_ascii=False)+"\n")
    if args.markdown_output: args.markdown_output.write_text(render_markdown(trend))
    print(json.dumps(trend,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
