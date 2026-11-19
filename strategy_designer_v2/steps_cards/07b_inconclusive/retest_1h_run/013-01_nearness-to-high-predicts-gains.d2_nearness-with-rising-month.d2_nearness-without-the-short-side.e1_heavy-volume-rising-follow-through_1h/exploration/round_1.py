def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def grid(h):
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                r = df["regime"].values
                ts = pd.to_datetime(df["timestamp"])
                n = len(df)
                for i in range(0, n - h, h):
                    rows.append((coin, w, ts.iloc[i].year, ts.iloc[i].hour, f[i], r[i], c[i+h]/c[i]-1))
        g = pd.DataFrame(rows, columns=["coin","w","year","hour","f","reg","ret"])
        g["ex"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        return g
    def slope(d):
        d = d.dropna(subset=["f","ex"])
        if len(d) < 10 or d["f"].std() == 0:
            return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        res = stats.linregress(d["f"], d["ex"])
        return pd.Series({"n": len(d), "npos": (d["f"]>0).sum(), "slope": res.slope, "t": res.slope/res.stderr})
    hs = {}
    for h in [24, 72, 168, 336]:
        g = grid(h)
        tr = g[g.reg == "trending"]
        hs[f"{h}h"] = slope(tr)
        if h == 72:
            g72 = g; tr72 = tr
    out["slope by horizon"] = pd.DataFrame(hs).T
    out["by coin 72"] = tr72.groupby("coin").apply(slope)
    out["by year 72"] = tr72.groupby("year").apply(slope)
    out["by window 72 (t)"] = tr72.groupby("w").apply(slope)
    pos = tr72[tr72.f > 0].copy()
    pos["q"] = pd.qcut(pos["f"].rank(method="first"), 3, labels=["low","mid","high"])
    z = tr72[tr72.f == 0]
    tab = pos.groupby("q")["ex"].agg(["count","mean","std"])
    tab.loc["zero"] = [len(z), z["ex"].mean(), z["ex"].std()]
    out["excess by forecast group"] = tab
    # positive forecast vs zero, t
    out["pos minus zero welch t"] = float(stats.ttest_ind(pos["ex"], z["ex"], equal_var=False).statistic)
    # non-trending bars: does forecast-like effect exist? (no forecast there) skip
    # market-move drowning: share of variance
    out["excess ret std trending 72"] = float(tr72["ex"].std())
    out["slope within positive forecasts only"] = slope(pos)
    return out
