"""Planted-effect test of step 5 (not market evidence). Copies a real backtest record and its plan, and adds a known
drift to the next-bar return in the direction of the forecast: r'(t+1) = r(t+1) + delta * sign(forecast(t)).
Prices are rebuilt from the new returns (open, high, low scaled with the close). Nothing else in the record changes,
so the situation check still sees the same forecast and indicator values. Step 5 is then run on it unchanged.

  python make_planted.py PLAN_ID DELTA_LABEL DELTA   (run with the venv's Python)
"""
import gzip, shutil, sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
plan_id, label, delta = sys.argv[1], sys.argv[2], float(sys.argv[3])
new_id = f"{plan_id}_{label}"
src_rec, dst_rec = STEPS / "04_backtest" / "backtests" / plan_id, HERE / "records" / new_id
src_plan = STEPS / "03_test_plan" / "plans"
(HERE / "plans").mkdir(parents=True, exist_ok=True)
shutil.copy(src_plan / f"{plan_id}.md", HERE / "plans" / f"{new_id}.md")
shutil.copy(src_plan / f"{plan_id}_config.json", HERE / "plans" / f"{new_id}_config.json")
if dst_rec.exists():
    shutil.rmtree(dst_rec)
for f in src_rec.glob("*/w*/bars.csv.gz"):
    d = pd.read_csv(f, low_memory=False)
    r = d["close"].pct_change().fillna(0.0).to_numpy()
    drift = np.zeros(len(d))
    drift[1:] = delta * np.sign(d["forecast"].to_numpy()[:-1])
    factor = np.cumprod(1 + r + drift) / np.cumprod(1 + r)
    for c in ("open", "high", "low", "close"):
        if c in d.columns:
            d[c] = d[c] * factor
    out = dst_rec / f.parent.relative_to(src_rec)
    out.mkdir(parents=True, exist_ok=True)
    with gzip.open(out / "bars.csv.gz", "wt") as g:
        d.to_csv(g, index=False)
print(new_id)
