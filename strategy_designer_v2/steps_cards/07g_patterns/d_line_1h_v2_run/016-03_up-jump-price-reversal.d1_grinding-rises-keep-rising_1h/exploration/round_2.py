def explore(data):
    import numpy as np, pandas as pd
    out = {}
    hourly = []
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            ts = pd.to_datetime(b["timestamp"])
            # trailing 72h abs-return volatility proxy known at bar close of previous bar
            absr = pd.Series(np.abs(r)).rolling(72, min_periods=48).mean().shift(1).values
            hourly.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"hour":ts.dt.hour.values,
                                        "wd":ts.dt.weekday.values,"r":r,"vol72":absr}))
            for t in range(0, n, 72):
                if t-72 < 0 or t+72 >= n: continue
                past = c[t]/c[t-72]-1
                fwd = c[t+72]/c[t]-1
                rr = r[t-71:t+1]; rr = rr[~np.isnan(rr)]
                eff = abs(np.log(c[t]/c[t-72]))/np.abs(np.log1p(rr)).sum()
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,past=past,fwd=fwd,eff=eff))
    h = pd.concat(hourly)
    h["late"] = h.hour.isin([21,22])
    def tt(s):
        s = s.dropna(); return pd.Series({"bp":s.mean()*1e4,"t":s.mean()/s.std()*np.sqrt(len(s)),"n":len(s)})
    out["h21-22 ret by coin"] = h[h.late].groupby("coin")["r"].apply(tt).unstack()
    out["h21-22 ret by year"] = h[h.late].groupby("year")["r"].apply(tt).unstack()
    out["other hours ret by year"] = h[~h.late].groupby("year")["r"].apply(tt).unstack()
    h["vq"] = h.groupby("coin")["vol72"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["h21-22 ret by vol quintile"] = h[h.late].groupby("vq")["r"].apply(tt).unstack()
    out["h21-22 ret by weekday"] = h[h.late].groupby("wd")["r"].apply(tt).unstack()
    # efficiency: signed continuation, graded, by coin and by year
    g = pd.DataFrame(rows)
    g["ex"] = g.fwd - g.groupby("coin")["fwd"].transform("mean")
    g["sx"] = np.sign(g.past)*g.ex
    g["eq"] = g.groupby("coin")["eff"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["up moves: ex by eff quintile"] = g[g.past>0].groupby("eq")["ex"].apply(tt).unstack()
    out["down moves: ex by eff quintile"] = g[g.past<0].groupby("eq")["ex"].apply(tt).unstack()
    def ct(d, x, y):
        rho = np.corrcoef(d[x], d[y])[0,1]; k=len(d); return pd.Series({"rho":rho,"t":rho*np.sqrt((k-2)/(1-rho**2)),"n":k})
    g["effsign"] = g.eff*np.sign(g.past)
    out["corr eff*sign(past) vs ex, by coin"] = g.groupby("coin").apply(lambda d: ct(d,"effsign","ex"))
    out["corr eff*sign(past) vs ex, by year"] = g.groupby("year").apply(lambda d: ct(d,"effsign","ex"))
    out["corr eff*sign(past) vs ex, all"] = ct(g,"effsign","ex")
    out["corr past vs ex, all"] = ct(g,"past","ex")
    return out
