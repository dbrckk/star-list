#!/usr/bin/env python3
"""Regression checks for the first automated Stars review and canonical transfers."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location("star_import_pipeline", ROOT / "scripts/star_import_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

catalog = read("catalog.json")
manifest = read("imports/github-stars-2026-10-09-auto-1.json")
review = read("reports/github-stars-review-2026-10-09-reviewed.json")
report = read("reports/github-stars-review-2026-10-09-summary.json")
snapshots = (read("reports/github-stars-review-2026-10-09-metadata-1.json")["repositories"]
             + read("reports/github-stars-review-2026-10-09-metadata-2.json")["repositories"])

assert len(snapshots) == len(manifest["repositories"]) == 17
assert len(catalog["repositories"]) == report["summary"]["catalogAfter"] == 722
assert report["summary"]["admitted"] == 14
assert report["summary"]["transfersResolved"] == 3
assert report["summary"]["auditTier"] == 7

cat = {entry["repo"].lower(): entry for entry in catalog["repositories"]}
assert len(cat) == 722, "Case-insensitive GitHub identity duplicates"
snapshot_map = {entry["repo"].lower(): entry for entry in snapshots}
assert len(snapshot_map) == 17

stable_ids = [entry["githubRepositoryId"] for entry in catalog["repositories"]
              if "githubRepositoryId" in entry]
assert len(stable_ids) >= 17 and len(set(stable_ids)) == len(stable_ids)
for source in snapshots:
    entry = cat[source["repo"].lower()]
    assert entry["githubRepositoryId"] == source["id"]
    assert entry["github"] == source["github"], source["repo"]

transfers = {
    "danny-avila/LibreChat": "LibreChat-AI/LibreChat",
    "OpenBB-finance/OpenBB": "openbq-org/OpenBB",
    "KRTirtho/spotube": "team-spotube/spotube",
}
assert len(manifest["transfers"]) == len(transfers)
for former, current in transfers.items():
    assert former.lower() not in cat and current.lower() in cat
    assert cat[current.lower()]["githubRepositoryId"] == snapshot_map[current.lower()]["id"]

historic = read("history.json")["repositories"]
health_names = {entry["repo"] for entry in read("health-snapshot.json")["repositories"]}
stack_names = {name for stack in read("stacks.json")["stacks"] for name in stack["repos"]}
for former, current in transfers.items():
    assert former not in historic and former not in health_names and former not in stack_names
    assert current in historic and current in health_names
assert "openbq-org/OpenBB" in stack_names

assert len(review["repositories"]) == 14
assert len({x["repo"].lower() for x in review["repositories"]}) == 14
for record in review["repositories"]:
    source = snapshot_map[record["repo"].lower()]
    entry = cat[record["repo"].lower()]
    assert record["reviewed"] is True
    assert record["githubRepositoryId"] == source["id"]
    assert record["catalogEntry"] == entry
    assert record["github"] == entry["github"]
    candidate = {"repo": record["repo"], "key": record["repo"].lower(), "sources": ["automatic"]}
    assert pipeline.classify_candidate(candidate, record)["status"] == "accepted"

assert sum(cat[r["repo"].lower()]["tier"] == "audit" for r in review["repositories"]) == 7
assert cat["flutter-team-archive/plugins"]["github"]["archived"] is True
assert cat["flutter-team-archive/plugins"]["tier"] == "audit"
assert cat["freefq/free"]["tier"] == "audit"
assert cat["segfault42/heliosgen"]["tier"] == "audit"
assert cat["openbq-org/openbb"]["licenseEvidence"] == "verified-file"
assert cat["team-spotube/spotube"]["licenseEvidence"] == "verified-file"

import_records, malformed = pipeline.load_imports([ROOT / "imports/github-stars-2026-10-09-auto-1.json"])
assert len(import_records) == 17 and not malformed
partition = pipeline.partition_candidates(import_records, catalog)
assert len(partition["new"]) == 0
assert len(partition["already_cataloged"]) == 17

print("OK: all 17 automatic Stars accounted for; 14 admitted, 3 canonical transfers, 0 duplicates")
