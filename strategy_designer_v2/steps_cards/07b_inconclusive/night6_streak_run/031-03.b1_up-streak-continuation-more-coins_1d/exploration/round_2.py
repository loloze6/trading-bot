def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            up = np.zeros(n, int)
            for i in range(1, n):
                if c[i] > c[i-1]: up[i] = up[i-1] + 1
            s = pd.Series(c)
            r30 = s.pct_change(30).values; r60 = s.pct_change(60).values; r90 = s.pct_change(90).values
            fc = df["forecast"].astype(float).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            h = 5
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, up=up[i], fc=fc[i], r=c[i+h]/c[i]-1,
                                 r30=r30[i], r60=r60[i], r90=r90[i], yr=yr[i], day=ts[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    def clus_slope(sub, x="fc"):
        sub = sub.dropna(subset=[x, "ex"])
        if len(sub) < 30: return pd.Series(dict(n=len(sub), slope=np.nan, t=np.nan))
        X = sub[x].values; y = sub["ex"].values
        xm = X - X.mean(); b = (xm*y).sum()/(xm**2).sum()
        a = y.mean() - b*X.mean(); e = y - a - b*X
        g = pd.Series(xm*e).groupby(sub["day"].values).sum()
        se = np.sqrt((g**2).sum())/(xm**2).sum()
        return pd.Series(dict(n=len(sub), days=sub["day"].nunique(), slope=b, t=b/se))
    def clus_mean(sub):
        sub = sub.dropna(subset=["ex"])
        g = sub.groupby("day")["ex"].sum(); m = sub["ex"].mean()
        dev = (sub["ex"]-m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(sub)
        return pd.Series(dict(n=len(sub), days=sub["day"].nunique(), mean=m, t=m/se))
    out = {}
    for L in ("r30", "r60", "r90"):
        res = {}
        for lab, m in (("pos", d[L] > 0), ("neg", d[L] <= 0)):
            res[lab+" slope fc"] = clus_slope(d[m])
            res[lab+" mean fc>0"] = clus_mean(d[m & (d.fc > 0)])
            res[lab+" mean fc==0"] = clus_mean(d[m & (d.fc == 0)])
        out[L+" split"] = pd.DataFrame(res).T
    d["fcb"] = pd.cut(d.fc, [-0.1, 0.01, 5, 10, 15, 20.1], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["fc bin x r30 sign mean ex"] = d.pivot_table(index="fcb", columns=d.r30 > 0, values="ex", aggfunc="mean")
    out["fc bin x r30 sign n"] = d.pivot_table(index="fcb", columns=d.r30 > 0, values="ex", aggfunc="count")
    pos = d[(d.r30 > 0) & (d.fc > 0)]
    out["r30>0 fc>0 by year"] = pos.groupby("yr").apply(clus_mean)
    out["r30>0 slope by year"] = d[d.r30 > 0].groupby("yr").apply(clus_slope)
    out["slope on up x r30 interaction"] = clus_slope(d.assign(z=d.up*np.sign(d.r30)), "z")
    out["overall slope check"] = clus_slope(d)
    return out
