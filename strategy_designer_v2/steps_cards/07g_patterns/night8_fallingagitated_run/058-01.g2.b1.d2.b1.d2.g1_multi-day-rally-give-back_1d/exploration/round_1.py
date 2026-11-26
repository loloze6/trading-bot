def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3p = c / c.shift(3) - 1
            z3 = r3p / (sd30 * np.sqrt(3))
            r1z = r1 / sd30
            r60 = c / c.shift(60) - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            # wide range / close location
            rng = (b["high"] - b["low"]) / c
            cl = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "z3": z3, "r1z": r1z, "r60": r60, "f3": f3, "f1": f1,
                               "sd30": sd30, "cl": cl, "rng_z": rng / sd30,
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "alloc": b["postRebalance_current_allocation"],
                               "fc": b["forecast"],
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            df["grid"] = (df["pos"] % 3 == 0)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["grid"] & A["f3"].notna()].copy()
    drift = g.groupby("coin")["f3"].mean()
    g["u3"] = g["f3"] - g["coin"].map(drift)
    def summ(x, col="u3"):
        x = x.dropna(subset=[col])
        n = len(x); m = x[col].mean()
        # day-clustered t
        d = x.groupby("day")[col].apply(lambda s: (s - m).sum())
        D = len(d)
        se = np.sqrt((d**2).sum() * D / max(D - 1, 1)) / n if n > 1 else np.nan
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / se if se else np.nan})
    out = {}
    g["z3q"] = pd.qcut(g["z3"], 5, labels=False, duplicates="drop")
    out["z3 quintile, in profile"] = g[g.inprof == 1].groupby("z3q").apply(summ)
    out["z3 quintile, out of profile"] = g[g.inprof == 0].groupby("z3q").apply(summ)
    g["r1q"] = pd.qcut(g["r1z"], 5, labels=False, duplicates="drop")
    out["1d move z quintile in profile"] = g[g.inprof == 1].groupby("r1q").apply(summ)
    out["1d move z quintile out profile"] = g[g.inprof == 0].groupby("r1q").apply(summ)
    g["trend"] = pd.cut(g["r60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    gg = g[g.inprof == 0].dropna(subset=["trend"])
    out["out profile: trend x z3 tercile"] = gg.groupby(["trend", pd.qcut(gg["z3"], 3, labels=False)]).apply(summ)
    # next-day by weekday, all bars (non-overlap by 1 day automatically)
    a1 = A.dropna(subset=["f1"]).copy()
    a1["u1"] = a1["f1"] - a1["coin"].map(a1.groupby("coin")["f1"].mean())
    out["next-day by weekday"] = a1.groupby("wd").apply(lambda x: summ(x, "u1"))
    # close location
    a1["clq"] = pd.qcut(a1["cl"], 5, labels=False, duplicates="drop")
    out["next-day by close location quintile"] = a1.groupby("clq").apply(lambda x: summ(x, "u1"))
    out["next-day by close loc, in profile"] = a1[a1.inprof == 1].groupby("clq").apply(lambda x: summ(x, "u1"))
    # book days
    dd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book by year"] = bk.groupby(pd.to_datetime(bk.index).year)["book_return"].agg(["mean", "std", "count"])
    out["in-profile share, by coin"] = A.groupby("coin")["inprof"].mean()
    return out
