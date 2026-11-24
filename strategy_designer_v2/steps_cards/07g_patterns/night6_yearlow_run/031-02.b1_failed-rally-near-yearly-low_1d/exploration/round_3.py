def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=pd.Series(b["close"].values,dtype=float)
            r1=c.pct_change()
            vol=r1.rolling(20).std().shift(1)
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for i in range(61,n-1):
                rows.append(dict(coin=coin,w=w,wn=int(w[1:]),day=ts.iloc[i].normalize(),
                    z=r1.iloc[i]/vol.iloc[i],nx1=c.iloc[i+1]/c.iloc[i]-1,
                    p60=c.iloc[i]/c.iloc[i-60]-1,p20=c.iloc[i]/c.iloc[i-20]-1,
                    nx20=(c.iloc[i+20]/c.iloc[i]-1) if (i+20<n and (i-61)%20==0) else np.nan))
    d=pd.DataFrame(rows).dropna(subset=["z","p60"])
    d["e1"]=d.nx1-d.groupby("coin").nx1.transform("mean")
    d["p1"]=-d.z.clip(-4,4)*d.e1
    out={}
    def clus(x,col="p1"):
        p=x.groupby("day")[col].sum()
        return pd.Series(dict(mean=p.mean(),t=p.mean()/(p.std()/np.sqrt(len(p))),days=len(p)))
    d["down60"]=d.p60<=0
    out["rev1_clustered_by_down60"]=d.groupby("down60").apply(clus).round(5)
    d["half"]=np.where(d.wn<=12,"w1-w12","w13-w24")
    out["rev1_clustered_by_down60_half"]=d.groupby(["down60","half"]).apply(clus).round(5)
    dn=d[d.down60]
    a=dn.assign(zb=pd.cut(dn.z,[-99,-2,-1,0,1,2,99])).groupby("zb").e1.agg(["size","mean","std"])
    a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"]));out["down60_next1d_by_z"]=a.round(5)
    d["p60q"]=pd.qcut(d.p60,5,labels=False)
    out["rev1_clustered_by_p60_quintile"]=d.groupby("p60q").apply(clus).round(5)
    out["rev1_clustered_by_coin_down60"]=dn.groupby("coin").apply(clus).round(5)
    return out
