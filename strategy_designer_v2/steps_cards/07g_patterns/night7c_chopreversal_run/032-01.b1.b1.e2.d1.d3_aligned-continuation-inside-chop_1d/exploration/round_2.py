def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            vol = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "r7": r7, "r30": r30,
                               "s7": r7 / (vol * np.sqrt(7)), "vol": vol, "vr": vol / vol90,
                               "f7": c.shift(-7) / c - 1, "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                               "r1": r1, "z1": r1 / vol.shift(1), "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                               "yr": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def ct(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 20: return pd.Series({"n": len(d)})
        dev = d[col] - d[col].mean()
        s = dev.groupby([d["w"], d["day"]]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(d)
        return pd.Series({"n": len(d), "days": G, "mean": d[col].mean(), "t_cl": d[col].mean() / se})

    # daily drift and excess
    dm = A.groupby("coin")["f1"].mean()
    A["a1"] = A["f1"] - A["coin"].map(dm)
    A["zb"] = pd.cut(A["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["next-day excess by z1 bin, day-clustered"] = A.groupby("zb").apply(lambda d: ct(d, "a1"))
    # 3-day after big down day, on 3-day grid
    g3 = A[A["pos"] % 3 == 0].copy()
    g3["a3"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    out["3-day excess by z1 bin (3-day grid), clustered"] = g3.groupby("zb").apply(lambda d: ct(d, "a3"))
    # down-day reversal: graded slope on negative z1 only, by vol tercile and by regime
    A["volq"] = A.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    neg = A[A["z1"] < 0].dropna(subset=["a1", "z1"])
    def sl(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 30: return pd.Series({"n": len(d)})
        r = stats.linregress(d[x], d[y]); return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope / r.stderr})
    out["down days: next-day excess on z1, by vol tercile"] = neg.groupby("volq").apply(lambda d: sl(d, "z1", "a1"))
    out["down days: by chop/trend"] = neg.groupby(neg["er"] <= 0.3).apply(lambda d: sl(d, "z1", "a1"))
    out["down days: by year"] = neg.groupby("yr").apply(lambda d: sl(d, "z1", "a1"))
    out["down days: by coin"] = neg.groupby("coin").apply(lambda d: sl(d, "z1", "a1"))
    pos = A[A["z1"] > 0].dropna(subset=["a1", "z1"])
    out["up days: next-day excess on z1"] = pd.DataFrame([sl(pos, "z1", "a1")])
    # weekday excess, clustered
    out["weekday next-day excess, clustered"] = A.assign(wdn=(A["wd"] + 1) % 7).groupby("wdn").apply(lambda d: ct(d, "a1"))
    out["weekday by year: Fri+Sat minus others"] = A.groupby("yr").apply(lambda d: d.loc[d["wd"].isin([3, 4]), "a1"].mean() - d.loc[~d["wd"].isin([3, 4]), "a1"].mean())
    # 7-day continuation: chop aligned by vol tercile and by vol ratio
    g = A[A["pos"] % 7 == 0].copy()
    g["adj"] = g["f7"] - g["coin"].map(g.groupby("coin")["f7"].mean())
    g = g.dropna(subset=["adj", "s7", "er", "r30"])
    ca = g[(g["er"] <= 0.3) & (np.sign(g["r7"]) == np.sign(g["r30"]))]
    out["chop aligned: s7 slope by vol tercile"] = ca.groupby("volq").apply(lambda d: sl(d, "s7", "adj"))
    g["vrq"] = g.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["all grid: s7 slope by vol ratio tercile (30d/90d)"] = g.groupby("vrq").apply(lambda d: sl(d, "s7", "adj"))
    out["all grid: s7 slope by vol tercile, by year"] = g.groupby(["yr", "volq"]).apply(lambda d: sl(d, "s7", "adj")).unstack()
    lo = g[g["volq"] == 0]
    out["low vol: s7 slope chop vs trend"] = lo.groupby(lo["er"] <= 0.3).apply(lambda d: sl(d, "s7", "adj"))
    return out
