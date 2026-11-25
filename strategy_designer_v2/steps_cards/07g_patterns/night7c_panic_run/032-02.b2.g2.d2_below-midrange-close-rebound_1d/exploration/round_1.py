def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({"day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            d["coin"] = coin; d["win"] = w
            d["ex1"] = (c.shift(-1) / c - 1).values - drift
            d["r3f"] = (c.shift(-3) / c - 1).values - 3 * drift
            rng = (h - l) / c
            d["loc"] = ((h - c) / (h - l).replace(0, np.nan)).values  # 1 = close at low
            d["rr"] = ((h - l).rolling(90, min_periods=60).mean() / (h - l).rolling(30).mean()).values
            d["r1"] = (c / c.shift(1) - 1).values
            d["r7"] = (c / c.shift(7) - 1).values
            d["r30"] = (c / c.shift(30) - 1).values
            d["rngz"] = (rng / rng.rolling(30).mean()).values
            d["dist30low"] = (c / l.rolling(30).min() - 1).values
            d["newlow"] = (l <= l.rolling(30).min()).astype(float).values
            d["wd"] = d["day"].dt.weekday
            d["year"] = d["day"].dt.year
            d["fc"] = b["forecast"].values
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def grp(df, g, col="ex1"):
        out = {}
        df = df.dropna(subset=[col, g])
        for k, s in df.groupby(g):
            per = s.groupby("day")[col].sum()
            n = len(s); m = s[col].mean()
            dev = (s[col] - m).groupby(s["day"]).sum()
            se = np.sqrt((dev ** 2).sum()) / n
            out[k] = {"mean%": 100 * m, "t": m / se if se > 0 else np.nan, "n": n, "days": s["day"].nunique()}
        return pd.DataFrame(out).T

    D["locq"] = pd.qcut(D["loc"], 5, labels=False)
    D["r1q"] = pd.qcut(D["r1"], 5, labels=False)
    D["r7q"] = pd.qcut(D["r7"], 5, labels=False)
    D["r30q"] = pd.qcut(D["r30"], 5, labels=False)
    D["rngzq"] = pd.qcut(D["rngz"], 5, labels=False)
    D["dlq"] = pd.qcut(D["dist30low"], 5, labels=False)
    D["wide"] = (D["rr"] < 1).astype(float).where(D["rr"].notna())
    res = {}
    res["loc quintile all"] = grp(D, "locq")
    res["loc quintile wide regime"] = grp(D[D["wide"] == 1], "locq")
    res["loc quintile calm regime"] = grp(D[D["wide"] == 0], "locq")
    res["past1d quintile"] = grp(D, "r1q")
    res["past1d quintile wide"] = grp(D[D["wide"] == 1], "r1q")
    res["past7d quintile"] = grp(D, "r7q")
    res["past30d quintile"] = grp(D, "r30q")
    res["range vs 30d quintile"] = grp(D, "rngzq")
    res["dist 30d low quintile"] = grp(D, "dlq")
    res["new30low by wide"] = grp(D[D["newlow"] == 1], "wide")
    res["weekday"] = grp(D, "wd")
    res["loc q3d fwd"] = grp(D, "locq", "r3f")
    D["inpos"] = (D["alloc"].abs() > 0).astype(int)
    res["in position"] = grp(D, "inpos")
    res["loc quintile by coin(q4 only)"] = grp(D[D["locq"] == 4], "coin")
    res["loc q4 by year"] = grp(D[D["locq"] == 4], "year")
    return res
