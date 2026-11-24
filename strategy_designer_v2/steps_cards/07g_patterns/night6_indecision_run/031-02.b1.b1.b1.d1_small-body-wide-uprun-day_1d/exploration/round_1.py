def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        # pooled grid drift per coin
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            mr = rng.rolling(20, min_periods=20).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret5": c / c.shift(5) - 1,
                "ret1": c / c.shift(1) - 1,
                "ret20": c / c.shift(20) - 1,
                "wide": rng / mr,
                "flat": 1 - (c - o).abs() / rng.replace(0, np.nan),
                "clv": (c - l) / rng.replace(0, np.nan),
                "green": np.sign(c - o),
                "vol20": c.pct_change().rolling(20, min_periods=20).std(),
                "fwd3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
                "regime": b["regime"],
            })
            df = df[df["pos"] % 3 == 0]
            recs.append(df)
        cd = pd.concat(recs)
        drift = cd["fwd3"].mean()
        cd["unus"] = cd["fwd3"] - drift
        rows.append(cd)
    D = pd.concat(rows).dropna(subset=["unus"])
    D["year"] = D["day"].dt.year
    D["wd"] = D["day"].dt.weekday

    def stat(g):
        g = g.dropna(subset=["unus"])
        if len(g) < 5:
            return pd.Series({"n": len(g), "days": 0, "mean": np.nan, "t": np.nan})
        per = g.groupby("day")["unus"].sum()
        nd = len(per)
        m = g["unus"].mean()
        se = np.sqrt((per - per.sum() / len(g) * g.groupby("day").size()).pow(2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    out["all"] = stat(D)
    W = D[(D["wide"] >= 1.5)]
    W = W.assign(run=np.where(W["ret5"] > 0, "up", "down"), fl=np.where(W["flat"] >= 0.5, "flat", "body"))
    out["wide by run x flat"] = W.groupby(["run", "fl"]).apply(stat)
    N = D[(D["wide"] < 1.0) & (D["flat"] >= 0.5)]
    out["narrow flat by run"] = N.assign(run=np.where(N["ret5"] > 0, "up", "down")).groupby("run").apply(stat)
    out["wide buckets all"] = D.groupby(pd.cut(D["wide"], [0, .6, .8, 1, 1.25, 1.5, 2, 3, 99])).apply(stat)
    WU = W[W["run"] == "up"]
    out["wide up: clv buckets"] = WU.groupby(pd.cut(WU["clv"], [-.01, .2, .4, .6, .8, 1.01])).apply(stat)
    out["wide up: green/red"] = WU.groupby("green").apply(stat)
    out["ret5 quintile all"] = D.groupby(pd.qcut(D["ret5"], 5)).apply(stat)
    out["ret1 decile all"] = D.groupby(pd.qcut(D["ret1"], 10)).apply(stat)
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["wide up by vol quartile"] = WU.assign(vq=D.loc[WU.index.intersection(D.index), "vq"] if False else None).pipe(lambda x: x).shape[0]
    WU2 = D[(D["wide"] >= 1.5) & (D["ret5"] > 0)]
    out["wide up by volq"] = WU2.groupby("vq").apply(stat)
    out["wide up by ret20 sign"] = WU2.groupby(np.sign(WU2["ret20"])).apply(stat)
    out["wide up by year"] = WU2.groupby("year").apply(stat)
    out["weekday all"] = D.groupby("wd").apply(stat)
    return out
