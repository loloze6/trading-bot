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
            fwd2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"fwd":fwd,"fwd2":fwd2,"yr":ts.dt.year,
                            "pos":b["postRebalance_current_allocation"]})
            rows.append(d.iloc[::5])
    D=pd.concat(rows).dropna(subset=["fwd"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D=D.dropna(subset=["z","vr"])
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    up=D[D.z>0].copy(); dn=D[D.z<=0].copy()
    def sp(F,col):
        r,p=stats.spearmanr(F[col],F["ex"]); return pd.Series({"rho":r,"p":p,"n":len(F)})
    up["zv"]=up["z"]*np.exp(up["vr"])
    out["spearman up days"]=pd.DataFrame({k:sp(up,k) for k in ["z","vr","zv"]}).T
    out["spearman down days"]=pd.DataFrame({k:sp(dn,k) for k in ["z","vr"]}).T
    up["zq"]=pd.qcut(up["z"],4,labels=False)
    out["up days z quartile"]=up.groupby("zq").apply(summ)
    up["vq"]=pd.qcut(up["vr"],4,labels=False)
    out["up days vr quartile"]=up.groupby("vq").apply(summ)
    top=up[(up.zq==3)]
    out["top up quartile by coin"]=top.groupby("coin").apply(summ)
    out["top up quartile by year"]=top.groupby("yr").apply(summ)
    tv=top[top.vr>0]
    out["top up & heavy vol by coin"]=tv.groupby("coin").apply(summ)
    D["vq"]=pd.qcut(D["vr"],5,labels=False)
    out["all days vr quintile"]=D.groupby("vq").apply(summ)
    out["vr spearman by coin"]=D.groupby("coin").apply(lambda g: sp(g,"vr"))
    out["vr spearman by year"]=D.groupby("yr").apply(lambda g: sp(g,"vr"))
    # book exposure
    out["book: mean pos when active vs z quart (up)"]=up.groupby("zq")["pos"].mean()
    return out
