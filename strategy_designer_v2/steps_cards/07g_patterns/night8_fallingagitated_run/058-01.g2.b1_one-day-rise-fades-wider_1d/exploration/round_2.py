def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "z1": r1 / sd30, "z3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                               "r60": c / c.shift(60) - 1,
                               "f3": c.shift(-3) / c - 1, "f1": c.shift(-1) / c - 1,
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "dkey": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift3 = d[d.pos % 3 == 0].groupby("coin")["f3"].mean()
    d["x3"] = d["f3"] - d["coin"].map(drift3)
    d["x1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    out = {}
    def cl_slope(sub, xcol, ycol):
        sub = sub.dropna(subset=[xcol, ycol])
        x = sub[xcol].values; y = sub[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in sub.groupby("dkey").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return [len(sub), sub.dkey.nunique(), beta[1], beta[1] / np.sqrt(V[1, 1])]
    def cl_mean(sub, col):
        sub = sub.dropna(subset=[col])
        s = sub.groupby("dkey")[col].sum(); n = len(sub)
        m = sub[col].mean()
        se = np.sqrt(((s - sub.groupby("dkey")[col].count() * m) ** 2).sum()) / n
        return [n, sub.dkey.nunique(), m, m / se]
    g = d[d.pos % 3 == 0]
    res = {}
    for ip in [0, 1]:
        for side, s in [("z1up", g.z1 > 0), ("z1down", g.z1 < 0)]:
            res[f"prof{ip}_{side}_absz1"] = cl_slope(g[(g.inprof == ip) & s].assign(a=lambda x: x.z1.abs()), "a", "x3")
        for side, s in [("z3up", g.z3 > 0), ("z3down", g.z3 < 0)]:
            res[f"prof{ip}_{side}_absz3"] = cl_slope(g[(g.inprof == ip) & s].assign(a=lambda x: x.z3.abs()), "a", "x3")
    out["day-clustered slopes"] = pd.DataFrame(res, index=["n", "days", "slope", "t"]).T.round(4)
    # trend groups outside profile, z3 continuation
    g2 = g[g.inprof == 0].copy()
    g2["trend"] = np.where(g2.r60 > 0.10, "rising", np.where(g2.r60 < -0.10, "falling", "choppy"))
    g2.loc[g2.r60.isna(), "trend"] = "na"
    res = {}
    for tr in ["rising", "choppy", "falling", "na"]:
        res[tr] = cl_slope(g2[g2.trend == tr], "z3", "x3")
    out["outside profile: x3 on signed z3 by 60d trend"] = pd.DataFrame(res, index=["n", "days", "slope", "t"]).T.round(4)
    # weekday, clustered by day, by year
    res = {}
    for wd in range(7):
        res[f"all_wd{wd}"] = cl_mean(d[d.wd == wd], "x1")
    out["weekday next-day excess, day-clustered"] = pd.DataFrame(res, index=["n", "days", "mean", "t"]).T.round(4)
    t = d.dropna(subset=["x1"]).assign(thu_fri=lambda x: x.wd.isin([3, 4]).astype(int), wed=lambda x: (x.wd == 2).astype(int))
    yy = t.groupby(["yr"]).apply(lambda x: pd.Series({"thufri": x[x.thu_fri == 1].x1.mean(), "wed": x[x.wed == 1].x1.mean(), "n": len(x)}))
    out["weekday by year"] = yy.round(4)
    return out
