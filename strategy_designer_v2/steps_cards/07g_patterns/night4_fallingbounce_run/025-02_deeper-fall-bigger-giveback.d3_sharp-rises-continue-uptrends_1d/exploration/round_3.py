def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            n = len(d)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "yr": ts.dt.year.values,
                "z": (r1 / vol).values,
                "r5": (c / c.shift(5) - 1).values,
                "z5": ((c / c.shift(5) - 1) / (vol * np.sqrt(5))).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f2": (c.shift(-2) / c - 1).values,
                "f10": (c.shift(-10) / c - 1).values,
                "trend": (d["regime"] == "trending").astype(int).values,
            }))
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 10):
        g = A[A.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        sd = g.groupby("coin")[f"f{h}"].std()
        A[f"u{h}"] = A[f"f{h}"] - A.coin.map(dr)
        A[f"s{h}"] = A.coin.map(sd)
    res = {}
    def reg(df, y, x):
        df = df.dropna(subset=[y, x])
        if len(df) < 20: return pd.Series({"n": len(df), "slope": np.nan, "t": np.nan})
        r = stats.linregress(df[x], df[y])
        return pd.Series({"n": len(df), "slope": r.slope, "t": r.slope / r.stderr})
    G10 = A[(A.pos % 10 == 0) & (A.trend == 1)]
    res["trend: u10 on z5 all"] = reg(G10, "u10", "z5").round(5)
    res["trend: u10 on z5 by year"] = G10.groupby("yr").apply(lambda g: reg(g, "u10", "z5")).round(5)
    res["trend: u10 on z5 by coin"] = G10.groupby("coin").apply(lambda g: reg(g, "u10", "z5")).round(5)
    G = G10.dropna(subset=["z5", "u10"]).copy()
    G["zq"] = pd.qcut(G.z5, 5, labels=False)
    t = G.groupby("zq").agg(n=("u10", "size"), mean=("u10", "mean"), sd=("u10", "std"), z5=("z5", "mean"))
    t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
    t["strength"] = G.assign(st=G.u10 / G.s10).groupby("zq")["st"].mean()
    res["trend: u10 by z5 quintile"] = t.round(4)
    # non-trend one-day reversal, sizes
    N1 = A[(A.trend == 0)].dropna(subset=["z", "u1"]).copy()
    N1["zb"] = pd.cut(N1.z, [-99, -2, -1, 0, 1, 2, 99])
    t = N1.groupby("zb", observed=True).agg(n=("u1", "size"), mean=("u1", "mean"), sd=("u1", "std"))
    t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
    t["strength"] = N1.assign(st=N1.u1 / N1.s1).groupby("zb", observed=True)["st"].mean()
    res["nontrend: u1 by z bin, size"] = t.round(4)
    N2 = A[(A.trend == 0) & (A.pos % 2 == 0)]
    res["nontrend: u2 on z"] = reg(N2, "u2", "z").round(5)
    res["nontrend: u1 on z by coin"] = N1.groupby("coin").apply(lambda g: reg(g, "u1", "z")).round(5)
    res["nontrend: u1 on z by year"] = N1.groupby("yr").apply(lambda g: reg(g, "u1", "z")).round(5)
    return res
