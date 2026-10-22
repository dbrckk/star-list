This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*.{py,js,mjs,cjs,ts,tsx,jsx,java,kt,kts,gd,groovy,gradle,toml,json,yaml,yml,sql,sh}
- Files matching these patterns are excluded: .ai/**, **/node_modules/**, **/.gradle/**, **/build/**, **/dist/**, **/.venv/**, **/__pycache__/**, **/.pytest_cache/**, **/.git/**, **/coverage/**, **/*.lock, **/*.min.js, **/*.map, assets/**, art/**, art_sources/**, marketing/**, colab/**, kaggle/**, discovery-cache.json, health-snapshot.json, history.json
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
admit_github_stars.py
agent_skill_discovery.py
analyze_cache_health.py
analyze_coverage.py
audit_agent_skill_sources.py
audit_catalog_quality.py
backfill_github_ids.py
backfill_licenses.py
build_discovery_watchlist.py
catalog_domain_evidence.py
catalog_stats.py
check_readme_evidence_freshness.py
detect_health_drift.py
discover_candidates.py
evaluate_candidates.py
filter_discovery_memory.py
find_replacements.py
health_score.py
infer_selection_guidance.py
portfolio_daily.py
portfolio_failure_diagnostics.py
recommend.py
refresh_github_metadata.py
render_discovery_issue.py
render_health_issue.py
report_domain_coverage.py
star_import_pipeline.py
sync_github_stars.py
test_analyze_coverage.py
test_auto_stars_admission.py
test_backfill_licenses.py
test_cache_health_history.py
test_cache_health.py
test_catalog_domain_evidence.py
test_catalog_quality.py
test_degraded_inputs.py
test_discover_candidates.py
test_discovery_cache_stats.py
test_discovery_cache.py
test_discovery_memory.py
test_discovery_watchlist.py
test_documentation.py
test_evaluate_candidates.py
test_find_replacements.py
test_full_catalog_availability.py
test_health_drift.py
test_health_score.py
test_history.py
test_json_contracts.py
test_other_domain_expansion.py
test_pipeline_integration.py
test_readme_domain_evidence.py
test_readme_evidence_freshness.py
test_recommend.py
test_refresh_github_metadata.py
test_render_discovery_issue.py
test_render_health_issue.py
test_selection_guidance.py
test_star_import_pipeline.py
test_sync_github_stars.py
test_verify_catalog_evidence.py
update_cache_health_history.py
update_history.py
validate_catalog.py
validate_json_contract.py
validate_websites.py
verify_catalog_evidence.py
```

# Files

## File: admit_github_stars.py
```python
#!/usr/bin/env python3
"""Admit every accessible starred repository into the catalog, conservatively.

New entries receive an audit tier until a human or richer analysis verifies
license terms, suitability, and production readiness. Never silently skip a
Star or save a partly built catalog.
"""
⋮----
DOMAINS = (
CATEGORIES = {
⋮----
def classify(meta)
⋮----
text = " ".join([
⋮----
def get_repo(repo, token=None, opener=SAFE_GITHUB_HTTP.open, sleeper=time.sleep)
⋮----
"""Fetch full repository metadata, with bounded retry and canonical ID check."""
⋮----
url = "https://api.github.com/repos/" + repo
headers = {
⋮----
result = json.load(response)
⋮----
raw_delay = exc.headers.get("Retry-After", str(2 ** attempt))
⋮----
delay = min(20, max(0, float(raw_delay)))
⋮----
delay = float(2 ** attempt)
⋮----
def catalog_entry(meta)
⋮----
repo = meta.get("full_name")
⋮----
repo_id = meta.get("id")
⋮----
license_data = meta.get("license")
license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else None
⋮----
license_id = None
⋮----
def count(key)
⋮----
value = meta.get(key)
⋮----
branch = meta.get("default_branch")
⋮----
branch = "unknown"  # Nonempty schema value; indexed entries retain an explicit metadata gap.
domain = classify(meta)
language = meta.get("language")
languages = [language.lower()] if isinstance(language, str) and language.strip() else []
description = meta.get("description")
guidance = [re.sub(r"\s+", " ", description).strip()[:200]] if isinstance(description, str) and description.strip() else []
topics = meta.get("topics")
capabilities = [x[:80] for x in topics if isinstance(x, str) and x.strip()][:12] if isinstance(topics, list) else []
⋮----
def manifest_stable_ids(manifest, report)
⋮----
"""Verify that all identity rows belong to the exact read-only Stars scan."""
⋮----
summary = report.get("summary")
⋮----
expected_new = report.get("newRepositories")
⋮----
ids = {}
owners = {}
⋮----
key = normalize_repo(name)
rid = row.get("githubRepositoryId")
⋮----
key = normalize_repo(star["repo"])
⋮----
def admit(catalog, stars, fetcher, known_star_ids=None)
⋮----
"""Reconcile by both canonical name and permanent ID; fail on any ambiguity."""
old = catalog.get("repositories")
⋮----
by_name = {normalize_repo(x["repo"]): x.get("githubRepositoryId") for x in old}
by_id = {x["githubRepositoryId"] for x in old if type(x.get("githubRepositoryId")) is int}
⋮----
fresh = []
already = 0
transfers = []
⋮----
rid = star.get("githubRepositoryId")
recorded_id = by_name.get(key)
⋮----
# Re-check even when a stale read-only report reached admission:
# a recycled owner/name is not the same GitHub repository.
⋮----
meta = fetcher(star["repo"])
entry = catalog_entry(meta)
⋮----
canonical = normalize_repo(entry["repo"])
⋮----
previous_id = by_name[canonical]
⋮----
result = dict(catalog)
# Do not mutate the caller's loaded catalog before all checks pass.
entries = [dict(row) for row in old] + sorted(fresh, key=lambda r: r["repo"].lower())
enriched = 0
⋮----
rows_by_name = {normalize_repo(row["repo"]): row for row in entries}
rows_by_id = {
⋮----
key = normalize_repo(original_name)
⋮----
entry = rows_by_name.get(key)
⋮----
# An existing repository may have transferred to this new
# owner/name while preserving its stable ID.
⋮----
recorded_id = entry.get("githubRepositoryId")
⋮----
occupied = rows_by_id.get(rid)
⋮----
def main(argv=None)
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args(argv)
⋮----
report = json.loads(args.sync_report.read_text(encoding="utf-8"))
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
⋮----
# A report lists only missing Stars. The manifest provides the complete
# snapshot, and admission operates on a report produced in the same job.
stars = report.get("newRepositories")
⋮----
known_star_ids = None
⋮----
manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
known_star_ids = manifest_stable_ids(manifest, report)
token = os.environ.get("GITHUB_TOKEN")
```

## File: agent_skill_discovery.py
```python
#!/usr/bin/env python3
"""Offline, read-only Skill Issue skill discovery for repository agents.

A directory entry or an upstream repository is not authority to execute
unreviewed SKILL.md instructions, install scripts or network commands.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "agent-skills.json"
SKILL_ISSUE_URL = "https://skill-issue.in/"
VALID_DOMAINS = {
⋮----
def word_set(value: str) -> set[str]
⋮----
def load_skills() -> dict
⋮----
data = json.loads(CATALOG.read_text(encoding="utf-8"))
⋮----
directory = data.get("directory")
⋮----
skills = data.get("skills")
⋮----
ids = set()
⋮----
identifier = row.get("id")
⋮----
name = row.get("name")
description = row.get("description")
⋮----
repo = row.get("sourceRepository")
⋮----
expected = "https://github.com/" + repo
⋮----
url = urlsplit(expected)
⋮----
# The exact SKILL.md path is independently confirmed on a pinned
# upstream revision, rather than delegating review to a mutable repo root.
⋮----
"""Rank skill *references* by declared domain and concrete repo labels.

    Never treat broad README prose as verified compatibility and never return
    shell installers or instructions for agent execution.
    """
source = load_skills()
⋮----
words = set().union(*(word_set(term) for term in terms))
selected = []
⋮----
matched_domains = sorted(set(item["domains"]) & domains)
matched_tags = sorted(set(item["tags"]) & words)
⋮----
languages = {x.casefold() for x in item["languages"]}
⋮----
# An explicit relevant framework term is stronger evidence than
# GitHub's single primary language, but general domain is not.
explicit = {"react", "nextjs", "remotion"} & set(matched_tags)
⋮----
score = 8 * len(matched_domains) + 5 * len(matched_tags)
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args()
⋮----
catalog = load_skills()
matched = recommend_skills(word_set(args.query), set(args.domain), language=args.language, limit=args.top)
output = {
```

## File: analyze_cache_health.py
```python
#!/usr/bin/env python3
"""Classify discovery-cache efficiency and render an actionable health report."""
⋮----
def _ratio(value, total)
⋮----
def analyze(stats)
⋮----
logical=max(0,int(stats.get("logicalRequests",0) or 0))
fresh=max(0,int(stats.get("freshCacheHits",0) or 0))
not_modified=max(0,int(stats.get("notModifiedHits",0) or 0))
stale=max(0,int(stats.get("staleFallbacks",0) or 0))
network=max(0,int(stats.get("networkFetches",0) or 0))
avoidance=float(stats.get("apiCallAvoidanceRate",_ratio(fresh,logical)) or 0.0)
body_reuse=float(stats.get("bodyReuseRate",_ratio(fresh+not_modified+stale,logical)) or 0.0)
network_ratio=_ratio(network,logical)
stale_ratio=_ratio(stale,logical)
⋮----
findings=[]
severe=False
⋮----
severe=True
⋮----
status="degraded" if severe else "watch" if findings else "healthy"
⋮----
def render_markdown(report)
⋮----
m=report["metrics"]
lines=[
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
data=json.loads(args.discovery_report.read_text())
report=analyze(data.get("cacheStats",{}))
```

## File: analyze_coverage.py
```python
#!/usr/bin/env python3
"""Analyze catalog coverage and surface functional blind spots."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"catalog.json"
⋮----
def analyze(repos, min_domain=3, min_capability=2)
⋮----
domains=Counter(r.get("domain","other") for r in repos)
caps=Counter(c for r in repos for c in r.get("capabilities",[]))
healthy_domains=Counter()
healthy_caps=Counter()
by_domain=defaultdict(list)
⋮----
h=health_score(r)
usable=h["status"] not in {"inactive","weak"} if h["score"] is not None else True
⋮----
domain_gaps=[]
⋮----
healthy=healthy_domains[domain]
⋮----
capability_gaps=[]
⋮----
healthy=healthy_caps[cap]
⋮----
concentration=[]
⋮----
total=len(items)
top_tier=sum(r.get("tier") in {"core","recommended"} for r in items)
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
repos=json.loads(CATALOG.read_text()).get("repositories",[])
```

## File: audit_agent_skill_sources.py
```python
#!/usr/bin/env python3
"""Check immutable upstream SKILL.md links without executing remote instructions.

Offline mode validates local pinned-source contracts only. Online mode checks
GitHub API *file metadata*, never imports, executes or trusts remote SKILL.md.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "star-list-pinned-skill-source-audit/1.0"
MAX_RESPONSE = 500_000
⋮----
class RejectRedirect(HTTPRedirectHandler)
⋮----
"""Never forward a GitHub bearer token to a redirected URL."""
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
HTTP = build_opener(RejectRedirect())
⋮----
def inspect_source(row: dict, token: str) -> tuple[str, str]
⋮----
"""Check the pinned SKILL.md file metadata; never read/parse its instructions."""
⋮----
path = "/".join(quote(part, safe="") for part in row["sourcePath"].split("/"))
url = ("https://api.github.com/repos/" + quote(owner, safe="")
headers = {
⋮----
payload = response.read(MAX_RESPONSE + 1)
⋮----
value = json.loads(payload.decode("utf-8"))
⋮----
def make_report(*, online: bool, token: str) -> dict
⋮----
rows = load_skills()["skills"]
entries = []
⋮----
counts = {status: sum(item["status"] == status for item in entries)
complete = online and counts["unavailable"] == 0 and counts["unchecked"] == 0
⋮----
def markdown(report: dict) -> str
⋮----
counts = report["counts"]
lines = [
failures = [e for e in report["entries"] if e["status"] in ("missing", "invalid", "unavailable")]
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args()
report = make_report(online=args.online, token=os.environ.get("GITHUB_TOKEN", ""))
data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
```

## File: audit_catalog_quality.py
```python
#!/usr/bin/env python3
"""Audit catalog maintenance debt without mutating catalog.json."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
SEVERITY_ORDER = {"review": 0, "info": 1}
⋮----
def _age_days(value, now)
⋮----
pushed = datetime.fromisoformat(value.replace("Z", "+00:00"))
⋮----
pushed = pushed.replace(tzinfo=timezone.utc)
⋮----
def analyze(repos, stale_days=730, now=None)
⋮----
now = now or datetime.now(timezone.utc)
findings = []
guidance_fields = ("bestFor", "avoidWhen", "alternatives", "complements")
⋮----
def add(repo, severity, code, message)
⋮----
name = entry.get("repo", "<unknown>")
gh = entry.get("github")
⋮----
tier = entry.get("tier")
lifecycle = entry.get("lifecycle")
⋮----
code = f"archived-{lifecycle or 'indexed'}-retained"
label = lifecycle or "indexed"
⋮----
age = _age_days(gh.get("pushedAt"), now)
⋮----
license_name = gh.get("license")
⋮----
license_status = entry.get("licenseStatus")
status_messages = {
⋮----
severity_counts = Counter(row["severity"] for row in findings)
code_counts = Counter(row["code"] for row in findings)
guidance = {
⋮----
def render_markdown(report)
⋮----
summary = report["summary"]
lines = [
⋮----
review = [row for row in report["findings"] if row["severity"] == "review"]
info = [row for row in report["findings"] if row["severity"] == "info"]
⋮----
rendered = "\n".join(lines) + "\n"
# GitHub issue bodies have a size limit. Always retain complete JSON
# evidence while presenting a bounded, prioritized public review: the
# review-level rows precede informational findings.
max_bytes = 60_000
⋮----
cost = len((line + "\n").encode("utf-8"))
⋮----
bounded = "\n".join(kept) + "\n"
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Audit catalog maintenance debt.")
⋮----
args = parser.parse_args()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
report = analyze(repos, stale_days=args.stale_days)
```

## File: backfill_github_ids.py
```python
#!/usr/bin/env python3
"""Reconcile missing permanent GitHub repository IDs, without changing curation.

Read-only by default. --write needs an authenticated GitHub token, validates
current canonical names and existing IDs, and writes catalog.json atomically.
404/renamed repositories remain unresolved; an API outage blocks all writes.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
NAME = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
⋮----
def github_metadata(repo: str, token: str) -> dict | None
⋮----
"""One bounded GitHub metadata lookup for an already curated repository."""
⋮----
url = "https://api.github.com/repos/" + quote(owner, safe="") + "/" + quote(name, safe="")
headers = {
⋮----
raw = res.read(150_001)
⋮----
value = json.loads(raw.decode("utf-8"))
⋮----
def reconcile(data: dict, token: str | None = None, *, max_requests: int = 250) -> tuple[dict, dict]
⋮----
rows = data.get("repositories")
⋮----
owner_by_id = {}
names = set()
missing = []
⋮----
canonical = row["repo"].casefold()
⋮----
rid = row.get("githubRepositoryId")
⋮----
report = {
⋮----
repo = row["repo"]
⋮----
response = github_metadata(repo, token)
⋮----
actual = response.get("full_name")
stable_id = response.get("id")
⋮----
previous = owner_by_id.get(stable_id)
⋮----
def main() -> int
⋮----
ap = argparse.ArgumentParser(description=__doc__)
⋮----
args = ap.parse_args()
⋮----
token = (os.environ.get("GITHUB_TOKEN") or "").strip() if args.write else None
⋮----
data = json.loads(CATALOG.read_text(encoding="utf-8"))
⋮----
output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
⋮----
# Do not publish a partially serialized catalog; preserve all other
# repository fields, order, selection policy and metadata unchanged.
⋮----
temporary = Path(tmp.name)
```

## File: backfill_licenses.py
```python
#!/usr/bin/env python3
"""Backfill only unknown repository licenses using conservative root-file detection."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN = {None, "", "NOASSERTION"}
⋮----
def backfill(repos, resolver, token=None)
⋮----
changed = []
checked = 0
⋮----
github = repo.get("github")
⋮----
name = repo.get("repo")
branch = github.get("defaultBranch")
⋮----
detected = resolver(name, branch, token)
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Backfill unknown licenses without refreshing unrelated metadata.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
token = os.environ.get("GITHUB_TOKEN")
⋮----
result = {"checked": checked, "changed": len(changed), "licenses": changed}
```

## File: build_discovery_watchlist.py
```python
#!/usr/bin/env python3
"""Turn coverage gaps into a deterministic GitHub discovery watchlist."""
⋮----
def build(report, max_items=30)
⋮----
items=[]
⋮----
priority=100 if x.get("severity")=="critical" else 70
⋮----
priority=95 if x.get("severity")=="critical" else 65
⋮----
dedup={}
⋮----
key=(x["kind"],x["target"])
⋮----
rows=sorted(dedup.values(),key=lambda x:(-x["priority"],x["kind"],x["target"]))[:max_items]
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
```

## File: catalog_domain_evidence.py
```python
#!/usr/bin/env python3
"""Evidence-only advisory routing for catalog entries whose domain is unknown.

Neither text clues nor GitHub descriptions authorize installation or execution.
Keep named/curated domains authoritative and do not overwrite catalog metadata.
"""
⋮----
# Only explicit technical capabilities or unambiguous *task phrases* qualify.
# Generic words ("AI", "agent", "web", "app", "automation") never qualify alone.
CAPABILITY_DOMAIN_SIGNALS = {
# A title/description is *less* trustworthy than a structured capability.
# Match task-specific phrases, never freeform single-topic descriptions.
DESCRIPTION_DOMAIN_PHRASES = {
⋮----
def _normalized(value)
⋮----
@lru_cache(maxsize=1)
def _readme_source_map()
⋮----
"""Read a fixed, manually reviewed set of upstream blob references."""
path = Path(__file__).resolve().parents[1] / "catalog-readme-evidence.json"
data = json.loads(path.read_text(encoding="utf-8"))
⋮----
def reviewed_readme_source(item)
⋮----
"""Return reviewed evidence only for the exact catalog identity.

    All claims are advisory. Upstream README text is never executed or parsed as
    instructions; this file records reviewed descriptions and immutable hashes.
    """
⋮----
name = item.get("repo")
record = _readme_source_map().get(name)
⋮----
def reviewed_readme_task_terms(item)
⋮----
"""Task-specific hints only, never proof of software compatibility."""
record = reviewed_readme_source(item)
⋮----
def advisory_domain_evidence(item)
⋮----
"""Return {domain: supporting evidence strings}, for advisory routing only."""
domain = item.get("domain")
⋮----
caps = {str(v).strip().casefold() for v in (
# Structured capability labels may be overly broad or inaccurate. The
# result is therefore advisory even if the label is an exact match.
description = _normalized(" ".join(
# Exact ecosystem tokens from the repository slug are robust enough for
# advisory routing, but ambiguous brand/project names are not.
slug = str(item.get("repo") or "").split("/")[-1]
slug_terms = {x for x in re.split(r"[^a-z0-9]+", slug.lower()) if x}
slug_source = slug.casefold()
⋮----
specific_slug_technology = {
evidence = {}
⋮----
match = sorted(slug_terms & lexemes)
⋮----
hits = sorted(caps & signals)
⋮----
matches = [s for s in phrases if re.search(
⋮----
signal = "readme:" + record["path"] + "@" + record["blobSha"]
```

## File: catalog_stats.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def main()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
domains = Counter(r.get("domain", "other") for r in repos)
tiers = Counter(r.get("tier", "unknown") for r in repos)
languages = Counter(x for r in repos for x in r.get("languages", []))
platforms = Counter(x for r in repos for x in r.get("platforms", []))
capabilities = Counter(x for r in repos for x in r.get("capabilities", []))
self_hosted = sum(r.get("selfHosted") is True for r in repos)
scores = [r.get("score", 0) for r in repos if isinstance(r.get("score"), (int, float))]
by_domain = defaultdict(list)
⋮----
report = {
```

## File: check_readme_evidence_freshness.py
```python
#!/usr/bin/env python3
"""Read-only freshness check for manually reviewed GitHub README blob evidence.

A changed README requires a new review; it never authorizes automatic changes
to a catalog or target repository.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog-readme-evidence.json"
⋮----
def inspect(record, fetch_repo=gh.fetch, fetch_contents=gh.fetch_contents, token=None)
⋮----
name = record["repository"]
entry = {"repo": name, "recordedBlobSha": record["blobSha"],
⋮----
info = fetch_repo(name, token=token)
⋮----
payload = fetch_contents(name, path=record["path"], token=token)
sha = payload.get("sha") if isinstance(payload, dict) else None
⋮----
size = (len(sources) + batch_size - 1) // batch_size
⋮----
start = batch_index * batch_size
selected = sources[start:start + batch_size]
findings = [inspect(x, fetch_repo, fetch_contents, token) for x in selected]
counts = {k: sum(x["status"] == k for x in findings)
⋮----
def main()
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
data = json.loads(args.manifest.read_text(encoding="utf-8"))
⋮----
result = check(data["sources"], batch_size=args.batch_size,
⋮----
encoded = json.dumps(result,ensure_ascii=False,indent=2)+"\n"
```

## File: detect_health_drift.py
```python
#!/usr/bin/env python3
"""Compare repository health snapshots and detect meaningful deterioration."""
⋮----
def index(snapshot)
⋮----
rows = snapshot.get("repositories", snapshot if isinstance(snapshot, list) else [])
⋮----
def detect(previous, current, drop=10.0)
⋮----
findings = []
⋮----
before = old.get(repo)
⋮----
delta = round(b-a, 1)
status_changed = before.get("status") != now.get("status")
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
findings=detect(json.loads(args.previous.read_text()), json.loads(args.current.read_text()), args.drop)
```

## File: discover_candidates.py
```python
#!/usr/bin/env python3
"""Execute discovery watchlist against GitHub Search API and rank novel candidates."""
⋮----
# Preserve the existing injectable transport for offline cache tests, but
# never forward the authenticated discovery token on cross-origin redirects.
urlopen = SAFE_GITHUB_HTTP.open
⋮----
API="https://api.github.com/search/repositories"
REPO_API="https://api.github.com/repos/{}"
CACHE_SCHEMA_VERSION=1
DEFAULT_SEARCH_CACHE_TTL_HOURS=24
DEFAULT_METADATA_CACHE_TTL_HOURS=336
DEFAULT_SEARCH_STALE_MAX_HOURS=168
DEFAULT_METADATA_STALE_MAX_HOURS=2160
DEFAULT_CACHE_RETENTION_HOURS=max(DEFAULT_SEARCH_STALE_MAX_HOURS,DEFAULT_METADATA_STALE_MAX_HOURS)
⋮----
def empty_cache()
⋮----
def empty_cache_stats()
⋮----
def finalize_cache_stats(stats)
⋮----
result=dict(stats or empty_cache_stats())
total=max(0,int(result.get("logicalRequests",0)))
fresh=max(0,int(result.get("freshCacheHits",0)))
reused=(fresh + max(0,int(result.get("notModifiedHits",0))) +
⋮----
def _stat(stats, key)
⋮----
def load_cache(path)
⋮----
data=json.loads(path.read_text())
⋮----
def prune_cache(cache, max_age_seconds, now=None)
⋮----
now=time.time() if now is None else now
removed=0
⋮----
fetched=entry.get("fetchedAt") if isinstance(entry,dict) else None
⋮----
def save_cache(path, cache, max_age_seconds=DEFAULT_CACHE_RETENTION_HOURS*3600, now=None)
⋮----
tmp=path.with_name(path.name+".tmp")
⋮----
def _cache_entry(cache, url)
⋮----
entry=cache.get("entries",{}).get(url) if isinstance(cache,dict) else None
⋮----
fetched=entry.get("fetchedAt")
⋮----
def _headers_dict(headers)
⋮----
def _header_value(headers, name)
⋮----
wanted=name.lower()
⋮----
def cache_get(cache, url, ttl_seconds, now=None)
⋮----
entry=_cache_entry(cache,url)
⋮----
def cache_get_stale(cache, url, max_age_seconds, now=None)
⋮----
age=max(0,now-entry["fetchedAt"])
⋮----
def cache_put(cache, url, data, headers, now=None)
⋮----
def _api_result(data, headers, source, return_source)
⋮----
def _stale_result(cache, url, stale_max_seconds, now, return_source)
⋮----
stale=cache_get_stale(cache,url,stale_max_seconds,now) if cache is not None else None
⋮----
def _conditional_headers(headers, cache, url)
⋮----
result=dict(headers or {})
⋮----
etag=_header_value(entry.get("headers",{}),"etag")
⋮----
def _not_modified_result(cache, url, response_headers, now, return_source)
⋮----
merged_headers=dict(entry.get("headers",{}) or {})
⋮----
data=entry.get("data")
⋮----
def api_json(url, headers, attempts=4, cache=None, ttl_seconds=0, stale_max_seconds=0, now=None, return_source=False, stats=None)
⋮----
# A future caller must not pass its GitHub bearer token to an arbitrary
# initial URL. The shared opener independently blocks redirected tokens.
⋮----
parsed = urlsplit(url)
⋮----
hit=cache_get(cache,url,ttl_seconds,now)
⋮----
request_headers=_conditional_headers(headers,cache,url) if cache is not None and ttl_seconds>0 else dict(headers or {})
last=None
⋮----
data=json.load(res)
response_headers=_headers_dict(res.headers)
⋮----
last=e
⋮----
not_modified=_not_modified_result(cache,url,e.headers,now,return_source)
⋮----
transient=e.code in (403,429,500,502,503,504)
⋮----
stale=_stale_result(cache,url,stale_max_seconds,now,return_source)
⋮----
retry=e.headers.get("Retry-After")
reset=e.headers.get("X-RateLimit-Reset")
⋮----
wait=min(60,float(retry))
⋮----
wait=max(1,min(60,float(reset)-time.time()))
⋮----
wait=min(30,2**attempt)
⋮----
def fetch(query, token=None, per_page=10, cache=None, ttl_seconds=0, stale_max_seconds=0, return_source=False, stats=None)
⋮----
params=urlencode({"q":query,"sort":"stars","order":"desc","per_page":per_page})
headers={"Accept":"application/vnd.github+json","User-Agent":"star-list-discovery","X-GitHub-Api-Version":"2022-11-28"}
⋮----
def enrich(repo, token=None, cache=None, ttl_seconds=0, stale_max_seconds=0, stats=None)
⋮----
stale_endpoints=[]
⋮----
out={"topics":data.get("topics",[]),"watchers":data.get("subscribers_count",0),
⋮----
link=response_headers.get("Link","")
⋮----
m=re.search(r'[?&]page=(\\d+)>; rel="last"',link)
⋮----
def score(item, priority)
⋮----
stars=max(0,item.get("stargazers_count",0)); forks=max(0,item.get("forks_count",0))
popularity=min(25,5*math.log10(stars+1)); ecosystem=min(15,4*math.log10(forks+1))
metadata=5 if item.get("license") else 2
⋮----
candidates={}
errors=[]
stale_sources=[]
stats=empty_cache_stats()
⋮----
name=item.get("full_name")
⋮----
row={"repo":name,"url":item.get("html_url"),"description":item.get("description"),
⋮----
rows=sorted(candidates.values(),key=lambda x:(-x["discoveryScore"],-x["stars"],x["repo"].lower()))
⋮----
enriched=enrich(row["repo"],token,cache,metadata_ttl_seconds,metadata_stale_max_seconds,stats=stats)
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
ttls=(args.search_cache_ttl_hours,args.metadata_cache_ttl_hours,args.search_stale_max_hours,args.metadata_stale_max_hours)
⋮----
known={r["repo"] for r in json.loads(args.catalog.read_text()).get("repositories",[])}
cache=load_cache(args.cache) if args.cache else None
result=discover(
```

## File: evaluate_candidates.py
```python
#!/usr/bin/env python3
"""Evaluate discovered repositories into accept/review/reject buckets."""
⋮----
ACCEPT_THRESHOLD=80.0
REVIEW_THRESHOLD=55.0
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _integer(value,default=0)
⋮----
def _dict_list(value)
⋮----
def age_days(value, now=None)
⋮----
try: dt=datetime.fromisoformat(value.replace("Z","+00:00"))
⋮----
def text_fit(repo)
⋮----
text=((repo.get("repo") or "")+" "+(repo.get("description") or "")+" "+(repo.get("language") or "")).lower()
targets=_dict_list(repo.get("matchedTargets",[]))
⋮----
hits=0
⋮----
words=str(m.get("target","")).lower().replace("_"," ").replace("-"," ").split()
⋮----
def _bounded(value)
⋮----
def decision_for_score(score)
⋮----
score=_number(score)
⋮----
def evaluation_confidence(repo)
⋮----
release=repo.get("latestRelease")
signals=(
coverage=sum(signals)/len(signals)
⋮----
def score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues)
⋮----
fit_score=fit*65+min(20,topic_hits*10)+min(15,max(0,len(matches)-1)*7.5)
⋮----
if days is None: activity=0
elif days<=90: activity=70
elif days<=365: activity=55
elif days<=730: activity=35
else: activity=10
⋮----
if stars>=5000: adoption=55
elif stars>=1000: adoption=45
elif stars>=500: adoption=35
elif stars>=100: adoption=25
elif stars>=20: adoption=10
else: adoption=0
⋮----
fork_ratio=forks/max(1,stars) if stars else 0.0
⋮----
maturity=25 if repo.get("license") else 0
⋮----
maintenance=50
⋮----
issue_ratio=open_issues/max(1,stars)
⋮----
def evaluate(repo, now=None)
⋮----
score=_number(repo.get("discoveryScore",0))
reasons=[]
days=age_days(repo.get("pushedAt"),now)
⋮----
fit=text_fit(repo)
⋮----
created_days=age_days(repo.get("createdAt"),now)
⋮----
release=repo.get("latestRelease") or {}
release_days=age_days(release.get("publishedAt"),now) if isinstance(release,dict) else None
⋮----
stars=max(0,_integer(repo.get("stars",0)))
contributors=repo.get("contributors")
⋮----
topics={str(x).lower() for x in repo.get("topics",[]) if x is not None} if isinstance(repo.get("topics",[]),list) else set()
matches=_dict_list(repo.get("matchedTargets",[]))
target_words={w for m in matches for w in str(m.get("target","")).lower().replace("_","-").split("-") if w}
topic_hits=len(topics & target_words)
⋮----
watchers=max(0,_integer(repo.get("watchers",0)))
⋮----
forks=max(0,_integer(repo.get("forks",0)))
open_issues=max(0,_integer(repo.get("openIssues",0)))
⋮----
score=round(max(0,min(100,score)),1)
confidence=evaluation_confidence(repo)
decision=decision_for_score(score)
⋮----
decision="review"
⋮----
breakdown=score_breakdown(repo,fit,days,created_days,release_days,stars,contributors,topic_hits,matches,watchers,forks,open_issues)
⋮----
def evaluate_all(data, now=None)
⋮----
rows=[]
repositories=data.get("repositories",[]) if isinstance(data,dict) else []
⋮----
counts={k:sum(x["decision"]==k for x in rows) for k in ("accept","review","reject")}
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
```

## File: filter_discovery_memory.py
```python
#!/usr/bin/env python3
"""Suppress unchanged reviewed/rejected candidates while preserving meaningful changes."""
⋮----
SCHEMA_VERSION=1
⋮----
def empty_memory()
⋮----
def load_memory(path)
⋮----
data=json.loads(path.read_text())
⋮----
candidates={str(name):entry for name,entry in data["candidates"].items() if isinstance(entry,dict)}
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _targets(value)
⋮----
def fingerprint(r)
⋮----
def apply(data,memory,score_delta=5.0)
⋮----
if not isinstance(memory,dict): memory=empty_memory()
known=memory.get("candidates")
⋮----
known={}
memory={"schemaVersion":SCHEMA_VERSION,"candidates":known}
⋮----
visible=[]; suppressed=0
now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
repositories=data.get("repositories",[]) if isinstance(data,dict) else []
⋮----
name=r.get("repo")
⋮----
fp=fingerprint(r); old=known.get(name)
changed=True
⋮----
oldfp=old.get("fingerprint",{})
if not isinstance(oldfp,dict): oldfp={}
score_changed=abs(_number(fp.get("score"))-_number(oldfp.get("score")))>=score_delta
changed=(fp.get("decision")!=oldfp.get("decision") or fp.get("pushedAt")!=oldfp.get("pushedAt")
⋮----
base=data if isinstance(data,dict) else {}
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("memory",type=Path)
⋮----
args=ap.parse_args()
data=json.loads(args.evaluated.read_text()); memory=load_memory(args.memory)
⋮----
text=json.dumps(filtered,indent=2,ensure_ascii=False)+"\n"
```

## File: find_replacements.py
```python
#!/usr/bin/env python3
"""Detect unhealthy catalog entries and rank safer in-catalog replacements."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def overlap(a, b)
⋮----
def replacement_score(source, candidate)
⋮----
health = health_score(candidate)
⋮----
domain = 1.0 if source.get("domain") == candidate.get("domain") else 0.0
caps = overlap(source.get("capabilities"), candidate.get("capabilities"))
roles = overlap(source.get("roles"), candidate.get("roles"))
⋮----
platforms = overlap(source.get("platforms"), candidate.get("platforms"))
languages = overlap(source.get("languages"), candidate.get("languages"))
self_hosted = 1.0 if source.get("selfHosted") == candidate.get("selfHosted") else 0.0
fit = 35*domain + 25*caps + 12*roles + 8*platforms + 5*languages + 5*self_hosted
⋮----
def analyze(repos, threshold=55, top=3)
⋮----
findings = []
⋮----
health = health_score(source)
⋮----
candidates = []
⋮----
result = replacement_score(source, candidate)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser(description="Find catalog repositories that should be reviewed or replaced.")
⋮----
args = ap.parse_args()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
findings = analyze(repos, args.threshold, args.top)
```

## File: health_score.py
```python
#!/usr/bin/env python3
"""Deterministic repository health scoring from catalog + refreshed GitHub metadata."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
def _number(value, default=0.0)
⋮----
try: result=float(value)
⋮----
def age_days(pushed_at, now=None)
⋮----
dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
⋮----
now = now or datetime.now(timezone.utc)
⋮----
def health_score(repo, now=None)
⋮----
gh = repo.get("github")
⋮----
days = age_days(gh.get("pushedAt"), now)
freshness = 35.0
reasons = []
⋮----
freshness = 12.0; reasons.append("push-date-missing")
elif days <= 30: freshness = 35.0
elif days <= 90: freshness = 32.0
elif days <= 365: freshness = 25.0
elif days <= 730: freshness = 14.0; reasons.append("stale-over-1y")
else: freshness = 4.0; reasons.append("stale-over-2y")
⋮----
stars = max(0.0, _number(gh.get("stars", 0)))
forks = max(0.0, _number(gh.get("forks", 0)))
adoption = min(25.0, 5.0 * math.log10(stars + 1))
ecosystem = min(15.0, 4.0 * math.log10(forks + 1))
quality = max(0.0, min(20.0, 2.0 * _number(repo.get("score", 0))))
metadata = 5.0 if gh.get("license") else 2.0
total = round(min(100.0, freshness + adoption + ecosystem + quality + metadata), 1)
status = "healthy" if total >= 75 else "watch" if total >= 55 else "weak"
⋮----
def main()
⋮----
repos = json.loads(CATALOG.read_text()).get("repositories", [])
rows = [{"repo":r["repo"], **health_score(r)} for r in repos]
```

## File: infer_selection_guidance.py
```python
#!/usr/bin/env python3
"""Backfill conservative selection guidance from existing curated catalog metadata."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
⋮----
CAPABILITY_BEST_FOR = {
⋮----
DOMAIN_AVOID_WHEN = {
⋮----
def _humanize(value)
⋮----
def infer_guidance(repo)
⋮----
caps = list(dict.fromkeys(repo.get("capabilities", []) + repo.get("roles", [])))
best = []
domain = repo.get("domain")
⋮----
phrase = "retrieval and persistent-memory workflows"
⋮----
phrase = "agent memory and context retention"
⋮----
phrase = "knowledge retention and reference workflows"
⋮----
phrase = "stateful memory workflows"
⋮----
phrase = "vector search and embedding retrieval"
⋮----
phrase = "vector animation"
⋮----
phrase = CAPABILITY_BEST_FOR.get(cap)
⋮----
avoid = []
⋮----
domain_avoid = DOMAIN_AVOID_WHEN.get(repo.get("domain"))
⋮----
def enrich(repos, tier="recommended", refresh_inferred=False)
⋮----
changed = 0
⋮----
missing_best = not repo.get("bestFor")
missing_avoid = not repo.get("avoidWhen")
refresh = refresh_inferred and repo.get("guidanceSource") == "inferred"
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Backfill deterministic selection guidance.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
changed = enrich(data.get("repositories", []), tier=args.tier, refresh_inferred=args.refresh_inferred)
```

## File: portfolio_daily.py
```python
#!/usr/bin/env python3
"""Daily, read-only portfolio discovery with optional idempotent Production-OS handoff.

The GitHub Actions token can scan public repositories but cannot write to
other repositories. Actual code integration is delegated to a qualified
Production-OS worker, never treated as completed by this script.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
ALLOWED_LICENSES = {
KEYWORDS = {
GENERIC = {"ai", "agent", "dev", "web", "python", "typescript", "app", "open", "tools", "github", "repo"}
STOPWORDS = {
# Portfolio READMEs include French; shared prose must never be treated as
# evidence that a developer tool is genuinely compatible with an app.
⋮----
# Engine-specific runtime components are not drop-in replacements for
# incompatible engines. This is a hard gate, not a soft relevance penalty.
ENGINE_CONFLICTS = {
# A repository *using* an engine should not be told to integrate that engine's
# complete source tree as if it were a missing application dependency.
EXISTING_ENGINE_SOURCES = {
⋮----
# These are independently running coding agents/CLIs, not importable runtime
# libraries. Recommend them as development-side adapters, never dispatch a
# native app dependency just because the implementation language matches.
EXTERNAL_CODING_AGENT_CLIS = frozenset({
⋮----
MANIFESTS = ("pyproject.toml", "package.json", "requirements.txt", "Cargo.toml",
⋮----
# Only exact, declared dependency names may contribute framework evidence to
# skill references. Do not tokenize package scripts, README prose or arbitrary
# package names: none is an authorization to execute an upstream skill.
SKILL_FRAMEWORK_PACKAGES = {
⋮----
def package_skill_signals(filename: str, content: str) -> tuple[set[str], set[str]]
⋮----
"""Conservative framework hints from exact manifest dependencies only."""
⋮----
# Flutter is a real SDK dependency, not just a mention of the word
# "flutter" in an arbitrary description, comment or README. We only
# recognize the standard, indented pubspec dependency declaration.
section = ""
flutter_dependency = False
⋮----
line = raw_line.split("#", 1)[0].rstrip()
⋮----
indentation = len(line) - len(line.lstrip(" "))
⋮----
section = line[:-1] if line.endswith(":") else ""
⋮----
flutter_dependency = line.strip() == "flutter:"
⋮----
parsed = json.loads(content)
⋮----
dependencies = parsed.get(field)
⋮----
evidence = SKILL_FRAMEWORK_PACKAGES.get(name.strip().lower())
⋮----
class SameOriginRedirect(HTTPRedirectHandler)
⋮----
"""Never forward GitHub or Production-OS bearer tokens to another origin."""
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
original = urlparse(req.full_url)
destination = urlparse(newurl)
⋮----
SAFE_HTTP = build_opener(SameOriginRedirect())
⋮----
parsed = urlparse(url)
⋮----
# Retrying a POST after a timeout or 5xx can submit the same autonomous
# work twice if the first response was lost. Reconcile the authoritative
# inventory on the next scan instead of replaying a mutating request.
⋮----
max_attempts = 1
headers = {
⋮----
body = json.dumps(data).encode() if data is not None else None
⋮----
# Render free instances may need time to wake up. Restrict the
# extended timeout to the approved control-plane host; keep
# ordinary GitHub catalog lookups bounded at 25 seconds.
request_timeout = 60 if parsed.hostname == "production-os1.onrender.com" else 25
⋮----
raw = response.read(3_000_000)
⋮----
def github_repos(owner: str, token: str, portfolio_token: str) -> list[dict]
⋮----
base = (API + "/user/repos?affiliation=owner&sort=full_name&per_page=100"
result = []
⋮----
separator = "&" if "?" in base else "?"
rows = request_json(base + separator + "page=" + str(page), portfolio_token or token)
⋮----
def file_text(full_name: str, path: str, token: str, *, limit: int = 5500) -> str
⋮----
endpoint = API + "/repos/" + "/".join(quote(part, safe="") for part in full_name.split("/")) + "/contents/" + quote(path, safe="")
payload = request_json(endpoint, token)
⋮----
raw = base64.b64decode(payload.get("content", ""), validate=False)
⋮----
def project_profile(repo: dict, token: str) -> dict
⋮----
name = repo["full_name"]
description = str(repo.get("description") or "")
topics = repo.get("topics") or []
intro = file_text(name, "README.md", token, limit=2800)
dependency_text = ""
⋮----
first_manifest = ""
inspected_manifests = {}
⋮----
# Preserve the first-manifest behavior used by the existing repository
# integration ranker. Only skill discovery inspects more than one
# exact, known manifest; it never executes manifest scripts.
value = file_text(name, filename, token, limit=12000)
⋮----
first_manifest = filename
⋮----
# Polyglot projects often have a root pyproject.toml or Cargo.toml
# alongside frontend/mobile source. Those first manifests must not hide
# a real React/Flutter dependency from advisory Skill Issue discovery.
⋮----
# A missing manifest encountered before the primary one was already
# checked. Avoid a second GitHub GET, including duplicate 404s.
value = inspected_manifests.get(filename)
⋮----
# GitHub's own primary-language metadata is sufficient to identify
# GDScript-specific skill references without trusting README instructions.
primary_language = str(repo.get("language") or "").casefold()
⋮----
# Luau is distinct from general Lua. Do not infer Roblox merely
# because an arbitrary project happens to use Lua scripting.
⋮----
overview = " ".join([repo["name"], description, " ".join(topics), intro[:1200]])
label_text = " ".join([repo["name"], description, " ".join(topics)]).lower()
domains = set(infer_domains(tokens(label_text)))
⋮----
# Exact manifest package declarations and GitHub's primary Luau/GDScript
# language are stronger evidence than a missing or generic repo name.
# Reuse only the bounded, already-inspected technology signals, without
# tokenizing arbitrary dependency scripts or README instructions.
trusted_technology_terms = {
⋮----
project_terms = tokens(overview) | (skill_terms & trusted_technology_terms)
# README may refine a known project, but never invent a domain solely from README.
⋮----
def review_blockers(item: dict) -> list[str]
⋮----
"""Explain why a relevant catalog entry is advisory, never auto-dispatchable.

    A curated catalog row deserves task-relevance evaluation even when its
    licensing, maintenance or deployment maturity does not qualify it for
    autonomous code changes. This function preserves the existing strict
    integration policy and exposes its decisions instead of silently dropping
    most of the catalog before matching.
    """
gh = item.get("github") or {}
blockers = []
⋮----
def eligible(item: dict) -> bool
⋮----
"""Strict integration admission: do not widen with discovery coverage."""
⋮----
def is_reference_candidate(tool: dict) -> bool
⋮----
"""Keep demos, samples and architecture guides out of auto-implementation."""
guidance = " ".join(str(v).lower() for v in (tool.get("bestFor") or []))
capabilities = set(str(v).strip().lower() for v in (tool.get("capabilities") or []))
slug = str(tool.get("repo") or "").lower()
reference_clues = (
⋮----
# Generic README prose is not proof that a package provides an actionable
# capability. Such matches may stay in the review report, but cannot trigger
# an autonomous dependency integration solely because languages match.
WEAK_CAPABILITY_TERMS = {
⋮----
name = repo["full_name"].lower()
domains = set(profile["domains"])
⋮----
# Record each identity before considering any domain/score threshold.
# A rejected candidate remains accounted for in the scan evidence.
⋮----
target_identity = repo["name"].lower()
godot_target = profile["language"] == "gdscript" or "godot" in target_identity
roblox_target = profile["language"] in {"lua", "luau"} or "roblox" in target_identity
existing_engine_sources = set(EXISTING_ENGINE_SOURCES["godot"]) if godot_target else set()
# Engine alternatives are replacement *platforms*, not dependencies.
# Derive them from curated alternative relationships, rather than chasing
# arbitrary incompatible engine names by hand. Roblox has no cataloged
# engine-source counterpart, so exclude both sides of declared engine
# alternatives (e.g. godotengine/godot <-> libgdx/libgdx).
engine_pairs = [
excluded_engine_sources = existing_engine_sources | {
⋮----
matches = []
⋮----
slug = str(tool.get("repo") or "")
⋮----
blockers = review_blockers(tool)
domain_evidence = advisory_domain_evidence(tool)
⋮----
advisory_routing = tool.get("domain") not in domains
⋮----
# Exact hyphenated capability labels are meaningful metadata. Splitting
# them for advisory term matching recovers "video editing" vs
# "video-editing" without changing global tokenizer semantics.
capability_labels = " ".join(str(x) for x in (tool.get("capabilities") or []))
terms = (tokens(slug) | tokens(capability_labels)
exact_slug_terms = {
# Keep the standard tokenizer unchanged: only explicit high-specificity
# name evidence may split a hyphenated repository technology label.
⋮----
shared = sorted((profile["terms"] & terms) - GENERIC - STOPWORDS)
⋮----
# A lone match must describe an actual candidate capability/use case,
# not merely an organization name (or an incidental README word).
capability_terms = (
explicit_slug_match = bool(set(shared) & exact_slug_terms)
readme_term_match = bool(
# High-specificity technology tokens such as ESP32/agent-sdk in a
# repository slug can establish advisory relevance even when GitHub
# has no topics or description. This NEVER permits native dispatch.
⋮----
# Ignore the installed engine source and explicit substitute
# engines. Continue recommending compatible plugins/addons.
⋮----
slug_name = slug.rsplit("/", 1)[-1].lower()
⋮----
candidate_languages = set(str(x).lower() for x in (tool.get("languages") or []))
# Missing language metadata is unknown compatibility, not native support.
languages_match = bool(profile["language"]) and profile["language"] in candidate_languages
score = score_repo(tool, profile["terms"], domains, set(), set())
# Inferred domains remain review-only; rank specific evidence against
# a slightly lower threshold so valid indexed tools don't vanish just
# because the original catalog domain was "other".
threshold = 28 if advisory_routing else 35
⋮----
# An incidental word such as "workflows" from a README must not
# qualify an otherwise unrelated same-language library for dispatch.
concrete_terms = (
capability_overlap = bool(set(shared) & concrete_terms)
# An MCP control bridge runs alongside Roblox Studio. Its Lua/Luau
# plugin is not a library embedded in the published game: external
# Studio access, an MCP client and a development host are required.
# Do not spend autonomous runtime-integration budget on this match.
capabilities = {str(v).strip().lower() for v in (tool.get("capabilities") or [])}
external_studio_bridge = (
# A language mismatch remains adapter-review; same-language tools
# with only prose overlap remain discoverable but require review.
mode = (
policy_review = list(blockers)
⋮----
# A native library gets precedence over example applications and adapters.
# Otherwise a reference app can fill the three slots before a usable SDK.
priority = {"native": 0, "capability-review": 1,
⋮----
INTEGRATION_TOKEN_BUDGET = 90000
⋮----
def count_active_integrations(projects: list[dict]) -> int
⋮----
"""Only in-flight portfolio jobs occupy coding-worker capacity slots."""
⋮----
def busy_integration_targets(projects: list[dict]) -> set[str]
⋮----
"""Do not launch concurrent or review-conflicting changes into one repo.

    Unlike the fleet's worker cap, REVIEW_REQUIRED also blocks the target:
    that result may still have a branch/PR awaiting review. DONE and failed
    attempts are handled independently by versioned tracking/quarantine.
    """
⋮----
def unresolved_failed_v2_integrations(projects: list[dict]) -> list[dict]
⋮----
"""Failed v2 jobs still needing review after any successful v3 recovery.

    The v2 record itself remains NEEDS_ATTENTION forever: a later completed
    v3 recovery for the same exact candidate supersedes it for admission and
    reporting. Other failed candidate identities remain quarantined.
    """
recovered = set()
⋮----
marker = re.search(
⋮----
unresolved = []
⋮----
def count_failed_v2_integrations(projects: list[dict]) -> int
⋮----
"""Count only still-unresolved failed high-budget jobs."""
⋮----
def count_failed_v3_integrations(projects: list[dict]) -> int
⋮----
"""A terminal v3 retry is an operator-review gate, not an open slot.

    Never automatically launch unrelated jobs after a final recovery already
    failed. First establish real model/worker capacity and review the result.
    """
⋮----
def count_launches_on_utc_date(projects: list[dict], utc_day: str) -> int
⋮----
"""Account for the UTC launch quota, regardless of an API timestamp offset.

    Call only after verified_managed_projects has validated timezone-aware
    timestamps. A local-calendar comparison can admit extra launches around
    midnight even when the per-UTC-day safety quota is already exhausted.
    """
⋮----
def verified_managed_projects(payload: object) -> list[dict]
⋮----
"""Fail closed unless the inventory can safely authorize more launches.

    Production-OS returns *every* star-list tracking record, with a known
    lifecycle state and timestamp. An unknown state must not be interpreted
    as idle capacity; a duplicate marker or missing timestamp must not make
    retries look safe.
    """
⋮----
projects = payload.get("projects")
⋮----
known_states = {"ACTIVE", "REVIEW_REQUIRED", "NEEDS_ATTENTION", "DONE"}
seen_markers: set[str] = set()
⋮----
goal = project.get("final_goal")
⋮----
repo = project.get("repository")
⋮----
status = project.get("status")
⋮----
timestamp = project.get("created_at")
⋮----
created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
⋮----
def public_integration_status(target: str, projects: list[dict]) -> list[dict]
⋮----
"""Expose only validated status enums for an already-public repository.

    Never echo the worker instruction, project identifiers, private repository
    names, task diagnostics or model-provider traces into the public issue.
    """
results = []
accepted = {"ACTIVE", "QUEUED", "RUNNING", "NEEDS_ATTENTION",
⋮----
goal = str(project.get("final_goal") or "")
markers = re.findall(r"starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])", goal)
⋮----
status = str(project.get("status") or "").upper().replace("-", "_")
⋮----
def integration_marker(target: str, candidate: dict, version: int = 2) -> str
⋮----
identity = hashlib.sha256(
⋮----
"""Quarantine only targets with an *eligible* v3 retry still available.

    A previous candidate may later be rejected as a reference application,
    incompatible capability or low-value match. Keep the failed v2 record
    visible, but do not permanently block an unrelated qualified native tool.
    Existing v3 records (any status) are non-retryable.
    """
available: dict[str, set[str]] = {}
⋮----
target = str(project.get("repository") or "").lower()
⋮----
def launch_integration(url: str, token: str, target: str, candidate: dict, *, version: int = 2)
⋮----
marker = integration_marker(target, candidate, version=version)
goal = (
⋮----
def confirmed_launch(result: object, target: str, candidate: dict, *, version: int = 2) -> bool
⋮----
"""Accept only a bound, persistent, idempotent Production-OS receipt.

    An HTTP success containing {"project": {}} is not proof of the requested
    launch. Wrong-target acknowledgements must not consume a fleet slot or
    permit the dispatcher to submit more work under an inconsistent inventory.
    """
⋮----
identifier = project.get("id")
⋮----
def render_markdown(report: dict) -> str
⋮----
summary = report["summary"]
lines = ["<!-- star-list-portfolio-daily -->", "# Daily star-list portfolio discovery", "",
⋮----
review_gates = site.get("reviewGates") or ["third-party-source-review"]
# Preserve explicit model/provider risk information in the public
# review; do not treat a discovered model as installable software.
⋮----
"""Suggest websites only for applicable project domains, never as code.

    Game projects benefit from an art-direction atlas and reviewed baseline
    planning/QA/prototyping sources even when their GitHub metadata is sparse.
    Hosted services remain references: no credentials, installs or spending.
    """
domains = set(profile.get("domains") or [])
metadata_terms = tokens(" ".join([
⋮----
# GitHub labels often contain hyphens and have no description/topics;
# split names for advisory website matching, not native integration.
⋮----
# Use explicit repository *labels* to recover domains for reference-only
# sources, without modifying the stricter native-code integration profile.
⋮----
# Hosted social-marketing suggestions require explicit GitHub label
# evidence (not README prose, a generic 'promo' name, or an AI label).
# This does not affect the stricter GitHub native-code dispatch domains.
# Vision-language research is not necessarily marketed with the word
# "AI": OCR/screenshot/vision labels still qualify for *advisory* model
# discovery. No domain promotion reaches native-code integration.
⋮----
# A pipeline called "asset-forge" can be truly graphical while its sparse
# GitHub description and language do not disclose that. Require the asset
# name plus specific README capability evidence (not generic prose)
# before considering graphics/media model references. README text is
# untrusted and may influence advisory relevance only, never dispatch.
visual_terms = {
⋮----
candidates = recommend_websites(metadata_terms, domains, limit=None)
chosen = [
⋮----
game_art = next((site for site in candidates if site["id"] == "game-art-style"), None)
⋮----
# Give real game projects the visual atlas without letting generic
# wording rank it above relevant websites for unrelated projects.
chosen = [game_art] + [site for site in chosen if site["id"] != "game-art-style"]
jupiter_art = next((site for site in candidates if site["id"] == "jupiter-game-art-style"), None)
⋮----
chosen = [site for site in chosen if site["id"] != "jupiter-game-art-style"]
⋮----
# 3D motion/rigging tools need concrete project metadata evidence, not
# simply a generic game label; game-art-style retains top priority.
# Explicit 3D engine names qualify for an advisory motion library review.
# They do NOT establish FBX rig compatibility or grant MCP credentials.
motion_signals = {"mocap", "rigging", "rigged", "skeletal", "blender",
character_animation = {"character", "characters"} & metadata_terms and "animation" in metadata_terms
⋮----
pinoc = next((site for site in candidates if site["id"] == "viggle-pinoc-mcp"), None)
⋮----
position = 1 if chosen and chosen[0]["id"] == "game-art-style" else 0
chosen = [site for site in chosen if site["id"] != "viggle-pinoc-mcp"]
⋮----
# The ranking considers every curated website; retain the disposition
# for those that fail the project/task/licence-safe reference filters.
⋮----
site_domains = set(site["domains"])
required = set(site.get("portfolioRequiredSignals") or [])
⋮----
reason = "skill-directory-discovered-for-every-target"
decision = "directory-review"
⋮----
reason = "project-domain-mismatch"
decision = "not-relevant"
⋮----
reason = "specialist-project-signals-unmatched"
⋮----
reason = "no-specific-project-signal"
⋮----
def main() -> int
⋮----
ap = argparse.ArgumentParser()
⋮----
args = ap.parse_args()
⋮----
gh_token = os.getenv("GITHUB_TOKEN", "")
portfolio_token = os.getenv("PORTFOLIO_GITHUB_TOKEN", "")
operator_token = os.getenv("PRODUCTION_OS_OPERATOR_TOKEN", "")
service = os.getenv("PRODUCTION_OS_URL", "https://production-os1.onrender.com")
report = {"generated_at": datetime.now(timezone.utc).isoformat(), "owner": args.owner,
⋮----
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))["repositories"]
catalog_ids = {str(item["repo"]) for item in catalog}
⋮----
websites = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))["websites"]
website_ids = {str(site["id"]) for site in websites}
⋮----
target = request_json(API + "/repos/" + args.repository, portfolio_token or gh_token)
⋮----
source = [target]
⋮----
source = github_repos(args.owner, gh_token, portfolio_token)
# The central issue is public: never publish private target metadata there.
source = [repo for repo in source if not repo.get("private")]
⋮----
target = repo["full_name"]
row = {"repository": target, "status": "scanned", "suggestions": [], "website_references": [],
⋮----
profile = project_profile(repo, portfolio_token or gh_token)
⋮----
# All targets receive the directory; skill matches are based
# on owned GitHub labels and language, never README instructions.
skill_terms = word_set(" ".join([
skill_domains = (set(profile.get("domains") or [])
⋮----
# Owned GitHub metadata only: reference sites never become
# installable tools, and unrelated domain/prose matches are out.
⋮----
repo_checked = set(row["source_assessment"]["repositories"])
websites_checked = set(row["source_assessment"]["websites"])
⋮----
# Incomplete decision traces must not trigger any mutation.
⋮----
# Discovery must be complete before starting any potentially mutating
# managed project. A per-repository read error is not a partial success.
scan_complete = not report["errors"]
⋮----
dispatched = 0
# A lost response does not prove a POST was rejected. Stop sending other
# candidates until the next run reconciles a fresh managed-project inventory.
launch_outcome_uncertain = False
active_integrations = None
failed_v2_integrations = None
failed_v3_integrations = None
available_slots = None
launches_today = None
⋮----
# Validate the origin before even the read-only authenticated request.
parsed_service = urlparse(service)
⋮----
operator_token = ""
⋮----
# Always prioritize highest-confidence matches, irrespective of repository order.
queue = sorted(((item["score"], row, item) for row in report["projects"]
⋮----
existing = request_json(service.rstrip("/") + "/v1/managed-projects/integration-inventory", operator_token)
already = verified_managed_projects(existing)
⋮----
existing = None
⋮----
# Public issue rows originate only from public GitHub discovery.
# Never include private managed-project names or instruction text.
⋮----
# Limit active portfolio work across multiple scheduled/manual runs,
# not merely the number of launches in this one workflow run.
active_integrations = count_active_integrations(already)
failed_v2_integrations = count_failed_v2_integrations(already)
failed_v3_integrations = count_failed_v3_integrations(already)
busy_targets = busy_integration_targets(already)
# Failed projects are quarantined instead of occupying all
# capacity slots forever. While failures remain, admit at most
# ONE distinct project per UTC day and only with an idle portfolio
# worker. This avoids both deadlock and unlimited paid/free-token
# retries from scans triggered repeatedly by GitHub events.
unresolved_failures = unresolved_failed_v2_integrations(already)
failed_targets = recoverable_failure_targets(
# Historical failures for candidates now disqualified remain
# counted and reported; they cannot hold a target hostage forever.
# The global one-launch-per-day cap still applies whenever a
# historical v2 failure remains unresolved.
⋮----
current_day = report["generated_at"][:10]
launches_today = count_launches_on_utc_date(already, current_day)
available_slots = (
⋮----
available_slots = min(
# The final automatic recovery version has already failed.
# Until operators establish working capacity and review outcomes,
# further autonomous submissions only consume scarce free tokens.
# Continue full discovery, reporting and inventory reconciliation.
⋮----
available_slots = 0
# Reevaluate a previously failed compatible candidate before
# consuming the single daily slot on an unrelated new project.
# A v3 marker is distinct and can be submitted only once.
⋮----
# Existing work and earlier successful dispatches in this same
# run must not modify one target repository concurrently.
⋮----
failed_marker = integration_marker(row["repository"], item)
recovery_marker = integration_marker(row["repository"], item, version=3)
matching_failure = any(
⋮----
result = launch_integration(
⋮----
launch_outcome_uncertain = True
⋮----
marker = integration_marker(row["repository"], item)
previous = integration_marker(row["repository"], item, version=1)
⋮----
old = next(
# Do not duplicate active/reviewable jobs. Allow exactly one
# idempotent higher-budget restart when a v1 job has failed.
is_recovery = False
⋮----
status = str(old.get("status") or "").upper().replace("-", "_")
⋮----
is_recovery = True
⋮----
result = launch_integration(service, operator_token, row["repository"], item)
```

## File: portfolio_failure_diagnostics.py
```python
#!/usr/bin/env python3
"""Operator-only, read-only diagnosis of failed public star-list integrations.

Do not copy worker goals, error messages, project IDs, job keys, private repos,
tokens or URLs from Production-OS into a public GitHub Actions artifact.
"""
⋮----
PUBLIC_FAILED_TARGETS = frozenset({
# This O(1)-query index replaces the global production inbox, which eagerly
# materializes hundreds of unrelated project statuses before search filtering.
# Only an authenticated operator receives per-project diagnostic IDs.
ENDPOINT = (
TRACKING = re.compile(r"(?<![a-z0-9])starlist-integration-v([123])-[0-9a-f]{24}(?![0-9a-f])")
CATEGORIES = (
WORKFLOW_STATES = frozenset({
VALIDATION_STATES = frozenset({
⋮----
def safe_state(raw: object, allowed: frozenset[str]) -> str
⋮----
value = raw.strip().lower() if isinstance(raw, str) else ""
⋮----
def failure_category(outcome: object) -> str
⋮----
# Scan free text internally only; NEVER persist or print it.
⋮----
message = outcome.get("summary")
⋮----
content = message[:8000].lower()
⋮----
def safe_public_failure(item: object) -> dict | None
⋮----
target = item.get("repository")
⋮----
goal = item.get("final_goal")
marker = TRACKING.search(goal) if isinstance(goal, str) else None
⋮----
outcome = item.get("outcome")
outcome = outcome if isinstance(outcome, dict) else {}
runtime = item.get("runtime")
runtime = runtime if isinstance(runtime, dict) else {}
commits = outcome.get("commit_shas")
commits_count = min(20, len(commits)) if isinstance(commits, list) else 0
⋮----
def task_failure_evidence(detail: object) -> dict
⋮----
"""Summarize failed workflow tasks without exposing source text or identifiers."""
workflow = detail.get("current_workflow") if isinstance(detail, dict) else None
tasks = workflow.get("tasks") if isinstance(workflow, dict) else None
⋮----
failed = [task for task in tasks if isinstance(task, dict)
# A terminal project without any terminal task is missing evidence, not
# proof that a deep task diagnosis has succeeded.
⋮----
category = "unknown"
⋮----
result = task.get("result")
⋮----
fields = [result.get(key) for key in (
evidence = result.get("evidence")
⋮----
# All raw fields are classified in memory only; none are persisted.
description = " ".join(value[:1000] for value in fields if isinstance(value, str))
category = failure_category({"summary": description})
⋮----
final = failed[-1] if failed else {}
attempts = final.get("attempts")
budget = final.get("max_attempts")
exhausted = (attempts >= budget if type(attempts) is int
result = final.get("result") if isinstance(final.get("result"), dict) else {}
evidence = result.get("evidence") if isinstance(result.get("evidence"), dict) else {}
known_result_keys = (
known_evidence_keys = (
⋮----
def add_deep_task_diagnostics(result: dict, inbox: object, token: str) -> dict
⋮----
"""Inspect public failed v2 and v3 projects with operator privileges.

    Internal project IDs are used only in the request path, never in output.
    A missing/mismatched detail makes the diagnosis incomplete, not successful.
    """
⋮----
items = inbox.get("items")
⋮----
selected = {}
ambiguous = set()
⋮----
record = safe_public_failure(item)
⋮----
# v2 and v3 on the same target are distinct projects and must both
# be inspected; only duplicate identities within a version are unsafe.
identity = (record["target"], record["tracking_version"])
⋮----
checked_v2 = 0
checked_v3 = 0
⋮----
item = selected.get(identity)
identifier = item.get("project_id") if isinstance(item, dict) else None
⋮----
response = request_json(
project = response.get("project") if isinstance(response, dict) else None
⋮----
raw_goal = str(project.get("final_goal") or "")
expected_goal = str(item.get("final_goal") or "")
actual = TRACKING.search(raw_goal)
expected = TRACKING.search(expected_goal)
⋮----
# The lightweight tracking index intentionally has no outcome.
# Populate delivery/validation evidence only from this separately
# identity-verified project detail, never assume zero delivery.
verified_detail = safe_public_failure(project)
⋮----
deeper = task_failure_evidence(project)
⋮----
# Fail closed on terminal v3 evidence as well: it is the final allowed
# recovery, and its failure must be understood before further admission.
⋮----
def inventory_diagnostic_inbox(payload: object) -> dict
⋮----
"""Convert a complete operator-only index into filtered-inbox structure.

    Never copy raw worker instructions into artifacts. The server itself
    redacts tracking goals; this in-memory conversion keeps only the fields
    needed to fetch the four public failed v2 project details.
    """
⋮----
rows = payload.get("projects")
total = payload.get("total_count")
⋮----
items = []
⋮----
# An incomplete privileged index cannot prove absence of a job.
⋮----
def public_diagnostics(payload: object) -> dict
⋮----
summary = payload.get("summary")
items = payload.get("items")
⋮----
matching = summary.get("matching")
⋮----
rows = [record for item in items if (record := safe_public_failure(item)) is not None]
# The public issue previously verified exactly these four unresolved v2 targets.
v2_targets = [row["target"] for row in rows if row["tracking_version"] == "v2"]
found = set(v2_targets)
# Multiple failures for the same target and version cannot safely be
# attributed by repository alone. A v2 and v3 pair is expected and valid.
unique_v2_targets = len(v2_targets) == len(found)
v3_targets = [row["target"] for row in rows if row["tracking_version"] == "v3"]
unique_v3_targets = len(v3_targets) == len(set(v3_targets))
⋮----
def main() -> int
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
# Always create a secret-free artifact, including when Render is sleeping,
# an operator credential is missing, or an authenticated read times out.
# The previous early-return behavior concealed why a diagnosis failed.
result = {
token = os.environ.get("PRODUCTION_OS_OPERATOR_TOKEN", "")
⋮----
stage = "inbox"
⋮----
inbox = inventory_diagnostic_inbox(
result = public_diagnostics(inbox)
stage = "task-details"
result = add_deep_task_diagnostics(result, inbox, token)
⋮----
# Never echo network exception text or the private API response:
# both can contain backend details or credential-bearing URLs.
⋮----
# The log and artifact contain only allowlisted public names, enums and
# counters. Unavailable and incomplete diagnoses still exit nonzero.
```

## File: recommend.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
STACKS = ROOT / "stacks.json"
HISTORY = ROOT / "history.json"
WEBSITES = ROOT / "websites.json"
⋮----
DOMAIN_ALIASES = {
TIER_BONUS = {"core": 1.0, "recommended": 0.6, "specialized": 0.25, "indexed": -0.4}
LEVEL = {"low": 0, "medium": 1, "high": 2}
GUIDANCE_WEIGHT = {"curated": 1.0, "inferred": 0.55}
SPECIALIZED_INFERRED_WEIGHT = 0.35
⋮----
def norm(s)
⋮----
def tokens(s)
⋮----
def load()
⋮----
data = json.loads(CATALOG.read_text())
stacks = json.loads(STACKS.read_text()) if STACKS.exists() else {"stacks": []}
⋮----
def infer_domains(qtokens)
⋮----
domains = {DOMAIN_ALIASES[t] for t in qtokens if t in DOMAIN_ALIASES}
# "AI" alone is generic. In an explicitly media, graphics, marketing, or
# writing task, it should not add a spurious coding-agent domain.
explicit_agents = {"agent", "agents", "coding", "code", "dev"}
⋮----
# Generic connective words in curator prose are not evidence that a website
# applies to a project (e.g. "and" in both a TTS description and art guidance).
WEBSITE_MATCH_STOPWORDS = frozenset(
⋮----
def website_review_gates(site)
⋮----
"""Stable, auditable reasons a curated web resource needs separate review.

    These are discovery metadata only, not install instructions or a grant of
    commercial image/model rights. All web resources remain non-executable.
    """
gates = []
resource_type = site.get("type")
reuse = site.get("reuse")
⋮----
# Rewriting output is never guaranteed to retain names, dates, numbers,
# quotations, formatting or source language. Label these constraints
# independently from a licence or hosted compute review.
⋮----
def recommend_websites(qtokens, domains, limit=5, include_unmatched=False)
⋮----
"""Rank non-GitHub references separately from code integration candidates.

    This remains advisory: no site can be auto-dispatched as a dependency.
    Repository-specific hard filters have no meaning for inspiration pages.
    """
data = json.loads(WEBSITES.read_text(encoding="utf-8"))
ranked = []
⋮----
site_domains = set(site["domains"])
matched_domains = sorted(site_domains & domains)
baseline_domains = sorted(set(site.get("portfolioBaselineDomains", [])) & domains)
matched_tags = sorted(qtokens & set(site["tags"]))
matched_text = sorted((qtokens & tokens(
⋮----
score = (12 * len(matched_domains) + 10 * len(matched_tags)
⋮----
# A verified documentation endpoint is reference metadata only;
# the recommender never connects or authorizes paid MCP tools.
⋮----
def activity_adjustment(r)
⋮----
gh = r.get("github")
⋮----
pushed = gh.get("pushedAt")
⋮----
dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
days = max(0, (datetime.now(timezone.utc) - dt).days)
⋮----
@lru_cache(maxsize=8192)
def trend_adjustment(repo_name)
⋮----
pts=json.loads(HISTORY.read_text()).get("repositories",{}).get(repo_name,[])
⋮----
recent=pts[-5:] if len(pts)>=5 else pts
⋮----
days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
⋮----
days=max(1,7*(len(recent)-1))
def delta(k)
⋮----
stars_week=(sd*7/days) if sd is not None else 0.0
forks_week=(fd*7/days) if fd is not None else 0.0
momentum=max(-3.0,min(3.0, stars_week/50.0)) + max(-1.0,min(1.0, forks_week/10.0))
⋮----
momentum=round(max(-6.0,min(6.0,momentum)),3)
reason="declining" if momentum<=-2 else "improving" if momentum>=2 else "growing" if momentum>0.5 else "stable"
⋮----
def guidance_weight(r)
⋮----
source = r.get("guidanceSource")
⋮----
def ranking_review_gates(r)
⋮----
"""Rank everything, but expose the reasons an entry requires review."""
⋮----
def metadata_review_gates(r)
⋮----
"""Report factual gaps without guessing about hosting or licensing."""
⋮----
def score_repo(r, qtokens, requested_domains, required_caps, excluded_caps)
⋮----
caps = set(r.get("capabilities", [])) | set(r.get("roles", []))
⋮----
rtoks = tokens(" ".join([
# Exact task tokens from manually reviewed upstream README blobs improve
# only advisory relevance. They do not elevate tier or integration trust.
⋮----
lexical = len(qtokens & rtoks) / max(1, len(qtokens))
cap_match = len(required_caps & caps) / max(1, len(required_caps)) if required_caps else 0.0
domain_evidence = advisory_domain_evidence(r)
domain_match = 1.0 if requested_domains and requested_domains & domain_evidence.keys() else 0.0
quality = max(0.0, min(1.0, r.get("score", 0) / 10.0))
tier = TIER_BONUS.get(r.get("tier"), 0.0)
best_for = tokens(" ".join(r.get("bestFor", [])))
best_match = len(qtokens & best_for) / max(1, len(qtokens)) if best_for else 0.0
guidance = guidance_weight(r)
s = 34*cap_match + 22*domain_match + 18*lexical + 12*guidance*best_match + 10*quality + 4*max(0.0, tier)
⋮----
avoid = tokens(" ".join(r.get("avoidWhen", [])))
⋮----
health = health_score(r)
⋮----
def explain_repo(r, qtokens, domains, required_caps)
⋮----
best = tokens(" ".join(r.get("bestFor", [])))
reasons = []
matched_domains = sorted(domains & advisory_domain_evidence(r).keys())
⋮----
matched_caps = sorted(required_caps & caps)
⋮----
matched_terms = sorted(qtokens & (tokens(r.get("repo", "")) | caps | best))
⋮----
# Generic words can occur in unrelated stacks. They cannot establish a fit
# on their own (e.g. "AI video" must not select a coding-agent stack).
STACK_GENERIC_TERMS = frozenset(
⋮----
def choose_stack(stacks, qtokens, domains, allowed_names=None)
⋮----
domain_match = st.get("domain") in domains
⋮----
title_terms = tokens(st.get("name", ""))
goal_terms = tokens(st.get("goal", ""))
significant = (qtokens & (title_terms | goal_terms)) - STACK_GENERIC_TERMS
# Require a strong named match, or two independent task-specific
# signals. Notes cannot be evidence: they often describe caveats,
# alternatives or unrelated technologies.
title_words = norm(st.get("name", "")).split()
anchor = next((word for word in title_words if word not in STACK_GENERIC_TERMS), None)
anchored = anchor is not None and anchor in qtokens
⋮----
score = 4 * len(significant) + (3 if domain_match else 0) + (2 if anchored else 0)
⋮----
def infer_alternatives(source, repos, top=3, allowed_names=None)
⋮----
candidates = []
⋮----
result = replacement_score(source, candidate)
⋮----
def infer_complements(source, stacks, repo_by_name, top=4, allowed_names=None)
⋮----
seen = set()
complements = []
⋮----
members = stack.get("repos", [])
⋮----
candidate = repo_by_name.get(name)
⋮----
health = health_score(candidate)
⋮----
def resolve_relations(source, repos, stacks, repo_by_name, allowed_names=None)
⋮----
# Curated links are suggestions, not exemptions from the user's constraints.
def usable(names)
⋮----
seen = {source["repo"]}
result = []
⋮----
explicit_alternatives = usable(source.get("alternatives", []))
explicit_complements = usable(source.get("complements", []))
alternatives = explicit_alternatives or infer_alternatives(source, repos, allowed_names=allowed_names)
complements = explicit_complements or infer_complements(source, stacks, repo_by_name, allowed_names=allowed_names)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser(description="Recommend repositories from star-list catalog.")
⋮----
archived_filter = ap.add_mutually_exclusive_group()
⋮----
indexed_filter = ap.add_mutually_exclusive_group()
⋮----
args = ap.parse_args()
⋮----
repo_by_name = {r["repo"]: r for r in repos}
qtokens = tokens(args.query)
domains = set(args.domain) or infer_domains(qtokens)
⋮----
relation_names = set()  # Advisory links may reference indexed sources; installation remains independently gated.
filtered = {"platform":0, "language":0, "selfHosted":0, "inactive":0, "indexed":0, "resource":0, "complexity":0, "capability":0, "excluded":0, "minScore":0}
⋮----
gh = r.get("github", {})
⋮----
s = score_repo(r, qtokens, domains, required_caps, excluded_caps)
⋮----
# Eligibility for related tools/stacks must obey the same hard constraints.
⋮----
top = []
⋮----
relations = resolve_relations(r, repos, stacks, repo_by_name, relation_names)
⋮----
result = {
⋮----
all_gates = (item["rankingReviewGates"] + item["metadataReviewGates"]
⋮----
st = result["recommendedStack"]
```

## File: refresh_github_metadata.py
```python
#!/usr/bin/env python3
"""Refresh non-opinionated GitHub metadata for catalog repositories.

Uses only the Python standard library. GITHUB_TOKEN is optional but strongly
recommended in CI to avoid anonymous API rate limits.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
API = "https://api.github.com/repos/{}"
CONTENTS_API = "https://api.github.com/repos/{}/contents/{}"
LICENSE_NAMES = ("license", "licence", "copying", "notice")
README_NAMES = ("readme",)
FIELDS = {
⋮----
def _request_json(url, token=None, retries=2)
⋮----
headers = {"Accept":"application/vnd.github+json","User-Agent":"star-list-metadata-refresh","X-GitHub-Api-Version":"2022-11-28"}
⋮----
req = Request(url, headers=headers)
⋮----
# The shared GitHub-only opener refuses authenticated cross-origin
# redirects. urllib.urlopen would forward the refresh bearer token.
⋮----
def fetch(repo, token=None, retries=2)
⋮----
def fetch_contents(repo, path="", ref=None, token=None, retries=2)
⋮----
encoded = quote(path, safe="/")
url = CONTENTS_API.format(repo, encoded)
⋮----
def detect_license_text(text)
⋮----
normalized = re.sub(r"\s+", " ", (text or "")).strip().lower()
signatures = [
⋮----
def root_license_scope_warning(text)
⋮----
"""Catch explicit partial, commercial or directory-specific licence grants."""
⋮----
lower = re.sub(r"\s+", " ", text).lower()
⋮----
def strict_root_license(text)
⋮----
"""No README guesses, SPDX strings alone or isolated 'MIT' mentions."""
⋮----
# Text signatures are accepted only for the authoritative root licence
# file, never for incidental descriptions or nested examples.
⋮----
def _decode_content(payload)
⋮----
encoded = payload.get("content")
⋮----
def fallback_license(repo, default_branch, token=None)
⋮----
root = fetch_contents(repo, ref=default_branch, token=token)
⋮----
candidates = []
⋮----
name = str(item.get("name", "")).lower()
stem = re.split(r"[._-]", name, maxsplit=1)[0]
⋮----
detected_licenses = set()
⋮----
path = item.get("path")
⋮----
payload = fetch_contents(repo, path=path, ref=default_branch, token=token)
⋮----
# Incomplete root-file inspection is not enough to safely infer
# a repository-wide license.
⋮----
text = _decode_content(payload)
⋮----
detected = strict_root_license(text)
⋮----
# Conflicting licence files are treated as unresolved, not first-match wins.
# README prose is never a grant covering all directories.
⋮----
def metadata(raw)
⋮----
out = {}
⋮----
lic = raw.get("license")
⋮----
def refresh_primary_language(repo, raw)
⋮----
current=repo.get("languages")
⋮----
language=raw.get("language")
⋮----
def is_missing_repository_error(error)
⋮----
def main()
⋮----
ap = argparse.ArgumentParser()
⋮----
args = ap.parse_args()
⋮----
data = json.loads(CATALOG.read_text())
repos = data.get("repositories", [])
if args.limit > 0: repos = repos[:args.limit]
token = os.environ.get("GITHUB_TOKEN")
⋮----
known_ids = {
⋮----
name = r["repo"]
⋮----
raw = fetch(name, token)
⋮----
stable_id = raw.get("id")
⋮----
previous_id = r.get("githubRepositoryId")
⋮----
existing_name = known_ids.get(stable_id)
⋮----
fresh = metadata(raw)
⋮----
detected = fallback_license(name, raw.get("default_branch"), token)
⋮----
current_github = r.get("github")
current_license = current_github.get("license") if isinstance(current_github, dict) else None
⋮----
entry_changed = r.get("github") != fresh
⋮----
# No additional API calls: this is the same verified repository
# metadata response already used for the weekly refresh.
⋮----
entry_changed = True
⋮----
failure = {"repo":name,"error":str(e)}
```

## File: render_discovery_issue.py
```python
#!/usr/bin/env python3
"""Render actionable discovery candidates as a stable GitHub issue."""
⋮----
SCORE_COMPONENTS=("fit","activity","adoption","maturity","maintenance")
⋮----
def score_profile(row)
⋮----
breakdown=row.get("scoreBreakdown") or {}
⋮----
def render(data,limit=20)
⋮----
rows=[x for x in data.get("repositories",[]) if x.get("decision") in {"accept","review"}][:limit]
counts=data.get("counts",{})
lines=["## Discovery candidates","",f"Evaluated **{data.get('candidates',0)}** candidates: **{counts.get('accept',0)} accept**, **{counts.get('review',0)} review**, **{counts.get('reject',0)} reject**.",""]
⋮----
targets=", ".join(f"{m.get('kind')}:{m.get('target')}" for m in x.get("matchedTargets",[]))
url=x.get("url") or ""
repo=f"[{x['repo']}]({url})" if url else x["repo"]
⋮----
reasons=', '.join(x.get('reasons',[])) or 'no additional signals'
profile=score_profile(x)
if profile: reasons=f"{reasons}; score profile: {profile}"
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("evaluated",type=Path); ap.add_argument("--output",type=Path); ap.add_argument("--limit",type=int,default=20)
args=ap.parse_args(); body=render(json.loads(args.evaluated.read_text()),args.limit)
```

## File: render_health_issue.py
```python
#!/usr/bin/env python3
"""Render replacement and health-drift reports as one stable GitHub issue body."""
⋮----
def render(report, drift=None)
⋮----
rows = report.get("repositories", [])
drift = drift or {"repositories": [], "findings": 0}
drifts = drift.get("repositories", [])
lines = [
⋮----
h=row.get("health",{}); repl=row.get("suggestedReplacements",[]); best=repl[0] if repl else None
⋮----
h=row.get("health",{}); reasons=", ".join(h.get("reasons",[])) or "health threshold"
⋮----
repl=row.get("suggestedReplacements",[])
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
drift=json.loads(args.drift.read_text()) if args.drift else None
body=render(json.loads(args.report.read_text()),drift)
```

## File: report_domain_coverage.py
```python
#!/usr/bin/env python3
"""Inspect evidence-backed advisory domain coverage without mutating catalog."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def analyze(catalog)
⋮----
repositories = catalog["repositories"]
rows = [r for r in repositories if r.get("domain") == "other"]
⋮----
domains = Counter()
⋮----
evidence = advisory_domain_evidence(row)
⋮----
record = reviewed_readme_source(row)
output = {
⋮----
def main()
⋮----
parser = argparse.ArgumentParser()
⋮----
args = parser.parse_args()
result = analyze(json.loads(args.catalog.read_text(encoding="utf-8")))
encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
```

## File: star_import_pipeline.py
```python
#!/usr/bin/env python3
"""Deterministic ingestion for screenshot-derived GitHub star manifests."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def normalize_repo_identity(value: str) -> tuple[str, str]
⋮----
raw = value.strip()
⋮----
parsed = urlsplit(raw)
⋮----
parts = [p for p in parsed.path.split("/") if p]
⋮----
parts = raw.split("/")
⋮----
name = name[:-4] if name.lower().endswith(".git") else name
⋮----
display = f"{owner}/{name}"
⋮----
def load_imports(paths: list[Path]) -> tuple[list[dict], list[dict]]
⋮----
payload = json.loads(path.read_text(encoding="utf-8"))
⋮----
values = payload.get("repositories") if isinstance(payload, dict) else None
⋮----
def partition_candidates(records: list[dict], catalog: dict) -> dict
⋮----
catalog_keys = {}
⋮----
key = record["key"]
⋮----
item = {"key": key, "repo": record["repo"], "sources": sources[key]}
⋮----
duplicates = [{"key": key, "repo": first[key]["repo"], "sources": sources[key]} for key in duplicate_keys]
⋮----
def load_reviewed_metadata(paths: list[Path]) -> tuple[dict[str, dict], list[dict]]
⋮----
"""Load offline metadata snapshots. Only explicitly reviewed entries are eligible."""
⋮----
rows = payload.get("repositories") if isinstance(payload, dict) else None
⋮----
def classify_candidate(candidate: dict, metadata: dict | None = None) -> dict
⋮----
result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])), "status": "needs_review"}
⋮----
entry = copy.deepcopy(metadata["catalogEntry"])
raw_github = metadata.get("github")
⋮----
verified_identity = (normalize_repo_identity(metadata.get("repo"))[0] == candidate["key"]
⋮----
verified_identity = False
required_fields = ("score", "tier", "category", "domain", "resourceLevel", "integrationComplexity")
⋮----
result = {"repo": candidate["repo"], "sources": list(candidate.get("sources", [])),
⋮----
metadata = metadata or {}
metadata_errors = metadata_errors or []
classified = [classify_candidate(c, metadata.get(c["key"])) for c in partition["new"]]
needs_review = [x for x in classified if x["status"] == "needs_review"]
accepted = [x for x in classified if x["status"] == "accepted"]
unique = len(partition["new"]) + len(partition["already_cataloged"])
⋮----
def render_markdown(report: dict) -> str
⋮----
s = report["summary"]
lines = ["# GitHub Star Import Report", "", f"- Raw records: {s['rawRecords']}", f"- Unique normalized repositories: {s['uniqueNormalized']}", f"- Duplicate imports: {s['duplicateImports']}", f"- Already cataloged: {s['alreadyCataloged']}", f"- New candidates: {s['newCandidates']}", f"- Accepted: {s['accepted']}", f"- Needs review: {s['needsReview']}", f"- Malformed: {s['malformed']}", f"- Metadata errors: {s['malformedMetadata']}", "", "## New candidates", ""]
⋮----
def integrate_catalog(catalog: dict, accepted: list[dict]) -> dict
⋮----
result = copy.deepcopy(catalog)
entries = result.setdefault("repositories", [])
seen = {str(x.get("repo", "")).lower() for x in entries}
additions = []
⋮----
key = str(entry.get("repo", "")).lower()
⋮----
def validate_candidate_catalog(candidate: dict, root: Path) -> tuple[bool, str]
⋮----
root = Path(root).resolve()
⋮----
sandbox = Path(td) / "repo"
⋮----
output = []
⋮----
proc = subprocess.run(command, cwd=sandbox, text=True, capture_output=True)
⋮----
def write_catalog_if_valid(candidate: dict, catalog_path: Path, validator=None) -> tuple[bool, str]
⋮----
catalog_path = Path(catalog_path)
validator = validator or (lambda data: validate_candidate_catalog(data, catalog_path.parent))
⋮----
def main(argv=None) -> int
⋮----
parser = argparse.ArgumentParser(description=__doc__)
⋮----
args = parser.parse_args(argv)
paths = args.imports or sorted((ROOT / "imports").glob("github-stars-*.json"))
catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
⋮----
partition = partition_candidates(records, catalog)
⋮----
report = build_report(partition, malformed, [str(p) for p in paths],
payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
⋮----
accepted = [x["catalogEntry"] for x in report["newCandidates"] if x["status"] == "accepted"]
⋮----
candidate = integrate_catalog(catalog, accepted)
```

## File: sync_github_stars.py
```python
#!/usr/bin/env python3
"""Read public GitHub Stars and prepare a review report; never edit catalog.json."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
USER_PATTERN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
REPO_PATTERN = re.compile(r"([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/([A-Za-z0-9_.-]{1,100})\Z")
ISSUE_MARKER = "<!-- star-list-star-sync -->"
⋮----
class SameOriginGitHubRedirect(HTTPRedirectHandler)
⋮----
"""Do not forward the Stars workflow's bearer token outside GitHub API.

    urllib's default redirect handler copies request headers, including
    Authorization. The public Stars sync and metadata admission both use
    authenticated GitHub API calls; fail closed on redirect origin changes.
    """
⋮----
def redirect_request(self, req, fp, code, msg, headers, newurl)
⋮----
original = urlsplit(req.full_url)
destination = urlsplit(newurl)
⋮----
SAFE_GITHUB_HTTP = build_opener(SameOriginGitHubRedirect())
⋮----
def validate_user(user)
⋮----
def normalize_repo(repo)
⋮----
def api_stars(user, token=None, max_pages=100, opener=SAFE_GITHUB_HTTP.open, sleeper=time.sleep)
⋮----
"""Fetch all public stars. A failed/truncated page aborts the entire synchronization."""
⋮----
headers = {
⋮----
found = {}
names_by_stable_id = {}
duplicate_items = 0
pages = 0
⋮----
url = "https://api.github.com/users/" + user + "/starred?" + urlencode(
request = Request(url, headers=headers)
⋮----
raw = response.read()
link = response.headers.get("Link", "")
⋮----
retryable = exc.code in (429, 500, 502, 503, 504)
⋮----
delay = min(8.0, max(0.0, float(exc.headers.get("Retry-After", 2 ** attempt))))
⋮----
delay = float(2 ** attempt)
⋮----
hint = " (check token permissions or API rate limits)" if exc.code in (401, 403, 429) else ""
⋮----
payload = json.loads(raw)
⋮----
repo = entry.get("full_name")
⋮----
key = normalize_repo(repo)
⋮----
repo_id = entry.get("id")
⋮----
original_id = found[key]["githubRepositoryId"]
⋮----
license_obj = entry.get("license")
license_name = license_obj.get("spdx_id") if isinstance(license_obj, dict) else None
⋮----
# We generate the next URL locally; never follow an untrusted Link URL.
has_next = bool(re.search(r'rel\s*=\s*["\x27]?next(?:["\x27]|[,;\s]|$)', link, re.IGNORECASE))
⋮----
def catalog_identities(path, include_ids=False, include_name_ids=False)
⋮----
data = json.loads(Path(path).read_text(encoding="utf-8"))
⋮----
rows = data.get("repositories") if isinstance(data, dict) else None
⋮----
identity = normalize_repo(row.get("repo"))
⋮----
repo_id = row.get("githubRepositoryId")
⋮----
catalog_ids = catalog_ids or set()
catalog_name_ids = catalog_name_ids or {}
# Owner/name values can be reused after deletion or transfer. If the
# catalog has a trusted numeric ID for that exact name, a different live
# ID must never be counted as already admitted.
⋮----
key = normalize_repo(entry["repo"])
recorded_id = catalog_name_ids.get(key)
observed_id = entry.get("githubRepositoryId")
⋮----
# A verified permanent ID remains the same across owner/name transfers.
new = [
⋮----
def render_issue(report, limit=50)
⋮----
user = report["username"]
counts = report["summary"]
entries = report["newRepositories"]
lines = [
⋮----
status = "archived" if row["archived"] else ("disabled" if row["disabled"] else "review")
stars = str(row["stars"]) if row["stars"] is not None else "?"
language = (row["language"] or "unknown").replace("|", "/").replace("\n", " ")
license_name = (row["license"] or "unresolved").replace("|", "/").replace("\n", " ")
⋮----
def write_json(path, payload)
⋮----
output = Path(path)
⋮----
def main(argv=None)
⋮----
parser = argparse.ArgumentParser(description="Check GitHub Stars against star-list (read-only).")
⋮----
args = parser.parse_args(argv)
⋮----
report = build_report(
⋮----
# This is the *same* verified Stars API response, not another
# GitHub request. Admission uses stable IDs to enrich legacy
# catalog entries and reject mismatched snapshots.
```

## File: test_analyze_coverage.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"analyze_coverage.py"
spec=importlib.util.spec_from_file_location("coverage",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
repos=[
r=mod.analyze(repos,min_domain=2,min_capability=2)
```

## File: test_auto_stars_admission.py
```python
#!/usr/bin/env python3
"""Regression checks for the first automated Stars review and canonical transfers."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
def read(path)
⋮----
spec = importlib.util.spec_from_file_location("star_import_pipeline", ROOT / "scripts/star_import_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
⋮----
catalog = read("catalog.json")
manifest = read("imports/github-stars-2026-10-09-auto-1.json")
review = read("reports/github-stars-review-2026-10-09-reviewed.json")
report = read("reports/github-stars-review-2026-10-09-summary.json")
snapshots = (read("reports/github-stars-review-2026-10-09-metadata-1.json")["repositories"]
⋮----
cat = {entry["repo"].lower(): entry for entry in catalog["repositories"]}
⋮----
snapshot_map = {entry["repo"].lower(): entry for entry in snapshots}
⋮----
stable_ids = [entry["githubRepositoryId"] for entry in catalog["repositories"]
⋮----
entry = cat[source["repo"].lower()]
⋮----
transfers = {
⋮----
historic = read("history.json")["repositories"]
health_names = {entry["repo"] for entry in read("health-snapshot.json")["repositories"]}
stack_names = {name for stack in read("stacks.json")["stacks"] for name in stack["repos"]}
⋮----
source = snapshot_map[record["repo"].lower()]
entry = cat[record["repo"].lower()]
⋮----
candidate = {"repo": record["repo"], "key": record["repo"].lower(), "sources": ["automatic"]}
⋮----
partition = pipeline.partition_candidates(import_records, catalog)
⋮----
# A second real sync surfaced three later stars. Keep both historic review batches sound.
followup = read("reports/github-stars-followup-2026-10-09-reviewed.json")
later = read("reports/github-stars-followup-2026-10-09-metadata.json")["repositories"]
⋮----
entry = cat[approved["repo"].lower()]
```

## File: test_backfill_licenses.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "backfill_licenses.py"
spec = importlib.util.spec_from_file_location("backfill_licenses", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
repos = [
seen = []
def resolver(repo, branch, token=None)
```

## File: test_cache_health_history.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_cache_health_history.py"
spec = importlib.util.spec_from_file_location("cache_history", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
history={"schemaVersion":1,"points":[
current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.32,"bodyReuseRate":0.55,"networkFetchRate":0.60,"staleFallbackRate":0.05}}
⋮----
baseline_history={"schemaVersion":1,"points":[
baseline_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.48,"bodyReuseRate":0.58,"networkFetchRate":0.52,"staleFallbackRate":0.00}}
⋮----
confidence_points=[]
⋮----
high_history={"schemaVersion":1,"points":[]}
⋮----
healthy_current={"status":"healthy","metrics":{"logicalRequests":20,"apiCallAvoidanceRate":0.70,"bodyReuseRate":0.80,"networkFetchRate":0.30,"staleFallbackRate":0.00}}
⋮----
cooldown_points=[
```

## File: test_cache_health.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_cache_health.py"
spec = importlib.util.spec_from_file_location("cache_health", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
healthy = mod.analyze({
⋮----
watch = mod.analyze({
⋮----
degraded = mod.analyze({
```

## File: test_catalog_domain_evidence.py
```python
#!/usr/bin/env python3
"""Offline regression: improve indexed source discovery without auto-authorization."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
repos = json.loads((ROOT / "catalog.json").read_text())["repositories"]
by_name = {r["repo"]: r for r in repos}
⋮----
# Real GitHub metadata: identify unambiguous sources without rewriting catalog.
other = [r for r in repos if r["tier"] == "indexed" and r.get("domain") == "other"]
routed = [r for r in other if advisory_domain_evidence(r)]
⋮----
def project(domain, query, language="python")
⋮----
decisions = {}
suggestions = recommendations(target, profile, repos, None, decisions)
⋮----
matched = {s["repository"]: s for s in suggestions}
⋮----
picked = matched[required]
⋮----
ranking_query = [
⋮----
ranking = json.loads(subprocess.check_output(ranking_query, text=True, cwd=ROOT))
ranked = next(row for row in ranking["recommendations"] if row["repo"] == required)
⋮----
# No weak/reused topic labels become grounds for autonomous execution.
unsafe = {
⋮----
# All original review blockers still apply when evidence is strong.
flagged = {
⋮----
matches = recommendations(target, profile, [flagged])
```

## File: test_catalog_quality.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_catalog_quality.py"
spec = importlib.util.spec_from_file_location("audit_catalog_quality", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
now = datetime(2026, 9, 21, tzinfo=timezone.utc)
repos = [
⋮----
report = mod.analyze(repos, stale_days=730, now=now)
⋮----
markdown = mod.render_markdown(report)
⋮----
# Large collections must not exceed the GitHub issue-body limit: full
# structured evidence remains available from the workflow artifact.
oversized = {**report, "findings": report["findings"] * 1000}
oversized_markdown = mod.render_markdown(oversized)
```

## File: test_degraded_inputs.py
```python
#!/usr/bin/env python3
"""Regression tests for degraded, malformed, empty, and large pipeline inputs."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
⋮----
def load(name)
⋮----
path=ROOT/"scripts"/f"{name}.py"
spec=importlib.util.spec_from_file_location(name,path)
mod=importlib.util.module_from_spec(spec)
⋮----
evaluation=load("evaluate_candidates")
health=load("health_score")
memory=load("filter_discovery_memory")
history=load("update_history")
cache_history=load("update_cache_health_history")
⋮----
# Malformed candidate metadata must degrade to conservative defaults, not crash.
bad={
result=evaluation.evaluate(bad,NOW)
⋮----
# Sorting and volume must tolerate numeric strings and malformed rows.
rows=[]
⋮----
bulk=evaluation.evaluate_all({"repositories":rows},NOW)
⋮----
# Health scoring must tolerate corrupt scalar metadata conservatively.
h=health.health_score({
⋮----
# Discovery memory must survive malformed historical fingerprints and targets.
row={"repo":"broken/memory","decision":"review","evaluationScore":"bad","stars":"bad","pushedAt":None,"matchedTargets":None}
old={"schemaVersion":1,"candidates":{"broken/memory":{"fingerprint":{"decision":"review","score":"also-bad","stars":None,"pushedAt":None,"targets":[]}}}}
⋮----
# Persistent memory/history files are caches/state: corrupt JSON or wrong shapes reset safely.
⋮----
td=Path(td)
bad_memory=td/"memory.json"; bad_memory.write_text("{not-json")
bad_history=td/"history.json"; bad_history.write_text("[]")
⋮----
# In-memory malformed history shapes must also recover.
updated_history=history.update(
⋮----
# Cache-health report metrics may be absent or malformed without killing persistence.
point=cache_history.point_from_report({"status":"watch","metrics":{"logicalRequests":"bad","networkFetchRate":"bad"}},"2026-09-15")
```

## File: test_discover_candidates.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"discover_candidates.py"
spec=importlib.util.spec_from_file_location("discover",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
item={"stargazers_count":10000,"forks_count":1000,"license":{"spdx_id":"MIT"}}
```

## File: test_discovery_cache_stats.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
stats = mod.empty_cache_stats()
cache = {"schemaVersion": 1, "entries": {}}
⋮----
fresh_url = "https://api.github.test/fresh"
⋮----
etag_url = "https://api.github.test/etag"
⋮----
real_urlopen = mod.urlopen
⋮----
def not_modified(req, *args, **kwargs)
⋮----
stale_url = "https://api.github.test/stale"
⋮----
def offline(*args, **kwargs)
⋮----
class Response
⋮----
def __init__(self): self.headers = {"ETag": '"network"'}
def __enter__(self): return self
def __exit__(self, *args): return False
def read(self): return b'{"ok":"network"}'
⋮----
network_url = "https://api.github.test/network"
⋮----
summary = mod.finalize_cache_stats(stats)
```

## File: test_discovery_cache.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "discover_candidates.py"
spec = importlib.util.spec_from_file_location("discover", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
# The discoverer must use the shared opener that rejects authenticated
# cross-origin redirects, while the API entrypoint refuses hostile initial
# URLs even before a fresh cache result could conceal them.
⋮----
# Nonsecret GitHub metadata requests continue to use the normal cache path.
api_url = "https://api.github.com/search/repositories"
valid_cache = {"schemaVersion": 1, "entries": {}}
⋮----
cache = {"schemaVersion": 1, "entries": {}}
url = "https://api.github.test/repos/a/x"
⋮----
fresh = mod.cache_get(cache, url, ttl_seconds=60, now=1030)
⋮----
expired = mod.cache_get(cache, url, ttl_seconds=60, now=1061)
⋮----
# Expired data may be used only as a bounded fallback when GitHub/network is unavailable.
stale_url = "https://api.github.test/repos/stale/x"
⋮----
real_urlopen = mod.urlopen
⋮----
def offline(*args, **kwargs)
⋮----
too_old_failed = False
⋮----
too_old_failed = True
⋮----
# Expired entries with an ETag should be conditionally revalidated. A 304 refreshes
# the cache timestamp while preserving the cached body and useful response headers.
revalidate_url = "https://api.github.test/repos/etag/x"
⋮----
seen_headers = {}
⋮----
def not_modified(req, *args, **kwargs)
⋮----
path = Path(td) / "cache.json"
⋮----
loaded = mod.load_cache(path)
⋮----
old={"schemaVersion":1,"entries":{"old":{"fetchedAt":0,"data":{}},"fresh":{"fetchedAt":1900,"data":{}}}}
removed=mod.prune_cache(old,max_age_seconds=500,now=2000)
```

## File: test_discovery_memory.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"filter_discovery_memory.py"
spec=importlib.util.spec_from_file_location("m",SCRIPT); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
row={"repo":"a/x","decision":"review","evaluationScore":70,"stars":1000,"pushedAt":"2026-09-01","matchedTargets":[]}
data={"repositories":[row],"counts":{"accept":0,"review":1,"reject":0}}
⋮----
changed={**row,"evaluationScore":76}; third,mem=m.apply({"repositories":[changed]},mem); assert third["candidates"]==1
```

## File: test_discovery_watchlist.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"build_discovery_watchlist.py"
spec=importlib.util.spec_from_file_location("watchlist",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
report={"policy":{"minHealthyPerDomain":3,"minHealthyPerCapability":2},
r=mod.build(report)
```

## File: test_documentation.py
```python
#!/usr/bin/env python3
"""Keep the public v1 documentation aligned with the executable pipeline."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
SCORING=ROOT/"docs"/"DISCOVERY_SCORING.md"
VERSION=ROOT/"VERSION"
CHANGELOG=ROOT/"CHANGELOG.md"
⋮----
readme=README.read_text()
scoring=SCORING.read_text()
version=VERSION.read_text().strip()
changelog=CHANGELOG.read_text()
⋮----
website_guide = (ROOT / "WEB_RESOURCES.md").read_text()
websites = __import__("json").loads((ROOT / "websites.json").read_text())
⋮----
# Local Markdown links from README must point to repository files/directories.
⋮----
local=target.split("#",1)[0]
⋮----
spec=importlib.util.spec_from_file_location("evaluation",ROOT/"scripts"/"evaluate_candidates.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
⋮----
# The hourly Stars job pushes with GITHUB_TOKEN; GitHub deliberately
# suppresses a second workflow's normal push trigger for that commit.
# Keep the qualified reusable audit dependency wired to the actual push.
sync_yaml = (ROOT / ".github/workflows/sync-github-stars.yml").read_text()
audit_yaml = (ROOT / ".github/workflows/catalog-quality-on-change.yml").read_text()
stars_docs = (ROOT / "docs/GITHUB_STARS_SYNC.md").read_text()
⋮----
identity_yaml = (ROOT / ".github/workflows/backfill-github-ids.yml").read_text()
identity_code = (ROOT / "scripts/backfill_github_ids.py").read_text()
⋮----
skills_workflow = (ROOT / ".github/workflows/audit-agent-skill-sources.yml").read_text()
skills_validator = (ROOT / "scripts/audit_agent_skill_sources.py").read_text()
⋮----
maintenance_yaml = (ROOT / ".github/workflows/refresh-metadata.yml").read_text()
⋮----
skills_docs = (ROOT / "AGENT_SKILLS.md").read_text()
skills_catalog = (ROOT / "agent-skills.json").read_text()
skills_scanner = (ROOT / "scripts/agent_skill_discovery.py").read_text()
portfolio_scanner = (ROOT / "scripts/portfolio_daily.py").read_text()
portfolio_yaml = (ROOT / ".github/workflows/daily-portfolio-integration.yml").read_text()
```

## File: test_evaluate_candidates.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"evaluate_candidates.py"
spec=importlib.util.spec_from_file_location("evaluate",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
strong={"repo":"a/ai-agents","description":"AI agents framework","language":"Python","discoveryScore":75,"stars":5000,"forks":500,"license":"MIT","pushedAt":"2026-09-01T00:00:00Z","createdAt":"2020-01-01T00:00:00Z","latestRelease":{"publishedAt":"2026-08-01T00:00:00Z"},"contributors":50,"watchers":200,"openIssues":20,"hasDiscussions":True,"topics":["ai","agents"],"matchedTargets":[{"target":"ai"},{"target":"agents"}]}
weak={"repo":"b/y","description":"unrelated tool","language":"C","discoveryScore":50,"stars":20,"forks":0,"license":None,"pushedAt":"2020-01-01T00:00:00Z","matchedTargets":[{"target":"mobile"}]}
sparse={"repo":"c/ai-tool","description":"AI tool","language":"Python","discoveryScore":60,"stars":100,"matchedTargets":[{"target":"ai"}]}
sparse_high={"repo":"c/high-score-ai","description":"AI framework","language":"Python","discoveryScore":100,"stars":100,"matchedTargets":[{"target":"ai"}]}
a=mod.evaluate(strong,NOW); b=mod.evaluate(weak,NOW); c=mod.evaluate(sparse,NOW); d=mod.evaluate(sparse_high,NOW)
⋮----
components={"fit","activity","adoption","maturity","maintenance"}
⋮----
# Low-confidence metadata can never produce automatic acceptance.
⋮----
# Decision boundaries are part of the public calibration contract.
⋮----
calibration_cases=[
results=[mod.evaluate(repo,NOW) for repo,_ in calibration_cases]
```

## File: test_find_replacements.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "find_replacements.py"
spec = importlib.util.spec_from_file_location("find_replacements", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
bad = {"repo":"x/bad","score":8.0,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
good = {"repo":"x/good","score":9.5,"domain":"backend","capabilities":["api"],"platforms":["linux"],"languages":["python"],"selfHosted":True,
other = {"repo":"x/other","score":9.5,"domain":"graphics","capabilities":["vector"],"platforms":["linux"],"languages":["rust"],"selfHosted":True,
⋮----
rows = mod.analyze([bad, good, other])
```

## File: test_full_catalog_availability.py
```python
#!/usr/bin/env python3
"""Catalog-wide availability contract: no audit tier / no silent admission queue."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["repositories"]
websites = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))["websites"]
names = [entry["repo"].lower() for entry in catalog]
⋮----
counts = Counter(entry["tier"] for entry in catalog)
⋮----
# An indexed source is never blocked *just* because it has not been hand-curated.
clean = {
⋮----
unsafe = {**clean, "github": {**clean["github"], "license": None}}
⋮----
query = [
payload = json.loads(subprocess.check_output(query, cwd=ROOT, text=True))
⋮----
recs = payload["recommendations"]
⋮----
project = {"full_name": "dbrckk/Moneyprinterturbo_perso", "name": "Moneyprinterturbo_perso",
profile = {"domains": ["ai_media", "productivity"],
assessed = {}
site_assessed = {}
matches = recommendations(project, profile, catalog, None, assessed)
references = website_references_for_project(project, profile, None, site_assessed)
```

## File: test_health_drift.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"detect_health_drift.py"
spec=importlib.util.spec_from_file_location("drift",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
old={"repositories":[{"repo":"a/x","score":90,"status":"healthy"},{"repo":"b/y","score":60,"status":"watch"}]}
new={"repositories":[{"repo":"a/x","score":78,"status":"healthy"},{"repo":"b/y","score":52,"status":"weak"},{"repo":"c/z","score":20,"status":"weak"}]}
rows=mod.detect(old,new,10)
```

## File: test_health_score.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "health_score.py"
spec = importlib.util.spec_from_file_location("health_score", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
NOW = datetime(2026, 9, 15, tzinfo=timezone.utc)
⋮----
active = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2026-09-10T00:00:00Z"}}
stale = {"score":9.5,"github":{"stars":10000,"forks":1000,"archived":False,"disabled":False,"license":"MIT","pushedAt":"2023-01-01T00:00:00Z"}}
```

## File: test_history.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"update_history.py"
spec=importlib.util.spec_from_file_location("h",SCRIPT); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
pts=[{"date":"2026-08-18","health":70,"stars":100,"forks":10},{"date":"2026-08-25","health":72,"stars":114,"forks":12},{"date":"2026-09-01","health":75,"stars":128,"forks":14},{"date":"2026-09-08","health":78,"stars":142,"forks":16},{"date":"2026-09-15","health":82,"stars":156,"forks":18}]
m=h.window_metrics(pts,5); assert m["healthDelta"]==12 and m["starsPerWeek"]==14 and m["forksPerWeek"]==2
t=h.trends({"repositories":{"a/x":pts}})["repositories"][0]; assert t["trend"]=="improving" and t["fourWeeks"]["points"]==5 and t["week"]["points"]==2
```

## File: test_other_domain_expansion.py
```python
#!/usr/bin/env python3
"""Regression tests for broad yet conservative advisory classification."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
rows = catalog["repositories"]
lookup = {r["repo"]: r for r in rows}
report = analyze(catalog)
⋮----
# Explicit high-quality labels and descriptions. Never rewrite original domain.
⋮----
row = lookup[name]
⋮----
evidence = advisory_domain_evidence(row)
⋮----
# Ambiguous metadata must never gain a domain merely to increase the metric.
⋮----
# An inferred domain can be suggested to a compatible task but never silently
# authorize a third-party integration. The existing trust boundary must hold.
project = {"full_name": "dbrckk/esp32-project", "name": "esp32-project"}
profile = {
decision_trace = {}
suggestions = recommendations(project, profile, rows, None, decision_trace)
⋮----
by_suggestion = {r["repository"]: r for r in suggestions}
⋮----
row = by_suggestion[name]
⋮----
# Real inactive or unresolved sources continue to carry source-specific guards.
unsafe = dict(lookup["espressif/arduino-esp32"])
```

## File: test_pipeline_integration.py
```python
#!/usr/bin/env python3
"""Offline integration test for the discovery review pipeline."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
⋮----
def load(name)
⋮----
path=SCRIPTS/f"{name}.py"
spec=importlib.util.spec_from_file_location(name,path)
module=importlib.util.module_from_spec(spec)
⋮----
coverage=load("analyze_coverage")
watchlists=load("build_discovery_watchlist")
discovery=load("discover_candidates")
evaluation=load("evaluate_candidates")
memory=load("filter_discovery_memory")
renderer=load("render_discovery_issue")
⋮----
NOW=datetime(2026,9,15,tzinfo=timezone.utc)
catalog=[{
⋮----
report=coverage.analyze(catalog,min_domain=2,min_capability=2)
⋮----
watchlist=watchlists.build(report,max_items=10)
⋮----
high={
review={
⋮----
def fake_fetch(query,token=None,per_page=10,cache=None,ttl_seconds=0,stale_max_seconds=0,return_source=False,stats=None)
⋮----
payload={"items":[high,review]}
⋮----
def fake_enrich(repo,token=None,cache=None,ttl_seconds=0,stale_max_seconds=0,stats=None)
⋮----
discovered=discovery.discover(watchlist,{"known/agent-core"},per_query=5)
⋮----
evaluated=evaluation.evaluate_all(discovered,NOW)
⋮----
by_repo={row["repo"]:row for row in evaluated["repositories"]}
⋮----
state={"schemaVersion":1,"candidates":{}}
⋮----
body=renderer.render(visible)
```

## File: test_readme_domain_evidence.py
```python
#!/usr/bin/env python3
"""Offline evidence-integrity and relevance regressions for immutable README hints."""
⋮----
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
repos = catalog["repositories"]
by_repo = {r["repo"]: r for r in repos}
manifest = json.loads((ROOT / "catalog-readme-evidence.json").read_text(encoding="utf-8"))
sources = manifest["sources"]
⋮----
allowed = {
⋮----
name = entry["repository"]
⋮----
row = by_repo[name]
⋮----
ev = advisory_domain_evidence(row)
⋮----
wrong_id = {**row, "githubRepositoryId": row["githubRepositoryId"] + 1000000}
⋮----
curated = {**row, "domain": "game_dev"}
⋮----
report = analyze(catalog)
⋮----
assert len(report["unrouted"]) >= 1  # Never invent a domain to reach 100% classification.
⋮----
ref = row["readmeEvidence"]
⋮----
# Grounded examples: targeted routes derived from upstream README snapshots.
cases = [
⋮----
tool = by_repo[name]
⋮----
project = {"full_name": "dbrckk/target-test", "name": "target-test"}
profile = {"domains":[domain],"terms":tokens(query),"language":"python",
assessment = {}
picks = recommendations(project, profile, [tool], None, assessment)
⋮----
picked = picks[0]
⋮----
# A source with conflicting identity or unsupported domain must not inherit
# the vetted README instructions / routing.
⋮----
# CLI ranking works with a new task domain without mutating catalog.
args = [sys.executable, str(ROOT / "scripts/recommend.py"),
payload = json.loads(subprocess.check_output(args,cwd=ROOT,text=True))
⋮----
record = next(row for row in payload["recommendations"] if row["repo"] == "withmarbleapp/os-taxonomy")
⋮----
# Real safeguards remain independent of source evidence.
unsafe = {**by_repo["hexgrad/kokoro"],
```

## File: test_readme_evidence_freshness.py
```python
#!/usr/bin/env python3
"""Offline proof: drift checks preserve original source facts and identity."""
⋮----
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/"catalog-readme-evidence.json").read_text())["sources"]
known=records[0]
def repo(name, token=None)
def content(name, path="", token=None)
base=inspect(known,repo,content)
⋮----
def failed(*args,**kwargs)
⋮----
reports=check([known],1,0,repo,content)
```

## File: test_refresh_github_metadata.py
```python
#!/usr/bin/env python3
"""Regression tests for resilient GitHub metadata refresh behavior."""
⋮----
def http_error(repo, code, message)
⋮----
def run_main(args)
⋮----
old_argv = sys.argv
⋮----
def test_missing_repo_is_recorded_but_nonfatal()
⋮----
catalog = Path(tmp) / "catalog.json"
⋮----
def fake_fetch(repo, token=None, retries=2)
⋮----
written = json.loads(catalog.read_text())
⋮----
def test_license_signature_detection()
⋮----
# Bare words and README snippets must not grant repo-wide reuse rights.
⋮----
def test_license_fallback_reads_root_license_file()
⋮----
original = refresh.fetch_contents
⋮----
def fake_contents(repo, path="", ref=None, token=None, retries=2)
⋮----
content = base64.b64encode(
⋮----
def test_license_fallback_reads_readme_when_root_license_is_absent()
⋮----
def test_license_fallback_rejects_conflicting_root_files()
⋮----
content = (
⋮----
def test_metadata_refresh_uses_license_fallback()
⋮----
def test_metadata_refresh_preserves_verified_license_when_github_is_inconclusive()
⋮----
def test_server_error_remains_fatal()
⋮----
# Reusing an existing slug for a new GitHub ID must not silently change
# the catalog's established permanent identity.
⋮----
unchanged = json.loads(catalog.read_text())["repositories"][0]
⋮----
# Metadata and license fallback requests must use the same authenticated
# GitHub-only opener as Stars synchronization, never urlopen's default
# unrestricted redirect handling.
⋮----
class RejectingOpener
⋮----
def open(self, request, timeout=20)
previous_opener = refresh.SAFE_GITHUB_HTTP
```

## File: test_render_discovery_issue.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"render_discovery_issue.py"
spec=importlib.util.spec_from_file_location("renderer",SCRIPT); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
data={"candidates":2,"counts":{"accept":1,"review":1,"reject":0},"repositories":[{"repo":"a/x","url":"https://github.com/a/x","decision":"accept","evaluationScore":90,"evaluationConfidence":"high","scoreBreakdown":{"fit":92.5,"activity":100.0,"adoption":75.0,"maturity":80.0,"maintenance":85.0},"stars":1000,"ageDays":5,"matchedTargets":[{"kind":"domain","target":"mobile"}],"reasons":["active<=90d"]}]}
body=mod.render(data)
```

## File: test_render_health_issue.py
```python
#!/usr/bin/env python3
⋮----
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"render_health_issue.py"
spec=importlib.util.spec_from_file_location("renderer",SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
report={"threshold":55,"repositories":[]}
drift={"findings":1,"repositories":[{"repo":"a/x","previousScore":90,"currentScore":78,"delta":-12,"previousStatus":"healthy","currentStatus":"healthy"}]}
body=mod.render(report,drift)
⋮----
report={"threshold":55,"repositories":[{"repo":"b/y","health":{"score":40,"status":"weak","reasons":[]},"suggestedReplacements":[]}]}
body=mod.render(report,{"repositories":[]})
```

## File: test_selection_guidance.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "infer_selection_guidance.py"
spec = importlib.util.spec_from_file_location("infer_selection_guidance", SCRIPT)
mod = importlib.util.module_from_spec(spec)
⋮----
repos = [
⋮----
changed = mod.enrich(repos)
```

## File: test_star_import_pipeline.py
```python
#!/usr/bin/env python3
⋮----
SCRIPT = Path(__file__).with_name("star_import_pipeline.py")
⋮----
# Normalization
⋮----
root = Path(td)
p1 = root / "one.json"
p2 = root / "two.json"
⋮----
catalog = {"repositories": [{"repo": "OPENAI/CODEX", "score": 9.5}]}
partition = partition_candidates(records, catalog)
⋮----
candidate = partition["new"][0]
classified = classify_candidate(candidate)
⋮----
report = build_report(partition, malformed, [str(p1), str(p2)])
⋮----
# A raw GitHub snapshot cannot approve itself. Approval is explicit and tied to GitHub evidence.
verified_github = {
new_entry = {
reviewed = {"repo": "Anthropic/Claude-Code", "github": verified_github,
⋮----
review_report = build_report(partition, malformed, ["batch"], {candidate["key"]: reviewed}, ["metadata"])
⋮----
# Integration preserves existing records, sorts only additions deterministically, and is idempotent.
base = {"schemaVersion": 1, "repositories": [{"repo": "z/existing", "score": 8.0}]}
accepted = [
once = integrate_catalog(base, accepted)
twice = integrate_catalog(once, accepted)
⋮----
# Failed validation never replaces the authoritative catalog.
⋮----
catalog_path = root / "catalog.json"
original = json.dumps(base, indent=2) + "\n"
⋮----
# CLI is dry-run by default, emits requested reports, and leaves catalog unchanged.
⋮----
import_path = root / "stars.json"
⋮----
report_json = root / "report.json"
report_md = root / "report.md"
⋮----
catalog_payload = {"schemaVersion": 1, "repositories": [{"repo": "openai/codex"}]}
original = json.dumps(catalog_payload) + "\n"
⋮----
proc = subprocess.run([
⋮----
cli_report = json.loads(report_json.read_text())
⋮----
# End-to-end CLI: importing needs human approval, accepts reviewed data, and stays idempotent.
⋮----
scripts = root / "scripts"
⋮----
baseline = {**new_entry, "repo": "Existing/Project"}
proposed = {**new_entry, "repo": "New/Project"}
⋮----
args = [sys.executable, str(SCRIPT), str(import_path), "--catalog", str(catalog_path),
before = catalog_path.read_text()
raw = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
success = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
merged = json.loads(catalog_path.read_text())
⋮----
new_before_repeat = catalog_path.read_text()
repeat = subprocess.run(args + ["--write"], text=True, capture_output=True)
⋮----
bad = subprocess.run(args + ["--write"], text=True, capture_output=True)
```

## File: test_verify_catalog_evidence.py
```python
#!/usr/bin/env python3
"""Deterministic offline tests for evidence-based metadata review."""
⋮----
def source(text)
⋮----
data = text.encode("utf-8")
blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
⋮----
MIT = ("MIT License\nCopyright (c) 2026 Example\n"
LISTING = [
row = {"repo": "example/project", "tier": "indexed", "githubRepositoryId": 123,
⋮----
def fake_repo(name, token=None)
⋮----
def fake_content(name, path="", ref=None, token=None)
⋮----
def main()
⋮----
partial = ('Portions of this software are licensed as follows: '
⋮----
def scoped_content(name, path="", ref=None, token=None)
scoped_row = audit.inspect_entry(row, fake_repo, scoped_content)
⋮----
bad = source(MIT)
⋮----
report = audit.inspect_entry(row, fake_repo, fake_content)
⋮----
changed = dict(row, licenseStatus="partial")
⋮----
changed = dict(row, github={**row["github"], "license": "Apache-2.0"})
⋮----
def conflicting_repo(name, token=None)
⋮----
def reused_repo(name, token=None)
⋮----
# A README claim without a root licence is never promoted.
def readme_only(name, path="", ref=None, token=None)
⋮----
entries = [dict(row), {**row, "repo": "example/second"}]
⋮----
flagged = dict(row, repo="example/audit-only", selfHosted=True,
⋮----
only = [dict(row, github=dict(row["github"]))]
original_self_hosted = only[0]["selfHosted"]
full = audit.audit(only, only, 1, fake_repo, fake_content, apply=True)
⋮----
schema = json.loads((Path(__file__).resolve().parents[1]
report_contract = {**full, "batchIndex": 0, "wroteCatalog": True}
⋮----
unsafe = dict(report_contract, counts={**full["counts"], "scopedLicenses": "not-a-number"})
⋮----
# Caller writes nothing if any individual operation fails, including an
# identity conflict in a later entry in the batch.
⋮----
path = Path(tmp) / "catalog.json"
```

## File: update_cache_health_history.py
```python
#!/usr/bin/env python3
"""Persist bounded cache-health history and derive multi-week drift signals."""
⋮----
SCHEMA_VERSION=1
DEFAULT_MAX_POINTS=26
ADAPTIVE_MIN_SAMPLES=4
ADAPTIVE_MAX_SAMPLES=8
ADAPTIVE_THRESHOLD=0.20
COOLDOWN_POINTS=2
SEVERITY_RANK={"healthy":0,"watch":1,"degraded":2}
⋮----
def empty_history()
⋮----
def load_history(path)
⋮----
data=json.loads(path.read_text())
⋮----
def save_history(path,history)
⋮----
tmp=path.with_name(path.name+".tmp")
⋮----
def _number(value,default=0.0)
⋮----
try: result=float(value)
⋮----
def _metric(metrics,name)
⋮----
value=metrics.get(name,0.0) if isinstance(metrics,dict) else 0.0
⋮----
def point_from_report(report,date)
⋮----
metrics=report.get("metrics",{}) if isinstance(report,dict) else {}
if not isinstance(metrics,dict): metrics={}
⋮----
def _point_metric(point,name)
⋮----
def _baseline_confidence(sample_size)
⋮----
score=round(min(1.0,max(0.0,sample_size/ADAPTIVE_MAX_SAMPLES)),3)
⋮----
def adaptive_baseline(points,min_samples=ADAPTIVE_MIN_SAMPLES,max_samples=ADAPTIVE_MAX_SAMPLES,threshold=ADAPTIVE_THRESHOLD)
⋮----
history=points[:-1][-max_samples:] if points else []
⋮----
result={
⋮----
current=points[-1]
names=("apiCallAvoidanceRate","bodyReuseRate","networkFetchRate")
baselines={name:round(float(median([_point_metric(p,name) for p in history])),4) for name in names}
deltas={name:round(_point_metric(current,name)-baselines[name],4) for name in names}
findings=[]
⋮----
def _adaptive_severity(adaptive)
⋮----
def _severity(value)
⋮----
def combine_severity(status,adaptive_severity,direction)
⋮----
values=[_severity(status),_severity(adaptive_severity)]
⋮----
def hysteresis_state(previous_candidate,current_candidate)
⋮----
previous=_severity(previous_candidate)
current=_severity(current_candidate)
⋮----
def _point_alert(point)
⋮----
def issue_action(points,current_alert,cooldown_points=COOLDOWN_POINTS)
⋮----
current=_severity(current_alert)
⋮----
states=[_point_alert(point) for point in points]
last_close=None
⋮----
last_close=index
⋮----
observations_since_close=len(states)-1-last_close
⋮----
def analyze_trend(points)
⋮----
adaptive=adaptive_baseline(points)
adaptive_severity=_adaptive_severity(adaptive)
recent=points[-3:]
⋮----
avoidance=[_point_metric(p,"apiCallAvoidanceRate") for p in recent]
network=[_point_metric(p,"networkFetchRate") for p in recent]
body=[_point_metric(p,"bodyReuseRate") for p in recent]
ad=round(avoidance[-1]-avoidance[0],4)
nd=round(network[-1]-network[0],4)
bd=round(body[-1]-body[0],4)
⋮----
direction="declining" if findings else "stable"
⋮----
direction="improving"
⋮----
def update(history,current,date=None,max_points=DEFAULT_MAX_POINTS)
⋮----
today=str(date or date_type.today().isoformat())
base=history if isinstance(history,dict) else empty_history()
source_points=base.get("points",[])
if not isinstance(source_points,list): source_points=[]
points=[dict(p) for p in source_points if isinstance(p,dict) and p.get("date")]
points=[p for p in points if p.get("date")!=today]
previous=points[-1] if points else None
point=point_from_report(current,today)
⋮----
points=points[-max_points:]
trend=analyze_trend(points)
candidate=combine_severity(point.get("status"),trend.get("adaptiveSeverity"),trend.get("direction"))
previous_candidate=(previous or {}).get("candidateSeverity") or (previous or {}).get("status")
⋮----
alert="healthy" if candidate=="healthy" else "watch"
⋮----
alert=hysteresis_state(previous_candidate,candidate)
action=issue_action(points[:-1],alert)
⋮----
updated={"schemaVersion":SCHEMA_VERSION,"points":points}
⋮----
def render_markdown(trend)
⋮----
lines=[
⋮----
adaptive=trend.get("adaptiveBaseline",{})
⋮----
deltas=adaptive.get("deltas",{})
⋮----
def main()
⋮----
ap=argparse.ArgumentParser()
⋮----
args=ap.parse_args()
⋮----
history=load_history(args.history)
current=json.loads(args.current_report.read_text())
```

## File: update_history.py
```python
#!/usr/bin/env python3
"""Maintain bounded weekly repository history and derive multi-window trend signals."""
⋮----
SCHEMA_VERSION=1
⋮----
def empty_history()
⋮----
def load_history(path)
⋮----
data=json.loads(path.read_text())
⋮----
repositories={}
⋮----
def update(history,catalog,health,max_points=26,now=None)
⋮----
now=(now or datetime.now(timezone.utc)).date().isoformat()
if not isinstance(history,dict): history=empty_history()
store=history.get("repositories")
⋮----
store={}
history={"schemaVersion":SCHEMA_VERSION,"repositories":store}
⋮----
health_rows=health.get("repositories",[]) if isinstance(health,dict) else []
hmap={x.get("repo"):x for x in health_rows if isinstance(x,dict) and isinstance(x.get("repo"),str)} if isinstance(health_rows,list) else {}
catalog_rows=catalog.get("repositories",[]) if isinstance(catalog,dict) else []
⋮----
name=r.get("repo")
⋮----
gh=r.get("github",{}); gh=gh if isinstance(gh,dict) else {}
h=hmap.get(name,{})
point={"date":now,"health":h.get("score"),"status":h.get("status"),"stars":gh.get("stars"),"forks":gh.get("forks")}
points=store.get(name,[])
points=[p for p in points if isinstance(p,dict)] if isinstance(points,list) else []
⋮----
def window_metrics(points,size)
⋮----
pts=points[-size:] if size else points
⋮----
days=max(1,(datetime.fromisoformat(last["date"])-datetime.fromisoformat(first["date"])).days)
except (ValueError,TypeError,KeyError): days=max(1,7*(len(pts)-1))
def delta(k)
⋮----
def trends(history)
⋮----
rows=[]
repositories=history.get("repositories",{}) if isinstance(history,dict) else {}
⋮----
pts=[p for p in pts if isinstance(p,dict)]
⋮----
w1=window_metrics(pts,2); w4=window_metrics(pts,5); full=window_metrics(pts,None)
recent=w4 or w1 or full
hd=recent.get("healthDelta")
direction="stable"
if hd is not None and hd<=-10: direction="declining"
elif hd is not None and hd>=10: direction="improving"
elif (recent.get("starsPerWeek") or 0)>0: direction="growing"
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(); ap.add_argument("history",type=Path); ap.add_argument("catalog",type=Path); ap.add_argument("health",type=Path)
⋮----
args=ap.parse_args()
⋮----
history=load_history(args.history)
history=update(history,json.loads(args.catalog.read_text()),json.loads(args.health.read_text()),args.max_points)
```

## File: validate_catalog.py
```python
#!/usr/bin/env python3
⋮----
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "catalog.json").read_text())
⋮----
valid_domains = {"ai_agents","ai_memory","ai_media","software_engineering","web_frontend","backend","mobile","graphics","game_dev","trading","cybersecurity","data_ml","devops","productivity","other"}
valid_roles = {"data","alpha","regime","backtest","risk","execution","portfolio","xauusd","macro","ml","microstructure","performance","volatility","optimization","forecasting","feature-engineering","derivatives","diagnostic","feature-selection","filtering"}
valid_tiers = {"core","recommended","specialized","indexed"}
valid_levels = {"low","medium","high"}
valid_lifecycles = {"active","stable","reference","legacy"}
valid_guidance_sources = {"curated","inferred"}
valid_license_evidence = {"verified-file","no-root-license-file"}
valid_license_statuses = {"not-found","custom-restrictive","partial","external-terms"}
seen = set()
repos = data.get("repositories", [])
⋮----
name = r.get("repo", "")
prefix = name or f"entry[{i}]"
⋮----
score = r.get("score")
⋮----
score = -1
⋮----
tier = r.get("tier")
⋮----
domain = r.get("domain")
⋮----
lifecycle = r.get("lifecycle")
⋮----
guidance_source = r.get("guidanceSource")
⋮----
license_evidence = r.get("licenseEvidence")
⋮----
license_status = r.get("licenseStatus")
⋮----
gh_license = (r.get("github") or {}).get("license") if isinstance(r.get("github"), dict) else None
⋮----
value = r.get(field, [])
⋮----
self_hosted = r.get("selfHosted")
⋮----
gh = r.get("github")
⋮----
value = gh.get(field)
⋮----
roles = set(r.get("roles", []))
bad = roles - valid_roles
⋮----
# Relationship integrity: known catalog repos only, no self-links.
⋮----
counts = Counter(r.get("domain") for r in repos)
```

## File: validate_json_contract.py
```python
#!/usr/bin/env python3
"""Validate JSON documents against the contract-focused JSON Schema subset used by star-list."""
⋮----
def _matches_type(value, expected)
⋮----
def _path(parent, key)
⋮----
SUPPORTED_KEYWORDS={
⋮----
def validate(value, schema, path="$")
⋮----
errors=[]
⋮----
unsupported=sorted(set(schema)-SUPPORTED_KEYWORDS)
⋮----
branches=schema.get("anyOf")
⋮----
expected=schema.get("type")
⋮----
allowed=expected if isinstance(expected, list) else [expected]
⋮----
required=schema.get("required",[])
⋮----
properties=schema.get("properties",{})
⋮----
additional=schema.get("additionalProperties",True)
known=set(properties) if isinstance(properties,dict) else set()
⋮----
seen=set()
⋮----
marker=json.dumps(item,sort_keys=True,ensure_ascii=False)
⋮----
items=schema.get("items")
⋮----
pattern=schema.get("pattern")
⋮----
def main()
⋮----
ap=argparse.ArgumentParser(description="Validate a JSON document against a star-list JSON contract.")
⋮----
args=ap.parse_args()
⋮----
schema=json.loads(args.schema.read_text())
document=json.loads(args.document.read_text())
⋮----
errors=validate(document,schema)
```

## File: validate_websites.py
```python
#!/usr/bin/env python3
"""Audit website catalog URL identity and source usage without network access.

The schema checks structure. This adds security and deduplication rules that
JSON Schema cannot express; neither stage authorizes copying third-party code.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
⋮----
def canonical_url(value)
⋮----
parsed = urlsplit(value)
⋮----
def check_websites(data, schema)
⋮----
errors = list(validate(data, schema))
⋮----
ids = set()
owner_by_url = {}
⋮----
identity = site["id"]
⋮----
# 'originalUrl' records an old URL or user-supplied alternate link.
# Each such alias must remain attached
# to the same entry, not silently create an extra website identity.
⋮----
normalized = canonical_url(url)
⋮----
prior = owner_by_url.get(normalized)
⋮----
# Always-review declarations must not escape a website\'s stated domain.
baseline = set(site.get("portfolioBaselineDomains", []))
⋮----
# Specialist triggers must be explicit canonical labels, not prose.
required_signals = site.get("portfolioRequiredSignals", [])
⋮----
# Converted HF weights inherit upstream usage restrictions. The
# 'other' hub tag is unknown permission, never an approval to install
# or use images commercially; checkpoint provenance is mandatory.
⋮----
# Rewriting checkpoints must disclose verified supported languages
# and cannot be implicitly recommended to every chatbot.
⋮----
# Safety-modified multimodal checkpoints must carry an explicit
# reduced-refusal flag, not hide behind an open source licence.
⋮----
lowered_tags = {str(t).lower() for t in site["tags"]}
⋮----
# Social network automation is hosted, credential-sensitive and
# platform-policy sensitive. Never admit a blanket auto-publish tool.
⋮----
# An MCP endpoint is an authenticated remote service, not a harmless
# website link. Require a bounded HTTPS /mcp URL owned by the
# documented provider; no credentials, foreign hosts or auto-install.
endpoint = site.get("mcpEndpoint")
is_mcp = site["type"] == "mcp-service"
⋮----
service = urlsplit(endpoint)
website = urlsplit(site["url"])
host = service.hostname.lower()
root = website.hostname.lower().removeprefix("www.")
⋮----
def main()
⋮----
data = json.loads((ROOT / "websites.json").read_text(encoding="utf-8"))
schema = json.loads((ROOT / "schemas/websites.schema.json").read_text(encoding="utf-8"))
errors = check_websites(data, schema)
```

## File: verify_catalog_evidence.py
```python
#!/usr/bin/env python3
"""Evidence-based, read-only by default triage for uncertain catalog metadata.

GitHub is the only remote source. A verified root licence can be applied with
--apply, but deployment configuration files are never proof that a project
is fully self-hostable.
"""
⋮----
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
UNKNOWN_LICENSE = (None, "", "NOASSERTION")
MAX_FILE_BYTES = 128 * 1024
LICENSE_STEMS = frozenset({"license", "licence", "copying"})
COMPOSE_FILES = frozenset({
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
⋮----
def root_files(payload)
⋮----
files = {}
⋮----
name = item.get("name")
path = item.get("path")
⋮----
def is_license_file(name)
⋮----
stem = re.split(r"[._-]", name.lower(), maxsplit=1)[0]
⋮----
def content_with_sha(payload)
⋮----
size = payload.get("size")
⋮----
sha = payload.get("sha")
⋮----
encoded = payload.get("content")
⋮----
raw = base64.b64decode(encoded, validate=False)
⋮----
actual_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
⋮----
text = raw.decode("utf-8")
⋮----
def blob_evidence(name, sha)
⋮----
# Immutable blob reference, not a mutable default-branch page.
⋮----
def inspect_entry(entry, fetch_repo=github.fetch, fetch_content=github.fetch_contents, token=None)
⋮----
name = entry.get("repo")
⋮----
gh = entry.get("github") or {}
⋮----
raw = fetch_repo(name, token=token)
⋮----
expected_id = entry.get("githubRepositoryId")
actual_id = raw.get("id")
⋮----
branch = raw.get("default_branch")
⋮----
files = root_files(fetch_content(name, ref=branch, token=token))
item = {
api_license = raw.get("license")
api_spdx = api_license.get("spdx_id") if isinstance(api_license, dict) else None
⋮----
strong = set()
scoped = False
⋮----
payload = fetch_content(name, path=file["path"], ref=branch, token=token)
⋮----
scoped = True
⋮----
detected = github.strict_root_license(content)
⋮----
verified = next(iter(strong))
⋮----
# A previous restrictive/partial/external-terms review is not
# invalidated by finding one apparently permissive root file.
⋮----
# Never infer selfHosted=True from root Docker files; report candidates
# for human examination instead.
⋮----
file = files.get(filename)
⋮----
def requires_review(row)
⋮----
"""Watch missing facts and inactive projects, without gating discovery."""
gh = row.get("github")
⋮----
def select_entries(repos, limit, batch_index, selected_names)
⋮----
uncertain = [row for row in repos if requires_review(row)]
⋮----
by_name = {row.get("repo"): row for row in repos}
missing = sorted(set(selected_names) - set(by_name))
⋮----
rows = [by_name[name] for name in selected_names]
⋮----
rows = sorted(uncertain, key=lambda x: x["repo"].lower())
chunks = max(1, (len(rows) + limit - 1) // limit)
⋮----
rows = rows[batch_index * limit:(batch_index + 1) * limit]
⋮----
by_name = {x.get("repo"): x for x in repos}
⋮----
result = inspect_entry(entry, fetch_repo, fetch_content, token)
⋮----
license_value = result.get("proposedLicense")
⋮----
current = by_name[result["repository"]]
⋮----
# API failures and identity conflicts are never interpreted as
# 'not licensed' or 'not self-hostable'.
⋮----
def main()
⋮----
parser = argparse.ArgumentParser(description="Verify evidence for uncertain Star List metadata.")
⋮----
args = parser.parse_args()
⋮----
data = json.loads(args.catalog.read_text(encoding="utf-8"))
repos = data["repositories"]
⋮----
result = audit(repos, entries, total_uncertain, token=os.environ.get("GITHUB_TOKEN"),
⋮----
# An interrupted process must never leave a partially written catalog.
⋮----
temporary_path = Path(handle.name)
⋮----
# Fail closed; avoid partial catalog writes if even one source failed.
⋮----
encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
```
