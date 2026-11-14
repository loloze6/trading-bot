def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["r"]=d["close"].pct_change()
            d["r_next"]=d["r"].shift(-1)
            d["wd_next"]=d["ts"].shift(-1).dt.dayofweek
            d["wd"]=d["ts"].dt.dayofweek
            d["vol20"]=d["r"].rolling(20).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["r5"]=d["close"].pct_change(5)
            d["ma50"]=d["close"]/d["close"].rolling(50).mean()-1
            d["coin"]=coin; d["w"]=w; d["year"]=d["ts"].dt.year
            d["rng"]=(d["high"]-d["low"])/d["close"]
            d["vchg"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            rows.append(d)
    A=pd.concat(rows)
    A["dm"]=A["r_next"]-A.groupby("coin")["r"].transform("mean")
    def tt(g):
        x=g.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    out["next_wd"]=A.groupby("wd_next")["dm"].apply(tt).unstack()
    out["sat_by_coin"]=A[A.wd_next==5].groupby("coin")["dm"].apply(tt).unstack()
    out["sat_by_year"]=A[A.wd_next==5].groupby("year")["dm"].apply(tt).unstack()
    A["zb"]=pd.cut(A["z"],[-99,-2,-1,0,1,2,99])
    out["after_z"]=A.groupby("zb")["dm"].apply(tt).unstack()
    A["vq"]=A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["by_volq"]=A.groupby("vq")["dm"].apply(tt).unstack()
    A["mb"]=pd.cut(A["ma50"],[-9,-0.2,-0.05,0.05,0.2,9])
    out["by_ma50"]=A.groupby("mb")["dm"].apply(tt).unstack()
    A["vb"]=pd.cut(A["vchg"],[0,0.7,1,1.5,2.5,999])
    out["by_volume_surge"]=A.groupby("vb")["dm"].apply(tt).unstack()
    # weekday x volq for saturday
    out["sat_by_volq"]=A[A.wd_next==5].groupby("vq")["dm"].apply(tt).unstack()
    out["sat_by_fri_ret_sign"]=A[A.wd_next==5].groupby(np.sign(A.loc[A.wd_next==5,"r"]))["dm"].apply(tt).unstack()
    # book
    D=pd.concat([df.assign(coin=c) for c,ws in data["days"].items() for w,df in ws.items()])
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    out["book_by_wd"]=D.groupby("wd")["book_return"].apply(tt).unstack()
    T=pd.concat([df.assign(coin=c) for c,ws in data["trades"].items() for w,df in ws.items()])
    out["trades"]=T.groupby("side")["net_profit_loss_percent"].describe()
    return out
