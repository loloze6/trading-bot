def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            n = len(d)
            pos = np.arange(n)
            out = pd.DataFrame({
                "coin": coin, "win": w, "pos": pos,
                "r1": r1.values, "vol": vol.values, "z": (r1 / vol).values,
                "r5": (c / c.shift(5) - 1).values,
                "r20": (c / c.shift(20) - 1).values,
                "dd20": (c / c.rolling(20, min_periods=10).max() - 1).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f3": (c.shift(-3) / c - 1).values,
                "f10": (c.shift(-10) / c - 1).values,
                "regime": d["regime"].values,
                "alloc": d["postRebalance_current_allocation"].astype(float).values,
                "fc": d["forecast"].astype(float).values,
                "wd": d["ts"].dt.weekday.values,
            })
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["trend"] = (A["regime"] == "trending").astype(int)
    res = {}
    # drift per coin, 10-bar and 1/3-bar grids
    for h in (1, 3, 10):
        g = A[(A["pos"] % h == 0)]
        dr = g.groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    G10 = A[A["pos"] % 10 == 0].dropna(subset=["u10", "z"])
    G3 = A[A["pos"] % 3 == 0].dropna(subset=["u3", "z"])
    G1 = A.dropna(subset=["u1", "z"])

    def summ(df, col, by):
        g = df.groupby(by, observed=True)[col]
        t = g.agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["count", "mean", "t"]].round(4)

    zb = [-99, -2, -1, 0, 1, 2, 99]
    for G, h in ((G10, 10), (G3, 3), (G1, 1)):
        G = G.copy()
        G["zb"] = pd.cut(G["z"], zb)
        res[f"u{h} by z bin x trend"] = summ(G, f"u{h}", ["trend", "zb"])
    # vol level quintile within coin
    G = G10.copy()
    G["volq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["u10 by vol quintile"] = summ(G, "u10", "volq")
    G["r20q"] = G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["u10 by r20 quintile"] = summ(G.dropna(subset=["r20"]), "u10", "r20q")
    G["dd"] = G.groupby("coin")["dd20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["u10 by dist from 20d high quintile"] = summ(G.dropna(subset=["dd20"]), "u10", "dd")
    G["r5q"] = G.groupby("coin")["r5"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["u10 by r5 quintile x trend"] = summ(G.dropna(subset=["r5"]), "u10", ["trend", "r5q"])
    # weekday next-day
    res["u1 by weekday"] = summ(G1, "u1", "wd")
    # by coin trend regime
    res["u10 by coin x trend"] = summ(G10, "u10", ["coin", "trend"])
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day", "book_return", "coin_return"]].copy()
            x["win"] = w; x["coin"] = coin
            dl.append(x)
    D = pd.concat(dl, ignore_index=True)
    B = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book daily"] = pd.Series({"n": len(B), "mean": B.book_return.mean(), "std": B.book_return.std(),
                                   "coin_mean": B.coin_return.mean(),
                                   "corr_book_coin": B.corr().iloc[0, 1]}).round(5)
    q = B.book_return.quantile([0.02, 0.98])
    res["book extreme days coin return"] = pd.DataFrame({
        "top2pct_book": B[B.book_return >= q.iloc[1]].mean(),
        "bot2pct_book": B[B.book_return <= q.iloc[0]].mean()}).round(4)
    # allocation vs next-day
    res["alloc share active, mean u1 when long vs flat"] = summ(G1.assign(on=(G1.alloc.abs() > 0.01).astype(int)), "u1", "on")
    return res
