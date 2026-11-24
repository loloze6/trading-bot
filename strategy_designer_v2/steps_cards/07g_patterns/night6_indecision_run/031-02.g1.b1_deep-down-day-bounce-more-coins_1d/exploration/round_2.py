def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            o, h, l, c = [b[k].astype(float) for k in ["open","high","low","close"]]
            r = c / c.shift(1) - 1
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            d["coin"] = coin; d["pos"] = np.arange(len(b))
            d["r"] = r
            vol = r.shift(1).rolling(20, min_periods=10).std()
            d["z"] = r / vol
            rng = (h - l).replace(0, np.nan)
            d["cl_low"] = (h - c) / rng
            d["rangeZ"] = ((h - l) / c) / (((h - l) / c).shift(1).rolling(20, min_periods=10).mean())
            for H in [1, 3, 5]:
                d[f"nx{H}"] = c.shift(-H) / c - 1
                d[f"u{H}"] = vol * np.sqrt(H)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["yr"] = D["ts"].dt.year
    out = {}
    def slope_t(df, x, y):
        df = df.dropna(subset=[x, y])
        df = df[np.isfinite(df[x]) & np.isfinite(df[y])]
        X = df[x] - df[x].mean(); Y = df[y] - df[y].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        S = (X * e).groupby(df["day"]).sum()
        se = np.sqrt((S ** 2).sum()) / (X * X).sum()
        return b, b / se, len(df), df["day"].nunique()
    res = []
    for H in [1, 3, 5]:
        G = D[D["pos"] % H == 0].copy()
        mu = G.groupby("coin")[f"nx{H}"].transform("mean")
        G["s"] = (G[f"nx{H}"] - mu) / G[f"u{H}"]
        G["zc"] = G["z"].clip(-5, 5)
        b, t, n, nd = slope_t(G, "zc", "s")
        res.append({"H": H, "what": "strength on z(all)", "slope": b, "t": t, "n": n, "days": nd})
        Dn = G[G["z"] < 0].copy()
        Dn["deep_low"] = (-Dn["zc"]) * Dn["cl_low"]
        b, t, n, nd = slope_t(Dn, "deep_low", "s")
        res.append({"H": H, "what": "strength on fall*closeNearLow (down days)", "slope": b, "t": t, "n": n, "days": nd})
        b, t, n, nd = slope_t(G, "rangeZ", "s")
        res.append({"H": H, "what": "strength on relative range", "slope": b, "t": t, "n": n, "days": nd})
    out["graded_slopes"] = pd.DataFrame(res)
    G = D.copy()
    mu = G.groupby("coin")["nx1"].transform("mean")
    G["s"] = (G["nx1"] - mu) / G["u1"]; G["zc"] = G["z"].clip(-5, 5)
    yy = []
    for y, g in G.groupby("yr"):
        b, t, n, nd = slope_t(g, "zc", "s")
        yy.append({"yr": y, "slope": b, "t": t, "n": n})
    out["z_slope_by_year_H1"] = pd.DataFrame(yy)
    return out
