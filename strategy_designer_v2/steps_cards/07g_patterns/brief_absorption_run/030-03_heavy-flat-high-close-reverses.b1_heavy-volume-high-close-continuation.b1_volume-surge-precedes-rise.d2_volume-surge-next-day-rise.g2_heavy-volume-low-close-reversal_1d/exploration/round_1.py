def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]; v = b["volume"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "cl": (h - c) / rng,  # 0 at high, 1 at low
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "r0": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "body": (c - o).abs() / rng,
                "rngrel": (rng / c),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "pos": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "i": np.arange(len(b)),
            })
            d["rngrel_ratio"] = d["rngrel"] / d["rngrel"].shift(1).rolling(20, min_periods=20).mean()
            d["vol20"] = d["r0"].shift(0).rolling(20, min_periods=20).std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - mu1
    D3 = D[D["i"] % 3 == 0].copy()
    mu3 = D3.groupby("coin")["f3"].transform("mean")
    D3["x3"] = D3["f3"] - mu3
    out = {}
    def tab(df, key, val):
        g = df.dropna(subset=[key, val]).groupby(key)[val]
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    D["clq"] = pd.cut(D["cl"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    D["vrq"] = pd.cut(D["vr"], [0, .7, 1, 1.5, 2.5, 100])
    g = D.dropna(subset=["clq", "vrq", "x1"]).groupby(["vrq", "clq"])["x1"]
    r = g.agg(["mean", "count", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
    out["x1 by volratio x closeloc"] = r.drop(columns="std")
    D3["clq"] = pd.cut(D3["cl"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["x3 by closeloc (3d grid)"] = tab(D3, "clq", "x3")
    D["r0q"] = pd.qcut(D["r0"], 10, labels=False, duplicates="drop")
    out["x1 by prior-day return decile"] = tab(D, "r0q", "x1")
    D["r5q"] = pd.qcut(D["r5"], 5, labels=False, duplicates="drop")
    out["x1 by 5d return quintile"] = tab(D, "r5q", "x1")
    D["volq"] = pd.qcut(D["vol20"], 5, labels=False, duplicates="drop")
    out["x1 by vol20 quintile"] = tab(D, "volq", "x1")
    D["rrq"] = pd.qcut(D["rngrel_ratio"], 5, labels=False, duplicates="drop")
    out["x1 by range-vs-20d quintile"] = tab(D, "rrq", "x1")
    out["x1 by weekday"] = tab(D, "wd", "x1")
    out["x1 by year"] = tab(D, "yr", "x1")
    out["x1 by coin x closeloc low(>.8) minus high(<.2)"] = pd.DataFrame({
        c: [D[(D.coin == c) & (D.cl > .8)]["x1"].mean() - D[(D.coin == c) & (D.cl < .2)]["x1"].mean(),
            stats.ttest_ind(D[(D.coin == c) & (D.cl > .8)]["x1"].dropna(), D[(D.coin == c) & (D.cl < .2)]["x1"].dropna(), equal_var=False).statistic]
        for c in D.coin.unique()}, index=["diff", "t"]).T
    # forecast and position
    D["fcq"] = pd.qcut(D["fc"].rank(method="first"), 5, labels=False)
    r = D.groupby("fcq").agg(fc=("fc", "mean"), pos=("pos", "mean"), x1=("x1", "mean"), n=("x1", "count"))
    out["by forecast quintile"] = r
    out["position stats"] = pd.Series({"mean pos": D["pos"].mean(), "share pos>0.01": (D["pos"] > .01).mean(),
                                       "corr pos vol20": D[["pos", "vol20"]].corr().iloc[0, 1]})
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna()
    bk["bq"] = pd.qcut(bk["b"], 10, labels=False)
    out["book decile vs coins"] = bk.groupby("bq").agg(b=("b", "mean"), c=("c", "mean"), n=("b", "count"))
    out["book beta to coins"] = pd.Series({"corr": bk[["b", "c"]].corr().iloc[0, 1],
                                           "slope": np.polyfit(bk["c"], bk["b"], 1)[0],
                                           "book mean": bk["b"].mean(), "coin mean": bk["c"].mean()})
    return out
