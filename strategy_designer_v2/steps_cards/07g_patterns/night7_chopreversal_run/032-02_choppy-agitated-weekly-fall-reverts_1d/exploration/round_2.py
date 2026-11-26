def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    dr = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy().reset_index(drop=True)
            d["coin"] = coin; d["win"] = w
            c = d["close"].astype(float)
            r = d["coin_return"]
            d["prev"] = r.shift(1)
            d["vol30"] = r.shift(1).rolling(30, min_periods=20).std()
            d["tr60"] = c.shift(1) / c.shift(61) - 1
            d["vrank"] = d["vol30"].rank(pct=True)
            d["fwd3"] = c.shift(-2) / c.shift(1) - 1
            dr.append(d)
    D = pd.concat(dr, ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    D["vr"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["pz"] = D["prev"] / D["vol30"]
    D["drift"] = D.groupby("coin")["coin_return"].transform("mean")
    D["ex"] = D["coin_return"] - D["drift"]
    D["ez"] = D["ex"] / D["vol30"]
    D = D.dropna(subset=["pz", "ez"])

    def clus(g):
        # day-clustered t of mean excess, and slope of ez on pz with per-day summed residual
        s = g.groupby("day")["ex"].sum()
        nd = len(s)
        m = g["ex"].mean()
        t = s.mean() / (s.std() / np.sqrt(nd)) if nd > 2 else np.nan
        x = g["pz"].values; y = g["ez"].values
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        V = XtXi @ (sc.T @ sc) @ XtXi
        return pd.Series(dict(n=len(g), days=nd, mean_ex=m, t_mean=t, slope=b[1], t_slope=b[1] / np.sqrt(V[1, 1])))

    out = {}
    out["all"] = clus(D)
    Fall = D[D["pz"] < 0]
    out["after_fall_slope"] = clus(Fall)
    out["after_rise_slope"] = clus(D[D["pz"] > 0])
    D["pb"] = pd.cut(D["pz"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_day_by_prev_z_clustered"] = D.groupby("pb").apply(clus)
    out["after_fall_by_coin"] = Fall.groupby("coin").apply(clus)
    out["after_fall_by_year"] = Fall.groupby(Fall["day"].dt.year).apply(clus)
    Fall = Fall.copy()
    Fall["tb"] = pd.cut(Fall["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    Fall["vb"] = pd.cut(Fall["vr"], [0, 0.5, 1], labels=["calm", "agit"])
    out["after_fall_by_trend"] = Fall.groupby("tb").apply(clus)
    out["after_fall_by_vol"] = Fall.groupby("vb").apply(clus)
    out["after_fall_by_trend_vol"] = Fall.groupby(["tb", "vb"]).apply(clus)
    # 3-day horizon after fall, grid every 3 days not done; check mean fwd3 by bucket
    Fall["pb2"] = pd.cut(Fall["pz"], [-99, -2, -1, 0])
    out["fwd3_after_fall"] = Fall.groupby("pb2")["fwd3"].agg(["size", "mean"])
    # weekday, mean across coins per day (one obs per day)
    dm = D.groupby("day")["ex"].mean()
    wd = pd.DataFrame(dict(ex=dm, wd=dm.index.weekday))
    out["weekday_daymean"] = wd.groupby("wd")["ex"].agg(["size", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["weekday_by_year_fri_sat"] = wd[wd["wd"].isin([4, 5])].groupby(wd[wd["wd"].isin([4, 5])].index.year)["ex"].agg(["size", "mean"])
    return out
