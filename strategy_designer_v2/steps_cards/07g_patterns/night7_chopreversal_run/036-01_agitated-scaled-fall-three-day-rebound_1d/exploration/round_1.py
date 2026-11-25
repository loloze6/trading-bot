def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "r": r, "z": z, "sd": sd,
                "f1": c.shift(-1)/c - 1, "f3": c.shift(-3)/c - 1,
                "f23": c.shift(-3)/c.shift(-1) - 1,
                "r5": c/c.shift(5) - 1, "r20": c/c.shift(20) - 1,
                "rng": (b["high"]-b["low"])/c/sd,
                "clv": (c - b["low"])/(b["high"]-b["low"]).replace(0, np.nan),
                "agit": (b["regime"] != "chop"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # coin drift
    g3 = d[d["pos"] % 3 == 0].dropna(subset=["f3"])
    drift3 = g3.groupby("coin")["f3"].mean()
    d["x3"] = d["f3"] - d["coin"].map(drift3)
    d["x1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    g = d[(d["pos"] % 3 == 0)].dropna(subset=["x3", "z"]).copy()
    g["zq"] = pd.qcut(g["z"], 7, labels=False)
    def summ(x, col):
        return pd.Series({"n": len(x), "mean%": 100*x[col].mean(),
                          "t": stats.ttest_1samp(x[col], 0).statistic if len(x) > 2 else np.nan})
    out["x3 by z septile x agitated"] = g.groupby(["agit", "zq"]).apply(lambda x: summ(x, "x3")).reset_index()
    out["z septile edges"] = pd.Series(pd.qcut(g["z"], 7, retbins=True)[1]).round(2)
    g["rq"] = pd.qcut(g["rng"], 5, labels=False)
    out["x3 by range/sd quintile"] = g.groupby("rq").apply(lambda x: summ(x, "x3"))
    g["cq"] = pd.qcut(g["clv"], 5, labels=False)
    out["x3 by close location quintile"] = g.groupby("cq").apply(lambda x: summ(x, "x3"))
    g["q5"] = pd.qcut(g["r5"]/g["sd"], 5, labels=False)
    out["x3 by 5d ret/sd quintile"] = g.groupby("q5").apply(lambda x: summ(x, "x3"))
    g["q20"] = pd.qcut(g["r20"]/g["sd"], 5, labels=False)
    out["x3 by 20d ret/sd quintile"] = g.groupby("q20").apply(lambda x: summ(x, "x3"))
    g["sq"] = pd.qcut(g["sd"], 5, labels=False)
    out["x3 by vol level quintile"] = g.groupby("sq").apply(lambda x: summ(x, "x3"))
    d1 = d.dropna(subset=["x1"])
    out["next-day x1 by weekday of signal bar"] = d1.groupby("wd").apply(lambda x: summ(x, "x1"))
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"]).round(5)
    q = bk["book_return"].quantile([0.05, 0.95])
    out["coin ret on book worst/best 5% days"] = pd.Series({
        "worst_book": bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(),
        "worst_coin": bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean(),
        "best_book": bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(),
        "best_coin": bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean()})
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = tr.groupby("fq").agg(
        n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"),
        fc=("entry_forecast", "mean"), dur_d=("duration_minutes", lambda s: s.mean()/1440))
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
