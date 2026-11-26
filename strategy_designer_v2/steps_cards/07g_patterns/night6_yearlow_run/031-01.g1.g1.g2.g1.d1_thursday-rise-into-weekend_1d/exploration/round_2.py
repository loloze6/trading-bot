def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        g2 = []; g1 = []; g4 = []
        for w, df in wins.items():
            c = df["close"].values
            if len(c) > 2:
                a = c[0::2]; g2 += list(a[1:] / a[:-1] - 1)
            if len(c) > 4:
                a = c[0::4]; g4 += list(a[1:] / a[:-1] - 1)
            g1 += list(c[1:] / c[:-1] - 1)
        d2 = np.nanmean(g2); d1 = np.nanmean(g1); d4 = np.nanmean(g4); sd2 = np.nanstd(g2, ddof=1)
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            if ts.isna().all():
                ts = pd.to_datetime(d["timestamp"], unit="ms", utc=True)
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            d["hour"] = ts.dt.hour.values
            c = d["close"]
            d["r1"] = c / c.shift(1) - 1
            d["r14"] = c / c.shift(14) - 1
            d["r7"] = c / c.shift(7) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["x2"] = c.shift(-2) / c - 1 - d2
            d["x4"] = c.shift(-4) / c - 1 - d4
            d["x1"] = c.shift(-1) / c - 1 - d1
            d["sd2"] = sd2
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    out["hours seen"] = A["hour"].value_counts().head(3)
    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    def slope(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        z = g.groupby("coin")[xcol].transform(lambda s: (s - s.mean()) / s.std())
        r = stats.linregress(z, g[ycol])
        return pd.Series({"n": len(g), "slope%": 100 * r.slope, "t": r.slope / r.stderr})
    G2 = A[A["pos"] % 2 == 0]
    G4 = A[A["pos"] % 4 == 0]
    dn = G2[G2["r14"] <= 0]
    out["grid2 r14<=0: slope x2 on z r14, all weekdays"] = slope(dn, "r14", "x2")
    out["grid2 r14<=0: slope by coin"] = dn.groupby("coin").apply(lambda g: slope(g, "r14", "x2"))
    out["grid2 r14<=0: slope by year"] = dn.groupby("year").apply(lambda g: slope(g, "r14", "x2"))
    out["grid2 r14<=0 excl Thu/Fri bar: slope"] = slope(dn[~dn["wd"].isin([3, 4])], "r14", "x2")
    out["grid4 r14<=0: slope x4"] = slope(G4[G4["r14"] <= 0], "r14", "x4")
    out["grid2 r14>0: slope x2 all weekdays"] = slope(G2[G2["r14"] > 0], "r14", "x2")
    # fall quintiles within r14<=0
    q = dn.groupby("coin")["r14"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["grid2 r14<=0 x2 by r14 quintile"] = dn.groupby(q)["x2"].apply(tstat).unstack()
    # one-day drop bounce
    dn1 = G2[G2["r1"] <= 0]
    out["grid2 r1<=0: slope x2 on z r1"] = slope(dn1, "r1", "x2")
    out["grid2 r1<=0: slope by year"] = dn1.groupby("year").apply(lambda g: slope(g, "r1", "x2"))
    out["grid2 r1<=0 slope by vol tercile"] = dn1.groupby(dn1.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))).apply(lambda g: slope(g, "r1", "x2"))
    # weekend day excess by year and coin (Fri, Sat bars: wd 4,5)
    wk = A[A["wd"].isin([4, 5])]
    out["Fri+Sat bar 1d excess by year"] = wk.groupby("year")["x1"].apply(tstat).unstack()
    out["Fri+Sat bar 1d excess by coin"] = wk.groupby("coin")["x1"].apply(tstat).unstack()
    # Thursday bar, r14>0, by year (tested idea's stability)
    th = A[(A["wd"] == 3) & (A["r14"] > 0)]
    out["Thu r14>0 slope by year"] = th.groupby("year").apply(lambda g: slope(g, "r14", "x2"))
    return out
