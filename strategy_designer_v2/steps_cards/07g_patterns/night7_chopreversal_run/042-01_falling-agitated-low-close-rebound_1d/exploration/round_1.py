def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in ws.items():
            b = b.copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": (h - c) / (h - l).replace(0, np.nan),
                "rng": (h - l) / c,
                "dret": c / o - 1,
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] == "unknown").values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
            })
            d["ex1"] = d["r1"] - mu
            d["ex3"] = d["r3"] - 3*mu
            d["ret5"] = c / c.shift(5) - 1
            d["rngz"] = d["rng"] / d["rng"].rolling(20, min_periods=10).mean().shift(1)
            d["day"] = d["ts"].dt.floor("D")
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["yr"] = D["ts"].dt.year
    D["wd"] = D["ts"].dt.dayofweek

    def clus(sub, y, x):
        s = sub.dropna(subset=[y, x])
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan, "days": 0})
        X = s[x] - s[x].mean(); Y = s[y]
        beta = (X*Y).sum() / (X*X).sum()
        a = Y.mean() - beta*s[x].mean()
        e = Y - a - beta*s[x]
        g = (X*e).groupby(s["day"]).sum()
        se = np.sqrt((g**2).sum()) / (X*X).sum()
        return pd.Series({"n": len(s), "slope": beta, "t": beta/se, "days": s["day"].nunique()})

    def tmean(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})

    out = {}
    D["clvq"] = pd.cut(D["clv"], [-0.01, .2, .4, .6, .8, 1.01], labels=["top", "q2", "mid", "q4", "bottom"])
    out["clv_quint_by_profile_ex1"] = D.groupby(["inprof", "clvq"])["ex1"].apply(tmean).unstack()
    out["slope_ex1_by_profile"] = D.groupby("inprof").apply(lambda s: clus(s, "ex1", "clv"))
    out["slope_ex3_by_profile"] = D.groupby("inprof").apply(lambda s: clus(s, "ex3", "clv"))
    out["slope_ex1_by_profile_year"] = D.groupby(["inprof", "yr"]).apply(lambda s: clus(s, "ex1", "clv"))
    out["slope_ex1_by_coin_in"] = D[D.inprof].groupby("coin").apply(lambda s: clus(s, "ex1", "clv"))
    out["slope_ex1_by_coin_out"] = D[~D.inprof].groupby("coin").apply(lambda s: clus(s, "ex1", "clv"))
    # day return and 5-day return
    out["slope_ex1_on_dret"] = D.groupby("inprof").apply(lambda s: clus(s, "ex1", "dret"))
    out["slope_ex1_on_ret5"] = D.groupby("inprof").apply(lambda s: clus(s, "ex1", "ret5"))
    # range size interaction among low closes
    D["rngq"] = D.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    out["clv_slope_by_rng_profile"] = D.groupby(["inprof", "rngq"]).apply(lambda s: clus(s, "ex1", "clv"))
    out["wd_ex1"] = D.groupby("wd")["ex1"].apply(tmean).unstack()
    out["wd_in_ex1"] = D[D.inprof].groupby("wd")["ex1"].apply(tmean).unstack()
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_mean_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std", "sum"])
    out["book_by_year"] = bk.groupby(pd.to_datetime(bk.index.get_level_values(1)).year).agg(["count", "mean", "sum"])
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trade_duration_days"] = (T["duration_minutes"]/1440).describe()
    return out
