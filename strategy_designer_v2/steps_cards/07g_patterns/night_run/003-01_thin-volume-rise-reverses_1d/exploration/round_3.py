def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(20,min_periods=10).std()
            z=r1/sd
            vr=np.log(v/v.shift(1).rolling(30,min_periods=15).mean())
            fwd=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"fwd":fwd,"yr":ts.dt.year,"wd":ts.dt.weekday})
            rows.append(d.iloc[::5])
    D=pd.concat(rows).dropna(subset=["fwd"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D=D.dropna(subset=["z","vr"])
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    up=D[D.z>0].copy()
    up["zv"]=up["z"]*(1+up["vr"].clip(-1,2))
    up["zvq"]=pd.qcut(up["zv"],5,labels=False)
    out["up days z x (1+vr) quintile"]=up.groupby("zvq").apply(summ)
    big=up[up.z>up.z.quantile(0.5)].copy()
    big["vq"]=pd.qcut(big["vr"],3,labels=False)
    out["larger up half by vr tercile"]=big.groupby("vq").apply(summ)
    D["half"]=np.where(D.yr<=2021,"2018-2021","2022-2025")
    D["zq"]=pd.qcut(D["z"],5,labels=False)
    out["top z quintile by half"]=D[D.zq==4].groupby("half").apply(summ)
    out["weekday by half"]=D.groupby(["half","wd"]).apply(summ)
    D["vq"]=pd.qcut(D["vr"],5,labels=False)
    out["vr quintile by half"]=D.groupby(["half","vq"]).apply(summ)
    # book's worst/best days
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(t.assign(coin=coin))
    B=pd.concat(dd).dropna(subset=["book_return"])
    out["book daily by coin"]=B.groupby("coin")["book_return"].agg(["count","mean","std"])
    return out
