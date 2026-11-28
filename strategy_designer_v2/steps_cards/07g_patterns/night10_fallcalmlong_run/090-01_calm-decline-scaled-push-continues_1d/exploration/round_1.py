def explore(data):
    import numpy as np, pandas as pd
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            f5 = c.shift(-5) / c - 1
            allf.append(f5.iloc[::5].dropna())
        drift[coin] = pd.concat(allf).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]; v = b["volume"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "inprof": (b["regime"] == "unknown").astype(int),
                "fwd5": c.shift(-5) / c - 1 - drift[coin],
                "fwd2": c.shift(-2) / c - 1,
                "s1": r / vol,
                "s5": (c / c.shift(5) - 1) / vol,
                "s20": (c / c.shift(20) - 1) / vol,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "rng": (h - l) / c / vol,
                "body": (c - o) / c / vol,
                "volr": np.log(v / v.rolling(20, min_periods=10).mean()),
                "dd60": (c / c.rolling(60, min_periods=20).max() - 1) / vol,
                "up20": (r > 0).rolling(20, min_periods=10).mean(),
                "volchg": np.log(vol / vol.shift(10)),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df[df["pos"] % 5 == 0])
    D = pd.concat(rows).dropna(subset=["fwd5"])
    P = D[D.inprof == 1]
    out = {}

    def clus_t(x, y, g):
        m = x.notna() & y.notna()
        x, y, g = x[m].values, y[m].values, g[m].values
        if len(x) < 30: return (np.nan, np.nan, len(x))
        xs = (x - x.mean()) / x.std()
        X = np.c_[np.ones(len(xs)), xs]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for gg in np.unique(g):
            i = g == gg
            s = X[i].T @ e[i]
            S += np.outer(s, s)
        V = XtX @ S @ XtX
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(x))

    feats = ["s1", "s5", "s20", "clv", "rng", "body", "volr", "dd60", "up20", "volchg"]
    res = []
    for f in feats:
        b, t, n = clus_t(P[f], P["fwd5"], P["day"])
        b2, t2, n2 = clus_t(D[D.inprof == 0][f], D[D.inprof == 0]["fwd5"], D[D.inprof == 0]["day"])
        res.append([f, b, t, n, b2, t2, n2])
    out["slope per 1sd feature, in-profile vs out"] = pd.DataFrame(res, columns=["feat", "b_in", "t_in", "n_in", "b_out", "t_out", "n_out"])
    q = []
    for f in feats:
        s = P[[f, "fwd5"]].dropna()
        s["q"] = pd.qcut(s[f].rank(method="first"), 5, labels=False)
        g = s.groupby("q")["fwd5"]
        q.append([f] + list(g.mean().round(4)) + [g.count().min()])
    out["in-profile quintile mean fwd5 (minus drift)"] = pd.DataFrame(q, columns=["feat", "q1", "q2", "q3", "q4", "q5", "nmin"])
    g = P.groupby("wd")["fwd5"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["in-profile by weekday"] = g
    g = P.groupby("coin")["fwd5"].agg(["mean", "count"])
    out["in-profile by coin"] = g
    out["in-profile mean fwd5 overall"] = pd.Series({"mean": P.fwd5.mean(), "n": len(P), "t": P.fwd5.mean() / (P.fwd5.std() / np.sqrt(len(P)))})
    return out
