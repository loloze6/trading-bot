def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z1 = r1 / sd30
            r3p = c / c.shift(3) - 1
            z3 = r3p / (sd30 * np.sqrt(3))
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z1": z1, "z3": z3,
                               "clv": clv, "f3": f3, "f1": f1, "inprof": (b["regime"] == "unknown").astype(int),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "wd": ts.dt.weekday, "sd30": sd30})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d[d.pos % 3 == 0].groupby("coin")["f3"].mean()
    d["x3"] = d["f3"] - d["coin"].map(drift)
    g = d[(d.pos % 3 == 0)].dropna(subset=["x3", "z1"])
    out = {}
    def tab(sub, col, bins):
        sub = sub.copy(); sub["bin"] = pd.cut(sub[col], bins)
        t = sub.groupby(["inprof", "bin"], observed=True)["x3"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    out["z1 bins -> excess 3d"] = tab(g, "z1", [-10, -2, -1, -0.3, 0.3, 1, 2, 10])
    out["z3 bins -> excess 3d"] = tab(g.dropna(subset=["z3"]), "z3", [-10, -1.5, -0.5, 0.5, 1.5, 10])
    gg = g.dropna(subset=["clv"]).copy()
    gg["clvb"] = pd.cut(gg["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    t = gg.groupby(["inprof", "clvb"], observed=True)["x3"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); out["close location -> excess 3d"] = t.round(4)
    # regression slopes in and out of profile, both sides
    res = {}
    for ip in [0, 1]:
        for side, s in [("up", g.z1 > 0), ("down", g.z1 < 0)]:
            sub = g[(g.inprof == ip) & s]
            lr = stats.linregress(sub.z1.abs(), sub.x3)
            res[f"prof{ip}_{side}"] = [len(sub), lr.slope, lr.slope / lr.stderr]
    out["slope x3 on |z1|"] = pd.DataFrame(res, index=["n", "slope", "t"]).T.round(4)
    # weekday, 1-day forward, all bars
    d["x1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    t = d.dropna(subset=["x1"]).groupby(["inprof", "wd"])["x1"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); out["weekday next-day excess"] = t.round(4)
    # book days
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    out["book by window"] = dd.groupby("w")["book_return"].agg(["count", "mean", "sum"]).round(5)
    out["book by coin"] = dd.groupby("coin")["book_return"].agg(["count", "mean", "sum"]).round(5)
    return out
