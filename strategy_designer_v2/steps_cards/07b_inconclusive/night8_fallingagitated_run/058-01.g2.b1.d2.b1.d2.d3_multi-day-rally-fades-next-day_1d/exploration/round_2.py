def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        allc = np.concatenate(allr)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            r5 = pd.Series(c).pct_change(5).values
            r3 = pd.Series(c).pct_change(3).values
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            for i in range(n):
                if f[i] < 0 and i+1 < n and sd30[i] > 0:
                    rows.append({"coin": coin, "window": w, "year": ts[i].year, "day": ts[i].normalize(),
                                 "z5": r5[i]/sd30[i], "z1": r1[i]/sd30[i], "z3": r3[i]/sd30[i],
                                 "z4": (c[i-1]/c[i-5]-1)/sd30[i] if i >= 5 else np.nan,
                                 "u1": -(c[i+1]/c[i]-1-mu), "s1": -(c[i+1]/c[i]-1-mu)/sd30[i]})
    df = pd.DataFrame(rows)
    def stat(g, col="u1"):
        s = g.dropna(subset=[col]); n = len(s)
        if n < 2: return pd.Series({"n": n, "days": s["day"].nunique(), "mean": s[col].mean(), "t": np.nan})
        m = s[col].mean()
        dev = (s[col]-m).groupby(s["day"]).sum()
        se = np.sqrt((dev**2).sum())/n
        return pd.Series({"n": n, "days": s["day"].nunique(), "mean": m, "t": m/se})
    out = {}
    df["z5h"] = (df["z5"] > df["z5"].median()).astype(int)
    df["z1h"] = (df["z1"] > df["z1"].median()).astype(int)
    out["z5half_x_z1half"] = df.groupby(["z5h", "z1h"]).apply(stat)
    df["z4q"] = pd.qcut(df["z4"], 4, labels=False, duplicates="drop")
    out["by_z4_quartile_prior4days"] = df.groupby("z4q").apply(stat)
    df["z3q"] = pd.qcut(df["z3"], 4, labels=False, duplicates="drop")
    out["by_z3_quartile"] = df.groupby("z3q").apply(stat)
    df["z5q"] = pd.qcut(df["z5"], 4, labels=False)
    out["z5top_by_year"] = df[df["z5q"] == 3].groupby("year").apply(stat)
    out["z5top_by_coin"] = df[df["z5q"] == 3].groupby("coin").apply(stat)
    out["strength_by_z5q"] = df.groupby("z5q").apply(lambda g: stat(g, "s1"))
    # day-pooled regression slope t of u1 on z5
    x = df["z5"] - df["z5"].mean(); y = df["u1"] - df["u1"].mean()
    b = (x*y).sum()/(x*x).sum(); e = y - b*x
    se = np.sqrt(((x*e).groupby(df["day"]).sum()**2).sum())/(x*x).sum()
    out["slope_u1_on_z5"] = pd.Series({"slope": b, "t": b/se, "n": len(df)})
    x = df["z4"] - df["z4"].mean(); m = x.notna()
    b4 = (x[m]*y[m]).sum()/(x[m]**2).sum(); e = y[m]-b4*x[m]
    se4 = np.sqrt(((x[m]*e).groupby(df["day"][m]).sum()**2).sum())/(x[m]**2).sum()
    out["slope_u1_on_z4"] = pd.Series({"slope": b4, "t": b4/se4})
    return out
