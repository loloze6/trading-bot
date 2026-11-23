def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            r = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "ret": r,
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "vol20": r.rolling(20, min_periods=10).std().shift(1),
                "vr": b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1),
                "clv": ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)) * 2 - 1,
                "rng": (b["high"] - b["low"]) / c,
                "r20": c / c.shift(20) - 1,
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "pos_in_win": np.arange(len(b)),
            })
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    d["mu"] = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - d["mu"]
    d["z"] = d["ret"] / d["vol20"]
    d["rng_z"] = d["rng"] / d["vol20"]
    d["r20z"] = d["r20"] / (d["vol20"] * np.sqrt(20))
    out = {}
    def tab(g, col="ex"):
        a = d.dropna(subset=[col]).groupby(g)[col]
        t = a.agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]]
    d["fcq"] = pd.cut(d["fc"], [-0.01, 0.0001, 2, 5, 10, 21])
    out["fc bucket next-day ex"] = tab("fcq")
    d["zq"] = pd.qcut(d["z"], 10, labels=False)
    out["day z decile"] = tab("zq")
    d["vrq"] = pd.qcut(d["vr"], 5, labels=False)
    d["clvq"] = pd.qcut(d["clv"], 5, labels=False)
    t = d.dropna(subset=["ex"]).groupby(["vrq", "clvq"])["ex"].agg(["mean", "count"])
    out["vol quint x clv quint mean ex"] = t["mean"].unstack()
    out["clv quint"] = tab("clvq")
    d["rngq"] = pd.qcut(d["rng_z"], 5, labels=False)
    out["range/vol quint"] = tab("rngq")
    d["r20q"] = pd.qcut(d["r20z"], 5, labels=False)
    out["r20z quint"] = tab("r20q")
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol tercile"] = tab("volq")
    out["weekday"] = tab("wd")
    out["year"] = tab("year")
    # pooled regressions of ex on standardised features
    reg = {}
    for col in ["z", "clv", "vr", "rng_z", "r20z"]:
        s = d.dropna(subset=[col, "ex"])
        s = s[np.isfinite(s[col])]
        x = s[col].clip(s[col].quantile(0.01), s[col].quantile(0.99))
        res = stats.linregress(x, s["ex"])
        reg[col] = {"slope": res.slope, "t": res.slope / res.stderr, "n": len(s)}
    out["single regressions"] = pd.DataFrame(reg).T
    # 3-day non-overlap
    g = d[d["pos_in_win"] % 3 == 0].dropna(subset=["nxt3", "z"]).copy()
    g["ex3"] = g["nxt3"] - g.groupby("coin")["nxt3"].transform("mean")
    g["zq"] = pd.qcut(g["z"], 5, labels=False)
    a = g.groupby("zq")["ex3"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["3d ex by day z quint (nonoverlap)"] = a
    # coin breakdown of up-day large z
    out["by coin: ex after z>1.5 / z<-1.5"] = pd.DataFrame({
        "up": d[d.z > 1.5].groupby("coin")["ex"].mean(),
        "dn": d[d.z < -1.5].groupby("coin")["ex"].mean(),
        "n_up": d[d.z > 1.5].groupby("coin")["ex"].count()})
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    bk = bd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: q01, q99, skew"] = pd.Series({"q01": bk.quantile(0.01), "q99": bk.quantile(0.99), "skew": bk.skew(), "share top5% of sum": bk[bk > bk.quantile(0.95)].sum() / bk.sum()})
    return out
