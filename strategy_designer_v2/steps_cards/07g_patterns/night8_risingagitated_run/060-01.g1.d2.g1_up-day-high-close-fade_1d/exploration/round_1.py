def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": (c - l) / rng,
                "r1": c / c.shift(1) - 1,
                "body": (c - o) / rng,
                "rngrel": rng / c,
                "nxt": c.shift(-1) / c - 1,
                "regime": b["regime"].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "year": pd.to_datetime(b["timestamp"]).dt.year.values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
            })
            df["r5"] = c / c.shift(5) - 1
            df["unus"] = df["nxt"] - drift
            df["vol20"] = df["r1"].rolling(20).std()
            df["rngz"] = df["rngrel"] / df["rngrel"].rolling(20).mean()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "loc", "r1"])
    d["inprof"] = d["regime"] != "chop"

    def summ(g):
        x = g["unus"]
        return pd.Series({"n": len(x), "mean_unus": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    d["locq"] = pd.cut(d["loc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    d["up"] = d["r1"] > 0
    out = {}
    out["regime counts"] = d["regime"].value_counts()
    out["in profile: loc bin x up"] = d[d.inprof].groupby(["up", "locq"]).apply(summ)
    out["out profile: loc bin x up"] = d[~d.inprof].groupby(["up", "locq"]).apply(summ)
    d["r1q"] = pd.qcut(d["r1"], 5)
    out["in profile: r1 quintile"] = d[d.inprof].groupby("r1q").apply(summ)
    out["out profile: r1 quintile"] = d[~d.inprof].groupby("r1q").apply(summ)
    d["rngq"] = pd.qcut(d["rngz"], 4)
    sub = d[d.inprof & d.up & (d["loc"] > .5)]
    out["cases: by range vs 20d"] = sub.groupby("rngq").apply(summ)
    sub2 = sub.copy(); sub2["r5q"] = pd.qcut(sub2["r5"], 3)
    out["cases: by 5d return"] = sub2.groupby("r5q").apply(summ)
    out["cases: by year"] = sub.groupby("year").apply(summ)
    out["in profile: weekday"] = d[d.inprof].groupby("wd").apply(summ)
    out["all: weekday"] = d.groupby("wd").apply(summ)
    out["in profile: down day by loc"] = d[d.inprof & ~d.up].groupby("locq").apply(summ)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bd.append(dd.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    out["book by window"] = bd.groupby("win")["book_return"].agg(["mean", "std", "count"])
    return out
