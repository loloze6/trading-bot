"""Per held book: the share of bars in a position where the position is on the other side of the target the forecast
asks (held against the forecast), and the share of the units held that way."""
import sys, pathlib, numpy as np, pandas as pd
from concurrent.futures import ProcessPoolExecutor
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
def one(rec):
    inpos = against = 0; ua = ut = 0.0
    for f in rec.glob("*/w*/bars.csv.gz"):
        b = pd.read_csv(f, usecols=["sizing_target_allocation", "postRebalance_current_allocation"])
        t = b["sizing_target_allocation"].fillna(0).to_numpy(); p = b["postRebalance_current_allocation"].fillna(0).to_numpy()
        m = np.abs(p) > 1e-9; a = m & (np.sign(p) != np.sign(t)) & (np.abs(t) > 1e-9)
        inpos += m.sum(); against += a.sum(); ut += np.abs(p[m]).sum(); ua += np.abs(p[a]).sum()
    return rec.parent.parent.name, rec.name, inpos, against, ua / ut if ut else 0
recs = [r for run in sys.argv[1:] for r in sorted((ST/"04_backtest"/run/"backtests").iterdir()) if r.is_dir() and (r/"run.md").exists()]
with ProcessPoolExecutor(2) as ex:
    for run, pid, n, a, u in ex.map(one, recs):
        if n: print(f"{run[:18]:18s} {pid.split('.')[-1][:48]:48s} against the forecast: {a/n*100:5.1f} % of bars in position, {u*100:5.1f} % of units held")
