def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "r1": c.pct_change(),
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "r60": c / c.shift(60) - 1,
                "vol20": lr.rolling(20).std(),
                "near30": c / b["high"].astype(float).rolling(30).max() - 1,
                "fwd5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
            })
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")

    def tab(col, q=5):
        x = g.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = x.groupby("q").agg(n=("ex5", "size"), mean_ex=("ex5", "mean"), sd=("ex5", "std"), mean_tot=("fwd5", "mean"))
        out["t"] = out["mean_ex"] / (out["sd"] / np.sqrt(out["n"]))
        return out.drop(columns="sd").round(4)

    res = {}
    for col in ["r1", "r5", "r20", "r60", "vol20", "near30"]:
        res["q_" + col] = tab(col)
    # r20 > 0 vs <= 0
    x = g.dropna(subset=["r20"])
    a, bb = x[x.r20 > 0]["ex5"], x[x.r20 <= 0]["ex5"]
    res["r20_pos_minus_neg"] = pd.Series({"n_pos": len(a), "mean_pos": a.mean(), "n_neg": len(bb), "mean_neg": bb.mean(),
                                          "welch_t": stats.ttest_ind(a, bb, equal_var=False).statistic}).round(4)
    # within r20>0: forecast>0 vs ==0
    y = x[x.r20 > 0]
    a, bb = y[y.fc > 0]["ex5"], y[y.fc <= 0]["ex5"]
    res["in_r20pos_fc_pos_minus_zero"] = pd.Series({"n_fc": len(a), "mean_fc": a.mean(), "n_0": len(bb), "mean_0": bb.mean(),
                                                    "welch_t": stats.ttest_ind(a, bb, equal_var=False).statistic}).round(4)
    # weekday
    wd = g.groupby("wd")["ex5"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["weekday"] = wd.round(4)
    # vol x r20 interaction
    z = x.dropna(subset=["vol20"]).copy()
    z["vq"] = z.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    z["rs"] = np.where(z.r20 > 0, "up", "down")
    it = z.groupby(["vq", "rs"])["ex5"].agg(["size", "mean", "std"])
    it["t"] = it["mean"] / (it["std"] / np.sqrt(it["size"]))
    res["vol_x_r20"] = it.round(4)
    # book daily: gains by window and year
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w
            dd.append(t)
    D = pd.concat(dd, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), yr=("year", "first")).dropna()
    yy = bk.groupby("yr").agg(n=("br", "size"), book=("br", "mean"), hold=("cr", "mean"))
    yy["book_sharpe"] = bk.groupby("yr")["br"].mean() / bk.groupby("yr")["br"].std() * np.sqrt(365)
    res["book_by_year"] = yy.round(5)
    return res
