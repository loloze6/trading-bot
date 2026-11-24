def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            # 30-day past return for regime
            for h in (1, 2, 3, 5, 10):
                for i in range(0, n - h, h):
                    past30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i+h]/c[i]-1,
                                     r1=r1[i], past30=past30, year=ts.iloc[i].year,
                                     dayk=ts.iloc[i].strftime("%j%Y")))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    out = {}

    def slope_t(g):
        g = g.dropna(subset=["f", "ex"])
        x = g["f"] - g["f"].mean()
        b = (x*g["ex"]).sum()/(x**2).sum()
        e = g["ex"] - g["ex"].mean() - b*x
        s = (x*e).groupby(g["dayk"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum()*G/(G-1))/(x**2).sum()
        return pd.Series(dict(slope=b, t=b/se, n=len(g)))

    out["by horizon"] = d.groupby("h").apply(slope_t)
    d2 = d[d.h == 2].copy()
    out["h2 by coin"] = d2.groupby("coin").apply(slope_t)
    out["h2 by year"] = d2.groupby("year").apply(slope_t)
    pos = d2[d2.f > 0].copy()
    pos["q"] = pd.qcut(pos["f"], 5, labels=False)
    out["h2 positive-forecast quintiles"] = pos.groupby("q").agg(fmean=("f", "mean"), ex=("ex", "mean"), ret=("ret", "mean"), n=("ex", "size"))
    out["h2 forecast zero ex mean"] = d2[d2.f == 0]["ex"].agg(["mean", "count"])
    d2["trend"] = np.where(d2.past30 > 0, "up30", np.where(d2.past30 <= 0, "down30", "na"))
    out["h2 by 30d trend"] = d2[d2.trend != "na"].groupby("trend").apply(slope_t)
    # quintiles by horizon for positive forecasts
    res = {}
    for h in (1, 3, 5, 10):
        p = d[(d.h == h) & (d.f > 0)].copy()
        p["q"] = pd.qcut(p["f"], 5, labels=False)
        res[h] = p.groupby("q")["ex"].mean()
    out["ex by quintile per horizon"] = pd.DataFrame(res)
    pos["trend"] = np.where(pos.past30 > 0, "up30", "down30")
    out["h2 pos quint x trend ex"] = pos[pos.past30.notna()].groupby(["trend", "q"])["ex"].agg(["mean", "count"])
    return out
