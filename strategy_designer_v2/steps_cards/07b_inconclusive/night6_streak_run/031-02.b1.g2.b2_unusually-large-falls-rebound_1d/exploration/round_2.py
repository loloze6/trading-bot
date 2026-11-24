def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            sd = pd.Series(r1).rolling(60, min_periods=30).std().values
            z = r1/sd
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for h in (1, 2):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], z=z[i], ret=c[i+h]/c[i]-1,
                                     year=ts.iloc[i].year, dayk=ts.iloc[i].strftime("%j%Y")))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    d["fall"] = (-d["z"]).clip(lower=0)
    out = {}

    def slope_t(g, col="f"):
        g = g.dropna(subset=[col, "ex"])
        x = g[col] - g[col].mean()
        b = (x*g["ex"]).sum()/(x**2).sum()
        e = g["ex"] - g["ex"].mean() - b*x
        s = (x*e).groupby(g["dayk"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum()*G/(G-1))/(x**2).sum()
        return pd.Series(dict(slope=b, t=b/se, n=len(g)))

    def mean_t(g):
        s = g.groupby("dayk")["ex"].sum()
        cnt = g.groupby("dayk").size()
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["dayk"]).sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum()*G/(G-1))/len(g)
        return pd.Series(dict(mean=m, t=m/se, n=len(g), days=G))

    d1 = d[d.h == 1]; d2 = d[d.h == 2]
    out["h1 by coin"] = d1.groupby("coin").apply(slope_t)
    out["h1 by year"] = d1.groupby("year").apply(slope_t)
    out["raw scaled fall slope h1/h2"] = pd.DataFrame({h: slope_t(d[d.h == h], "fall") for h in (1, 2)}).T
    for h, g in ((1, d1), (2, d2)):
        p = g[g.f > 0].copy()
        p["q"] = pd.qcut(p["f"], 5, labels=False)
        out[f"h{h} quintile mean t"] = p.groupby("q").apply(mean_t)
    # raw z bins
    b = d2.dropna(subset=["z"]).copy()
    b["zb"] = pd.cut(-b["z"], [-np.inf, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    out["h2 by raw fall in sds"] = b.groupby("zb").apply(mean_t)
    b1 = d1.dropna(subset=["z"]).copy()
    b1["zb"] = pd.cut(-b1["z"], [-np.inf, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    out["h1 by raw fall in sds"] = b1.groupby("zb").apply(mean_t)
    return out
