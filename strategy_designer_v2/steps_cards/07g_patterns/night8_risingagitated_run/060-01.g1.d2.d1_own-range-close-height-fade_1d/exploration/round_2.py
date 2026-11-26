def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<30: continue
            rng=(b.high-b.low)
            loc=(b.close-b.low)/rng.replace(0,np.nan)
            r1=b.close.shift(-1)/b.close-1
            r0=b.close/b.close.shift(1)-1
            r3=b.close/b.close.shift(3)-1
            ret60=b.close/b.close.shift(60)-1
            vol30=r0.rolling(30).std()
            inprof=b.regime.isin(["mean_reversion","unknown"])
            df=pd.DataFrame(dict(coin=coin,w=w,day=pd.to_datetime(b.timestamp).dt.floor("D"),loc=loc,r1=r1,r0=r0,r3=r3,
                z0=r0/vol30,ret60=ret60,inprof=inprof,yr=pd.to_datetime(b.timestamp).dt.year))
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1","r0"])
    drift=d.groupby("coin").r1.mean()
    d["ex"]=d.r1-d.coin.map(drift)
    def summ(g):
        s=g.groupby("day").ex.apply(lambda x:(x).sum())
        G=len(s); n=len(g)
        m=g.ex.mean()
        se=np.sqrt((s - s.index.map(g.groupby("day").size())*m).pow(2).sum()*G/(G-1))/n if G>1 else np.nan
        return pd.Series(dict(n=n,days=G,mean=m,t_day=m/se if se else np.nan))
    out={}
    p=d[d.inprof].dropna(subset=["z0"])
    p["zq"]=pd.cut(p.z0,[-99,-1.5,-0.75,-0.25,0,0.25,0.75,1.5,99])
    out["prof_by_z0"]=p.groupby("zq").apply(summ)
    up=p[p.r0>0]
    up["ret60q"]=pd.qcut(up.ret60,3,labels=["deepfall","mid","mildfall"])
    out["prof_up_by_ret60"]=up.groupby("ret60q").apply(summ)
    up["locb"]=np.where(up["loc"]>0.5,"upperhalf","lowerhalf")
    out["prof_up_by_loc"]=up.groupby("locb").apply(summ)
    up["r3q"]=pd.qcut(up.r3,3,labels=["r3low","r3mid","r3high"])
    out["prof_up_by_r3"]=up.groupby("r3q").apply(summ)
    out["prof_up_by_year"]=up.groupby("yr").apply(summ)
    out["prof_up_by_coin"]=up.groupby("coin").apply(summ)
    o=d[~d.inprof].dropna(subset=["z0"])
    o["zq"]=pd.cut(o.z0,[-99,-1.5,-0.75,-0.25,0,0.25,0.75,1.5,99])
    out["outprof_by_z0"]=o.groupby("zq").apply(summ)
    return out
