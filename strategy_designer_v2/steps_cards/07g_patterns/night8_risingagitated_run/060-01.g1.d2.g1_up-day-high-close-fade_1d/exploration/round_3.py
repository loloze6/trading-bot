def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            rr = rng / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": ((c - l) / rng).values,
                "r1": (c / c.shift(1) - 1).values,
                "r5": (c.shift(1) / c.shift(6) - 1).values,  # 5-day return before the up day
                "rngz": (rr / rr.rolling(20).mean().shift(1)).values,
                "nxt": (c.shift(-1) / c - 1).values,
                "regime": b["regime"].values,
                "dayk": ts.dt.strftime("%Y%m%d").values,
                "year": ts.dt.year.values,
            })
            df["unus"] = df["nxt"] - drift
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "loc", "r1"])
    d["inprof"] = d["regime"] != "chop"

    def ct(g):
        n = len(g); m = g["unus"].mean()
        dev = (g["unus"] - m).groupby(g["dayk"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return pd.Series({"n": n, "days": G, "mean_unus": m, "t_day": m / se if se else np.nan})

    def slope_t(g, x):
        g = g.dropna(subset=[x, "unus"])
        X = g[x] - g[x].mean(); y = g["unus"] - g["unus"].mean()
        b = (X * y).sum() / (X ** 2).sum()
        e = y - b * X
        sc = (X * e).groupby(g["dayk"]).sum(); G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(g), "days": G, "slope": b, "t_day": b / se,
                          "spearman": g[x].rank().corr(g["unus"].rank())})

    out = {}
    up = d[d.inprof & (d.r1 > 0)].copy()
    out["prof up: slope on rngz (clip 3)"] = slope_t(up.assign(rz=up["rngz"].clip(upper=3)), "rz").to_frame().T
    out["prof up: slope on prior 5d ret"] = slope_t(up.assign(p5=up["r5"].clip(-0.4, 0.4)), "p5").to_frame().T
    out["prof up: slope on loc"] = slope_t(up, "loc").to_frame().T
    up["p5q"] = pd.qcut(up["r5"], 4)
    out["prof up: prior 5d quartile"] = up.groupby("p5q").apply(ct)
    lowp = up[up["r5"] < up["r5"].median()]
    out["prof up, prior 5d below median: by coin"] = lowp.groupby("coin").apply(ct)
    out["prof up, prior 5d below median: by year"] = lowp.groupby("year").apply(ct)
    out["prof up: by coin"] = up.groupby("coin").apply(ct)
    out["prof up: by year"] = up.groupby("year").apply(ct)
    wide = up[up["rngz"] > up["rngz"].median()]
    out["prof up wide: by year"] = wide.groupby("year").apply(ct)
    o = d[~d.inprof & (d.r1 > 0)].copy()
    out["out prof up: slope on prior 5d"] = slope_t(o.assign(p5=o["r5"].clip(-0.4, 0.4)), "p5").to_frame().T
    out["out prof up: slope on rngz"] = slope_t(o.assign(rz=o["rngz"].clip(upper=3)), "rz").to_frame().T
    return out
