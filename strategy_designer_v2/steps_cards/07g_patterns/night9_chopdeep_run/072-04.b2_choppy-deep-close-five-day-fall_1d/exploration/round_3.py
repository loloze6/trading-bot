def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); n = len(b)
            r1 = c.pct_change()
            f5 = c.shift(-5) / c - 1
            sd20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            depth = (c / hi20 - 1) / sd20
            rngpos = (c - lo20) / (hi20 - lo20)
            ret60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            ret10 = (c / c.shift(10) - 1) / sd20
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "regime": b["regime"].values,
                "r1": r1, "f5": f5, "depth": depth, "rngpos": rngpos, "ret60": ret60, "ret10": ret10,
                "sd30": sd30, "sd20": sd20, "year": ts.dt.year.values, "day": ts.dt.floor("D").values}))
    D = pd.concat(rows, ignore_index=True)
    g = D[D.pos % 5 == 0].dropna(subset=["f5"])
    drift5 = g.groupby("coin")["f5"].mean()
    D["x5"] = D["f5"] - D.coin.map(drift5)
    D["choppy"] = D.regime == "unknown"
    D["volpct"] = D.groupby("coin")["sd30"].rank(pct=True)
    D["agit"] = D.volpct > 0.5
    G = D[D.pos % 5 == 0].dropna(subset=["x5", "depth"]).copy()
    out = {}
    def slope_t(s, x, y="x5"):
        s = s.dropna(subset=[x, y])
        X = s[x] - s[x].mean(); Y = s[y]
        b = (X * Y).sum() / (X * X).sum()
        e = Y - Y.mean() - b * X
        sc = (X * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X * X).sum()
        return pd.Series({"slope": b, "t_day": b / se, "n": len(s), "days": s["day"].nunique()})
    res = {}
    for nm, sub in [("choppy all", G[G.choppy]), ("choppy calm", G[G.choppy & ~G.agit]),
                    ("choppy agit", G[G.choppy & G.agit]), ("nonchoppy", G[~G.choppy])]:
        for x in ["depth", "rngpos", "ret10", "volpct"]:
            res[(nm, x)] = slope_t(sub, x)
    out["slopes (clustered by day)"] = pd.DataFrame(res).T
    def ttab(s, by, y="x5"):
        s = s.dropna(subset=[y])
        t = s.groupby(by)[y].agg(["mean", "std", "size"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
        return t.drop(columns="std")
    CA = G[G.choppy & G.agit].copy()
    out["choppy agit by year"] = ttab(CA, "year")
    out["choppy agit by coin"] = ttab(CA, "coin")
    CA["vq"] = pd.qcut(CA.volpct, 3, labels=False)
    out["choppy agit vol tercile"] = ttab(CA, "vq")
    CA["rq"] = pd.qcut(CA.ret10, 3, labels=False)
    out["choppy agit ret10 tercile"] = ttab(CA, "rq")
    N = G[~G.choppy & G.ret60.notna()].copy()
    N["tr"] = np.where(N.ret60 > 0.1, "rising", "falling")
    N["rq"] = pd.qcut(N.rngpos, 3, labels=False)
    out["nonchoppy trend x agit x rngpos"] = ttab(N, ["tr", "agit", "rq"])
    out["falling rngpos slope by year"] = pd.DataFrame({y: slope_t(N[(N.tr == "falling") & (N.year == y)], "rngpos") for y in sorted(N.year.unique())}).T
    out["choppy agit share of grid"] = float(len(CA) / len(G))
    return out
