def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 20
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
        usual[coin] = np.std(rets, ddof=1) if len(rets) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, H):
                r = {"coin": coin, "win": w, "pos": i, "year": ts.iloc[i].year,
                     "day": ts.iloc[i].normalize(), "regime": df["regime"].iloc[i],
                     "fc": df["forecast"].iloc[i]}
                for h in (5, 10, 20, 40):
                    r["f%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                r["r60"] = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                r["r20"] = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                r["drift"] = drift[coin]
                r["usual"] = usual[coin]
                rows.append(r)
    g = pd.DataFrame(rows)
    g["u20"] = g["f20"] - g["drift"]
    out = {}
    mr = g[g.regime == "mean_reversion"]
    out["regime counts"] = g.regime.value_counts()
    out["mr cases with r60 / with any"] = pd.Series({"with_r60": mr.r60.notna().sum(), "all_mr": len(mr),
                                                    "with_f20": mr.f20.notna().sum()})

    def slope(d, x, y):
        d = d[[x, y, "day"]].dropna()
        if len(d) < 10:
            return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        X = d[x].values - d[x].mean()
        Y = d[y].values - d[y].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        s = pd.Series(X * e).groupby(d["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (X * X).sum()
        return pd.Series({"n": len(d), "days": d.day.nunique(), "slope": b, "t": b / se})

    # slope by horizon, regime vs outside
    res = {}
    for h in (5, 10, 20, 40):
        g["u%d" % h] = g["f%d" % h] - g["drift"] * h / 20
        res["mr_h%d" % h] = slope(g[g.regime == "mean_reversion"], "r60", "u%d" % h)
        res["out_h%d" % h] = slope(g[g.regime != "mean_reversion"], "r60", "u%d" % h)
        res["mr_r20_h%d" % h] = slope(g[g.regime == "mean_reversion"], "r20", "u%d" % h)
    out["slope by horizon"] = pd.DataFrame(res).T
    mr = g[g.regime == "mean_reversion"].copy()
    out["slope by year (mr)"] = mr.groupby("year").apply(lambda d: slope(d, "r60", "u20"))
    out["slope by coin (mr)"] = mr.groupby("coin").apply(lambda d: slope(d, "r60", "u20"))
    m = mr.dropna(subset=["r60", "u20"]).copy()
    m["q"] = pd.qcut(m.r60, 5, labels=False)
    out["r60 quintile (mr)"] = m.groupby("q").agg(n=("u20", "size"), r60=("r60", "mean"),
                                                 u20=("u20", "mean"), f20=("f20", "mean"),
                                                 t=("u20", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    o = g[g.regime != "mean_reversion"].dropna(subset=["r60", "u20"]).copy()
    o["q"] = pd.qcut(o.r60, 5, labels=False)
    out["r60 quintile (outside)"] = o.groupby("q").agg(n=("u20", "size"), r60=("r60", "mean"),
                                                      u20=("u20", "mean"))
    # side: positive vs negative r60 inside mr
    m["side"] = np.where(m.r60 > 0, "rebound", "falling")
    out["side (mr)"] = m.groupby("side").agg(n=("u20", "size"), u20=("u20", "mean"),
                                            sd=("u20", "std"))
    out["slope rebound only"] = slope(m[m.r60 > 0], "r60", "u20")
    # strength
    out["strength mr short cases"] = pd.Series({
        "mean -u20/usual (r60>0)": (-m[m.r60 > 0].u20 / m[m.r60 > 0].usual).mean()})
    return out
