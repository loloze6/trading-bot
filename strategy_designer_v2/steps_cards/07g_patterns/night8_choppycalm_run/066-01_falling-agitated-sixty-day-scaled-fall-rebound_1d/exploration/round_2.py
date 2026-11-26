def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd60 = r.rolling(60, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z60": r / sd60.shift(1),
                "loc": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown"),
                "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "ret5p": c / c.shift(5) - 1,
                "zp5": (c / c.shift(5) - 1) / (sd60.shift(1) * np.sqrt(5)),
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r"].mean()
    for h in [1, 2, 3]:
        d["x%d" % h] = d["r%d" % h] - d["coin"].map(mu) * h
    d["day"] = d["ts"].dt.floor("D")
    def cl(g, col):
        g = g[[col, "day"]].dropna()
        n = len(g)
        if n < 5: return pd.Series({"n": n, "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        m = g[col].mean(); s = (g[col] - m).groupby(g["day"]).sum(); D = len(s)
        se = np.sqrt(D / (D - 1) * (s ** 2).sum()) / n
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t_day": m / se})
    out = {}
    P = d[d.inprof]
    # up-day grading in profile, day-clustered
    P = P.copy()
    P["zb"] = pd.cut(P["z60"], [-np.inf, -1.5, -0.75, -0.25, 0, 0.25, 0.75, 1.5, np.inf])
    out["in-prof x1 by z60 (day-clustered)"] = P.groupby("zb", observed=True).apply(lambda g: cl(g, "x1"))
    up = P[P.z60 > 0]
    out["in-prof up days: spearman z60 vs x1"] = pd.Series(stats.spearmanr(up.z60, up.x1, nan_policy="omit"), index=["rho", "p"])
    up = up.copy()
    up["locb"] = pd.cut(up["loc"], [0, 0.33, 0.67, 1.0], include_lowest=True)
    out["in-prof up days by close location"] = up.groupby("locb", observed=True).apply(lambda g: cl(g, "x1"))
    up["zp5b"] = pd.qcut(up["zp5"], 4, duplicates="drop")
    out["in-prof up days by prior 5d scaled return"] = up.groupby("zp5b", observed=True).apply(lambda g: cl(g, "x1"))
    out["in-prof up days x1 by window"] = up.groupby("win").apply(lambda g: cl(g, "x1"))
    # 3-day horizon after falls in profile, non-overlapping grid
    G = d[(d.pos % 3 == 0) & d.inprof & (d.z60 < 0)].copy()
    G["zb"] = pd.cut(G["z60"], [-np.inf, -2, -1.25, -0.5, 0])
    out["in-prof falls x3 grid3 by z60"] = G.groupby("zb", observed=True).apply(lambda g: cl(g, "x3"))
    out["in-prof falls x3 grid3 spearman"] = pd.Series(stats.spearmanr(-G.z60, G.x3, nan_policy="omit"), index=["rho", "p"])
    G2 = d[(d.pos % 3 == 0) & (~d.inprof) & (d.z60 < 0)].copy()
    G2["zb"] = pd.cut(G2["z60"], [-np.inf, -2, -1.25, -0.5, 0])
    out["out-prof falls x3 grid3 by z60"] = G2.groupby("zb", observed=True).apply(lambda g: cl(g, "x3"))
    # day 2-3 only (beyond the next day) after big falls in profile
    d["x23"] = d["r3"] / 1 - d["r1"]
    B = d[d.inprof & (d.z60 < -1.25)].copy()
    B["x23"] = (1 + B["r3"]) / (1 + B["r1"]) - 1 - 2 * B["coin"].map(mu)
    out["in-prof big falls: days 2-3 excess"] = cl(B, "x23")
    out["in-prof falls x1 by window (z60<-0.75)"] = P[P.z60 < -0.75].groupby("win").apply(lambda g: cl(g, "x1"))
    return out
