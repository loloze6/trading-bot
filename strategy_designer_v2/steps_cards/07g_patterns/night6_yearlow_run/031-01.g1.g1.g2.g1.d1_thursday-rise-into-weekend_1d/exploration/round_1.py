def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift2 = {}
    drift1 = {}
    for coin, wins in bars.items():
        g2 = []; g1 = []
        for w, df in wins.items():
            c = df["close"].values
            g2 += list(c[2::2][: len(c[0::2]) ] / c[0::2][: len(c[2::2])] - 1) if len(c) > 2 else []
            g1 += list(c[1:] / c[:-1] - 1)
        drift2[coin] = np.nanmean(g2); drift1[coin] = np.nanmean(g1)
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            if ts.isna().all():
                ts = pd.to_datetime(d["timestamp"], unit="ms", utc=True)
            d["wd"] = ts.dt.weekday.values
            c = d["close"]
            d["r1"] = c / c.shift(1) - 1
            d["r14"] = c / c.shift(14) - 1
            d["r3"] = c / c.shift(3) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            lo = d["low"].rolling(60, min_periods=60).min()
            hi = d["high"].rolling(60, min_periods=60).max()
            d["pos60"] = (c - lo) / (hi - lo)
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            d["x2"] = d["f2"] - drift2[coin]
            d["x1"] = d["f1"] - drift1[coin]
            d["bookr"] = d["postRebalance_total_value"].shift(-1) / d["postRebalance_total_value"] - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # 1: weekday of bar start x sign of r14, forward 2-day excess
    A["s14"] = np.where(A["r14"] > 0, "up", "down")
    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["fwd2 excess by weekday x r14 sign"] = A.groupby(["wd", "s14"])["x2"].apply(tstat).unstack()
    # 2: slope of x2 on standardized r14 per weekday, up only
    res = {}
    for wd, g in A[A["r14"] > 0].groupby("wd"):
        g = g.dropna(subset=["x2", "r14"])
        z = g.groupby("coin")["r14"].transform(lambda s: (s - s.mean()) / s.std())
        r = stats.linregress(z, g["x2"])
        res[wd] = {"n": len(g), "slope%": 100 * r.slope, "t": r.slope / r.stderr}
    out["slope x2 on z r14 (r14>0) by weekday"] = pd.DataFrame(res).T
    res = {}
    for wd, g in A[A["r14"] <= 0].groupby("wd"):
        g = g.dropna(subset=["x2", "r14"])
        z = g.groupby("coin")["r14"].transform(lambda s: (s - s.mean()) / s.std())
        r = stats.linregress(z, g["x2"])
        res[wd] = {"n": len(g), "slope%": 100 * r.slope, "t": r.slope / r.stderr}
    out["slope x2 on z r14 (r14<=0) by weekday"] = pd.DataFrame(res).T
    # 3: next-day excess by weekday of next bar (wd+1)
    A["nextwd"] = (A["wd"] + 1) % 7
    out["next 1d excess by weekday of that day"] = A.groupby("nextwd")["x1"].apply(tstat).unstack()
    # 4: grid-based (h=2) forward 2d by quintile of r1, r3, r14, vol, pos60
    G = A[A["pos"] % 2 == 0].copy()
    for col in ["r1", "r3", "r14", "vol20", "pos60"]:
        q = G.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"grid fwd2 excess by {col} quintile"] = G.groupby(q)["x2"].apply(tstat).unstack()
    # 5: book daily returns by weekday
    out["book bar return by weekday (bar start)"] = A.groupby("wd")["bookr"].apply(tstat).unstack()
    out["years"] = ts.dt.year.min() if False else "na"
    return out
