def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"]), "coin": coin, "win": w})
            d["r1"] = c / c.shift(1) - 1
            d["r5"] = c / c.shift(5) - 1
            d["r20"] = c / c.shift(20) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["rng"] = (b["high"] - b["low"]) / c
            d["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["prof"] = (b["regime"] == "unknown").values
            d["pos"] = b["postRebalance_current_allocation"].astype(float).values
            d["grid3"] = (np.arange(len(b)) % 3 == 0)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].mean(); mu3 = D[D.grid3].groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu1)
    D["x3"] = D["f3"] - D["coin"].map(mu3)
    D["day"] = D["ts"].dt.floor("D")

    def ct(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean(); g = (s - m).groupby(dd).sum()
        se = np.sqrt((g**2).sum()) / len(s)
        return m, m / se if se > 0 else np.nan, len(s), dd.nunique()

    def tab(sub, by, col="x1"):
        out = []
        for k, g in sub.groupby(by, observed=True):
            m, t, n, nd = ct(g[col], g["day"])
            out.append({"grp": str(k), "mean%": m*100, "t": t, "n": n, "days": nd})
        return pd.DataFrame(out)

    def reg(sub, xs, y="x1"):
        s = sub.dropna(subset=xs+[y])
        X = np.column_stack([np.ones(len(s))] + [((s[x]-s[x].mean())/s[x].std()).values for x in xs])
        Y = s[y].values
        bt = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ bt
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((X.shape[1],)*2)
        for _, idx in s.groupby("day").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return pd.DataFrame({"coef%_per_sd": bt*100, "t": bt/se}, index=["const"]+xs)

    res = {}
    P = D[D.prof]; N = D[~D.prof]
    res["share profile"] = float(D.prof.mean())
    res["prof r5<0 quintiles"] = tab(P[P.r5<0], pd.qcut(P[P.r5<0].r5, 5))
    res["nonprof r5<0 quintiles"] = tab(N[N.r5<0], pd.qcut(N[N.r5<0].r5, 5))
    res["prof all r5 quintiles"] = tab(P, pd.qcut(P.r5, 5))
    res["prof reg r5 r1 (r5<0)"] = reg(P[P.r5<0], ["r5", "r1"])
    res["prof reg r5 r1 r20 all"] = reg(P, ["r5", "r1", "r20"])
    res["nonprof reg r5 r1 r20 all"] = reg(N, ["r5", "r1", "r20"])
    res["all r1 quintiles x vol tercile"] = tab(D, [pd.qcut(D.r1, 5, labels=False), pd.qcut(D.vol20, 3, labels=False)])
    res["all clpos quintiles"] = tab(D, pd.qcut(D.clpos, 5, labels=False))
    res["all weekday"] = tab(D, D.ts.dt.dayofweek)
    res["prof weekday"] = tab(P, P.ts.dt.dayofweek)
    G = D[D.grid3]
    res["grid3 r20 quintiles"] = tab(G, pd.qcut(G.r20, 5, labels=False), "x3")
    res["grid3 prof r5 quintiles"] = tab(G[G.prof], pd.qcut(G[G.prof].r5, 5, labels=False), "x3")
    res["by year prof r5<0 slope"] = pd.DataFrame({str(y): reg(g, ["r5"]).loc["r5"] for y, g in P[P.r5<0].groupby(P.ts.dt.year) if len(g) > 50}).T
    return res
