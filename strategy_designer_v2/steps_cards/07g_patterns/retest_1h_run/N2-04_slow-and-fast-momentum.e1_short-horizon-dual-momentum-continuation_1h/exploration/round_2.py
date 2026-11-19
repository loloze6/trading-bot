def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def tstat(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return np.nan
        return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    rows = []; hourly = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values)
            ts = pd.to_datetime(b["timestamp"])
            r1 = cl.pct_change()
            r24p = cl/cl.shift(24)-1
            vol = r1.rolling(720).std()*np.sqrt(24)
            n = len(b)
            for i in range(0, n-24, 24):
                rows.append(dict(coin=c, w=w, fwd24=cl.iloc[i+24]/cl.iloc[i]-1,
                                 fwd72=(cl.iloc[i+72]/cl.iloc[i]-1) if i+72 < n else np.nan,
                                 r24=r24p.iloc[i], z=r24p.iloc[i]/vol.iloc[i] if vol.iloc[i]>0 else np.nan,
                                 vol=vol.iloc[i], fc=b["forecast"].iloc[i], yr=ts.iloc[i].year, hr=ts.iloc[i].hour))
            hourly.append(pd.DataFrame(dict(coin=c, hr=ts.dt.hour, yr=ts.dt.year, r=r1.shift(-1).values,
                                            prev=r1.values)))
    g = pd.DataFrame(rows)
    g["ex24"] = g["fwd24"] - g.groupby("coin")["fwd24"].transform("mean")
    g["ex72"] = g["fwd72"] - g.groupby("coin")["fwd72"].transform("mean")
    d = g.dropna(subset=["r24"]).copy()
    d["dec"] = d.groupby("coin")["r24"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out["24h excess by 24h ret decile"] = d.groupby("dec").agg(r24=("r24","mean"), ex=("ex24","mean"), t=("ex24",tstat), n=("ex24","count"))
    out["slope ex24 on r24 by coin"] = d.groupby("coin").apply(lambda x: pd.Series({"beta": np.polyfit(x["r24"], x["ex24"],1)[0], "corr": x["r24"].corr(x["ex24"]), "n": len(x)}))
    out["slope ex24 on r24 by year"] = d.groupby("yr").apply(lambda x: pd.Series({"corr": x["r24"].corr(x["ex24"]), "n": len(x)}))
    dz = d.dropna(subset=["z"]).copy()
    dz["zq"] = dz.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["24h excess by vol-scaled 24h ret quintile"] = dz.groupby("zq").agg(ex=("ex24","mean"), t=("ex24",tstat), n=("ex24","count"))
    dz["vq"] = dz.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["corr r24 vs ex24 by vol tercile"] = dz.groupby("vq").apply(lambda x: pd.Series({"corr": x["r24"].corr(x["ex24"]), "n": len(x)}))
    out["corr r24 vs ex24 trending vs not"] = d.groupby(d["fc"]>0).apply(lambda x: pd.Series({"corr": x["r24"].corr(x["ex24"]), "n": len(x)}))
    # 72h horizon after 24h return, non-overlapping 72 grid subset
    d72 = d[d.index % 3 == 0].dropna(subset=["ex72"]) if False else d.dropna(subset=["ex72"])
    d72 = d72.groupby(["coin","w"], group_keys=False).apply(lambda x: x.iloc[::3])
    d72["q"] = d72.groupby("coin")["r24"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["72h excess by 24h ret quintile (72h grid)"] = d72.groupby("q").agg(ex=("ex72","mean"), t=("ex72",tstat), n=("ex72","count"))
    H = pd.concat(hourly).dropna()
    H["ex"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    H["ev"] = H["hr"].isin([20,21])
    out["hours 20-21 excess bp by coin"] = H[H.ev].groupby("coin")["ex"].agg(bp=lambda s: s.mean()*1e4, t=tstat, n="count")
    out["hours 20-21 excess bp by year"] = H[H.ev].groupby("yr")["ex"].agg(bp=lambda s: s.mean()*1e4, t=tstat, n="count")
    out["hour 13 excess bp by year"] = H[H.hr==13].groupby("yr")["ex"].agg(bp=lambda s: s.mean()*1e4, t=tstat, n="count")
    # hourly reversal: next hour vs this hour
    H["pq"] = H.groupby("coin")["prev"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["next-hour excess bp by this-hour ret quintile"] = H.groupby("pq")["ex"].agg(bp=lambda s: s.mean()*1e4, t=tstat, n="count")
    return out
