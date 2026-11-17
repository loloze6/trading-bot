def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1 / vol20
            vr = v / v.rolling(30).mean()
            r5p = c / c.shift(5) - 1
            z5 = r5p / (vol20 * np.sqrt(5))
            f1 = c.shift(-1) / c - 1
            f5 = c.shift(-5) / c - 1
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "vr": vr, "z5": z5,
                              "vol20": vol20, "f1": f1, "f5": f5,
                              "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek, "fc": b["forecast"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    g5 = D[D.pos % 5 == 0].copy()
    m5 = g5.groupby("coin")["f5"].mean()
    m1 = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D.coin.map(m1)
    g5["x5"] = g5["f5"] - g5.coin.map(m5)
    def summ(df, col, by):
        gg = df.dropna(subset=[col]).groupby(by, observed=True)[col]
        out = gg.agg(["mean", "std", "count"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.round(4)
    zb = [-99, -2, -1, 1, 2, 99]
    D["zb"] = pd.cut(D.z, zb); g5["zb"] = pd.cut(g5.z, zb)
    D["vb"] = pd.cut(D.vr, [0, 0.8, 1.5, 99]); g5["vb"] = pd.cut(g5.vr, [0, 0.8, 1.5, 99])
    out = {}
    out["x1 by z,vol"] = summ(D, "x1", ["zb", "vb"])
    out["x5 grid by z,vol"] = summ(g5, "x5", ["zb", "vb"])
    g5["z5b"] = pd.cut(g5.z5, [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["x5 by prior5d z"] = summ(g5, "x5", ["z5b"])
    g5["vq"] = g5.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["x5 by vol quintile"] = summ(g5, "x5", ["vq"])
    out["x1 by weekday"] = summ(D, "x1", ["wd"])
    out["x1 by coin, z<=-2"] = summ(D[D.z <= -2], "x1", ["coin"])
    out["x1 by coin, z>=2"] = summ(D[D.z >= 2], "x1", ["coin"])
    return out
