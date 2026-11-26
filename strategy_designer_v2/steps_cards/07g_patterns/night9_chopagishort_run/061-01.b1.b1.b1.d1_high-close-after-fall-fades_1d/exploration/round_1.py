def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 20:
                continue
            c = b["close"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "cloc": (c - b["low"]) / rng,
                "ret5": c / c.shift(5) - 1,
                "ret1": c / c.shift(1) - 1,
                "ret60": c / c.shift(60) - 1,
                "wid": rng / c,
                "fwd5": c.shift(-5) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "inprof": (b["regime"] != "chop"),
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            d["widrel"] = d["wid"] / d["wid"].rolling(20, min_periods=10).mean().shift(1)
            d["vol20"] = d["ret1"].rolling(20, min_periods=10).std()
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    # drift per coin, non-overlapping 5-bar
    g5 = P[P.pos % 5 == 0]
    drift5 = g5.groupby("coin")["fwd5"].mean()
    g2 = P[P.pos % 2 == 0]
    drift2 = g2.groupby("coin")["fwd2"].mean()
    P["u5"] = P["fwd5"] - P["coin"].map(drift5)
    P["u2"] = P["fwd2"] - P["coin"].map(drift2)
    P["day"] = P["ts"].dt.floor("D")

    def st(df, col):
        df = df.dropna(subset=[col])
        if len(df) < 3:
            return pd.Series({"n": len(df), "mean": np.nan, "t": np.nan, "days": 0})
        dev = df[col] - df[col].mean()
        s = dev.groupby(df["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(df)
        return pd.Series({"n": len(df), "mean": df[col].mean(), "t": df[col].mean() / se if se > 0 else np.nan, "days": G})

    G5 = P[P.pos % 5 == 0].copy()
    G2 = P[P.pos % 2 == 0].copy()
    for G in (G5, G2):
        G["clq"] = pd.cut(G["cloc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1low", "q2", "q3", "q4high"])
        G["r5s"] = np.where(G["ret5"] < 0, "fall5", "rise5")
        G["prof"] = np.where(G["inprof"], "chopagi", "other")
    out = {}
    out["A_u5_by_prof_cloc_r5"] = G5.groupby(["prof", "r5s", "clq"]).apply(lambda x: st(x, "u5")).round(4)
    out["B_u2_by_prof_cloc_r5"] = G2.groupby(["prof", "r5s", "clq"]).apply(lambda x: st(x, "u2")).round(4)
    # other split by 60d trend where known
    G5["tr"] = pd.cut(G5["ret60"], [-10, -0.1, 0.1, 10], labels=["falling", "choppy", "rising"])
    o = G5[(G5.prof == "other")]
    out["C_other_trend_cloc_u5"] = o.groupby(["tr", "clq"]).apply(lambda x: st(x, "u5")).round(4)
    # in-profile by ret5 quintile and by widrel tercile
    ip = G5[G5.prof == "chopagi"].copy()
    ip["r5q"] = pd.qcut(ip["ret5"], 5, labels=False, duplicates="drop")
    out["D_in_r5quint_u5"] = ip.groupby("r5q").apply(lambda x: st(x, "u5")).round(4)
    ip["wq"] = pd.qcut(ip["widrel"], 3, labels=False, duplicates="drop")
    out["E_in_wide_cloc_u5"] = ip.groupby(["wq", "clq"]).apply(lambda x: st(x, "u5")).round(4)
    # all bars: ret1 extreme relative to vol, by profile
    G5["z1"] = G5["ret1"] / G5["vol20"]
    G5["z1q"] = pd.cut(G5["z1"], [-99, -2, -1, 1, 2, 99])
    out["F_z1_prof_u5"] = G5.groupby(["prof", "z1q"]).apply(lambda x: st(x, "u5")).round(4)
    G5["wd"] = G5["ts"].dt.dayofweek
    out["G_prof_wd_u5"] = G5[G5.prof == "chopagi"].groupby("wd").apply(lambda x: st(x, "u5")).round(4)
    # book daily
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["H_book_by_year"] = bk.groupby(bk.index.year).agg(["count", "mean", "std", "sum"]).round(5)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=False, duplicates="drop")
    out["I_trades_by_fq"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    out["I2_trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    out["J_share_inprof"] = float(P["inprof"].mean())
    return out
