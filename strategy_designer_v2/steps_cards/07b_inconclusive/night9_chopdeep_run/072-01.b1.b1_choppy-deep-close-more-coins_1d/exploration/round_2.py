def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
    out = {}
    allrows = {}
    for h in H:
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; o = df["open"].values
                n = len(c); ts = pd.to_datetime(df["timestamp"])
                for i in range(0, n - h, h):
                    if df["regime"].iloc[i] != "unknown":
                        continue
                    f = df["forecast"].iloc[i]
                    if not (f < 0):
                        continue
                    rows.append({"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                                 "f": f, "up": c[i] > o[i],
                                 "ex": c[i + h] / c[i] - 1 - drift[(coin, h)]})
        d = pd.DataFrame(rows)
        d["absf"] = d["f"].abs()
        d["terc"] = pd.qcut(d["absf"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
        allrows[h] = d
    def slope_t(d, y="ex"):
        x = d["absf"].values; yy = -d[y].values
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, yy, rcond=None)[0]
        e = yy - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        dd = pd.DataFrame({"g": d["day"].values, "e0": e, "e1": e * x}).groupby("g").sum()
        S = dd.values
        V = XtXi @ (S.T @ S) @ XtXi
        return b[1], b[1] / np.sqrt(V[1, 1]), len(dd)
    res = {}
    for h in H:
        d = allrows[h]
        b, t, nd = slope_t(d)
        dw = d.copy()
        lo, hi = dw["ex"].quantile([0.01, 0.99])
        dw["exw"] = dw["ex"].clip(lo, hi)
        bw, tw, _ = slope_t(dw, "exw")
        a = dw[dw.terc == "deep"]["exw"]; s = dw[dw.terc == "shallow"]["exw"]
        tt = stats.ttest_ind(-a, -s, equal_var=False)
        res[h] = {"n": len(d), "days": nd, "slope_short": b, "t_day": t, "slope_wins": bw, "t_wins": tw,
                  "deep_minus_shallow_short_wins": (-a.mean()) - (-s.mean()), "welch_t": tt.statistic,
                  "spearman_rho": stats.spearmanr(d["absf"], -d["ex"]).correlation}
    out["slope_by_h"] = pd.DataFrame(res).T
    d5 = allrows[5]
    out["h5_terc_median_short"] = d5.groupby("terc")["ex"].apply(lambda x: pd.Series({"median_short": -x.median(), "n_abs_gt30pct": (x.abs() > 0.3).sum(), "max_ex": x.max(), "min_ex": x.min()})).unstack()
    def summ(g):
        x = -g["ex"]
        return pd.Series({"n": len(x), "mean_short": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    d1 = allrows[1]
    out["h1_year_terc"] = d1.groupby(["year", "terc"]).apply(summ)
    out["h1_up_terc"] = d1.groupby(["up", "terc"]).apply(summ)
    core = ["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]
    out["h1_core_vs_other"] = d1.groupby(d1["coin"].isin(core)).apply(summ)
    out["h5_core_vs_other"] = d5.groupby(d5["coin"].isin(core)).apply(summ)
    return out
