def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42}
    rows = []
    for coin, wins in bars.items():
        wl = list(wins.keys())
        for wi, (w, df) in enumerate(wins.items()):
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            rng = (df["high"] - df["low"]) / c
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=30).mean()
            z = r6 / mabs
            rr = rng.rolling(6).mean() / rng.rolling(180, min_periods=30).mean()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "half": "early" if wi < 12 else "late",
                              "pos": np.arange(len(df)), "z": z, "rr": rr,
                              "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "alloc": df["postRebalance_current_allocation"]})
            for k, h in H.items():
                d["f" + k] = c.shift(-h) / c - 1
            d["f4h"] = c.shift(-1) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for k, h in list(H.items()) + [("4h", 1)]:
        g = A[A["pos"] % h == 0]
        m = g.groupby("coin")["f" + k].mean()
        A["x" + k] = A["f" + k] - A["coin"].map(m)
    def summ(sub, col):
        s = sub[col].dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    bins = [0, 0.7, 1, 1.5, 2, 3, np.inf]
    # range ratio graded, by horizon
    for k, h in H.items():
        g = A[A["pos"] % h == 0].dropna(subset=["rr"]).copy()
        g["rq"] = pd.cut(g["rr"], bins)
        out["x%s by range ratio" % k] = g.groupby("rq", observed=True).apply(lambda s: summ(s, "x" + k))
    g = A[A["pos"] % 18 == 0].dropna(subset=["rr", "x3d", "z"]).copy()
    g["lrr"] = np.log(g["rr"])
    # regression of x3d on log rr, per coin and per half, and controlling for z
    res = {}
    for key, sub in list(g.groupby("coin")) + list(g.groupby("half")):
        sl = stats.linregress(sub["lrr"], sub["x3d"])
        res[key] = pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["x3d on log range ratio, by coin and half"] = pd.DataFrame(res).T
    X = np.column_stack([np.ones(len(g)), g["lrr"], g["z"]])
    beta, *_ = np.linalg.lstsq(X, g["x3d"].values, rcond=None)
    resid = g["x3d"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=3)
    out["x3d ~ log rr + z"] = pd.Series({"b_lrr": beta[1], "t_lrr": beta[1] / np.sqrt(cov[1, 1]),
                                          "b_z": beta[2], "t_z": beta[2] / np.sqrt(cov[2, 2]), "n": len(g)})
    # high range, rises vs falls vs flat
    g["zs"] = pd.cut(g["z"], [-np.inf, -1, 1, np.inf], labels=["fall", "flat", "rise"])
    hi = g[g["rr"] >= 1.5]
    out["x3d rr>=1.5 by direction"] = hi.groupby("zs", observed=True).apply(lambda s: summ(s, "x3d"))
    # Friday: by coin, by half, by hour (4h grid 1)
    g6 = A[A["pos"] % 6 == 0]
    fr = g6[g6["wd"] == 4]
    out["friday x1d by coin"] = fr.groupby("coin").apply(lambda s: summ(s, "x1d"))
    out["friday x1d by half"] = fr.groupby("half").apply(lambda s: summ(s, "x1d"))
    out["friday x1d by year"] = fr.groupby("year").apply(lambda s: summ(s, "x1d"))
    out["x4h by weekday,hour friday"] = A[A["wd"] == 4].groupby("hour").apply(lambda s: summ(s, "x4h"))
    out["x4h by hour all"] = A.groupby("hour").apply(lambda s: summ(s, "x4h"))
    # book exposure when active
    act = A[A["alloc"] > 0]
    out["alloc when active"] = pd.Series({"share_bars_active": (A["alloc"] > 0).mean(),
                                          "mean_alloc_active": act["alloc"].mean()})
    return out
