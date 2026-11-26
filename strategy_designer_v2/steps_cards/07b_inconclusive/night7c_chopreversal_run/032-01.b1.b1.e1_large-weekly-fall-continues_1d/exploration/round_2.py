def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=30).std(ddof=1)
            vsr = (c / c.shift(7) - 1) / (vol * np.sqrt(7))
            er = (c / c.shift(30) - 1).abs() / r.abs().rolling(30).sum()
            n = len(c)
            for p in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, year=ts[p].year, day=ts[p].normalize(),
                                 vsr=vsr[p], er=er[p], ret=c[p + 7] / c[p] - 1))
    d = pd.DataFrame(rows)
    g = d.groupby("coin")["ret"]
    d["unus"] = d["ret"] - g.transform("mean"); d["usual"] = g.transform("std")
    d = d.dropna(subset=["vsr", "er"]).copy()
    d["y"] = d.unus / d.usual
    med = d.er.median()
    d["chop"] = np.where(d.er < med, "chop", "trend")

    def slope(sub):
        x, y = sub.vsr, sub.y
        if len(x) < 10: return pd.Series(dict(n=len(x), slope=np.nan, t=np.nan, spear=np.nan, sp_p=np.nan))
        res = stats.linregress(x, y)
        yw = y.clip(y.quantile(0.02), y.quantile(0.98))
        rw = stats.linregress(x, yw)
        sp = stats.spearmanr(x, y)
        return pd.Series(dict(n=len(x), slope=res.slope, t=res.slope / res.stderr,
                              slope_wins=rw.slope, t_wins=rw.slope / rw.stderr,
                              spear=sp.correlation, sp_p=sp.pvalue))
    out = {}
    out["slope by chop"] = d.groupby("chop").apply(slope)
    out["slope by year x chop"] = d.groupby(["year", "chop"]).apply(slope)
    out["slope by coin, chop only"] = d[d.chop == "chop"].groupby("coin").apply(slope)
    out["slope by window group, chop only"] = d[d.chop == "chop"].assign(
        wg=lambda z: z.w.str[1:].astype(int)).groupby("wg").apply(slope)
    out["slope falls only (vsr<0) by chop"] = d[d.vsr < 0].groupby("chop").apply(slope)
    out["slope rises only (vsr>0) by chop"] = d[d.vsr > 0].groupby("chop").apply(slope)

    def ct(x):
        m = x["v"].mean()
        dev = (x["v"] - m).groupby(x["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=m, t=m / se, days=G))
    f = d[d.vsr <= -1].copy(); f["v"] = -f["unus"]
    out["fall>=1 short-side unusual by chop"] = f.groupby("chop").apply(ct)
    out["fall>=1 short-side by vsr band, chop"] = f[f.chop == "chop"].groupby(
        pd.cut(f[f.chop == "chop"].vsr, [-99, -2, -1.5, -1])).apply(ct)
    return out
