def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            n = len(b)
            fwd = c.shift(-5) / c - 1
            for i in range(0, n, 5):
                sd = sd30[i]
                rows.append(dict(coin=coin, z=r1[i] / sd if sd > 0 else np.nan,
                                 zp5=(c[i] / c[i-5] - 1) / (sd * np.sqrt(5)) if i >= 5 and sd > 0 else np.nan,
                                 tr=c[i] / c[i-60] - 1 if i >= 60 else np.nan,
                                 fwd=fwd[i], calm=b["regime"].iloc[i] != "chop",
                                 day=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["fwd", "zp5"])
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["tb"] = pd.cut(d["tr"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    def dayt(g, col):
        s = g.groupby("day")[col].sum()
        m = g[col].mean()
        se = np.sqrt((s - s.mean() * 0).pow(2).sum()) / len(g) if len(g) > 1 else np.nan
        # clustered se of mean: sqrt(sum_day (sum dev)^2)/n
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=m, t=m / se))
    out = {}
    g = d[d.calm & (d.tb == "fall")].copy()
    g["pb"] = pd.cut(g["zp5"], [-99, -1.5, -0.5, 0, 0.5, 99])
    out["calm_fall_by_zp5_ex"] = g.groupby("pb").apply(lambda x: dayt(x, "ex"))
    out["calm_fall_by_zp5_raw"] = g.groupby("pb").apply(lambda x: dayt(x, "fwd"))
    g2 = d[d.calm & (d.tb == "fall") & (d.zp5 < -0.5)]
    out["calm_fall_neg_by_year"] = g2.groupby("year").apply(lambda x: dayt(x, "ex"))
    out["calm_fall_neg_by_coin"] = g2.groupby("coin").apply(lambda x: dayt(x, "ex"))
    a = d[~d.calm & (d.tb == "fall")].copy()
    a["pb"] = pd.cut(a["zp5"], [-99, -1.5, -0.5, 0, 0.5, 99])
    out["agit_fall_by_zp5_ex"] = a.groupby("pb").apply(lambda x: dayt(x, "ex"))
    # weekday by profile on daily coin returns
    rr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.shift(-1) / c - 1
            tr = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            rr.append(pd.DataFrame(dict(r=r, tr=tr, calm=b["regime"] != "chop", wd=(ts + pd.Timedelta(days=1)).dt.weekday, day=ts.dt.normalize())))
    rr = pd.concat(rr).dropna()
    rr["drift"] = rr["r"].mean()
    rr["tb"] = pd.cut(rr["tr"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    rr["late"] = rr["wd"].isin([4, 5])
    out["late_week_by_profile"] = rr.groupby(["tb", "calm", "late"]).apply(lambda x: dayt(x, "r")).unstack("late")
    return out
