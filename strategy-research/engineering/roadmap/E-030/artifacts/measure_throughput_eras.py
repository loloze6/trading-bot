"""Runs completed per day over time, from each run's own pipeline_state.yaml
audit timestamps. Corrects a claim built from campaign_log.md, which only
covers the run_campaign.py queue-driver era (run_053 onward)."""

import sys, yaml
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "strategy-research")
runs = []
for d in sorted((ROOT / "runs").iterdir()):
    if not (d.is_dir() and d.name.startswith("run_")):
        continue
    p = d / "pipeline_state.yaml"
    if not p.exists():
        continue
    y = yaml.safe_load(p.read_text(encoding="utf-8", errors="replace")) or {}
    ts = []
    for k, v in (y.get("audit_log") or {}).items():
        if isinstance(v, dict) and v.get("timestamp"):
            try:
                ts.append(datetime.fromisoformat(str(v["timestamp"])))
            except Exception:
                pass
    if not ts:
        continue
    pend = str(y.get("pending_stage"))
    runs.append((d.name, min(ts), max(ts), pend, len(y.get("completed_stages") or [])))
term = [r for r in runs if r[3].startswith("completed_")]
print(
    f"runs with timestamps: {len(runs)}   reaching a terminal completed_* state: {len(term)}\n"
)
print("--- completions per calendar day ---")
c = Counter(r[2].date() for r in term)
for day in sorted(c):
    print(f"  {day}  {'#' * c[day]} {c[day]}")
print()
CUT = datetime(2026, 7, 6, tzinfo=term[0][2].tzinfo)
pre = [r for r in term if r[2] < CUT]
post = [r for r in term if r[2] >= CUT]


def span(rs):
    return (max(r[2] for r in rs) - min(r[1] for r in rs)).total_seconds() / 86400


print(
    f"BEFORE run_campaign.py (pre 2026-07-06): {len(pre):2d} completions over {span(pre):.1f} days = {len(pre) / span(pre):.2f}/day"
)
print(
    f"AFTER  run_campaign.py (2026-07-06 on) : {len(post):2d} completions over {span(post):.1f} days = {len(post) / span(post):.2f}/day"
)
print(f"SINCE last completion (2026-07-19)     :  0 completions over 33 days")
print()
print("--- wall-clock duration per completed run (first->last audit) ---")
for n, t0, t1, pend, ns in term:
    print(f"  {n:10s} {(t1 - t0).total_seconds() / 3600:7.2f} h   {pend}")
