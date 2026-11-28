def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["r1"] = c.pct_change()
            b["r3p"] = c / c.shift(3) - 1
            b["r7p"] = c / c.shift(7) - 1
            hi30 = c.rolling(30, min_periods=30).max()
            lo30 = c.rolling(30, min_periods=30).min()
            b["pbelow"] = c / hi30 - 1
            b["pos30"] = (c - lo30) / (hi30 - lo30)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"]) / rng
            b["rngrel"] = (rng / c) / (rng / c).rolling(20, min_periods=10).mean().shift(1)
            b["volrel"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1)
            sd = b["r1"].rolling(20, min_periods=10).std()
            b["z1"] = b["r1"] / sd.shift(1)
            b["upwick"] = (b["high"] - np.maximum(b["open"], c)) / rng
            b["f1"] = c.shift(-1) / c - 1
            b["f3"] = c.shift(-3) / c - 1
            b["f5"] = c.shift(-5) / c - 1
            b["fa"] = b["regime"].isin(["mean_reversion", "unknown"])
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    fa = d[d["fa"]].copy()
    out = {}
    out["fa share of bars"] = float(d["fa"].mean())
    out["fa bars per coin"] = fa.groupby("coin").size()
    # drift over all windows per coin
    drift = {}
    for h in (1, 3, 5):
        g = d[d["pos"] % h == 0]
        drift[h] = g.groupby("coin")["f%d" % h].mean()
    def table(feat, h, q=5):
        g = fa[fa["pos"] % h == 0].dropna(subset=[feat, "f%d" % h]).copy()
        g["s"] = -(g["f%d" % h] - g["coin"].map(drift[h]))  # short-direction unusual move
        g["bin"] = pd.qcut(g[feat], q, labels=False, duplicates="drop")
        t = g.groupby("bin").agg(lo=(feat, "min"), hi=(feat, "max"), n=("s", "size"),
                                 short_mean=("s", "mean"), short_sd=("s", "std"))
        t["t"] = t["short_mean"] / (t["short_sd"] / np.sqrt(t["n"]))
        sl = stats.linregress(g[feat], g["s"])
        t.loc["slope_t", "t"] = sl.slope / sl.stderr
        return t.drop(columns="short_sd")
    for feat in ["r1", "z1", "r3p", "r7p", "pbelow", "pos30", "clv", "rngrel", "volrel", "upwick"]:
        out["%s h1" % feat] = table(feat, 1)
        out["%s h3" % feat] = table(feat, 3)
    g = fa.dropna(subset=["f1"]).copy()
    g["s"] = -(g["f1"] - g["coin"].map(drift[1]))
    wt = g.groupby("wd")["s"].agg(["size", "mean", "std"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["size"]))
    out["weekday h1 short"] = wt
    ct = g.groupby("coin")["s"].agg(["size", "mean", "std"])
    ct["t"] = ct["mean"] / (ct["std"] / np.sqrt(ct["size"]))
    out["coin h1 short"] = ct
    return out
