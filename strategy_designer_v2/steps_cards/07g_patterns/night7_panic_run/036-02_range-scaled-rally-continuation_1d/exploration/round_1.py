def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            n = len(d)
            rr = ((h - l) / c).rolling(30, min_periods=10).mean()
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=10).std()
            r3 = c / c.shift(3) - 1
            r7p = c / c.shift(7) - 1
            r14p = c / c.shift(14) - 1
            r30p = c / c.shift(30) - 1
            fwd7 = c.shift(-7) / c - 1
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(d["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                              "fc": d["forecast"].astype(float), "alloc": d["postRebalance_current_allocation"].astype(float),
                              "s3r": r3 / rr, "s3v": r3 / sd30, "r1s": r1 / sd30, "r7p": r7p / sd30, "r14p": r14p / sd30,
                              "r30p": r30p, "vol": sd30, "fwd7": fwd7, "fwd3": fwd3, "fwd1": fwd1,
                              "wd": ts.dt.weekday, "yr": ts.dt.year, "rrng": ((h - l) / c) / rr,
                              "clv": (c - l) / (h - l).replace(0, np.nan)})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    # coin mean 7-bar return over non-overlapping grid
    G7 = A[(A.pos % 7 == 0)].dropna(subset=["fwd7"]).copy()
    m7 = G7.groupby("coin")["fwd7"].mean()
    G7["ex7"] = G7["fwd7"] - G7["coin"].map(m7)
    G3 = A[(A.pos % 3 == 0)].dropna(subset=["fwd3"]).copy()
    G3["ex3"] = G3["fwd3"] - G3["coin"].map(G3.groupby("coin")["fwd3"].mean())
    G1 = A.dropna(subset=["fwd1"]).copy()
    G1["ex1"] = G1["fwd1"] - G1["coin"].map(G1.groupby("coin")["fwd1"].mean())

    def tab(G, col, y, q=5):
        G = G.dropna(subset=[col, y]).copy()
        G["b"] = G.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        o = G.groupby("b")[y].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.round(4)
    def slope(G, col, y):
        G = G.dropna(subset=[col, y])
        r = stats.linregress(G[col], G[y]); return round(r.slope / r.stderr, 2)
    out = {}
    out["s3r quint ex7"] = tab(G7, "s3r", "ex7")
    out["s3v quint ex7"] = tab(G7, "s3v", "ex7")
    out["r14p quint ex7"] = tab(G7, "r14p", "ex7")
    out["r30p quint ex7"] = tab(G7, "r30p", "ex7")
    out["vol quint ex7"] = tab(G7, "vol", "ex7")
    out["r1s quint ex1"] = tab(G1, "r1s", "ex1", 10)
    out["r1s quint ex3"] = tab(G3, "r1s", "ex3", 5)
    out["clv quint ex3"] = tab(G3, "clv", "ex3", 5)
    out["rrng quint ex3"] = tab(G3, "rrng", "ex3", 5)
    out["slopes t"] = pd.Series({"s3r->ex7": slope(G7, "s3r", "ex7"), "r14p->ex7": slope(G7, "r14p", "ex7"),
                                 "r30p->ex7": slope(G7, "r30p", "ex7"), "r1s->ex1": slope(G1, "r1s", "ex1"),
                                 "r1s->ex3": slope(G3, "r1s", "ex3"), "vol->ex7": slope(G7, "vol", "ex7")})
    wd = G1.groupby("wd")["ex1"].agg(["count", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday ex1"] = wd.round(5)
    # trend profile within window (r30p as 60d not available often)
    G7["tr"] = pd.cut(G7["r30p"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    G7["pos3"] = G7["s3r"] > 0
    pt = G7.groupby(["tr", "pos3"])["ex7"].agg(["count", "mean", "std"]); pt["t"] = pt["mean"] / (pt["std"] / np.sqrt(pt["count"]))
    out["trend30 x rally ex7"] = pt.round(4)
    # book
    D = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; D.append(x)
    D = pd.concat(D, ignore_index=True)
    bw = D.groupby("w")[["book_return", "coin_return"]].mean()
    out["book by window"] = (bw * 100).round(4)
    bc = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean"])
    out["book by coin"] = (bc * 100).round(4)
    return out
