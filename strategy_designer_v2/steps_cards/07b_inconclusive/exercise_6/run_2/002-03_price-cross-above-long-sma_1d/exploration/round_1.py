def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    rows=[]
    for coin,ws in bars.items():
        # pooled mean daily return
        rets=[]
        for w,df in ws.items():
            c=df["close"].values; rets.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(rets))
        for w,df in ws.items():
            c=df["close"].values; n=len(c)
            f=df["forecast"].values; a=df["postRebalance_current_allocation"].values
            raw=df.get("debug_info.components.above_ma.last_history_value",pd.Series(np.nan,index=df.index)).values
            for h in [5,10,20,40,60]:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,f=f[i],a=a[i],raw=raw[i],
                        ex=c[i+h]/c[i]-1-h*mu, yr=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    out={}
    def tt(x):
        x=x.dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    d["on"]=d.f>0
    out["by_h_on"]=d.groupby(["h","on"]).ex.apply(tt).unstack()
    d20=d[d.h==20].copy()
    out["coin_on"]=d20.groupby(["coin","on"]).ex.apply(tt).unstack()
    out["year_on"]=d20.groupby(["yr","on"]).ex.apply(tt).unstack()
    pos=d20[d20.on].copy()
    pos["q"]=pd.qcut(pos.f.rank(method="first"),4,labels=False)
    out["fq"]=pos.groupby("q").agg(fmean=("f","mean"),rawmean=("raw","mean"),n=("ex","size"),ex=("ex","mean"),win=("ex",lambda x:(x>0).mean()))
    pos40=d[(d.h==40)&d.on].copy(); pos40["q"]=pd.qcut(pos40.f.rank(method="first"),4,labels=False)
    out["fq40"]=pos40.groupby("q").agg(fmean=("f","mean"),n=("ex","size"),ex=("ex","mean"))
    out["med_ex_on20"]=float(pos.ex.median())
    out["raw_desc"]=d20.raw.describe()
    return out
