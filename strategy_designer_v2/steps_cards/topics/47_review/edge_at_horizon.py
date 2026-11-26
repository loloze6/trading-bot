"""Topic 47, check of a claim before it becomes a next step: per real book of night 5, the idea's gain beyond the
coin's drift at the horizon its plan holds (min_holding_bars; none: 1 bar), per trade, in % before costs, with its t
from errors clustered by day; against the round trip in these records (about 0.2 % with fees and slippage; the fee
alone is 0.1 %).  python3 topics/47_review/edge_at_horizon.py TRADES.csv.gz"""
import json, sys, pathlib, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
STEPS = pathlib.Path(__file__).resolve().parents[2]; DATA = STEPS.parents[1] / "trading-bot" / "local_data"
d = pd.read_csv(sys.argv[1]); d["entry_time"] = pd.to_datetime(d.entry_time, format="ISO8601"); d["day"] = d.entry_time.dt.normalize()
px = {}
rows = []
for (run, book), x in d.groupby(["run", "book"]):
    bar = book[-2:]
    k = json.load(open(STEPS / "03_test_plan" / run / "plans" / f"{book}_config.json"))["strategies"].get("min_holding_bars") or 1
    edges = []
    for coin, y in x.groupby("symbol"):
        if (coin, bar) not in px:
            p = pd.read_csv(DATA / f"kraken_{coin}_{bar}.csv", usecols=["timestamp", "close"]).drop_duplicates("timestamp")
            p["timestamp"] = pd.to_datetime(p.timestamp, format="ISO8601"); px[(coin, bar)] = p.set_index("timestamp").sort_index().close
        c = px[(coin, bar)].to_numpy(float); ei = px[(coin, bar)].index.get_indexer(y.entry_time)
        ok = (ei >= 0) & (ei + k < len(c)); sgn = np.where(y.direction == "long", 1.0, -1.0)
        drift = np.nanmean(c[k:] / c[:-k] - 1)
        e = np.full(len(y), np.nan); e[ok] = 100 * sgn[ok] * (c[ei[ok] + k] / c[ei[ok]] - 1 - drift)
        edges.append(pd.DataFrame({"edge": e, "day": y.day.to_numpy()}))
    e = pd.concat(edges).dropna()
    m = e.edge.mean(); dev = (e.edge - m).groupby(e.day).sum()
    t = m / (np.sqrt((dev ** 2).sum()) / len(e))
    rows.append({"book": book, "bar": bar, "horizon": k, "trades": len(e), "edge": m, "t_by_day": t,
                 "pays": bool(x.pays.iloc[0])})
r = pd.DataFrame(rows); r.to_csv(pathlib.Path(__file__).with_name("edge_at_horizon.csv"), index=False, float_format="%.4g")
for bar, x in r.groupby("bar"):
    print(f"{bar}: {len(x)} real books | edge beyond drift at the plan's horizon: median {x.edge.median():+.3f} % | below 0: {int((x.edge < 0).sum())} | "
          f"significantly below 0 (t < -2): {int((x.t_by_day < -2).sum())} | above the 0.1 % fee: {int((x.edge > 0.1).sum())} | above a 0.2 % round trip: {int((x.edge > 0.2).sum())} | "
          f"significantly above 0: {int((x.t_by_day > 2).sum())}")
    print("   paying books:", x[x.pays][["edge", "t_by_day"]].round(2).values.tolist())
