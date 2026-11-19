def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    def tstat(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return np.nan
        return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    # grid samples at h=72 and h=24
    rows72 = []; rows24 = []; hourly = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            ret24p = pd.Series(cl)/pd.Series(cl).shift(24)-1
            ret480 = pd.Series(cl)/pd.Series(cl).shift(480)-1
            ret168p = pd.Series(cl)/pd.Series(cl).shift(168)-1
            vol72 = r1.rolling(72).std()
            vol720 = r1.rolling(720).std()
            n = len(b)
            for h, store in ((72, rows72), (24, rows24)):
                for i in range(0, n-h, h):
                    store.append(dict(coin=c, w=w, fwd=cl[i+h]/cl[i]-1, fc=b["forecast"].iloc[i],
                                      reg=b["regime"].iloc[i], r24=ret24p.iloc[i], r168=ret168p.iloc[i], r480=ret480.iloc[i],
                                      vol=vol72.iloc[i], volrel=vol72.iloc[i]/vol720.iloc[i] if vol720.iloc[i]>0 else np.nan,
                                      wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
            hourly.append(pd.DataFrame(dict(coin=c, hr=ts.dt.hour, wd=ts.dt.weekday, r=r1.shift(-1).values)))
    g72 = pd.DataFrame(rows72); g24 = pd.DataFrame(rows24)
    for g in (g72, g24):
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def qtab(g, col, q=5, mask=None):
        d = g if mask is None else g[mask]
        d = d.dropna(subset=[col])
        d = d.assign(q=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False)))
        return d.groupby("q")["ex"].agg(mean="mean", n="count", t=tstat)
    tr = g72["fc"] > 0
    out["72h excess by regime"] = g72.groupby("reg")["ex"].agg(mean="mean", n="count", t=tstat)
    out["72h excess by forecast quintile (trending)"] = qtab(g72, "fc", mask=tr)
    out["72h excess by 20d ret quintile (all)"] = qtab(g72, "r480")
    out["72h excess by 7d ret quintile (all)"] = qtab(g72, "r168")
    out["24h excess by 24h ret quintile (all)"] = qtab(g24, "r24")
    out["24h excess by 7d ret quintile (all)"] = qtab(g24, "r168")
    out["72h excess by 72h vol quintile (all)"] = qtab(g72, "vol")
    out["72h excess by vol ratio quintile (all)"] = qtab(g72, "volrel")
    out["72h excess by 7d ret quintile (trending)"] = qtab(g72, "r168", mask=tr)
    out["72h excess by 7d ret quintile (not trending)"] = qtab(g72, "r168", mask=~tr)
    out["72h excess trending by year"] = g72[tr].groupby("yr")["ex"].agg(mean="mean", n="count", t=tstat)
    out["72h excess trending by coin"] = g72[tr].groupby("coin")["ex"].agg(mean="mean", n="count", t=tstat)
    # 7d ret correlation per coin
    out["corr 7d past vs 72h fwd, per coin (spearman)"] = g72.dropna(subset=["r168"]).groupby("coin").apply(lambda d: stats.spearmanr(d["r168"], d["fwd"])[0])
    H = pd.concat(hourly).dropna()
    H["ex"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    out["hourly excess by hour (bp)"] = H.groupby("hr")["ex"].agg(mean=lambda s: s.mean()*1e4, t=tstat, n="count")
    # daily
    D = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"]=c; dd["w"]=w
            dd["day"]=pd.to_datetime(dd["day"])
            dd["next"] = dd["coin_return"].shift(-1)
            dd["prev"] = dd["coin_return"]
            D.append(dd)
    D = pd.concat(D)
    D["cex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    D["wd"] = D["day"].dt.weekday
    out["coin daily excess by weekday"] = D.groupby("wd")["cex"].agg(mean="mean", t=tstat, n="count")
    out["book daily return by weekday"] = D.groupby("wd")["book_return"].agg(mean="mean", t=tstat, n="count")
    # book extremes: coin's next day return after book's top/bottom 5% days
    Db = D.dropna(subset=["book_return","next"])
    Db = Db[Db["book_return"]!=0]
    lo, hi = Db["book_return"].quantile([0.05,0.95])
    Db["nex"] = Db["next"] - Db.groupby("coin")["coin_return"].transform("mean")
    out["coin next-day excess after book extremes"] = pd.DataFrame({
        "worst5%": [Db[Db.book_return<=lo]["nex"].mean(), tstat(Db[Db.book_return<=lo]["nex"]), (Db.book_return<=lo).sum()],
        "best5%": [Db[Db.book_return>=hi]["nex"].mean(), tstat(Db[Db.book_return>=hi]["nex"]), (Db.book_return>=hi).sum()],
        "middle": [Db[(Db.book_return>lo)&(Db.book_return<hi)]["nex"].mean(), tstat(Db[(Db.book_return>lo)&(Db.book_return<hi)]["nex"]), ((Db.book_return>lo)&(Db.book_return<hi)).sum()]},
        index=["mean","t","n"])
    # all days: next-day excess by today's coin return quintile
    Dq = D.dropna(subset=["coin_return","next"]).copy()
    Dq["nex"] = Dq["next"] - Dq.groupby("coin")["coin_return"].transform("mean")
    Dq["q"] = Dq.groupby("coin")["coin_return"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["next-day excess by today return quintile"] = Dq.groupby("q")["nex"].agg(mean="mean", t=tstat, n="count")
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    T["dur_d"] = T["duration_minutes"]/1440
    T["dq"] = pd.qcut(T["dur_d"].rank(method="first"),5,labels=False)
    out["trades by duration quintile"] = T.groupby("dq").agg(dur_d=("dur_d","mean"), pnl=("net_profit_loss_percent","mean"), n=("coin","count"), win=("net_profit_loss_percent", lambda s:(s>0).mean()))
    return out
