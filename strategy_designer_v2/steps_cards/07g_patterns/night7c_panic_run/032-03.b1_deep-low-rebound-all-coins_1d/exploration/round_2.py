def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fwd": c.shift(-H) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r20": c / c.shift(20) - 1,
                "highdist20": c / c.rolling(20).max() - 1,
                "highdist30": c / c.rolling(30).max() - 1,
                "lowdist20": c / c.rolling(20).min() - 1,
                "closepos": (c - lo) / (hi - lo).replace(0, np.nan),
                "rngratio": rng.rolling(10).mean() / rng.rolling(60, min_periods=40).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            }).iloc[::H]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    d["fold"] = np.where(d["win"].str[1:].astype(int) <= 12, "B", "C")
    def pooled(g):
        x = g.dropna(subset=["u"])
        if len(x) < 5: return pd.Series({"n": len(x), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = x["u"].mean()
        s = (x["u"] - m).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t": m / se})
    def slope(x, f):
        x = x.dropna(subset=[f, "u"]).copy()
        x["z"] = x.groupby("coin")[f].rank(pct=True) - 0.5
        x["z"] = x["z"] / x["z"].std()
        b = (x["z"] * x["u"]).sum() / (x["z"] ** 2).sum()
        e = x["u"] - b * x["z"]
        s = (x["z"] * e).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (x["z"] ** 2).sum()
        return b, b / se, len(x), G
    out = {}
    for f in ["highdist20", "highdist30", "lowdist20", "r20", "closepos", "r1", "rngratio"]:
        dd = d.dropna(subset=[f]).copy()
        dd["q"] = dd.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["pooled_quint_" + f] = dd.groupby("q").apply(pooled)
    sl = []
    for f in ["highdist20", "highdist30", "lowdist20", "r20", "closepos", "r1", "rngratio"]:
        for fo in ["all", "B", "C"]:
            x = d if fo == "all" else d[d["fold"] == fo]
            b, t, n, G = slope(x, f)
            sl.append({"f": f, "fold": fo, "slope": b, "t": t, "n": n, "days": G})
    out["slopes"] = pd.DataFrame(sl)
    out["weekday_pooled"] = d.groupby("wd").apply(pooled)
    # highdist20 within high vs low vol
    dd = d.dropna(subset=["highdist20", "rngratio"]).copy()
    dd["volhi"] = (dd.groupby("coin")["rngratio"].rank(pct=True) > 0.5).astype(int)
    r = []
    for v in [0, 1]:
        b, t, n, G = slope(dd[dd["volhi"] == v], "highdist20")
        r.append({"volhi": v, "slope": b, "t": t, "n": n, "days": G})
    out["highdist20_by_vol"] = pd.DataFrame(r)
    dd["q"] = dd.groupby("coin")["highdist20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["highdist20_q_by_fold"] = dd.groupby(["fold", "q"]).apply(pooled)
    return out
