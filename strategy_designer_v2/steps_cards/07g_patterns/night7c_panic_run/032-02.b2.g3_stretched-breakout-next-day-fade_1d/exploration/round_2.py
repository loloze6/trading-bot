def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["fwd1"] = c.shift(-1)/c - 1
            d["fwd2"] = c.shift(-2)/c - 1
            d["r30"] = c/c.shift(30) - 1
            d["volratio"] = r1.rolling(5).std()/r1.rolling(60).std()
            d["clv"] = (c - l)/(h - l).replace(0, np.nan)
            d["z1"] = r1/r1.shift(1).rolling(60).std()
            rng = (h - l)/c
            d["rngz"] = rng/rng.shift(1).rolling(30).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in (1,2):
        dr = D.loc[D.pos % k == 0].groupby("coin")[f"fwd{k}"].mean()
        D[f"ex{k}"] = D[f"fwd{k}"] - D["coin"].map(dr)
    D["volfall"] = (D.r30 < 0) & (D.volratio > D.groupby("coin").volratio.transform("median"))
    D["calm_or_up"] = ~D["volfall"]
    def cl_t(X, xcols, y):
        X = X.dropna(subset=xcols+[y])
        A = np.column_stack([np.ones(len(X))] + [X[c].values for c in xcols])
        Y = X[y].values
        beta, *_ = np.linalg.lstsq(A, Y, rcond=None)
        e = Y - A@beta
        AtA = np.linalg.inv(A.T@A)
        g = pd.DataFrame(A*e[:,None]).groupby(X["day"].values).sum().values
        G = len(g); n, p = A.shape
        V = AtA@(g.T@g)@AtA * G/(G-1)*(n-1)/(n-p)
        return pd.Series(beta[1:]/np.sqrt(np.diag(V))[1:], index=xcols), G
    out = {}
    res = {}
    for name, sub in [("all", D), ("volfall", D[D.volfall]), ("other", D[D.calm_or_up])]:
        for xs in (["z1"], ["clv"], ["z1","clv"], ["rngz"], ["z1","rngz"]):
            t, G = cl_t(sub, xs, "ex1")
            for c in xs:
                res[(name, "+".join(xs), c)] = {"t_day_clustered": t[c], "days": G}
    out["cluster_t_h1"] = pd.DataFrame(res).T
    # by coin and year: slope t of z1 on ex1, all bars and volfall
    r = {}
    for coin, g in D.groupby("coin"):
        g = g.dropna(subset=["z1","ex1"])
        s = stats.linregress(g.z1, g.ex1); r[(coin,"all")] = s.slope/s.stderr
        gv = g[g.volfall]; s = stats.linregress(gv.z1, gv.ex1); r[(coin,"volfall")] = s.slope/s.stderr
    for y, g in D.groupby("year"):
        g = g.dropna(subset=["z1","ex1"])
        s = stats.linregress(g.z1, g.ex1); r[(y,"all")] = s.slope/s.stderr
        gv = g[g.volfall]; s = stats.linregress(gv.z1, gv.ex1); r[(y,"volfall")] = s.slope/s.stderr
    out["z1_slope_t_by_coin_year"] = pd.Series(r).unstack()
    # graded: z1 deciles in volfall (sign-fixed: next day excess)
    X = D[D.volfall].dropna(subset=["z1","ex1"]).copy()
    X["b"] = pd.cut(X.z1, [-99,-2,-1,-0.5,0,0.5,1,2,99])
    g = X.groupby("b", observed=True)["ex1"]
    out["volfall_z1_bins_h1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    X = D[D.calm_or_up].dropna(subset=["z1","ex1"]).copy()
    X["b"] = pd.cut(X.z1, [-99,-2,-1,-0.5,0,0.5,1,2,99])
    g = X.groupby("b", observed=True)["ex1"]
    out["other_z1_bins_h1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    # h2 non-overlapping in volfall
    X2 = D[(D.pos % 2 == 0) & D.volfall]
    t2, G2 = cl_t(X2, ["z1"], "ex2")
    out["volfall_z1_h2_t"] = pd.Series({"t": t2["z1"], "days": G2, "n": len(X2.dropna(subset=["z1","ex2"]))})
    # magnitude: mean |z1| reversal size per case, top/bottom 20% within volfall, sign = -sign(z1)
    X = D[D.volfall].dropna(subset=["z1","ex1"]).copy()
    X["sig"] = -np.sign(X.z1)*X.ex1
    q = X.z1.abs() > X.z1.abs().quantile(0.6)
    out["volfall_fade_size"] = pd.Series({"mean_signed%": X.loc[q,"sig"].mean()*100,
        "t": X.loc[q,"sig"].mean()/(X.loc[q,"sig"].std()/np.sqrt(q.sum())), "n": q.sum(),
        "usual_move%": D.ex1.std()*100})
    return out
