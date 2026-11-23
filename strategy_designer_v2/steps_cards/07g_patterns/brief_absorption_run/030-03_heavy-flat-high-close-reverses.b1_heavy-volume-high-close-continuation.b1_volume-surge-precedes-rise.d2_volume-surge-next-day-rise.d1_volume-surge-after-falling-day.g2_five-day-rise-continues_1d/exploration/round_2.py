def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["r5"] = c / c.shift(5) - 1
            b["relvol"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1)
            v5 = b["volume"].rolling(5).sum()
            b["relvol5"] = v5 / (b["volume"].rolling(60, min_periods=30).mean().shift(5) * 5)
            b["lrv"] = np.log(b["relvol"])
            b["lrv5"] = np.log(b["relvol5"])
            b["fc"] = b["forecast"]
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    g = df[(df["pos"] % H == 0) & df["fwd"].notna()].copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["ex"] / g["coin"].map(usual)
    g["r5z"] = g["r5"] / g.groupby("coin")["r5"].transform(lambda s: s.abs().mean())
    def summ(grp):
        x = grp["ex"]
        return pd.Series({"n": len(x), "mean_ex%": 100*x.mean(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "meanz": grp["z"].mean()})
    def ols(x, y):
        m = x.notna() & y.notna() & np.isfinite(x)
        r = stats.linregress(x[m], y[m])
        return pd.Series({"n": m.sum(), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    out["all grid: ex z on log relvol"] = ols(g["lrv"], g["z"])
    out["all grid: ex z on log relvol5"] = ols(g["lrv5"], g["z"])
    p = g[g["fc"] > 0].copy()
    out["fc>0: z on log relvol"] = ols(p["lrv"], p["z"])
    out["fc>0: z on log relvol5"] = ols(p["lrv5"], p["z"])
    out["fc>0: z on fc"] = ols(p["fc"], p["z"])
    # interaction regression on all grid
    X = g[["r5z", "lrv", "z"]].replace([np.inf, -np.inf], np.nan).dropna()
    X["inter"] = X["r5z"] * X["lrv"]
    A = np.column_stack([np.ones(len(X)), X["r5z"], X["lrv"], X["inter"]])
    beta, *_ = np.linalg.lstsq(A, X["z"].values, rcond=None)
    res = X["z"].values - A @ beta
    s2 = res @ res / (len(X) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    out["all grid: z ~ r5z + lrv + r5z*lrv"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["const", "r5z", "lrv", "inter"])
    # signed volume: r5 sign times relvol
    g["lrv_q"] = pd.qcut(g["lrv"], 5)
    out["r5 up vs down by relvol quintile"] = g.assign(up=g["r5"] > 0).groupby(["lrv_q", "up"]).apply(summ)
    out["relvol top quintile by coin"] = g[g["lrv"] > g["lrv"].quantile(0.8)].groupby("coin").apply(summ)
    out["relvol top quintile by year"] = g[g["lrv"] > g["lrv"].quantile(0.8)].groupby("yr").apply(summ)
    hp = p[p["lrv"] > p["lrv"].quantile(2/3)]
    out["fc>0 & top relvol tercile by coin"] = hp.groupby("coin").apply(summ)
    out["fc>0 & top relvol tercile by year"] = hp.groupby("yr").apply(summ)
    # up day vs down day heavy volume
    hv = g[g["lrv"] > g["lrv"].quantile(0.8)]
    out["heavy vol days: by 1d sign"] = hv.groupby(hv["r1"] > 0).apply(summ)
    return out
