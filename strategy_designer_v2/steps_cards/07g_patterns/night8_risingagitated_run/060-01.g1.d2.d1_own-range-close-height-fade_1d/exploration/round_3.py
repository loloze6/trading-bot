def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<30: continue
            rng=(b.high-b.low)
            r1=b.close.shift(-1)/b.close-1
            r0=b.close/b.close.shift(1)-1
            vol30=r0.rolling(30).std()
            width=rng/rng.rolling(20).mean()
            vr=b.volume/b.volume.rolling(20).mean()
            ma10=b.close.rolling(10).mean()
            dma=(b.close/ma10-1)/vol30
            hi20=b.high.rolling(20).max(); lo20=b.low.rolling(20).min()
            pos20=(b.close-lo20)/(hi20-lo20)
            nup=(r0>0).astype(int).rolling(3).sum()
            inprof=b.regime.isin(["mean_reversion","unknown"])
            df=pd.DataFrame(dict(coin=coin,w=w,day=pd.to_datetime(b.timestamp).dt.floor("D"),r1=r1,r0=r0,
                width=width,vr=vr,dma=dma,pos20=pos20,nup=nup,inprof=inprof))
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1","r0"])
    drift=d.groupby("coin").r1.mean()
    d["ex"]=d.r1-d.coin.map(drift)
    def summ(g):
        g=g.dropna(subset=["ex"])
        s=g.groupby("day").ex.sum(); c=g.groupby("day").size()
        G=len(s); n=len(g); m=g.ex.mean()
        se=np.sqrt(((s-c*m)**2).sum()*G/(G-1))/n if G>1 else np.nan
        return pd.Series(dict(n=n,days=G,mean=m,t_day=m/se if se else np.nan))
    out={}
    up=d[d.inprof&(d.r0>0)].copy()
    for col in ["width","vr","dma","pos20"]:
        x=up.dropna(subset=[col]).copy()
        x["q"]=pd.qcut(x[col],3,labels=["low","mid","high"])
        out["up_by_"+col]=x.groupby("q").apply(summ)
    out["up_by_nup3"]=up.dropna(subset=["nup"]).groupby("nup").apply(summ)
    o=d[(~d.inprof)&(d.r0>0)].dropna(subset=["pos20"]).copy()
    o["q"]=pd.qcut(o.pos20,3,labels=["low","mid","high"])
    out["outprof_up_by_pos20"]=o.groupby("q").apply(summ)
    out["prof_all_updays"]=summ(up).to_frame().T
    out["prof_all_downdays"]=summ(d[d.inprof&(d.r0<=0)]).to_frame().T
    return out
