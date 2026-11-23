def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 3, 3):
                g3.append(c[i + 3] / c[i] - 1)
        g3 = np.array(g3); drift3, sd3 = g3.mean(), g3.std(ddof=1)
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["wd"] = ts.dt.weekday.values
            d["wk"] = (ts.dt.floor("D") - pd.to_timedelta(ts.dt.weekday, unit="D")).astype("int64") // 10**9
            d["year"] = ts.dt.year.values
            c = d["close"]
            d["r1"] = c.pct_change(); d["r20"] = c / c.shift(20) - 1
            d["f3"] = c.shift(-3) / c - 1
            d["ex3"] = d["f3"] - drift3
            d["str3"] = d["ex3"] / sd3
            d["vol20"] = np.log(c).diff().rolling(20).std()
            d["r1z"] = d["r1"] / d["vol20"].shift(1)
            d["coin"] = coin
            rows.append(d[["coin","wd","wk","year","r1","r20","f3","ex3","str3","vol20","r1z"]])
    A = pd.concat(rows, ignore_index=True)
    A["vr"] = A.groupby("coin")["vol20"].rank(pct=True)
    A = A.dropna(subset=["ex3", "r1z", "vr"])
    A["qv"] = pd.qcut(A["vr"], 3, labels=False)
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    sun = A[A.wd == 6].copy()
    # demean each week's cross-section: coin-specific part
    sun["ex3_dm"] = sun["ex3"] - sun.groupby("wk")["ex3"].transform("mean")
    sun["str3_dm"] = sun["str3"] - sun.groupby("wk")["str3"].transform("mean")
    sun["r1z_dm"] = sun["r1z"] - sun.groupby("wk")["r1z"].transform("mean")
    ff = sun[(sun.r1 < 0) & (sun.r20 < 0)]
    out["sun fall&fall week-demeaned ex3 by vol tercile"] = ff.groupby("qv")["ex3_dm"].apply(summ).unstack()
    out["sun fall&fall week-clustered ex3 by vol tercile"] = ff.groupby("qv").apply(lambda g: summ(g.groupby("wk")["ex3"].mean())).reset_index().set_index("qv")
    out["sun rise week-demeaned ex3"] = summ(sun[sun.r1 > 0]["ex3_dm"]).to_frame().T
    r = stats.linregress(sun.r1z_dm.values, sun.str3_dm.values)
    out["sun slope str3_dm on r1z_dm"] = pd.DataFrame({"slope": [r.slope], "t": [r.slope / r.stderr], "n": [len(sun)]})
    # slope by vol tercile, week-demeaned, all Sundays
    sl = {}
    for q, g in sun.groupby("qv"):
        rr = stats.linregress(g.r1z_dm.values, g.str3_dm.values)
        sl[q] = {"slope": rr.slope, "t": rr.slope / rr.stderr, "n": len(g)}
    out["sun week-demeaned slope by vol tercile"] = pd.DataFrame(sl).T
    # same on other weekdays (week-demeaned per weekday-week)
    oth = A[A.wd != 6].copy()
    oth["key"] = oth["wk"].astype(str) + "_" + oth["wd"].astype(str)
    oth["str3_dm"] = oth["str3"] - oth.groupby("key")["str3"].transform("mean")
    oth["r1z_dm"] = oth["r1z"] - oth.groupby("key")["r1z"].transform("mean")
    sl = {}
    for q, g in oth.groupby("qv"):
        rr = stats.linregress(g.r1z_dm.values, g.str3_dm.values)
        sl[q] = {"slope": rr.slope, "t": rr.slope / rr.stderr, "n": len(g)}
    out["other days week-demeaned slope by vol tercile"] = pd.DataFrame(sl).T
    # high-vol fall&fall Sunday by year (week-demeaned)
    out["sun high-vol fall&fall demeaned ex3 by year"] = ff[ff.qv == 2].groupby("year")["ex3_dm"].apply(summ).unstack()
    return out
