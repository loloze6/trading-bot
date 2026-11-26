def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "fa": (b["regime"] == "unknown").astype(int),
                "s1": r1 / vol,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1, "vol": vol,
            })
            d["s5"] = d["r5"] / (vol * np.sqrt(5))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["yr"] = D["ts"].dt.year
    for h in (1, 2, 3):
        dr = D[D.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(dr)

    def clslope(g, x, y):
        g = g.dropna(subset=[x, y])
        xx = g[x].clip(-4, 4); yy = g[y]
        n = len(g)
        if n < 10: return pd.Series({"n": n})
        xm = xx - xx.mean()
        b = (xm * (yy - yy.mean())).sum() / (xm ** 2).sum()
        res = yy - yy.mean() - b * xm
        sc = (xm * res).groupby(g["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (xm ** 2).sum()
        return pd.Series({"n": n, "days": g.day.nunique(), "slope%": 100 * b, "t_day": b / se})

    out = {}
    res = {}
    for h in (1, 2, 3):
        G = D[D.pos % h == 0]
        for side, sub in (("all", G), ("up", G[G.s1 > 0]), ("down", G[G.s1 <= 0])):
            for fa in (0, 1):
                res[(h, side, fa)] = clslope(sub[sub.fa == fa], "s1", f"u{h}")
    out["slope u_h on s1, day-clustered"] = pd.DataFrame(res).T
    # by year, fa, h=3, all & up
    ry = {}
    G = D[D.pos % 3 == 0]
    for (fa, y), g in G.groupby(["fa", "yr"]):
        ry[(fa, y, "all")] = clslope(g, "s1", "u3")
        ry[(fa, y, "up")] = clslope(g[g.s1 > 0], "s1", "u3")
    out["slope u3 on s1 by year"] = pd.DataFrame(ry).T
    # s5 continuation outside profile, clustered
    rs = {}
    for h in (1, 3):
        G = D[D.pos % h == 0]
        for fa in (0, 1):
            rs[(h, fa)] = clslope(G[G.fa == fa], "s5", f"u{h}")
        for y, g in G[G.fa == 0].groupby("yr"):
            rs[(h, "fa0", y)] = clslope(g, "s5", f"u{h}")
    out["slope u_h on s5"] = pd.DataFrame(rs).T
    # fa up days by s1 quantile, next 1 day and 3 days
    U = D[(D.fa == 1) & (D.s1 > 0)].dropna(subset=["u1"])
    U = U.assign(q=pd.qcut(U.s1, 4, labels=False))
    def ct(g, col):
        g = g.dropna(subset=[col]); n = len(g); m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum(); se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": g.day.nunique(), "mean%": 100 * m, "t": m / se, "s1mean": g.s1.mean()})
    out["fa up days by s1 quartile u1"] = U.groupby("q").apply(lambda g: ct(g, "u1"))
    out["fa up days by s1 quartile u2"] = U.groupby("q").apply(lambda g: ct(g, "u2"))
    return out
