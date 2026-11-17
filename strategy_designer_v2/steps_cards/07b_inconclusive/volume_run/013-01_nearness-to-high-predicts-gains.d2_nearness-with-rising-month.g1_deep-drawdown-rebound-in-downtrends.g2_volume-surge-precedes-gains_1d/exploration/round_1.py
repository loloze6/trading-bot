def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            f = df["forecast"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            vr = pd.Series(v) / pd.Series(v).rolling(20, min_periods=20).mean()
            r1 = pd.Series(c).pct_change().values
            r20 = pd.Series(c).pct_change(20).values
            for h in (1, 3, 7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, year=yr[i], h=h, f=f[i], vr=vr.iloc[i],
                                     r1=r1[i], r20=r20[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def slope_t(x, y):
        m = x.notna() & y.notna()
        x, y = x[m], y[m]
        if len(x) < 10 or x.std() == 0:
            return np.nan, np.nan, len(x)
        r = stats.linregress(x, y)
        return r.slope, r.slope / r.stderr, len(x)

    out = {}
    hz = []
    for h, g in d.groupby("h"):
        s, t, n = slope_t(g["f"], g["ex"])
        hz.append(dict(h=h, slope=s, t=t, n=n))
    out["by_horizon"] = pd.DataFrame(hz)
    d7 = d[d.h == 7].copy()
    pc = []
    for k, g in d7.groupby("coin"):
        s, t, n = slope_t(g["f"], g["ex"]); pc.append(dict(coin=k, slope=s, t=t, n=n))
    out["per_coin_7"] = pd.DataFrame(pc)
    py = []
    for k, g in d7.groupby("year"):
        s, t, n = slope_t(g["f"], g["ex"]); py.append(dict(year=k, slope=s, t=t, n=n))
    out["per_year_7"] = pd.DataFrame(py)
    d7["fq"] = pd.qcut(d7["f"].rank(method="first"), 5, labels=False)
    out["quintile_7"] = d7.groupby("fq").agg(fmean=("f", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                             sd=("ex", "std"))
    # side of the volume day: up vs down day
    sd = []
    for lab, g in [("up_day", d7[d7.r1 > 0]), ("down_day", d7[d7.r1 <= 0])]:
        s, t, n = slope_t(g["f"], g["ex"]); sd.append(dict(side=lab, slope=s, t=t, n=n))
    for lab, g in [("r20_up", d7[d7.r20 > 0]), ("r20_down", d7[d7.r20 <= 0])]:
        s, t, n = slope_t(g["f"], g["ex"]); sd.append(dict(side=lab, slope=s, t=t, n=n))
    out["by_side_7"] = pd.DataFrame(sd)
    # signed: forecast x sign of day return
    d7["fs"] = d7["f"] * np.sign(d7["r1"])
    s, t, n = slope_t(d7["fs"], d7["ex"])
    out["signed_f_by_dayret_7"] = pd.DataFrame([dict(slope=s, t=t, n=n)])
    # signed at other horizons
    sh = []
    for h, g in d.groupby("h"):
        s, t, n = slope_t(g["f"] * np.sign(g["r1"]), g["ex"]); sh.append(dict(h=h, slope=s, t=t, n=n))
    out["signed_by_horizon"] = pd.DataFrame(sh)
    return out
