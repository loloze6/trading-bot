def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        allr = [pd.Series(b["close"].astype(float).values).pct_change().dropna() for b in ws.values()]
        drift[coin] = pd.concat(allr).mean()
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float)
            rng = h - l
            cl = (c - l) / rng.replace(0, np.nan)
            r = c.pct_change()
            sd = r.rolling(20).std()
            wide = (rng / c) / sd
            active = b["regime"] != "chop"
            for H in [1, 2]:
                fwd = c.shift(-H) / c - 1
                for i in range(len(b)):
                    if i % H != 0 or np.isnan(fwd.iloc[i]) or not active.iloc[i]:
                        continue
                    rows.append(dict(coin=coin, w=w, H=H, day=str(b["timestamp"].iloc[i])[:10],
                                     year=pd.to_datetime(b["timestamp"].iloc[i]).year,
                                     cl=cl.iloc[i], wide=wide.iloc[i], dayret=r.iloc[i],
                                     body=(c.iloc[i] - o.iloc[i]) / c.iloc[i],
                                     ex=fwd.iloc[i] - drift[coin] * H))
    d = pd.DataFrame(rows).dropna(subset=["cl", "ex"])
    out = {}
    def cl_t(g):
        s = g.groupby("day")["ex"].sum()
        nd = len(s); n = len(g)
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series(dict(n=n, days=nd, mean_ex=m, t_clust=m / se if se > 0 else np.nan))
    d1 = d[d.H == 1].copy()
    d1["upper"] = d1["cl"] > 0.5
    out["H1 upper vs lower half (clustered t)"] = d1.groupby("upper").apply(cl_t)
    u = d1[d1.upper]
    sl = stats.linregress(u["cl"], u["ex"])
    out["H1 upper half: slope of ex on cl"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(u)))
    sl2 = stats.linregress(d1["cl"], d1["ex"])
    out["H1 all active: slope of ex on cl"] = pd.Series(dict(slope=sl2.slope, t=sl2.slope / sl2.stderr, n=len(d1)))
    d1["cl3"] = pd.cut(d1["cl"], [-0.01, 0.33, 0.67, 1.01])
    out["H1 cl thirds by year"] = d1.groupby(["cl3", "year"]).apply(cl_t)
    out["H1 top third by coin"] = d1[d1.cl > 0.67].groupby("coin").apply(cl_t)
    out["H1 bottom third by coin"] = d1[d1.cl <= 0.33].groupby("coin").apply(cl_t)
    d1["wide2"] = pd.qcut(d1["wide"], 2, labels=["less", "more"])
    out["H1 cl thirds x wide halves"] = d1.groupby(["cl3", "wide2"]).apply(cl_t)
    d1["upday"] = d1["dayret"] > 0
    out["H1 cl thirds x day up/down"] = d1.groupby(["cl3", "upday"]).apply(cl_t)
    d2 = d[d.H == 2].copy()
    d2["cl3"] = pd.cut(d2["cl"], [-0.01, 0.33, 0.67, 1.01])
    out["H2 cl thirds"] = d2.groupby("cl3").apply(cl_t)
    return out
