def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.shift(1).rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            n = len(b)
            df = pd.DataFrame({"coin": coin, "w": w, "ts": b["timestamp"], "z": z,
                               "agit": (b["regime"] != "chop").astype(int), "tr60": tr60,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year, "idx": np.arange(n)})
            for h in (1, 2, 3, 5, 10):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["trend"] = np.where(d.tr60 > 0.1, "rise", np.where(d.tr60 < -0.1, "fall", np.where(d.tr60.notna(), "chop", "na")))
    def slope(x, y="y", xx="z"):
        x = x.dropna(subset=[y, xx])
        if len(x) < 10: return pd.Series({"slope%": np.nan, "t": np.nan, "n": len(x), "days": 0})
        X = x[xx].values; Y = x[y].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = (Y - Y.mean()) - b * Xc
        s = pd.Series(Xc * e).groupby(x["day"].values).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / (Xc ** 2).sum()
        return pd.Series({"slope%": 100 * b, "t": b / se, "n": len(x), "days": G})
    def ct(x, col):
        x = x.dropna(subset=[col]); m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum(); se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series({"mean%": 100 * m, "t": m / se, "n": len(x), "days": len(s)})
    out = {}
    res = {}
    for h in (1, 2, 3, 5, 10):
        g = d[(d.idx % h == 0)].copy()
        g["y"] = g["f%d" % h] - g.groupby("coin")["f%d" % h].transform("mean")
        for a in (0, 1):
            res[("h%d" % h, a)] = slope(g[g.agit == a])
    out["slope f_h on z by agit"] = pd.DataFrame(res).T.round(3)
    g = d[d.idx % 5 == 0].copy()
    g["y"] = g.f5 - g.groupby("coin").f5.transform("mean")
    g["sy"] = np.sign(g.z) * g.y
    cal = g[g.agit == 0]
    out["calm slope by trend"] = cal.groupby("trend").apply(slope).round(3)
    out["calm slope by year"] = cal.groupby("yr").apply(slope).round(3)
    out["calm slope by coin"] = cal.groupby("coin").apply(slope).round(3)
    cal2 = cal.copy(); cal2["up"] = (cal2.z > 0).astype(int)
    out["calm slope by side of day"] = cal2.groupby("up").apply(slope).round(3)
    big = cal[cal.z.abs() > 1.5]
    out["calm big days signed f5 by year"] = big.groupby("yr").apply(lambda x: ct(x, "sy")).round(3)
    out["calm big days signed f5 by side"] = big.groupby(big.z > 0).apply(lambda x: ct(x, "sy")).round(3)
    # windows: share with positive slope
    ws = cal.groupby("w").apply(slope)
    out["calm per-window slope"] = pd.Series({"windows": len(ws), "positive": int((ws["slope%"] > 0).sum()),
                                              "mean slope%": ws["slope%"].mean()}).round(3)
    return out
