"""Does the loop learn? Classify each graded run's primary_failure_mode into
coarse buckets and print them in run order. If the same bucket keeps recurring
late in the sequence, the system is re-deriving knowledge it already has.

STRICT: only the FIRST SENTENCE of primary_failure_mode counts as "the primary
cause" -- a loose whole-text match inflates the count (measured 2026-08-21:
24 loose vs 16 strict on this project's own verdict set). A cause merely
mentioned later in the text is not what killed the run.
"""
import sys, re, yaml
from pathlib import Path
from collections import Counter

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "strategy-research")
BUCKETS = [
    ("regime",  r"regime|gat(e|ing)|activation|starvation"),
    ("cost",    r"cost.drag|fee|over-?trad|turnover|sizing/frequency"),
    ("nosignal",r"no (statistically |directional )?(significant )?edge|no informational|no predictive|inversion|uninformative signal"),
    ("sample",  r"insufficient sample|sample size|sparsity|min-?n"),
]
rows = []
fallback_n = 0
for d in sorted((ROOT/"runs").iterdir()):
    if not (d.is_dir() and d.name.startswith("run_")): continue
    v = d/"artifacts"/"verdict_interpretation.yaml"
    if not v.exists(): continue
    y = yaml.safe_load(v.read_text(encoding="utf-8", errors="replace")) or {}
    pf = y.get("primary_failure_mode")
    via_fallback = pf is None
    if pf is None:
        rc = y.get("root_cause") or {}
        pf = rc.get("mechanism_failure") if isinstance(rc, dict) else None
    if pf is None: continue
    if via_fallback: fallback_n += 1
    full = " ".join(str(pf).split())
    first = re.split(r"(?<=[.;:])\s", full)[0]  # STRICT: first sentence only
    tags = [name for name, pat in BUCKETS if re.search(pat, first, re.I)] or ["other"]
    rows.append((d.name, tags, first[:60]))

print(f"graded runs with a classifiable failure mode: {len(rows)} "
      f"({len(rows) - fallback_n} carry primary_failure_mode; "
      f"{fallback_n} via root_cause.mechanism_failure fallback)")
print()
print("run       buckets")
for name, tags, txt in rows:
    print(f"{name:10s} {','.join(tags):22s} {txt}")
print()
c = Counter(t for _, tags, _ in rows for t in tags)
print("--- bucket totals (a run may carry more than one) ---")
for k, n in c.most_common(): print(f"  {n:3d}  {k}")
print()
half = len(rows)//2
early = Counter(t for _, tags, _ in rows[:half] for t in tags)
late  = Counter(t for _, tags, _ in rows[half:] for t in tags)
print(f"--- first {half} graded runs vs last {len(rows)-half} ---")
for k in sorted(set(early)|set(late)):
    print(f"  {k:10s} early={early[k]:3d}  late={late[k]:3d}")
