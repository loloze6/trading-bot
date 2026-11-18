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
            r5p=c/c.shift(5)-1
            r20p=c/c.shift(20)-1
            fwd=c.shift(-5)/c-1
            rng=np.log(b["high"]/b["low"])
            clv=(c-b["low"])/(b["high"]-b["low"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"r5p":r5p,"r20p":r20p,"fwd":fwd,"sd":sd,
                            "clv":clv,"wd":pd.to_datetime(b["timestamp"]).dt.weekday,"fc":b["forecast"],
                            "pos":b["postRebalance_current_allocation"]})
            d=d.iloc[::5]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    E=D.dropna(subset=["z","vr"]).copy()
    E["zq"]=pd.qcut(E["z"],5,labels=False)
    E["vq"]=pd.qcut(E["vr"],3,labels=False)
    out["by z quintile x vol tercile"]=E.groupby(["zq","vq"]).apply(summ)
    out["by z quintile"]=E.groupby("zq").apply(summ)
    for col in ["r5p","r20p","sd","clv"]:
        F=D.dropna(subset=[col]).copy(); F["q"]=pd.qcut(F[col],5,labels=False)
        out["by "+col+" quintile"]=F.groupby("q").apply(summ)
    out["by weekday"]=D.groupby("wd").apply(summ)
    out["by coin"]=D.groupby("coin").apply(summ)
    # rank corr
    res={}
    for col in ["z","vr","r5p","r20p","sd","clv"]:
        F=D.dropna(subset=[col,"ex"])
        rho,p=stats.spearmanr(F[col],F["ex"]); res[col]=(rho,p,len(F))
    out["spearman vs ex"]=pd.DataFrame(res,index=["rho","p","n"]).T
    return out
