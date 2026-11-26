def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.Series(df["close"].astype(float).values)
            n = len(c)
            if n < 60: continue
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            z = r7 / (sd30 * np.sqrt(7))
            z30 = r30 / (sd30 * np.sqrt(30))
            reg = df["regime"].values
            for h in (3, 7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     fwd=c[i+h]/c[i]-1, z=z[i], z30=z30[i], er=er[i], reg=reg[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["z", "er", "z30"])
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["mr"] = d.reg == "mean_reversion"
    def summ(g):
        x = g["ex"]
        if len(g) < 6:
            return pd.Series(dict(n=len(g)))
        sl = stats.linregress(g["z"], g["ex"])
        return pd.Series(dict(n=len(g), mean_ex=x.mean(), t_mean=x.mean()/(x.std()/np.sqrt(len(g))),
                              slope_z=sl.slope, t_slope=sl.slope/sl.stderr))
    out = {}
    m = d[d.mr]
    out["mr all cases by h"] = m.groupby("h").apply(summ)
    out["mr by h x z sign"] = m.assign(s=np.sign(m.z)).groupby(["h", "s"]).apply(summ)
    m7 = m[m.h == 7]
    out["mr h7 by z quintile"] = m7.groupby(pd.qcut(m7.z, 5)).apply(summ)
    f7 = m7[m7.z < 0]
    out["mr falls h7 by 30d return sign"] = f7.groupby(np.sign(f7.z30)).apply(summ)
    out["mr falls h7 by z30 tercile"] = f7.groupby(pd.qcut(f7.z30, 3)).apply(summ)
    # difference rises minus falls in mr, h7, Welch
    a = m7[m7.z > 0].ex; b = m7[m7.z < 0].ex
    out["mr h7 rises minus falls welch t"] = float(stats.ttest_ind(a, b, equal_var=False).statistic)
    out["mr h7 rises minus falls diff"] = float(a.mean() - b.mean())
    # mr by year, all cases slope
    out["mr h7 all by year"] = m7.groupby("year").apply(summ)
    out["mr h7 all by coin"] = m7.groupby("coin").apply(summ)
    return out
