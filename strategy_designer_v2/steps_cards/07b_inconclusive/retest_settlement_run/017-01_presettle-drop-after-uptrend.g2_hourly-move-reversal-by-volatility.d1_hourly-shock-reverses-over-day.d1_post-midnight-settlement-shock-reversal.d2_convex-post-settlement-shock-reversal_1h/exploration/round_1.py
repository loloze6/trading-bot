def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [1, 4, 8, 24]
    for coin, wins in data["bars"].items():
        # drift per horizon, non-overlapping grid pooled over windows
        drift = {}
        for h in H:
            vals = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            drift[h] = np.nanmean(np.concatenate(vals))
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = b["close"].pct_change()
            vol = r1.rolling(24).std()
            z = r1 / vol
            df = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour.values,
                               "year": ts.dt.year.values, "z": z.values,
                               "vol": vol.values})
            for h in H:
                df["r%d" % h] = (b["close"].shift(-h) / b["close"] - 1).values - drift[h]
            rows.append(df)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["z", "r24"])
    D = D[np.isfinite(D["z"])]
    D["sgn"] = -np.sign(D["z"])
    D["az"] = D["z"].abs()
    for h in H:
        D["f%d" % h] = D["sgn"] * D["r%d" % h]

    def summ(g, col="f24"):
        x = g[col].dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_pct": 100 * x.mean(), "t": t,
                          "per_unit_pct": 100 * (g["sgn"] * g[col.replace("f", "r")]).sum() / g["az"].sum()})

    h0 = D[D["hour"] == 0].copy()
    h0["q"] = pd.qcut(h0["az"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out = {}
    out["h0_by_size_quintile"] = h0.groupby("q", observed=True).apply(summ)
    out["h0_by_horizon"] = pd.DataFrame({h: summ(h0, "f%d" % h) for h in H}).T
    out["by_hour_f24"] = D.groupby("hour").apply(summ)
    out["by_hour_f4"] = D.groupby("hour").apply(lambda g: summ(g, "f4"))
    out["h0_by_coin"] = h0.groupby("coin").apply(summ)
    out["h0_by_year"] = h0.groupby("year").apply(summ)
    h0["side"] = np.where(h0["z"] > 0, "up_move", "down_move")
    out["h0_by_side"] = h0.groupby("side").apply(summ)
    # linear vs convex regression of r24 on z
    y = h0["r24"].values
    s1 = stats.linregress(h0["z"].values, y)
    s2 = stats.linregress(h0["z"].values * h0["az"].values, y)
    out["h0_linear_vs_convex"] = pd.DataFrame({"slope": [s1.slope, s2.slope], "t": [s1.slope / s1.stderr, s2.slope / s2.stderr], "r2": [s1.rvalue**2, s2.rvalue**2]}, index=["z", "z|z|"])
    # raw return (not vol scaled) sign fade, hour 0 vs others
    return out
