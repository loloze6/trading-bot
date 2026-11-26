def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            rng = (b["high"]-b["low"]).astype(float)/c
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "fwd1": c.shift(-1)/c-1, "fwd2": c.shift(-2)/c-1, "fwd4": c.shift(-4)/c-1,
                "r1": r1,
                "volz": v/v.rolling(20).mean(),
                "volz7": v.rolling(7).mean()/v.rolling(60, min_periods=40).mean(),
                "rngz": rng/rng.rolling(20).mean(),
                "clv": ((c-b["low"])/(b["high"]-b["low"])).astype(float),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["lvolz"] = np.log(A["volz"].replace(0, np.nan))
    A["lvolz7"] = np.log(A["volz7"].replace(0, np.nan))
    out = {}
    def cl_slope(df, x, y, h):
        g = df[df.pos % h == 0].copy()
        g["ex"] = g[y] - g.groupby("coin")[y].transform("mean")
        d = g[["day", x, "ex"]].replace([np.inf,-np.inf], np.nan).dropna()
        z = (d[x]-d[x].mean())/d[x].std()
        X = np.column_stack([np.ones(len(d)), z.values]); Y = d["ex"].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X@beta
        XtXi = np.linalg.inv(X.T@X)
        S = pd.DataFrame(X*e[:,None]).groupby(d["day"].values).sum().values
        V = XtXi@(S.T@S)@XtXi
        return pd.Series({"slope_per_sd": beta[1], "t_dayclust": beta[1]/np.sqrt(V[1,1]), "n": len(d), "days": d["day"].nunique()})
    res = {}
    for x in ["lvolz","rngz","lvolz7","clv"]:
        for y,h in [("fwd1",1),("fwd2",2),("fwd4",4)]:
            res[x+"_"+y] = cl_slope(A, x, y, h)
    out["clustered_slopes"] = pd.DataFrame(res).T
    # volz split by sign of day's return
    A["up"] = np.where(A["r1"]>0, "up", "down")
    out["lvolz_fwd2_by_daysign"] = pd.DataFrame({s: cl_slope(A[A.up==s], "lvolz", "fwd2", 2) for s in ["up","down"]}).T
    # signed: volume-weighted direction (r1 sign * volz) -> fwd2 in dir of day
    A["sgnvol"] = np.sign(A["r1"])*A["lvolz"]
    out["signed_dayret_x_lvolz_fwd2"] = cl_slope(A, "sgnvol", "fwd2", 2)
    # by coin and by year
    out["lvolz_fwd2_by_coin"] = pd.DataFrame({c: cl_slope(A[A.coin==c], "lvolz", "fwd2", 2) for c in A.coin.unique()}).T
    out["lvolz_fwd2_by_year"] = pd.DataFrame({y: cl_slope(A[A.yr==y], "lvolz", "fwd2", 2) for y in sorted(A.yr.unique())}).T
    # quintiles volz -> fwd2 excess, with position held
    g = A[A.pos % 2 == 0].copy()
    g["ex"] = g["fwd2"] - g.groupby("coin")["fwd2"].transform("mean")
    d = g.dropna(subset=["lvolz","ex"])
    d["q"] = pd.qcut(d["lvolz"].rank(method="first"), 5, labels=False)
    out["q_lvolz_fwd2"] = d.groupby("q").agg(ex=("ex","mean"), n=("ex","size"), r1=("r1","mean"), alloc=("alloc","mean"), absalloc=("alloc", lambda s: s.abs().mean()))
    # does volume add over the idea's forecast? regress ex on fc and lvolz
    dd = d.dropna(subset=["fc"])
    X = np.column_stack([np.ones(len(dd)), dd["fc"], (dd["lvolz"]-dd["lvolz"].mean())/dd["lvolz"].std()])
    b, *_ = np.linalg.lstsq(X, dd["ex"].values, rcond=None)
    e = dd["ex"].values - X@b; s2 = e@e/(len(dd)-3); se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["multi_fc_lvolz"] = pd.Series({"b_fc": b[1], "t_fc": b[1]/se[1], "b_lvolz": b[2], "t_lvolz": b[2]/se[2]})
    out["corr_fc_lvolz"] = dd[["fc","lvolz","r1"]].corr()
    return out
