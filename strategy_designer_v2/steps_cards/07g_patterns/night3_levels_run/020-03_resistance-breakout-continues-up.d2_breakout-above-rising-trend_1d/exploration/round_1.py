def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": c.pct_change(), "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "r60p": c / c.shift(60) - 1,
                "dist50": c / c.rolling(50, min_periods=50).mean() - 1,
                "hi20": c / c.rolling(20).max() - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "trend": (b["regime"] == "trending").astype(int),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            f["rng"] = (b["high"] - b["low"]) / c
            f["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f = f[f["pos"] % 5 == 0]
            recs.append(f)
        cf = pd.concat(recs)
        drift = cf["fwd5"].mean()
        cf["ex"] = cf["fwd5"] - drift
        cf["usual"] = cf["fwd5"].std()
        cf["str"] = cf["ex"] / cf["usual"]
        for col in ["r1", "r5p", "r20p", "r60p", "dist50", "vol20", "rng", "clv", "hi20"]:
            cf["q_" + col] = pd.qcut(cf[col].rank(method="first"), 5, labels=False)
        rows.append(cf)
    A = pd.concat(rows).dropna(subset=["ex"])

    def g(df, key):
        out = df.groupby(key)["ex"].agg(["mean", "count", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["str"] = df.groupby(key)["str"].mean()
        return out[["mean", "t", "count", "str"]].round(4)

    res = {}
    for col in ["r1", "r5p", "r20p", "r60p", "dist50", "vol20", "rng", "clv", "hi20"]:
        res["q_" + col] = g(A, "q_" + col)
    res["weekday"] = g(A, "wd")
    res["year"] = g(A, "yr")
    res["trend_flag"] = g(A, "trend")
    pos = A[A["dist50"] > 0]
    res["dist50pos_q_by_trend"] = pos.groupby(["q_dist50", "trend"])["ex"].agg(["mean", "count"]).round(4)
    res["coin"] = g(A, "coin")
    res["vol_x_r20"] = A.groupby(["q_vol20", "q_r20p"])["ex"].mean().unstack().round(4)
    res["dist_x_vol"] = A.groupby(["q_dist50", "q_vol20"])["ex"].mean().unstack().round(4)

    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy().reset_index(drop=True)
            d["coin"] = coin
            d["c5p"] = d["close"] / d["close"].shift(5) - 1
            d["c20p"] = d["close"] / d["close"].shift(20) - 1
            D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    act = D[D["book_return"].abs() > 1e-9]
    lo, hi = act["book_return"].quantile([0.05, 0.95])
    act = act.assign(tail=np.where(act["book_return"] <= lo, "worst5", np.where(act["book_return"] >= hi, "best5", "mid")))
    res["book_tails"] = act.groupby("tail")[["book_return", "coin_return", "c5p", "c20p"]].mean().round(4)
    res["book_tails_n"] = act.groupby("tail").size()

    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    res["trades_by_fq"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    res["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return res
