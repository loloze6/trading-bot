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
            up = np.zeros(n, int); dn = np.zeros(n, int)
            for i in range(1, n):
                if c[i] > c[i-1]:
                    up[i] = up[i-1] + 1
                elif c[i] < c[i-1]:
                    dn[i] = dn[i-1] + 1
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=year[i], fc=df["forecast"].iloc[i],
                                     up=up[i], dn=dn[i], r=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["r"].transform("mean")
    R["ex"] = R["r"] - R["drift"]
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean()/(g["ex"].std(ddof=1)/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    R3 = R[R.h == 3].copy()
    R3["fcbin"] = pd.cut(R3["fc"], [-0.1, 0.001, 5, 10, 19.99, 20.1], labels=["0", "0-5", "5-10", "10-20", "20"])
    out["h3 by forecast bin"] = R3.groupby("fcbin").apply(summ)
    R3["upb"] = R3["up"].clip(upper=6)
    out["h3 by raw up streak"] = R3.groupby("upb").apply(summ)
    R3["dnb"] = R3["dn"].clip(upper=6)
    out["h3 by raw down streak"] = R3.groupby("dnb").apply(summ)
    for h in (1, 3, 5, 10):
        g = R[R.h == h]
        s = stats.linregress(g["fc"], g["ex"])
        sd = stats.linregress(g["dn"].clip(upper=8), g["ex"])
        su = stats.linregress(g["up"].clip(upper=8), g["ex"])
        out[f"slopes h{h}"] = pd.Series(dict(n=len(g), fc_slope_t=s.slope/s.stderr,
                                             up_slope_t=su.slope/su.stderr, dn_slope=sd.slope, dn_slope_t=sd.slope/sd.stderr))
    pos = R3[R3.fc > 0]
    out["h3 fc>0 by coin"] = pos.groupby("coin").apply(summ)
    out["h3 fc>0 by year"] = pos.groupby("year").apply(summ)
    out["h3 dn>=3 by coin"] = R3[R3.dn >= 3].groupby("coin").apply(summ)
    out["h3 dn>=3 by year"] = R3[R3.dn >= 3].groupby("year").apply(summ)
    return out
