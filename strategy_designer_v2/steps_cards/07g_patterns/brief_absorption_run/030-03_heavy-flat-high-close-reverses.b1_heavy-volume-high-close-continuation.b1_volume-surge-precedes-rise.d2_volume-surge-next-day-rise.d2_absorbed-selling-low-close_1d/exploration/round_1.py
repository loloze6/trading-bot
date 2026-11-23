def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float); v = b["volume"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "loc": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r0": c / c.shift(1) - 1,
                "r5p": c / c.shift(5) - 1,
                "rngp": rng / c,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            for k in (1, 3, 5):
                d[f"f{k}"] = c.shift(-k) / c - 1
            d["vol20"] = d["r0"].rolling(20, min_periods=15).std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in (1, 3, 5):
        mu = D.groupby("coin")[f"f{k}"].transform(lambda s: s[D.loc[s.index, "pos"] % k == 0].mean())
        D[f"x{k}"] = D[f"f{k}"] - mu
    out = {}
    def tstat(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # forecast quintiles, horizons 1,3,5 on own grids
    res = {}
    for k in (1, 3, 5):
        G = D[(D.pos % k == 0)].dropna(subset=["fc", f"x{k}"])
        G = G.assign(q=pd.qcut(G.fc.rank(method="first"), 5, labels=False))
        res[f"h{k}"] = G.groupby("q")[f"x{k}"].apply(lambda s: 100*s.mean())
    out["fc quintile excess % by horizon"] = pd.DataFrame(res)
    # close location alone vs volume ratio alone, 1d
    G = D.dropna(subset=["loc", "vr", "x1"]).copy()
    G["lq"] = pd.qcut(G["loc"].rank(method="first"), 5, labels=False)
    G["vq"] = pd.qcut(G["vr"].rank(method="first"), 3, labels=["lowV", "midV", "highV"])
    out["x1 % by loc quintile (0=close at high) x vol tercile"] = G.pivot_table(index="lq", columns="vq", values="x1", aggfunc=lambda s: 100*s.mean())
    out["x3 % by loc quintile x vol tercile (3d grid)"] = G[G.pos % 3 == 0].dropna(subset=["x3"]).pivot_table(index="lq", columns="vq", values="x3", aggfunc=lambda s: 100*s.mean())
    # prior 5-day return quintiles
    G2 = D.dropna(subset=["r5p", "x1"]).copy()
    G2["pq"] = pd.qcut(G2.r5p.rank(method="first"), 5, labels=False)
    out["x1 by prior 5d return quintile"] = G2.groupby("pq")["x1"].apply(tstat).unstack()
    G3 = D[D.pos % 5 == 0].dropna(subset=["r5p", "x5"]).copy()
    G3["pq"] = pd.qcut(G3.r5p.rank(method="first"), 5, labels=False)
    out["x5 by prior 5d return quintile (5d grid)"] = G3.groupby("pq")["x5"].apply(tstat).unstack()
    # same-day return quintile -> next day
    G4 = D.dropna(subset=["r0", "x1"]).copy()
    G4["q"] = pd.qcut(G4.r0.rank(method="first"), 5, labels=False)
    out["x1 by today's return quintile"] = G4.groupby("q")["x1"].apply(tstat).unstack()
    # vol regime: loc effect within vol terciles
    G5 = D.dropna(subset=["vol20", "loc", "x1"]).copy()
    G5["volq"] = pd.qcut(G5.vol20.rank(method="first"), 3, labels=["calm", "mid", "wild"])
    G5["low_close"] = G5["loc"]
    out["slope x1 on loc by vol regime"] = G5.groupby("volq").apply(lambda g: pd.Series(dict(zip(["slope%", "t"], [100*stats.linregress(g["loc"], g.x1).slope, stats.linregress(g["loc"], g.x1).slope/stats.linregress(g["loc"], g.x1).stderr])), n=len(g)))
    out["x1 by weekday"] = D.groupby("wd")["x1"].apply(tstat).unstack()
    out["loc slope t by coin"] = G.groupby("coin").apply(lambda g: pd.Series({"slope%": 100*stats.linregress(g["loc"], g.x1).slope, "t": stats.linregress(g["loc"], g.x1).slope/stats.linregress(g["loc"], g.x1).stderr, "n": len(g)}))
    out["loc slope t by year"] = G.groupby("yr").apply(lambda g: pd.Series({"slope%": 100*stats.linregress(g["loc"], g.x1).slope, "t": stats.linregress(g["loc"], g.x1).slope/stats.linregress(g["loc"], g.x1).stderr, "n": len(g)}))
    # book: mean alloc, alloc vs fc
    out["mean alloc, share alloc>0, corr(alloc,fc)"] = pd.Series({"mean_alloc": D.alloc.mean(), "share>0.01": (D.alloc > 0.01).mean(), "corr": D[["alloc", "fc"]].corr().iloc[0, 1], "share fc>0": (D.fc > 0).mean()})
    return out
