def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=84
    rows=[]; gen=[]; hourly=[]; drift={}
    for coin,ws in data["bars"].items():
        f84=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            for i in range(0,n-H,H): f84.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(f84); sd=np.std(f84)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])/c
            ratio=rng.rolling(6).mean()/rng.rolling(180).mean()
            r6=c/c.shift(6)-1
            vol6=r6.abs().rolling(180).mean()
            z6=r6/vol6
            r180=c/c.shift(180)-1
            fwd=c.shift(-H)/c-1
            fwd6=c.shift(-6)/c-1
            n=len(c)
            for s in range(0,n-H,H):
                cell=slice(s,s+H)
                rr=ratio.iloc[cell]; 
                # generic grid sample
                gen.append(dict(coin=coin,w=w,z6=z6.iloc[s],ratio=ratio.iloc[s],r180=r180.iloc[s],
                    fwd=fwd.iloc[s]-drift[coin],sd=sd))
                idx=[j for j in range(s,s+H) if ratio.iloc[j]>=2 and j+H<n]
                if idx:
                    j=idx[0]
                    rows.append(dict(coin=coin,w=w,ratio=ratio.iloc[j],r6=r6.iloc[j],z6=z6.iloc[j],
                        r180=r180.iloc[j],un=fwd.iloc[j]-drift[coin],un6=fwd6.iloc[j],strength=(fwd.iloc[j]-drift[coin])/sd,
                        fc=b["forecast"].iloc[j]))
            ts=pd.to_datetime(b["timestamp"])
            r1=c.pct_change().shift(-1)
            hourly.append(pd.DataFrame(dict(h=ts.dt.hour,wd=ts.dt.weekday,r=r1,coin=coin)))
    P=pd.DataFrame(rows); G=pd.DataFrame(gen).dropna(); Hh=pd.concat(hourly).dropna()
    def summ(df,col="un"):
        x=df[col].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    P["rbin"]=pd.cut(P.ratio,[2,2.5,3,4,100])
    P["dir"]=np.where(P.r6<0,"fall","rise")
    out["panic by ratio x dir"]=P.groupby(["rbin","dir"]).apply(summ).round(4)
    P["trend"]=np.where(P.r180>0,"up30d","down30d")
    out["panic>=3 by dir x 30d trend"]=P[P.ratio>=3].groupby(["dir","trend"]).apply(summ).round(4)
    P3=P[(P.ratio>=2.5)]
    P3["zq"]=pd.qcut(P3.z6,4,labels=False,duplicates="drop")
    out["panic>=2.5 by z6 quartile"]=P3.groupby("zq").apply(lambda d:pd.concat([summ(d),pd.Series({"z6":d.z6.mean()})])).round(4)
    out["panic>=2.5 by coin"]=P3.groupby("coin").apply(summ).round(4)
    out["panic>=2.5 fwd 24h"]=P3.groupby("dir").apply(lambda d:summ(d,"un6")).round(4)
    G["zq"]=pd.qcut(G.z6,5,labels=False)
    out["all grid by z6 quintile"]=G.groupby("zq").apply(lambda d:pd.concat([summ(d,"fwd"),pd.Series({"z6":d.z6.mean()})])).round(4)
    G["vq"]=pd.qcut(G.ratio,5,labels=False)
    out["all grid by range ratio quintile"]=G.groupby("vq").apply(lambda d:pd.concat([summ(d,"fwd"),pd.Series({"ratio":d.ratio.mean()})])).round(4)
    G["tq"]=pd.qcut(G.r180,5,labels=False)
    out["all grid by 30d ret quintile"]=G.groupby("tq").apply(lambda d:pd.concat([summ(d,"fwd"),pd.Series({"r180":d.r180.mean()})])).round(4)
    hh=Hh.groupby("h").r.agg(["count","mean","std"]); hh["t"]=hh["mean"]/(hh["std"]/np.sqrt(hh["count"]))
    out["by hour 4h ret"]=hh.round(5)
    wd=Hh.groupby("wd").r.agg(["count","mean","std"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["by weekday"]=wd.round(5)
    return out
