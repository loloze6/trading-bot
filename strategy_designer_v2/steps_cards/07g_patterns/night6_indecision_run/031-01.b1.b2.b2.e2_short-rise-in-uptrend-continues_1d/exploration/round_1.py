def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w})
            d["r1"] = c.pct_change()
            d["r5"] = c / c.shift(5) - 1
            d["r20"] = c / c.shift(20) - 1
            d["r60"] = c / c.shift(60) - 1
            rng = (h - l) / c
            d["rngrel"] = rng / rng.rolling(20, min_periods=10).mean()
            d["body"] = (c - o).abs() / (h - l).replace(0, np.nan)
            d["clpos"] = (c - l) / (h - l).replace(0, np.nan)
            d["vol20"] = d["r1"].rolling(20, min_periods=10).std()
            d["f3"] = c.shift(-3) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["fc"] = b["forecast"].astype(float)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["pos"] = np.arange(len(d))
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    drift3 = P[P.pos % 3 == 0].groupby("coin")["f3"].mean()
    drift1 = P.groupby("coin")["f1"].mean()
    P["x3"] = P["f3"] - P["coin"].map(drift3)
    P["x1"] = P["f1"] - P["coin"].map(drift1)
    G = P[(P.pos % 3 == 0)].dropna(subset=["x3"])
    out = {}
    def tab(df, key, col="x3", q=5):
        df = df.dropna(subset=[key, col]).copy()
        df["b"] = df.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = df.groupby("b")[col].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g[["mean", "count", "t"]].round(4)
    up = G[G.r60 > 0]; dn = G[G.r60 <= 0]
    out["x3 by r5 quintile, r60>0"] = tab(up, "r5")
    out["x3 by r5 quintile, r60<=0"] = tab(dn, "r5")
    out["x3 by r60 quintile, all"] = tab(G, "r60")
    out["x3 by r20 quintile, all"] = tab(G, "r20")
    out["x3 by vol20 quintile"] = tab(G, "vol20")
    out["x3 by rngrel quintile"] = tab(G, "rngrel")
    out["x3 by close position quintile"] = tab(G, "clpos")
    # brief: wide flat day after a run up (r5>0)
    ru = G[(G.r5 > 0)].copy()
    ru["wideflat"] = ru["rngrel"] * (1 - ru["body"])
    out["x3 by wide*flat quintile, after 5d rise"] = tab(ru, "wideflat")
    # after large daily moves: signed
    out["x1 by r1 quintile"] = tab(P.dropna(subset=["x1"]), "r1", "x1")
    out["x1 by weekday"] = P.groupby("wd")["x1"].agg(["mean", "count"]).assign(
        t=lambda g: g["mean"] / (P.groupby("wd")["x1"].std() / np.sqrt(g["count"]))).round(4)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w; D.append(dd)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book vs hold daily corr, mean"] = pd.Series({
        "corr": bk.corr().iloc[0, 1], "book_mean": bk.book_return.mean(), "hold_mean": bk.coin_return.mean(),
        "n": len(bk)}).round(5)
    # book by year
    bk2 = bk.reset_index(); bk2["yr"] = pd.to_datetime(bk2["day"]).dt.year
    out["book by year"] = bk2.groupby("yr")[["book_return", "coin_return"]].agg(["mean"]).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.qcut(T["dur_d"].rank(method="first"), 5, labels=False)
    out["trades by duration quintile"] = T.groupby("db").agg(dur=("dur_d", "mean"), pl=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()), n=("dur_d", "size")).round(3)
    return out
