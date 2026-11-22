def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            mabs = r1.abs().rolling(180, min_periods=60).mean()
            ret18 = c / c.shift(18) - 1
            vol30 = r1.rolling(180, min_periods=60).std()
            vol6 = r1.rolling(6, min_periods=6).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "fwd": fwd, "r1": r1,
                                      "z18": ret18 / (mabs * np.sqrt(18)), "volratio": vol6 / vol30,
                                      "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year}))
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ufwd"] = A["fwd"] - A["coin"].map(drift)
    G = A[A.pos % H == 0].dropna(subset=["ufwd", "z18", "volratio"]).copy()
    G["zq"] = G.groupby("coin")["z18"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    G["vq"] = G.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    def mt(g, keys, col="ufwd"):
        o = g.groupby(keys)[col].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std").round(5)
    res = {}
    # graded slope of z18 -> ufwd, per coin
    sl = {}
    for coin, g in G.groupby("coin"):
        x = g["z18"].clip(-4, 4); y = g["ufwd"]
        b1 = np.cov(x, y)[0, 1] / x.var()
        resid = y - y.mean() - b1 * (x - x.mean())
        se = resid.std() / (x.std() * np.sqrt(len(x)))
        sl[coin] = {"slope": b1, "t": b1 / se, "n": len(x)}
    res["z18_slope_by_coin"] = pd.DataFrame(sl).T.round(5)
    res["z18_top_by_coin"] = mt(G[G.zq == 4], "coin")
    res["z18_top_minus_mid_by_year"] = (G[G.zq == 4].groupby("year")["ufwd"].mean() - G[G.zq.isin([1, 2, 3])].groupby("year")["ufwd"].mean()).round(5)
    res["volratio_top_minus_bottom_by_coin"] = (G[G.vq == 4].groupby("coin")["ufwd"].mean() - G[G.vq == 0].groupby("coin")["ufwd"].mean()).round(5)
    # own-bar return by start hour, by coin and by year
    B = A.dropna(subset=["r1"])
    res["own_bar_by_hour"] = mt(B, "hour", "r1")
    hc = B.groupby(["coin", "hour"])["r1"].mean().unstack().round(5)
    res["own_bar_hour_by_coin"] = hc
    hy = B.groupby(["year", "hour"])["r1"].mean().unstack().round(5)
    res["own_bar_hour_by_year"] = hy
    # weekend
    res["sat_by_coin"] = (B[B.wd == 5].groupby("coin")["r1"].mean() - B[B.wd != 5].groupby("coin")["r1"].mean()).round(6)
    res["sat_by_year"] = (B[B.wd == 5].groupby("year")["r1"].mean() - B[B.wd != 5].groupby("year")["r1"].mean()).round(6)
    # 20h-start bar t per coin
    t20 = {}
    for coin, g in B.groupby("coin"):
        x = g[g.hour == 20]["r1"]; y = g[g.hour != 20]["r1"]
        from scipy import stats
        t20[coin] = stats.ttest_ind(x, y, equal_var=False).statistic
    res["t_hour20_vs_rest_by_coin"] = pd.Series(t20).round(3)
    return res
