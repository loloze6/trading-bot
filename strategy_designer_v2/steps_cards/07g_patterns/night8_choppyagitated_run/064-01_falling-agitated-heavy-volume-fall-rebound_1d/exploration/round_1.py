def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"]), "coin": coin, "win": w})
            d["ret1"] = c.pct_change()
            d["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan))
            d["rng_rel"] = (rng / c) / ((rng / c).shift(1).rolling(20, min_periods=20).mean())
            d["ret5"] = c / c.shift(5) - 1
            d["vol20"] = d["ret1"].rolling(20, min_periods=20).std()
            d["z"] = d["ret1"] / d["vol20"].shift(1)
            d["regime"] = b["regime"].values
            d["inprof"] = d["regime"] != "chop"
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["tr60"] = c / c.shift(60) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    mu = D.groupby("coin")["ret1"].mean()
    D["mu"] = D["coin"].map(mu)
    for h in (1, 2, 3):
        D[f"x{h}"] = D[f"n{h}"] - h * D["mu"]
    D["year"] = D["ts"].dt.year; D["wd"] = D["ts"].dt.dayofweek

    def ct(s, sub, col="x1"):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t": np.nan})
        m = s[col].mean(); g = (s[col] - m).groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / max(G - 1, 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    dn = D[D["ret1"] < 0].copy()
    bins = [0, 0.7, 1.0, 1.3, 1.8, 3, 100]
    dn["vrb"] = pd.cut(dn["vr"], bins)
    out["down in-profile by vr"] = dn[dn.inprof].groupby("vrb", observed=True).apply(lambda s: ct(None, s))
    out["down out-profile by vr"] = dn[~dn.inprof].groupby("vrb", observed=True).apply(lambda s: ct(None, s))
    up = D[D["ret1"] > 0].copy(); up["vrb"] = pd.cut(up["vr"], bins)
    out["up in-profile by vr"] = up[up.inprof].groupby("vrb", observed=True).apply(lambda s: ct(None, s))
    out["up out-profile by vr"] = up[~up.inprof].groupby("vrb", observed=True).apply(lambda s: ct(None, s))
    # out of profile, split by 60d trend (computable)
    oo = dn[(~dn.inprof) & (dn.vr > 1)].copy()
    oo["trend"] = pd.cut(oo["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["down heavy out-prof by trend"] = oo.groupby("trend", observed=True).apply(lambda s: ct(None, s))
    cs = dn[dn.inprof & (dn.vr > 1)].copy()
    out["cases horizons"] = pd.DataFrame({h: ct(None, cs, f"x{h}") for h in ("x1", "x2", "x3")}).T
    cs["zb"] = pd.qcut(cs["z"], 3, labels=["big fall", "mid", "small fall"])
    out["cases by fall size z"] = cs.groupby("zb", observed=True).apply(lambda s: ct(None, s))
    cs["clvb"] = pd.cut(cs["clv"], [-0.01, 0.33, 0.66, 1.01], labels=["low", "mid", "high"])
    out["cases by close location"] = cs.groupby("clvb", observed=True).apply(lambda s: ct(None, s))
    cs["r5b"] = pd.qcut(cs["ret5"], 3, labels=["deep5d", "mid", "shallow5d"])
    out["cases by 5d ret"] = cs.groupby("r5b", observed=True).apply(lambda s: ct(None, s))
    out["cases by weekday"] = cs.groupby("wd").apply(lambda s: ct(None, s))
    out["cases by year"] = cs.groupby("year").apply(lambda s: ct(None, s))
    out["cases by coin"] = cs.groupby("coin").apply(lambda s: ct(None, s))
    # all in-profile days next-day, by z of the day (any volume)
    ip = D[D.inprof].copy(); ip["zb"] = pd.qcut(ip["z"], 5)
    out["in-profile all days by z"] = ip.groupby("zb", observed=True).apply(lambda s: ct(None, s))
    op = D[~D.inprof].copy(); op["zb"] = pd.qcut(op["z"], 5)
    out["out-profile all days by z"] = op.groupby("zb", observed=True).apply(lambda s: ct(None, s))
    return out
