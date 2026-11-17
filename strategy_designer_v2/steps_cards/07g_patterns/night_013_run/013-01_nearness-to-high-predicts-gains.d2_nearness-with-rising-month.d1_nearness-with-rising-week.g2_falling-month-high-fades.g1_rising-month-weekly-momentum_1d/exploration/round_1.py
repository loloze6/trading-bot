def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            df = pd.DataFrame({"close": c})
            df["r1"] = c.pct_change()
            df["r7"] = c / c.shift(7) - 1
            df["r30"] = c / c.shift(30) - 1
            df["hi30"] = c / b["high"].astype(float).rolling(30).max() - 1
            df["vol20"] = df["r1"].rolling(20).std()
            df["vr"] = v.rolling(7).mean() / v.rolling(60).mean()
            df["f7"] = c.shift(-7) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            df["coin"] = coin; df["win"] = w
            df["grid"] = (np.arange(len(df)) % 7 == 0)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    cm = A[A.grid].groupby("coin")["f7"].mean()
    A["f7d"] = A["f7"] - A["coin"].map(cm)
    cm1 = A.groupby("coin")["f1"].mean()
    A["f1d"] = A["f1"] - A["coin"].map(cm1)
    G = A[A.grid].dropna(subset=["f7d", "r7", "r30"])
    out = {}

    def slope(d, x):
        d = d.dropna(subset=[x, "f7d"])
        if len(d) < 30: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["f7d"])
        return (r.slope, r.slope / r.stderr, len(d))

    tab = {}
    for name, d in [("r30>0", G[G.r30 > 0]), ("r30<=0", G[G.r30 <= 0]), ("all", G)]:
        for x in ["r7", "r30", "hi30", "vol20", "vr"]:
            s, t, n = slope(d, x)
            tab[(name, x)] = {"slope": s, "t": t, "n": n}
    out["slopes_by_regime"] = pd.DataFrame(tab).T

    # quintile of r7 by regime
    G2 = G.copy()
    G2["q7"] = G2.groupby("coin")["r7"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["f7d_by_r7quint_regime"] = G2.groupby([G2.r30 > 0, "q7"])["f7d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    G2["qh"] = G2.groupby("coin")["hi30"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["f7d_by_hi30quint"] = G2.groupby("qh")["f7d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    G2["qv"] = G2.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["f7d_by_volterc_regime"] = G2.groupby(["qv", G2.r30 > 0])["f7d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    G2["qvr"] = G2.groupby("coin")["vr"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["f7d_by_volumeratio"] = G2.groupby("qvr")["f7d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["r7slope_by_coin_trending"] = pd.DataFrame({c: dict(zip(["slope", "t", "n"], slope(G[(G.coin == c) & (G.r30 > 0)], "r7"))) for c in G.coin.unique()}).T
    # weekday daily returns (all bars, 1-day non-overlap ok)
    out["f1d_by_weekday"] = A.dropna(subset=["f1d"]).groupby("wd")["f1d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # after large daily moves
    A["z1"] = A["r1"] / A["vol20"]
    A["zb"] = pd.cut(A["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["f1d_after_z1"] = A.dropna(subset=["f1d", "zb"]).groupby("zb", observed=True)["f1d"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), year=("year", "first")).dropna()
    out["book_by_year"] = bk.groupby("year").agg(book_mean=("book", "mean"), hold_mean=("hold", "mean"), n=("book", "count"))
    out["book_by_window"] = bk.groupby("win").agg(book=("book", "sum"), hold=("hold", "sum")).sort_values("book")
    return out
