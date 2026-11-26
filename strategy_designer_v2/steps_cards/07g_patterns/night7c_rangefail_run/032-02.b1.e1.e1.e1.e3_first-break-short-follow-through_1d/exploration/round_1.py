def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            hi60 = c.shift(1).rolling(60, min_periods=60).max()
            lo60 = c.shift(1).rolling(60, min_periods=60).min()
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            ret60 = c / c.shift(60) - 1
            width = hi60 / lo60 - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "close": c, "margin": (c / hi60 - 1) * 100,
                "r1": r1, "vol20": vol20, "ret60": ret60, "width": width,
                "r5past": c / c.shift(5) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "regime": b["regime"], "alloc": b["postRebalance_current_allocation"],
            })
            for h in [1, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # coin normal drift over 3 days on grid
    g3 = D[D["pos"] % 3 == 0]
    drift3 = g3.groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(drift3)
    g10 = D[D["pos"] % 10 == 0]
    D["x10"] = D["f10"] - D["coin"].map(g10.groupby("coin")["f10"].mean())
    # break cases, dedup within 3 bars
    def dedup(df, h):
        keep = []
        for (cn, w), g in df.groupby(["coin", "win"]):
            last = -999
            for i, p in zip(g.index, g["pos"]):
                if p - last > h:
                    keep.append(i); last = p
        return df.loc[keep]
    brk = D[D["margin"] > 0].dropna(subset=["x3"])
    B = dedup(brk, 3)
    def summ(df, col, by):
        r = df.groupby(by)[col].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    B["mq"] = pd.qcut(B["margin"], 5, labels=False)
    out["break x3 by margin quintile"] = summ(B, "x3", "mq").join(B.groupby("mq")["margin"].median().rename("med_margin"))
    B["wq"] = pd.qcut(B["width"], 3, labels=False)
    out["break x3 by prior range width tercile"] = summ(B, "x3", "wq").join(B.groupby("wq")["width"].median().rename("med_width"))
    B["vq"] = pd.qcut(B["vol20"], 3, labels=False)
    out["break x3 by vol20 tercile"] = summ(B, "x3", "vq")
    B["pq"] = pd.qcut(B["r5past"], 3, labels=False)
    out["break x3 by past5d return tercile"] = summ(B, "x3", "pq")
    B10 = dedup(D[D["margin"] > 0].dropna(subset=["x10"]), 10)
    B10["mq"] = pd.qcut(B10["margin"], 5, labels=False)
    out["break x10 by margin quintile"] = summ(B10, "x10", "mq")
    out["break x3 by coin"] = summ(B, "x3", "coin")
    out["break x3 by year"] = summ(B.assign(yr=D.loc[B.index, "win"]), "x3", "yr")
    # all bars: distance from 60d high, grid 3
    G = D[(D["pos"] % 3 == 0)].dropna(subset=["x3", "margin"]).copy()
    G["dq"] = pd.qcut(G["margin"], 8, labels=False, duplicates="drop")
    out["grid x3 by distance-from-high octile"] = summ(G, "x3", "dq").join(G.groupby("dq")["margin"].median().rename("med_dist"))
    # after large daily moves, by vol tercile, grid 3
    G = G.dropna(subset=["r1", "vol20"])
    G["z"] = G["r1"] / G["vol20"]
    G["zq"] = pd.qcut(G["z"], 5, labels=False)
    out["grid x3 by z of today's return quintile"] = summ(G, "x3", "zq")
    G["vq"] = pd.qcut(G["vol20"], 3, labels=False)
    out["grid x3 by vol tercile"] = summ(G, "x3", "vq")
    # weekday daily returns
    out["daily r1 by weekday"] = summ(D.dropna(subset=["r1"]).assign(nx=D["r1"]), "r1", "wd")
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    bk = bk.reset_index()
    out["book by window"] = bk.groupby("win")["book_return"].agg(["count", "mean", "std"]).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades"] = T.groupby(pd.cut(T["dur_d"], [0, 3.5, 6.5, 100]))["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
