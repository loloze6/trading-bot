def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol60 = r1.rolling(60, min_periods=60).std()
            df = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "pos": np.arange(len(c)), "r1": r1, "vol60": vol60,
                               "r20": c / c.shift(20) - 1, "r60": c / c.shift(60) - 1})
            for h in (2, 5, 10, 20):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["yr"] = A["day"].dt.year
    A["z20"] = A["r20"] / (A["vol60"] * np.sqrt(20))
    A["z60"] = A["r60"] / (A["vol60"] * np.sqrt(60))
    A["absz1"] = (A["r1"] / A["vol60"]).abs()
    A["z1"] = A["r1"] / A["vol60"]
    out = {}

    def clus_reg(g, y, x):
        g = g.dropna(subset=[y, x])
        X = g[x] - g[x].mean(); Y = g[y]
        beta = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
        e = (Y - Y.mean()) - beta * X
        s = (X * e).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return len(g), g["day"].nunique(), beta, beta / se

    res = []
    for h in (2, 5, 10, 20):
        G = A[A["pos"] % h == 0].copy()
        G["x"] = G[f"f{h}"] - G.groupby("coin")[f"f{h}"].transform("mean")
        for x in ("z20", "z60", "absz1", "z1"):
            n, d, b_, t = clus_reg(G, "x", x)
            res.append({"h": h, "x": x, "n": n, "days": d, "slope_%": round(100 * b_, 3), "t": round(t, 2)})
        if h in (5, 10):
            yrs = []
            for y, g in G.groupby("yr"):
                n, d, b_, t = clus_reg(g, "x", "z20")
                yrs.append({"yr": y, "n": n, "slope_%": round(100 * b_, 3), "t": round(t, 2)})
            out[f"h{h} z20 slope by year"] = pd.DataFrame(yrs)
            G["z20q"] = pd.qcut(G["z20"], 5, labels=False)
            out[f"h{h} by z20 quintile"] = G.groupby("z20q").agg(n=("x", "size"),
                mean_excess_pct=("x", lambda s: round(100 * s.mean(), 3)))
    out["regressions"] = pd.DataFrame(res)
    return out
