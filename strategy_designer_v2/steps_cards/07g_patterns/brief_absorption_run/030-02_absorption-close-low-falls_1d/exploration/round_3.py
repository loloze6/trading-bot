def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            rng = (h - l).replace(0, np.nan)
            cl = (c - l) / rng
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(b["timestamp"])
            fwd = c.shift(-1) / c - 1
            rows.append(pd.DataFrame({"coin": coin, "yr": ts.dt.year.values, "fwd": fwd.values,
                "vr": vr.values, "cl": cl.values, "z1": (r1 / sd20).values,
                "lowtail": ((np.minimum(o, c) - l) / rng).values,
                "uptail": ((h - np.maximum(o, c)) / rng).values,
                "rngsd": (((h - l) / c) / sd20).values}))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "cl", "vr", "z1"])
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    D["sig"] = 0.5 - D["cl"]
    def ols(M, cols):
        X = np.column_stack([np.ones(len(M))] + [M[c].values for c in cols])
        y = M["ex"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(M) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se, "n": len(M)}, index=["const"] + cols)
    out = {}
    out["joint_vr_gt_1.5"] = ols(D[D.vr > 1.5], ["sig", "z1"])
    out["joint_vr_gt_2"] = ols(D[D.vr > 2], ["sig", "z1"])
    out["joint_vr_lt_1"] = ols(D[D.vr < 1], ["sig", "z1"])
    D["sigv"] = D["sig"] * D["vr"]
    out["joint_all_interaction"] = ols(D, ["sig", "z1", "sigv", "vr"])
    out["joint_tails"] = ols(D, ["lowtail", "uptail", "z1"])
    D["clq"] = pd.cut(D["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["low", "q2", "mid", "q4", "high"])
    H = D[D.vr > 1.5]
    out["vr>1.5_by_closeloc"] = H.groupby("clq")["ex"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["vr>1.5_low_minus_high_by_year"] = H.groupby("yr").apply(lambda g: pd.Series({
        "n_low": (g.clq == "low").sum(), "n_high": (g.clq == "high").sum(),
        "diff": g.loc[g.clq == "low", "ex"].mean() - g.loc[g.clq == "high", "ex"].mean(),
        "t": stats.ttest_ind(g.loc[g.clq == "low", "ex"], g.loc[g.clq == "high", "ex"], equal_var=False).statistic}))
    out["vr>1.5_slope_by_coin"] = H.groupby("coin").apply(lambda g: pd.Series({"n": len(g),
        "slope": stats.linregress(g["sig"], g["ex"]).slope,
        "t": stats.linregress(g["sig"], g["ex"]).slope / stats.linregress(g["sig"], g["ex"]).stderr}))
    out["vr>1.5_lowclose_rawfwd"] = H.groupby("clq")["fwd"].mean()
    return out
