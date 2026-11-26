def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=pd.Series(b["close"].values,dtype=float)
            r1=c.pct_change()
            vol=r1.rolling(20).std().shift(1)
            lo365=c.rolling(365,min_periods=91).min()
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for i in range(21,n-3):
                rows.append(dict(coin=coin,w=w,day=ts.iloc[i].normalize(),yr=ts.iloc[i].year,
                    z=r1.iloc[i]/vol.iloc[i],nx1=c.iloc[i+1]/c.iloc[i]-1,
                    nx3=c.iloc[i+3]/c.iloc[i]-1 if i%3==0 else np.nan,
                    dlow=c.iloc[i]/lo365.iloc[i]-1,reg=b["regime"].iloc[i]))
    d=pd.DataFrame(rows).dropna(subset=["z"])
    d["e1"]=d.nx1-d.groupby("coin").nx1.transform("mean")
    d["e3"]=d.nx3-d.groupby("coin").nx3.transform("mean")
    d["sig"]=-d.z.clip(-4,4)*d.groupby("coin").nx1.transform("std")  # reversal direction weight
    out={}
    # day-clustered t of slope: per day sum of (-z*e1)
    d["p1"]=-d.z.clip(-4,4)*d.e1
    pdy=d.groupby("day").p1.sum()
    out["rev1_dayclustered"]=pd.Series(dict(mean=pdy.mean(),t=pdy.mean()/(pdy.std()/np.sqrt(len(pdy))),days=len(pdy)))
    d3=d.dropna(subset=["e3"]).copy(); d3["p3"]=-d3.z.clip(-4,4)*d3.e3
    p3=d3.groupby("day").p3.sum()
    out["rev3_dayclustered"]=pd.Series(dict(mean=p3.mean(),t=p3.mean()/(p3.std()/np.sqrt(len(p3))),days=len(p3)))
    def corr_t(x):
        r,p=stats.pearsonr(-x.z.clip(-4,4),x.e1);n=len(x)
        return pd.Series(dict(n=n,r=r,t=r*np.sqrt((n-2)/(1-r*r))))
    out["rev1_by_coin"]=d.groupby("coin").apply(corr_t).round(4)
    out["rev1_by_year"]=d.groupby("yr").apply(corr_t).round(4)
    out["rev1_by_regime"]=d.groupby("reg").apply(corr_t).round(4)
    d["lowq"]=pd.qcut(d.dlow,4,labels=False,duplicates="drop")
    out["rev1_by_dist_low_q"]=d.dropna(subset=["dlow"]).groupby("lowq").apply(corr_t).round(4)
    d["zb"]=pd.cut(d.z,[-99,-2,-1,0,1,2,99])
    a=d3.assign(zb=pd.cut(d3.z,[-99,-2,-1,0,1,2,99])).groupby("zb").e3.agg(["size","mean","std"])
    a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"]));out["next3d_by_z"]=a.round(5)
    return out
