import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    recs=[]
    means={}
    for H in (2,3,5,10):
        for coin,ws in data["bars"].items():
            g=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(b)-H,H):
                    g.append(c[i+H]/c[i]-1)
            means[(coin,H)]=np.mean(g)
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]
            r10=c/c.shift(10)-1
            ext=r10/r10.abs().rolling(60,min_periods=60).mean()
            hh=hi.rolling(30).max(); ll=lo.rolling(30).min()
            nmr=(c-c.shift(30)).abs()/(hh-ll)
            mid=(hh+ll)/2
            year=pd.to_datetime(b["timestamp"]).dt.year
            cv=c.values
            for H in (2,3,5,10):
                for i in range(0,len(b)-H,H):
                    ret=cv[i+H]/cv[i]-1
                    f=b["forecast"].iloc[i]
                    situ=(nmr.iloc[i]<=0.3) and (cv[i]<mid.iloc[i]) and (r10.iloc[i]<0)
                    recs.append(dict(coin=coin,H=H,year=year.iloc[i],f=abs(f),active=f<0,
                        situ=situ,vetoed=situ and (ext.iloc[i]<=-2),r10=r10.iloc[i],
                        u=-(ret-means[(coin,H)]),tot=-ret))
    d=pd.DataFrame(recs)
    def agg(x):
        n=len(x); m=x.u.mean()
        return pd.Series(dict(n=n,mean_u=m,t=m/(x.u.std()/np.sqrt(n)) if n>2 else np.nan,mean_total=x.tot.mean()))
    a=d[d.active]
    out["active_by_horizon"]=a.groupby("H").apply(agg)
    out["active_noZEC_by_horizon"]=a[a.coin!="ZECUSD"].groupby("H").apply(agg)
    a5=a[a.H==5].copy()
    a5["r10q"]=pd.qcut(a5.r10.rank(method="first"),4,labels=["deepest","q2","q3","shallowest"])
    out["active5_by_raw_r10_quartile"]=a5.groupby("r10q").apply(agg)
    s5=d[(d.H==5)&d.situ]
    out["situ5_vetoed_vs_not"]=s5.groupby("vetoed").apply(agg)
    a5["period"]=np.where(a5.year<=2022,"2018-2022","2023-2025")
    out["active5_by_period"]=a5.groupby("period").apply(agg)
    out["active5_by_period_coin"]=a5.groupby(["period","coin"]).apply(agg)
    lo_=a5[a5.f<=a5.f.median()]; hi_=a5[a5.f>a5.f.median()]
    out["half_diff_by_period"]=pd.Series({p:(a5[(a5.period==p)&(a5.f>a5.f.median())].u.mean()-a5[(a5.period==p)&(a5.f<=a5.f.median())].u.mean()) for p in ["2018-2022","2023-2025"]})
    return out
