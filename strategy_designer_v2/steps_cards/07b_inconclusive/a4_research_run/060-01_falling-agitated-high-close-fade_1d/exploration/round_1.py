def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean daily return over all windows
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(allr))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            n=len(b)
            rng=h-l
            loc=np.where(rng>0,2*(c-l)/rng-1,np.nan)
            for H in (1,2,3,5):
                fr=np.full(n,np.nan)
                fr[:n-H]=c[H:]/c[:-H]-1
                b[f"r{H}"]=fr
            ts=pd.to_datetime(b["timestamp"])
            for i in range(n):
                rows.append(dict(coin=coin,w=w,year=ts[i].year,day=ts[i].normalize(),
                    regime=b["regime"].iloc[i],fc=b["forecast"].iloc[i],loc=loc[i],
                    r1=b["r1"].iloc[i],r2=b["r2"].iloc[i],r3=b["r3"].iloc[i],r5=b["r5"].iloc[i],mu=mu,
                    rng=rng[i]/c[i]))
    d=pd.DataFrame(rows)
    d["ex1"]=-(d["r1"]-d["mu"])
    def summ(g,col="ex1"):
        g=g.dropna(subset=[col])
        if len(g)<3: return pd.Series(dict(n=len(g),mean=np.nan,t=np.nan))
        s=g.groupby("day")[col].apply(lambda x:(x-g[col].mean()).sum())
        nd=len(s); se=np.sqrt((s**2).sum()*nd/(nd-1))/len(g)
        return pd.Series(dict(n=len(g),days=nd,mean=g[col].mean(),t=g[col].mean()/se))
    out={}
    out["regime counts"]=d["regime"].value_counts()
    cases=d[d.fc<0]
    out["cases all"]=summ(cases)
    out["cases by coin"]=cases.groupby("coin").apply(summ)
    out["cases by window"]=cases.groupby("w").apply(summ)
    inprof=d[d.regime.isin(["mean_reversion","unknown"])].copy()
    inprof["lq"]=pd.cut(inprof["loc"],[-1.01,-0.5,0,0.5,0.8,1.01])
    out["in profile by close location (short excess 1d)"]=inprof.groupby("lq").apply(summ)
    chop=d[d.regime=="chop"].copy()
    chop["lq"]=pd.cut(chop["loc"],[-1.01,-0.5,0,0.5,0.8,1.01])
    out["out of profile by close location"]=chop.groupby("lq").apply(summ)
    hz={}
    for H in (2,3,5):
        cc=cases.copy(); cc[f"e{H}"]=-(cc[f"r{H}"]-H*cc["mu"])
        hz[H]=summ(cc,f"e{H}")
    out["cases longer horizons (overlapping, rough)"]=pd.DataFrame(hz).T
    cases=cases.copy(); cases["rq"]=pd.qcut(cases["rng"],3,labels=["narrow","mid","wide"])
    out["cases by day range"]=cases.groupby("rq").apply(summ)
    out["cases by year"]=cases.groupby("year").apply(summ)
    return out
