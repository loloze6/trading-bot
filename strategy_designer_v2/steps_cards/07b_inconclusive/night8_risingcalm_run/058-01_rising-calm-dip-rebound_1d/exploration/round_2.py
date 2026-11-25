def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [5, 10]
    coinmean = {}
    for c, ws in bars.items():
        for h in H:
            vals = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    vals.append(cl[i + h] / cl[i] - 1)
            coinmean[(c, h)] = np.mean(vals)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            pb = (cl / cl.shift(3) - 1) / sd
            tr = cl / cl.shift(60) - 1
            vol30 = r.rolling(30, min_periods=20).std()
            n = len(b)
            for i in range(0, n - 5, 5):
                d = {"coin": c, "win": w, "pb": pb.iloc[i], "tr": tr.iloc[i],
                     "inprof": b["regime"].iloc[i] == "unknown",
                     "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(b["timestamp"].iloc[i]).normalize()}
                for h in H:
                    if i + h < n:
                        d["x%d" % h] = cl.iloc[i + h] / cl.iloc[i] - 1 - coinmean[(c, h)]
                rows.append(d)
    df = pd.DataFrame(rows)
    dip = df[df.pb < 0].copy()
    dip["depth"] = -dip["pb"]
    def cl_t(s, y):
        s = s.dropna(subset=["depth", y])
        if len(s) < 10: return (len(s), np.nan, np.nan, np.nan)
        x = s["depth"].values; yy = s[y].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, yy, rcond=None)[0]
        e = yy - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        g = s["day"].values
        for gg in np.unique(g):
            m = g == gg
            u = X[m].T @ e[m]
            meat += np.outer(u, u)
        G = len(np.unique(g)); N = len(x)
        V = XtXi @ meat @ XtXi * G / (G - 1) * (N - 1) / (N - 2)
        return (N, beta[1], beta[1] / np.sqrt(V[1, 1]), G)
    out = {}
    sets = {"rc": dip[dip.inprof], "falling": dip[dip.tr < -0.10],
            "rising_agit": dip[(~dip.inprof) & (dip.tr > 0.10)]}
    tab = []
    for k, s in sets.items():
        for h in H:
            n, sl, t, G = cl_t(s, "x%d" % h)
            tab.append({"set": k, "h": h, "n": n, "slope": sl, "t_clust": t, "days": G})
        for yr, sy in s.groupby("year"):
            n, sl, t, G = cl_t(sy, "x5")
            tab.append({"set": k + "_" + str(yr), "h": 5, "n": n, "slope": sl, "t_clust": t, "days": G})
    out["clustered"] = pd.DataFrame(tab)
    fa = sets["falling"].copy()
    fa["q"] = pd.qcut(fa["depth"], 4, labels=False)
    out["falling_quartiles"] = fa.groupby("q").agg(n=("x5", "size"), depth=("depth", "mean"),
                                                   x5=("x5", "mean"), x10=("x10", "mean"))
    out["falling_by_coin"] = fa.groupby("coin").agg(n=("x5", "size"), x5=("x5", "mean"),
        corr=("x5", lambda v: np.corrcoef(fa.loc[v.index, "depth"], v)[0, 1]))
    return out
