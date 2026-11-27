def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = ((b["close"] - b["low"]) / rng).values
            r5 = pd.Series(c).pct_change(5).values
            r1 = pd.Series(c).pct_change(1).values
            r20 = pd.Series(c).pct_change(20).values
            vol20 = pd.Series(c).pct_change().rolling(20).std().values
            rngrel = (rng / b["close"]).values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i + H] / c[i] - 1, clv=clv[i], r5=r5[i], r1=r1[i],
                                 r20=r20[i], vol20=vol20[i], rngrel=rngrel[i], regime=b["regime"].iloc[i],
                                 wd=ts.iloc[i].dayofweek, alloc=b["postRebalance_current_allocation"].iloc[i]))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    d["clvq"] = pd.qcut(d["clv"], 5, labels=False)
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["regime_counts"] = d["regime"].value_counts()
    out["by_prof_clvq"] = d.groupby(["inprof", "clvq"]).apply(summ)
    d["r5s"] = np.sign(d["r5"])
    out["by_prof_r5sign_clvhalf"] = d.groupby(["inprof", "r5s", d["clv"] > 0.5]).apply(summ)
    d["r5q"] = pd.qcut(d["r5"], 5, labels=False)
    out["by_prof_r5q"] = d.groupby(["inprof", "r5q"]).apply(summ)
    d["r20q"] = pd.qcut(d["r20"], 5, labels=False)
    out["by_r20q_all"] = d.groupby("r20q").apply(summ)
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_volq_r1sign"] = d.groupby(["volq", np.sign(d["r1"])]).apply(summ)
    d["rngq"] = d.groupby("coin")["rngrel"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_rngq_clvhalf"] = d.groupby(["rngq", d["clv"] > 0.5]).apply(summ)
    out["by_weekday"] = d.groupby("wd").apply(summ)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book_by_window"] = dd.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_coin"] = dd.groupby("coin").agg(book=("book_return", "mean"), sumbook=("book_return", "sum"))
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    tr = pd.concat(tr)
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_dur"] = tr["duration_minutes"].describe()
    return out
