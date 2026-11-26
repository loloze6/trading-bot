def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            sd20 = r.rolling(20).std()
            hh = h.rolling(20).max()
            rng = (h - l) / c
            df = pd.DataFrame({
                "coin": coin, "ts": pd.to_datetime(b["timestamp"]), "regime": b["regime"],
                "nxt": nxt, "nxt2": nxt2, "rngsd": rng / sd20, "rngz": rng / rng.rolling(20).mean(),
                "z1": r / sd20, "depth": (c - hh) / hh / sd20, "sd20": sd20,
                "tr60": c / c.shift(60) - 1, "up": (c > o).astype(int),
                "clpos": (c - l) / (h - l)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["ex2"] = d["nxt2"] - d.groupby("coin")["nxt2"].transform("mean")
    d["day"] = d["ts"].dt.floor("D"); d["yr"] = d["ts"].dt.year
    d["volq"] = d.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    d["tr"] = np.where(d["tr60"] > 0.1, "rising", np.where(d["tr60"] < -0.1, "falling", "choppy"))
    d.loc[d["tr60"].isna(), "tr"] = np.nan
    def slope(g, xcol, ycol="ex"):
        g = g.dropna(subset=[xcol, ycol])
        if len(g) < 30: return pd.Series({"n": len(g)})
        X = g[xcol] - g[xcol].mean(); y = g[ycol] - g[ycol].mean()
        beta = (X * y).sum() / (X ** 2).sum(); res = y - beta * X
        s = (X * res).groupby(g["day"]).sum(); se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "beta_%": 100 * beta, "t_day": beta / se})
    def ct(g, col="ex"):
        g = g.dropna(subset=[col]); x = g[col]; n = len(x)
        if n < 5: return pd.Series({"n": n})
        dev = (x - x.mean()).groupby(g["day"]).sum(); se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean_%": 100 * x.mean(), "t_day": x.mean() / se})
    out = {}
    up = d[d["up"] == 1].dropna(subset=["tr"])
    out["up days: slope ex on range/sd20, by trend"] = up.groupby("tr").apply(lambda g: slope(g, "rngsd"))
    out["up days: slope ex on range/20d mean range, by trend"] = up.groupby("tr").apply(lambda g: slope(g, "rngz"))
    out["up days: slope ex on z1, by trend"] = up.groupby("tr").apply(lambda g: slope(g, "z1"))
    out["up days: slope ex2 on rngz, by trend"] = up.groupby("tr").apply(lambda g: slope(g, "rngz", "ex2"))
    f = up[up["tr"] == "falling"].copy()
    f["q"] = pd.qcut(f["rngz"].rank(method="first"), 5, labels=False)
    out["falling up days: rngz quintile"] = f.groupby("q").apply(ct)
    out["falling up days: slope rngz by vol half"] = f.groupby("volq").apply(lambda g: slope(g, "rngz"))
    out["falling up days: slope rngz by year"] = f.groupby("yr").apply(lambda g: slope(g, "rngz"))
    out["falling up days: slope rngz by coin"] = f.groupby("coin").apply(lambda g: slope(g, "rngz"))
    dn = d[d["up"] == 0].dropna(subset=["tr"])
    out["down days: slope ex on rngz, by trend"] = dn.groupby("tr").apply(lambda g: slope(g, "rngz"))
    ch = d[d["regime"] == "unknown"]
    out["choppy: slope ex on depth by up"] = ch.groupby("up").apply(lambda g: slope(g, "depth"))
    return out
