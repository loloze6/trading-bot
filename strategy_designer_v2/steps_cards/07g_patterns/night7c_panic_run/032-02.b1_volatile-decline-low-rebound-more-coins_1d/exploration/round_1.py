def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            rng = (hi - lo) / c
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "dlo20": c / lo.shift(1).rolling(20).min() - 1,
                "dhi20": c / hi.shift(1).rolling(20).max() - 1,
                "rng1": rng / rng.rolling(20).mean(),
                "vol20": r1.rolling(20).std(),
                "body": (c - b["open"].astype(float)) / (hi - lo).replace(0, np.nan),
                "volu": b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean(),
                "fwd": c.shift(-H) / c - 1,
                "fc": b["forecast"].astype(float),
            })
            f["pos"] = np.arange(len(f))
            f = f[(f["pos"] % H == 0)]
            rows.append(f)
    g = pd.concat(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["dev"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["dev"] / g["coin"].map(sd)
    # standardise features per coin
    feats = ["r1", "r5", "r20", "dlo20", "dhi20", "rng1", "vol20", "body", "volu"]
    out = {}
    def summ(gr):
        def f(x):
            n = len(x)
            m = x["dev"].mean()
            t = m / (x["dev"].std() / np.sqrt(n)) if n > 2 else np.nan
            return pd.Series({"n": n, "mean_dev": m, "t": t, "mean_z": x["z"].mean()})
        return gr.apply(f)
    for ft in feats:
        x = g.dropna(subset=[ft]).copy()
        x["q"] = x.groupby("coin")[ft].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["q_" + ft] = summ(x.groupby("q"))
    out["weekday"] = summ(g.groupby("wd"))
    out["by_coin"] = summ(g.groupby("coin"))
    out["by_win"] = summ(g.groupby("win"))
    # interaction: r20 down & vol20 high quintiles
    x = g.dropna(subset=["r20", "vol20"]).copy()
    x["qr"] = x.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["qv"] = x.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["r20_x_vol20"] = summ(x.groupby(["qr", "qv"]))
    out["fc_pos_vs_zero"] = summ(g.assign(a=(g["fc"] > 0)).groupby("a"))
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, win=w))
    if tr:
        T = pd.concat(tr)
        out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                                   "median_net": T["net_profit_loss_percent"].median(),
                                   "share_win": (T["net_profit_loss_percent"] > 0).mean(),
                                   "mean_days": T["duration_minutes"].mean() / 1440})
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
