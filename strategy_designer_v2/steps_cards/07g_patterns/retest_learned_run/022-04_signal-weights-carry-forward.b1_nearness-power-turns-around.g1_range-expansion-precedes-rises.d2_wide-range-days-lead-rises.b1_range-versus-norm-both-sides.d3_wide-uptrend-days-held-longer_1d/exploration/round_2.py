def explore(data):
    import numpy as np, pandas as pd
    H = 6
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]) / c
            b["rr"] = rng / rng.rolling(30, min_periods=20).mean()
            b["ret30"] = c / c.shift(30) - 1
            b["ret1"] = c / c.shift(1) - 1
            b["ret7"] = c / c.shift(7) - 1
            hh = b["high"].rolling(30, min_periods=20).max()
            b["near_hi"] = c / hh - 1
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["fwd"] = c.shift(-H) / c - 1
            g = b.iloc[::H].copy()
            g["coin"] = coin; g["win"] = w
            g["year"] = pd.to_datetime(g["timestamp"]).dt.year
            g["ts"] = pd.to_datetime(g["timestamp"])
            rows.append(g)
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["z"] = G["ex"] / G.groupby("coin")["fwd"].transform("std")
    res = {}

    def tt(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})

    def clustered(df):
        # one value per date: mean z across coins on that date (removes cross-coin dependence)
        s = df.groupby("ts")["z"].mean()
        return tt(s)

    up = G[G["ret30"] > 0].copy()
    up["q"] = pd.qcut(up["rr"], 5, labels=False)
    top = up[up["q"] == 4]
    # finer grading inside the top range quintile of the uptrend
    top = top.copy(); top["q2"] = pd.qcut(top["rr"], 3, labels=False)
    res["up_toprange_tercile"] = top.groupby("q2").apply(lambda d: tt(d["z"])).round(3)
    res["up_toprange_clustered"] = clustered(top).round(3)
    res["up_toprange_by_year"] = top.groupby("year").apply(lambda d: tt(d["z"])).round(3)
    # direction of the wide day: close location inside the wide day
    top["clvh"] = np.where(top["clv"] >= 0.5, "closeHigh", "closeLow")
    res["up_toprange_by_clv"] = top.groupby("clvh").apply(lambda d: tt(d["z"])).round(3)
    top["r1s"] = np.where(top["ret1"] > 0, "upday", "downday")
    res["up_toprange_by_ret1sign"] = top.groupby("r1s").apply(lambda d: tt(d["z"])).round(3)
    # wide days in all regimes split by day direction
    G["rq"] = pd.qcut(G["rr"], 5, labels=False)
    W = G[G["rq"] == 4].copy()
    W["r1s"] = np.where(W["ret1"] > 0, "upday", "downday")
    W["trend"] = np.where(W["ret30"] > 0, "up30", "dn30")
    res["wide_all_by_dir_trend"] = W.groupby(["trend", "r1s"]).apply(lambda d: tt(d["z"])).round(3)
    # near high and ret7 top quintile: clustered and by year
    for col in ["near_hi", "ret7"]:
        G["q"] = pd.qcut(G[col], 5, labels=False)
        T = G[G["q"] == 4]
        res[f"{col}_top_clustered"] = clustered(T).round(3)
        res[f"{col}_top_by_year"] = T.groupby("year").apply(lambda d: tt(d["z"])).round(3)
        res[f"{col}_top_by_coin"] = T.groupby("coin").apply(lambda d: tt(d["z"])).round(3)
    # near_hi graded within top half
    G["nq10"] = pd.qcut(G["near_hi"], 10, labels=False)
    res["near_hi_deciles"] = G.groupby("nq10").apply(lambda d: tt(d["z"])).round(3)
    # overlap: near_hi top vs range top
    G["nh_top"] = G["near_hi"] >= G["near_hi"].quantile(0.8)
    G["rr_top"] = G["rq"] == 4
    res["nearhi_x_range"] = G.groupby(["nh_top", "rr_top"]).apply(lambda d: tt(d["z"])).round(3)
    return res
