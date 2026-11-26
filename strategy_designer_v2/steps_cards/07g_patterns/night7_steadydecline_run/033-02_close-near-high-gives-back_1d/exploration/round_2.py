def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c = b["high"], b["low"], b["close"]
            rng = h - l
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                              "cl": np.where(rng > 0, (c - l) / rng, np.nan),
                              "r0": c / c.shift(1) - 1, "r1": c.shift(-1) / c - 1,
                              "r2": c.shift(-2) / c - 1, "width": rng / c})
            d["vol20"] = d["r0"].rolling(20, min_periods=10).std().shift(1)
            d["wz"] = d["width"] / d["width"].rolling(20, min_periods=10).mean().shift(1)
            d["tr60"] = c / c.shift(60) - 1
            d["pos2"] = np.arange(len(d)) % 2 == 0
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["r1"] - D["coin"].map(D.groupby("coin")["r1"].mean())
    s2 = D[D["pos2"]]
    D["x2"] = D["r2"] - D["coin"].map(s2.groupby("coin")["r2"].mean())
    D["day"] = D["ts"].dt.floor("D")
    D["z1"] = D["x1"] / D["vol20"]
    # low-close pressure: (1-cl) * width relative; signed by today's move
    D["lowpress"] = (1 - D["cl"]) * D["wz"]
    D["highpress"] = D["cl"] * D["wz"]

    def ct(sub, col="x1"):
        s = sub.dropna(subset=[col])
        if len(s) < 30:
            return pd.Series({"n": len(s), "mean%": np.nan, "t": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum(); G = len(g)
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
    D["wzq"] = D.groupby("coin")["wz"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D["clq"] = pd.cut(D["cl"], [-0.01, .2, .4, .6, .8, 1.01], labels=False)
    out["wide tercile x cl quintile next-day"] = D[D["wzq"] == 2].groupby("clq").apply(ct)
    out["narrow tercile x cl quintile next-day"] = D[D["wzq"] == 0].groupby("clq").apply(ct)
    out["slope x1 on lowpress"] = slope(D, "lowpress")
    out["slope x1 on highpress"] = slope(D, "highpress")
    out["slope z1 on lowpress"] = slope(D, "lowpress", "z1")
    out["slope x2 on lowpress (non-overlap)"] = slope(D[D["pos2"]], "lowpress", "x2")
    D["dn"] = D["r0"] < 0
    out["down days: slope x1 on lowpress"] = slope(D[D["dn"]], "lowpress")
    out["up days: slope x1 on highpress"] = slope(D[~D["dn"]], "highpress")
    D["trq"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["slope x1 on cl by 60d trend"] = D.groupby("trq").apply(lambda s: slope(s, "cl"))
    out["slope x1 on lowpress by 60d trend"] = D.groupby("trq").apply(lambda s: slope(s, "lowpress"))
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 2, labels=False, duplicates="drop"))
    out["slope x1 on lowpress by vol half"] = D.groupby("volq").apply(lambda s: slope(s, "lowpress"))
    # total move for top lowpress quintile vs cost
    D["lpq"] = D.groupby("coin")["lowpress"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next-day raw r1 by lowpress quintile"] = D.groupby("lpq").apply(lambda s: ct(s, "r1"))
    out["next-day x1 by lowpress quintile"] = D.groupby("lpq").apply(ct)
    D["year"] = D["ts"].dt.year
    out["lowpress slope by year"] = D.groupby("year").apply(lambda s: slope(s, "lowpress"))
    out["lowpress slope by coin"] = D.groupby("coin").apply(lambda s: slope(s, "lowpress"))
    return out
