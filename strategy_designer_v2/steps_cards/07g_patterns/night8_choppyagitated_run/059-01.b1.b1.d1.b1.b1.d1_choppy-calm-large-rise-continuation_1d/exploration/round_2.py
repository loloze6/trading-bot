def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def tclust(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 5: return pd.Series(dict(n=n, days=0, mean=np.nan, t=np.nan))
        m = x[col].mean()
        d = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / n
        return pd.Series(dict(n=n, days=x["day"].nunique(), mean=m, t=m / se if se else np.nan))
    def slope_t(x, xc, yc):
        x = x.dropna(subset=[xc, yc])
        if len(x) < 15: return pd.Series(dict(n=len(x), slope=np.nan, t=np.nan))
        X = x[xc] - x[xc].mean(); y = x[yc] - x[yc].mean()
        b = (X * y).sum() / (X ** 2).sum()
        e = y - b * X
        s = (X * e).groupby(x["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(n=len(x), days=x["day"].nunique(), slope=b, t=b / se))
    G = {h: [] for h in (1, 3, 7, 14)}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            r1 = c / c.shift(1) - 1
            r7 = c / c.shift(7) - 1
            s7 = r7 / r7.abs().rolling(30, min_periods=20).mean()
            vol30 = r1.rolling(30, min_periods=20).std()
            r60 = c / c.shift(60) - 1
            z1 = r1 / vol30
            for h in G:
                f = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if np.isnan(f.iloc[i]): continue
                    G[h].append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek,
                                     s7=s7.iloc[i], z1=z1.iloc[i], r60=r60.iloc[i], vol=vol30.iloc[i],
                                     inprof=df["regime"].iloc[i] == "unknown", f=f.iloc[i]))
    for h in G:
        g = pd.DataFrame(G[h])
        g["ex"] = g["f"] - g.groupby("coin")["f"].transform("mean")
        G[h] = g
    g1 = G[1]
    out["wd_next1d_excess"] = g1.groupby("wd").apply(lambda x: tclust(x, "ex"))
    for h in (7, 14):
        g = G[h].copy()
        g["tr"] = pd.cut(g["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
        g = g[~g.inprof]
        out[f"s7_slope_h{h}_outprof_by_trend"] = g.groupby("tr").apply(lambda x: slope_t(x, "s7", "ex"))
    for h in (3, 7):
        g = G[h].copy()
        g["volt"] = g.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
        out[f"z1_slope_h{h}_by_voltercile"] = g.groupby("volt").apply(lambda x: slope_t(x, "z1", "ex"))
        g["tr"] = pd.cut(g["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
        out[f"s7_slope_h{h}_by_trend_all"] = g.groupby("tr").apply(lambda x: slope_t(x, "s7", "ex"))
    g = G[14]
    out["s7_slope_h14_all"] = slope_t(g, "s7", "ex")
    out["s7_slope_h14_inprof"] = slope_t(g[g.inprof], "s7", "ex")
    return out
