def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.abs().shift(1).rolling(60, min_periods=20).mean()
            z = r1 / sd
            s20 = r1.rolling(20).std()
            vr = s20 / s20.rolling(60, min_periods=20).mean()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "vr": vr,
                               "r5z": r5 / (sd * np.sqrt(5)), "r20z": r20 / (sd * np.sqrt(20)),
                               "f3": f3, "f1": f1, "reg": b["regime"].values,
                               "alloc": b["postRebalance_current_allocation"].astype(float).values,
                               "wd": ts.dt.weekday.values, "yr": ts.dt.year.values})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["f3x"] = d["f3"] - d.groupby("coin")["f3"].transform("mean")
    g = d[(d["pos"] % 3 == 0)].dropna(subset=["z", "f3x", "vr"])
    def tab(df, col, q=5):
        df = df.copy()
        df["q"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        a = df.groupby("q")["f3x"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["xmean"] = df.groupby("q")[col].mean()
        return a.round(4)
    hi = g[g["vr"] >= 1]; lo = g[g["vr"] < 1]
    out["z quint, vr>=1, f3x"] = tab(hi, "z")
    out["z quint, vr<1, f3x"] = tab(lo, "z")
    out["r5z quint all"] = tab(g.dropna(subset=["r5z"]), "r5z")
    out["r20z quint all"] = tab(g.dropna(subset=["r20z"]), "r20z")
    out["vr quint all"] = tab(g, "vr")
    # correlation by coin and regime
    cc = []
    for (coin, h), s in g.groupby(["coin", g["vr"] >= 1]):
        rr, p = stats.spearmanr(s["z"], s["f3x"])
        cc.append({"coin": coin, "vr>=1": h, "rho": rr, "n": len(s), "p": p})
    out["spearman z vs f3x"] = pd.DataFrame(cc).round(4)
    # day returns: book vs coin by weekday, and decomposition
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book by weekday"] = D.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"]).round(5)
    out["book by year"] = D.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    # position sign stats
    a = d.dropna(subset=["f1"])
    a["gain"] = a["alloc"] * a["f1"]
    out["gain by alloc sign"] = a.groupby(np.sign(a["alloc"]))["gain"].agg(["mean", "count", "sum"]).round(5)
    out["mean alloc, share long/short/flat"] = pd.Series({
        "mean_alloc": a["alloc"].mean(), "long": (a["alloc"] > 0).mean(),
        "short": (a["alloc"] < 0).mean(), "flat": (a["alloc"] == 0).mean()}).round(4)
    return out
