def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g.extend(list(c[idx + 2] / c[idx] - 1))
        dr = np.mean(g)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            h = df["high"]
            n = len(c)
            r14 = pd.Series(c).pct_change(14).values
            r7 = pd.Series(c).pct_change(7).values
            hi = h.rolling(365, min_periods=180).max().values
            prox = c / hi
            r2 = np.full(n, np.nan); r2[:-2] = c[2:] / c[:-2] - 1
            for i in range(n):
                if np.isnan(r2[i]) or np.isnan(r14[i]):
                    continue
                rows.append(dict(coin=coin, wd=ts[i].weekday(), year=ts[i].year, day=ts[i].normalize(),
                                 r14=r14[i], r7=r7[i], prox=prox[i], ex=r2[i] - dr))
    d = pd.DataFrame(rows)

    def cslope(sub, x):
        sub = sub.dropna(subset=[x, "ex"])
        X = sub[x].values; Y = sub["ex"].values
        xm = X - X.mean(); b = (xm * Y).sum() / (xm ** 2).sum()
        res = Y - Y.mean() - b * xm
        s = pd.Series(xm * res).groupby(sub["day"].values).sum().values
        G = len(s)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / (xm ** 2).sum()
        return pd.Series(dict(slope=b, t=b / se, n=len(sub), days=G))

    out = {}
    out["slope ex on r14 by weekday (clustered)"] = d.groupby("wd").apply(lambda s: cslope(s, "r14"))
    out["slope ex on r7 by weekday (clustered)"] = d.groupby("wd").apply(lambda s: cslope(s, "r7"))
    fr = d[d.wd == 4]
    up = fr[fr.r14 > 0]
    out["Fri up: slope on prox (clustered)"] = cslope(up, "prox")
    out["Fri all: slope on prox (clustered)"] = cslope(fr, "prox")
    out["Fri all: slope on r14 (clustered)"] = cslope(fr, "r14")
    out["Fri up: slope on r14 (clustered)"] = cslope(up, "r14")
    out["Fri all: slope r14 by coin"] = fr.groupby("coin").apply(lambda s: cslope(s, "r14"))
    out["Fri all: slope r14 by year"] = fr.groupby("year").apply(lambda s: cslope(s, "r14"))
    nf = d[(d.wd != 4)]
    out["non-Fri all: slope on r14"] = cslope(nf, "r14")
    return out
