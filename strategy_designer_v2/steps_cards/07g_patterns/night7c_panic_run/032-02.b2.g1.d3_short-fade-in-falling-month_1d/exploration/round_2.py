def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(b))
            d["cl"] = (c - l) / rng.replace(0, np.nan)
            rr = rng / c
            d["rm"] = rr / rr.shift(1).rolling(20).mean()
            d["r1"] = c.pct_change()
            d["ret20"] = c / c.shift(20) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["vol_rel"] = d["vol20"] / d["r1"].rolling(60).std()
            d["low_dist"] = c / l.rolling(20).min() - 1
            d["newlow"] = (l <= l.rolling(30).min()).astype(float)
            d["hi_dist"] = c / h.rolling(20).max() - 1
            for k in [1, 3, 5]:
                d["f%d" % k] = c.shift(-k) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["fc"] = b["forecast"].astype(float)
            d["gain"] = d["alloc"] * d["f1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f3", "f5"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")

    def summ(df, col, by):
        g = df.dropna(subset=[col, by]).groupby(by)[col]
        out = pd.DataFrame({"mean%": g.mean() * 100, "n": g.count()})
        out["t"] = g.mean() / (g.std() / np.sqrt(g.count()))
        return out

    res = {}
    fall = D[D["ret20"] < 0].copy()
    fall["clq"] = pd.qcut(fall["cl"], 5, labels=False, duplicates="drop")
    fall["rmq"] = pd.qcut(fall["rm"], 5, labels=False, duplicates="drop")
    res["fall_f1x_by_closeloc_q"] = summ(fall, "f1x", "clq")
    res["fall_f1x_by_rangemult_q"] = summ(fall, "f1x", "rmq")
    fall["r1q"] = pd.qcut(fall["r1"], 5, labels=False, duplicates="drop")
    res["fall_f1x_by_r1_q"] = summ(fall, "f1x", "r1q")
    res["fall_f1x_short_gain_by_window"] = summ(fall.assign(s=-fall["f1x"]), "s", "win")

    g3 = D[D["pos"] % 3 == 0].copy()
    g3["r1q"] = pd.qcut(g3["r1"], 5, labels=False, duplicates="drop")
    res["all_f3x_by_r1_q"] = summ(g3, "f3x", "r1q")
    g3["r20q"] = pd.qcut(g3["ret20"], 5, labels=False, duplicates="drop")
    res["all_f3x_by_ret20_q"] = summ(g3, "f3x", "r20q")
    g3["vq"] = pd.qcut(g3["vol_rel"], 3, labels=False, duplicates="drop")
    res["all_f3x_by_volrel_t"] = summ(g3, "f3x", "vq")
    fv = g3[g3["ret20"] < 0].copy()
    fv["ldq"] = pd.qcut(fv["low_dist"], 5, labels=False, duplicates="drop")
    res["fall_f3x_by_lowdist_q"] = summ(fv, "f3x", "ldq")
    fvv = fv[fv["vq"] == 2].copy()
    res["fall_highvol_f3x_by_newlow30"] = summ(fvv, "f3x", "newlow")
    g5 = D[D["pos"] % 5 == 0].copy()
    g5["hdq"] = pd.qcut(g5["hi_dist"], 5, labels=False, duplicates="drop")
    res["all_f5x_by_dist_20d_high_q"] = summ(g5, "f5x", "hdq")
    g5["r20q"] = pd.qcut(g5["ret20"], 5, labels=False, duplicates="drop")
    res["all_f5x_by_ret20_q"] = summ(g5, "f5x", "r20q")
    fv5 = g5[g5["ret20"] < 0].copy()
    res["fall_f5x_by_newlow30"] = summ(fv5, "f5x", "newlow")
    res["f1x_by_weekday"] = summ(D, "f1x", "wd")

    # positions / forecast
    act = D[D["fc"] < 0].copy()
    act["fq"] = pd.qcut(act["fc"], 5, labels=False, duplicates="drop")
    res["active_gain_by_fc_q_(0=most_short)"] = summ(act, "gain", "fq")
    res["active_gain_by_coin"] = summ(act, "gain", "coin")

    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    if tr:
        T = pd.concat(tr, ignore_index=True)
        T["dur_d"] = T["duration_minutes"] / 1440.0
        T["dq"] = pd.qcut(T["dur_d"], 4, labels=False, duplicates="drop")
        res["trades_net_by_duration_q"] = T.groupby("dq").agg(dur=("dur_d", "mean"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"), n=("dur_d", "count"))
        res["trades_overall"] = pd.Series({"n": len(T), "gross_mean": T["profit_loss_percent"].mean(), "net_mean": T["net_profit_loss_percent"].mean(), "dur_mean_d": T["dur_d"].mean()})

    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna().reset_index()
    res["book_by_window"] = bk.groupby("win").agg(b_mean=("b", "mean"), c_mean=("c", "mean"), n=("b", "count"))
    bk["bq"] = pd.qcut(bk["b"], 10, labels=False, duplicates="drop")
    res["book_decile_vs_coin"] = bk.groupby("bq").agg(b=("b", "mean"), c=("c", "mean"), n=("b", "count"))
    bk = bk.sort_values(["win", "day"])
    bk["c_prev"] = bk.groupby("win")["c"].shift(1)
    bk["c_next"] = bk.groupby("win")["c"].shift(-1)
    res["around_book_extremes"] = bk.groupby("bq")[["c_prev", "c", "c_next"]].mean()
    return res
