"""Topic 51 proof: the same plans on the engine before and after option A (a move to flat never refused by the band),
record by record, window by window. Records in a scratch folder (before/, after/: step 4 with --out-root).
  python3 topics/51_review/compare.py FOLDER"""
import sys, glob, os
from pathlib import Path
import numpy as np, pandas as pd
STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "orchestration/ideas_similarities_check/helper"))
from book_returns import book_returns
S = Path(sys.argv[1])                       # the folder holding before/ and after/
COLS = ["timestamp", "forecast", "approved_rebalance", "postRebalance_current_allocation", "postRebalance_total_value", "allocation_change"]
rows = []
for rec in sorted(p for p in (S / "before").iterdir() if p.is_dir()):
    after = S / "after" / rec.name
    t = dict(book=rec.name.split("_")[0], windows=0, windows_same=0, closes=0, consequences=0, unexplained=0, days_held_before=0, days_held_after=0)
    for f in sorted(rec.glob("*/w*/bars.csv.gz")):
        g = after / f.relative_to(rec)
        if not g.exists():
            t["unexplained"] += 1; continue
        b = pd.read_csv(f, usecols=COLS, dtype={"approved_rebalance": str}); a = pd.read_csv(g, usecols=COLS, dtype={"approved_rebalance": str})
        t["windows"] += 1
        hb = b.postRebalance_current_allocation.fillna(0).shift().fillna(0); ha = a.postRebalance_current_allocation.fillna(0).shift().fillna(0)
        t["days_held_before"] += int((b.postRebalance_current_allocation.fillna(0).abs() > 1e-9).sum())
        t["days_held_after"] += int((a.postRebalance_current_allocation.fillna(0).abs() > 1e-9).sum())
        same = (b[COLS[:5]].astype(str) == a[COLS[:5]].astype(str)).all(axis=1)
        if same.all():
            t["windows_same"] += 1; continue
        first = int((~same).idxmax())
        # a close: the order takes the book to flat (this code: approved, flat after it) where the old engine did not
        # trade it (refused by the band, or left to the end-of-window close), and the order is under the band
        close = lambda i: (b.approved_rebalance[i] != "True" and a.approved_rebalance[i] == "True"
                           and abs(a.postRebalance_current_allocation[i]) < 1e-12 and abs(float(b.allocation_change[i])) < 0.2)
        # the named difference: a window's first differing bar is a remainder under the band, closed; every later
        # difference follows from it (the book's cash, or its position, differs from then on)
        if close(first):
            t["closes"] += 1 + sum(close(i) for i in range(first + 1, len(b)) if not same[i])
            t["consequences"] += sum(1 for i in range(first + 1, len(b)) if not same[i] and not close(i))
        else:
            t["unexplained"] += 1
            if t["unexplained"] <= 2:
                print("FIRST DIFFERENCE NOT A CLOSE", rec.name, f.parent.parent.name, f.parent.name, first,
                      b.loc[max(first-1,0):first].to_dict("records"), a.loc[max(first-1,0):first].to_dict("records"))
    for k, r in (("before", rec), ("after", after)):
        br = book_returns(r, "1d").book
        t[f"sharpe_{k}"] = round(br.mean() / br.std() * np.sqrt(365), 3)
    rows.append(t)
out = pd.DataFrame(rows); pd.set_option("display.width", 250)
print(out.to_string(index=False))
out.to_csv(Path(__file__).with_name("compare.csv"), index=False)
