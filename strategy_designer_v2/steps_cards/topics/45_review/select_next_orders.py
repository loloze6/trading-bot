"""select_next: three orders against the old score on every named run (the first 10 candidates after a brief's ideas); topic 45, operator 2026-11-22. Run from steps_cards/."""
import sys, glob, statistics as st
sys.path.insert(0, "orchestration/select_next/helper"); import select_next as sn
runs = sorted({p.split("/")[1] for p in glob.glob("03_test_plan/*_run/plans")})
w = lambda r: r.get("difference", 0.5) if r["group"] == 2 else 0.5
orders = {"old (score)": lambda r: (-r["score"], r["number"], r["idea"]),
          "A (proven first, then x difference)": lambda r: (r["group"], -r["priority"], r["number"], r["idea"]),
          "B (one priority: score x w)": lambda r: (-r["score"] * w(r), r["number"], r["idea"]),
          "C (proven and different first, then score x w)": lambda r: (0 if (r["group"] == 2 and w(r) > 0.5) else 1, -r["score"] * w(r), r["number"], r["idea"])}
tot = {k: [0, 0, [], 0, 0] for k in orders}
for run in runs:
    rows = [r for r in sn.rank(run) if r["status"] == "candidate" and r["generation"] != 0]
    if len(rows) < 3: continue
    for k, key in orders.items():
        top = sorted(rows, key=key)[:10]; t = tot[k]
        t[0] += len(top); t[1] += sum(r["group"] == 2 for r in top); t[2] += [w(r) for r in top]
        t[3] += sum(r["group"] == 2 and r.get("difference", 0.5) < 0.5 for r in top)
        t[4] += sum(r["group"] == 2 and r.get("difference", 0.5) > 0.5 for r in top)
print(f"{'order':48s} {'top-10 slots':>12s} {'confirmed parent':>17s} {'... different (d>0.5)':>22s} {'... we already earn (d<0.5)':>28s} {'mean w':>7s}")
for k, t in tot.items(): print(f"{k:48s} {t[0]:12d} {t[1]:17d} {t[4]:22d} {t[3]:28d} {st.mean(t[2]):7.2f}")
avail = [r for run in runs for r in sn.rank(run) if r["status"] == "candidate" and r["generation"] != 0]
print(f"\nall candidates after the briefs' ideas: {len(avail)}; from a confirmed parent {sum(r['group']==2 for r in avail)} (different {sum(r['group']==2 and r.get('difference',0.5)>0.5 for r in avail)}, already earned {sum(r['group']==2 and r.get('difference',0.5)<0.5 for r in avail)})")
