def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r1 = c / c.shift(1) - 1
            sd = r1.rolling(30, min_periods=15).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c - 1,
                "r1": r1, "r1z": r1 / sd.shift(1),
                "r3z": (c / c.shift(3) - 1) / (sd.shift(1) * np.sqrt(3)),
                "loc": ((h - c) / (h - l)).where(h > l),
                "body": ((c - o) / (h - l)).where(h > l),
                "r30": c / c.shift(30) - 1,
                "reg": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].values,
            })
            d["pos2"] = (np.arange(len(d)) % 2 == 0)
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["ex"] = df["nxt"] - df["coin"].map(df.groupby("coin")["nxt"].mean())
    df["ex2"] = df["nxt2"] - df["coin"].map(df[df.pos2].groupby("coin")["nxt2"].mean())
    df["day"] = df["ts"].dt.floor("D"); df["yr"] = df["ts"].dt.year

    def tclu(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean(); dev = (s - m).groupby(dd).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return m, m / se if se > 0 else np.nan, len(s), dd.nunique()

    def table(sub, key, col="ex"):
        out = []
        for k, g in sub.groupby(key, observed=True):
            m, t, n, nd = tclu(g[col], g["day"])
            out.append({"grp": str(k), "mean%": round(m * 100, 3), "t": round(t, 2), "n": n, "days": nd})
        return pd.DataFrame(out)

    def slope(sub, x, col="ex"):
        s = sub[[x, col, "day"]].dropna()
        z = (s[x] - s[x].mean()) / s[x].std()
        v = z * s[col]
        m, t, n, nd = tclu(v, s["day"])
        return {"cov%": round(m * 100, 4), "t": round(t, 2), "n": n, "days": nd}

    res = {}
    df["r1zq"] = pd.qcut(df["r1z"], 5, labels=False)
    df["r3zq"] = pd.qcut(df["r3z"], 5, labels=False)
    df["locq"] = pd.qcut(df["loc"], 5, labels=False)
    df["bodyq"] = pd.qcut(df["body"], 5, labels=False)
    res["r1z quintile (vol-scaled day return)"] = table(df, "r1zq")
    res["r3z quintile"] = table(df, "r3zq")
    res["body quintile (close-open)/range"] = table(df, "bodyq")
    res["r1z quintile, 2d grid"] = table(df[df.pos2], "r1zq", "ex2")
    # slopes by year
    out = []
    for y, g in df.groupby("yr"):
        out.append({"yr": y, **{f"{k}_{x}": v for x in ["r1z", "loc"] for k, v in slope(g, x).items() if k in ("cov%", "t")}})
    res["slopes by year (r1z neg = reversal; loc pos = near-low rebound)"] = pd.DataFrame(out)
    out = []
    for cn, g in df.groupby("coin"):
        out.append({"coin": cn, **{f"{k}_{x}": v for x in ["r1z", "loc"] for k, v in slope(g, x).items() if k in ("cov%", "t")}})
    res["slopes by coin"] = pd.DataFrame(out)
    # loc within r1z groups: is loc independent of the day's return?
    df["r1z3"] = pd.qcut(df["r1z"], 3, labels=False)
    out = []
    for k, g in df.groupby("r1z3"):
        out.append({"r1z tercile": k, **slope(g, "loc")})
    res["loc slope within r1z terciles"] = pd.DataFrame(out)
    out = []
    for k, g in df.groupby("locq"):
        out.append({"loc q": k, **slope(g, "r1z")})
    res["r1z slope within loc quintiles"] = pd.DataFrame(out)
    # r1z reversal by 30d trend sign
    df["dn30"] = (df["r30"] < 0).astype(int)
    out = []
    for k, g in df.groupby("dn30"):
        out.append({"r30<0": k, **slope(g, "r1z"), **{"loc_" + a: b for a, b in slope(g, "loc").items()}})
    res["slopes by 30d trend sign"] = pd.DataFrame(out)
    res["overall slopes"] = pd.DataFrame([{"x": x, **slope(df, x)} for x in ["r1z", "r3z", "loc", "body"]])
    return res
