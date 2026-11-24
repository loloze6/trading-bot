import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = r1 / sd30
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "f3": f3, "f1": f1,
                               "r5": r5, "sd30": sd30, "rising": (b["regime"] == "unknown").values,
                               "fc": b["forecast"].astype(float), "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "range": (b["high"] - b["low"]) / c,
                               "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].dropna(subset=["f3"]).copy()
    drift = g.groupby("coin")["f3"].mean()
    g["ex3"] = g["f3"] - g["coin"].map(drift)
    g["zb"] = pd.cut(g["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex3": x["ex3"].mean(), "t": x["ex3"].mean() / (x["ex3"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["ex3 by z bucket x rising"] = g.groupby(["rising", "zb"], observed=True).apply(summ)
    # slope of ex3 on z by regime
    res = {}
    for rg, x in g.dropna(subset=["z"]).groupby("rising"):
        s = stats.linregress(x["z"], x["ex3"])
        res[str(rg)] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}
    out["slope ex3 on z by rising"] = pd.DataFrame(res).T
    # 5-day return scaled
    g["z5"] = g["r5"] / (g["sd30"] * np.sqrt(5))
    g["z5b"] = pd.qcut(g["z5"], 5)
    out["ex3 by 5d scaled ret quintile x rising"] = g.groupby(["rising", "z5b"], observed=True).apply(summ)
    # vol level
    g["volq"] = g.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ex3 by vol tercile x rising"] = g.groupby(["rising", "volq"]).apply(summ)
    # close location of day
    g["clvb"] = pd.cut(g["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["ex3 by close location"] = g.groupby(["rising", "clvb"], observed=True).apply(summ)
    # weekday next-day return (all bars, 1-day non-overlapping automatically)
    d1 = d.dropna(subset=["f1"])
    out["f1 by weekday"] = d1.groupby("wd")["f1"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # by window
    out["ex3 by window, rising & z<-1 vs rising other"] = g[g["rising"]].assign(dn=g["z"] < -1).groupby(["win", "dn"])["ex3"].agg(["count", "mean"]).unstack()
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, win=w))
    T = pd.concat(tr, ignore_index=True)
    T["efb"] = pd.qcut(T["entry_forecast"].astype(float), 4, duplicates="drop")
    out["trades by entry forecast"] = T.groupby("efb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
