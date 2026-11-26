def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1
                r30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                lr = np.log(c[max(0, i - 30):i + 1])
                vol30 = np.std(np.diff(lr), ddof=1) if i >= 30 else np.nan
                rows.append(dict(coin=coin, win=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 day=pd.Timestamp(b["timestamp"].iloc[i]).floor("D"),
                                 r=r, reg=b["regime"].iloc[i], f=b["forecast"].iloc[i],
                                 raw=b.get("debug_info.components.quiet_volume.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 r30=r30, r60=r60, vol30=vol30))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["r"].mean()
    g["ex"] = g["r"] - g["coin"].map(drift)
    g["short_ex"] = -g["ex"]
    t = g[g.reg == "trending"].dropna(subset=["f"]).copy()

    def cl_slope(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ Y; e = Y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = d["day"].nunique(); k = 2; N = len(d)
        V = XtX @ meat @ XtX * G / (G - 1) * (N - 1) / (N - k)
        return pd.Series(dict(n=N, days=G, slope=beta[1], t=beta[1] / np.sqrt(V[1, 1])))

    def grp(d):
        s = d["short_ex"]
        return pd.Series(dict(n=len(d), mean_short_ex=s.mean(), t=s.mean() / (s.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan))

    out = {}
    out["overall_slope_BC"] = cl_slope(t, "f", "ex").to_frame().T
    t["fbin"] = pd.cut(t["f"], [-21, -10, -4, -2, -0.5, 0.01], labels=["<=-10", "-10..-4", "-4..-2", "-2..-0.5", "~0"])
    out["by_forecast_bin"] = t.groupby("fbin").apply(grp)
    t["depth"] = pd.qcut(t["r30"], 3, labels=["deep", "mid", "shallow"])
    out["by_depth_tercile"] = t.groupby("depth").apply(grp)
    out["slope_by_depth"] = t.groupby("depth").apply(lambda d: cl_slope(d, "f", "ex"))
    t["trend60"] = pd.cut(t["r60"], [-10, -0.10, 0.10, 10], labels=["falling", "choppy", "rising"])
    out["by_trend60"] = t.groupby("trend60").apply(grp)
    out["slope_by_trend60"] = t.groupby("trend60").apply(lambda d: cl_slope(d, "f", "ex"))
    out["slope_r30_all_trending"] = cl_slope(t, "r30", "ex").to_frame().T
    out["by_year"] = t.groupby("year").apply(grp)
    out["slope_by_year"] = t.groupby("year").apply(lambda d: cl_slope(d, "f", "ex"))
    out["by_coin"] = t.groupby("coin").apply(grp)
    # depth x volume
    t["quiet"] = np.where(t["f"] <= -2, "quiet", "notquiet")
    out["depth_x_quiet"] = t.groupby(["depth", "quiet"]).apply(grp)
    # raw volume ratio slope
    out["slope_raw"] = cl_slope(t, "raw", "ex").to_frame().T
    return out
