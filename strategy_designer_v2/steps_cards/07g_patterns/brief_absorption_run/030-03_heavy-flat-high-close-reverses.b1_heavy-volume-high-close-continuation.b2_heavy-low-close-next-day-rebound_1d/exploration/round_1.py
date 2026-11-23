def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "ret0": c / c.shift(1) - 1,
                "rngpct": rng / c,
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "ret5p": c / c.shift(5) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "idx": np.arange(len(b)),
            })
            d["vol20"] = d["ret0"].rolling(20, min_periods=15).std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu1)
    # 3-day grid
    D3 = D[D["idx"] % 3 == 0].copy()
    mu3 = D3.groupby("coin")["r3"].mean()
    D3["x3"] = D3["r3"] - D3["coin"].map(mu3)
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    D["vrbin"] = pd.cut(D["vr"], [0, 0.7, 1.0, 1.5, 2.0, 3.0, 100])
    D["locq"] = pd.cut(D["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["x1 mean% by vr bin x loc bin"] = D.pivot_table(index="vrbin", columns="locq", values="x1", aggfunc="mean", observed=True)*100
    out["counts vr x loc"] = D.pivot_table(index="vrbin", columns="locq", values="x1", aggfunc="count", observed=True)
    # slope of x1 on loc by vr bin
    sl = {}
    for k, g in D.dropna(subset=["x1", "loc", "vr"]).groupby("vrbin", observed=True):
        r = stats.linregress(g["loc"], g["x1"]); sl[str(k)] = {"n": len(g), "slope%": 100*r.slope, "t": r.slope/r.stderr}
    out["slope x1 on loc by vr"] = pd.DataFrame(sl).T
    H = D[D["vr"] >= 2].dropna(subset=["x1", "loc"])
    H["r0bin"] = pd.qcut(H["ret0"], 4)
    out["heavy: x1 by day-return quartile x loc"] = H.pivot_table(index="r0bin", columns="locq", values="x1", aggfunc="mean", observed=True)*100
    out["heavy: x1 by day return quartile"] = H.groupby("r0bin", observed=True)["x1"].apply(tt).unstack()
    out["all days: x1 by ret0 quintile"] = D.groupby(pd.qcut(D["ret0"], 5), observed=True)["x1"].apply(tt).unstack()
    H["volq"] = H.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["heavy: slope by vol tercile"] = H.groupby("volq").apply(lambda g: pd.Series({"n": len(g), "slope%": 100*stats.linregress(g["loc"], g["x1"]).slope, "t": stats.linregress(g["loc"], g["x1"]).slope/stats.linregress(g["loc"], g["x1"]).stderr}))
    out["heavy: slope by coin"] = H.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "slope%": 100*stats.linregress(g["loc"], g["x1"]).slope, "t": stats.linregress(g["loc"], g["x1"]).slope/stats.linregress(g["loc"], g["x1"]).stderr}))
    out["heavy: slope by year"] = H.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "slope%": 100*stats.linregress(g["loc"], g["x1"]).slope, "t": stats.linregress(g["loc"], g["x1"]).slope/stats.linregress(g["loc"], g["x1"]).stderr}))
    out["heavy: x1 by weekday"] = H.groupby("wd")["x1"].apply(tt).unstack()
    out["all: x1 by weekday"] = D.groupby("wd")["x1"].apply(tt).unstack()
    H3 = D3[(D3["vr"] >= 2)].dropna(subset=["x3", "loc"])
    r = stats.linregress(H3["loc"], H3["x3"]); out["heavy 3d slope on loc"] = pd.Series({"n": len(H3), "slope%": 100*r.slope, "t": r.slope/r.stderr})
    A3 = D3.dropna(subset=["x3", "loc"])
    r = stats.linregress(A3["loc"], A3["x3"]); out["all 3d slope on loc"] = pd.Series({"n": len(A3), "slope%": 100*r.slope, "t": r.slope/r.stderr})
    out["all: x1 by range% quintile"] = D.groupby(pd.qcut(D["rngpct"], 5), observed=True)["x1"].apply(tt).unstack()
    out["all: x1 by 5d past return quintile"] = D.groupby(pd.qcut(D["ret5p"], 5), observed=True)["x1"].apply(tt).unstack()
    # book: largest loss/gain days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    br = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: quantiles%"] = br.quantile([0.01, 0.05, 0.5, 0.95, 0.99])*100
    out["book: share of total from top/bottom 5% days"] = pd.Series({"sum_all%": br.sum()*100, "sum_top5%": br[br >= br.quantile(0.95)].sum()*100, "sum_bot5%": br[br <= br.quantile(0.05)].sum()*100})
    return out
