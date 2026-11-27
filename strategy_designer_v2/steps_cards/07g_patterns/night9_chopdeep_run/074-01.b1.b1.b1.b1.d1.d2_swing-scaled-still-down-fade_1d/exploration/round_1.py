def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r1 = c/c.shift(1)-1
            d = pd.DataFrame({
                "coin":coin,"win":w,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                "nxt":(c.shift(-1)/c-1)-mu,
                "nxt3":(c.shift(-3)/c-1)-3*mu,
                "r1":r1,"r5":c/c.shift(5)-1,"r60":c/c.shift(60)-1,
                "vol20":r1.rolling(20).std(),
                "rng":(h-l)/c, "clv":(c-l)/(h-l).replace(0,np.nan),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "fc":b["forecast"].astype(float),
            })
            d["rngz"]=d["rng"]/d["rng"].shift(1).rolling(20).mean()
            d["z1"]=d["r1"]/d["vol20"]
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["trend"]=np.where(D.r60>0.10,"rising",np.where(D.r60<-0.10,"falling","choppy"))
    D.loc[D.r60.isna(),"trend"]="na"
    def tday(x, day):
        m = x.notna(); x=x[m]; day=day[m]
        n=len(x)
        if n<10: return (n, np.nan, np.nan, 0)
        mean=x.mean(); dev=(x-mean).groupby(day).sum(); Dn=len(dev)
        se=np.sqrt((dev**2).sum()*Dn/(Dn-1))/n
        return (n, mean, mean/se, Dn)
    def tab(df, keys, col="nxt"):
        out=[]
        for k,g in df.groupby(keys):
            n,m,t,dn=tday(g[col], g["day"])
            out.append((k,n,dn,m,t))
        return pd.DataFrame(out,columns=["grp","n","days","mean","t"]).set_index("grp")
    res={}
    D["upday"]=np.where(D.r1>0,"up","down")
    D["r5neg"]=np.where(D.r5<0,"r5neg","r5pos")
    res["nxt by trend x up/down x r5"]=tab(D[D.trend!="na"],["trend","upday","r5neg"])
    # z1 quintiles within trend
    D["z1q"]=pd.qcut(D["z1"],5,labels=False)
    res["nxt by trend x z1 quintile"]=tab(D[D.trend!="na"],["trend","z1q"])
    D["rngq"]=pd.qcut(D["rngz"],3,labels=False)
    res["nxt falling by up/down x range tercile"]=tab(D[D.trend=="falling"],["upday","rngq"])
    D["clvq"]=pd.qcut(D["clv"],3,labels=False)
    res["nxt by trend x close-location tercile"]=tab(D[D.trend!="na"],["trend","clvq"])
    res["nxt by weekday"]=tab(D,["wd"])
    res["nxt falling by weekday"]=tab(D[D.trend=="falling"],["wd"])
    D["volq"]=pd.qcut(D["vol20"],3,labels=False)
    res["nxt by vol tercile x up/down"]=tab(D,["volq","upday"])
    res["nxt3 by trend x up/down"]=tab(D[D.trend!="na"],["trend","upday"],"nxt3")
    res["trend coverage"]=D["trend"].value_counts()
    # book: position side and gain
    D["gain"]=D["alloc"]*(D["nxt"])
    D["held"]=D.alloc.abs()>1e-9
    res["held share by trend"]=D.groupby("trend")["held"].mean()
    return res
