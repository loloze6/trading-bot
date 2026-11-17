"""Diagnostic (no model call, no new backtest): one book made of the confirmed ideas' books, measured as step 6 does."""
import json, math, sys
from pathlib import Path
import numpy as np, pandas as pd
STEPS = Path(sys.argv[1]); sys.path.insert(0, str(STEPS / "06_profitability" / "helper"))
import check_profitability as cp
books, holds, names = [], None, []
for run in ("demo_run", "night_run"):
    for r in json.load(open(STEPS / "orchestration/run_idea" / run / "table.json")):
        if not str(r.get("step5", "")).startswith("confirmed"):
            continue
        rec = STEPS / "04_backtest" / run / "backtests" / f"{r['idea']}_1d"
        if not list(rec.glob("*/w*/bars.csv.gz")):
            continue
        b, h, _, _, _ = cp.load(rec)
        books.append(pd.concat({w: s for w, s in b.items()}))     # (window, day) -> return
        names.append(run + ":" + r["idea"][-40:])
        if holds is None:
            holds = pd.concat({w: s for w, s in h.items()})
df = pd.concat(books, axis=1).fillna(0.0)                         # a day a book has no return: flat
df.columns = names
rule = __import__("yaml").safe_load(open(STEPS / "06_profitability/helper/rule.yaml"))
def measures(r):
    r = np.asarray(r, float); curve = np.cumprod(1 + r); years = len(r) / 365
    ann = curve[-1] ** (1 / years) - 1 if curve[-1] > 0 else -1
    fall = float(np.max(1 - curve / np.maximum.accumulate(np.concatenate([[1.0], curve]))[1:]))
    return {"Sharpe": cp.sharpe(r), "minus hold": cp.sharpe(r) - cp.sharpe(holds.reindex(df.index).fillna(0).to_numpy()),
            "mean/day %": r.mean() * 100, "Calmar": ann / fall if fall > 0 else math.inf, "vol/day %": r.std() * 100, "ann %": ann * 100}
print(f"{df.shape[1]} confirmed books; mean pairwise correlation {df.corr().values[np.triu_indices(df.shape[1], 1)].mean():.2f}")
ind = pd.DataFrame({c: measures(df[c]) for c in df}).T
print("single books (median):", {k: round(v, 3) for k, v in ind.median().items()})
eq = df.mean(axis=1)
print("one book, equal weight:", {k: round(v, 3) for k, v in measures(eq).items()})
k = ind["vol/day %"].median() / (eq.std() * 100)
print(f"same book sized to a single book's volatility (x{k:.2f}):", {k2: round(v, 3) for k2, v in measures(eq * k).items()})
print("step 6 bars: mean/day >= 0.05 %, Calmar > 0.75, Sharpe and minus-hold > 0")
sized = eq * k
loo = min(cp.sharpe(sized[sized.index.get_level_values(0) != w].to_numpy()) for w in sorted(set(sized.index.get_level_values(0))))
print(f"lowest Sharpe with one window left out: {loo:.3f}; windows: {len(set(sized.index.get_level_values(0)))}; days: {len(sized)}")
