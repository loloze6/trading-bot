def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    hrows = []; HRl = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float)
            n = len(s)
            ts = pd.to_datetime(b["timestamp"])
            r1 = s / s.shift(24) - 1
            r30 = s / s.shift(720) - 1
            lr = np.log(s).diff()
            vol7 = lr.rolling(168, min_periods=100).std()
            f1 = s.shift(-24) / s - 1
            z1 = r1 / (vol7 * np.sqrt(24))
            idx = np.arange(0, n, 24)
            for i in idx:
                hrows.append(dict(coin=c, w=w, yr=ts.iat[i].year, r1=r1[i], r30=r30[i], z1=z1[i],
                                  vol=vol7[i], f1=f1[i]))
            r = s.pct_change()
            pos = b["postRebalance_current_allocation"].shift(1)
            HRl.append(pd.DataFrame({"coin": c, "w": w, "yr": ts.dt.year, "h": ts.dt.hour, "r": r, "g": pos * r}))
    h = pd.DataFrame(hrows)
    h["ex"] = h["f1"] - h.groupby("coin")["f1"].transform("mean")
    h = h.dropna(subset=["ex", "r1"])
    def sl(d, col="r1"):
        d = d.dropna(subset=[col, "ex"])
        if len(d) < 30: return pd.Series(dict(slope=np.nan, t=np.nan, n=len(d)))
        r = stats.linregress(d[col], d["ex"]); return pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(d)))
    out["1d rev by coin"] = h.groupby("coin").apply(sl).round(4)
    out["1d rev by year"] = h.groupby("yr").apply(sl).round(4)
    h["volq"] = h.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["1d rev by vol tercile"] = h.groupby("volq").apply(sl).round(4)
    out["1d rev on z1 by vol tercile"] = h.groupby("volq").apply(lambda d: sl(d, "z1")).round(4)
    h["zq"] = pd.qcut(h["z1"].rank(method="first"), 5, labels=False)
    t = h.dropna(subset=["z1"]).groupby("zq")["ex"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); out["1d fwd by z1 quint"] = t.round(4)
    HR = pd.concat(HRl).dropna(subset=["r"])
    HR["late"] = HR["h"].isin([21, 22])
    def tt(x):
        return pd.Series(dict(mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))), n=len(x)))
    out["h21-22 ret by coin"] = HR[HR.late].groupby("coin")["r"].apply(tt).unstack().round(6)
    out["h21-22 ret by year"] = HR[HR.late].groupby("yr")["r"].apply(tt).unstack().round(6)
    out["h21-22 minus other, Welch"] = pd.Series(dict(t=stats.ttest_ind(HR[HR.late]["r"], HR[~HR.late]["r"], equal_var=False).statistic))
    out["book hourly gain by hour 21-22 vs other"] = HR.dropna(subset=["g"]).groupby("late")["g"].apply(tt).unstack()
    dd = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; dd.append(d)
    D = pd.concat(dd)
    dt = pd.to_datetime(D["day"]); D["wd"] = dt.dt.weekday; D["yr"] = dt.dt.year
    sat = D[D.wd == 5]
    out["sat coin ret by coin"] = sat.groupby("coin")["coin_return"].apply(lambda x: tt(x.dropna())).unstack().round(5)
    out["sat coin ret by year"] = sat.groupby("yr")["coin_return"].apply(lambda x: tt(x.dropna())).unstack().round(5)
    out["book ret by weekday"] = D.groupby("wd")["book_return"].apply(lambda x: tt(x.dropna())).unstack().round(5)
    return out
