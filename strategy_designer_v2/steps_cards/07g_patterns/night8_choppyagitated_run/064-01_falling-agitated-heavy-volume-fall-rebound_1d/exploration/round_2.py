def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"]), "coin": coin, "win": w})
            d["pos"] = np.arange(len(b))
            d["ret1"] = c.pct_change()
            d["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan))
            d["ret5"] = c / c.shift(5) - 1
            d["vol20"] = d["ret1"].rolling(20, min_periods=20).std()
            d["z"] = d["ret1"] / d["vol20"].shift(1)
            d["regime"] = b["regime"].values
            d["inprof"] = d["regime"] != "chop"
            d["tr60"] = c / c.shift(60) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    mu = D.groupby("coin")["ret1"].mean()
    D["mu"] = D["coin"].map(mu)
    for h in (1, 2, 3):
        D[f"x{h}"] = D[f"n{h}"] - h * D["mu"]
    D["year"] = D["ts"].dt.year; D["wd"] = D["ts"].dt.dayofweek

    def ct(sub, col="x1", h=1):
        s = sub.dropna(subset=[col])
        if h > 1: s = s[s["pos"] % h == 0]
        if len(s) < 5: return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t": np.nan})
        m = s[col].mean(); g = (s[col] - m).groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / max(G - 1, 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    out["regime counts"] = D["regime"].value_counts()
    bins = [0, 0.7, 1.0, 1.3, 1.8, 3, 100]
    dn = D[D["ret1"] < 0].copy(); dn["vrb"] = pd.cut(dn["vr"], bins)
    out["down in-profile by vr"] = dn[dn.inprof].groupby("vrb", observed=True).apply(ct)
    out["down out-profile by vr"] = dn[~dn.inprof].groupby("vrb", observed=True).apply(ct)
    up = D[D["ret1"] > 0].copy(); up["vrb"] = pd.cut(up["vr"], bins)
    out["up in-profile by vr"] = up[up.inprof].groupby("vrb", observed=True).apply(ct)
    out["up out-profile by vr"] = up[~up.inprof].groupby("vrb", observed=True).apply(ct)
    oo = dn[(~dn.inprof) & (dn.vr > 1)].copy()
    oo["trend"] = pd.cut(oo["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["down heavy out-prof by trend"] = oo.groupby("trend", observed=True).apply(ct)
    oo2 = dn[(~dn.inprof) & (dn.vr > 1.8)].copy()
    oo2["trend"] = pd.cut(oo2["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["down vr>1.8 out-prof by trend"] = oo2.groupby("trend", observed=True).apply(ct)
    cs = dn[dn.inprof & (dn.vr > 1)].copy()
    out["cases horizons"] = pd.DataFrame({c: ct(cs, c, h) for c, h in (("x1", 1), ("x2", 2), ("x3", 3))}).T
    cs["zb"] = pd.qcut(cs["z"], 3, labels=["big fall", "mid", "small fall"])
    out["cases by fall size z"] = cs.groupby("zb", observed=True).apply(ct)
    cs["clvb"] = pd.cut(cs["clv"], [-0.01, 0.33, 0.66, 1.01], labels=["low", "mid", "high"])
    out["cases by close location"] = cs.groupby("clvb", observed=True).apply(ct)
    cs["r5b"] = pd.qcut(cs["ret5"], 3, labels=["deep5d", "mid", "shallow5d"])
    out["cases by 5d ret"] = cs.groupby("r5b", observed=True).apply(ct)
    out["cases by weekday"] = cs.groupby("wd").apply(ct)
    out["cases by year"] = cs.groupby("year").apply(ct)
    out["cases by coin"] = cs.groupby("coin").apply(ct)
    ip = D[D.inprof].copy(); ip["zb"] = pd.qcut(ip["z"], 5)
    out["in-profile all days by z"] = ip.groupby("zb", observed=True).apply(ct)
    op = D[~D.inprof].copy(); op["zb"] = pd.qcut(op["z"], 5)
    out["out-profile all days by z"] = op.groupby("zb", observed=True).apply(ct)
    return out
