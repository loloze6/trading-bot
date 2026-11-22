def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=10).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "z": (r1 / sd).values, "regime": b["regime"].values,
                               "r30": (c / c.shift(30) - 1).values,
                               "r5": (c / c.shift(5) - 1).values,
                               "sd5": (sd * np.sqrt(5)).values,
                               "wd": ts.dt.weekday.values, "year": ts.dt.year.values})
            for h in (1, 2, 5):
                df[f"f{h}"] = (c.shift(-h) / c - 1).values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 5):
        g = A[A.pos % h == 0]
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(g.groupby("coin")[f"f{h}"].mean())
    A["mr"] = A.regime == "mean_reversion"
    A["z5"] = A.r5 / A.sd5
    def st(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"mean": s.mean(), "n": n, "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    g5 = A[(A.pos % 5 == 0)].dropna(subset=["x5", "z", "r30"])
    up = g5[(~g5.mr) & (g5.r30 > 0)].copy()
    up["zb"] = pd.cut(up.z, [-np.inf, 0, 1, 2, np.inf])
    out["rising r30>0: x5 by z bucket"] = up.groupby("zb", observed=True)["x5"].apply(st).unstack().round(4)
    out["rising r30>0, z>1: x5 by year"] = up[up.z > 1].groupby("year")["x5"].apply(st).unstack().round(4)
    out["rising r30>0: corr z vs x5"] = float(up[["z", "x5"]].corr().iloc[0, 1])
    out["rising r30>0, z>1: x5 by coin share positive mean"] = float((up[up.z > 1].groupby("coin")["x5"].mean() > 0).mean())
    g5b = A[(A.pos % 5 == 0)].dropna(subset=["x5", "z5"])
    fr = g5b[g5b.mr].copy()
    fr["qb"] = pd.qcut(fr.z5, 5)
    out["falling: x5 by z5 (5-day rise in usual moves) quintile"] = fr.groupby("qb", observed=True)["x5"].apply(st).unstack().round(4)
    out["falling, top z5 quintile: x5 by year"] = fr[fr.z5 > fr.z5.quantile(0.8)].groupby("year")["x5"].apply(st).unstack().round(4)
    out["falling: corr z5 vs x5"] = float(fr[["z5", "x5"]].corr().iloc[0, 1])
    g1 = A.dropna(subset=["x1"])
    out["x1 weekday by year (mean)"] = g1.groupby(["year", "wd"])["x1"].mean().unstack().round(4)
    # falling regime one-day fade, z>1, x2 by year
    g2 = A[(A.pos % 2 == 0)].dropna(subset=["x2", "z"])
    out["falling z>1: x2 by year"] = g2[g2.mr & (g2.z > 1)].groupby("year")["x2"].apply(st).unstack().round(4)
    return out
