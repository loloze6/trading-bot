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
            for H in (1, 2, 3):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, n, H)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "H": H, "yr": ts.dt.year.iloc[idx].values,
                    "fwd": fwd.iloc[idx].values, "vr": vr.iloc[idx].values, "cl": cl.iloc[idx].values,
                    "r1": r1.iloc[idx].values, "z1": (r1 / sd20).iloc[idx].values,
                    "wd": ts.dt.weekday.iloc[idx].values}))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "cl"])
    D["ex"] = D["fwd"] - D.groupby(["coin", "H"])["fwd"].transform("mean")
    D["sig"] = 0.5 - D["cl"]  # positive when close near low
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))})
    def slope(g, col="sig"):
        g = g.dropna(subset=[col, "ex"])
        r = stats.linregress(g[col], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    for H in (1, 2, 3):
        out[f"slope_ex_on_lowclose_H{H}"] = slope(D[D.H == H]).to_frame().T
    D1 = D[D.H == 1].copy()
    out["H1_slope_by_coin"] = D1.groupby("coin").apply(slope)
    out["H1_slope_by_year"] = D1.groupby("yr").apply(slope)
    D1["vrb"] = pd.cut(D1["vr"], [0, 0.8, 1.2, 2, 100], labels=["<0.8", "0.8-1.2", "1.2-2", ">2"])
    out["H1_slope_by_volratio"] = D1.groupby("vrb").apply(slope)
    # multivariate: close location vs own day's return z
    M = D1.dropna(subset=["z1", "sig", "ex"])
    X = np.column_stack([np.ones(len(M)), M["sig"], M["z1"]])
    beta, *_ = np.linalg.lstsq(X, M["ex"].values, rcond=None)
    res = M["ex"].values - X @ beta
    s2 = res @ res / (len(M) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["H1_joint_sig_and_z1"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "lowclose", "z1"])
    D1["clq"] = pd.cut(D1["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["low", "q2", "mid", "q4", "high"])
    out["H1_low_minus_high_by_coin"] = D1.groupby("coin").apply(lambda g: pd.Series({
        "low": g.loc[g.clq == "low", "ex"].mean(), "high": g.loc[g.clq == "high", "ex"].mean(),
        "t_welch": stats.ttest_ind(g.loc[g.clq == "low", "ex"], g.loc[g.clq == "high", "ex"], equal_var=False).statistic}))
    out["H1_weekday_by_coin_fri"] = D1[D1.wd == 4].groupby("coin").apply(summ)
    out["H1_weekday_by_year_fri"] = D1[D1.wd == 4].groupby("yr").apply(summ)
    out["H1_closeloc_raw_mean_fwd"] = D1.groupby("clq")["fwd"].agg(["count", "mean"])
    return out
