#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "find_replacements.py"
spec = importlib.util.spec_from_file_location("find_replacements", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

bad = {"repo":"x/bad","score":8.0,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
       "github":{"stars":10,"forks":1,"archived":True,"disabled":False,"license":"MIT","pushedAt":"2020-01-01T00:00:00Z"}}
good = {"repo":"x/good","score":9.5,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
        "github":{"stars":100000,"forks":10000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2099-01-01T00:00:00Z"}}
other = {"repo":"x/other","score":9.5,"domain":"graphics","capabilities":["vector"],"platforms":["linux"],"languages":["rust"],"selfHosted":True,
         "github":{"stars":100000,"forks":10000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2099-01-01T00:00:00Z"}}

rows = mod.analyze([bad, good, other])
assert len(rows) == 1
assert rows[0]["repo"] == "x/bad"
assert rows[0]["suggestedReplacements"][0]["repo"] == "x/good"
assert rows[0]["suggestedReplacements"][0]["replacementScore"] > rows[0]["suggestedReplacements"][1]["replacementScore"]
print("OK: replacement detection tests passed")
