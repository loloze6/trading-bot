def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "fa": (b["regime"] == "unknown").astype(int),
                "r1": r1, "s1": r1 / vol,
                "rng": (b["high"] - b["low"]) / c / vol,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1, "alloc": b["postRebalance_current_allocation"],
            })
            d["s5"] = d["r5"] / (vol * np.sqrt(5))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.weekday
    drift3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    drift1 = D.groupby("coin")["f1"].mean()
    D["u3"] = D["f3"] - D["coin"].map(drift3)
    D["u1"] = D["f1"] - D["coin"].map(drift1)
    G3 = D[(D.pos % 3 == 0)].dropna(subset=["u3", "s1"])
    G1 = D.dropna(subset=["u1", "s1"])

    def ct(g, col):
        s = g.groupby("day")[col].sum()
        n = len(g); m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n if n > 1 else np.nan
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean%": 100 * m, "t_day": m / se if se else np.nan})

    bins = [-np.inf, -2, -1, 0, 1, 2, np.inf]
    out = {}
    G3 = G3.assign(sb=pd.cut(G3.s1, bins))
    out["u3 by profile x scaled day"] = G3.groupby(["fa", "sb"], observed=True).apply(lambda g: ct(g, "u3"))
    G1b = G1.assign(sb=pd.cut(G1.s1, bins))
    out["u1 by profile x scaled day"] = G1b.groupby(["fa", "sb"], observed=True).apply(lambda g: ct(g, "u1"))
    G3 = G3.assign(s5b=pd.cut(G3.s5, bins))
    out["u3 by profile x scaled 5d"] = G3.dropna(subset=["s5b"]).groupby(["fa", "s5b"], observed=True).apply(lambda g: ct(g, "u3"))
    G3 = G3.assign(rb=pd.qcut(G3.rng, 4, labels=False, duplicates="drop"), cb=pd.cut(G3.clpos, [0, .25, .75, 1.0001], include_lowest=True))
    out["u3 by profile x range quartile x close pos"] = G3.dropna(subset=["rb", "cb"]).groupby(["fa", "rb", "cb"], observed=True).apply(lambda g: ct(g, "u3"))
    out["u1 by profile x weekday"] = G1.groupby(["fa", "wd"]).apply(lambda g: ct(g, "u1"))
    # slopes of u3 on s1 within each profile
    sl = {}
    for fa, g in G3.groupby("fa"):
        x = g.s1.clip(-4, 4); y = g.u3
        b = np.cov(x, y)[0, 1] / x.var()
        res = y - y.mean() - b * (x - x.mean())
        se = np.sqrt((res ** 2).sum() / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
        sl[fa] = {"slope%perSD": 100 * b, "t": b / se, "n": len(x)}
    out["slope u3 on s1"] = pd.DataFrame(sl).T
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, w=w))
    B = pd.concat(dd).dropna(subset=["book_return"])
    out["book day ret by year"] = B.assign(y=pd.to_datetime(B.day).dt.year).groupby("y")["book_return"].agg(["count", "mean", "std"])
    return out
