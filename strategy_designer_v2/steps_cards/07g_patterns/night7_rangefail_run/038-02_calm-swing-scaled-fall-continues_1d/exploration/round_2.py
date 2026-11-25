def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            s5 = r5 / (sd20 * np.sqrt(5))
            z = (s5 - s5.rolling(60, min_periods=20).mean()) / s5.rolling(60, min_periods=20).std()
            r10 = c / c.shift(10) - 1
            s10 = r10 / (sd20 * np.sqrt(10))
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "s5": s5, "z": z, "s10": s10,
                               "f5": c.shift(-5) / c - 1, "f3": c.shift(-3) / c - 1, "f10": c.shift(-10) / c - 1,
                               "r1": r1, "calm": (b["regime"] != "chop").astype(int),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def clus(sub, xcol, ycol):
        sub = sub.dropna(subset=[xcol, ycol])
        x = sub[xcol].values; y = sub[ycol].values
        X = np.c_[np.ones_like(x), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        sc = pd.DataFrame(X * e[:, None]).groupby(sub["day"].values).sum().values
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ (sc.T @ sc) @ XtXi
        return pd.Series({"slope%": 100 * beta[1], "t": beta[1] / np.sqrt(V[1, 1]), "n": len(sub), "days": sub["day"].nunique()})

    out = {}
    res = {}
    for h in [3, 5, 10]:
        gg = d[(d["pos"] % h == 0)].copy()
        gg["ex"] = gg[f"f{h}"] - gg.groupby("coin")[f"f{h}"].transform("mean")
        for cm in [0, 1]:
            s = gg[gg["calm"] == cm]
            res[f"h{h} calm{cm} raw s5"] = clus(s, "s5", "ex")
            res[f"h{h} calm{cm} std z"] = clus(s, "z", "ex")
            res[f"h{h} calm{cm} s10"] = clus(s, "s10", "ex")
            res[f"h{h} calm{cm} s5 up only"] = clus(s[s["s5"] > 0], "s5", "ex")
            res[f"h{h} calm{cm} s5 down only"] = clus(s[s["s5"] < 0], "s5", "ex")
    out["slopes"] = pd.DataFrame(res).T
    g = d[d["pos"] % 5 == 0].copy()
    g["ex"] = g["f5"] - g.groupby("coin")["f5"].transform("mean")
    c1 = g[g["calm"] == 1]
    out["calm s5 slope by year"] = c1.groupby("yr").apply(lambda s: clus(s, "s5", "ex"))
    out["calm s5 slope by coin"] = c1.groupby("coin").apply(lambda s: clus(s, "s5", "ex"))
    out["calm s5 slope by window"] = c1.groupby("win").apply(lambda s: clus(s, "s5", "ex"))
    # weekday, day-clustered: mean over coins per day then t across days
    dd = d.dropna(subset=["r1"])
    dm = dd.groupby(["day", "wd"])["r1"].mean().reset_index()
    out["weekday day-mean ret"] = dm.groupby("wd")["r1"].agg(mean="mean", n="count", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    return out
