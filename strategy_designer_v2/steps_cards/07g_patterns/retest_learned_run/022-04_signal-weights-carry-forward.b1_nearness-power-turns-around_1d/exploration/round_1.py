def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 5d return over all windows' grids
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        mu = np.mean(allr) if allr else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": r1.rolling(20, min_periods=15).std(),
                "near": c / c.rolling(60, min_periods=30).max() - 1,
                "range": (b["high"] - b["low"]) / c,
                "volz": b["volume"] / b["volume"].rolling(20, min_periods=15).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1 - mu,
            })
            df = df.iloc[np.arange(0, len(df), H)]
            rows.append(df)
    g = pd.concat(rows).dropna(subset=["fwd"])
    out = {}
    def quint(col):
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = d.groupby("q")["fwd"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        z = d.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std())
        rr = stats.spearmanr(z, d["fwd"])
        t.loc["rho", "mean"] = rr[0]; t.loc["rho", "t"] = rr[0] * np.sqrt(len(d) - 2) / np.sqrt(1 - rr[0] ** 2); t.loc["rho","count"]=len(d)
        return t.round(4)
    for col in ["fc", "r1", "r5", "r20", "vol20", "near", "range", "volz"]:
        out["fwd5 by quintile of " + col] = quint(col)
    wd = g.groupby("wd")["fwd"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["fwd5 by weekday"] = wd.round(4)
    # absolute forecast: gain of position sign
    g["sgnret"] = np.sign(g["fc"]) * g["fwd"]
    d = g.copy(); d["afq"] = pd.qcut(d["fc"].abs().rank(method="first"), 5, labels=False)
    t = d.groupby("afq")["sgnret"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["signed fwd5 by |forecast| quintile"] = t.round(4)
    # per coin forecast skill
    pc = g.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "corr_fc_fwd": x["fc"].corr(x["fwd"]), "mean_sgnret": x["sgnret"].mean(), "share_long": (x["fc"] > 0).mean()}))
    out["per coin"] = pc.round(4)
    # book daily returns: by year and window, book vs coin
    dd = []
    for coin, wins in data["days"].items():
        for w, d0 in wins.items():
            x = d0.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book by year"] = dd.groupby("year")[["book_return", "coin_return"]].mean().mul(1e4).round(2)
    # largest book loss days: coin return then and prior
    dd = dd.sort_values(["coin", "win", "day"])
    dd["coin_prev5"] = dd.groupby(["coin", "win"])["coin_return"].transform(lambda s: (1 + s).rolling(5).apply(np.prod, raw=True).shift(1) - 1)
    q = dd["book_return"].quantile([0.02, 0.98])
    lo = dd[dd["book_return"] <= q.iloc[0]]; hi = dd[dd["book_return"] >= q.iloc[1]]
    out["extreme book days"] = pd.DataFrame({
        "n": [len(lo), len(hi)],
        "mean_book": [lo.book_return.mean(), hi.book_return.mean()],
        "mean_coin": [lo.coin_return.mean(), hi.coin_return.mean()],
        "share_coin_down": [(lo.coin_return < 0).mean(), (hi.coin_return < 0).mean()],
        "mean_coin_prev5": [lo.coin_prev5.mean(), hi.coin_prev5.mean()],
    }, index=["worst2%", "best2%"]).round(4)
    return out
