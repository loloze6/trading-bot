def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allret = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            ph = h.shift(1).rolling(30, min_periods=30).max()
            pl = l.shift(1).rolling(30, min_periods=30).min()
            dist = c / ph - 1
            distl = c / pl - 1
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            vol_rel = vol / r1.rolling(120, min_periods=60).std()
            ret30 = c / c.shift(30) - 1
            for H in (1, 3, 5, 10):
                fwd = c.shift(-H) / c - 1
                grid = (np.arange(len(b)) % H == 0)
                df = pd.DataFrame({"coin": coin, "w": w, "H": H, "dist": dist, "distl": distl,
                                   "fwd": fwd, "grid": grid, "vol_rel": vol_rel, "ret30": ret30,
                                   "year": b["timestamp"].astype("datetime64[ns]").dt.year,
                                   "day": b["timestamp"].astype("datetime64[ns]").dt.floor("D")})
                rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["grid"] & D["fwd"].notna()]
    drift = D.groupby(["coin", "H"])["fwd"].mean().rename("drift")
    D = D.join(drift, on=["coin", "H"])
    D["ex"] = D["fwd"] - D["drift"]
    out = {}
    br = D[D["dist"] > 0].copy()
    lo = D[D["distl"] < 0].copy()
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["breakout ex by H"] = br.groupby("H")["ex"].apply(tt).unstack()
    out["monthlylow ex by H"] = lo.groupby("H")["ex"].apply(tt).unstack()
    b1 = br[br.H == 1].copy()
    b1["q"] = pd.qcut(b1["dist"], 4, labels=False)
    out["breakout H1 by dist quartile"] = b1.groupby("q")["ex"].apply(tt).unstack()
    out["breakout H1 by coin"] = b1.groupby("coin")["ex"].apply(tt).unstack()
    out["breakout H1 by year"] = b1.groupby("year")["ex"].apply(tt).unstack()
    for H in (1, 3, 5, 10):
        s = br[br.H == H].dropna(subset=["dist", "ex"])
        r = stats.linregress(s["dist"], s["ex"])
        out[f"breakout slope H{H}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
        s = lo[lo.H == H].dropna(subset=["distl", "ex"])
        r = stats.linregress(-s["distl"], s["ex"])
        out[f"low depth slope H{H}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
    l1 = lo[lo.H.isin([1, 3, 5])].copy()
    l1["volhi"] = l1["vol_rel"] > 1.2
    l1["falling"] = l1["ret30"] < 0
    out["low ex by H, volhi, falling"] = l1.groupby(["H", "volhi", "falling"])["ex"].apply(tt).unstack()
    b2 = br[br.H.isin([1, 3, 5])].copy()
    b2["volhi"] = b2["vol_rel"] > 1.2
    out["breakout ex by H, volhi"] = b2.groupby(["H", "volhi"])["ex"].apply(tt).unstack()
    return out
