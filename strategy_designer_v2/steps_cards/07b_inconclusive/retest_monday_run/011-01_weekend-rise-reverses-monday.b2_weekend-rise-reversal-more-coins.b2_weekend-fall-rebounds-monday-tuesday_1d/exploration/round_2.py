def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in (1, 2, 3, 4, 5):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(60, min_periods=20).std()
            mu = r1.rolling(60, min_periods=20).mean()
            z = (r1 - mu) / sd
            vol = df["volume"]
            vrel = vol / vol.rolling(60, min_periods=20).median()
            n = len(df)
            for t in range(n):
                if np.isnan(z.iloc[t]):
                    continue
                rec = {"coin": coin, "win": w, "year": ts.iloc[t].year, "dow": ts.iloc[t].dayofweek,
                       "key": ts.iloc[t].normalize().value, "z": z.iloc[t], "vrel": vrel.iloc[t],
                       "fc": df["forecast"].iloc[t]}
                for h in (1, 2, 3, 4, 5):
                    rec[f"x{h}"] = (c.iloc[t + h] / c.iloc[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                rec["d3"] = (c.iloc[t + 3] / c.iloc[t + 2] - 1 - drift[(coin, 1)]) if t + 3 < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def clus(g, col):
        g = g.dropna(subset=[col])
        m = g.groupby("key")[col].mean()
        return pd.Series({"cases": len(g), "dates": len(m), "pooled%": 100 * g[col].mean(),
                          "date_mean%": 100 * m.mean(), "t_dates": m.mean() / (m.std() / np.sqrt(len(m)))})
    out = {}
    fall = d[d.z < 0]
    sun = fall[fall.dow == 6]
    out["sun_fall_clustered"] = pd.DataFrame({h: clus(sun, h) for h in ["x1", "x2", "x3", "d3", "x4", "x5"]}).T
    for k in range(7):
        pass
    out["fall_x3_clustered_by_dow"] = pd.DataFrame({k: clus(fall[fall.dow == k], "x3") for k in range(7)}).T
    out["fall_x2_clustered_by_dow"] = pd.DataFrame({k: clus(fall[fall.dow == k], "x2") for k in range(7)}).T
    rise = d[(d.z > 0) & (d.dow == 6)]
    out["sun_rise_clustered"] = pd.DataFrame({h: clus(rise, h) for h in ["x1", "x2", "x3"]}).T
    out["sun_fall_x3_by_year"] = sun.groupby("year").apply(lambda g: clus(g, "x3"))
    out["sun_fall_x2_by_year"] = sun.groupby("year").apply(lambda g: clus(g, "x2"))
    s = sun.copy()
    s["fq"] = pd.qcut(-s.z, 5, labels=False)
    out["sun_fall_x3_by_quint"] = s.groupby("fq").apply(lambda g: clus(g, "x3"))
    s["vq"] = pd.qcut(s.vrel, 3, labels=False)
    out["sun_fall_x3_by_volterc"] = s.groupby("vq").apply(lambda g: clus(g, "x3"))
    # forecast-weighted per-Sunday check on the recorded forecast
    sf = sun[sun.fc > 0].dropna(subset=["x2"])
    out["recorded_fc_cases"] = float(len(sf))
    out["recorded_fc_wmean_x2%"] = float(100 * (sf.x2 * sf.fc).sum() / sf.fc.sum())
    return out
