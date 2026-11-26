def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 20
    drift = {}; usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets); usual[coin] = np.std(rets, ddof=1) if len(rets) > 1 else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, H):
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "regime": df["regime"].iloc[i], "usual": usual[coin]}
                for h in (10, 20, 40):
                    r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[coin] * h / 20) if i + h < n else np.nan
                r["r60"] = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                r["r20"] = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                # distance from in-window low over the available past (up to 365)
                lo = c[max(0, i - 365):i + 1].min() if i >= 60 else np.nan
                r["dist"] = c[i] / lo - 1 if i >= 60 else np.nan
                lo_prev = c[max(0, i - 365):i].min() if i >= 60 else np.nan
                r["broke"] = float(c[i] < lo_prev) if i >= 60 else np.nan
                r["ldist"] = np.log1p(r["dist"]) if i >= 60 else np.nan
                rows.append(r)
    g = pd.DataFrame(rows)

    def slope(d, x, y):
        d = d[[x, y, "day"]].dropna()
        if len(d) < 10:
            return pd.Series({"n": len(d), "days": np.nan, "slope": np.nan, "t": np.nan})
        X = d[x].values - d[x].mean(); Y = d[y].values - d[y].mean()
        b = (X * Y).sum() / (X * X).sum(); e = Y - b * X
        s = pd.Series(X * e).groupby(d["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (X * X).sum()
        return pd.Series({"n": len(d), "days": d.day.nunique(), "slope": b, "t": b / se})
    out = {}
    res = {}
    for h in (10, 20, 40):
        res["all_ldist_h%d" % h] = slope(g, "ldist", "u%d" % h)
        res["mr_ldist_h%d" % h] = slope(g[g.regime == "mean_reversion"], "ldist", "u%d" % h)
    out["slope on log distance from low"] = pd.DataFrame(res).T
    d = g.dropna(subset=["dist", "u20"]).copy()
    d["q"] = pd.qcut(d.ldist, 5, labels=False)
    out["dist quintile, all"] = d.groupby("q").agg(n=("u20", "size"), dist=("dist", "mean"),
        u20=("u20", "mean"), t=("u20", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["slope ldist by year"] = d.groupby("year").apply(lambda x: slope(x, "ldist", "u20"))
    out["broke"] = d.groupby("broke").agg(n=("u20", "size"), u20=("u20", "mean"),
        u10=("u10", "mean"), sd=("u20", "std"))
    # mr regime: mean u20 per year (regime underperformance stability)
    m = g[g.regime == "mean_reversion"].dropna(subset=["u20"])
    out["mr mean u20 by year"] = m.groupby("year").agg(n=("u20", "size"), u20=("u20", "mean"))
    o = g[g.regime != "mean_reversion"].dropna(subset=["u20"])
    out["regime mean u20"] = pd.Series({"mr": m.u20.mean(), "mr_t_daycl": m.groupby("day").u20.sum().mean() / (m.groupby("day").u20.sum().std() / np.sqrt(m.day.nunique())) / 1,
                                        "out": o.u20.mean(), "n_mr": len(m), "n_out": len(o)})
    return out
