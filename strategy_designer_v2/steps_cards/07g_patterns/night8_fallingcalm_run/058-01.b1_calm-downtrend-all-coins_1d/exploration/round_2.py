def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "inprof": (b["regime"] == "unknown").astype(int),
                "r30": c / c.shift(30) - 1,
                "r1": r1, "r3p": c / c.shift(3) - 1,
                "r5p": c / c.shift(5) - 1, "r10p": c / c.shift(10) - 1,
                "vol20": r1.rolling(20).std(),
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
            })
            df["pos"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["yr"] = A["ts"].dt.year
    drift = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    A["z1"] = A["r1"] / A["vol20"]
    A["z5"] = A["r5p"] / (A["vol20"] * np.sqrt(5))
    G = A[A.pos % 5 == 0].dropna(subset=["ex5"]).copy()
    G["prof"] = np.where(G.inprof == 1, "fallcalm", "other")

    def ct(g, col="ex5"):
        x = g.dropna(subset=[col])
        d = x.groupby("day")[col].sum()
        n = len(x); m = x[col].mean()
        nd = len(d)
        se = np.sqrt(((d - x.groupby("day")[col].size() * m) ** 2).sum()) / n
        return pd.Series({"n": n, "days": nd, "mean": m, "t_day": m / se if se > 0 else np.nan})

    def slope(g, xc, yc="ex5"):
        x = g.dropna(subset=[xc, yc]).copy()
        X = x[xc] - x[xc].mean(); Y = x[yc] - x[yc].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        s = (X * e).groupby(x["day"]).sum()
        G_ = len(s)
        var = (s ** 2).sum() / (X * X).sum() ** 2 * G_ / (G_ - 1)
        return pd.Series({"n": len(x), "days": G_, "slope": b, "t_day": b / np.sqrt(var)})

    out = {}
    res = {}
    for p, g in G.groupby("prof"):
        for xc in ["z1", "z5", "r5p", "r3p", "r10p", "r30"]:
            res[(p, xc)] = slope(g, xc)
    out["clustered slopes ex5 on past moves"] = pd.DataFrame(res).T
    P = G[G.prof == "fallcalm"].copy()
    P["z1q"] = pd.qcut(P["z1"], 5, labels=False)
    out["fallcalm z1 quintile clustered"] = P.groupby("z1q").apply(ct)
    out["fallcalm z1 q bounds"] = P.groupby("z1q")["z1"].agg(["min", "max"])
    P["z5q"] = pd.qcut(P["z5"], 5, labels=False)
    out["fallcalm z5 quintile clustered"] = P.groupby("z5q").apply(ct)
    out["fallcalm z5 slope by year"] = pd.DataFrame({y: slope(g, "z5") for y, g in P.groupby("yr") if len(g) > 30}).T
    O = G[G.prof == "other"]
    out["other z5 slope by year"] = pd.DataFrame({y: slope(g, "z5") for y, g in O.groupby("yr") if len(g) > 30}).T
    # weekday, clustered across days (mean of coins per day)
    A1 = A.dropna(subset=["fwd1"]).copy()
    A1["wd"] = A1["ts"].dt.dayofweek
    out["fwd1 by weekday clustered"] = A1.groupby("wd").apply(lambda g: ct(g, "fwd1"))
    A1["prof"] = np.where(A1.inprof == 1, "fallcalm", "other")
    out["fwd1 by weekday x prof clustered t"] = A1.groupby(["prof", "wd"]).apply(lambda g: ct(g, "fwd1"))["t_day"].unstack(0)
    out["fwd1 weekday mean by year (Thu+Fri minus rest)"] = A1.groupby("yr").apply(
        lambda g: g[g.wd.isin([3, 4])]["fwd1"].mean() - g[~g.wd.isin([3, 4])]["fwd1"].mean())
    # leave-one-coin-out for fallcalm z5 slope
    out["fallcalm z5 slope leave one coin out"] = pd.DataFrame({c: slope(P[P.coin != c], "z5") for c in P.coin.unique()}).T
    return out
