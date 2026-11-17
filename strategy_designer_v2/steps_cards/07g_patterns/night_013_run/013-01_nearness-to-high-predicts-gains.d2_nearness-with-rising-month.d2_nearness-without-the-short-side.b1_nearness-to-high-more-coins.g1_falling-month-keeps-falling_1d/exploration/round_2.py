def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            hi60 = c.rolling(60, min_periods=30).max()
            depth = c / hi60 - 1
            vrel = v / v.rolling(20, min_periods=15).mean()
            vol20 = r1.rolling(20, min_periods=15).std()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b), H):
                rows.append(dict(coin=coin, w=w, ret30=ret30[i], depth=depth[i], vrel=vrel[i], vol20=vol20[i],
                                 fwd=fwd[i], year=ts[i].year, date=ts[i].floor("D")))
            daily.append(pd.DataFrame(dict(coin=coin, w=w, wd=ts.dt.weekday, year=ts.dt.year,
                                           date=ts.dt.floor("D"), fwd1=c.shift(-1)/c-1)))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def dclust_t(d, col):
        # date-clustered: regress, then t from per-date mean of residual-weighted products
        d = d.dropna(subset=[col, "ex"])
        x = d[col] - d[col].mean()
        sl = (x * d["ex"]).sum() / (x**2).sum()
        e = d["ex"] - d["ex"].mean() - sl * x
        sc = (x * e).groupby(d["date"]).sum()
        se = np.sqrt((sc**2).sum()) / (x**2).sum()
        return round(sl, 4), round(sl / se, 2), len(d), d["date"].nunique()
    f = g[g.ret30 < 0].copy()
    out["clustered_slopes"] = pd.DataFrame({
        "depth_falling": dclust_t(f, "depth"),
        "ret30_all": dclust_t(g, "ret30"),
        "ret30_falling": dclust_t(f, "ret30"),
        "ret30_rising": dclust_t(g[g.ret30 >= 0], "ret30"),
        "logvrel_falling": dclust_t(f.assign(lv=np.log(f.vrel)), "lv"),
        "logvrel_all": dclust_t(g.assign(lv=np.log(g.vrel)), "lv"),
    }, index=["slope", "t_dateclust", "n", "dates"]).T
    # regime mean excess, clustered by date
    def cmean(d):
        m = d.groupby("date")["ex"].mean()
        return pd.Series(dict(mean=d["ex"].mean(), t_dates=m.mean()/(m.std()/np.sqrt(len(m))), n=len(d)))
    out["falling_vs_rising_excess"] = pd.DataFrame({"falling": cmean(f), "rising": cmean(g[g.ret30 >= 0])}).T.round(4)
    # ret30 momentum by year
    yr = {}
    for y, d in g.groupby("year"):
        yr[y] = dclust_t(d, "ret30")
    out["ret30_slope_by_year"] = pd.DataFrame(yr, index=["slope", "t", "n", "dates"]).T
    # falling month: deep tercile vs rest by year
    f = f.dropna(subset=["depth"])
    f["deep"] = f.groupby("coin")["depth"].transform(lambda s: s.rank(pct=True)) <= 0.2
    out["deep20_falling_by_year"] = f.groupby(["year", "deep"])["ex"].mean().unstack().round(4)
    # low volume falling by year
    f2 = g[g.ret30 < 0].dropna(subset=["vrel"]).copy()
    f2["lowv"] = f2.groupby("coin")["vrel"].transform(lambda s: s.rank(pct=True)) <= 0.2
    out["lowvol_falling_by_year"] = f2.groupby(["year", "lowv"])["ex"].mean().unstack().round(4)
    out["lowvol_falling_clustered"] = pd.DataFrame({"low": cmean(f2[f2.lowv]), "rest": cmean(f2[~f2.lowv])}).T.round(4)
    # weekday clustered and by year
    D = pd.concat(daily).dropna(subset=["fwd1"])
    D["ex"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    out["weekday_clustered"] = D.groupby("wd").apply(cmean).round(5)
    out["weekday_by_year"] = D.groupby(["year", "wd"])["ex"].mean().unstack().round(4)
    return out
