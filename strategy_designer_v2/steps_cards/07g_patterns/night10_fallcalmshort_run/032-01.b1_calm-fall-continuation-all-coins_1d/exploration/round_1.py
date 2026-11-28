def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            allr.append((c.shift(-1)/c - 1).dropna())
        drift[coin] = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]; v = b["volume"]
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["regime"].astype(str) == "unknown",
                "r1f": c.shift(-1)/c - 1,
                "r3f": c.shift(-3)/c - 1,
                "r1": c/c.shift(1) - 1,
                "r3": c/c.shift(3) - 1,
                "r7": c/c.shift(7) - 1,
                "r30": c/c.shift(30) - 1,
                "clv": (c - l)/(h - l).replace(0, np.nan),
                "rng": (h - l)/c,
                "rngrel": ((h-l)/c) / ((h-l)/c).rolling(20).mean(),
                "dd30": c/c.rolling(30).max() - 1,
                "up30": c/c.rolling(30).min() - 1,
                "volrel": v / v.rolling(20).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["drift"] = df["coin"].map(drift)
    df["ex1"] = df["r1f"] - df["drift"]
    df["ex3"] = df["r3f"] - 3*df["drift"]
    fc = df[df["fc"]].copy()
    out = {}
    out["counts"] = pd.Series({"all bars": len(df), "fc bars": len(fc),
                               "fc share": fc.shape[0]/len(df)})
    out["fc by coin"] = fc.groupby("coin")["ex1"].agg(["count", "mean"])
    def qtab(col, k=5, ycol="ex1"):
        s = fc.dropna(subset=[col, ycol]).copy()
        s["q"] = pd.qcut(s[col], k, labels=False, duplicates="drop")
        g = s.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=(ycol, "count"),
                                mean=(ycol, "mean"), sd=(ycol, "std"))
        g["t"] = g["mean"]/(g["sd"]/np.sqrt(g["n"]))
        rho, p = stats.spearmanr(s[col], s[ycol])
        g.loc["rho", "mean"] = rho; g.loc["rho", "t"] = p
        return g
    for col in ["r1", "r3", "r7", "r30", "clv", "rngrel", "dd30", "up30", "volrel"]:
        out["ex1 by " + col] = qtab(col)
    # 3-day horizon, non-overlapping grid
    fc3 = fc[fc["pos"] % 3 == 0]
    for col in ["r1", "r3", "up30", "clv"]:
        s = fc3.dropna(subset=[col, "ex3"]).copy()
        s["q"] = pd.qcut(s[col], 3, labels=False, duplicates="drop")
        g = s.groupby("q")["ex3"].agg(["count", "mean", "std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out["ex3 by " + col] = g
    g = fc.groupby("wd")["ex1"].agg(["count", "mean", "std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["ex1 by weekday"] = g
    g = fc.groupby("win")["ex1"].agg(["count", "mean"])
    out["ex1 by window"] = g
    # book daily returns: largest gains/losses context
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd, ignore_index=True)
    br = dd["book_return"].dropna()
    out["book daily"] = pd.Series({"mean": br.mean(), "sd": br.std(), "n": len(br),
                                   "share nonzero": (br.abs() > 1e-9).mean()})
    return out
