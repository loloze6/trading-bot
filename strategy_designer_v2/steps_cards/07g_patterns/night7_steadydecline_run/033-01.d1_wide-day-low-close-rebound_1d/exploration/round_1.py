def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "clv": (c - l) / rng.replace(0, np.nan),
                "rmult": rng / rng.shift(1).rolling(20).mean(),
                "r1": c / c.shift(1) - 1,
                "r3": c / c.shift(3) - 1,
                "r10": c / c.shift(10) - 1,
                "body": (c - o) / rng.replace(0, np.nan),
                "vol20": (c / c.shift(1) - 1).rolling(20).std(),
                "n1": c.shift(-1) / c - 1 - drift,
                "n2": c.shift(-2) / c - 1 - 2 * drift,
                "n3": c.shift(-3) / c - 1 - 3 * drift,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
            })
            d["vrank"] = d["vol20"].rank(pct=True)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["vrank"] = D.groupby("coin")["vol20"].rank(pct=True)
    D["r1z"] = D["r1"] / D["vol20"]

    def tday(s, days):
        g = pd.DataFrame({"v": s.values, "d": days.values}).dropna().groupby("d")["v"].sum()
        n = len(g)
        tot = g.sum(); se = np.sqrt((g ** 2).sum())
        return tot / se if se > 0 else np.nan

    def tab(df, key, col="n1"):
        out = []
        for k, g in df.dropna(subset=[key, col]).groupby(key):
            out.append({key: k, "n": len(g), "mean%": g[col].mean() * 100,
                        "t_day": tday(g[col] - 0, g["day"])})
        return pd.DataFrame(out)

    res = {}
    D["clvq"] = D.groupby("coin")["clv"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    D["rmq"] = D.groupby("coin")["rmult"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    D["r1q"] = D.groupby("coin")["r1z"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    D["r3q"] = D.groupby("coin")["r3"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    D["vq"] = pd.cut(D["vrank"], [0, .33, .66, 1], labels=False)
    res["clv quintile -> next1"] = tab(D, "clvq")
    res["clv quintile -> next3"] = tab(D, "clvq", "n3")
    # clv x range
    t = []
    for (a, bq), g in D.dropna(subset=["clvq", "rmq", "n1"]).groupby(["clvq", "rmq"]):
        t.append({"clvq": a, "rmq": bq, "n": len(g), "mean%": g.n1.mean() * 100, "t": tday(g.n1, g.day)})
    res["clv x range tercile"] = pd.DataFrame(t)
    res["r1z quintile -> next1"] = tab(D, "r1q")
    res["r3 quintile -> next1"] = tab(D, "r3q")
    res["r3 quintile -> next3"] = tab(D, "r3q", "n3")
    res["weekday -> next1"] = tab(D, "wd")
    res["vol tercile -> next1"] = tab(D, "vq")
    # clv x r1 sign
    D["r1s"] = np.sign(D["r1"])
    t = []
    for (a, s), g in D.dropna(subset=["clvq", "n1"]).groupby(["clvq", "r1s"]):
        t.append({"clvq": a, "r1sign": s, "n": len(g), "mean%": g.n1.mean() * 100, "t": tday(g.n1, g.day)})
    res["clv x day sign"] = pd.DataFrame(t)
    # by coin, slope of n1 on (1-clv)
    t = []
    for coin, g in D.dropna(subset=["clv", "n1"]).groupby("coin"):
        lr = stats.linregress(1 - g.clv, g.n1)
        t.append({"coin": coin, "slope%": lr.slope * 100, "t": lr.slope / lr.stderr})
    res["by coin slope n1 on 1-clv"] = pd.DataFrame(t)
    res["year x clv extreme"] = D[D.clvq.isin([0, 4])].dropna(subset=["n1"]).groupby(["yr", "clvq"])["n1"].agg(["count", "mean"]).reset_index()
    # book daily returns: largest days
    B = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            B.append(d.assign(coin=coin, win=w))
    B = pd.concat(B)
    bk = B.groupby(["win", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    res["book vs coin corr"] = float(bk.corr().iloc[0, 1])
    res["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    return res
