def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "r7p": c / c.shift(7) - 1,
                "r1": r1,
                "vol30": r1.rolling(30).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "regime": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            df["pos"] = np.arange(len(df))
            df["vrank"] = df["vol30"].rolling(120, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # coin drift over all windows (grid)
    G = A[(A.pos % H == 0)].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean()
    usual = G.groupby("coin")["fwd"].std()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    G["z"] = G["ex"] / G["coin"].map(usual)
    G["day"] = G["ts"].dt.floor("D")
    G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G.loc[G.r60.isna(), "trend"] = np.nan

    def summ(g, col="ex"):
        d = g.groupby("day")[col].sum()
        n = len(d)
        t = d.mean() / (d.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": len(g), "days": n, "mean_ex": g[col].mean(), "t_day": t})

    out = {}
    G2 = G.dropna(subset=["r30"]).copy()
    G2["r30q"] = pd.qcut(G2.r30, 5, labels=False)
    out["r30 quintile all"] = G2.groupby("r30q").apply(summ)
    gc = G2[G2.trend == "choppy"].copy()
    gc["r30q"] = pd.qcut(gc.r30, 5, labels=False)
    out["r30 quintile choppy"] = gc.groupby("r30q").apply(summ)
    out["regime x sign r30"] = G2.groupby([G2.regime, np.sign(G2.r30)]).apply(summ)
    out["trend x sign r30"] = G2.groupby([G2.trend, np.sign(G2.r30)]).apply(summ)
    G3 = G.dropna(subset=["r7p"]).copy()
    G3["r7q"] = pd.qcut(G3.r7p, 5, labels=False)
    out["past7 quintile all"] = G3.groupby("r7q").apply(summ)
    G4 = G.dropna(subset=["vrank"]).copy()
    G4["vq"] = pd.qcut(G4.vrank, 3, labels=False, duplicates="drop")
    out["vol tercile"] = G4.groupby("vq").apply(summ)
    # 1-day: returns after large daily moves, weekday
    D = A.dropna(subset=["r1", "fwd1"]).copy()
    d1 = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D.coin.map(d1)
    D["z1"] = D["r1"] / D["vol30"]
    D["day"] = D.ts.dt.floor("D")
    Dz = D.dropna(subset=["z1"]).copy()
    Dz["zq"] = pd.cut(Dz.z1, [-99, -2, -1, 0, 1, 2, 99])
    out["next day after z move"] = Dz.groupby("zq").apply(lambda g: summ(g, "ex1"))
    out["weekday next day"] = D.groupby(D.ts.dt.dayofweek).apply(lambda g: summ(g, "ex1"))
    # book: position contribution by window
    book = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            book.append(pd.DataFrame({"coin": coin, "win": w, "br": d["book_return"].values}))
    B = pd.concat(book)
    out["book by window"] = B.groupby("win")["br"].agg(["mean", "count"])
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin, win=w))
    if T:
        T = pd.concat(T)
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"])
    return out
