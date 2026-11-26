def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            sdy=r.rolling(365,min_periods=200).apply(lambda x: np.nan, raw=True) if False else None
            vol30=r.rolling(30,min_periods=20).std()
            volpct=vol30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            rng=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"win":w,"rw":rng/sd,"cl":(b["high"]-c)/(b["high"]-b["low"]).replace(0,np.nan),
                "ret60":c/c.shift(60)-1,"volpct":volpct,"inprof":b["regime"]!="chop",
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"ts":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in ["f1","f2"]:
        d["u"+h]=d[h]-d["coin"].map(d.groupby("coin")[h].mean())
    def summ(g,col="uf1"):
        x=g[[col,"ts"]].dropna()
        if len(x)<3: return pd.Series({"n":len(x),"days":0,"mean":np.nan,"tday":np.nan})
        s=x.groupby("ts")[col].sum(); m=x[col].mean()
        se=np.sqrt((s - x.groupby("ts")[col].count()*m).pow(2).sum())/len(x)
        return pd.Series({"n":len(x),"days":len(s),"mean":m,"tday":m/se})
    d["wide"]=pd.cut(d["rw"],[0,1,1.5,2,3,100])
    d["clq"]=pd.cut(d["cl"],[-.01,.25,.5,.75,1.01])
    d["trend"]=pd.cut(d["ret60"],[-10,-.1,.1,100],labels=["fall","chop","rise"])
    d["agit"]=np.where(d["volpct"]>0.5,"agit",np.where(d["volpct"].notna(),"calm",None))
    out={}
    rc=d[d.inprof]
    out["risingcalm wide x clq (day t)"]=rc.groupby(["wide","clq"],observed=True).apply(summ)
    # graded score: rw * cl, in rising calm, deciles
    rc=rc.assign(score=rc["rw"]*rc["cl"])
    rc["sq"]=pd.qcut(rc["score"],5,labels=False)
    out["risingcalm score quintile"]=rc.groupby("sq").apply(summ)
    out["risingcalm score q, by year"]=rc[rc.sq==4].groupby("yr").apply(summ)
    out["risingcalm score q4 f2"]=rc.groupby("sq").apply(lambda g: summ(g,"uf2"))
    # high close (cl<=.25) wide days by trend x agit
    hc=d[(d.rw>=1.5)&(d.cl<=0.25)]
    out["wide high close by trend x agit"]=hc.groupby(["trend","agit"],observed=True).apply(summ)
    hc2=d[(d.cl<=0.25)&d.trend.isin(["fall"])]
    out["falling high close by width"]=hc2.groupby("wide",observed=True).apply(summ)
    out["falling high close wide>=2 by year"]=hc2[hc2.rw>=2].groupby("yr").apply(summ)
    return out
