def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            vol = r1.rolling(180, min_periods=60).std()
            volrel = r1.rolling(18).std() / vol
            rngrel = (hi - lo).rolling(18).mean() / (hi - lo).rolling(180, min_periods=60).mean()
            r18 = c / c.shift(18) - 1
            prL = lo.shift(1).rolling(12).min()
            dn = (prL - c) / c * 100
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            n = len(b)
            idx = np.arange(0, n - H, H)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year.values[idx],
                "ex": (fwd.values[idx] - drift) / usual, "exr": fwd.values[idx] - drift,
                "volrel": volrel.values[idx], "rngrel": rngrel.values[idx],
                "r18": r18.values[idx], "dn": dn.values[idx]}))
    D = pd.concat(rows).dropna(subset=["ex", "volrel", "rngrel", "r18"])
    def tstat(s):
        return s.mean() / (s.std() / np.sqrt(len(s)))
    def grp(X, col, q):
        g = pd.qcut(X[col].rank(method="first"), q, labels=False)
        t = X.groupby(g)["ex"].agg(["count", "mean"])
        t["t"] = X.groupby(g)["ex"].apply(tstat)
        t["exr_mean"] = X.groupby(g)["exr"].mean()
        return t
    out = {}
    out["volrel_dec"] = grp(D, "volrel", 10)
    out["rngrel_dec"] = grp(D, "rngrel", 10)
    # per coin: top minus bottom quintile of volrel and rngrel, and correlations
    def coinstats(X):
        q = pd.qcut(X["volrel"].rank(method="first"), 5, labels=False)
        q2 = pd.qcut(X["rngrel"].rank(method="first"), 5, labels=False)
        return pd.Series({"n": len(X),
            "vr_top_ex": X.ex[q == 4].mean(), "vr_bot_ex": X.ex[q == 0].mean(),
            "rr_top_ex": X.ex[q2 == 4].mean(), "rr_bot_ex": X.ex[q2 == 0].mean(),
            "spearman_rr": X[["rngrel", "ex"]].corr(method="spearman").iloc[0, 1]})
    out["by_coin"] = D.groupby("coin").apply(coinstats)
    out["by_year"] = D.groupby("year").apply(coinstats)
    # does high recent range help after rises and after falls alike?
    D["up18"] = np.where(D.r18 > 0, "after_rise", "after_fall")
    D["rrq"] = pd.qcut(D["rngrel"].rank(method="first"), 3, labels=["low", "mid", "high"])
    t = D.groupby(["up18", "rrq"])["ex"].agg(["count", "mean"])
    t["t"] = D.groupby(["up18", "rrq"])["ex"].apply(tstat)
    t["exr_mean"] = D.groupby(["up18", "rrq"])["exr"].mean()
    out["rise_fall_x_range"] = t
    # down-break by size per coin
    dnb = D[D.dn > 0]
    out["dnbreak_by_coin"] = dnb.groupby("coin")["ex"].agg(["count", "mean"])
    # weekday daily returns size (non overlapping days)
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.dropna(subset=["coin_return"])
            dd.append(pd.DataFrame({"coin": coin, "wd": pd.to_datetime(x["day"]).dt.weekday, "r": x["coin_return"]}))
    DD = pd.concat(dd)
    DD["ex"] = DD["r"] - DD.groupby("coin")["r"].transform("mean")
    wt = DD.groupby("wd")["ex"].agg(["count", "mean"])
    wt["t"] = DD.groupby("wd")["ex"].apply(tstat)
    out["weekday_daily_excess"] = wt
    out["friday_by_coin"] = DD[DD.wd == 4].groupby("coin")["ex"].mean()
    return out
