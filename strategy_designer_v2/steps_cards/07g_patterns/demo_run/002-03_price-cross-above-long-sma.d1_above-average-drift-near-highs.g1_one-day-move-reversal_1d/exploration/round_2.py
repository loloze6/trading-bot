def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=10).std()
            sd60 = r1.rolling(60, min_periods=30).std()
            z = r1 / sd20
            nxt = c.shift(-1) / c - 1
            n3 = c.shift(-3) / c - 1
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(len(b))
            d = pd.DataFrame({"coin": coin, "w": w, "z": z, "nxt": nxt, "n3": n3, "g3": (idx % 3 == 0),
                              "r5z": r5 / (sd20 * np.sqrt(5)), "vol": sd20, "vr": sd20 / sd60,
                              "year": ts.dt.year,
                              "pos": b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    m3 = D[D["g3"]].groupby("coin")["n3"].mean()
    D["ex3"] = D["n3"] - D["coin"].map(m3)
    X = D.dropna(subset=["z", "ex", "vol"]).copy()
    X["vq"] = X.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    def st(g, x="z", y="ex"):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(g[x], g[y]); return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    H = X[X["vq"] == 2]; L = X[X["vq"] == 0]
    out = {}
    out["hivol_slope_by_coin"] = H.groupby("coin").apply(st)
    out["hivol_slope_by_year"] = H.groupby("year").apply(st)
    out["lovol_slope_by_coin"] = L.groupby("coin").apply(st)
    # asymmetry in high vol: falls vs rises
    H2 = H.copy(); H2["zb"] = pd.cut(H2["z"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["hivol_next_by_zbin"] = H2.groupby("zb").agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    # 3-day horizon non-overlapping in high vol
    out["hivol_3d_slope"] = st(H[H["g3"]], "z", "ex3")
    # continuous: slope of ex on z*vol rank interaction
    X["vrk"] = X.groupby("coin")["vol"].rank(pct=True)
    X["zv"] = X["z"] * X["vrk"]
    import numpy.linalg as la
    A = np.column_stack([np.ones(len(X)), X["z"], X["vrk"], X["zv"]])
    beta, *_ = la.lstsq(A, X["ex"].values, rcond=None)
    res = X["ex"].values - A @ beta
    cov = np.linalg.inv(A.T @ A) * res.var(ddof=4)
    out["interaction_z_volrank"] = pd.Series(beta / np.sqrt(np.diag(cov)), index=["c", "z", "vrk", "zxvrk"])
    # vol expansion ratio
    Y = X.dropna(subset=["vr"]).copy()
    Y["vrq"] = pd.qcut(Y["vr"], 3, labels=False)
    out["slope_by_vol_ratio_tercile"] = Y.groupby("vrq").apply(st)
    # 5d momentum by coin top vs rest
    out["r5z_slope_by_coin"] = D.dropna(subset=["r5z", "ex"]).groupby("coin").apply(lambda g: st(g, "r5z", "ex"))
    # book pnl by vol tercile
    X["g"] = X["pos"] * X["nxt"]
    out["book_gain_by_vol_tercile"] = X.groupby("vq").agg(n=("g", "size"), gain=("g", "mean"),
        t=("g", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    return out
