def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]; v = b["volume"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r0": r,
                "loc": (h - c) / (h - l).replace(0, np.nan),
                "vol20": r.rolling(20, min_periods=10).std(),
                "vrel": v / v.rolling(20, min_periods=10).mean(),
                "rng": (h - l) / c,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "body": (c - o).abs() / (h - l).replace(0, np.nan),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - mu1
    D["z1"] = D["x1"] / D.groupby("coin")["f1"].transform("std")
    D["volrank"] = D.groupby("coin")["vol20"].rank(pct=True)
    D["vrelrank"] = D.groupby("coin")["vrel"].rank(pct=True)
    D["r0z"] = D["r0"] / D["vol20"]
    D["wd"] = D["ts"].dt.dayofweek
    D["yr"] = D["ts"].dt.year
    def tab(g):
        x = D.groupby(g, observed=True)["x1"]
        t = x.agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["mean"] *= 100
        return t[["mean", "count", "t"]].round(3)
    out = {}
    D["locq"] = pd.cut(D["loc"], [-.01, .2, .4, .6, .8, 1.01])
    out["x1 % by close loc (1=low)"] = tab("locq")
    D["volq"] = pd.qcut(D["volrank"], 4, labels=["v1", "v2", "v3", "v4"])
    D["vrq"] = pd.qcut(D["vrelrank"], 4, labels=["q1", "q2", "q3", "q4"])
    out["x1 by vol quartile"] = tab("volq")
    out["x1 by relvol quartile"] = tab("vrq")
    D["r0zq"] = pd.qcut(D["r0z"], 5, labels=["d1", "d2", "d3", "d4", "d5"])
    out["x1 by today's return/vol quintile"] = tab("r0zq")
    D["r5q"] = pd.qcut(D.groupby("coin")["r5"].rank(pct=True), 5, labels=["a1","a2","a3","a4","a5"])
    out["x1 by 5d return quintile"] = tab("r5q")
    D["r20q"] = pd.qcut(D.groupby("coin")["r20"].rank(pct=True), 5, labels=["b1","b2","b3","b4","b5"])
    out["x1 by 20d return quintile"] = tab("r20q")
    out["x1 by weekday"] = tab("wd")
    out["x1 by year"] = tab("yr")
    # interaction loc x vol
    D["lowc"] = D["loc"] > 0.5
    out["x1 low-close x volq"] = D.groupby(["lowc", "volq"], observed=True)["x1"].agg(lambda s: f"{100*s.mean():.3f}% n={len(s)} t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}").unstack()
    out["x1 todayret x volq"] = D.groupby(["r0zq", "volq"], observed=True)["x1"].agg(lambda s: f"{100*s.mean():.3f} t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}").unstack()
    out["x1 loc x relvol"] = D.groupby(["lowc", "vrq"], observed=True)["x1"].agg(lambda s: f"{100*s.mean():.3f} t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}").unstack()
    # regressions pooled: x1 on loc, loc*vol, r0, r0z
    from numpy.linalg import lstsq
    E = D.dropna(subset=["x1", "loc", "vol20", "r0", "vrel"]).copy()
    def ols(cols):
        X = np.column_stack([np.ones(len(E))] + [E[c].values for c in cols])
        y = E["x1"].values
        bta, *_ = lstsq(X, y, rcond=None)
        res = y - X @ bta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.Series(bta / se, index=["c"] + cols)
    E["locvol"] = E["loc"] * E["vol20"]
    E["r0vol"] = E["r0"]  # raw return
    E["absr0"] = E["r0"].abs()
    out["t: x1 ~ locvol + r0 + vol20"] = ols(["locvol", "r0", "vol20"]).round(2)
    out["t: x1 ~ loc + vol20 + locvol"] = ols(["loc", "vol20", "locvol"]).round(2)
    out["t: x1 ~ absr0 + r0 + rng"] = ols(["absr0", "r0", "rng"]).round(2)
    # by coin
    out["x1 low-close minus high-close by coin, high vol"] = D[D.volq.isin(["v3","v4"])].groupby("coin").apply(lambda g: pd.Series({"diff%": 100*(g.loc[g.lowc,"x1"].mean()-g.loc[~g.lowc,"x1"].mean()), "t": stats.ttest_ind(g.loc[g.lowc,"x1"].dropna(), g.loc[~g.lowc,"x1"].dropna(), equal_var=False)[0]})).round(3)
    return out
