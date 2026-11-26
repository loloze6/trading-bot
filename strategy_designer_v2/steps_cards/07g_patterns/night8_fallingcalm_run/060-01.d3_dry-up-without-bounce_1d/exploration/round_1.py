def explore(data):
    import numpy as np, pandas as pd
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["ret5"] = c / c.shift(5) - 1
            b["ret1"] = c / c.shift(1) - 1
            b["ret20"] = c / c.shift(20) - 1
            b["vr5"] = np.log(v.rolling(5).mean() / v.shift(5).rolling(20).mean())
            b["rng"] = (b["high"] - b["low"]) / c
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["falling"] = (b["regime"] != "chop").astype(int)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["vol"] = b["sizing_realised_vol"]
            b["alloc"] = b["postRebalance_current_allocation"]
            rows.append(b[["coin","win","pos","day","wd","close","fwd5","fwd1","ret5","ret1","ret20","vr5","rng","clv","falling","regime","vol","alloc","forecast"]])
    A = pd.concat(rows, ignore_index=True)
    A["vq"] = A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    G = A[(A["pos"] % 5 == 0) & A["fwd5"].notna()].copy()
    G["ex"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")

    def stat(df, col="ex"):
        x = df[col].dropna()
        d = df.loc[x.index]
        n = len(x)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "days": 0})
        m = x.mean()
        S = (x - m).groupby(d["day"]).sum()
        se = np.sqrt((S**2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se if se > 0 else np.nan, "days": d["day"].nunique()})

    out = {}
    out["by_falling"] = G.groupby("falling").apply(stat)
    out["by_regime"] = G.groupby("regime").apply(stat)
    for col in ["ret5", "ret1", "ret20", "vr5", "rng", "clv"]:
        g = G[G[col].notna()].copy()
        g["q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = g.groupby(["falling", "q"]).apply(stat)
        out["q5_" + col + "_by_falling"] = t
    g = G.copy()
    out["falling_by_volq"] = g.groupby(["falling", "vq"]).apply(stat)
    out["by_wd_fwd1_falling"] = A[A["fwd1"].notna()].groupby(["falling", "wd"]).apply(lambda d: stat(d, "ex1"))
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    return out
