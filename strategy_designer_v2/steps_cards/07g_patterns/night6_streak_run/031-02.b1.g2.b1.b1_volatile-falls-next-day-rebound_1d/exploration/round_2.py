def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b["close"].astype(float).pct_change().dropna() for b in wins.values()])
        mu = allr.mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            df["day"] = df["ts"].dt.floor("D")
            df["r0"] = r
            df["vol60"] = r.rolling(60, min_periods=20).std()
            df["z0"] = r / df["vol60"]
            df["clv"] = ((c - l) / (h - l)).where(h > l)
            df["rng"] = np.log(h / l) / np.log(h / l).rolling(60, min_periods=20).mean()
            df["vz"] = np.log(v.replace(0, np.nan)) - np.log(v.replace(0, np.nan)).rolling(30, min_periods=10).mean()
            df["y1"] = c.shift(-1) / c - 1 - mu
            df["y3"] = c.shift(-3) / c - 1 - 3 * mu
            df["g3"] = (np.arange(len(df)) % 3 == 0)
            df["f"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    def ct(g, y):
        g = g.dropna(subset=[y]); n = len(g)
        if n < 10: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": np.nan})
        m = g[y].mean(); s = (g[y] - m).groupby(g["day"]).sum()
        return pd.Series({"n": n, "mean%": 100*m, "t": m/(np.sqrt((s**2).sum())/n), "days": g["day"].nunique()})

    def slope(g, x, y):
        g = g.dropna(subset=[x, y]); X = g[x] - g[x].mean(); Y = g[y] - g[y].mean()
        b = (X*Y).sum()/(X*X).sum(); e = Y - b*X
        s = (X*e).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum())/(X*X).sum()
        return pd.Series({"n": len(g), "slope": b, "t": b/se, "days": g["day"].nunique()})

    out = {}
    d = D.dropna(subset=["clv", "y1"])
    out["next1 by close-location quintile"] = d.assign(q=pd.qcut(d["clv"], 5, labels=False)).groupby("q").apply(lambda g: ct(g, "y1"))
    d = D.dropna(subset=["rng", "y1"])
    out["next1 by range/avg quintile"] = d.assign(q=pd.qcut(d["rng"], 5, labels=False)).groupby("q").apply(lambda g: ct(g, "y1"))
    d = D.dropna(subset=["vz", "y1"])
    out["next1 by volume-surprise quintile"] = d.assign(q=pd.qcut(d["vz"], 5, labels=False)).groupby("q").apply(lambda g: ct(g, "y1"))
    g3 = D[D["g3"]]
    out["slopes"] = pd.DataFrame({
        "y1~z0": slope(D, "z0", "y1"),
        "y1~clv": slope(D, "clv", "y1"),
        "y3~clv grid": slope(g3, "clv", "y3"),
        "y1~vz": slope(D, "vz", "y1"),
        "y1~rng": slope(D, "rng", "y1"),
        "y1~f (f>0)": slope(D[D["f"] > 0], "f", "y1"),
    }).T
    dn = D[(D["r0"] < 0)].dropna(subset=["clv", "y1"])
    out["down days: next1 by clv quintile"] = dn.assign(q=pd.qcut(dn["clv"], 5, labels=False)).groupby("q").apply(lambda g: ct(g, "y1"))
    out["position: next1 by alloc>0 vs 0"] = D.assign(inpos=(D["alloc"] > 0).astype(int)).groupby("inpos").apply(lambda g: ct(g, "y1"))
    return out
