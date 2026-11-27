def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame({"coin":c,"w":w})
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["r0"]=cl/cl.shift(1)-1
            d["r1"]=cl.shift(-1)/cl-1
            d["vr"]=v/v.shift(1).rolling(20).mean()
            d["rng"]=(b["high"]-b["low"])/cl
            d["clpos"]=(cl-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d["r60"]=cl/cl.shift(60)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["r5"]=cl/cl.shift(5)-1
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["gain"]=d["alloc"]*d["r1"]
            d["fc"]=b["forecast"].astype(float)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["r0","r1"])
    mu=D.groupby("coin")["r1"].mean()
    D["ex"]=D["r1"]-D["coin"].map(mu)
    D["z0"]=D["r0"]/D["vol20"]
    D["lvr"]=np.log(D["vr"])
    D["year"]=D["ts"].dt.year; D["wd"]=D["ts"].dt.weekday
    D["day"]=D["ts"].dt.floor("D")
    def tstat(x):
        x=x.dropna(); 
        return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def dayt(df,col="ex"):
        g=df.groupby("day")[col].mean()
        return tstat(g)
    out={}
    E=D.dropna(subset=["vr"]).copy()
    E["dn"]=np.where(E["r0"]<0,"down","up")
    E["vq"]=E.groupby("dn")["lvr"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["ex by dir x vol quintile (day-pooled)"]=E.groupby(["dn","vq"]).apply(lambda g: dayt(g)).reset_index()
    # size of down move quintile x vol
    Dn=E[E.r0<0].copy()
    Dn["zq"]=pd.qcut(Dn["z0"],4,labels=False)
    Dn["vq3"]=pd.qcut(Dn["lvr"],3,labels=False)
    out["down: z-move quartile x vol tercile mean ex%"]=Dn.groupby(["zq","vq3"])["ex"].mean().unstack()*100
    out["down: z-move quartile x vol tercile n"]=Dn.groupby(["zq","vq3"])["ex"].size().unstack()
    # close position on down days
    Dn["cq"]=pd.qcut(Dn["clpos"],3,labels=False,duplicates="drop")
    out["down: closepos tercile x vol tercile ex%"]=Dn.groupby(["cq","vq3"])["ex"].mean().unstack()*100
    # trend regime
    E["tr"]=pd.cut(E["r60"],[-np.inf,-0.1,0.1,np.inf],labels=["fall","chop","rise"])
    out["by trend x dir x vol tercile ex% "]=E.assign(vq3=E.groupby("dn")["lvr"].transform(lambda s: pd.qcut(s,3,labels=False))).groupby(["tr","dn","vq3"]).apply(lambda g: dayt(g)).reset_index()
    # all-day graded slope by volume
    E["vlq"]=pd.qcut(E["vol20"],3,labels=False)
    out["by vol level x dir: corr lvr,ex"]=E.groupby(["vlq","dn"]).apply(lambda g: pd.Series({"n":len(g),"corr":g["lvr"].corr(g["ex"]),"t":g["lvr"].corr(g["ex"])*np.sqrt(len(g))})).reset_index()
    # weekday
    out["weekday all ex"]=E.groupby("wd").apply(lambda g: dayt(g))
    # after large moves both sides
    E["zb"]=pd.cut(E["z0"],[-np.inf,-2,-1,0,1,2,np.inf])
    out["z0 bucket ex"]=E.groupby("zb").apply(lambda g: dayt(g))
    # 5-day return quintile
    E["r5q"]=pd.qcut(E["r5"],5,labels=False)
    out["r5 quintile ex"]=E.groupby("r5q").apply(lambda g: dayt(g))
    # book gain by year/window
    out["book gain by window"]=D.groupby("w")["gain"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*100)
    return out
