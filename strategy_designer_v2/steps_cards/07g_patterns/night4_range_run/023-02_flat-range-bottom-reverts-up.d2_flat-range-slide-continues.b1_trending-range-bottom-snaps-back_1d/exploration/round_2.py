def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            hh=h.rolling(30).max(); ll=l.rolling(30).min(); rng=hh-ll
            nm=(c-c.shift(30)).abs()/rng
            stoch=(c-ll)/rng
            r10=c/c.shift(10)-1
            f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame(dict(coin=coin,w=w,yr=ts.dt.year,r10=r10,nm=nm,stoch=stoch,f5=f5))
            rows.append(df.iloc[::5])
        for w,d in data["days"][coin].items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; drows.append(dd)
    g=pd.concat(rows).dropna(subset=["f5","r10","nm"])
    g["ex"]=g["f5"]-g.groupby("coin")["f5"].transform("mean")
    g["exz"]=g["ex"]/g.groupby("coin")["f5"].transform("std")
    g["r10z"]=g["r10"]/g.groupby("coin")["r10"].transform("std")
    out={}
    def reg(x,col="r10z"):
        x=x.dropna(subset=[col,"exz"])
        if len(x)<10: return pd.Series(dict(n=len(x),slope=np.nan,t=np.nan))
        s=stats.linregress(x[col],x["exz"])
        return pd.Series(dict(n=len(x),slope=s.slope,t=s.slope/s.stderr))
    fl=g[g.nm<0.5]; tr=g[g.nm>=0.5]
    out["flat: exz on r10z pooled"]=reg(fl)
    out["trend: exz on r10z pooled"]=reg(tr)
    out["flat: by coin"]=fl.groupby("coin").apply(reg)
    out["flat: by year"]=fl.groupby("yr").apply(reg)
    out["flat: exz on stoch by coin"]=fl.groupby("coin").apply(lambda x:reg(x,"stoch"))
    tr2=tr.copy(); tr2["absr"]=tr2["r10z"].abs()
    out["trend: exz on |r10z| by coin"]=tr2.groupby("coin").apply(lambda x:reg(x,"absr"))
    out["trend: exz on |r10z| pooled"]=reg(tr2,"absr")
    D=pd.concat(drows); D["wd"]=pd.to_datetime(D["day"]).dt.weekday; D["yr"]=pd.to_datetime(D["day"]).dt.year
    def tt(s):
        s=s.dropna(); return pd.Series(dict(mean=s.mean(),n=len(s),t=s.mean()/(s.std()/np.sqrt(len(s)))))
    cs=D.groupby(["w","day","wd","yr"])["coin_return"].mean().reset_index()
    out["weekday, coins averaged per day"]=cs.groupby("wd")["coin_return"].apply(tt).unstack()
    out["saturday by coin"]=D[D.wd==5].groupby("coin")["coin_return"].apply(tt).unstack()
    out["saturday by year (coin avg)"]=cs[cs.wd==5].groupby("yr")["coin_return"].apply(tt).unstack()
    out["sat minus other days by year"]=cs.groupby("yr").apply(lambda x: x[x.wd==5].coin_return.mean()-x[x.wd!=5].coin_return.mean())
    return out
