"""Topic 47, next steps 2b: search luck measured again, splitting the books built before step 3 kept the idea's
situation (N3, 2026-11-23) from those built under it (night 6 onwards, and N3's own proof run). Reads search_luck.csv
(written by search_luck.py); the same measure: the share of the in-sample effect kept on each unseen period.
  python3 topics/47_review/search_luck.py && python3 topics/47_review/search_luck_n3.py"""
import math, pathlib
import pandas as pd

d = pd.read_csv(pathlib.Path(__file__).with_name("search_luck.csv"))
d["build"] = d.run.map(lambda r: "under N3" if r.startswith("night6_") or r == "step3_situation_run" else "before N3")
L = {"unseen_2016_2017": 725, "unseen_2026": 318}; IN = 2920
for p in L:
    x = d[d[f"holds_{p}"].notna()].copy()
    x["kept"] = x[f"t_{p}"] / (x.t_in * math.sqrt(L[p] / IN))
    print(f"\n== {p}")
    for b in ("before N3", "under N3"):
        for name, g in (("all", x[x.build == b]), ("generation 0-2", x[(x.build == b) & (x.generation <= 2)]),
                        ("generation 3+", x[(x.build == b) & (x.generation >= 3)])):
            if len(g):
                print(f" {b:9s} {name:15s} n {len(g):3d} | holds {100 * (g[f'holds_{p}'] == True).mean():3.0f} % | "
                      f"median in-sample t {g.t_in.median():.2f} | median share kept {g.kept.median():.2f}")
