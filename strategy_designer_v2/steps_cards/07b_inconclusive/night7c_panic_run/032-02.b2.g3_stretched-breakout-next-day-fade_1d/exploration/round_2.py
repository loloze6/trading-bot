def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            ph = h.shift(1).rolling(30, min_periods=30).max()
            pl = l.shift(1).rolling(30, min_periods=30).min()
            r1 = c.pct_change()
            vol_rel = r1.rolling(20).std() / r1.rolling(120, min_periods=60).std()
            ret30 = c / c.shift(30) - 1
            for H in (1, 3, 5, 10):
                fwd = c.shift(-H) / c - 1
                df = pd.DataFrame({"coin": coin, "w": w, "H": H, "dist": c / ph - 1, "distl": c / pl - 1,
                                   "fwd": fwd, "grid": (np.arange(len(b)) % H == 0), "vol_rel": vol_rel.values,
                                   "ret30": ret30.values, "fc": b["forecast"].astype(float).values,
                                   "regime": b["regime"].values, "year": ts.dt.year.values,
                                   "day": ts.dt.floor("D").dt.tz_localize(None).values})
                rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["grid"] & D["fwd"].notna()].copy()
    drift = D.groupby(["coin", "H"])["fwd"].mean().rename("drift")
    D = D.join(drift, on=["coin", "H"])
    D["ex"] = D["fwd"] - D["drift"]
    def tt(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    br = D[D["dist"] > 0]
    lo = D[D["distl"] < 0]
    out["breakout ex by H"] = br.groupby("H")["ex"].apply(tt).unstack()
    out["monthlylow ex by H"] = lo.groupby("H")["ex"].apply(tt).unstack()
    b1 = br[br.H == 1].copy()
    b1["q"] = pd.qcut(b1["dist"], 4, labels=False)
    out["breakout H1 by dist quartile"] = b1.groupby("q")["ex"].apply(tt).unstack()
    out["breakout H1 by coin"] = b1.groupby("coin")["ex"].apply(tt).unstack()
    out["breakout H1 by year"] = b1.groupby("year")["ex"].apply(tt).unstack()
    b1f = b1[b1["fc"] < 0].copy()
    if len(b1f) > 20:
        b1f["q"] = pd.qcut(-b1f["fc"], 3, labels=False, duplicates="drop")
        out["breakout H1 by -forecast tercile (fc<0)"] = b1f.groupby("q")["ex"].apply(tt).unstack()
    out["breakout H1 forecast==0 vs <0"] = b1.groupby(b1["fc"] < 0)["ex"].apply(tt).unstack()
    sl = {}
    for H in (1, 3, 5, 10):
        s = br[br.H == H].dropna(subset=["dist", "ex"])
        r = stats.linregress(s["dist"], s["ex"])
        q = lo[lo.H == H].dropna(subset=["distl", "ex"])
        r2 = stats.linregress(-q["distl"], q["ex"])
        sl[H] = {"brk slope": r.slope, "brk t": r.slope / r.stderr, "brk n": len(s),
                 "lowdepth slope": r2.slope, "lowdepth t": r2.slope / r2.stderr, "low n": len(q)}
    out["slopes by H"] = pd.DataFrame(sl).T
    l1 = lo[lo.H.isin([1, 3, 5])].copy()
    l1["volhi"] = l1["vol_rel"] > 1.2
    l1["falling"] = l1["ret30"] < 0
    out["low ex by H, volhi, falling"] = l1.groupby(["H", "volhi", "falling"])["ex"].apply(tt).unstack()
    b2 = br[br.H.isin([1, 3, 5])].copy()
    b2["volhi"] = b2["vol_rel"] > 1.2
    out["breakout ex by H, volhi"] = b2.groupby(["H", "volhi"])["ex"].apply(tt).unstack()
    return out
