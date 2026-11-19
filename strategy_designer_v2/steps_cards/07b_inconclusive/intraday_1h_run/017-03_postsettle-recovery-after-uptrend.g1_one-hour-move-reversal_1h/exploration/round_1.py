def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            r=df["close"].shift(-1)/df["close"]-1
            allr.append(r.dropna())
        mu=pd.concat(allr).mean()
        for w,df in ws.items():
            c=df["close"]; r1=c.shift(-1)/c-1
            past=c/c.shift(1)-1
            vol720=past.rolling(720,min_periods=720).std()
            a=df["postRebalance_current_allocation"]
            ex=a*(r1-mu)
            z=past/past.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"ex":ex,"vol":vol720,"fc":df["forecast"],
                            "hour":pd.to_datetime(df["timestamp"]).dt.hour,"year":pd.to_datetime(df["timestamp"]).dt.year,
                            "z":z,"r1":r1,"past":past,"a":a,"turn":(a-df["previous_allocation"]).abs()})
            rows.append(d.dropna(subset=["ex"]))
    D=pd.concat(rows,ignore_index=True)
    D["med"]=D.groupby("coin")["vol"].transform("median")
    D["vg"]=np.where(D.vol>D.med,"high",np.where(D.vol<D.med,"low",None))
    D.loc[D.vol.isna(),"vg"]=None
    def t(x): x=x.dropna(); return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    out={}
    out["by_coin"]=D.groupby("coin").ex.agg(["mean","count",t])
    out["by_year"]=D.groupby("year").ex.agg(["mean","count",t])
    out["by_volgroup"]=D.groupby("vg").ex.agg(["mean","count",t])
    out["by_coin_vg"]=D.groupby(["coin","vg"]).ex.agg(["mean","count",t]).unstack()
    D["vq"]=D.groupby("coin").vol.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["by_volquintile"]=D.groupby("vq").ex.agg(["mean","count",t])
    D["fq"]=pd.cut(D.fc.abs(),[-0.01,2,5,10,15,20.1])
    out["by_absforecast"]=D.groupby("fq").ex.agg(["mean","count",t])
    # unscaled slope: next return vs past standardized move
    D["sgn"]=-np.sign(D.past)*(D.r1)
    D["zq"]=pd.qcut(D.z.abs(),5,labels=False,duplicates="drop")
    out["fade_raw_by_absz"]=D.groupby("zq").sgn.agg(["mean","count",t])
    out["by_hour"]=D.groupby("hour").ex.agg(["mean",t])
    out["turnover_mean"]=float(D.turn.mean())
    out["abs_alloc_mean"]=float(D.a.abs().mean())
    out["gross_mean"]=float(D.ex.mean())
    return out
