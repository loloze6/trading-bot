def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; days.append(d)
    D = pd.concat(days, ignore_index=True)
    D["dt"] = pd.to_datetime(D["day"]); D["wd"] = D.dt.dt.weekday; D["yr"] = D.dt.dt.year
    D["sat"] = (D.wd == 5)
    out = {}
    def welch(sub, col="coin_return"):
        a = sub[sub.sat][col].dropna(); b = sub[~sub.sat][col].dropna()
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        return pd.Series({"n_sat": len(a), "sat_mean": a.mean(), "rest_mean": b.mean(), "t": t})
    out["sat_by_year"] = D.groupby("yr").apply(welch).round(5)
    out["sat_by_coin"] = D.groupby("coin").apply(welch).round(5)
    # cross-coin averaged per day (removes same-day correlation)
    M = D.groupby(["win", "day", "wd"])["coin_return"].mean().reset_index()
    M["sat"] = M.wd == 5
    out["sat_daymean"] = welch(M).round(5)
    out["book_sat"] = welch(D, "book_return").round(5)
    # hi20 x volume, per year, on bars grid
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy(); c = b["close"]
            b["coin"] = coin
            b["f7"] = c.shift(-7) / c - 1
            b["hi20"] = c / c.rolling(20, min_periods=20).max().shift(1) - 1
            b["vr"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean().shift(1)
            b["grid"] = (np.arange(len(b)) % 7) == 0
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["trend"] = b["regime"] == "trending"
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B[B.grid].groupby("coin")["f7"].mean()
    B["f7x"] = B["f7"] - B["coin"].map(cm)
    G = B[B.grid].dropna(subset=["f7x", "hi20", "vr"]).copy()
    G["x"] = (G.hi20.rank(pct=True) - 0.5) + (G.vr.rank(pct=True) - 0.5)
    yt = {}
    for yr, s in G.groupby("yr"):
        r = stats.linregress(s.x, s.f7x); yt[yr] = {"n": len(s), "slope": r.slope, "t": r.slope / r.stderr}
    r = stats.linregress(G.x, G.f7x); yt["all"] = {"n": len(G), "slope": r.slope, "t": r.slope / r.stderr}
    out["hi20vol_year"] = pd.DataFrame(yt).T.round(4)
    # interaction: near 20d high (top quintile) vs vr, vs rest
    G["hq"] = pd.qcut(G.hi20.rank(method="first"), 5, labels=False)
    G["vq"] = pd.qcut(G.vr.rank(method="first"), 3, labels=False)
    out["hi20q_x_vq"] = G.pivot_table(index="hq", columns="vq", values="f7x", aggfunc="mean").round(4)
    out["hi20q_x_vq_n"] = G.pivot_table(index="hq", columns="vq", values="f7x", aggfunc="count")
    return out
