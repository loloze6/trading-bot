def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float)
            ratio = (v.rolling(14).mean() / v.rolling(30).mean() - 1).values
            sma = pd.Series(c).rolling(50).mean().values
            ret20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (7, 14, 28):
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     yr=yr[i], fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                     ratio=ratio[i], dist=c[i]/sma[i]-1 if not np.isnan(sma[i]) else np.nan,
                                     ret20=ret20[i], r=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["r"] - df.groupby(["coin", "h"])["r"].transform("mean")

    def clus(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 30: return (np.nan, np.nan, len(d))
        X = np.column_stack([np.ones(len(d)), d[x].values]); y = d["ex"].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ y; e = y - X @ beta
        g = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(g); V = XtX @ (g.T @ g) @ XtX * G/(G-1)*(len(d)-1)/(len(d)-2)
        return (beta[1], beta[1]/np.sqrt(V[1, 1]), len(d))

    def dayt(d):
        s = d.groupby("day")["ex"].sum(); n = len(d)
        m = d["ex"].mean(); se = np.sqrt(((d.groupby("day")["ex"].apply(lambda z: (z - m).sum()))**2).sum())/n
        return m, m/se, n

    out = {}
    T = df[df.reg == "trending"]
    res = {}
    for h in (7, 14, 28):
        t = T[T.h == h]
        res[f"h{h}_fc"] = clus(t, "fc")
        res[f"h{h}_ratio"] = clus(t, "ratio")
        res[f"h{h}_dist"] = clus(t, "dist")
        res[f"h{h}_ret20"] = clus(t, "ret20")
        res[f"h{h}_fc>0 mean"] = dayt(t[t.fc > 0])
        res[f"h{h}_fc=0 mean"] = dayt(t[t.fc == 0])
        res[f"h{h}_nontrend mean"] = dayt(df[(df.h == h) & (df.reg != "trending")])
    out["slopes (beta,t,n)"] = pd.DataFrame(res, index=["coef", "t", "n"]).T
    t14 = T[T.h == 14].copy()
    t14["fbin"] = pd.cut(t14.fc, [-0.1, 0, 0.5, 1, 1.5, 2, 30])
    out["h14 by fc bin"] = t14.groupby("fbin")["ex"].agg(["mean", "count", "median"])
    t14p = t14.dropna(subset=["dist"]).copy()
    t14p["dbin"] = pd.qcut(t14p.dist, 5)
    out["h14 by dist quint"] = t14p.groupby("dbin")["ex"].agg(["mean", "count"])
    out["h14 by year"] = t14.groupby("yr").apply(lambda d: pd.Series(dict(n=len(d), mean=d.ex.mean(), slope_t=clus(d, "fc")[1])))
    out["h14 by coin"] = t14.groupby("coin").apply(lambda d: pd.Series(dict(n=len(d), mean=d.ex.mean(), npos=(d.fc>0).sum(), mpos=d[d.fc>0].ex.mean(), m0=d[d.fc==0].ex.mean())))
    return out
