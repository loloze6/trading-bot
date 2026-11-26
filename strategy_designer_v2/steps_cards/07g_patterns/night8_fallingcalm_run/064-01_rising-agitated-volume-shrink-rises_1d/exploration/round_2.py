def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            vr10 = np.log(v.rolling(10).mean() / v.shift(10).rolling(20).mean())
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            vrel = r1.rolling(20).std() / r1.rolling(60).std()
            fwd5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b), 5):
                rows.append(dict(coin=coin, w=w, inprof=b["regime"].iat[i] == "unknown", vr=vr.iat[i], vr10=vr10.iat[i],
                                 ret20=ret20.iat[i], ret60=ret60.iat[i], vrel=vrel.iat[i], fwd5=fwd5.iat[i],
                                 day=ts.iat[i].normalize(), year=ts.iat[i].year))
    df = pd.DataFrame(rows).dropna(subset=["fwd5"])
    df["ex5"] = df["fwd5"] - df["coin"].map(df.groupby("coin")["fwd5"].mean())
    def reg(sub, x):
        s = sub.dropna(subset=[x, "ex5"]).copy()
        if len(s) < 30: return dict(n=len(s))
        s["z"] = (s[x] - s[x].mean()) / s[x].std()
        sl = stats.linregress(s["z"], s["ex5"])
        # day-clustered t: residual*z summed per day
        res = s["ex5"] - sl.intercept - sl.slope * s["z"]
        sc = (res * (s["z"] - s["z"].mean())).groupby(s["day"]).sum()
        se_cl = np.sqrt((sc ** 2).sum()) / ((s["z"] - s["z"].mean()) ** 2).sum()
        return dict(n=len(s), days=s["day"].nunique(), slope=sl.slope, t=sl.slope / sl.stderr, t_day=sl.slope / se_cl)
    rising = df.ret60 > 0.1; falling = df.ret60 < -0.1; choppy = df.ret60.abs() <= 0.1
    sets = {"rising_agit(inprof)": df[df.inprof], "rising_notinprof(calm)": df[rising & ~df.inprof],
            "rising60_all": df[rising], "falling60": df[falling], "choppy60": df[choppy],
            "up20_vrel_hi": df[(df.ret20 > 0.1) & (df.vrel > 1)], "up20_vrel_lo": df[(df.ret20 > 0.1) & (df.vrel <= 1)],
            "flat20_vrel_hi": df[(df.ret20.abs() <= 0.1) & (df.vrel > 1)], "flat20_vrel_lo": df[(df.ret20.abs() <= 0.1) & (df.vrel <= 1)]}
    res = []
    for x in ["vr", "vr10", "ret20", "vrel"]:
        for k, s in sets.items():
            d = reg(s, x); d.update(pred=x, set=k); res.append(d)
    out = {"regressions": pd.DataFrame(res)}
    # ret20 in choppy (flat20) by year, and quintiles
    f = df[df.ret20.abs() <= 0.1].dropna(subset=["ret20"]).copy()
    f["q"] = pd.qcut(f["ret20"], 5, labels=False)
    out["flat20 ret20 quintiles"] = f.groupby("q")["ex5"].agg(["count", "mean"])
    out["flat20 ret20 slope by year"] = pd.DataFrame([dict(year=y, **reg(g, "ret20")) for y, g in f.groupby("year")])
    u = df[df.ret20 > 0.1].dropna(subset=["vr"])
    out["up20 vr slope by year"] = pd.DataFrame([dict(year=y, **reg(g, "vr")) for y, g in u.groupby("year")])
    out["up20 vr slope by coin"] = pd.DataFrame([dict(coin=y, **reg(g, "vr")) for y, g in u.groupby("coin")])
    dn = df[df.ret20 < -0.1].dropna(subset=["vr"])
    out["down20 vr slope by year"] = pd.DataFrame([dict(year=y, **reg(g, "vr")) for y, g in dn.groupby("year")])
    return out
