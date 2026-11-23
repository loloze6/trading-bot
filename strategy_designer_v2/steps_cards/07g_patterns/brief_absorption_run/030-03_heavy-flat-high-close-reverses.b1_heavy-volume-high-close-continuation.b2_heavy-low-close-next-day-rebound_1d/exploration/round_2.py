def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "ret0": c / c.shift(1) - 1,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "uwick": (h - np.maximum(o, c)) / rng,
                "lwick": (np.minimum(o, c) - l) / rng,
                "rngpct": rng / c,
                "idx": np.arange(len(b)),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            d["vol20"] = d["ret0"].shift(1).rolling(20, min_periods=15).std()
            d["z0"] = d["ret0"] / d["vol20"]
            d["rngz"] = d["rngpct"] / d["rngpct"].shift(1).rolling(20, min_periods=15).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["r1"]:
        D["x1"] = D["r1"] - D["coin"].map(D.groupby("coin")["r1"].mean())
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    def ols(g, xs, y="x1"):
        g = g.dropna(subset=xs+[y]); X = np.column_stack([np.ones(len(g))]+[g[x].values for x in xs]); Y = g[y].values
        b, *_ = np.linalg.lstsq(X, Y, rcond=None); e = Y - X@b; s2 = e@e/(len(Y)-X.shape[1])
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.DataFrame({"coef": b, "t": b/se}, index=["const"]+xs).assign(n=len(Y))
    H = D[D["vr"] >= 2]
    out["heavy: x1 ~ loc + z0"] = ols(H, ["loc", "z0"])
    out["all: x1 ~ loc + z0"] = ols(D, ["loc", "z0"])
    D["neg"] = np.minimum(D["z0"], 0)
    D["lvr"] = np.log(D["vr"])
    D["neg_x_lvr"] = D["neg"] * D["lvr"]
    out["all: x1 ~ neg z0 + logvr + interaction"] = ols(D, ["neg", "lvr", "neg_x_lvr"])
    # down-move z quintile on all days, by heavy or not
    D["zq"] = pd.qcut(D["z0"], 5)
    D["heavy"] = D["vr"] >= 2
    out["x1 mean% by z0 quintile x heavy"] = D.pivot_table(index="zq", columns="heavy", values="x1", aggfunc="mean", observed=True)*100
    out["t by z0 quintile (all)"] = D.groupby("zq", observed=True)["x1"].apply(tt).unstack()
    # down days only: slope on z0 by vr bin
    dn = D[D["z0"] < 0]
    dn = dn.assign(vrb=pd.cut(dn["vr"], [0, 1, 1.5, 2, 100]))
    out["down days: slope x1 on z0 by vr bin"] = dn.groupby("vrb", observed=True).apply(lambda g: (lambda r: pd.Series({"n": len(g), "slope%": 100*r.slope, "t": r.slope/r.stderr}))(stats.linregress(g.dropna(subset=["z0","x1"])["z0"], g.dropna(subset=["z0","x1"])["x1"])))
    # down days: slope by year (all vr)
    out["down days: slope x1 on z0 by year"] = dn.groupby("yr").apply(lambda g: (lambda gg: (lambda r: pd.Series({"n": len(gg), "slope%": 100*r.slope, "t": r.slope/r.stderr}))(stats.linregress(gg["z0"], gg["x1"])))(g.dropna(subset=["z0","x1"])))
    out["down days: slope x1 on z0 by coin"] = dn.groupby("coin").apply(lambda g: (lambda gg: (lambda r: pd.Series({"n": len(gg), "slope%": 100*r.slope, "t": r.slope/r.stderr}))(stats.linregress(gg["z0"], gg["x1"])))(g.dropna(subset=["z0","x1"])))
    # lower wick heavy
    out["heavy: x1 ~ lwick + uwick + z0"] = ols(H, ["lwick", "uwick", "z0"])
    out["all: x1 ~ rngz + z0"] = ols(D, ["rngz", "z0"])
    # 3-day grid on down days, non-overlapping
    D3 = D[D["idx"] % 3 == 0].copy(); D3["x3"] = D3["r3"] - D3["coin"].map(D3.groupby("coin")["r3"].mean())
    out["3d grid: x3 ~ neg z0"] = ols(D3, ["neg"], y="x3")
    D2 = D[D["idx"] % 2 == 0].copy(); D2["x2"] = D2["r2"] - D2["coin"].map(D2.groupby("coin")["r2"].mean())
    out["2d grid: x2 ~ neg z0"] = ols(D2, ["neg"], y="x2")
    out["3d grid heavy: x3 ~ loc + z0"] = ols(D3[D3["vr"] >= 2], ["loc", "z0"], y="x3")
    return out
