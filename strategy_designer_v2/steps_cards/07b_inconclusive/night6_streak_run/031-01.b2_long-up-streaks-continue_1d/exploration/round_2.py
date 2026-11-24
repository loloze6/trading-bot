def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            up = np.zeros(n, int)
            for i in range(1, n):
                if c[i] > c[i-1]:
                    up[i] = up[i-1] + 1
            ts = pd.to_datetime(df["timestamp"])
            year = ts.dt.year.values
            dayid = ts.dt.floor("D").astype("int64").values
            for h in (3, 5, 7, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=year[i], d=dayid[i], fc=df["forecast"].iloc[i],
                                     up=up[i], r=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["r"].transform("mean")
    R["ex"] = R["r"] - R["drift"]
    def summ(g):
        n = len(g)
        if n < 3:
            return pd.Series(dict(n=n, mean_ex=np.nan, t=np.nan, t_day=np.nan, share_pos=np.nan))
        t = g["ex"].mean()/(g["ex"].std(ddof=1)/np.sqrt(n))
        dd = g.groupby("d")["ex"].sum()
        nd = len(dd)
        # day-clustered t: sum of per-day sums / n, se from per-day sums
        m = g["ex"].mean()
        dev = g.assign(dv=g["ex"]-m).groupby("d")["dv"].sum()
        se = np.sqrt((dev**2).sum())/n
        return pd.Series(dict(n=n, mean_ex=m, t=t, t_day=m/se if se > 0 else np.nan, share_pos=(g["ex"] > 0).mean()))
    out = {}
    R["upb"] = R["up"].clip(upper=6)
    for h in (5, 7, 10):
        out[f"h{h} by raw up streak"] = R[R.h == h].groupby("upb").apply(summ)
    L = R[R.up >= 4]
    out["up>=4 by horizon"] = L.groupby("h").apply(summ)
    out["h3 up>=4 by coin"] = L[L.h == 3].groupby("coin").apply(summ)
    out["h3 up>=4 by year"] = L[L.h == 3].groupby("year").apply(summ)
    out["h10 up>=3 by coin"] = R[(R.h == 10) & (R.up >= 3)].groupby("coin").apply(summ)
    out["h10 up>=3 by year"] = R[(R.h == 10) & (R.up >= 3)].groupby("year").apply(summ)
    # slope of ex on raw up streak (clipped 8) by horizon, excluding 2021
    res = {}
    for h in (3, 5, 7, 10):
        g = R[R.h == h]
        s = stats.linregress(g["up"].clip(upper=8), g["ex"])
        g2 = g[g.year != 2021]
        s2 = stats.linregress(g2["up"].clip(upper=8), g2["ex"])
        res[f"h{h}"] = dict(slope=s.slope, t=s.slope/s.stderr, slope_no2021=s2.slope, t_no2021=s2.slope/s2.stderr)
    out["raw up slope by horizon"] = pd.DataFrame(res).T
    # forecast vs raw streak
    g = R[(R.h == 3) & (R.up > 0)]
    out["h3 forecast mean by raw up"] = g.groupby("upb")["fc"].describe()[["count", "mean", "min", "max"]]
    return out
