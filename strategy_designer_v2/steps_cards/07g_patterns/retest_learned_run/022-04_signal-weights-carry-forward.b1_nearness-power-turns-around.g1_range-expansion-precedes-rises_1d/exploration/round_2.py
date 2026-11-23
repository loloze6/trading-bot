def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- weekday effect: one value per calendar day (mean over coins), by year and coin
    allb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy(); c = b["close"]
            b["fwd1"] = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["year"] = ts.dt.year
            b["coin"] = coin; b["win"] = w; b["key"] = ts.dt.strftime("%Y%m%d")
            allb.append(b[["fwd1", "wd", "year", "coin", "win", "key"]])
    A = pd.concat(allb).dropna()
    dm = A.groupby(["win", "key"]).agg(fwd1=("fwd1", "mean"), wd=("wd", "first"), year=("year", "first")).reset_index()
    a = dm.groupby("wd")["fwd1"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["wd_daymean_over_coins"] = a
    dm["thfr"] = dm["wd"].isin([3, 4])
    def welch(x):
        p, q = x.loc[x.thfr, "fwd1"], x.loc[~x.thfr, "fwd1"]
        return pd.Series({"n_thfr": len(p), "diff": p.mean() - q.mean(), "t": stats.ttest_ind(p, q, equal_var=False)[0]})
    out["thfr_minus_rest_by_year"] = dm.groupby("year").apply(welch)
    A["thfr"] = A["wd"].isin([3, 4])
    out["thfr_minus_rest_by_coin"] = A.groupby("coin").apply(welch)
    # ---- signed range: range ratio x close location, 5-day grid
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            b["rr"] = (h - l) / (h - l).rolling(30, min_periods=10).mean()
            b["clv"] = (c - l) / (h - l).replace(0, np.nan)
            b["srr"] = b["rr"] * (2 * b["clv"] - 1)
            b["r20p"] = c / c.shift(20) - 1
            b["fwd5"] = c.shift(-5) / c - 1
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            g = b.iloc[::5].copy(); g["coin"] = coin; g["win"] = w
            rows.append(g)
    G = pd.concat(rows).dropna(subset=["fwd5"])
    G["ex"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    res = []
    for f in ["rr", "srr", "clv"]:
        d = G[[f, "ex"]].dropna(); s = stats.linregress(d[f], d["ex"])
        res.append({"feat": f, "n": len(d), "t": s.slope / s.stderr})
    d = G[["rr", "clv", "ex"]].dropna()
    X = np.column_stack([np.ones(len(d)), d["rr"], d["clv"]])
    beta, *_ = np.linalg.lstsq(X, d["ex"].values, rcond=None)
    resid = d["ex"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=3)
    res.append({"feat": "multi rr | clv", "n": len(d), "t": beta[1] / np.sqrt(cov[1, 1])})
    res.append({"feat": "multi clv | rr", "n": len(d), "t": beta[2] / np.sqrt(cov[2, 2])})
    out["range_features_t"] = pd.DataFrame(res)
    d = G[["srr", "ex"]].dropna().copy()
    d["q"] = pd.qcut(d["srr"], 5, labels=False)
    a = d.groupby("q")["ex"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["q_srr"] = a
    def st(x, f):
        x = x.dropna(subset=[f, "ex"])
        s = stats.linregress(x[f], x["ex"]); return s.slope / s.stderr
    out["srr_t_by_coin"] = G.groupby("coin").apply(lambda x: st(x, "srr"))
    out["srr_t_by_year"] = G.groupby("year").apply(lambda x: st(x, "srr"))
    out["r20_t_by_coin"] = G.groupby("coin").apply(lambda x: st(x, "r20p"))
    # ---- book: weekday of its daily returns
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["win"] = w; D.append(x)
    D = pd.concat(D).dropna(subset=["book_return"])
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    a = bk.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book_by_weekday"] = a
    return out
