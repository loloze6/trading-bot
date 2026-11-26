def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            up = np.zeros(n, int); dn = np.zeros(n, int)
            for i in range(1, n):
                if c[i] > c[i-1]: up[i] = up[i-1] + 1
                if c[i] < c[i-1]: dn[i] = dn[i-1] + 1
            ret30 = pd.Series(c).pct_change(30).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            fc = df["forecast"].astype(float).values
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, up=up[i], dn=dn[i], fc=fc[i],
                                     r=c[i+h]/c[i]-1, r30=ret30[i], yr=yr[i],
                                     ts=str(df["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # by up streak bin and horizon
    d["upb"] = d["up"].clip(upper=5)
    d["dnb"] = d["dn"].clip(upper=5)
    out["up streak x horizon mean excess"] = d.pivot_table(index="upb", columns="h", values="ex", aggfunc="mean")
    out["up streak x horizon t"] = d.groupby(["h", "upb"])["ex"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).unstack()
    out["down streak x horizon mean excess"] = d.pivot_table(index="dnb", columns="h", values="ex", aggfunc="mean")
    out["down streak x horizon t"] = d.groupby(["h", "dnb"])["ex"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).unstack()
    d5 = d[d.h == 5]
    out["h5 up>=1 by coin"] = d5[d5.up >= 1].groupby("coin")["ex"].apply(tt).unstack()
    out["h5 up>=3 by year"] = d5[d5.up >= 3].groupby("yr")["ex"].apply(tt).unstack()
    d5 = d5.assign(trend=np.where(d5.r30 > 0, "r30>0", np.where(d5.r30 <= 0, "r30<=0", "na")))
    out["h5 up streak x 30d trend"] = d5.pivot_table(index="upb", columns="trend", values="ex", aggfunc="mean")
    out["h5 up streak x 30d trend n"] = d5.pivot_table(index="upb", columns="trend", values="ex", aggfunc="count")
    out["h5 down streak x 30d trend"] = d5.pivot_table(index="dnb", columns="trend", values="ex", aggfunc="mean")
    return out
