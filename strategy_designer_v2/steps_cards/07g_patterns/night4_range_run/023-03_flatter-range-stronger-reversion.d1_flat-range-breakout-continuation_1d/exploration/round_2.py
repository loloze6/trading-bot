def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            hi = c.rolling(31).max(); lo = c.rolling(31).min()
            rng = hi - lo
            pos = (c - lo) / rng
            net = (c - c.shift(30)) / rng
            r1 = c.pct_change()
            v10 = r1.rolling(10).std(); v20 = r1.rolling(20).std(); v60 = r1.rolling(60, min_periods=40).std()
            rngrel = rng / c
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, pos=pos.iloc[i], net=net.iloc[i], v20=v20.iloc[i],
                                 vr=v10.iloc[i] / v60.iloc[i] if v60.iloc[i] > 0 else np.nan,
                                 rngrel=rngrel.iloc[i], fwd=fwd.iloc[i], year=ts.iloc[i].year,
                                 fc=b["forecast"].iloc[i]))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    g["s"] = 2 * g["pos"] - 1
    # causal: coin's v20 rank against its own past cases only (expanding over window order)
    g["v20_rank_coin"] = g.groupby("coin")["v20"].rank(pct=True)
    g["half"] = np.where(g["year"] <= 2021, "2018-21", "2022-25")
    out = {}
    def slopes(d, xcol, bycol, q=3):
        d = d.dropna(subset=[xcol, bycol, "z"])
        bb = pd.qcut(d[bycol].rank(method="first"), q, labels=False)
        res = []
        for k, sub in d.groupby(bb):
            sl = stats.linregress(sub[xcol], sub["z"])
            res.append(dict(tercile=k, mean_by=sub[bycol].mean(), n=len(sub), slope=sl.slope, t=sl.slope / sl.stderr,
                            ex_top_minus_bot_pct=(sub.loc[sub[xcol] > 0.5, "ex"].mean() - sub.loc[sub[xcol] < -0.5, "ex"].mean()) * 100))
        return pd.DataFrame(res).round(4)
    out["pos_slope_by_v20coinrank"] = slopes(g, "s", "v20_rank_coin")
    out["pos_slope_by_v10v60"] = slopes(g, "s", "vr")
    out["pos_slope_by_range_width"] = slopes(g, "s", "rngrel")
    for h, sub in g.groupby("half"):
        out["pos_slope_by_v20rank_" + h] = slopes(sub, "s", "v20_rank_coin")
    d = g.dropna(subset=["s", "v20_rank_coin", "z"]).copy()
    d["low"] = d["v20_rank_coin"] <= 1/3
    res = []
    for c, sub in d[d["low"]].groupby("coin"):
        sl = stats.linregress(sub["s"], sub["z"]); res.append(dict(coin=c, n=len(sub), slope=sl.slope, t=sl.slope / sl.stderr))
    out["lowvol_pos_slope_by_coin"] = pd.DataFrame(res).round(4)
    # graded interaction: z on s, s*calm where calm = 1 - rank
    d["calm"] = 1 - d["v20_rank_coin"]
    X = np.column_stack([np.ones(len(d)), d["s"], d["s"] * d["calm"], d["calm"]])
    beta, *_ = np.linalg.lstsq(X, d["z"].values, rcond=None)
    resid = d["z"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=4)
    out["interaction_s_x_calm"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                               index=["const", "s", "s_x_calm", "calm"]).round(4)
    # weekday robustness
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; dl.append(x)
    D = pd.concat(dl); D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek; D["half"] = np.where(D["day"].dt.year <= 2021, "a", "b")
    sat = D[D["wd"] == 5]; oth = D[D["wd"] != 5]
    res = []
    for c in D["coin"].unique():
        a = sat[sat.coin == c]["coin_return"].dropna(); b2 = oth[oth.coin == c]["coin_return"].dropna()
        res.append(dict(coin=c, sat=a.mean(), other=b2.mean(), t=stats.ttest_ind(a, b2, equal_var=False).statistic))
    for h in ["a", "b"]:
        a = sat[sat.half == h]["coin_return"].dropna(); b2 = oth[oth.half == h]["coin_return"].dropna()
        res.append(dict(coin="half_" + h, sat=a.mean(), other=b2.mean(), t=stats.ttest_ind(a, b2, equal_var=False).statistic))
    out["saturday_vs_other"] = pd.DataFrame(res).round(5)
    out["book_by_weekday"] = D.groupby("wd")["book_return"].agg(["mean", "count"]).round(5)
    return out
