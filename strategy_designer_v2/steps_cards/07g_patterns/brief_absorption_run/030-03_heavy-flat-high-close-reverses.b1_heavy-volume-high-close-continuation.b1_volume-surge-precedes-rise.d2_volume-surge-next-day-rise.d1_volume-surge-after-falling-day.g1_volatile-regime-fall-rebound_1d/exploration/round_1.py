def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            s20=r.rolling(20).std()
            d=pd.DataFrame({"coin":c,"win":w,"r":r,"z":r/s20,
                "vr":s20/s20.rolling(120,min_periods=60).mean(),
                "clv":(cl-b["low"])/(b["high"]-b["low"]),
                "volr":b["volume"]/b["volume"].rolling(20).mean(),
                "rng":(b["high"]-b["low"])/cl/s20,
                "r5":cl/cl.shift(5)-1,
                "fwd1":cl.shift(-1)/cl-1,"fwd3":cl.shift(-3)/cl-1,
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows)
    mu=D.groupby("coin")["fwd1"].transform("mean")
    D["x1"]=D["fwd1"]-mu
    def summ(g,col="x1"):
        v=g[col].dropna(); 
        return pd.Series({"n":len(v),"mean%":100*v.mean(),"t":v.mean()/v.std()*np.sqrt(len(v)) if len(v)>2 else np.nan})
    out={}
    F=D[D.r<0].copy()
    F["clvq"]=pd.qcut(F.clv,3,labels=["low","mid","high"])
    F["zq"]=pd.qcut(F.z,3,labels=["deep","mid","shallow"])
    F["volq"]=pd.qcut(F.volr,3,labels=["lowvol","midvol","highvol"])
    out["fall: z x clv"]=F.groupby(["zq","clvq"]).apply(summ)
    out["fall: volume x clv"]=F.groupby(["volq","clvq"]).apply(summ)
    A=D.copy(); A["clvq"]=pd.qcut(A.clv,5,labels=False)
    A["volq"]=pd.qcut(A.volr,3,labels=False)
    out["all days clv quintile x volume"]=A.groupby(["volq","clvq"]).apply(summ)
    U=D[D.r>0].copy(); U["zq"]=pd.qcut(U.z,3,labels=["small","mid","big"])
    out["up days by size"]=U.groupby("zq").apply(summ)
    out["by weekday all"]=D.groupby("wd").apply(summ)
    out["fall by year"]=F[F.z<F.z.quantile(1/3)].groupby("yr").apply(summ)
    # book
    dl=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=c; dd["win"]=w; dl.append(dd)
    Dy=pd.concat(dl)
    bk=Dy.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book days: corr with coin"]=float(bk.corr().iloc[0,1])
    q=bk.book_return.quantile([0.02,0.98])
    out["worst2% days: coin ret mean%"]=100*bk[bk.book_return<=q.iloc[0]].coin_return.mean()
    out["best2% days: coin ret mean%"]=100*bk[bk.book_return>=q.iloc[1]].coin_return.mean()
    return out
