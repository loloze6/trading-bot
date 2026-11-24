def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    def ctest(v, day):
        d = pd.DataFrame(dict(v=v, day=day)).dropna()
        m = d["v"].mean()
        g = (d["v"] - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g**2).sum() * D / (D - 1)) / len(d) if D > 1 else np.nan
        return m, m / se, len(d), D
    # 10-day grid: past 10/30 day return
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].astype(float).values)
            ts = pd.to_datetime(b["timestamp"])
            p10 = c.pct_change(10).values; p30 = c.pct_change(30).values
            r1 = c.pct_change()
            v60 = r1.rolling(60, min_periods=30).std().values
            for t in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, w=w, wd=ts.iloc[t].weekday(), yr=ts.iloc[t].year,
                                 day=ts.iloc[t].normalize(), fwd=c[t+H]/c[t]-1,
                                 p10=p10[t], p30=p30[t], s30=p30[t]/(v60[t]*np.sqrt(30)) if v60[t] > 0 else np.nan))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df["coin"].map(df.groupby("coin")["fwd"].mean())
    res = {}
    for col in ["p10", "p30", "s30"]:
        d = df.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        for q in range(5):
            g = d[d["q"] == q]
            m, t, n, D = ctest(g["ex"], g["day"])
            res[(col, q)] = dict(mean_ex=m, t_day=t, n=n, days=D)
        top = d[d["q"] == 4]["ex"]; bot = d[d["q"].isin([0, 1])]["ex"]
        # slope with day clustering via rank corr per coin
        d["rz"] = d.groupby("coin")[col].rank(pct=True) - 0.5
        X = d["rz"].values; y = d["ex"].values
        b1 = np.sum(X * (y - y.mean())) / np.sum(X**2)
        e = (y - y.mean() - b1 * X) * X
        g = pd.Series(e).groupby(d["day"].values).sum()
        se = np.sqrt((g**2).sum()) / np.sum(X**2)
        res[(col, "slope_rank")] = dict(mean_ex=b1, t_day=b1/se, n=len(d), days=g.size)
    out["momentum_quintiles_clustered"] = pd.DataFrame(res).T
    # momentum s30 top-vs-rest by year
    d = df.dropna(subset=["s30"]).copy()
    d["hi"] = d.groupby("coin")["s30"].transform(lambda s: s.rank(pct=True) > 0.8)
    out["s30_top_minus_rest_by_year"] = d.groupby("yr").apply(lambda g: pd.Series(dict(
        top=g[g.hi]["ex"].mean(), rest=g[~g.hi]["ex"].mean(), n_top=int(g.hi.sum()))))
    m, t, n, D = ctest(df["ex"].where(df["wd"] == 3), df["day"])
    out["thursday_clustered"] = f"mean={m:.4f} t={t:.2f} n={n} days={D}"
    # daily: next 1,3,5 days after shock z, day-clustered
    dr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = pd.Series(b["close"].astype(float).values)
            ts = pd.to_datetime(b["timestamp"]).dt.normalize().values
            r = c.pct_change()
            z = r / r.rolling(60, min_periods=30).std().shift(1)
            dr.append(pd.DataFrame(dict(coin=coin, w=w, day=ts, z=z, r=r,
                                        n1=c.shift(-1)/c-1, n3=c.shift(-3)/c-1, n5=c.shift(-5)/c-1,
                                        yr=pd.to_datetime(ts).year)))
    dd = pd.concat(dr).dropna()
    for k in ["n1", "n3", "n5"]:
        dd[k + "x"] = dd[k] - dd["coin"].map(dd.groupby("coin")[k].mean())
    dd["zb"] = pd.cut(dd["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    tab = {}
    for zb, g in dd.groupby("zb"):
        r = {}
        for k in ["n1x", "n3x", "n5x"]:
            m, t, n, D = ctest(g[k], g["day"])
            r[k] = m; r["t_" + k] = t
        r["n"] = len(g); r["days"] = g["day"].nunique()
        tab[str(zb)] = r
    out["after_shock_clustered"] = pd.DataFrame(tab).T
    # within down shocks, graded? and by year
    neg = dd[dd["z"] < -2].copy()
    out["down_shock_n1x_by_year"] = neg.groupby("yr").agg(n=("n1x", "size"), n1x=("n1x", "mean"), n3x=("n3x", "mean"))
    out["down_shock_n1x_by_coin"] = neg.groupby("coin").agg(n=("n1x", "size"), n1x=("n1x", "mean"), n3x=("n3x", "mean"))
    rho, p = stats.spearmanr(neg["z"], neg["n1x"])
    out["down_shock_grade_spearman"] = f"rho={rho:.3f} p={p:.4f} n={len(neg)}"
    # non-overlapping 3-day grid for down shocks: count once
    return out
