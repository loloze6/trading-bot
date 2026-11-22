def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std()
            d=pd.DataFrame({"coin":coin,"win":w,"r":r,"z":r/vol,"vol":vol,
                            "fall":(b["regime"]=="mean_reversion").values,
                            "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1,
                            "r5":c/c.shift(5)-1,
                            "pos":np.arange(len(b)),
                            "ts":pd.to_datetime(b["timestamp"]),
                            "alloc":b["postRebalance_current_allocation"].astype(float),
                            "bv":b["postRebalance_total_value"].astype(float)})
            d["bret"]=d["bv"].shift(-1)/d["bv"]-1
            d["z5"]=d["r5"]/(vol*np.sqrt(5))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu={h:D.groupby("coin")[h].mean() for h in ["f1","f3","f5"]}
    for h in ["f1","f3","f5"]:
        D["x"+h]=D[h]-D["coin"].map(mu[h])
        sd=D.groupby("coin")[h].std()
        D["s"+h]=D["x"+h]/D["coin"].map(sd)
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    D["z5b"]=pd.cut(D["z5"],[-99,-1.5,-0.5,0.5,1.5,99])
    def tab(df,g,h,step):
        df=df[df["pos"]%step==0].dropna(subset=[h])
        a=df.groupby(g,observed=True)[h].agg(["mean","std","count"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.drop(columns="std").round(4)
    out={}
    out["f1 strength by z x fall"]=tab(D,["fall","zb"],"sf1",1)
    out["f3 strength by z x fall"]=tab(D,["fall","zb"],"sf3",3)
    out["f5 strength by z5(5d) x fall"]=tab(D,["fall","z5b"],"sf5",5)
    out["f1 strength by weekday"]=tab(D.assign(wd=D.ts.dt.dayofweek),"wd","sf1",1)
    D["vq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["f1 strength by vol tercile x fall"]=tab(D,["fall","vq"],"sf1",1)
    out["f1 z>1 falling by coin"]=tab(D[(D.z>1)&D.fall],"coin","sf1",1)
    out["f1 z>1 not falling by coin"]=tab(D[(D.z>1)&~D.fall],"coin","sf1",1)
    # book
    act=D[D.alloc.abs()>1e-6]
    out["book bar ret when positioned"]=pd.Series({"n":len(act),"mean":act.bret.mean(),"t":act.bret.mean()/(act.bret.std()/np.sqrt(len(act))),"mean_alloc":act.alloc.mean(),"mean f1 raw":act.f1.mean()})
    out["share bars short"]=float((D.alloc<-1e-6).mean())
    return out
