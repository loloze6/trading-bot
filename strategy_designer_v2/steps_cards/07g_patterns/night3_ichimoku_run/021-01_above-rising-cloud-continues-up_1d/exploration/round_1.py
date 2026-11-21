def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    # coin drift over H on grid
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            lr = np.log(c)
            ret1_past = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol20 = pd.Series(ret1_past).rolling(20, min_periods=15).std().values
            past26 = np.full(n, np.nan); past26[H:] = c[H:] / c[:-H] - 1
            past7 = np.full(n, np.nan); past7[7:] = c[7:] / c[:-7] - 1
            hi = pd.Series(b["high"].values).rolling(26, min_periods=20).max().values
            lo = pd.Series(b["low"].values).rolling(26, min_periods=20).min().values
            pos26 = (c - lo) / (hi - lo)
            rng = (hi - lo) / c
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                grid.append(dict(coin=coin, w=w, fwd=c[i + H] / c[i] - 1, fc=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], past26=past26[i], past7=past7[i], vol=vol20[i],
                                 pos26=pos26[i], rng=rng[i], alloc=b["postRebalance_current_allocation"].iloc[i]))
            for i in range(n - 1):
                daily.append(dict(coin=coin, w=w, r=r1[i], rp=ret1_past[i], vol=vol20[i],
                                  wd=ts.iloc[i].dayofweek, past7=past7[i], past26=past26[i],
                                  pos26=pos26[i], rng=rng[i], fc=b["forecast"].iloc[i],
                                  alloc=b["postRebalance_current_allocation"].iloc[i], year=ts.iloc[i].year))
        g = pd.DataFrame(grid)
        g["ex"] = g["fwd"] - g["fwd"].mean()
        g["usual"] = g["fwd"].std()
        g["str"] = g["ex"] / g["usual"]
        rows.append(g)
    G = pd.concat(rows)
    D = pd.DataFrame(daily)
    D["ex"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    D["z"] = D["rp"] / D["vol"]

    def summ(df, key, col="ex"):
        a = df.groupby(key)[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")

    out["grid_by_regime"] = summ(G, "reg")
    out["grid_trending_by_coin"] = summ(G[G.reg == "trending"], "coin")
    for v in ["past26", "past7", "vol", "pos26", "rng"]:
        q = G.dropna(subset=[v]).copy()
        q["q"] = q.groupby("coin")[v].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["grid26_by_" + v + "_q"] = summ(q, "q", "str")
    # daily next-day by z of today's move
    q = D.dropna(subset=["z", "ex"]).copy()
    q["q"] = pd.qcut(q["z"], 7, labels=False)
    out["next1_by_todayz"] = summ(q, "q")
    q = D.dropna(subset=["ex"])
    out["next1_by_weekday"] = summ(q, "wd")
    for v in ["past7", "past26", "pos26", "rng", "vol"]:
        q = D.dropna(subset=[v, "ex"]).copy()
        q["q"] = q.groupby("coin")[v].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        # next 7 days excess, non-overlapping approx by taking every 7th row
        out["next1_by_" + v + "_q"] = summ(q, "q")
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; bd.append(dd)
    B = pd.concat(bd)
    B["year"] = pd.to_datetime(B["day"]).dt.year
    yb = B.groupby("year")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book_vs_coin_by_year"] = yb
    out["book_by_coin"] = B.groupby("coin")[["book_return", "coin_return"]].mean()
    # position vs vol
    q = D.dropna(subset=["vol", "ex"]).copy()
    q["inpos"] = (q["alloc"].abs() > 1e-6).astype(int)
    out["next1_by_inpos"] = summ(q, "inpos")
    return out
