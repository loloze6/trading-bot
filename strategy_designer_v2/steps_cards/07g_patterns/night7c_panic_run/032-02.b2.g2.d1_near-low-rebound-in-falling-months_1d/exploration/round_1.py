def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = (h - l) / c
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r30": c / c.shift(30) - 1,
                "loc": ((h - c) / (h - l)).where(h > l),
                "rng": rng,
                "rr": rng.rolling(30, min_periods=20).mean() / rng.rolling(90, min_periods=40).mean(),
                "volz": rng / rng.rolling(30, min_periods=15).mean(),
                "low30": (c <= c.rolling(30, min_periods=20).min()).astype(float),
                "reg": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "fc": b["forecast"].values,
            })
            d["pos3"] = (np.arange(len(d)) % 3 == 0)
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["nxt"].mean()
    df["ex"] = df["nxt"] - df["coin"].map(drift)
    drift3 = df[df.pos3].groupby("coin")["nxt3"].mean()
    df["ex3"] = df["nxt3"] - df["coin"].map(drift3)
    df["day"] = df["ts"].dt.floor("D")

    def tclu(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean(); dev = (s - m).groupby(dd).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return m, m / se if se > 0 else np.nan, len(s), dd.nunique()

    def table(sub, key, col="ex"):
        out = []
        for k, g in sub.groupby(key, observed=True):
            m, t, n, nd = tclu(g[col], g["day"])
            out.append({"grp": str(k), "mean%": round(m * 100, 3), "t": round(t, 2), "n": n, "days": nd})
        return pd.DataFrame(out)

    res = {}
    df["locq"] = pd.qcut(df["loc"], 5, labels=False)
    df["r1q"] = pd.qcut(df["r1"], 5, labels=False)
    df["r30q"] = pd.qcut(df["r30"], 5, labels=False)
    df["rngq"] = pd.qcut(df["rng"], 5, labels=False)
    df["rrq"] = pd.qcut(df["rr"], 5, labels=False)
    df["volzq"] = pd.qcut(df["volz"], 5, labels=False)
    df["wd"] = df["ts"].dt.weekday
    df["yr"] = df["ts"].dt.year
    inreg = df["reg"] == "mean_reversion"
    res["loc quintile all bars (0=close at high)"] = table(df, "locq")
    res["loc quintile in regime"] = table(df[inreg], "locq")
    res["loc quintile outside regime"] = table(df[~inreg], "locq")
    res["r1 quintile all"] = table(df, "r1q")
    res["r1 quintile in regime"] = table(df[inreg], "r1q")
    res["r30 quintile all"] = table(df, "r30q")
    res["day range quintile all"] = table(df, "rngq")
    res["range ratio 30/90 quintile all"] = table(df, "rrq")
    res["range vs 30d mean quintile all"] = table(df, "volzq")
    res["new 30d low all"] = table(df, "low30")
    res["new 30d low, 3d, grid"] = table(df[df.pos3], "low30", "ex3")
    res["weekday all"] = table(df, "wd")
    res["regime all"] = table(df, "reg")
    res["year all"] = table(df, "yr")
    res["coin in regime"] = table(df[inreg], "coin")
    # book
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dl.append(x)
    dd = pd.concat(dl)
    bk = dd.groupby(["win", "day"])["book_return"].mean().dropna()
    res["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"]).mul([100, 100, 1])
    return res
