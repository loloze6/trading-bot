def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.shift(-1) / c - 1
            d["r2"] = c.shift(-2) / c - 1
            d["pos2"] = np.arange(len(c)) % 2 == 0
            d["prev1"] = c / c.shift(1) - 1
            d["g20"] = c / c.shift(20) - 1
            d["g5"] = c / c.shift(5) - 1
            d["vol20"] = d["prev1"].rolling(20).std()
            d["nextwd"] = (d["ts"] + pd.Timedelta(days=1)).dt.weekday
            d["year"] = d["ts"].dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu1)
    lo, hi = D["x1"].quantile([0.01, 0.99])
    D["x1w"] = D["x1"].clip(lo, hi)
    D["g20s"] = D["g20"] / (D["vol20"] * np.sqrt(20))
    D["p1s"] = D["prev1"] / D["vol20"]

    def cslope(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        n = len(g)
        if n < 30: return pd.Series({"n": n})
        x = g[xcol] - g[xcol].mean(); y = g[ycol]
        b = (x * y).sum() / (x ** 2).sum()
        e = y - y.mean() - b * x
        s = (x * e).groupby(g["ts"]).sum()
        se = np.sqrt((s ** 2).sum()) / (x ** 2).sum()
        rho, p = stats.spearmanr(g[xcol], g[ycol])
        return pd.Series({"n": n, "slope": b, "t_clust": b / se, "spearman": rho, "days": s.size})

    out = {}
    pos = D[D.g20 > 0]; neg = D[D.g20 <= 0]
    out["pos_g20s_wins_by_nextwd"] = pos.groupby("nextwd").apply(lambda g: cslope(g, "g20s", "x1w"))
    out["neg_g20s_wins_by_nextwd"] = neg.groupby("nextwd").apply(lambda g: cslope(g, "g20s", "x1w"))
    out["all_g20s_wins_by_nextwd"] = D.groupby("nextwd").apply(lambda g: cslope(g, "g20s", "x1w"))
    fri = D[(D.nextwd == 4)]
    out["thu_close_pos_by_coin"] = fri[fri.g20 > 0].groupby("coin").apply(lambda g: cslope(g, "g20s", "x1w"))
    out["thu_close_pos_by_year"] = fri[fri.g20 > 0].groupby("year").apply(lambda g: cslope(g, "g20s", "x1w"))
    sat = D[D.nextwd == 5]
    out["sat_neg_by_coin"] = sat[sat.g20 <= 0].groupby("coin").apply(lambda g: cslope(g, "g20s", "x1w"))
    out["sat_neg_by_year"] = sat[sat.g20 <= 0].groupby("year").apply(lambda g: cslope(g, "g20s", "x1w"))
    # Thursday close -> two days (Fri+Sat)
    th = D[D.nextwd == 4].copy()
    mu2 = D[D.pos2].groupby("coin")["r2"].mean()
    th["x2"] = th["r2"] - th["coin"].map(mu2)
    out["thu_close_2day_all_g20s"] = cslope(th, "g20s", "x2").to_frame().T
    # 1-day reversal after large down day, graded, by weekday
    out["p1s_by_nextwd"] = D.groupby("nextwd").apply(lambda g: cslope(g, "p1s", "x1w"))
    out["p1s_all"] = cslope(D, "p1s", "x1w").to_frame().T
    out["p1s_down_only"] = cslope(D[D.prev1 < 0], "p1s", "x1w").to_frame().T
    out["p1s_up_only"] = cslope(D[D.prev1 > 0], "p1s", "x1w").to_frame().T
    out["p1s_down_by_year"] = D[D.prev1 < 0].groupby("year").apply(lambda g: cslope(g, "p1s", "x1w"))
    # book by weekday of the day
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; bk.append(dd)
    B = pd.concat(bk)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_weekday_%"] = (B.groupby("wd")[["book_return", "coin_return"]].mean() * 100)
    out["book_by_year_%"] = (B.groupby("year")[["book_return", "coin_return"]].mean() * 100)
    return out
