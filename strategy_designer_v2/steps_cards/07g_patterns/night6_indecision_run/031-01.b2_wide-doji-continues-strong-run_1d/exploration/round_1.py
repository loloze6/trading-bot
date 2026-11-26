def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        allg = []
        frames = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo)
            b["r5"] = c / c.shift(5) - 1
            b["r1"] = c / c.shift(1) - 1
            b["r20"] = c / c.shift(20) - 1
            b["wide"] = rng / rng.rolling(20).mean()
            b["flat"] = 1 - (c - o).abs() / rng.replace(0, np.nan)
            b["vol20"] = b["r1"].rolling(20).std()
            b["fwd"] = c.shift(-H) / c - 1
            b["pos"] = np.arange(len(b))
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b[(b["pos"] % H == 0) & b["fwd"].notna()]
            frames.append(g)
        g = pd.concat(frames)
        drift = g["fwd"].mean(); usual = g["fwd"].std()
        g = g.assign(coin=coin, unus=g["fwd"] - drift, strength=(g["fwd"] - drift) / usual,
                     volq=g.groupby("win")["vol20"].transform(lambda s: s))
        rows.append(g)
    G = pd.concat(rows)
    G["volrank"] = G.groupby("coin")["vol20"].rank(pct=True)

    def summ(df):
        if len(df) < 5:
            return pd.Series({"n": len(df), "days": df["day"].nunique() if len(df) else 0})
        d = df.groupby("day")["unus"].sum()
        nd = len(d)
        m = df["unus"].mean()
        se = np.sqrt((d**2).sum() * nd / (nd - 1)) / len(df) if nd > 1 else np.nan
        return pd.Series({"n": len(df), "days": nd, "mean_unus": m, "t": m / se,
                          "strength": df["strength"].mean(), "hit_up": (df["fwd"] > 0).mean()})

    out = {}
    G["run"] = np.where(G["r5"] > 0, "up", "down")
    G["wideb"] = pd.cut(G["wide"], [0, 1.0, 1.5, 100], labels=["narrow", "mid", "wide"])
    G["flatb"] = np.where(G["flat"] >= 0.8, "flat", "body")
    out["run_x_width_x_flat"] = G.groupby(["run", "wideb", "flatb"]).apply(summ)
    G["r5q"] = G.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["r5_quintile"] = G.groupby("r5q").apply(summ)
    G["r1q"] = G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["r1_quintile"] = G.groupby("r1q").apply(summ)
    G["r20q"] = G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["r20_quintile"] = G.groupby("r20q").apply(summ)
    G["wq"] = G.groupby("coin")["wide"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["width_quintile"] = G.groupby("wq").apply(summ)
    G["vq"] = pd.cut(G["volrank"], 5, labels=False)
    out["vol_quintile"] = G.groupby("vq").apply(summ)
    out["weekday"] = G.groupby("wd").apply(summ)
    # wide day close location: close position in range
    out["wide_day_by_r1_sign"] = G[G["wideb"] == "wide"].groupby(np.sign(G.loc[G["wideb"] == "wide", "r1"])).apply(summ)
    # book: days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_year"] = bk.groupby(pd.to_datetime(bk.index.get_level_values("day")).year).agg(["mean", "count", "std"])
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_entryforecast_q"] = T.groupby(pd.qcut(T["entry_forecast"], 3, duplicates="drop"))["net_profit_loss_percent"].agg(["count", "mean"])
    return out
