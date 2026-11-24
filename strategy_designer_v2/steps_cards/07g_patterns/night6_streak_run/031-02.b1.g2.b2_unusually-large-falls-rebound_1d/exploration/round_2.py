def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol60 = r1.rolling(60, min_periods=20).std()
            vol10 = r1.rolling(10, min_periods=8).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "z1": r1 / vol60,
                "z5": (c / c.shift(5) - 1) / (vol60 * np.sqrt(5)),
                "z20": (c / c.shift(20) - 1) / (vol60 * np.sqrt(20)),
                "lvr": np.log(vol10 / vol60),
                "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    d["year"] = d["ts"].dt.year
    out = {}
    def slope(g, h, x):
        col = "f%d" % h
        s = g[g["pos"] % h == 0].dropna(subset=[col, x]).copy()
        drift = s.groupby("coin")[col].mean()
        s["y"] = s[col] - s["coin"].map(drift)
        xc = s[x] - s[x].mean()
        beta = (xc * s["y"]).sum() / (xc ** 2).sum()
        e = s["y"] - s["y"].mean() - beta * xc
        sc = (xc * e).groupby(s["day"]).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (xc ** 2).sum()
        return beta, beta / se, len(s), G
    res = []
    for x in ["z1", "z5", "z20", "lvr"]:
        for h in [2, 5, 10]:
            b_, t, n, G = slope(d, h, x)
            res.append((x, h, round(b_ * 100, 3), round(t, 2), n, G))
    out["slopes all (beta in % per unit)"] = pd.DataFrame(res, columns=["x", "h", "beta%", "t", "n", "days"])
    # up-side only z1
    res = []
    for side, g in [("up z1>0", d[d.z1 > 0]), ("down z1<0", d[d.z1 < 0])]:
        for h in [2, 5, 10]:
            b_, t, n, G = slope(g, h, "z1")
            res.append((side, h, round(b_ * 100, 3), round(t, 2), n, G))
    out["z1 slopes by side"] = pd.DataFrame(res, columns=["side", "h", "beta%", "t", "n", "days"])
    # z20 slope h10 by year and coin
    res = []
    for k, g in d.groupby("year"):
        b_, t, n, G = slope(g, 10, "z20")
        res.append((k, round(b_ * 100, 3), round(t, 2), n))
    out["z20 h10 slope by year"] = pd.DataFrame(res, columns=["year", "beta%", "t", "n"])
    res = []
    for k, g in d.groupby("coin"):
        b_, t, n, G = slope(g, 10, "z20")
        res.append((k, round(b_ * 100, 3), round(t, 2), n))
    out["z20 h10 slope by coin"] = pd.DataFrame(res, columns=["coin", "beta%", "t", "n"])
    res = []
    for k, g in d.groupby("coin"):
        b_, t, n, G = slope(g, 5, "lvr")
        res.append((k, round(b_ * 100, 3), round(t, 2), n))
    out["lvr h5 slope by coin"] = pd.DataFrame(res, columns=["coin", "beta%", "t", "n"])
    return out
