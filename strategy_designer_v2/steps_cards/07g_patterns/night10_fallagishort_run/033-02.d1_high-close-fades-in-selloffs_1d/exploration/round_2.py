def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []; drift = {}
    for coin, wins in data["bars"].items():
        allr = [b["close"].values[1:]/b["close"].values[:-1]-1 for b in wins.values()]
        drift[coin] = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            r = c.pct_change()
            v20 = r.rolling(20, min_periods=10).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] == "unknown").astype(int),
                "cl": (c-l)/(h-l).replace(0, np.nan), "r0z": r/v20,
                "r7z": (c/c.shift(7)-1)/(v20*np.sqrt(7)),
                "r14z": (c/c.shift(14)-1)/(v20*np.sqrt(14)),
                "f1": c.shift(-1)/c-1, "f2": c.shift(-2)/c-1, "f3": c.shift(-3)/c-1,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True); D["d"] = D["coin"].map(drift)
    P = D[D.inprof == 1].copy()
    for k in [1, 2, 3]:
        P["s%d" % k] = -(P["f%d" % k] - k*P["d"])
    out = {}
    def clust(g, f, s):
        # graded slope-ish: mean of s weighted by rank-centred feature, day-clustered t
        g = g[[f, s, "day"]].dropna().copy()
        z = (g[f].rank() / len(g)) - 0.5
        g["x"] = z * g[s]
        dd = g.groupby("day")["x"].sum()
        t = dd.mean()/(dd.std()/np.sqrt(len(dd)))
        return len(g), len(dd), t
    res = {}
    for k in [1, 2, 3]:
        G = P[P.pos % k == 0]
        for f in ["r0z", "r7z", "r14z", "cl"]:
            n, nd, t = clust(G, f, "s%d" % k)
            res[(k, f)] = {"n": n, "days": nd, "t_clust": t}
    out["graded_clustered"] = pd.DataFrame(res).T
    # r7z h3 by coin and year, top half minus bottom half
    G = P[P.pos % 3 == 0][["coin", "yr", "r7z", "s3"]].dropna()
    G["hi"] = G.r7z > G.r7z.median()
    def hl(x):
        a, b2 = x[x.hi]["s3"], x[~x.hi]["s3"]
        return pd.Series({"n": len(x), "hi": a.mean(), "lo": b2.mean(), "diff": a.mean()-b2.mean()})
    out["r7z_h3_by_coin"] = G.groupby("coin").apply(hl)
    out["r7z_h3_by_year"] = G.groupby("yr").apply(hl)
    # r0z h1 by coin and year
    G = P[["coin", "yr", "r0z", "s1"]].dropna()
    G["hi"] = G.r0z > G.r0z.median()
    G = G.rename(columns={"s1": "s3"})
    out["r0z_h1_by_coin"] = G.groupby("coin").apply(hl)
    out["r0z_h1_by_year"] = G.groupby("yr").apply(hl)
    # up days only: graded by r0z size, h1 and h2
    U = P[P.r0z > 0][["r0z", "s1", "s2", "day"]].dropna()
    q = pd.qcut(U.r0z.rank(method="first"), 3, labels=False)
    out["updays_r0z_terc"] = pd.DataFrame({"n": U.groupby(q).size(), "s1": U.groupby(q)["s1"].mean(),
                                           "s2": U.groupby(q)["s2"].mean()})
    # up days: cl tercile
    q2 = pd.qcut(P.loc[U.index, "cl"].rank(method="first"), 3, labels=False)
    out["updays_cl_terc"] = pd.DataFrame({"n": U.groupby(q2).size(), "s1": U.groupby(q2)["s1"].mean(),
                                          "s2": U.groupby(q2)["s2"].mean()})
    return out
