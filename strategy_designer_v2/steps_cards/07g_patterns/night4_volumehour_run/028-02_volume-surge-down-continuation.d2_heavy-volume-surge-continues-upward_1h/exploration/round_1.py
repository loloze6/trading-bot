def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            z = r1 / sd
            r24 = c / c.shift(24) - 1
            z24 = r24 / (sd * np.sqrt(24))
            rv24 = r1.rolling(24).std() / sd
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "z24": z24, "rv24": rv24,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "f1": c.shift(-1) / c - 1, "f6": c.shift(-6) / c - 1,
                               "f24": c.shift(-24) / c - 1, "fc": b["forecast"],
                               "pos": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    def summ(g, col):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # 6h grid
    g6 = d[d.pos % 6 == 0].copy()
    g6["zb"] = pd.cut(g6.z, [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    g6["vb"] = pd.cut(g6.vr, [0, 1, 2, 4, np.inf])
    out["f6 by z bucket"] = g6.groupby("zb", observed=True).apply(summ, "f6")
    out["f6 by z x volratio (|z|>2)"] = g6[g6.z.abs() > 2].groupby(["zb", "vb"], observed=True).apply(summ, "f6")
    out["f1 by z bucket (all bars)"] = d.assign(zb=pd.cut(d.z, [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])).groupby("zb", observed=True).apply(summ, "f1")
    # 24h grid
    g24 = d[d.pos % 24 == 0].copy()
    g24["z24b"] = pd.qcut(g24.z24, 5)
    out["f24 by 24h-return quintile"] = g24.groupby("z24b", observed=True).apply(summ, "f24")
    g24["rvb"] = pd.qcut(g24.rv24, 5)
    out["f24 by 24h vol quintile"] = g24.groupby("rvb", observed=True).apply(summ, "f24")
    out["f1 by hour"] = d.groupby("hour").apply(summ, "f1")
    out["f24 by weekday (grid)"] = g24.groupby("wd").apply(summ, "f24")
    out["f6 by coin x year"] = g6.groupby(["coin", "year"]).apply(summ, "f6")
    return out
