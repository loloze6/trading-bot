def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def cl_slope(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 20 or d[x].std() == 0: return pd.Series(dict(n=len(d), days=np.nan, slope=np.nan, t=np.nan))
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ Y; e = Y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = d["day"].nunique(); N = len(d)
        V = XtX @ meat @ XtX * G / (G - 1) * (N - 1) / (N - 2)
        return pd.Series(dict(n=N, days=G, slope=beta[1], t=beta[1] / np.sqrt(V[1, 1])))
    def grp(d, col):
        s = d[col].dropna()
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    # per-coin median of 30d swing over all its bars (proxy for agitation split)
    swing_all = {}
    for coin, wins in data["bars"].items():
        vals = []
        for w, b in wins.items():
            lr = np.log(b["close"].values); d1 = np.diff(lr)
            s = pd.Series(d1).rolling(30).std().values
            vals.extend(list(s[~np.isnan(s)]))
        swing_all[coin] = np.median(vals) if vals else np.nan
    res = {}
    for H in (3, 5, 10):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True); c = b["close"].values; n = len(b)
                d1 = np.r_[np.nan, np.diff(np.log(c))]
                sw = pd.Series(d1).rolling(30).std().values
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, day=pd.Timestamp(b["timestamp"].iloc[i]).floor("D"),
                                     r=c[i + H] / c[i] - 1, reg=b["regime"].iloc[i], f=b["forecast"].iloc[i],
                                     r60=c[i] / c[i - 60] - 1 if i >= 60 else np.nan,
                                     agit=(sw[i] > swing_all[coin]) if not np.isnan(sw[i]) else np.nan))
        g = pd.DataFrame(rows)
        g["ex"] = g["r"] - g["coin"].map(g.groupby("coin")["r"].mean())
        g["sx"] = -g["ex"]
        t = g[g.reg == "trending"].dropna(subset=["f"]).copy()
        res[H] = t
        out[f"slope_H{H}"] = cl_slope(t, "f", "ex").to_frame().T
        t["quiet"] = np.where(t["f"] <= -2, "quiet", "notquiet")
        out[f"short_by_quiet_H{H}"] = t.groupby("quiet").apply(lambda d: grp(d, "sx"))
    t = res[5].copy()
    t["trend60"] = pd.cut(t["r60"], [-10, -0.10, 0.10, 10], labels=["falling", "choppy", "rising"])
    t["ag"] = t["agit"].map({True: "agitated", False: "calm"})
    t["quiet"] = np.where(t["f"] <= -2, "quiet", "notquiet")
    out["H5_profile_short"] = t.groupby(["trend60", "ag"]).apply(lambda d: grp(d, "sx"))
    out["H5_profile_slope"] = t.groupby(["trend60", "ag"]).apply(lambda d: cl_slope(d, "f", "ex"))
    out["H5_falling_calm_by_quiet"] = t[(t.trend60 == "falling") & (t.ag == "calm")].groupby("quiet").apply(lambda d: grp(d, "sx"))
    out["H5_agit_by_quiet"] = t.groupby(["ag", "quiet"]).apply(lambda d: grp(d, "sx"))
    # all bars (not only trending) short excess, to see if fall regime itself matters
    g5 = res[5]
    return out
