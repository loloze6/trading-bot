def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "cl": np.where(rng > 0, (c - l) / rng, np.nan),
                "r0": c / c.shift(1) - 1,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "r5_past": c / c.shift(5) - 1,
                "body": (c - o) / rng.replace(0, np.nan),
                "width": rng / c,
                "alloc": b["postRebalance_current_allocation"],
                "pv": b["postRebalance_total_value"],
            })
            d["vol20"] = d["r0"].rolling(20, min_periods=10).std()
            d["wz"] = d["width"] / d["width"].rolling(20, min_periods=10).mean().shift(1)
            d["r0z"] = d["r0"] / d["vol20"].shift(1)
            d["gain"] = d["alloc"] * d["r1"]
            d["pos3"] = np.arange(len(d)) % 3 == 0
            d["pos2"] = np.arange(len(d)) % 2 == 0
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mean_r = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mean_r)
    D["day"] = D["ts"].dt.floor("D")
    D["year"] = D["ts"].dt.year
    D["wd"] = D["ts"].dt.weekday

    def ct(sub, col="x1"):
        s = sub.dropna(subset=[col])
        if len(s) < 30:
            return pd.Series({"n": len(s), "mean%": np.nan, "t": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t": m / se})

    def slope(sub, xcol, ycol="x1"):
        s = sub.dropna(subset=[xcol, ycol])
        x = s[xcol] - s[xcol].mean(); y = s[ycol]
        b = (x * y).sum() / (x**2).sum()
        e = y - y.mean() - b * x
        g = (e * x).groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / (x**2).sum()
        return pd.Series({"n": len(s), "slope": b, "t": b / se})

    out = {}
    D["clq"] = pd.cut(D["cl"], [-0.01, .2, .4, .6, .8, 1.01], labels=False)
    out["next day by close-loc quintile"] = D.groupby("clq").apply(ct)
    # multi-day horizons, non-overlapping
    for hcol, pcol in [("r2", "pos2"), ("r3", "pos3")]:
        s = D[D[pcol]].copy()
        s[hcol + "x"] = s[hcol] - s["coin"].map(D[D[pcol]].groupby("coin")[hcol].mean())
        out[f"slope {hcol} on cl"] = slope(s, "cl", hcol + "x")
    out["slope by coin"] = D.groupby("coin").apply(lambda s: slope(s, "cl"))
    out["slope by year"] = D.groupby("year").apply(lambda s: slope(s, "cl"))
    # interactions
    D["wzq"] = D.groupby("coin")["wz"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope by width tercile"] = D.groupby("wzq").apply(lambda s: slope(s, "cl"))
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope by vol tercile"] = D.groupby("volq").apply(lambda s: slope(s, "cl"))
    D["r0s"] = np.sign(D["r0"])
    out["slope by today's sign"] = D.groupby("r0s").apply(lambda s: slope(s, "cl"))
    D["p5q"] = D.groupby("coin")["r5_past"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope by past-5d tercile"] = D.groupby("p5q").apply(lambda s: slope(s, "cl"))
    # bars: returns after large moves
    D["r0zq"] = pd.cut(D["r0z"], [-99, -2, -1, 0, 1, 2, 99], labels=False)
    out["next day by today's z-move"] = D.groupby("r0zq").apply(ct)
    out["slope next on r0z"] = slope(D, "r0z")
    out["slope next on body"] = slope(D, "body")
    out["slope next on wz"] = slope(D, "wz")
    out["next day by weekday"] = D.groupby("wd").apply(ct)
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    Y = pd.concat(days, ignore_index=True)
    Y["day"] = pd.to_datetime(Y["day"])
    bk = Y.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["year"] = bk["day"].dt.year; bk["wd"] = bk["day"].dt.weekday
    out["book by year"] = bk.groupby("year").agg(mean_bp=("book_return", lambda s: 1e4 * s.mean()),
                                                 coin_bp=("coin_return", lambda s: 1e4 * s.mean()),
                                                 n=("book_return", "size"))
    out["book by window"] = bk.groupby("win").agg(mean_bp=("book_return", lambda s: 1e4 * s.mean()),
                                                  coin_bp=("coin_return", lambda s: 1e4 * s.mean()))
    out["book corr with coin"] = float(bk[["book_return", "coin_return"]].corr().iloc[0, 1])
    out["mean alloc"] = float(D["alloc"].mean())
    out["gain before costs bp/bar"] = float(1e4 * D["gain"].mean())
    return out
