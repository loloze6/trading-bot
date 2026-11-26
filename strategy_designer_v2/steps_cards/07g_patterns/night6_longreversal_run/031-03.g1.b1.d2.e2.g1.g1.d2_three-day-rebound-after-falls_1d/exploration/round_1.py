def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    W = data["bars"][coin]
    rows = []
    for w, b in W.items():
        b = b.reset_index(drop=True).copy()
        c = b["close"].astype(float)
        r1 = c.pct_change()
        vol30 = r1.rolling(30, min_periods=20).std()
        b["z1"] = r1 / vol30
        b["vol30"] = vol30
        b["volratio"] = vol30 / r1.rolling(90, min_periods=45).std()
        b["r10p"] = c / c.shift(10) - 1
        b["r30p"] = c / c.shift(30) - 1
        b["z10p"] = b["r10p"] / (vol30 * np.sqrt(10))
        b["z30p"] = b["r30p"] / (vol30 * np.sqrt(30))
        rng = (b["high"] - b["low"]) / c
        b["rngz"] = rng / rng.rolling(30, min_periods=20).mean()
        b["volz"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
        b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
        for h in (1, 3, 10):
            b[f"f{h}"] = c.shift(-h) / c - 1
        b["pos"] = np.arange(len(b))
        b["win"] = w
        b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
        b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out = {}
    def grp(h, col, q=5, cond=None):
        g = B[B["pos"] % h == 0].copy()
        if cond is not None:
            g = g[cond(g)]
        g = g.dropna(subset=[col, f"f{h}"])
        mu = B[B["pos"] % h == 0][f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - mu
        g["bin"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        t = g.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), mean_ex=("ex", "mean"),
                                 sd=("ex", "std"), n=("ex", "size"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        rr, p = stats.pearsonr(g[col], g["ex"])
        t["corr"] = rr
        t["corr_t"] = rr * np.sqrt((len(g) - 2) / (1 - rr ** 2))
        return t.drop(columns="sd").round(4)
    for h in (1, 3, 10):
        out[f"z1 -> f{h}"] = grp(h, "z1")
    out["z10p -> f3"] = grp(3, "z10p")
    out["z10p -> f10"] = grp(10, "z10p")
    out["z30p -> f10"] = grp(10, "z30p")
    out["volratio -> f3"] = grp(3, "volratio")
    out["vol30 -> f3"] = grp(3, "vol30")
    out["rngz -> f3"] = grp(3, "rngz")
    out["volz -> f3"] = grp(3, "volz")
    out["clv -> f1"] = grp(1, "clv")
    out["clv -> f3"] = grp(3, "clv")
    out["z1 up days -> f3"] = grp(3, "z1", q=4, cond=lambda g: g["z1"] > 0)
    out["z1 down days -> f3"] = grp(3, "z1", q=4, cond=lambda g: g["z1"] < 0)
    g1 = B.dropna(subset=["f1"])
    wd = g1.groupby("wd")["f1"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday f1"] = wd.round(4)
    yr = g1.groupby("yr")["f1"].agg(["mean", "size"])
    out["year f1"] = yr.round(4)
    # book
    D = []
    for w, d in data["days"][coin].items():
        d = d.copy(); d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    out["book corr coin"] = float(D["book_return"].corr(D["coin_return"]))
    bw = D.groupby("win").agg(book=("book_return", "sum"), coin=("coin_return", "sum"))
    out["book by window (sum daily)"] = bw.round(3)
    al = B[["postRebalance_current_allocation", "forecast"]].describe().round(3)
    out["alloc/forecast"] = al
    # allocation when forecast 0
    out["share alloc>0 with forecast 0"] = float(((B["forecast"] == 0) & (B["postRebalance_current_allocation"] > 0.01)).mean())
    return out
