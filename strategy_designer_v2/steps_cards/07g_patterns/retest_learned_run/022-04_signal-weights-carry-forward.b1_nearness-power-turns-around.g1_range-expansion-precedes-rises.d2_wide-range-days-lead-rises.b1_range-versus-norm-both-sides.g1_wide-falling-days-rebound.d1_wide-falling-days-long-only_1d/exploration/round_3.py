def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = h - l
            f = pd.DataFrame(index=b.index)
            f["coin"] = coin; f["win"] = w
            f["r1"] = c / c.shift(1) - 1
            f["rx"] = rng / rng.rolling(30, min_periods=30).mean() - 1
            f["clv"] = (c - l) / rng.replace(0, np.nan)
            f["wick"] = (np.minimum(o, c) - l) / rng.rolling(30, min_periods=30).mean()
            f["r7"] = c / c.shift(7) - 1
            f["year"] = pd.to_datetime(b["timestamp"]).dt.year
            f["fwd3"] = c.shift(-3) / c - 1
            f["alloc"] = b["postRebalance_current_allocation"].values
            f["pos"] = np.arange(len(b))
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    g["drift"] = g.groupby("coin")["fwd3"].transform("mean")
    g["u"] = g["fwd3"] - g["drift"]
    def stats(d, by):
        r = d.groupby(by)["u"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r[["mean", "t", "count"]].round(4)
    out = {}
    dn = g[g["r1"] < 0].dropna(subset=["rx", "clv"]).copy()
    dn["rxh"] = (dn.groupby("coin")["rx"].rank(pct=True) > 0.5).astype(int)
    dn["clvq"] = dn.groupby("coin")["clv"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["down days: rx half x clv third"] = stats(dn, ["rxh", "clvq"])
    dn["wq"] = dn.groupby("coin")["wick"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["down days: lower wick / 30d range q5"] = stats(dn, "wq")
    dn["inpos"] = (dn["alloc"].abs() > 1e-6).astype(int)
    out["down days top clv third, by inpos"] = stats(dn[dn["clvq"] == 2], "inpos")
    out["down days top clv third by year"] = stats(dn[dn["clvq"] == 2], "year")
    out["down days top clv third by coin"] = stats(dn[dn["clvq"] == 2], "coin")
    up = g[g["r1"] > 0].dropna(subset=["clv"]).copy()
    up["clvq"] = up.groupby("coin")["clv"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["up days clv third"] = stats(up, "clvq")
    m = g.dropna(subset=["r7"]).copy()
    m["q"] = m.groupby("coin")["r7"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["r7 top quintile by year"] = stats(m[m["q"] == 4], "year")
    out["r7 top quintile by coin"] = stats(m[m["q"] == 4], "coin")
    return out
