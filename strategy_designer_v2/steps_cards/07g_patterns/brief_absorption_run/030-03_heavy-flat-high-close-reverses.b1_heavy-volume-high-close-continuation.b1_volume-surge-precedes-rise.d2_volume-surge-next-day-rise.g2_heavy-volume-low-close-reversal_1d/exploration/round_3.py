def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            rng = (h - l).replace(0, np.nan)
            r0 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w,
                "cl": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "r0": r0,
                "vol20": r0.shift(1).rolling(20, min_periods=20).std(),
                "rr": (rng / c) / (rng / c).shift(1).rolling(20, min_periods=20).mean(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "i": np.arange(len(b)),
                "yr": ts.dt.year, "wd": ts.dt.weekday,
            }))
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    out = {}
    def tab(df, key, val):
        r = df.dropna(subset=[key, val]).groupby(key)[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    ext = D[(D.vr > 2) & (D.cl > 0.8)]
    out["vr>2 & cl>.8 by coin"] = tab(ext, "coin", "x1")
    out["vr>2 & cl>.8 by year"] = tab(ext, "yr", "x1")
    dn = D[(D.r0 < 0)].copy()
    dn["rrq"] = pd.qcut(dn["rr"], 5, labels=False, duplicates="drop")
    dn["vrh"] = np.where(dn["vr"] > 1.5, "heavy", "normal")
    g = dn.dropna(subset=["x1", "rrq"]).groupby(["rrq", "vrh"])["x1"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); out["down days range q x vol"] = g.drop(columns="std")
    wide = dn[dn.rrq == 4]
    out["wide down days by coin"] = tab(wide, "coin", "x1")
    out["wide down days by year"] = tab(wide, "yr", "x1")
    J = dn.dropna(subset=["x1", "rr", "vr", "cl"])
    s = stats.linregress(J["rr"], J["x1"])
    out["down days slope x1 on range ratio"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(J)})
    J2 = J[J.vr < 1]
    s2 = stats.linregress(J2["rr"], J2["x1"])
    out["down light-vol days slope on rr"] = pd.Series({"slope": s2.slope, "t": s2.slope / s2.stderr, "n": len(J2)})
    out["friday bar by coin"] = tab(D[D.wd == 4], "coin", "x1")
    out["friday bar by year"] = tab(D[D.wd == 4], "yr", "x1")
    D2 = D[D.i % 2 == 0].copy()
    D2["x2"] = D2["f2"] - D2.groupby("coin")["f2"].transform("mean")
    D2["cvq"] = pd.qcut(D2["cl"] * D2["vr"], 5, labels=False, duplicates="drop")
    out["x2 by cl*vr quintile (2d grid)"] = tab(D2, "cvq", "x2")
    return out
