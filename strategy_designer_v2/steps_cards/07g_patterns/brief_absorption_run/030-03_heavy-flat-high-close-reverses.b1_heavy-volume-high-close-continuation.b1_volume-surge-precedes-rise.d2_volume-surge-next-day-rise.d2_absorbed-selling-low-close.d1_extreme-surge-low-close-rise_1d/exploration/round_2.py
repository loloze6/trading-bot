def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = (h - l).replace(0, np.nan)
            r1 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "clvlow": (h - c) / rng,
                "surge": v / v.shift(1).rolling(20, min_periods=10).mean(),
                "r1": r1,
                "vol20": r1.rolling(20, min_periods=10).std(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "yr": ts.dt.year, "wd": ts.dt.weekday,
            })
            rows.append(df)
    X = pd.concat(rows, ignore_index=True)
    for hh in [1, 2, 3]:
        g = X[X["pos"] % hh == 0]
        m = g.groupby("coin")["f%d" % hh].mean()
        X["e%d" % hh] = X["f%d" % hh] - X["coin"].map(m)
    X["z1"] = X["r1"] / X["vol20"]           # day's return in units of its own 20-day vol
    X["q_vol20"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    X["q_z1"] = X.groupby("coin")["z1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    X["q_clv"] = X.groupby("coin")["clvlow"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    X["lsurge"] = np.log(X["surge"])
    res = {}
    d = X[["e1", "r1", "z1", "clvlow", "lsurge", "vol20", "q_vol20", "yr", "coin", "q_z1", "q_clv"]].dropna()
    def ols(df, ycol, xcols):
        Y = df[ycol].values; M = np.column_stack([np.ones(len(df))] + [df[c].values for c in xcols])
        beta, *_ = np.linalg.lstsq(M, Y, rcond=None)
        resid = Y - M @ beta
        # HC1 robust se
        XtXi = np.linalg.inv(M.T @ M)
        S = (M * resid[:, None]).T @ (M * resid[:, None])
        V = XtXi @ S @ XtXi * len(Y) / (len(Y) - M.shape[1])
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + xcols).round(5)
    dd = d.copy()
    for c in ["z1", "clvlow", "lsurge"]:
        dd[c] = dd.groupby("coin")[c].transform(lambda s: (s - s.mean()) / s.std())
    dd["hv"] = (dd["q_vol20"] == 4).astype(float)
    dd["z1_hv"] = dd["z1"] * dd["hv"]; dd["clv_hv"] = dd["clvlow"] * dd["hv"]; dd["surge_clv"] = dd["lsurge"] * dd["clvlow"]
    res["ols e1 all"] = ols(dd, "e1", ["z1", "clvlow", "lsurge", "surge_clv"])
    res["ols e1 with hv"] = ols(dd, "e1", ["z1", "clvlow", "lsurge", "surge_clv", "hv", "z1_hv", "clv_hv"])
    hv = dd[dd.hv == 1]
    res["ols e1 high-vol only"] = ols(hv, "e1", ["z1", "clvlow", "lsurge"])
    # r1 reversal in high vol by year and coin (sign of slope of e1 on z1)
    def slope_t(g):
        if len(g) < 30: return pd.Series({"beta": np.nan, "t": np.nan, "n": len(g)})
        r = stats.linregress(g["z1"], g["e1"]); return pd.Series({"beta": r.slope, "t": r.slope / r.stderr, "n": len(g)})
    res["hv z1 slope by year"] = hv.groupby("yr").apply(slope_t).round(5)
    res["hv z1 slope by coin"] = hv.groupby("coin").apply(slope_t).round(5)
    res["hv clv slope by coin"] = hv.groupby("coin").apply(lambda g: slope_t(g.assign(z1=g["clvlow"]))).round(5)
    res["all z1 slope by vol quintile"] = dd.groupby("q_vol20").apply(slope_t).round(5)
    # z1 x clv within high vol
    res["hv e1 z1 x clv"] = X[X.q_vol20 == 4].pivot_table(index="q_z1", columns="q_clv", values="e1", aggfunc="mean").round(4)
    # does reversal last: e2, e3 on grid in high vol by q_z1
    for hh in [2, 3]:
        g = X[(X.pos % hh == 0) & (X.q_vol20 == 4)].dropna(subset=["e%d" % hh, "q_z1"])
        o = g.groupby("q_z1")["e%d" % hh].agg(["mean", "std", "count"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        res["hv e%d by q_z1" % hh] = o[["mean", "t", "count"]].round(5)
    # weekday by year stability
    res["e1 weekday x year"] = X.pivot_table(index="yr", columns="wd", values="e1", aggfunc="mean").round(4)
    return res
