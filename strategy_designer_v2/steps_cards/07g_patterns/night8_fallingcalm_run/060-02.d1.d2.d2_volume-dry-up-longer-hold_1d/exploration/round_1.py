def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    rows = []
    trows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            m30 = v.rolling(30).mean(); vr = np.log(m30 / m30.shift(30))
            vr10 = np.log(v.rolling(10).mean() / v.rolling(30).mean().shift(10))
            sd20 = r1.rolling(20).std()
            sdrat = np.log(sd20 / r1.rolling(60).std())
            rng = (b["high"] - b["low"]) / c
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "ret20": ret20, "ret60": ret60,
                               "ret5": ret5, "vr": vr, "vr10": vr10, "sdrat": sdrat, "r1": r1, "rng": rng,
                               "fwd": fwd, "fwd1": fwd1, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = grid.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift); grid["ex"] = grid["fwd"] - grid["coin"].map(drift)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["drift20"] = drift
    # forecast buckets in situation on grid
    g = grid[grid["fc"] != 0].copy()
    g["side"] = np.sign(g["fc"])
    out["situation_by_side"] = g.groupby("side")["ex"].apply(tt).unstack()
    g["fq"] = pd.qcut(g["fc"], 4, labels=False, duplicates="drop")
    out["situation_fc_quartile"] = g.groupby("fq")["ex"].apply(tt).unstack()
    # vr in all bars by trend
    gg = grid.dropna(subset=["vr", "ret60"]).copy()
    gg["trend"] = np.where(gg["ret60"] > .1, "rising", np.where(gg["ret60"] < -.1, "falling", "choppy"))
    gg["vrq"] = gg.groupby("trend")["vr"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vr_tercile_by_trend"] = gg.groupby(["trend", "vrq"])["ex"].apply(tt).unstack()
    out["corr_vr_ex_by_trend"] = gg.groupby("trend").apply(lambda d: pd.Series({"n": len(d), "rho": stats.spearmanr(d["vr"], d["ex"])[0]}))
    # ret20 tercile in all bars
    g2 = grid.dropna(subset=["ret20"]).copy()
    g2["q"] = pd.qcut(g2["ret20"], 5, labels=False)
    out["ret20_quintile"] = g2.groupby("q")["ex"].apply(tt).unstack()
    g3 = grid.dropna(subset=["sdrat"]).copy()
    g3["q"] = pd.qcut(g3["sdrat"], 5, labels=False)
    out["volratio20_60_quintile"] = g3.groupby("q")["ex"].apply(tt).unstack()
    # 1-day: weekday, after large moves (all bars, 1-day non-overlapping trivially)
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out["weekday_next1"] = A.groupby("wd")["ex1"].apply(tt).unstack()
    A["r1q"] = pd.qcut(A["r1"], 5, labels=False)
    out["after_r1_quintile_next1"] = A.groupby("r1q")["ex1"].apply(tt).unstack()
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0)["book_return"].agg(["count", "mean", "sum"])
    q = bk["book_return"].quantile([.02, .98])
    out["book_extremes"] = pd.DataFrame({"n_low": [(bk.book_return <= q.iloc[0]).sum()],
        "sum_low": [bk.book_return[bk.book_return <= q.iloc[0]].sum()],
        "sum_high": [bk.book_return[bk.book_return >= q.iloc[1]].sum()],
        "total": [bk.book_return.sum()],
        "coin_ret_on_low": [bk.coin_return[bk.book_return <= q.iloc[0]].mean()],
        "coin_ret_on_high": [bk.coin_return[bk.book_return >= q.iloc[1]].mean()]})
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_coin_side"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "mean"]).unstack()
    return out
