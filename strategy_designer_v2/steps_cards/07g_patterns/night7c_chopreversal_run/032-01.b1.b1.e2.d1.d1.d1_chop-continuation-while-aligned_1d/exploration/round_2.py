def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            vol = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "year": ts.dt.year, "r1": r1, "z1": r1 / vol, "er": er,
                               "s7": r7 / (vol * np.sqrt(7)), "vol": vol,
                               "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f7": c.shift(-7) / c - 1,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "regime": b["regime"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D.f1 - D.coin.map(D.groupby("coin")["f1"].mean())
    D["x2"] = D.f2 - D.coin.map(D[D.pos % 2 == 0].groupby("coin")["f2"].mean())
    D["x7"] = D.f7 - D.coin.map(D[D.pos % 7 == 0].groupby("coin")["f7"].mean())
    D["volq"] = D.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))

    def ct(s, col):
        s = s.dropna(subset=[col]); g = s.groupby("day")[col].sum(); n = len(s); nd = len(g)
        if nd < 5: return (np.nan, np.nan, n, nd)
        m = s[col].mean(); se = g.std(ddof=1) * np.sqrt(nd) / n
        return (m, m / se, n, nd)

    def slope(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 20: return {"slope": np.nan, "t": np.nan, "n": len(s)}
        xx = s[x] - s[x].mean()
        b = (xx * s[y]).sum() / (xx ** 2).sum()
        e = s[y] - s[y].mean() - b * xx
        g = (xx * e).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (xx ** 2).sum()
        return {"slope": b, "t": b / se, "n": len(s), "days": s.day.nunique()}

    res = {}
    G1 = D[D.pos >= 30].dropna(subset=["z1", "x1"]).copy()
    G1["dz"] = -G1.z1.clip(-4, 4)  # reversal side
    G1["rev1"] = -np.sign(G1.z1) * G1.x1
    out = {}
    out["all"] = slope(G1, "z1", "x1")
    for k, g in G1.groupby("volq"): out[f"vol{k}"] = slope(g, "z1", "x1")
    for k, g in G1.groupby("year"): out[f"y{k}"] = slope(g, "z1", "x1")
    for k, g in G1.groupby("coin"): out[k] = slope(g, "z1", "x1")
    G1["erq"] = pd.qcut(G1.er, 3, labels=False)
    for k, g in G1.groupby("erq"): out[f"er{k}"] = slope(g, "z1", "x1")
    res["slope next-day excess on z1 (clip none)"] = pd.DataFrame(out).T
    # down-day vs up-day asymmetry
    G1["zq"] = pd.qcut(G1.z1, 7, labels=False)
    a = {}
    for (v, q), g in G1.groupby(["volq", "zq"]):
        if q in (0, 6):
            m, t, n, nd = ct(g, "x1"); a[f"vol{v}_z{q}"] = {"mean": m, "t": t, "n": n, "days": nd}
    res["extreme z1 septiles by vol tercile, next-day excess"] = pd.DataFrame(a).T
    G2 = D[(D.pos >= 30) & (D.pos % 2 == 0)].dropna(subset=["z1", "x2"])
    res["slope 2-day excess on z1"] = pd.DataFrame({"all": slope(G2, "z1", "x2")}).T
    # weekly continuation by vol
    G7 = D[D.pos % 7 == 0].dropna(subset=["s7", "x7"])
    o = {}
    for k, g in G7.groupby("volq"): o[f"vol{k}"] = slope(g, "s7", "x7")
    o["all"] = slope(G7, "s7", "x7")
    for k, g in G7.groupby("year"): o[f"y{k}"] = slope(g, "s7", "x7")
    res["slope 7d excess on s7 by vol tercile/year"] = pd.DataFrame(o).T
    # book gain by ER within positions, by year
    D["gain"] = D.alloc * D.f1
    P = D[D.alloc.abs() > 1e-9].dropna(subset=["gain", "er"]).copy()
    P["erq"] = pd.qcut(P.er, 3, labels=False)
    b = {}
    for (y, q), g in P.groupby(["year", "erq"]):
        m, t, n, nd = ct(g, "gain"); b[f"y{y}_er{q}"] = {"mean": m, "t": t, "n": n}
    res["book gain by year x ER tercile"] = pd.DataFrame(b).T
    res["ER tercile edges among positions"] = pd.Series(P.er.quantile([0, 1/3, 2/3, 1]).values)
    return res
