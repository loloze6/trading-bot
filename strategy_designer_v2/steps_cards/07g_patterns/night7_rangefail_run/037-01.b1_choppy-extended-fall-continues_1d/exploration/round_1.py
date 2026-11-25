def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol20=r.rolling(20).std()
            z=(c/c.shift(5)-1)/(vol20*np.sqrt(5))
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            r1z=r/vol20
            vol30=r.rolling(30).std(); volrel=vol30/vol30.rolling(60,min_periods=30).median()
            f5=c.shift(-5)/c-1; f1=c.shift(-1)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"r20":r20,"r60":r60,"r1z":r1z,
                            "volrel":volrel,"f5":f5,"f1":f1,"wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                            "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),"fc":b["forecast"]})
            rows.append(d)
    A=pd.concat(rows)
    g=A[A.pos%5==0].copy()
    drift=g.groupby("coin")["f5"].mean(); g["u5"]=g["f5"]-g["coin"].map(drift)
    d1=A.groupby("coin")["f1"].mean(); A["u1"]=A["f1"]-A["coin"].map(d1)
    g["trend"]=pd.cut(g.r60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
    g["zb"]=pd.cut(g.z,[-99,-1.5,-0.75,0,0.75,1.5,99])
    def summ(df,col="u5"):
        x=df[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["u5 by trend x z-bin"]=g.dropna(subset=["trend","zb"]).groupby(["trend","zb"],observed=True).apply(summ).round(3)
    g["r20s"]=np.where(g.r20<0,"r20neg","r20pos")
    out["u5 chop by r20 sign x zbin"]=g[g.trend=="chop"].groupby(["r20s","zb"],observed=True).apply(summ).round(3)
    g["vb"]=pd.qcut(g.volrel,3,labels=["lowvol","midvol","hivol"])
    out["u5 by z-bin x vol"]=g.dropna(subset=["vb","zb"]).groupby(["vb","zb"],observed=True).apply(summ).round(3)
    A["r1b"]=pd.cut(A.r1z,[-99,-2,-1,0,1,2,99])
    out["u1 next day by 1d move z"]=A.dropna(subset=["r1b"]).groupby("r1b",observed=True).apply(lambda d: summ(d,"u1")).round(3)
    out["u1 by weekday"]=A.groupby("wd").apply(lambda d: summ(d,"u1")).round(3)
    out["u5 by window"]=g.groupby("w").apply(summ).round(3)
    return out
