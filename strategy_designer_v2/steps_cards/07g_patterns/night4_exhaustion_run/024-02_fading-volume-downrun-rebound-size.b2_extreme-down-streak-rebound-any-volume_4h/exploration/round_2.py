def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    allr = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(180, min_periods=45).std()
            past6 = c / c.shift(6) - 1
            past18 = c / c.shift(18) - 1
            volr = v.rolling(6).mean() / v.rolling(180, min_periods=45).mean()
            vol18 = v.rolling(18).mean() / v.rolling(180, min_periods=45).mean()
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "fwd6": fwd6,
                "z6": past6 / (sd * np.sqrt(6)), "z18": past18 / (sd * np.sqrt(18)),
                "volr": volr, "vol18": vol18, "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(len(b))})
            recs.append(df)
        d = pd.concat(recs).dropna(subset=["fwd"])
        g0 = d[d["pos"] % H == 0]
        drift = g0["fwd"].mean(); usual = g0["fwd"].std()
        d["u"] = (d["fwd"] - drift) / usual
        allr.append(d)
    A = pd.concat(allr)
    out = {}
    def slope(x, col):
        x = x.dropna(subset=[col, "u"])
        r = stats.linregress(x[col], x["u"]); return r.slope, r.slope / r.stderr, len(x)
    # robustness across grid offsets
    rows = []
    for off in [0, 3, 6, 9, 12, 15]:
        G = A[A["pos"] % H == off]
        s1 = slope(G, "z18"); s2 = slope(G, "volr"); s3 = slope(G, "z6")
        top = G[G["z18"] > G["z18"].quantile(0.8)]["u"]
        sun = G[G["wd"] == 6]["u"]
        rows.append([off, s1[0], s1[1], s2[0], s2[1], s3[0], s3[1], top.mean(), top.mean()/(top.std()/np.sqrt(len(top))), sun.mean(), sun.mean()/(sun.std()/np.sqrt(len(sun))), len(sun)])
    out["by grid offset"] = pd.DataFrame(rows, columns=["off","b_z18","t_z18","b_volr","t_volr","b_z6","t_z6","topz18_u","topz18_t","sun_u","sun_t","sun_n"]).round(4)
    G = A[A["pos"] % H == 0].copy()
    # z18 top quintile by year and by coin
    q = G["z18"].quantile(0.8)
    T = G[G["z18"] > q]
    def grp(x, col):
        o = x.groupby(col)["u"].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"])); return o[["mean","t","count"]].round(4)
    out["top z18 by year"] = grp(T, "year")
    out["top z18 by coin"] = grp(T, "coin")
    # volume x direction 2x3
    G["dir"] = np.where(G["z18"] > 0, "up", "down")
    G["vq"] = pd.qcut(G["vol18"].rank(method="first"), 3, labels=["lowV","midV","highV"])
    o = G.dropna(subset=["vol18","z18"]).groupby(["dir","vq"])["u"].agg(["mean","count","std"])
    o["t"] = o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["dir x vol18 tercile"] = o[["mean","t","count"]].round(4)
    # z18 quintiles within up moves graded
    U = G[G["z18"] > 0].dropna(subset=["z18"])
    gq = pd.qcut(U["z18"].rank(method="first"), 4, labels=False)
    o = U.groupby(gq)["u"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); o["x"]=U.groupby(gq)["z18"].mean()
    out["up z18 quartiles"] = o.round(4)
    # multiple regression
    X = G.dropna(subset=["z18","z6","volr","u"])
    M = np.column_stack([np.ones(len(X)), X["z18"], X["z6"], np.log(X["volr"])])
    beta, *_ = np.linalg.lstsq(M, X["u"].values, rcond=None)
    res = X["u"].values - M @ beta
    se = np.sqrt(np.diag(np.linalg.inv(M.T @ M)) * res.var(ddof=4))
    out["joint regression"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["c","z18","z6","logvolr"]).round(4)
    return out
