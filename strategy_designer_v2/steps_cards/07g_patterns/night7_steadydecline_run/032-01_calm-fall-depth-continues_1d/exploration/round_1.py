def explore(data):
    import pandas as pd, numpy as np
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
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": c.shift(-1) / c - 1 - drift,
                "r3": c.shift(-3) / c - 1 - 3 * drift,
                "r5": c.shift(-5) / c - 1 - 5 * drift,
                "ret1": r, "ret5": c / c.shift(5) - 1, "ret30": c / c.shift(30) - 1,
                "vol20": r.rolling(20).std(),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "prof": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            d["z1"] = d["ret1"] / d["vol20"]
            d["z5"] = d["ret5"] / (d["vol20"] * np.sqrt(5))
            d["z30"] = d["ret30"] / (d["vol20"] * np.sqrt(30))
            d["volrank"] = d["vol20"] / d["vol20"].rolling(60, min_periods=20).median()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        ds = s.groupby("day")[col].sum()
        t = ds.mean() / (ds.std(ddof=1) / np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return (s[col].mean(), t, len(ds))

    def bucket(feat, col, sub=None, q=5, grid=1):
        S = D if sub is None else sub
        if grid > 1: S = S[S["pos"] % grid == 0]
        S = S.dropna(subset=[feat, col]).copy()
        S["b"] = S.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        out = []
        for k, g in S.groupby("b"):
            m, t, n = tday(g, col)
            out.append({"q": int(k), "featmean": g[feat].mean(), "mean": m, "t": t, "days": n})
        return pd.DataFrame(out)

    res = {}
    res["profile share"] = D.groupby("coin")["prof"].mean()
    P = D[D.prof == 1]; N = D[D.prof == 0]
    res["z30 -> r1, in profile"] = bucket("z30", "r1", P)
    res["z30 -> r1, out profile"] = bucket("z30", "r1", N)
    res["z30 -> r5, all (grid5)"] = bucket("z30", "r5", None, grid=5)
    res["z1 -> r1, all"] = bucket("z1", "r1")
    res["z1 -> r1, in profile"] = bucket("z1", "r1", P, q=3)
    res["z5 -> r5, all (grid5)"] = bucket("z5", "r5", None, grid=5)
    res["z5 -> r3, all (grid3)"] = bucket("z5", "r3", None, grid=3)
    res["volrank -> r1"] = bucket("volrank", "r1")
    res["clpos -> r1"] = bucket("clpos", "r1")
    res["rng/vol -> r1"] = bucket("rng", "r1")
    wd = []
    for k, g in D.groupby(D["ts"].dt.weekday):
        m, t, n = tday(g, "r1"); wd.append({"wd": k, "mean": m, "t": t, "days": n})
    res["weekday r1"] = pd.DataFrame(wd)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    B = pd.concat(dd)
    bk = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book by window"] = bk.groupby(level=0).agg(["mean", "count"])
    return res
