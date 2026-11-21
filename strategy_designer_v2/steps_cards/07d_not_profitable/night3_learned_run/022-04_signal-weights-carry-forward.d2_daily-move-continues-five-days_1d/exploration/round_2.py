def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-5,5)
            g+=list(c[idx+5]/c[idx]-1)
        mu=np.mean(g)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            r20=c/c.shift(20)-1
            vol=r1.rolling(20).std()
            vol120=r1.rolling(120,min_periods=40).std()
            sd20=r1.rolling(20).std()*np.sqrt(20)
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0,len(b)-5,5):
                f=b["forecast"].iloc[i]
                if pd.isna(f) or f==0 or pd.isna(r20.iloc[i]): continue
                fr=c.iloc[i+5]/c.iloc[i]-1
                s=np.sign(f)
                rows.append(dict(coin=coin,yr=yr.iloc[i],af=abs(f),s=s,
                    sig=s*(fr-mu),tot=s*fr,
                    r20z=s*r20.iloc[i]/sd20.iloc[i] if sd20.iloc[i]>0 else np.nan,
                    vr=vol.iloc[i]/vol120.iloc[i] if not pd.isna(vol120.iloc[i]) else np.nan,
                    t20=np.sign(r20.iloc[i]), tr20=np.sign(r20.iloc[i])*(fr-mu)))
    d=pd.DataFrame(rows).dropna()
    def agg(x,col="sig"):
        v=x[col]
        return pd.Series(dict(n=len(v),bps=v.mean()*1e4,t=v.mean()/(v.std()/np.sqrt(len(v)))))
    out={}
    d["agree"]=d.r20z>0
    d["vq"]=pd.qcut(d.vr,3,labels=False)
    out["agree_x_vq"]=d.groupby(["agree","vq"]).apply(agg)
    a=d[d.agree].copy()
    a["zq"]=pd.qcut(a.r20z,4,labels=False)
    out["agree_by_r20z_quartile"]=a.groupby("zq").apply(agg)
    out["agree_by_coin"]=a.groupby("coin").apply(agg)
    out["agree_by_year"]=a.groupby("yr").apply(agg)
    out["agree_by_side"]=a.groupby("s").apply(agg)
    out["agree_by_afbin"]=a.groupby(pd.cut(a.af,[0,5,10,15,20.1])).apply(agg)
    # pure 20d trend signal, all cases, graded by |z|
    d["az"]=pd.qcut(d.r20z.abs(),4,labels=False)
    out["trend20_by_absz_quartile"]=d.groupby("az").apply(lambda x:agg(x,"tr20"))
    out["trend20_by_vq"]=d.groupby("vq").apply(lambda x:agg(x,"tr20"))
    return out
