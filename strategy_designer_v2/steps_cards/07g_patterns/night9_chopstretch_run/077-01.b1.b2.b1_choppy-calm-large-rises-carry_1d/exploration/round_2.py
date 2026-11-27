def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            vsr = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            vs7 = (c / c.shift(7) - 1) / (sd30 * np.sqrt(7))
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(d["timestamp"])
            pos = np.arange(len(d))
            inprof = d["regime"].astype(str).isin(["trending", "unknown"])
            t = pd.DataFrame(dict(coin=coin, w=w, day=ts.dt.normalize(), vsr=vsr, vs7=vs7, r1z=r1 / sd30,
                                  fwd=fwd, fwd1=fwd1, fwd3=fwd3, grid=(pos % H == 0), grid3=(pos % 3 == 0),
                                  inprof=inprof, wd=ts.dt.weekday, yr=ts.dt.year, w_=w))
            rows.append(t)
    A = pd.concat(rows, ignore_index=True)
    def ctt(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 5: return pd.Series(dict(n=n, days=x.day.nunique(), mean=np.nan, t_cl=np.nan))
        m = x[col].mean()
        dev = (x[col] - m).groupby(x.day).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n
        return pd.Series(dict(n=n, days=G, mean=m, t_cl=m / se if se > 0 else np.nan))
    out = {}
    out["share_bars_in_profile"] = A.inprof.mean()
    g = A[A.grid & A.fwd.notna()].copy()
    g["ex"] = g.fwd - g.coin.map(g.groupby("coin").fwd.mean())
    g["vbin"] = pd.cut(g.vsr, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["7d_by_inprof_vsr"] = g.groupby(["inprof", "vbin"]).apply(lambda x: ctt(x, "ex"))
    out["7d_all_vsr_clustered"] = g.groupby("vbin").apply(lambda x: ctt(x, "ex"))
    gp = g[g.inprof].dropna(subset=["vsr"])
    out["rho_vsr_inprof"] = pd.Series(dict(n=len(gp), rho=stats.spearmanr(gp.vsr, gp.ex)[0]))
    go = g[~g.inprof].dropna(subset=["vsr"])
    out["rho_vsr_outprof"] = pd.Series(dict(n=len(go), rho=stats.spearmanr(go.vsr, go.ex)[0]))
    g["v7bin"] = pd.cut(g.vs7, [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["7d_by_inprof_vs7"] = g.groupby(["inprof", "v7bin"]).apply(lambda x: ctt(x, "ex"))
    # next day after big day moves, clustered
    a1 = A[A.fwd1.notna()].copy()
    a1["ex1"] = a1.fwd1 - a1.groupby("coin").fwd1.transform("mean")
    a1["zbin"] = pd.cut(a1.r1z, [-np.inf, -2, -1, 1, 2, np.inf])
    out["1d_after_dayz_inprof"] = a1.groupby(["inprof", "zbin"]).apply(lambda x: ctt(x, "ex1"))
    a1s = a1.dropna(subset=["r1z"])
    out["rho_r1z_next_inprof"] = a1s.groupby("inprof").apply(lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x.r1z, x.ex1)[0])))
    # 3-day after big down day, grid3
    a3 = A[A.grid3 & A.fwd3.notna()].copy()
    a3["ex3"] = a3.fwd3 - a3.groupby("coin").fwd3.transform("mean")
    a3["zbin"] = pd.cut(a3.r1z, [-np.inf, -2, -1, 1, 2, np.inf])
    out["3d_after_dayz_inprof"] = a3.groupby(["inprof", "zbin"]).apply(lambda x: ctt(x, "ex3"))
    # weekday of the next-day return, clustered
    a1["rwd"] = (a1.wd + 1) % 7
    out["1d_by_return_weekday"] = a1.groupby("rwd").apply(lambda x: ctt(x, "ex1"))
    out["1d_by_return_weekday_inprof"] = a1[a1.inprof].groupby("rwd").apply(lambda x: ctt(x, "ex1"))
    # down-day rebound by year stability
    dd = a1[a1.r1z <= -1]
    out["1d_after_down_by_year"] = dd.groupby("yr").apply(lambda x: ctt(x, "ex1"))
    return out
