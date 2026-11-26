def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            dist = (c / hi - 1) / sd
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            vol_rel = sd / r1.rolling(60, min_periods=40).std()
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "dist": dist, "r1": r1, "r5p": r5p, "r20p": r20p,
                               "vol_rel": vol_rel, "fwd5": fwd5, "fwd1": fwd1,
                               "rng": rng, "clv": clv,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # normal drift per coin over all windows on grid
    G = A[(A["pos"] % 5 == 0)].dropna(subset=["fwd5"]).copy()
    drift = G.groupby("coin")["fwd5"].mean()
    usual = G.groupby("coin")["fwd5"].std()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    G["z5"] = G["ex5"] / G["coin"].map(usual)
    def summ(g, col="ex5"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    Gd = G.dropna(subset=["dist"])
    Gd["dq"] = pd.qcut(Gd["dist"], 8, duplicates="drop")
    out["ex5 by dist octile"] = Gd.groupby("dq").apply(summ)
    Gd["r5q"] = pd.qcut(Gd["r5p"], 8)
    out["ex5 by past5d return octile"] = Gd.groupby("r5q").apply(summ)
    Gd["r20q"] = pd.qcut(Gd["r20p"], 6)
    out["ex5 by past20d return sextile"] = Gd.groupby("r20q").apply(summ)
    Gd["vq"] = pd.qcut(Gd["vol_rel"], 5)
    out["ex5 by vol20/vol60 quintile"] = Gd.groupby("vq").apply(summ)
    Gd["r1q"] = pd.qcut(Gd["r1"], 8)
    out["ex5 by last-day return octile"] = Gd.groupby("r1q").apply(summ)
    Gd["clq"] = pd.qcut(Gd["clv"], 5)
    out["ex5 by close location quintile"] = Gd.groupby("clq").apply(summ)
    # deep cases split by vol regime and r5p
    deep = Gd[Gd["dist"] <= -2].copy()
    deep["vq2"] = pd.qcut(deep["vol_rel"], 3)
    out["deep (<=-2): ex5 by vol_rel tercile"] = deep.groupby("vq2").apply(summ)
    deep["r1q2"] = pd.qcut(deep["r1"], 3)
    out["deep: ex5 by last-day return tercile"] = deep.groupby("r1q2").apply(summ)
    # weekday fwd1 all bars
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out["ex1 by weekday"] = A.dropna(subset=["ex1"]).groupby("wd").apply(lambda g: summ(g, "ex1"))
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "count"])
    return out
