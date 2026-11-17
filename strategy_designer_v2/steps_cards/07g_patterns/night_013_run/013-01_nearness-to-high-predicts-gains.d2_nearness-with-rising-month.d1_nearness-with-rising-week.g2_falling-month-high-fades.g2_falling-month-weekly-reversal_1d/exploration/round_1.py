def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    drows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            feat = pd.DataFrame({
                "ret7": c / c.shift(7) - 1,
                "ret30": c / c.shift(30) - 1,
                "near30": c / h.rolling(30).max() - 1,
                "vol20": r1.rolling(20).std(),
                "volu": v.rolling(7).mean() / v.rolling(60, min_periods=30).mean(),
                "ret1": r1,
            })
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            idx = np.arange(0, len(df), 7)
            g = feat.iloc[idx].copy(); g["fwd7"] = fwd7.iloc[idx].values
            g["coin"] = coin; g["w"] = w
            g["forecast"] = df["forecast"].iloc[idx].values
            g["alloc"] = df["postRebalance_current_allocation"].iloc[idx].values
            rows.append(g)
            d = pd.DataFrame({"ret1": r1, "fwd1": fwd1, "vol20": feat["vol20"], "ret30": feat["ret30"],
                              "ret7": feat["ret7"], "near30": feat["near30"],
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday, "coin": coin, "w": w,
                              "year": pd.to_datetime(df["timestamp"]).dt.year})
            drows.append(d)
    G = pd.concat(rows).dropna(subset=["fwd7"])
    G["fwd7x"] = G["fwd7"] - G.groupby("coin")["fwd7"].transform("mean")
    D = pd.concat(drows).dropna(subset=["fwd1"])
    D["fwd1x"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    out = {}
    def slope(sub, x, y="fwd7x"):
        s = sub.dropna(subset=[x, y])
        if len(s) < 30: return (np.nan, np.nan, len(s))
        r = stats.linregress(s[x], s[y]); return (r.slope, r.slope / r.stderr, len(s))
    res = []
    for reg, sub in [("all", G), ("ret30<0", G[G.ret30 < 0]), ("ret30>=0", G[G.ret30 >= 0]),
                     ("hivol", G[G.vol20 > G.vol20.median()]), ("lovol", G[G.vol20 <= G.vol20.median()])]:
        for x in ["ret7", "ret30", "near30", "vol20", "volu"]:
            s, t, n = slope(sub, x); res.append([reg, x, s, t, n])
    out["grid slopes fwd7x"] = pd.DataFrame(res, columns=["regime", "x", "slope", "t", "n"])
    # per coin ret7 and near30 slope
    pc = []
    for coin, sub in G.groupby("coin"):
        for x in ["ret7", "near30", "ret30"]:
            s, t, n = slope(sub, x); pc.append([coin, x, s, t, n])
    out["per coin"] = pd.DataFrame(pc, columns=["coin", "x", "slope", "t", "n"])
    # near30 quintiles
    G["nq"] = pd.qcut(G["near30"], 5, labels=False)
    out["near30 quintile"] = G.groupby("nq")["fwd7x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # daily: weekday
    out["weekday fwd1x"] = D.groupby("wd")["fwd1x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # daily after large moves (z of ret1/vol20)
    D["z"] = D["ret1"] / D["vol20"]
    D["zq"] = pd.qcut(D["z"], 5, labels=False)
    out["after day z quintile fwd1x"] = D.groupby("zq")["fwd1x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    D["vq"] = pd.qcut(D["vol20"], 5, labels=False)
    out["by vol quintile fwd1x"] = D.groupby("vq")["fwd1x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # book daily
    B = []
    for coin in days:
        for w, dd in days[coin].items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w; B.append(x)
    B = pd.concat(B).dropna()
    out["book by coin"] = B.groupby("coin").agg(bm=("book_return", "mean"), cm=("coin_return", "mean"),
                                              corr=("book_return", lambda s: np.nan), n=("book_return", "size"))
    out["book coin corr"] = float(np.corrcoef(B.book_return, B.coin_return)[0, 1])
    return out
