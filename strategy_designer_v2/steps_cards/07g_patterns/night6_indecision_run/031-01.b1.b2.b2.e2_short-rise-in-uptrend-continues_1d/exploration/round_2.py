def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["r1"] = c.pct_change()
            d["r5"] = c / c.shift(5) - 1
            d["r20"] = c / c.shift(20) - 1
            d["r60"] = c / c.shift(60) - 1
            rng = (h - l) / c
            d["rngrel"] = rng / rng.rolling(20, min_periods=10).mean()
            d["body"] = (c - o).abs() / (h - l).replace(0, np.nan)
            d["clpos"] = (c - l) / (h - l).replace(0, np.nan)
            d["vol20"] = d["r1"].rolling(20, min_periods=10).std()
            d["volrel"] = d["vol20"] / d["r1"].rolling(60, min_periods=30).std()
            d["f3"] = c.shift(-3) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year
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
        g = df.groupby("b").agg(kmean=(key, "mean"), mean=(col, "mean"), count=(col, "count"), std=(col, "std"))
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g[["kmean", "mean", "count", "t"]].round(4)
    def slope_t(df, key, col="x3"):
        df = df.dropna(subset=[key, col])
        if len(df) < 30: return np.nan
        r = stats.linregress(df[key], df[col]); return round(r.slope / r.stderr, 2)
    up = G[G.r60 > 0]; dn = G[G.r60 <= 0]
    out["x3 by r5 quintile, r60>0"] = tab(up, "r5")
    out["x3 by r5 quintile, r60<=0"] = tab(dn, "r5")
    out["x3 by r60 quintile, all"] = tab(G, "r60")
    out["x3 by r20 quintile, all"] = tab(G, "r20")
    out["x3 by vol20 quintile"] = tab(G, "vol20")
    out["x3 by volrel quintile"] = tab(G, "volrel")
    out["x3 by rngrel quintile"] = tab(G, "rngrel")
    out["x3 by close position quintile"] = tab(G, "clpos")
    ru = G[(G.r5 > 0)].copy()
    ru["wideflat"] = ru["rngrel"] * (1 - ru["body"])
    out["x3 by wide*flat quintile, after 5d rise"] = tab(ru, "wideflat")
    rd = G[(G.r5 < 0)].copy()
    rd["wideflat"] = rd["rngrel"] * (1 - rd["body"])
    rd["x3neg"] = -rd["x3"]
    out["-x3 by wide*flat quintile, after 5d fall"] = tab(rd, "wideflat", "x3neg")
    out["x1 by r1 quintile"] = tab(P.dropna(subset=["x1"]), "r1", "x1")
    wd = P.groupby("wd")["x1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["x1 by weekday"] = wd.round(4)
    # slope t r5 in uptrend, per coin and per year
    out["slope t x3~r5 uptrend per coin"] = pd.Series({c: slope_t(g, "r5") for c, g in up.groupby("coin")})
    out["slope t x3~r5 uptrend per year"] = pd.Series({y: slope_t(g, "r5") for y, g in up.groupby("yr")})
    out["slope t x3~r5 downtrend per coin"] = pd.Series({c: slope_t(g, "r5") for c, g in dn.groupby("coin")})
    out["slope t x3~r20 all per coin"] = pd.Series({c: slope_t(g, "r20") for c, g in G.groupby("coin")})
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    out["book vs hold"] = pd.Series({"corr": bk[["book_return", "coin_return"]].corr().iloc[0, 1],
        "book_mean": bk.book_return.mean(), "hold_mean": bk.coin_return.mean(), "n": len(bk)}).round(5)
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    out["book by year"] = bk.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    # per-coin book days: largest gains/losses and the coin's state the prior day
    D["day"] = pd.to_datetime(D["day"])
    D = D.sort_values(["coin", "win", "day"])
    D["c5prev"] = D.groupby(["coin", "win"])["close"].transform(lambda s: s.shift(1) / s.shift(6) - 1)
    Db = D.dropna(subset=["book_return"])
    Db = Db[Db.book_return != 0]
    q = Db.book_return.quantile([0.05, 0.95])
    out["coin state around book extremes"] = pd.DataFrame({
        "worst5%": Db[Db.book_return <= q.iloc[0]][["coin_return", "c5prev"]].mean(),
        "best5%": Db[Db.book_return >= q.iloc[1]][["coin_return", "c5prev"]].mean(),
        "all in pos": Db[["coin_return", "c5prev"]].mean()}).round(4)
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.qcut(T["dur_d"].rank(method="first"), 5, labels=False)
    out["trades by duration quintile"] = T.groupby("db").agg(dur=("dur_d", "mean"), pl=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()), n=("dur_d", "size")).round(3)
    T["fb"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades by entry forecast quintile"] = T.groupby("fb").agg(fc=("entry_forecast", "mean"), pl=("net_profit_loss_percent", "mean"),
        n=("dur_d", "size")).round(3)
    return out
