def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b["close"].astype(float).pct_change().dropna() for b in wins.values()])
        mu = allr.mean(); usd = allr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float).replace(0, np.nan)
            r = c.pct_change()
            df = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            df["coin"] = coin; df["win"] = w
            df["day"] = df["ts"].dt.floor("D"); df["yr"] = df["ts"].dt.year
            df["r0"] = r
            lv = np.log(v)
            df["vz"] = lv - lv.rolling(30, min_periods=10).mean()
            df["vz7"] = np.log(v.rolling(7).mean()) - lv.rolling(30, min_periods=10).mean()
            df["rng"] = np.log(h / l) / np.log(h / l).rolling(60, min_periods=20).mean()
            df["y1"] = c.shift(-1) / c - 1 - mu
            df["y3"] = c.shift(-3) / c - 1 - 3 * mu
            df["y1n"] = df["y1"] / usd
            df["g3"] = (np.arange(len(df)) % 3 == 0)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    def slope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan, "days": np.nan})
        X = g[x] - g[x].mean(); Y = g[y] - g[y].mean()
        b = (X*Y).sum()/(X*X).sum(); e = Y - b*X
        s = (X*e).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum())/(X*X).sum()
        return pd.Series({"n": len(g), "slope": b, "t": b/se, "days": g["day"].nunique()})

    def ct(g, y):
        g = g.dropna(subset=[y]); n = len(g)
        m = g[y].mean(); s = (g[y] - m).groupby(g["day"]).sum()
        return pd.Series({"n": n, "mean%": 100*m, "t": m/(np.sqrt((s**2).sum())/n), "days": g["day"].nunique()})

    out = {}
    D["up"] = (D["r0"] > 0).astype(int)
    out["y1~vz by up day"] = D.groupby("up").apply(lambda g: slope(g, "vz", "y1"))
    out["y1~vz by year"] = D.groupby("yr").apply(lambda g: slope(g, "vz", "y1"))
    out["y1~vz by coin"] = D.groupby("coin").apply(lambda g: slope(g, "vz", "y1"))
    g3 = D[D["g3"]]
    out["other slopes"] = pd.DataFrame({
        "y3~vz grid": slope(g3, "vz", "y3"),
        "y1~vz7": slope(D, "vz7", "y1"),
        "y1n~vz": slope(D, "vz", "y1n"),
        "y1~rng": slope(D, "rng", "y1"),
    }).T
    # vz controlled for range: residualize
    d = D.dropna(subset=["vz", "rng", "y1"]).copy()
    bb = np.polyfit(d["rng"], d["vz"], 1)
    d["vz_res"] = d["vz"] - np.polyval(bb, d["rng"])
    out["vz resid on range: slope"] = slope(d, "vz_res", "y1")
    out["corr vz rng"] = float(d["vz"].corr(d["rng"]))
    dd = D.dropna(subset=["vz", "y1"]).copy()
    dd["q"] = pd.qcut(dd["vz"], 5, labels=False)
    out["vz quintile x up: next1"] = dd.groupby(["q", "up"]).apply(lambda g: ct(g, "y1"))
    return out
