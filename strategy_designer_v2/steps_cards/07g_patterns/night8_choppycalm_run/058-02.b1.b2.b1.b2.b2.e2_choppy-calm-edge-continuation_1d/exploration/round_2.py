def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            hh = h.rolling(20).max(); ll = l.rolling(20).min()
            df["pos"] = (c - ll) / (hh - ll) * 2 - 1
            r1 = c.pct_change()
            df["r1"] = r1
            df["r60"] = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            df["agit"] = (sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True))
            vol20 = r1.rolling(20).std()
            df["r1z"] = r1 / vol20.shift(1)
            df["f5"] = c.shift(-5) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            df["grid5"] = (np.arange(len(df)) % 5 == 0)
            df["coin"] = coin; df["win"] = w
            ts = pd.to_datetime(df["timestamp"]); df["dkey"] = ts.dt.floor("D"); df["year"] = ts.dt.year
            rows.append(df[["coin","win","pos","r1","r60","agit","r1z","f5","f2","grid5","dkey","year"]])
    A = pd.concat(rows, ignore_index=True)
    g = A[A.grid5 & A.f5.notna()]
    A["u5"] = A.f5 - A.coin.map(g.groupby("coin").f5.mean())
    def ctslope(d, x, y="u5"):
        d = d[[x, y, "dkey"]].dropna()
        if len(d) < 30: return (np.nan, np.nan, len(d), 0)
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2,2))
        for _, idx in d.groupby("dkey").indices.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        G = d.dkey.nunique(); n = len(d)
        V = XtXi @ meat @ XtXi * G/(G-1) * (n-1)/(n-2)
        return (round(b[1],4), round(b[1]/np.sqrt(V[1,1]),2), n, G)
    G5 = A[A.grid5 & A.u5.notna()].copy()
    G5["trend"] = pd.cut(G5.r60, [-10,-0.1,0.1,10], labels=["falling","choppy","rising"])
    G5["ag"] = np.where(G5.agit > 0.5, "agitated", "calm"); G5.loc[G5.agit.isna(), "ag"] = "na"
    res = {}
    out = {}
    for (t, a), d in G5.groupby(["trend","ag"]):
        out[f"{t} {a}"] = ctslope(d, "pos")
    res["pos slope by profile (slope, t day-clustered, n, days)"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    out = {}
    for (t, a), d in G5.groupby(["trend","ag"]):
        out[f"{t} {a}"] = ctslope(d, "r1z")
    res["daily z slope -> u5 by profile"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    out = {}
    for y, d in G5.groupby("year"):
        out[y] = ctslope(d, "r1z"); 
    res["daily z slope -> u5 by year"] = pd.DataFrame(out, index=["slope","t","n","days"]).T
    out = {}
    for w, d in G5.groupby("win"):
        out[w] = ctslope(d, "pos")[:3]
    res["pos slope by window"] = pd.DataFrame(out, index=["slope","t","n"]).T
    G5["up"] = G5.r1z.clip(lower=0); G5["dn"] = G5.r1z.clip(upper=0)
    res["up-day z slope (all)"] = str(ctslope(G5, "up"))
    res["down-day z slope (all)"] = str(ctslope(G5, "dn"))
    res["pos slope all"] = str(ctslope(G5, "pos"))
    return res
