def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        drift[coin] = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]; v = b["volume"]
            r = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "inprof": (b["regime"] == "unknown").astype(int),
                "cl": (c - l) / (h - l).replace(0, np.nan),
                "r0": r,
                "r3": c / c.shift(3) - 1,
                "r7": c / c.shift(7) - 1,
                "rng": (h - l) / c,
                "body": (c - o) / (h - l).replace(0, np.nan),
                "vol20": r.rolling(20, min_periods=10).std(),
                "vrat": v / v.rolling(20, min_periods=10).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
            })
            df["rngz"] = df["rng"] / df["vol20"]
            df["r0z"] = df["r0"] / df["vol20"]
            df["r3z"] = df["r3"] / (df["vol20"] * np.sqrt(3))
            df["r7z"] = df["r7"] / (df["vol20"] * np.sqrt(7))
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            df["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["d"] = D["coin"].map(drift)
    out = {}
    P = D[D.inprof == 1].copy()
    out["counts"] = pd.Series({"all_bars": len(D), "inprof_bars": len(P),
                               "inprof_share": len(P)/len(D)})
    out["inprof_by_coin"] = P.groupby("coin").size()
    for h in [1, 2, 3]:
        P["s%d" % h] = -(P["f%d" % h] - h * P["d"])   # short-direction excess
    feats = ["cl", "r0z", "r3z", "r7z", "rngz", "body", "vrat"]
    res = {}
    for h in [1, 2, 3]:
        G = P[P.pos % h == 0]
        for f in feats:
            g = G[[f, "s%d" % h, "day"]].dropna()
            if len(g) < 50: continue
            q = pd.qcut(g[f].rank(method="first"), 5, labels=False)
            m = g.groupby(q)["s%d" % h].mean()
            top, bot = g[q == 4]["s%d" % h], g[q == 0]["s%d" % h]
            t = stats.ttest_ind(top, bot, equal_var=False).statistic
            rho = stats.spearmanr(g[f], g["s%d" % h]).correlation
            res[(h, f)] = {"n": len(g), "q1": m.iloc[0], "q2": m.iloc[1], "q3": m.iloc[2],
                           "q4": m.iloc[3], "q5": m.iloc[4], "q5-q1": top.mean()-bot.mean(),
                           "t": t, "rho": rho}
    out["prof_quintiles_short_excess"] = pd.DataFrame(res).T
    # outside profile, same for cl and r0z, h=1
    Q = D[D.inprof == 0].copy()
    Q["s1"] = -(Q["f1"] - Q["d"])
    res2 = {}
    for f in ["cl", "r0z", "r3z", "rngz"]:
        g = Q[[f, "s1"]].dropna()
        q = pd.qcut(g[f].rank(method="first"), 5, labels=False)
        m = g.groupby(q)["s1"].mean()
        t = stats.ttest_ind(g[q == 4]["s1"], g[q == 0]["s1"], equal_var=False).statistic
        res2[f] = list(m.values) + [t, len(g)]
    out["outprof_h1_quint_t_n"] = pd.DataFrame(res2, index=["q1","q2","q3","q4","q5","t","n"]).T
    # mean short excess in profile overall, by weekday, by coin, by year
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(),
                                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["prof_s1_by_wd"] = P.groupby("wd")["s1"].apply(tt).unstack()
    out["prof_s1_by_coin"] = P.groupby("coin")["s1"].apply(tt).unstack()
    out["prof_s1_by_year"] = P.groupby("yr")["s1"].apply(tt).unstack()
    G3 = P[P.pos % 3 == 0]
    out["prof_s3_all"] = tt(G3["s3"])
    out["prof_s1_all"] = tt(P["s1"])
    # interaction: cl high AND r0 up (bounce close near high) vs cl high with r0 down
    g = P[["cl", "r0z", "s1", "s2"]].dropna()
    g["clh"] = (g.cl > g.cl.median()).astype(int)
    g["up"] = (g.r0z > 0).astype(int)
    out["cl_x_dayup_s1"] = g.groupby(["clh", "up"])["s1"].apply(tt).unstack()
    out["cl_x_dayup_s2"] = g.groupby(["clh", "up"])["s2"].apply(tt).unstack()
    return out
