def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            f5 = c.shift(-5) / c - 1
            p30 = c / c.shift(30) - 1
            p5 = c / c.shift(5) - 1
            p60 = c / c.shift(60) - 1
            vr = np.log(v.rolling(30).mean() / v.rolling(30).mean().shift(30))
            vr10 = np.log(v.rolling(5).mean() / v.rolling(30).mean().shift(5))
            vol20 = r1.rolling(20).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), 5)
            d = pd.DataFrame({"coin": coin, "w": w, "f5": f5.iloc[idx].values, "p30": p30.iloc[idx].values,
                              "p5": p5.iloc[idx].values, "p60": p60.iloc[idx].values, "vr": vr.iloc[idx].values,
                              "vr5": vr10.iloc[idx].values, "vol20": vol20.iloc[idx].values,
                              "r1": r1.iloc[idx].values, "rng": rng.iloc[idx].values, "clpos": clpos.iloc[idx].values,
                              "regime": b["regime"].iloc[idx].values, "wd": ts.iloc[idx].dt.weekday.values,
                              "yr": ts.iloc[idx].dt.year.values, "day": ts.iloc[idx].dt.floor("D").values})
            rows.append(d)
            dd = pd.DataFrame({"r1n": r1.shift(-1).values, "r1": r1.values, "wd": ts.dt.weekday.values,
                               "regime": b["regime"].values, "coin": coin})
            daily.append(dd)
    G = pd.concat(rows).dropna(subset=["f5"])
    D = pd.concat(daily).dropna(subset=["r1n"])
    drift = G["f5"].mean(); sd = G["f5"].std()
    G["u"] = G["f5"] - drift
    out = {"drift_sd_n": pd.Series({"drift": drift, "sd": sd, "n": len(G)})}
    def summ(g):
        return pd.Series({"n": len(g), "mean_u": g["u"].mean(), "t": g["u"].mean() / (g["u"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out["by_regime"] = G.groupby("regime").apply(summ)
    out["by_year"] = G.groupby("yr").apply(summ)
    for col in ["p30", "p5", "vr", "vr5", "vol20", "r1", "rng", "clpos", "p60"]:
        g = G.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        out["q_" + col] = g.groupby("q").apply(summ)
        # within chop (outside falling calm)
        gc = g[g["regime"] == "chop"]
        gm = g[g["regime"] != "chop"]
        out["corr_" + col] = pd.Series({
            "all_rho": stats.spearmanr(g[col], g["u"])[0], "all_n": len(g),
            "chop_rho": stats.spearmanr(gc[col], gc["u"])[0] if len(gc) > 10 else np.nan, "chop_n": len(gc),
            "fc_rho": stats.spearmanr(gm[col], gm["u"])[0] if len(gm) > 10 else np.nan, "fc_n": len(gm)})
    # trend by p60 sign buckets and vr interaction
    g = G.dropna(subset=["p60", "vr"]).copy()
    g["trend"] = np.where(g["p60"] > 0.1, "rising", np.where(g["p60"] < -0.1, "falling", "choppy"))
    g["vrq"] = pd.qcut(g["vr"], 3, labels=["shrink", "mid", "grow"])
    out["trend_x_vr"] = g.groupby(["trend", "vrq"]).apply(summ)
    out["weekday_next_day"] = D.groupby("wd")["r1n"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk).dropna(subset=["book_return"])
    bd = B.groupby(["w", "day"])[["book_return", "coin_return"]].mean()
    out["book_by_window"] = bd.groupby(level=0).agg(["mean", "count"])
    big = bd.sort_values("book_return")
    out["book_worst10_coin"] = big.head(10)[["book_return", "coin_return"]].reset_index(drop=True)
    out["book_best10_coin"] = big.tail(10)[["book_return", "coin_return"]].reset_index(drop=True)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
