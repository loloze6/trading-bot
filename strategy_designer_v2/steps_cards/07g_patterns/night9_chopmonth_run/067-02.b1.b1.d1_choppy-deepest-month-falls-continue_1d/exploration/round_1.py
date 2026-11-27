def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "r7p": c / c.shift(7) - 1,
                "r1": r1,
                "vol30": r1.rolling(30).std(),
                "vol120": r1.rolling(120, min_periods=60).std(),
                "f7": c.shift(-7) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d[d.pos % 7 == 0].groupby("coin")["f7"].mean()
    d["drift"] = d.coin.map(drift)
    d["u7"] = d.f7 - d.drift
    d["year"] = d.ts.dt.year
    d["agit"] = d.vol30 > d.vol120
    d["trend"] = np.where(d.r60 > 0.10, "rising", np.where(d.r60 < -0.10, "falling", "choppy"))
    g = d[(d.pos % 7 == 0)].dropna(subset=["f7", "r30", "r60"]).copy()
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # r30 quintile by trend: unusual 7d return
    g["q30"] = g.groupby("trend")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["u7_by_trend_q30"] = g.groupby(["trend", "q30"])["u7"].apply(tt).unstack()
    out["u7_by_trend_agit_q30_extremes"] = g[g.q30.isin([0, 4])].groupby(["trend", "agit", "q30"])["u7"].apply(tt).unstack()
    # rank correlation r30 vs u7 by trend x agit
    def sp(x):
        r, p = stats.spearmanr(x.r30, x.u7)
        return pd.Series({"n": len(x), "rho": r, "p": p})
    out["spearman_r30_u7_trend_agit"] = g.groupby(["trend", "agit"]).apply(sp)
    # 7-day past return quintile, all
    g["q7p"] = pd.qcut(g.r7p, 5, labels=False)
    out["u7_by_q7p_trend"] = g.groupby(["trend", "q7p"])["u7"].apply(tt).unstack()
    # vol level
    g["qv"] = pd.qcut(g.vol30 / g.vol120, 5, labels=False)
    out["u7_by_volratio"] = g.groupby("qv")["u7"].apply(tt).unstack()
    # weekday of grid day
    g["wd"] = g.ts.dt.weekday
    out["u7_by_weekday"] = g.groupby("wd")["u7"].apply(tt).unstack()
    out["u7_by_year_choppy_low_q30"] = g[(g.trend == "choppy") & (g.q30 == 0)].groupby("year")["u7"].apply(tt).unstack()
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["absf"] = tr.entry_forecast.abs()
    tr["qf"] = pd.qcut(tr.absf.rank(method="first"), 3, labels=False)
    out["trades_by_forecast_tercile"] = tr.groupby(["side", "qf"])["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_duration_days"] = (tr.duration_minutes / 1440).describe()
    return out
