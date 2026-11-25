def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l)
            d = pd.DataFrame({"coin": coin, "win": w})
            d["pos"] = np.arange(len(b))
            d["cl"] = ((c - l) / rng.replace(0, np.nan))
            d["rm"] = rng / (rng / c).shift(1).rolling(20).mean() / c
            d["r1"] = c.pct_change()
            d["ret20"] = c / c.shift(20) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["vol_rel"] = d["vol20"] / d["r1"].rolling(60).std()
            d["low_dist"] = c / l.rolling(20).min() - 1
            d["hi_dist"] = c / h.rolling(20).max() - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"] = b["postRebalance_current_allocation"]
            d["fc"] = b["forecast"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f3", "f5"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    def summ(df, col, by):
        g = df.dropna(subset=[col, by]).groupby(by)[col]
        out = pd.DataFrame({"mean%": g.mean() * 100, "n": g.count()})
        out["t"] = g.mean() / (g.std() / np.sqrt(g.count()))
        return out
    D["q"] = lambda: None
    res = {}
    fall = D[D["ret20"] < 0].copy(); rise = D[D["ret20"] >= 0].copy()
    for name, df in [("fall", fall), ("rise", rise)]:
        df["clq"] = pd.qcut(df["cl"], 5, labels=False, duplicates="drop")
        df["rmq"] = pd.qcut(df["rm"], 5, labels=False, duplicates="drop")
        res[name + "_f1x_by_closeloc_q"] = summ(df, "f1x", "clq")
        res[name + "_f1x_by_rangemult_q"] = summ(df, "f1x", "rmq")
    g3 = D[D["pos"] % 3 == 0].copy()
    g3["r1q"] = pd.qcut(g3["r1"], 5, labels=False)
    res["all_f3x_by_r1_q_grid3"] = summ(g3, "f3x", "r1q")
    g3["r20q"] = pd.qcut(g3["ret20"], 5, labels=False)
    res["all_f3x_by_ret20_q_grid3"] = summ(g3, "f3x", "r20q")
    g3["vq"] = pd.qcut(g3["vol_rel"], 3, labels=False)
    res["all_f3x_by_volrel_t_grid3"] = summ(g3, "f3x", "vq")
    fv = g3[(g3["ret20"] < 0)].copy()
    fv["ldq"] = pd.qcut(fv["low_dist"], 5, labels=False, duplicates="drop")
    res["fall_f3x_by_dist_to_20d_low_q"] = summ(fv, "f3x", "ldq")
    fvv = fv[fv["vq"] == 2].copy()
    fvv["ldq"] = pd.qcut(fvv["low_dist"], 4, labels=False, duplicates="drop")
    res["fall_highvol_f3x_by_lowdist_q4"] = summ(fvv, "f3x", "ldq")
    g5 = D[D["pos"] % 5 == 0].copy()
    g5["hdq"] = pd.qcut(g5["hi_dist"], 5, labels=False, duplicates="drop")
    res["all_f5x_by_dist_to_20d_high_q"] = summ(g5, "f5x", "hdq")
    res["f1x_by_weekday"] = summ(D, "f1x", "wd")
    res["f1x_by_window"] = summ(D, "f1x", "win")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna()
    res["book_by_window"] = bk.groupby(level=0).agg(b_mean=("b", "mean"), c_mean=("c", "mean"), n=("b", "count"))
    bk = bk.reset_index()
    bk["bq"] = pd.qcut(bk["b"], 10, labels=False, duplicates="drop")
    res["book_decile_vs_coin"] = bk.groupby("bq").agg(b=("b", "mean"), c=("c", "mean"), n=("b", "count"))
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    res["book_by_weekday"] = bk.groupby("wd")["b"].agg(["mean", "count"])
    return res
