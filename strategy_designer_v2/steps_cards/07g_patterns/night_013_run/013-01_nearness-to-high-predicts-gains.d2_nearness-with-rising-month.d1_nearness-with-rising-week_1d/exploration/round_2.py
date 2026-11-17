def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; days = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            b["coin"] = coin; b["win"] = w
            b["f7"] = c.shift(-7) / c - 1
            b["f3"] = c.shift(-3) / c - 1
            b["m7"] = c / c.shift(7) - 1
            b["m30"] = c / c.shift(30) - 1
            vol = r1.rolling(30, min_periods=20).std()
            b["vol"] = vol
            b["z1"] = r1 / vol.shift(1)
            b["vr"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean().shift(1)
            b["vr7"] = b["volume"].rolling(7).mean() / b["volume"].rolling(60, min_periods=30).mean().shift(7)
            b["hi20"] = c / c.rolling(20, min_periods=20).max().shift(1) - 1
            b["nh"] = c / c.rolling(364, min_periods=91).max() - 1
            b["grid"] = (np.arange(len(b)) % 7) == 0
            b["grid3"] = (np.arange(len(b)) % 3) == 0
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; days.append(d)
    B = pd.concat(rows, ignore_index=True); D = pd.concat(days, ignore_index=True)
    cm = B[B.grid].groupby("coin")["f7"].mean()
    B["f7x"] = B["f7"] - B["coin"].map(cm)
    G = B[B.grid & B.f7x.notna()].copy()
    out = {}
    def slope(df, col, y="f7x"):
        d = df[[col, y]].dropna()
        d = d[np.isfinite(d[col])]
        if len(d) < 30: return (len(d), np.nan, np.nan)
        x = d[col].rank(pct=True) - 0.5
        r = stats.linregress(x, d[y])
        return (len(d), round(r.slope, 4), round(r.slope / r.stderr, 2))
    res = {}
    for col in ["z1", "hi20", "vr", "vr7", "m7", "m30", "nh", "vol"]:
        for nm, sub in [("all", G), ("trend", G[G.regime == "trending"]), ("off", G[G.regime != "trending"])]:
            n, s, t = slope(sub, col)
            res[(col, nm)] = {"n": n, "rank_slope": s, "t": t}
    out["rank_slopes"] = pd.DataFrame(res).T
    # per-year consistency of z1 and hi20 slopes
    yt = {}
    for yr, sub in G.groupby("yr"):
        yt[yr] = {"z1_t": slope(sub, "z1")[2], "hi20_t": slope(sub, "hi20")[2], "vr_t": slope(sub, "vr")[2], "n": len(sub)}
    out["year_slopes"] = pd.DataFrame(yt).T
    # per coin
    ct = {}
    for co, sub in G.groupby("coin"):
        ct[co] = {"z1_t": slope(sub, "z1")[2], "hi20_t": slope(sub, "hi20")[2], "vr_t": slope(sub, "vr")[2], "nh_t": slope(sub, "nh")[2]}
    out["coin_slopes"] = pd.DataFrame(ct).T
    # multivariate: z1, hi20, vr, nh together
    from numpy.linalg import lstsq
    d = G[["z1", "hi20", "vr", "nh", "m7", "f7x"]].replace([np.inf, -np.inf], np.nan).dropna()
    X = np.column_stack([np.ones(len(d))] + [d[c].rank(pct=True) - 0.5 for c in ["z1", "hi20", "vr", "nh", "m7"]])
    beta, *_ = lstsq(X, d["f7x"].values, rcond=None)
    resid = d["f7x"].values - X @ beta
    s2 = resid @ resid / (len(d) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "z1", "hi20", "vr", "nh", "m7"]).round(4)
    out["multi_n"] = len(d)
    # volume near the 20d high: within top hi20 tercile, vr split
    H = G[G.hi20 > G.hi20.quantile(0.8)]
    H = H[H.vr.notna()]
    H["vq"] = pd.qcut(H.vr.rank(method="first"), 3, labels=False)
    out["nearhi20_by_vol"] = H.groupby("vq")["f7x"].agg(["count", "mean", "std"]).round(4)
    # weekday t-stat of coin daily return
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    wt = D.groupby("wd")["coin_return"].agg(["count", "mean", "std"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["weekday_t"] = wt.round(5)
    # book's largest gains/losses: what preceded (coin z1 day before) and followed
    D = D.sort_values(["coin", "win", "day"])
    D["next_coin"] = D.groupby(["coin", "win"])["coin_return"].shift(-1)
    D["prev_coin"] = D.groupby(["coin", "win"])["coin_return"].shift(1)
    q_hi = D.book_return.quantile(0.99); q_lo = D.book_return.quantile(0.01)
    out["book_extremes"] = pd.DataFrame({
        "top1pct": D[D.book_return >= q_hi][["coin_return", "prev_coin", "next_coin"]].mean(),
        "bot1pct": D[D.book_return <= q_lo][["coin_return", "prev_coin", "next_coin"]].mean(),
        "all": D[["coin_return", "prev_coin", "next_coin"]].mean()}).round(5)
    return out
