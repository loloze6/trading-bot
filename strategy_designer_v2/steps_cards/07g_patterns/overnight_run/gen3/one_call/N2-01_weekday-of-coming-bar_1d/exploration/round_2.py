def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["r"]=d["close"].pct_change()
            d["r_next"]=d["r"].shift(-1)
            d["wd_next"]=d["ts"].shift(-1).dt.dayofweek
            d["vol20"]=d["r"].rolling(20).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["vchg"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            d["ma50"]=d["close"]/d["close"].rolling(50).mean()-1
            d["clv"]=(d["close"]-d["low"])/(d["high"]-d["low"])
            d["coin"]=coin; d["w"]=w; d["year"]=d["ts"].dt.year
            rows.append(d)
    A=pd.concat(rows)
    A["dm"]=A["r_next"]-A.groupby("coin")["r"].transform("mean")
    def tt(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    dn=A[A.z<=-1]
    out["dn_by_coin"]=dn.groupby("coin")["dm"].apply(tt).unstack()
    out["dn_by_year"]=dn.groupby("year")["dm"].apply(tt).unstack()
    A["vs"]=A.vchg>1.5
    out["dn_x_volsurge"]=A[A.z<=-1].groupby("vs")["dm"].apply(tt).unstack()
    out["volsurge_by_zsign"]=A[A.vs].groupby(np.sign(A.loc[A.vs,"r"]))["dm"].apply(tt).unstack()
    out["volsurge_by_coin"]=A[A.vchg.between(1.5,2.5)].groupby("coin")["dm"].apply(tt).unstack()
    out["volsurge_by_year"]=A[A.vchg.between(1.5,2.5)].groupby("year")["dm"].apply(tt).unstack()
    out["up_small_by_coin"]=A[A.z.between(0,1)].groupby("coin")["dm"].apply(tt).unstack()
    A["cb"]=pd.cut(A["clv"],[-0.01,0.2,0.4,0.6,0.8,1.01])
    out["by_close_location"]=A.groupby("cb")["dm"].apply(tt).unstack()
    out["dn_by_close_location"]=A[A.z<=-1].groupby("cb")["dm"].apply(tt).unstack()
    out["thu_by_coin"]=A[A.wd_next==3].groupby("coin")["dm"].apply(tt).unstack()
    out["tue_by_coin"]=A[A.wd_next==1].groupby("coin")["dm"].apply(tt).unstack()
    out["thu_by_year"]=A[A.wd_next==3].groupby("year")["dm"].apply(tt).unstack()
    out["dn_x_sat"]=A[A.z<=-1].groupby(A.loc[A.z<=-1,"wd_next"]==5)["dm"].apply(tt).unstack()
    return out
