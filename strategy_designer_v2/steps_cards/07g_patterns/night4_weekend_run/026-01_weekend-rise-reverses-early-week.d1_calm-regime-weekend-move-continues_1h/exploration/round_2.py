def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    ev = []; d24 = []; fr = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            ct = pd.to_datetime(b["timestamp"]) + pd.Timedelta(hours=1)
            c = pd.Series(b["close"].values, index=ct)
            c = c[~c.index.duplicated()]
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=720).std()
            volr = vol / vol.expanding(min_periods=720).mean()
            # evening: close at 21:00 -> 23:00
            for T in c.index[c.index.hour == 21]:
                T2 = T + pd.Timedelta(hours=2); Tp = T - pd.Timedelta(hours=24); Tq = T - pd.Timedelta(hours=7)
                if T2 in c.index and Tp in c.index and Tq in c.index:
                    ev.append(dict(coin=coin, win=w, yr=T.year, wd=T.dayofweek,
                                   f=c[T2]/c[T]-1, p24=c[T]/c[Tp]-1, p7=c[T]/c[Tq]-1,
                                   v=vol.get(T, np.nan), vr=volr.get(T, np.nan)))
            cv = c.values; idx = np.arange(0, len(cv) - 48, 24)
            for i in idx:
                d24.append(dict(coin=coin, win=w, yr=c.index[i+24].year, p=cv[i+24]/cv[i]-1,
                                f=cv[i+48]/cv[i+24]-1, vr=volr.iloc[i+24], v=vol.iloc[i+24]))
    e = pd.DataFrame(ev)
    def tm(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out["21->23h return by coin"] = e.groupby("coin").f.apply(tm).unstack()
    out["21->23h return by year"] = e.groupby("yr").f.apply(tm).unstack()
    out["21->23h return by weekday"] = e.groupby("wd").f.apply(tm).unstack()
    e["wn"] = e.win.str[1:].astype(int)
    e["wq"] = pd.cut(e.wn, [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["21->23h by window group"] = e.groupby("wq").f.apply(tm).unstack()
    e["vq"] = e.groupby("coin").v.transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["21->23h by own vol tercile"] = e.groupby("vq").f.apply(tm).unstack()
    e["zf"] = e.f / e.v
    out["21->23h in vol units by vol tercile"] = e.groupby("vq").zf.apply(tm).unstack()
    e["pq"] = e.groupby("coin").p24.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["21->23h by prior 24h return quintile"] = e.groupby("pq").f.apply(tm).unstack()
    e["p7q"] = e.groupby("coin").p7.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["21->23h by prior 14->21h return quintile"] = e.groupby("p7q").f.apply(tm).unstack()
    d = pd.DataFrame(d24).dropna()
    d["zp"] = d.p / d.v; d["zf"] = d.f / d.v
    def slope(g):
        r = stats.linregress(g.zp, g.zf)
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    d["vq"] = d.groupby("coin").vr.transform(lambda x: pd.qcut(x, 3, labels=False))
    out["24h reversal slope by coin, high-vol tercile"] = d[d.vq == 2].groupby("coin").apply(slope)
    out["24h reversal slope by year, high-vol tercile"] = d[d.vq == 2].groupby("yr").apply(slope)
    out["24h reversal slope by volr tercile (coin-wise)"] = d.groupby("vq").apply(slope)
    d["vrq"] = pd.qcut(d.vr, 5, labels=False)
    out["24h reversal slope by volr quintile"] = d.groupby("vrq").apply(slope)
    return out
