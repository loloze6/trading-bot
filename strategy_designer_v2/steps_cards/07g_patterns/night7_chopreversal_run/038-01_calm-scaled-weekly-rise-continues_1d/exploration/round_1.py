def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            s7 = r7 / (sd30 * np.sqrt(7))
            r1s = r1 / sd30
            r3 = c / c.shift(3) - 1
            s3 = r3 / (sd30 * np.sqrt(3))
            r30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "s7": s7, "s3": s3, "r1s": r1s, "r30": r30,
                               "fwd": fwd, "regime": b["regime"].astype(str),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "sd30": sd30,
                               "alloc": b["postRebalance_current_allocation"]})
            df = df.iloc[::H]
            rows.append(df)
    g = pd.concat(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    g["u"] = g["fwd"] - g["coin"].map(drift)
    g["calm"] = np.where(g["regime"] == "chop", "agitated", "calm")
    out = {}
    out["regime counts"] = g["regime"].value_counts()

    def reg(sub, x):
        sub = sub.dropna(subset=[x, "u"])
        if len(sub) < 30: return pd.Series({"n": len(sub)})
        sl = stats.linregress(sub[x], sub["u"])
        return pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr, "corr": sl.rvalue})

    res = {}
    for prof in ["calm", "agitated"]:
        s = g[g["calm"] == prof]
        for x in ["s7", "s3", "r1s"]:
            res[(prof, x, "all")] = reg(s, x)
            res[(prof, x, "pos")] = reg(s[s[x] > 0], x)
            res[(prof, x, "neg")] = reg(s[s[x] < 0], x)
    out["slopes of unusual 5d move on scaled moves"] = pd.DataFrame(res).T

    g["s7q"] = pd.qcut(g["s7"], 5, labels=False)
    out["unusual 5d by s7 quintile and profile"] = g.groupby(["calm", "s7q"])["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    g["r1q"] = pd.qcut(g["r1s"], 5, labels=False)
    out["unusual 5d by 1d scaled move quintile and profile"] = g.groupby(["calm", "r1q"])["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    g["trend"] = np.where(g["r30"] > 0.1, "up", np.where(g["r30"] < -0.1, "down", "flat"))
    out["unusual 5d by 30d trend and profile"] = g.groupby(["calm", "trend"])["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    g["volq"] = g.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["unusual 5d by own vol tercile"] = g.groupby("volq")["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["by year: calm s7>0 slope"] = pd.DataFrame({y: reg(s[(s["calm"] == "calm") & (s["s7"] > 0)], "s7") for y, s in g.groupby("year")}).T
    out["by coin: calm s7 all slope"] = pd.DataFrame({k: reg(s[s["calm"] == "calm"], "s7") for k, s in g.groupby("coin")}).T

    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    out["book by weekday"] = D.groupby("wd")["book_return"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["book by window"] = D.groupby("w")["book_return"].agg(["count", "mean", "std"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["efq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("efq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
