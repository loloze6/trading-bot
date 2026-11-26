def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
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
                "fc": b["forecast"].astype(float),
                "r30": c / c.shift(30) - 1,
                "r1": r1,
                "r5p": c / c.shift(5) - 1,
                "vol20": r1.rolling(20).std(),
                "vrat": v.rolling(10).mean() / v.rolling(60, min_periods=30).mean(),
                "vday": v / v.rolling(30).mean(),
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
            })
            df["pos"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    A["z1"] = A["r1"] / A["vol20"].shift(0)
    G = A[(A.pos % 5 == 0)].dropna(subset=["ex5"]).copy()

    def summ(g, col="ex5"):
        x = g[col].dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": x.mean(), "t": t})

    out = {}
    G["prof"] = np.where(G.inprof == 1, "fallcalm", "other")
    G["r30q"] = G.groupby("prof")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex5 by profile x r30 quintile"] = G.groupby(["prof", "r30q"]).apply(summ).unstack(0)
    P = G[G.inprof == 1].dropna(subset=["vrat", "r30"]).copy()
    P["vq"] = pd.qcut(P["vrat"], 3, labels=["lowvol", "midvol", "highvol"])
    P["deep"] = np.where(P["r30"] < P["r30"].median(), "deep", "shallow")
    out["fallcalm ex5 by volume tercile x depth"] = P.groupby(["vq", "deep"]).apply(summ)
    G["z1q"] = pd.qcut(G["z1"], 5, labels=False)
    out["ex5 by prior-day z quintile x profile"] = G.groupby(["prof", "z1q"]).apply(summ).unstack(0)
    G["r5q"] = G.groupby("prof")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex5 by past-5d return quintile x profile"] = G.groupby(["prof", "r5q"]).apply(summ).unstack(0)
    G["vdq"] = pd.qcut(G["vday"], 5, labels=False, duplicates="drop")
    out["ex5 by day volume quintile x profile"] = G.groupby(["prof", "vdq"]).apply(summ).unstack(0)
    # weekday daily returns all bars
    A["wd"] = A["ts"].dt.dayofweek
    out["fwd1 by weekday"] = A.dropna(subset=["fwd1"]).groupby("wd").apply(lambda g: summ(g, "fwd1"))
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bd = D.groupby("day")["book_return"].mean().dropna()
    out["book daily: n, mean, std"] = pd.Series({"n": len(bd), "mean": bd.mean(), "std": bd.std()})
    A["yr"] = A["ts"].dt.year
    G["yr"] = G["ts"].dt.year
    out["fallcalm ex5 by year"] = G[G.inprof == 1].groupby("yr").apply(summ)
    out["share in profile by coin"] = A.groupby("coin")["inprof"].mean()
    return out
