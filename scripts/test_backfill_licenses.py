#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "backfill_licenses.py"
spec = importlib.util.spec_from_file_location("backfill_licenses", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

repos = [
    {"repo":"x/unknown","github":{"license":"NOASSERTION","defaultBranch":"main"}},
    {"repo":"x/null","github":{"license":None,"defaultBranch":"main"}},
    {"repo":"x/known","github":{"license":"MIT","defaultBranch":"main"}},
    {"repo":"x/no-branch","github":{"license":None}},
]
seen = []
def resolver(repo, branch, token=None):
    seen.append((repo, branch, token))
    return "Apache-2.0" if repo == "x/unknown" else None

checked, changed = mod.backfill(repos, resolver, "token")
assert checked == 3
assert changed == [{"repo":"x/unknown","license":"Apache-2.0"}]
assert repos[0]["github"]["license"] == "Apache-2.0"
assert repos[1]["github"]["license"] is None
assert repos[2]["github"]["license"] == "MIT"
assert seen == [("x/unknown","main","token"),("x/null","main","token")]
print("OK: targeted license backfill tests passed")
