def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float); v = b["volume"].astype(float)
            rng = (h - l).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "clvlow": (h - c) / rng,
                "surge": v / v.shift(1).rolling(20, min_periods=10).mean(),
                "r1": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "rngpct": (h - l) / c,
                "body": (c - o).abs() / rng,
                "vol20": (c / c.shift(1) - 1).rolling(20, min_periods=10).std(),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            rows.append(df)
    X = pd.concat(rows, ignore_index=True)
    # drift per coin, non-overlapping grids
    for hh in [1, 3, 5]:
        g = X[X["pos"] % hh == 0]
        m = g.groupby("coin")["f%d" % hh].mean()
        X["e%d" % hh] = X["f%d" % hh] - X["coin"].map(m)
        X["g%d" % hh] = X["pos"] % hh == 0
    # within-coin quintiles
    for col in ["clvlow", "surge", "r1", "r5", "r20", "rngpct", "vol20", "body"]:
        X["q_" + col] = X.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    def tab(by, hh=1, sub=None):
        d = X if sub is None else X[sub]
        d = d[d["g%d" % hh]]
        out = d.groupby(by)["e%d" % hh].agg(["mean", "count", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out[["mean", "t", "count"]].round(5)
    res = {}
    for col in ["clvlow", "surge", "r1", "r5", "r20", "rngpct", "vol20"]:
        res["e1 by q_" + col] = tab("q_" + col, 1)
    res["e3 by q_clvlow"] = tab("q_clvlow", 3)
    res["e3 by q_r1"] = tab("q_r1", 3)
    res["e5 by q_r20"] = tab("q_r20", 5)
    res["e1 clvlow x surge"] = X[X.g1].pivot_table(index="q_surge", columns="q_clvlow", values="e1", aggfunc="mean").round(4)
    res["e1 clvlow by vol20 (top q)"] = tab("q_clvlow", 1, X["q_vol20"] == 4)
    res["e1 clvlow by vol20 (bottom q)"] = tab("q_clvlow", 1, X["q_vol20"] == 0)
    res["e1 r1 x vol20"] = X[X.g1].pivot_table(index="q_vol20", columns="q_r1", values="e1", aggfunc="mean").round(4)
    res["e1 by weekday"] = tab("wd", 1)
    # position gain decomposition by allocation level
    X["gain"] = X["alloc"] * X["f1"]
    res["gain by alloc quintile"] = X.groupby(pd.qcut(X["alloc"].rank(method="first"), 5, labels=False))[["alloc", "gain", "e1"]].mean().round(5)
    # book days: largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    qq = bk["book_return"].quantile([0.02, 0.98])
    res["book extreme days"] = pd.DataFrame({
        "worst2%_book": bk[bk.book_return <= qq.iloc[0]].mean(),
        "best2%_book": bk[bk.book_return >= qq.iloc[1]].mean(),
        "all": bk.mean()}).round(5)
    res["book by window"] = bk.groupby("win")["book_return"].agg(["mean", "count"]).round(5)
    return res
