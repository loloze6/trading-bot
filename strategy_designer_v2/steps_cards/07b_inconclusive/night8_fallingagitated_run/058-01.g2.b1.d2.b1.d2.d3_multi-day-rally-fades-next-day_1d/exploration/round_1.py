def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        # coin mean daily return over all windows (visible)
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            r5 = pd.Series(c).pct_change(5).values
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            for i in range(n):
                if f[i] < 0:
                    d = {"coin": coin, "window": w, "year": ts[i].year, "day": ts[i].normalize(),
                         "f": -f[i], "r1": r1[i], "z5": r5[i]/sd30[i] if sd30[i] > 0 else np.nan,
                         "z1": r1[i]/sd30[i] if sd30[i] > 0 else np.nan}
                    for h in (1, 2, 3, 5, 10):
                        d["u%d" % h] = -(c[i+h]/c[i]-1 - h*mu) if i+h < n else np.nan
                    rows.append(d)
    df = pd.DataFrame(rows)
    def stat(g, col="u1"):
        s = g.dropna(subset=[col])
        dd = s.groupby("day")[col].sum()
        m = s[col].mean(); n = len(s)
        dev = (s[col]-m).groupby(s["day"]).sum()
        se = np.sqrt((dev**2).sum())/n if n > 1 else np.nan
        return pd.Series({"n": n, "days": s["day"].nunique(), "mean": m, "t": m/se if se else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: stat(df, "u%d" % h) for h in (1, 2, 3, 5, 10)}).T
    out["by_coin"] = df.groupby("coin").apply(stat)
    out["by_year"] = df.groupby("year").apply(stat)
    out["by_window"] = df.groupby("window").apply(stat)
    df["fq"] = pd.qcut(df["f"], 4, labels=False, duplicates="drop")
    out["by_f_quartile"] = df.groupby("fq").apply(stat)
    df["z5q"] = pd.qcut(df["z5"], 4, labels=False, duplicates="drop")
    out["by_z5_quartile"] = df.groupby("z5q").apply(stat)
    df["z1q"] = pd.qcut(df["z1"], 4, labels=False, duplicates="drop")
    out["by_z1_quartile"] = df.groupby("z1q").apply(stat)
    out["by_z5q_h3"] = df.groupby("z5q").apply(lambda g: stat(g, "u3"))
    out["corr_z5_u1"] = float(df[["z5", "u1"]].corr().iloc[0, 1])
    return out
