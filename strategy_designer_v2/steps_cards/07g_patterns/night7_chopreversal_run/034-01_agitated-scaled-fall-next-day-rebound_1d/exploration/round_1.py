def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r":r,"z":r/sd,"sd":sd,
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"n3":c.shift(-3)/c-1,
                "z3":(c/c.shift(3)-1)/(sd*np.sqrt(3)),
                "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "rng":(b["high"]-b["low"])/c.shift(1)/sd,
                "ag":(b["regime"]!="chop").astype(int),
                "fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["n1"].transform("mean")
    D["x1"]=D["n1"]-mu
    D["x2"]=D["n2"]-D.groupby("coin")["n2"].transform("mean")
    D=D.dropna(subset=["z","x1"])
    D["wd"]=D["ts"].dt.weekday
    D["zb"]=pd.cut(D["z"],[-99,-2.5,-1.5,-1,-0.5,0,0.5,1,1.5,2.5,99])
    def agg(g,col="x1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["next-day excess by z bin x agitated"]=D.groupby(["ag","zb"],observed=True).apply(agg).round(3)
    out["2-day excess by z bin x agitated"]=D.groupby(["ag","zb"],observed=True).apply(lambda g:agg(g,"x2")).round(3)
    dn=D[D.z<-1]
    dn=dn.assign(clvb=pd.cut(dn.clv,[0,0.25,0.5,0.75,1.0001],include_lowest=True))
    out["falls z<-1: next by close location"]=dn.groupby(["ag","clvb"],observed=True).apply(agg).round(3)
    up=D[D.z>1].assign(clvb=lambda x:pd.cut(x.clv,[0,0.25,0.5,0.75,1.0001],include_lowest=True))
    out["rises z>1: next by close location"]=up.groupby(["ag","clvb"],observed=True).apply(agg).round(3)
    D["z3b"]=pd.cut(D["z3"],[-99,-2,-1,0,1,2,99])
    out["next-day by 3-day scaled move x ag"]=D.groupby(["ag","z3b"],observed=True).apply(agg).round(3)
    out["all bars next-day by weekday"]=D.groupby("wd").apply(agg).round(3)
    out["falls z<-1 next by weekday"]=dn.groupby("wd").apply(agg).round(3)
    D["rb"]=pd.qcut(D["rng"],5,duplicates="drop")
    out["next-day by range/sd quintile x ag"]=D.groupby(["ag","rb"],observed=True).apply(agg).round(3)
    out["by coin, falls z<-1 ag"]=dn[dn.ag==1].groupby("coin").apply(agg).round(3)
    out["by window, falls z<-1 ag"]=dn[dn.ag==1].groupby("w").apply(agg).round(3)
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().dropna()
    out["book daily: n, mean%, worst%, best%"]=pd.Series({"n":len(bk),"mean%":100*bk.mean(),"q01%":100*bk.quantile(.01),"q99%":100*bk.quantile(.99)}).round(3)
    out["book mean by window %"]=(100*bk.groupby(level=0).mean()).round(3)
    return out
