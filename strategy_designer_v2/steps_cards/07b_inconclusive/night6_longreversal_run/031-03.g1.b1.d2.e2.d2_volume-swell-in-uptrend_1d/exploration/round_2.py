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
            r14p = pd.Series(c).pct_change(14).values
            h = 14
            for i in range(0, len(b) - h, h):
                rows.append(dict(coin=coin, day=str(b["timestamp"].iloc[i])[:10],
                                 fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                 ratio=ratio[i], dist=c[i]/sma[i]-1 if not np.isnan(sma[i]) else np.nan,
                                 past14=r14p[i], r=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["r"] - df.groupby("coin")["r"].transform("mean")

    def clus(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 30: return (np.nan, np.nan, len(d))
        X = np.column_stack([np.ones(len(d)), d[x].values]); y = d["ex"].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ y; e = y - X @ beta
        g = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(g); V = XtX @ (g.T @ g) @ XtX * G/(G-1)*(len(d)-1)/(len(d)-2)
        return (beta[1], beta[1]/np.sqrt(V[1, 1]), len(d))

    def dayt(d):
        d = d.dropna(subset=["ex"]); n = len(d)
        if n < 10: return (np.nan, np.nan, n)
        m = d["ex"].mean()
        se = np.sqrt((d.groupby("day")["ex"].apply(lambda z: (z - m).sum())**2).sum())/n
        return (m, m/se, n)

    out = {}
    T = df[df.reg == "trending"]
    out["fc quantiles (trending)"] = T.fc.quantile([.1,.25,.5,.6,.75,.9,.95,1.0])
    out["share fc==20"] = float((T.fc >= 19.99).mean())
    res = {}
    res["all bars ratio"] = clus(df, "ratio")
    res["nontrend ratio"] = clus(df[df.reg != "trending"], "ratio")
    res["trend ratio"] = clus(T, "ratio")
    res["trend ratio, ratio>0"] = clus(T[T.ratio > 0], "ratio")
    res["trend fc, fc>0"] = clus(T[T.fc > 0], "fc")
    Td = T.dropna(subset=["dist"])
    q = Td.dist.quantile([1/3, 2/3]).values
    res["trend ratio, dist low"] = clus(Td[Td.dist <= q[0]], "ratio")
    res["trend ratio, dist mid"] = clus(Td[(Td.dist > q[0]) & (Td.dist <= q[1])], "ratio")
    res["trend ratio, dist high"] = clus(Td[Td.dist > q[1]], "ratio")
    res["trend ratio, past14>0"] = clus(T[T.past14 > 0], "ratio")
    res["trend ratio, past14<=0"] = clus(T[T.past14 <= 0], "ratio")
    out["slopes (beta,t,n)"] = pd.DataFrame(res, index=["coef", "t", "n"]).T
    Tr = T.dropna(subset=["ratio"]).copy()
    Tr["rq"] = pd.qcut(Tr.ratio, 5)
    out["trend by ratio quintile"] = Tr.groupby("rq").apply(lambda d: pd.Series(dict(zip(["mean","t","n"], dayt(d)))))
    Ar = df.dropna(subset=["ratio"]).copy()
    Ar["rq"] = pd.qcut(Ar.ratio, 5)
    out["nontrend by ratio quintile"] = Ar[Ar.reg != "trending"].groupby("rq").apply(lambda d: pd.Series(dict(zip(["mean","t","n"], dayt(d)))))
    big = ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]
    res2 = {}
    res2["default6 ratio"] = clus(T[T.coin.isin(big)], "ratio")
    res2["other13 ratio"] = clus(T[~T.coin.isin(big)], "ratio")
    res2["default6 fc>0 mean"] = dayt(T[T.coin.isin(big) & (T.fc > 0)])
    res2["other13 fc>0 mean"] = dayt(T[~T.coin.isin(big) & (T.fc > 0)])
    out["by coin group"] = pd.DataFrame(res2, index=["a", "t", "n"]).T
    return out
