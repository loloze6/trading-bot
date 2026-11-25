def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "rng1": rng,
                "rngratio": rng.rolling(10).mean() / rng.rolling(60, min_periods=40).mean(),
                "low30": (c <= c.rolling(30).min()).astype(float).where(c.rolling(30).count() == 30),
                "lowdist20": c / c.rolling(20).min() - 1,
                "highdist20": c / c.rolling(20).max() - 1,
                "closepos": (c - lo) / (hi - lo).replace(0, np.nan),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "regime": b["regime"],
                "fc": b["forecast"],
            })
            df = df.iloc[::H]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    out = {}
    def summ(g):
        x = g["u"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for f in ["r1", "r5", "r20", "rng1", "rngratio", "lowdist20", "highdist20", "closepos"]:
        dd = d.dropna(subset=[f]).copy()
        dd["q"] = dd.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["quint_" + f] = dd.groupby("q").apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    out["regime"] = d.groupby("regime").apply(summ)
    out["low30"] = d.dropna(subset=["low30"]).groupby("low30").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    # high vol x r5 interaction
    dd = d.dropna(subset=["rngratio", "r5"]).copy()
    dd["volhi"] = (dd.groupby("coin")["rngratio"].rank(pct=True) > 0.5).astype(int)
    dd["r5q"] = dd.groupby("coin")["r5"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["vol_x_r5"] = dd.groupby(["volhi", "r5q"]).apply(summ)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr, ignore_index=True)
        T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
        out["trades_by_fc"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"), pnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
