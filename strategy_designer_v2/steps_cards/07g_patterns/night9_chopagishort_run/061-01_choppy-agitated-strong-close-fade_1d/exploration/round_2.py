def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            rng=h-l
            loc=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            r1=pd.Series(c).pct_change().values
            r5=pd.Series(c).pct_change(5).values
            r60=pd.Series(c).pct_change(60).values
            sd30=pd.Series(r1).rolling(30).std().values
            sd90=pd.Series(r1).rolling(90).std().values
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-2,2):
                rows.append(dict(coin=coin,w=w,loc=loc[i],r1=r1[i],r5=r5[i],r60=r60[i],
                    ag=sd30[i]/sd90[i] if sd90[i]>0 else np.nan,
                    wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                    f2=c[i+2]/c[i]-1, f1=c[i+1]/c[i]-1))
    d=pd.DataFrame(rows)
    d["u2"]=d["f2"]-d["coin"].map(d.groupby("coin")["f2"].mean())
    d["u1"]=d["f1"]-d["coin"].map(d.groupby("coin")["f1"].mean())
    def summ(g,col="u2"):
        x=g[col].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    d["trend"]=pd.cut(d["r60"],[-10,-0.1,0.1,100],labels=["falling","choppy","rising"])
    d["agit"]=np.where(d["ag"].isna(),None,np.where(d["ag"]>1,"agit","calm"))
    d["locq"]=pd.cut(d["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True)
    hi=d[d["loc"]>=0.8]
    out["hiloc by trend"]=hi.groupby("trend").apply(summ)
    out["hiloc by trend x agit"]=hi.dropna(subset=["agit"]).groupby(["trend","agit"]).apply(summ)
    out["hiloc by window"]=hi.groupby("w").apply(summ)
    out["hiloc by year"]=hi.groupby("yr").apply(summ)
    out["hiloc by coin"]=hi.groupby("coin").apply(summ)
    out["hiloc next1"]=summ(hi,"u1")
    d["hiq"]=pd.cut(d["loc"],[0.8,0.9,0.95,1.0001])
    out["hiloc grade"]=d[d["loc"]>=0.8].groupby("hiq").apply(summ)
    hi2=d[(d["loc"]>=0.8)]
    out["hiloc x r1 sign"]=hi2.groupby(hi2["r1"]>0).apply(summ)
    d["r5q"]=pd.qcut(d["r5"],5)
    out["r5 by trend"]=d.groupby(["trend","r5q"]).apply(summ)
    out["r5 top-bottom by year"]=d.groupby("yr").apply(lambda g: pd.Series(dict(
        top=g[g["r5"]>0.083]["u2"].mean(),bot=g[g["r5"]<-0.0744]["u2"].mean(),n=len(g))))
    out["sunday by year"]=d[d["wd"]==6].groupby("yr").apply(summ)
    out["thursday by year"]=d[d["wd"]==3].groupby("yr").apply(summ)
    return out
