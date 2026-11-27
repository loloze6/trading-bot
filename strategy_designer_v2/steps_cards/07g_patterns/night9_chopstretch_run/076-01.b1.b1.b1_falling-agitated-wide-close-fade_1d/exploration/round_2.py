def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            rng=b.high-b.low
            mr=rng.rolling(20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b.timestamp)})
            d["day"]=d.ts.dt.floor("D")
            d["prod"]=(b.close-(b.high+b.low)/2)/mr
            d["wid"]=rng/mr
            d["loc"]=(b.close-b.low)/rng.replace(0,np.nan)
            d["tr60"]=b.close/b.close.shift(60)-1
            d["vr"]=b.volume/b.volume.rolling(20).mean()
            d["nxt"]=b.close.shift(-1)/b.close-1
            d["nxt2"]=b.close.shift(-2)/b.close-1
            d["inprof"]=(b.regime!="chop")
            rows.append(d)
    D=pd.concat(rows)
    for h in ["nxt","nxt2"]:
        dr=D.groupby("coin")[h].mean()
        D["ab_"+h]=D[h]-D.coin.map(dr)
    D=D.dropna(subset=["prod","ab_nxt"])
    def ct(df,col="ab_nxt"):
        df=df.dropna(subset=[col])
        if len(df)<5: return pd.Series({"mean%":np.nan,"n":len(df),"days":0,"t_day":np.nan})
        s=df.groupby("day")[col].apply(lambda x:(x-df[col].mean()).sum())
        se=np.sqrt((s**2).sum())/len(df)
        return pd.Series({"mean%":df[col].mean()*100,"n":len(df),"days":df.day.nunique(),"t_day":df[col].mean()/se})
    D["trend"]=np.where(D.tr60.isna(),"na",np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling","choppy")))
    D["seg"]=np.where(D.inprof,"falling_agit",D.trend)
    hi=D[(D.wid>1)&(D["loc"]>0.5)].copy()
    hi["pq"]=hi.groupby("seg")["prod"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out={}
    out["wide high close, by seg x prod tercile, next day"]=hi.groupby(["seg","pq"]).apply(ct).round(3)
    out["wide high close, by seg, 2 days"]=hi.groupby("seg").apply(lambda g: ct(g,"ab_nxt2")).round(3)
    D["wq"]=pd.qcut(D.wid,3,labels=False)
    D["lb"]=pd.cut(D["loc"],[0,.5,.75,1.0001],include_lowest=True,labels=["low","mid-high","top"])
    out["inprof wid tercile x loc band"]=D[D.inprof].groupby(["wq","lb"]).apply(ct).round(3)
    D["vq"]=pd.qcut(D.vr,3,labels=False,duplicates="drop")
    out["inprof wide high close by volume tercile"]=D[D.inprof&(D.wid>1)&(D["loc"]>0.5)].groupby("vq").apply(ct).round(3)
    D["wd"]=D.ts.dt.weekday
    D["yr"]=D.ts.dt.year
    out["weekday day-clustered"]=D.groupby("wd").apply(ct).round(3)
    out["wed by year"]=D[D.wd==2].groupby("yr").apply(ct).round(3)
    out["inprof top-prod decile by year"]=D[D.inprof&(D["prod"]>D["prod"].quantile(0.8))].groupby("yr").apply(ct).round(3)
    return out
