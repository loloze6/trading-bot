def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            hh = h.rolling(20).max(); ll = l.rolling(20).min()
            df["pos"] = (c - ll) / (hh - ll) * 2 - 1
            r1 = c.pct_change()
            df["r60"] = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            df["vol20"] = vol20
            df["r1z"] = r1 / vol20.shift(1)
            df["f5"] = c.shift(-5) / c - 1
            df["grid5"] = (np.arange(len(df)) % 5 == 0)
            df["inprof"] = (df["regime"] == "unknown").astype(int)
            df["coin"] = coin; df["win"] = w
            ts = pd.to_datetime(df["timestamp"]); df["dkey"] = ts.dt.floor("D"); df["year"] = ts.dt.year
            df["alloc"] = df["postRebalance_current_allocation"].astype(float)
            rows.append(df[["coin","win","pos","r60","vol20","r1z","f5","grid5","inprof","dkey","year","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    g = A[A.grid5 & A.f5.notna()]
    A["u5"] = A.f5 - A.coin.map(g.groupby("coin").f5.mean())
    def ctslope(d, x, y="u5"):
        d = d[[x, y, "dkey"]].dropna()
        if len(d) < 30: return (np.nan, np.nan, len(d), 0)
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((2,2))
        for _, idx in d.groupby("dkey").indices.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        G = d.dkey.nunique(); n = len(d)
        V = XtXi @ meat @ XtXi * G/(G-1) * (n-1)/(n-2)
        return (round(b[1],4), round(b[1]/np.sqrt(V[1,1]),2), n, G)
    G5 = A[A.grid5 & A.u5.notna()].copy()
    G5["trend"] = pd.cut(G5.r60, [-10,-0.1,0.1,10], labels=["falling","choppy","rising"])
    G5["volq"] = G5.groupby("coin").vol20.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = {}
    out = {}
    for k, d in G5.groupby("volq"): out[f"vol{k}"] = ctslope(d, "pos")
    for (t, v), d in G5.groupby(["trend","volq"]): out[f"{t} vol{v}"] = ctslope(d, "pos")
    ch = G5[G5.trend=="choppy"]
    out["choppy inprof"] = ctslope(ch[ch.inprof==1], "pos")
    out["choppy outprof"] = ctslope(ch[ch.inprof==0], "pos")
    out["inprof all"] = ctslope(G5[G5.inprof==1], "pos")
    res["pos slope groups (slope,t_cl,n,days)"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    out = {}
    G5["up"] = G5.r1z.clip(lower=0)
    for k, d in G5.groupby("volq"): out[f"up vol{k}"] = ctslope(d, "up")
    for k, d in G5.groupby("trend"): out[f"up {k}"] = ctslope(d, "up")
    res["up-day z slope groups"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    G5["posq"] = pd.cut(G5.pos, [-1.01,-0.6,-0.2,0.2,0.6,1.01])
    lv = G5[G5.volq==0]
    res["low-vol tercile pos bins u5"] = lv.groupby("posq").u5.agg(["mean","count"]).round(4)
    out = {}
    for y, d in lv.groupby("year"): out[y] = ctslope(d, "pos")
    res["low-vol pos slope by year"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    res["low-vol share of in-profile grid bars"] = round(float((G5[G5.inprof==1].volq==0).mean()),3)
    return res
