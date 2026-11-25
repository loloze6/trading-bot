def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sd10 = r1.rolling(10, min_periods=8).std()
            ret3 = c / c.shift(3) - 1
            ret1 = r1
            ret7p = c / c.shift(7) - 1
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            fwd7 = c.shift(-7) / c - 1
            fwd3 = c.shift(-3) / c - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n, 7):
                if i + 7 < n:
                    allr.append(fwd7.iloc[i])
                rows.append(dict(coin=coin, win=w, i=i, s3=ret3.iloc[i] / (sd30.iloc[i] * np.sqrt(3)) if sd30.iloc[i] > 0 else np.nan,
                                 s1=ret1.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan,
                                 s7=ret7p.iloc[i] / (sd30.iloc[i] * np.sqrt(7)) if sd30.iloc[i] > 0 else np.nan,
                                 r30=ret30.iloc[i], r60=ret60.iloc[i], vr=sd10.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan,
                                 sd30=sd30.iloc[i], fwd7=fwd7.iloc[i], fwd3=fwd3.iloc[i], fc=b["forecast"].iloc[i],
                                 pos=pos.iloc[i], wd=ts.iloc[i].weekday(), day=ts.iloc[i].normalize()))
        drift[coin] = np.nanmean(allr)
    d = pd.DataFrame(rows)
    d["drift"] = d["coin"].map(drift)
    d["u7"] = d["fwd7"] - d["drift"]
    d = d.dropna(subset=["u7"])
    out = {}
    def summ(g):
        x = g["u7"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    for col, q in [("s3", 10), ("s1", 10), ("s7", 10), ("r30", 5), ("r60", 5), ("vr", 5), ("sd30", 5)]:
        dd = d.dropna(subset=[col]).copy()
        dd["b"] = pd.qcut(dd[col], q, labels=False, duplicates="drop")
        t = dd.groupby("b").apply(summ)
        t["mid"] = dd.groupby("b")[col].median()
        out["u7 by " + col] = t
    # s3 by trend
    dd = d.dropna(subset=["s3", "r60"]).copy()
    dd["tr"] = np.where(dd["r60"] > 0.1, "rising", np.where(dd["r60"] < -0.1, "falling", "choppy"))
    dd["sb"] = pd.qcut(dd["s3"], 3, labels=["low", "mid", "high"])
    out["u7 by trend x s3 tercile"] = dd.groupby(["tr", "sb"]).apply(summ)
    dd["vb"] = np.where(dd["vr"] > 1, "agit", "calm")
    out["u7 by volratio x s3 tercile"] = dd.groupby(["vb", "sb"]).apply(summ)
    # regression slopes per trend
    reg = {}
    for tr, g in dd.groupby("tr"):
        s = stats.linregress(g["s3"], g["u7"]); reg[tr] = (s.slope, s.slope / s.stderr, len(g))
    out["slope u7 on s3 by trend (slope,t,n)"] = pd.DataFrame(reg, index=["slope", "t", "n"]).T
    out["u7 by weekday"] = d.groupby("wd").apply(summ)
    out["u7 by coin"] = d.groupby("coin").apply(summ)
    # book: daily
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dl.append(x)
    D = pd.concat(dl)
    out["book vs coin by window (mean daily)"] = D.groupby("win")[["book_return", "coin_return"]].mean()
    D["cr"] = D["coin_return"]
    return out
