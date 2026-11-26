def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    daily = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.copy().reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5)/c - 1,
                "fwd1": c.shift(-1)/c - 1,
                "r1": r1,
                "r5": c/c.shift(5) - 1,
                "r30": c/c.shift(30) - 1,
                "r60": c/c.shift(60) - 1,
                "vol20": r1.rolling(20).std(),
                "vshock": v/v.rolling(30).mean(),
                "v30v90": v.rolling(30).mean()/v.rolling(90, min_periods=60).mean(),
                "pos30": (c - c.rolling(30).min())/(c.rolling(30).max()-c.rolling(30).min()),
                "clv": (df["close"]-df["low"])/(df["high"]-df["low"]),
                "rng": (df["high"]-df["low"])/c,
                "regime": df["regime"],
                "fc": df["forecast"],
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "pos": df.index,
            })
            f["rngz"] = f["rng"]/f["rng"].rolling(30).mean()
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["adj5"] = A["fwd5"] - A["coin"].map(drift5)
    A["adj1"] = A["fwd1"] - A["coin"].map(drift1)
    G = A[(A.pos % 5 == 0)].dropna(subset=["adj5"])
    def summ(g, col="adj5"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100*x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["by_regime"] = G.groupby("regime").apply(summ)
    def q(df, col, k=5):
        d = df.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), k, labels=False)
        return d.groupby("q").apply(summ).join(d.groupby("q")[col].median().rename("med"))
    out["r30_q_all"] = q(G, "r30")
    out["r30_q_trending"] = q(G[G.regime == "trending"], "r30", 4)
    out["r5_q_all"] = q(G, "r5")
    out["vol20_q_all"] = q(G, "vol20")
    out["vshock_q_all"] = q(G, "vshock")
    out["v30v90_q_all"] = q(G, "v30v90")
    out["pos30_q_all"] = q(G, "pos30")
    out["r60_q_all"] = q(G, "r60")
    # daily level: after big 1-day moves (all bars, next day)
    D = A.dropna(subset=["adj1"])
    out["r1_q_next1"] = q(D, "r1", 10)
    out["clv_q_next1"] = q(D, "clv", 5)
    out["weekday_next1"] = D.groupby("wd").apply(lambda g: summ(g, "adj1"))
    # falling (r60<-10%) split by vol20 above/below coin median
    med = A.groupby("coin")["vol20"].transform("median")
    G2 = G.copy(); G2["agit"] = (A.loc[G.index, "vol20"] > med.loc[G.index])
    G2["trend"] = pd.cut(G2["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["fall", "chop", "rise"])
    out["trend_x_agit"] = G2.groupby(["trend", "agit"]).apply(summ)
    # book largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(df.assign(coin=coin, win=w))
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = DD.groupby("win")["book_return"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"]*100)
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=coin))
    T = pd.concat(tr, ignore_index=True) if tr else pd.DataFrame()
    if len(T):
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
        out["trades_by_entryfc"] = T.assign(q=pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)).groupby("q")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
