"""Topic 47, measurement 2: does a book picked after more tries of the same effect hold less on unseen dates?
For every idea with an unseen test (orchestration/unseen_test/<run>/<id>.json): its in-sample step 5 statistic, its
statistic on each unseen period, whether it holds; and how many tries preceded it: its generation (one per step 7
step from the brief idea) and the number of ideas of its branch (same brief idea and first child) the run tested
before it (from the run's table, in order). Writes search_luck.csv and prints the comparison.
  python3 topics/47_review/search_luck.py"""
import json, math, pathlib, re
import pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
U = STEPS / "orchestration" / "unseen_test"
P = ("unseen_2016_2017", "unseen_2026")
rows = []
for f in sorted(U.glob("*_run/*.json")):
    run = f.parent.name; d = json.load(open(f)); ins = d.get("in_sample") or {}
    if "statistic" not in ins: continue
    bt = f.stem; idea = re.sub(r"_(1h|4h|1d)$", "", bt)
    gen = idea.count(".")
    branch = ".".join(idea.split(".")[:2])
    before = None
    t = STEPS / "orchestration" / "run_idea" / run / "table.json"
    if t.exists():
        order = [r["idea"] for r in json.load(open(t))]
        if idea in order:
            before = sum(1 for x in order[:order.index(idea)] if ".".join(x.split(".")[:2]) == branch)
    row = {"run": run, "backtest": bt, "generation": gen, "tested_before_in_branch": before, "t_in": ins["statistic"]}
    for p in P:
        v = (d.get("periods") or {}).get(p) or {}
        row[f"t_{p}"] = v.get("statistic"); row[f"holds_{p}"] = v.get("holds")
    rows.append(row)
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("search_luck.csv"), index=False, float_format="%.4g")
print(f"ideas with an unseen test: {len(d)}")
# what a real effect of the in-sample size would give on a shorter period: t scales with the square root of the length
L = {"unseen_2016_2017": 725, "unseen_2026": 318}; IN = 2920
for p in P:
    x = d[d[f"holds_{p}"].notna()].copy()
    x["kept"] = x[f"t_{p}"] / (x.t_in * math.sqrt(L[p] / IN))         # 1.0 = the effect kept its in-sample size
    print(f"\n== {p}: {len(x)} ideas; holds {int((x[f'holds_{p}'] == True).sum())}")
    for name, g in (("generation 0-2", x[x.generation <= 2]), ("generation 3-4", x[(x.generation >= 3) & (x.generation <= 4)]), ("generation 5+", x[x.generation >= 5])):
        if len(g): print(f" {name:15s} n {len(g):3d} | holds {int((g[f'holds_{p}'] == True).sum()):3d} ({100 * (g[f'holds_{p}'] == True).mean():3.0f} %) | median in-sample t {g.t_in.median():.2f} | median share of the effect kept {g.kept.median():.2f}")
    y = x[x.tested_before_in_branch.notna()]
    for name, g in (("0-4 tried before", y[y.tested_before_in_branch <= 4]), ("5+ tried before", y[y.tested_before_in_branch >= 5])):
        if len(g): print(f" {name:15s} n {len(g):3d} | holds {int((g[f'holds_{p}'] == True).sum()):3d} ({100 * (g[f'holds_{p}'] == True).mean():3.0f} %) | median share of the effect kept {g.kept.median():.2f}")
