def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            z5 = (c / c.shift(5) - 1) / (vol20 * np.sqrt(5))
            z1 = r1 / vol20
            rng = (hi - lo) / c.shift(1)
            rngz = rng / rng.rolling(20, min_periods=15).mean()
            lowext = (c - lo) / (hi - lo).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                              "fwd": c.shift(-H) / c - 1, "z5": z5, "z1": z1, "rngz": rngz,
                              "clv": lowext, "yr": ts.dt.year,
                              "fc": b["forecast"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].dropna(subset=["rngz", "z1", "z5"]).copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    def dayt(g, col="ex"):
        s = g.groupby("day")[col].sum()
        return pd.Series({"n": g[col].count(), "days": len(s), "mean_%": 100 * g[col].mean(),
                          "t_day": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    D = G[G["z1"] < 0].copy()
    # graded: excess range on down days
    D["xr"] = np.log(D["rngz"])
    def slope(g):
        s = stats.linregress(g["xr"], g["ex"])
        return pd.Series({"n": len(g), "slope_%": 100 * s.slope, "t": s.slope / s.stderr})
    out["down_logrange_slope_all"] = slope(D).to_frame().T
    out["down_logrange_slope_by_coin"] = D.groupby("coin").apply(slope)
    out["down_logrange_slope_by_yr"] = D.groupby("yr").apply(slope)
    U = G[G["z1"] >= 0].copy(); U["xr"] = np.log(U["rngz"])
    out["up_logrange_slope_all"] = slope(U).to_frame().T
    # wide down days: by z5 sign and by close location
    W = D[D["rngz"] > D["rngz"].quantile(0.6)].copy()
    out["wide_down_by_z5sign"] = W.groupby(np.where(W["z5"] < 0, "fell_5d", "rose_5d")).apply(dayt)
    out["wide_down_by_closeloc"] = W.groupby(pd.cut(W["clv"], [0, .33, .66, 1.0001])).apply(dayt)
    out["wide_down_by_coin"] = W.groupby("coin").apply(dayt)
    # multivariate with z5 and forecast
    X = np.column_stack([np.ones(len(D)), D["xr"], D["z5"]])
    beta, *_ = np.linalg.lstsq(X, D["ex"].values, rcond=None)
    res = D["ex"].values - X @ beta
    s2 = res @ res / (len(D) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["down_ols_logrange_z5"] = pd.DataFrame({"beta_%": 100 * beta, "t": beta / se}, index=["c", "logrange", "z5"])
    return out
