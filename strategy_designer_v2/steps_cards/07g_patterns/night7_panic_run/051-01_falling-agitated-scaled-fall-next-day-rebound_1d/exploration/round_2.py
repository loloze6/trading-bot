def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "z": r / sd30,
                "inprof": (b["regime"] == "unknown"),
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1,
                "ret60": c / c.shift(60) - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r"].mean()
    D["u1"] = D["n1"] - D["coin"].map(drift)
    D["u2"] = D["n2"] - 2 * D["coin"].map(drift)
    D["yr"] = D["day"].dt.year
    D["trend"] = np.where(D.ret60 > 0.10, "rising", np.where(D.ret60 < -0.10, "falling", np.where(D.ret60.notna(), "choppy", "na")))

    def pooled(sub, col):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 5:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        m = s[col].mean()
        g = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        Dd = len(g)
        se = np.sqrt(Dd / (Dd - 1) * (g ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se, "days": Dd})

    def slope(sub, x, y):
        s = sub.dropna(subset=[x, y])
        X = s[x] - s[x].mean(); Y = s[y]
        b = (X * Y).sum() / (X ** 2).sum()
        e = Y - Y.mean() - b * X
        g = (X * e).groupby(s["day"]).sum()
        Dd = len(g)
        se = np.sqrt(Dd / (Dd - 1) * (g ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(s), "slope%": 100 * b, "t": b / se, "days": Dd})

    out = {}
    P = D[D.inprof]
    out["in profile, up days u1"] = pooled(P[P.r > 0], "u1")
    out["in profile, up days slope u1 on z"] = slope(P[P.r > 0], "z", "u1")
    out["in profile, up days u1 by year"] = P[P.r > 0].groupby("yr").apply(lambda s: pooled(s, "u1"))
    out["in profile, up days u1 by coin"] = P[P.r > 0].groupby("coin").apply(lambda s: pooled(s, "u1"))
    out["in profile, all days slope u1 on z"] = slope(P, "z", "u1")
    out["in profile, down days slope u1 on z"] = slope(P[P.r < 0], "z", "u1")
    # close position
    D["lowclose"] = 1 - D["clpos"]
    out["all days slope u1 on (1-clpos)"] = slope(D, "lowclose", "u1")
    out["down days slope u1 on (1-clpos)"] = slope(D[D.r < 0], "lowclose", "u1")
    out["in profile slope u1 on (1-clpos)"] = slope(P, "lowclose", "u1")
    out["out profile slope u1 on (1-clpos)"] = slope(D[~D.inprof], "lowclose", "u1")
    D["cpb"] = pd.cut(D["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["all days u1 by close pos"] = D.groupby("cpb", observed=True).apply(lambda s: pooled(s, "u1"))
    out["low close (<0.2) u1 by year"] = D[D.clpos <= 0.2].groupby("yr").apply(lambda s: pooled(s, "u1"))
    # falls by own trend (out of profile too)
    dn = D[D.z < -1]
    out["z<-1 u1 by trend (all)"] = dn.groupby("trend").apply(lambda s: pooled(s, "u1"))
    out["z<-1 out-profile u1 by trend"] = dn[~dn.inprof].groupby("trend").apply(lambda s: pooled(s, "u1"))
    # 2-day horizon of in-profile falls, grid 2
    G = P[(P.pos % 2 == 0) & (P.r < 0)]
    out["in profile down days u2 grid2"] = pooled(G, "u2")
    out["in profile down days slope u2 on z grid2"] = slope(G, "z", "u2")
    return out
