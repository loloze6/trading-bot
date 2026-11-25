def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "z": r / sd30, "sd30": sd30,
                "f": b["forecast"].astype(float),
                "inprof": (b["regime"] == "unknown"),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "ret5": c / c.shift(5) - 1,
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
            })
            df["ret5z"] = df["ret5"] / (sd30 * np.sqrt(5))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r"].mean()
    D["u1"] = D["n1"] - D["coin"].map(drift)
    D["u3"] = D["n3"] - 3 * D["coin"].map(drift)
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year

    def pooled(sub, col):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 5:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        m = s[col].mean()
        g = s.groupby("day").apply(lambda x: (x[col] - m).sum())
        Dd = len(g)
        se = np.sqrt(Dd / (Dd - 1) * (g ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se, "days": Dd})

    out = {}
    D["zb"] = pd.cut(D["z"], [-99, -2.5, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2.5, 99])
    out["u1 by z bucket, in profile"] = D[D.inprof].groupby("zb", observed=True).apply(lambda s: pooled(s, "u1"))
    out["u1 by z bucket, out of profile"] = D[~D.inprof].groupby("zb", observed=True).apply(lambda s: pooled(s, "u1"))
    # 3-day horizon, non-overlapping grid
    G = D[D["pos"] % 3 == 0]
    out["u3 by z bucket, all profiles, grid3"] = G.groupby("zb", observed=True).apply(lambda s: pooled(s, "u3"))
    # 5-day scaled return buckets, next day
    D["r5b"] = pd.cut(D["ret5z"], [-99, -2, -1, 0, 1, 2, 99])
    out["u1 by 5d scaled ret, all"] = D.groupby("r5b", observed=True).apply(lambda s: pooled(s, "u1"))
    # close position in range for down days
    dd = D[D["r"] < 0].copy()
    dd["cpb"] = pd.cut(dd["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["u1 down days by close position"] = dd.groupby("cpb", observed=True).apply(lambda s: pooled(s, "u1"))
    # vol level
    D["volq"] = D.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["u1 by vol quartile, all"] = D.groupby("volq").apply(lambda s: pooled(s, "u1"))
    out["u1 by weekday, all"] = D.groupby("wd").apply(lambda s: pooled(s, "u1"))
    out["u1 by year, cases f>0"] = D[D.f > 0].groupby("yr").apply(lambda s: pooled(s, "u1"))
    out["u1 by coin, cases f>0"] = D[D.f > 0].groupby("coin").apply(lambda s: pooled(s, "u1"))
    out["share in profile"] = float(D.inprof.mean())
    # book: largest days
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd2 = d.copy(); dd2["coin"] = coin; dd2["win"] = w; days.append(dd2)
    Dy = pd.concat(days)
    bk = Dy.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book: top10 days share of total"] = float(bk.nlargest(10).sum() / bk.sum())
    out["book: bottom10 days sum / total"] = float(bk.nsmallest(10).sum() / bk.sum())
    out["book by window, mean% and sum%"] = bk.groupby(level=0).agg(lambda x: 100 * x.sum())
    return out
