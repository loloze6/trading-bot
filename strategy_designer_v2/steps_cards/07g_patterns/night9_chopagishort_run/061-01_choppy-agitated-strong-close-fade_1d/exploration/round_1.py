def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values; o=b["open"].values
            rng=h-l
            loc=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            r1=pd.Series(c).pct_change().values
            r5=pd.Series(c).pct_change(5).values
            vol10=pd.Series(r1).rolling(10).std().values
            rngrel=rng/c
            rr=pd.Series(rngrel).rolling(20).mean().values
            inprof=(b["regime"]!="chop").values
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-2,2):
                rows.append(dict(coin=coin,w=w,loc=loc[i],r1=r1[i],r5=r5[i],vol10=vol10[i],
                    wide=rngrel[i]/rr[i] if rr[i]>0 else np.nan, inprof=inprof[i],
                    wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                    f2=c[i+2]/c[i]-1, f1=c[i+1]/c[i]-1))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["f2"].mean()
    d["u2"]=d["f2"]-d["coin"].map(drift)
    def summ(g):
        x=g["u2"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    d["locq"]=pd.cut(d["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True)
    out["loc x inprof"]=d.groupby(["inprof","locq"]).apply(summ)
    d["r1q"]=pd.qcut(d["r1"],5)
    out["r1 x inprof"]=d.groupby(["inprof","r1q"]).apply(summ)
    d["r5q"]=pd.qcut(d["r5"],5)
    out["r5 quintile"]=d.groupby("r5q").apply(summ)
    d["wideq"]=pd.qcut(d["wide"],4)
    out["wide x high loc"]=d[d["loc"]>=0.8].groupby("wideq").apply(summ)
    out["wide x low loc"]=d[d["loc"]<=0.2].groupby("wideq").apply(summ)
    out["weekday"]=d.groupby("wd").apply(summ)
    out["inprof share"]=float(d["inprof"].mean())
    # high loc in profile by coin and year
    hp=d[(d["loc"]>=0.8)&d["inprof"]]
    out["hiloc inprof by coin"]=hp.groupby("coin").apply(summ)
    out["hiloc inprof by year"]=hp.groupby("yr").apply(summ)
    # corr loc vs u2 overall
    dd=d.dropna(subset=["loc","u2","r1"])
    out["corr loc,u2 all"]=float(stats.spearmanr(dd["loc"],dd["u2"])[0])
    out["corr r1,u2 all"]=float(stats.spearmanr(dd["r1"],dd["u2"])[0])
    # book days
    bd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            bd.append(x.assign(coin=coin,w=w))
    bd=pd.concat(bd)
    out["book by window"]=bd.groupby("w")["book_return"].agg(["mean","std","count"])
    return out
