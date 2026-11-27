def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            vol30 = r1.rolling(30).std()
            volrank = vol30 / vol30.expanding(30).median()
            f10 = c.shift(-10) / c - 1
            f1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "r5": r5, "r30": r30, "r60": r60,
                               "volrank": volrank, "f10": f10, "f1": f1, "regime": b["regime"], "fc": b["forecast"],
                               "alloc": b["postRebalance_current_allocation"], "rng": rng, "clpos": clpos,
                               "wd": ts.dt.weekday, "year": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift10 = d.loc[d.pos % 10 == 0].groupby("coin")["f10"].mean()
    d["u10"] = d["f10"] - d["coin"].map(drift10)
    g = d[(d.pos % 10 == 0)].dropna(subset=["f10", "r30", "r60"]).copy()
    g["trend"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    g["agit"] = np.where(g.regime == "unknown", "chopagit_reg", "other")
    g["r30q"] = g.groupby("trend")["r30"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    def summ(x):
        return pd.Series({"n": len(x), "mean_u10": x.u10.mean(), "t": stats.ttest_1samp(x.u10, 0).statistic if len(x) > 2 else np.nan,
                          "corr_r30": x[["r30", "u10"]].corr().iloc[0, 1] if len(x) > 3 else np.nan})
    out = {}
    out["by_trend_r30q"] = g.groupby(["trend", "r30q"]).apply(summ)
    out["by_trend_corr"] = g.groupby(["trend", "agit"]).apply(summ)
    g["r5q"] = pd.qcut(g.r5, 5, labels=False)
    out["by_r5q"] = g.groupby("r5q").apply(summ)
    g["vq"] = pd.qcut(g.volrank, 4, labels=False, duplicates="drop")
    out["by_volq_trend"] = g.groupby(["vq", "trend"]).apply(summ)
    # daily next-day: after large moves, by close position
    dd = d.dropna(subset=["f1", "r1"]).copy()
    dd["z"] = dd.r1 / dd.groupby("coin").r1.transform("std")
    dd["zq"] = pd.qcut(dd.z, 10, labels=False)
    out["next_day_by_zdecile"] = dd.groupby("zq").agg(n=("f1", "size"), mean_f1=("f1", "mean"), t=("f1", lambda x: stats.ttest_1samp(x, 0).statistic))
    out["next_day_by_weekday"] = dd.groupby("wd").agg(n=("f1", "size"), mean_f1=("f1", "mean"), t=("f1", lambda x: stats.ttest_1samp(x, 0).statistic))
    dd["cq"] = pd.qcut(dd.clpos, 5, labels=False, duplicates="drop")
    out["next_day_by_closepos"] = dd.groupby("cq").agg(n=("f1", "size"), mean_f1=("f1", "mean"), t=("f1", lambda x: stats.ttest_1samp(x, 0).statistic))
    # book
    dys = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dys.append(x)
    D = pd.concat(dys, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"),
                                                 med=("net_profit_loss_percent", "median"), dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    out["regime_share"] = d.regime.value_counts(normalize=True)
    return out
