def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            clv = (c - l) / rng.replace(0, np.nan)
            r0 = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": clv, "r0": r0,
                "body": (c - o) / o,
                "rngrel": (rng / c) / (rng / c).rolling(20, min_periods=10).mean(),
                "ret60": c / c.shift(60) - 1,
                "ret20": c / c.shift(20) - 1,
                "vol20": r0.rolling(20, min_periods=10).std(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
            })
            d["vol20rel"] = d["vol20"] / d["vol20"].rolling(60, min_periods=30).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f2", "f3"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["sig"] = 0.5 - D["clv"]  # + near low
    D["day"] = D["ts"].dt.floor("D")
    out = {}

    def tday(df, col):
        s = df.groupby("day")[col].sum()
        s = s.dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "days": len(s)})

    def bucket_tab(df, by, col="f1x"):
        g = df.dropna(subset=[col]).groupby(by)[col]
        return pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100,
                             "t": g.mean() / (g.std() / np.sqrt(g.size()))})

    D["clvq"] = pd.qcut(D["clv"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out["clv quintile next-day excess"] = bucket_tab(D, "clvq")
    # 2 and 3 day non-overlapping
    for hh, col in [(2, "f2x"), (3, "f3x")]:
        sub = D[D["pos"] % hh == 0]
        out[f"clv quintile {hh}d excess (grid)"] = bucket_tab(sub, "clvq", col)
    # day's return direction x clv
    D["r0q"] = pd.qcut(D["r0"], 5, labels=["r_bigdown", "r2", "r3", "r4", "r_bigup"])
    t = D.dropna(subset=["f1x"]).groupby(["r0q", "clvq"])["f1x"].mean().unstack() * 100
    out["mean next-day excess % by day-return q x clv q"] = t
    out["next-day excess by day-return quintile"] = bucket_tab(D, "r0q")
    # signed product sig*f1x per day: slope by regime splits
    D["p"] = D["sig"] * D["f1x"]
    D["rngq"] = pd.qcut(D["rngrel"], 3, labels=["narrow", "mid", "wide"])
    out["sig*f1x by range width"] = D.dropna(subset=["p", "rngq"]).groupby("rngq").apply(lambda x: tday(x, "p"))
    D["tr"] = pd.cut(D["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    out["sig*f1x by 60d trend"] = D.dropna(subset=["p", "tr"]).groupby("tr").apply(lambda x: tday(x, "p"))
    D["ag"] = np.where(D["vol20rel"] > 1, "agitated", "calm")
    out["sig*f1x by agitation(rel)"] = D.dropna(subset=["p", "vol20rel"]).groupby("ag").apply(lambda x: tday(x, "p"))
    out["sig*f1x by coin"] = D.dropna(subset=["p"]).groupby("coin").apply(lambda x: tday(x, "p"))
    out["sig*f1x by year"] = D.dropna(subset=["p"]).assign(y=D["ts"].dt.year).groupby("y").apply(lambda x: tday(x, "p"))
    D["wd"] = D["ts"].dt.dayofweek
    out["sig*f1x by weekday of signal"] = D.dropna(subset=["p"]).groupby("wd").apply(lambda x: tday(x, "p"))
    out["next-day excess by weekday of signal"] = bucket_tab(D, "wd")
    # book daily
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, win=w))
    B = pd.concat(bd, ignore_index=True)
    B["day"] = pd.to_datetime(B["day"])
    bk = B.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = bk.index.dayofweek
    out["book daily by weekday"] = bk.groupby("wd")["book_return"].agg(["mean", "count"]).assign(t=lambda x: x["mean"] / (bk.groupby("wd")["book_return"].std() / np.sqrt(x["count"])))
    out["book corr with coin day"] = float(bk["book_return"].corr(bk["coin_return"]))
    return out
