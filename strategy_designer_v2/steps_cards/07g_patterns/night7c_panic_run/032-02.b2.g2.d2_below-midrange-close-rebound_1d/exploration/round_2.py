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
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({"day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            d["coin"] = coin; d["win"] = w
            d["ex1"] = (c.shift(-1) / c - 1).values - drift
            d["ex2"] = (c.shift(-2) / c - 1).values - 2 * drift
            r1 = c / c.shift(1) - 1
            d["r1"] = r1.values
            sd = r1.rolling(30, min_periods=20).std().shift(1)
            d["z1"] = (r1 / sd).values
            d["loc"] = ((h - c) / (h - l).replace(0, np.nan)).values
            d["rr"] = ((h - l).rolling(90, min_periods=60).mean() / (h - l).rolling(30).mean()).values
            d["year"] = d["day"].dt.year
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def grp(df, g, col="ex1"):
        out = {}
        df = df.dropna(subset=[col, g])
        for k, s in df.groupby(g):
            n = len(s); m = s[col].mean()
            dev = (s[col] - m).groupby(s["day"]).sum()
            se = np.sqrt((dev ** 2).sum()) / n
            out[k] = {"mean%": 100 * m, "t": m / se if se > 0 else np.nan, "n": n, "days": s["day"].nunique()}
        return pd.DataFrame(out).T

    def wt(df, x, col="ex1"):
        df = df.dropna(subset=[x, col])
        w = df[x]; m = (w * df[col]).sum() / w.abs().sum()
        dev = (w * df[col] - w.abs() * m).groupby(df["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / w.abs().sum()
        return pd.Series({"mean%": 100 * m, "t": m / se, "n": len(df), "days": df["day"].nunique()})

    D["z1d"] = pd.qcut(D["z1"], 10, labels=False)
    D["r1d"] = pd.qcut(D["r1"], 10, labels=False)
    D["locq"] = pd.qcut(D["loc"], 5, labels=False)
    D["wide"] = (D["rr"] < 1).astype(float).where(D["rr"].notna())
    res = {}
    res["z1 decile"] = grp(D, "z1d")
    res["z1 decile 2d fwd"] = grp(D, "z1d", "ex2")
    res["r1 decile"] = grp(D, "r1d")
    low = D[D["z1"] < 0].copy(); low["neg_z"] = -low["z1"]
    res["graded neg z (z<0) weighted by -z"] = wt(low, "neg_z")
    res["graded neg z wide regime"] = wt(low[low["wide"] == 1], "neg_z")
    res["graded neg z calm regime"] = wt(low[low["wide"] == 0], "neg_z")
    res["bottom z quintile by loc quintile"] = grp(D[D["z1"] <= D["z1"].quantile(0.2)], "locq")
    res["loc q4 by z quintile"] = grp(D[D["locq"] == 4].assign(zq=pd.qcut(D["z1"], 5, labels=False)), "zq")
    b20 = D[D["z1"] <= D["z1"].quantile(0.2)]
    res["bottom z quintile by window"] = grp(b20, "win")
    res["bottom z quintile by coin"] = grp(b20, "coin")
    res["bottom z quintile by year"] = grp(b20, "year")
    return res
