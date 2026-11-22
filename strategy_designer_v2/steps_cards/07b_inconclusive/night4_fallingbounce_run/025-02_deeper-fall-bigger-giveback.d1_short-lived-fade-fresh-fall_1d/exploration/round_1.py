def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std().shift(1)
            z = r1 / vol
            r90 = c / c.shift(90) - 1
            r30 = c / c.shift(30) - 1
            reg = (b["regime"] == "mean_reversion")
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "z": z, "r90": r90, "r30": r30, "reg": reg,
                               "fc": b["forecast"].astype(float)})
            for h in [1, 2, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {}
    for h in [1, 2, 3, 5, 10]:
        g = A[A["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    def stat(sub, h, sign):
        v = sign * (sub[f"f{h}"] - sub["coin"].map(drift[h]))
        v = v.dropna()
        n = len(v)
        return pd.Series({"n": n, "mean": v.mean() if n else np.nan,
                          "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "total": (sign * sub[f"f{h}"]).mean()})
    zb = pd.cut(A["z"], [-99, 0, 1, 1.5, 2, 3, 99])
    A["zb"] = zb.astype(str)
    hz = []
    for h in [1, 2, 3, 5, 10]:
        g = A[(A["pos"] % h == 0)]
        fall = g[g["reg"]]
        rise = g[(g["r90"] > 0) & (g["r30"] > 0)]
        for b_, s in fall.groupby("zb"):
            r = stat(s, h, -1); r["h"] = h; r["set"] = "fall_short"; r["zb"] = b_; hz.append(r)
        for b_, s in rise.groupby("zb"):
            r = stat(s, h, -1); r["h"] = h; r["set"] = "rise_short"; r["zb"] = b_; hz.append(r)
    out["by_h_zbucket"] = pd.DataFrame(hz)[["set", "h", "zb", "n", "mean", "t", "total"]]
    g = A[(A["pos"] % 2 == 0) & A["reg"] & (A["z"] > 1)]
    out["h2_z>1_by_coin"] = g.groupby("coin").apply(lambda s: stat(s, 2, -1))
    out["h2_z>1_by_year"] = g.groupby("year").apply(lambda s: stat(s, 2, -1))
    # 90d only (no 30d condition)
    res = []
    for h in [1, 2, 3, 5, 10]:
        gg = A[(A["pos"] % h == 0) & (A["r90"] < 0) & (A["z"] > 1)]
        for k, s in gg.groupby(gg["r30"] < 0):
            r = stat(s, h, -1); r["h"] = h; r["r30neg"] = k; res.append(r)
    out["r90neg_z>1_split_r30"] = pd.DataFrame(res)
    return out
