def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            rng = (h - l)
            clv = np.where(rng > 0, 2 * (c - (h + l) / 2) / rng, np.nan)
            width = (rng / c) / vol
            ret60 = c / c.shift(60) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "inprof": (b["regime"] == "unknown").astype(int),
                "clv": clv, "width": width, "z": r / vol.shift(1),
                "ret60": ret60, "vol": vol,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - mu
    mu3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(mu3)

    def agg(g, col="x1"):
        v = g[col].dropna()
        n = len(v)
        return pd.Series({"n": n, "mean%": 100 * v.mean() if n else np.nan,
                          "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    D["clvq"] = pd.cut(D["clv"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["lo", "mlo", "mid", "mhi", "hi"])
    D["wq"] = pd.qcut(D["width"], 3, labels=["narrow", "mid", "wide"])
    out["clv x profile, next day"] = D.groupby(["inprof", "clvq"]).apply(agg).round(3)
    out["clv x width, all bars"] = D.groupby(["wq", "clvq"]).apply(agg).round(3)
    D["zq"] = pd.cut(D["z"], [-99, -2, -1, 1, 2, 99], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    D["tr"] = pd.cut(D["ret60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["move z x trend, next day"] = D.groupby(["tr", "zq"]).apply(agg).round(3)
    g3 = D[D.pos % 3 == 0]
    out["move z x trend, next 3d (grid)"] = g3.groupby(["tr", "zq"]).apply(lambda g: agg(g, "x3")).round(3)
    out["weekday next day"] = D.groupby("wd").apply(agg).round(3)
    out["weekday x inprof"] = D.groupby(["inprof", "wd"]).apply(agg).round(3)
    # volatility level
    D["volq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol tercile x clv"] = D.groupby(["volq", "clvq"]).apply(agg).round(3)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["count", "mean", "std", "sum"]).round(5)
    out["share in profile bars"] = float(D["inprof"].mean())
    return out
