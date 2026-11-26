def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = (h - l)
            mr = rng.rolling(20, min_periods=20).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret5": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret60": c / c.shift(60) - 1,
                "wide": rng / mr,
                "flat": 1 - (c - o).abs() / rng.replace(0, np.nan),
                "clv": (c - l) / rng.replace(0, np.nan),
                "body": (c - o) / mr,
                "volr": v / v.rolling(20, min_periods=20).mean(),
                "fwd3": c.shift(-3) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "pos": np.arange(len(b)),
                "fc": b["forecast"].astype(float),
            })
            df = df[df["pos"] % 3 == 0]
            recs.append(df)
        cd = pd.concat(recs)
        cd["unus"] = cd["fwd3"] - cd["fwd3"].mean()
        rows.append(cd)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["unus", "wide", "ret5"])
    D["year"] = D["day"].dt.year

    def stat(g):
        g = g.dropna(subset=["unus"])
        if len(g) < 5:
            return pd.Series({"n": len(g), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = g["unus"].mean()
        dev = (g["unus"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    U = D[D["ret5"] > 0]
    out["up-run: wide bucket"] = U.groupby(pd.cut(U["wide"], [0, 1, 1.5, 2, 3, 99])).apply(stat)
    Dn = D[D["ret5"] <= 0]
    out["down-run: wide bucket"] = Dn.groupby(pd.cut(Dn["wide"], [0, 1, 1.5, 2, 3, 99])).apply(stat)
    P = D[D["ret20"] > 0]
    out["ret20>0: wide bucket"] = P.groupby(pd.cut(P["wide"], [0, 1, 1.5, 2, 3, 99])).apply(stat)
    Nn = D[D["ret20"] <= 0]
    out["ret20<=0: wide bucket"] = Nn.groupby(pd.cut(Nn["wide"], [0, 1, 1.5, 2, 3, 99])).apply(stat)
    W = D[D["wide"] >= 1.5]
    out["wide: ret20 quintile"] = W.groupby(pd.qcut(W["ret20"], 5)).apply(stat)
    out["wide: ret60 sign"] = W.groupby(np.sign(W["ret60"])).apply(stat)
    out["wide: signed body bucket"] = W.groupby(pd.cut(W["body"], [-99, -1, -0.3, 0.3, 1, 99])).apply(stat)
    out["wide: volume ratio tercile"] = W.groupby(pd.qcut(W["volr"], 3)).apply(stat)
    out["wide&ret20>0 by year"] = W[W["ret20"] > 0].groupby("year").apply(stat)
    # forecast of the book on active bars
    A = D[D["fc"] > 0]
    out["book fc>0: fc tercile"] = A.groupby(pd.qcut(A["fc"], 3, duplicates="drop")).apply(stat)
    # book daily returns: largest gains/losses and what precedes
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dd.append(d)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book days: n, mean, share of gain from top 5% days"] = pd.Series({
        "n": len(bk), "mean": bk.mean(),
        "top5_share": bk[bk >= bk.quantile(.95)].sum() / bk.sum(),
        "bottom5_share": bk[bk <= bk.quantile(.05)].sum() / bk.sum()})
    return out
