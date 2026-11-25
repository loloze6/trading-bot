def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "z": r / sd, "sd": sd,
                "f3": c.shift(-3)/c - 1, "f1": c.shift(-1)/c - 1,
                "m20": (c/c.shift(20) - 1)/(sd*np.sqrt(20)),
                "m10": (c/c.shift(10) - 1)/(sd*np.sqrt(10)),
                "m5": (c/c.shift(5) - 1)/(sd*np.sqrt(5)),
                "m60": c/c.shift(60) - 1,
                "agit": (b["regime"] != "chop"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g3 = d[d["pos"] % 3 == 0].dropna(subset=["f3"])
    d["x3"] = d["f3"] - d["coin"].map(g3.groupby("coin")["f3"].mean())
    d["x1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    g = d[d["pos"] % 3 == 0].dropna(subset=["x3"]).copy()

    def clus_t(x, col, y="x3"):
        x = x.dropna(subset=[col, y])
        X = x[col].values; Y = x[y].values
        Xc = X - X.mean()
        b = (Xc*(Y-Y.mean())).sum()/(Xc**2).sum()
        e = Y - Y.mean() - b*Xc
        s = pd.Series(Xc*e).groupby(x["day"].values).sum()
        se = np.sqrt((s**2).sum())/(Xc**2).sum()
        return pd.Series({"n": len(x), "days": x["day"].nunique(), "slope%": 100*b, "t_day": b/se})

    res = {}
    for col in ["m5", "m10", "m20", "z"]:
        res[col+" all"] = clus_t(g, col)
        res[col+" agit"] = clus_t(g[g.agit], col)
        res[col+" calm"] = clus_t(g[~g.agit], col)
    out["slopes of x3 on signal (day-clustered)"] = pd.DataFrame(res).T.round(3)

    out["m20 slope by window"] = g.groupby("w").apply(lambda x: clus_t(x, "m20")).round(3)
    out["m20 slope by coin"] = g.groupby("coin").apply(lambda x: clus_t(x, "m20")).round(3)
    g["trend"] = pd.cut(g["m60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    out["m20 slope by trend x agit"] = g.groupby(["trend", "agit"]).apply(lambda x: clus_t(x, "m20")).round(3)
    # z reversal (both sides) in agitated by trend
    out["z slope agit by trend"] = g[g.agit].groupby("trend").apply(lambda x: clus_t(x, "z")).round(3)
    # weekday consistency
    d1 = d.dropna(subset=["x1"])
    out["x1 Thu+Fri minus Mon+Wed by year"] = d1.groupby("yr").apply(lambda x: pd.Series({
        "thufri%": 100*x[x.wd.isin([3,4])].x1.mean(), "monwed%": 100*x[x.wd.isin([0,2])].x1.mean(),
        "t": stats.ttest_ind(x[x.wd.isin([3,4])].x1, x[x.wd.isin([0,2])].x1, equal_var=False).statistic}))
    return out
