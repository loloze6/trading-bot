def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = [pd.Series(b[k].values) for k in ["open", "high", "low", "close"]]
            n = len(b)
            d = pd.DataFrame(index=range(n))
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(n)
            d["r1"] = (c / c.shift(1) - 1).values
            d["vol20"] = pd.Series(d["r1"]).rolling(20).std().shift(1).values
            d["z"] = d["r1"] / d["vol20"]
            rz = (h - l).replace(0, np.nan)
            d["clv"] = ((c - l) / rz).values
            for k in [1, 2, 3, 5]:
                d["f%d" % k] = (c.shift(-k) / c - 1).values
            ts = pd.to_datetime(b.timestamp)
            d["yr"] = ts.dt.year.values
            d["day"] = ts.dt.floor("D").values
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    out = {}
    D = P.dropna(subset=["f1", "r1"]).copy()
    mu = D.groupby("coin").f1.transform("mean")
    D["raw1"] = D.f1 - mu
    D["pct"] = D.groupby("coin").r1.rank(pct=True)
    def clus(df, val):
        s = df.dropna(subset=[val])
        g = s.groupby("day")[val].agg(["sum", "count"])
        m = s[val].mean()
        dev = s.groupby("day")[val].apply(lambda x: (x - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"mean": m, "t_dayclus": m / se, "cases": len(s), "days": G})
    bins = [0, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 1.0001]
    D["pb"] = pd.cut(D.pct, bins, labels=False)
    out["next-day raw unusual move by percentile bin of today's return"] = D.groupby("pb").apply(lambda x: clus(x, "raw1")).round(4)
    D["zb"] = pd.cut(D.z, [-99, -3, -2, -1.5, -1, 0, 1, 1.5, 2, 3, 99], labels=False)
    out["next-day raw unusual move by today's return in 20d vol units"] = D.groupby("zb").apply(lambda x: clus(x, "raw1")).round(4)
    B = D[D.pct <= 0.1]
    out["bottom decile: by coin"] = B.groupby("coin").apply(lambda x: clus(x, "raw1")).round(4)
    out["bottom decile: by year"] = B.groupby("yr").apply(lambda x: clus(x, "raw1")).round(4)
    out["bottom decile: by clv tercile"] = B.assign(ct=pd.cut(B.clv, [-0.01, 0.33, 0.66, 1.01], labels=False)).groupby("ct").apply(lambda x: clus(x, "raw1")).round(4)
    for k in [2, 3, 5]:
        B2 = P[(P.pos % k == 0)].dropna(subset=["f%d" % k, "r1"]).copy()
        B2["pct"] = B2.groupby("coin").r1.rank(pct=True)
        B2["raw"] = B2["f%d" % k] - B2.groupby("coin")["f%d" % k].transform("mean")
        out["bottom decile, %d-day raw unusual move (grid)" % k] = clus(B2[B2.pct <= 0.1], "raw").round(4)
    out["top decile next-day"] = clus(D[D.pct > 0.9], "raw1").round(4)
    out["daily std of next-day return by coin"] = D.groupby("coin").f1.std().round(4)
    return out
