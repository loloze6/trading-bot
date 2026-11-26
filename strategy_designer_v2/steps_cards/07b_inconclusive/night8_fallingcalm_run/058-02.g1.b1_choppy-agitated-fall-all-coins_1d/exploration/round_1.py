import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    # mean h-return per coin over all windows (grid)
    def coin_mean(coin, h):
        rs=[]
        for w,df in bars[coin].items():
            c=df["close"].values
            for i in range(0,len(c)-h,h):
                rs.append(c[i+h]/c[i]-1)
        return np.mean(rs) if rs else np.nan, np.std(rs) if rs else np.nan
    rows=[]
    for h in [1,3,5,10,20]:
        for coin in bars:
            m,s=coin_mean(coin,h)
            for w,df in bars[coin].items():
                df=df.reset_index(drop=True)
                c=df["close"].values; f=df["forecast"].values; v=df["volume"].values
                ts=pd.to_datetime(df["timestamp"])
                r30=pd.Series(c).pct_change(30).values
                vr=(pd.Series(v).rolling(30).mean()/pd.Series(v).rolling(60).mean()).values
                inprof=(df["regime"]!="chop").values
                for i in range(0,len(c)-h,h):
                    rows.append(dict(h=h,coin=coin,w=w,year=ts[i].year,f=f[i],inprof=inprof[i],
                        r30=r30[i],vr=vr[i],ex=-(c[i+h]/c[i]-1-m),tot=-(c[i+h]/c[i]-1),z=-(c[i+h]/c[i]-1-m)/s,day=ts[i].normalize()))
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["ex"]; n=len(x)
        t=x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series(dict(n=n,mean_ex=x.mean(),t=t,mean_tot=g["tot"].mean(),strength=g["z"].mean()))
    cases=d[d.f<0]
    out={}
    out["by_h"]=cases.groupby("h").apply(summ)
    c5=cases[cases.h==5].copy()
    out["by_coin"]=c5.groupby("coin").apply(summ)
    out["by_year"]=c5.groupby("year").apply(summ)
    out["by_window"]=c5.groupby("w").apply(summ)
    c5["fq"]=pd.qcut(c5.f.rank(method="first"),3,labels=["deep","mid","shallow"])
    out["by_depth"]=c5.groupby("fq").apply(summ)
    c5b=c5.dropna(subset=["vr"]).copy()
    c5b["vq"]=pd.qcut(c5b.vr.rank(method="first"),2,labels=["quiet","heavy"])
    out["by_volume"]=c5b.groupby("vq").apply(summ)
    # out of profile: 30d falls outside profile
    o=d[(~d.inprof)&(d.r30<0)]
    out["outprof_fall_by_h"]=o.groupby("h").apply(summ)
    o5=o[o.h==5].copy()
    o5["rq"]=pd.qcut(o5.r30.rank(method="first"),3,labels=["deep","mid","shallow"])
    out["outprof_fall5_by_depth"]=o5.groupby("rq").apply(summ)
    return out
