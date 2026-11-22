def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "year": ts.dt.year,
                               "pos": np.arange(len(b)), "r1": r1,
                               "f1": c.shift(-1) / c - 1,
                               "pos_alloc": b["postRebalance_current_allocation"]})
            for L in [12, 24, 48, 72]:
                df[f"z{L}"] = (c / c.shift(L) - 1) / (sd * np.sqrt(L))
            for H in [12, 24, 48]:
                df[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    def summ(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    # graded reversal: slope of forward return on past z, non-overlapping grid of H
    res = []
    for L in [12, 24, 48, 72]:
        for H in [12, 24, 48]:
            g = d[d.pos % H == 0][[f"z{L}", f"f{H}"]].dropna()
            sl, ic, r, p, se = stats.linregress(g[f"z{L}"], g[f"f{H}"])
            res.append({"L": L, "H": H, "n": len(g), "slope_bp_per_z": sl*1e4, "t": sl/se})
    out["reversal slope grid"] = pd.DataFrame(res)
    # 24/24 by coin and year: slope and bottom-quintile unusual move
    g24 = d[d.pos % 24 == 0].dropna(subset=["z24", "f24"]).copy()
    drift = g24.groupby("coin")["f24"].mean()
    g24["u24"] = g24["f24"] - g24["coin"].map(drift)
    g24["q"] = pd.qcut(g24.z24, 10, labels=False)
    out["u24 by z24 decile"] = g24.groupby("q")["u24"].apply(summ).unstack()
    def slope(g):
        sl, ic, r, p, se = stats.linregress(g.z24, g.f24)
        return pd.Series({"n": len(g), "slope_bp": sl*1e4, "t": sl/se})
    out["24/24 slope by coin x year"] = g24.groupby(["coin", "year"]).apply(slope)
    # hour 20-21 effect by coin and year
    h = d[d.hour.isin([20, 21])]
    out["f1 hours 20-21 by coin x year"] = h.groupby(["coin", "year"])["f1"].apply(summ).unstack()
    # does the hour-20/21 effect grade with anything? by sign of prior 24h
    h2 = h.dropna(subset=["z24"]).copy()
    h2["zq"] = pd.qcut(h2.z24, 3, labels=False)
    out["f1 hours 20-21 by prior z24 tercile"] = h2.groupby("zq")["f1"].apply(summ).unstack()
    # book exposure share
    out["share of bars in position"] = float((d.pos_alloc.abs() > 1e-9).mean())
    return out
