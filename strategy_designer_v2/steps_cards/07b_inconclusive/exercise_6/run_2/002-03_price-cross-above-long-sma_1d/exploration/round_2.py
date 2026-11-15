def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]
    rows=[];blocks=[]
    for coin,ws in bars.items():
        rets=[]
        for w,df in ws.items():
            c=df["close"].values; rets.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(rets))
        for w,df in ws.items():
            c=df["close"].values; n=len(c); h=20
            f=df["forecast"].values; a=df["postRebalance_current_allocation"].values
            raw=df["debug_info.components.above_ma.last_history_value"].values if "debug_info.components.above_ma.last_history_value" in df else np.full(n,np.nan)
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            ex=np.full(n,np.nan); ex[:n-h]=c[h:]/c[:n-h]-1-h*mu
            past=np.full(n,np.nan); past[h:]=c[h:]/c[:n-h]-1
            for i in range(0,n,h):
                seg=slice(i,min(i+h,n)); e=ex[seg]; al=a[seg]; m=~np.isnan(e)
                if m.sum()==0: continue
                blocks.append(dict(coin=coin,yr=yr[i],v=np.sum(al[m]*e[m]),nz=np.any(al[m]!=0),f0=f[i],raw0=raw[i],past=past[i],e0=ex[i]))
    b=pd.DataFrame(blocks)
    def tt(x):
        x=x.dropna();return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    out["all"]=tt(b.v)
    out["coin"]=b.groupby("coin").v.apply(tt).unstack()
    out["yr"]=b.groupby("yr").v.apply(tt).unstack()
    on=b[b.f0>0].copy()
    on["q"]=pd.qcut(on.f0.rank(method="first"),4,labels=False)
    out["fq_e0"]=on.groupby("q").e0.apply(tt).unstack()
    out["fq_v"]=on.groupby("q").v.apply(tt).unstack()
    on["rq"]=pd.qcut(on.raw0.rank(method="first"),4,labels=False)
    out["rawq_e0"]=on.groupby("rq").e0.apply(tt).unstack()
    on["pq"]=pd.qcut(on.past.rank(method="first"),3,labels=False)
    out["past20_on"]=on.groupby("pq").e0.apply(tt).unstack()
    out["share_v_top_q"]=float(on[on.q==3].v.sum()/b.v.sum())
    out["v_excl_top_coin"]=b.groupby("coin").v.sum()
    return out
