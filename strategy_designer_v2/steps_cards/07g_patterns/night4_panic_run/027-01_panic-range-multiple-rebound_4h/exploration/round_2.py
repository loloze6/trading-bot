def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d": 6, "3d": 18, "14d": 84}
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            hi6 = b["high"].rolling(6).max(); lo6 = b["low"].rolling(6).min()
            rng = (hi6 - lo6) / c
            rngm = rng / rng.rolling(180, min_periods=60).mean()
            r24 = c / c.shift(6) - 1
            vol = r1.rolling(180, min_periods=60).std()
            r7d = c / c.shift(42) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "ts": ts,
                               "year": ts.dt.year, "r24": r24, "rngm": rngm, "vol": vol,
                               "z24": r24 / (vol * np.sqrt(6)), "z7d": r7d / (vol * np.sqrt(42)),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1n": r1.shift(-1)})
            for k, h in H.items():
                df["f" + k] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def prep(hk, feat):
        h = H[hk]; g = A[A["pos"] % h == 0].dropna(subset=[feat, "f" + hk]).copy()
        g["ex"] = (g["f" + hk] - g.groupby("coin")["f" + hk].transform("mean")) / g.groupby("coin")["f" + hk].transform("std")
        g["bk"] = g.groupby("coin")[feat].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        return g
    def tt(s):
        return s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan
    def robust(g, top, name):
        sel = g[g["bk"] == top]
        r = {}
        r["by coin"] = sel.groupby("coin")["ex"].agg(["mean", "count", tt])
        r["by year"] = sel.groupby("year")["ex"].agg(["mean", "count", tt])
        ts_mean = sel.groupby("ts")["ex"].mean()
        r["clustered by time"] = pd.Series({"mean": ts_mean.mean(), "n_times": len(ts_mean), "t": tt(ts_mean)})
        for k, v in r.items():
            out[f"{name} | {k}"] = v
    g1 = prep("1d", "z24"); robust(g1, 0, "z24 bottom -> 1d")
    g3 = prep("3d", "rngm"); robust(g3, 4, "rngm top -> 3d")
    # range top split by direction of the 24h move
    t3 = g3[g3["bk"] == 4].copy(); t3["dir"] = np.where(t3["r24"] < 0, "fall", "rise")
    out["rngm top -> 3d by 24h direction"] = t3.groupby("dir")["ex"].agg(["mean", "count", tt])
    # graded within falls: depth of fall x range, 3d
    g3f = g3[g3["r24"] < 0].copy()
    g3f["sev"] = -g3f["z24"] * g3f["rngm"]
    g3f["sb"] = g3f.groupby("coin")["sev"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["fall severity quintiles -> 3d"] = g3f.groupby("sb")["ex"].agg(["mean", "count", tt])
    g1f = prep("1d", "z24"); g1f = g1f[g1f["r24"] < 0].copy(); g1f["sev"] = -g1f["z24"] * g1f["rngm"]
    g1f["sb"] = g1f.groupby("coin")["sev"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["fall severity quintiles -> 1d"] = g1f.groupby("sb")["ex"].agg(["mean", "count", tt])
    g14 = prep("14d", "z7d"); robust(g14, 4, "z7d top -> 14d")
    # hour 16 and friday, clustered by time and by year
    A["r1z"] = A["r1n"] / A["vol"]
    for nm, cond in [("hour16", A["hour"] == 16), ("friday", A["wd"] == 4)]:
        s = A[cond].dropna(subset=["r1z"])
        tm = s.groupby("ts")["r1z"].mean()
        out[f"{nm} clustered"] = pd.Series({"mean": tm.mean(), "n_times": len(tm), "t": tt(tm)})
        out[f"{nm} by year"] = s.groupby("year")["r1z"].agg(["mean", "count", tt])
    # forecast / position
    out["forecast share positive, alloc stats"] = pd.Series({
        "share fc>0": (A["fc"] > 0).mean(), "share fc>=2": (A["fc"] >= 2).mean(),
        "mean alloc": A["alloc"].mean(), "median alloc": A["alloc"].median(),
        "corr fc alloc": A[["fc", "alloc"]].corr().iloc[0, 1]})
    return out
