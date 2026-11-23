def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; allr.append((c.shift(-1)/c-1).dropna())
        drift=pd.concat(allr).mean()
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; d=pd.DataFrame()
            d["r0"]=c/c.shift(1)-1
            d["x1"]=c.shift(-1)/c-1-drift
            d["x2"]=c.shift(-2)/c-1-2*drift
            d["x3"]=c.shift(-3)/c-1-3*drift
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            rr=rng/c
            d["rngz"]=rr/rr.shift(1).rolling(20,min_periods=10).mean()
            d["vr"]=b["volume"]/b["volume"].shift(1).rolling(20,min_periods=10).mean()
            d["sd20"]=d["r0"].shift(1).rolling(20,min_periods=10).std()
            d["z0"]=d["r0"]/d["sd20"]
            d["volr"]=d["r0"].rolling(20,min_periods=10).std()/d["r0"].rolling(120,min_periods=40).std()
            d["fc"]=b["forecast"].values
            d["pos"]=np.arange(len(b))
            d["coin"]=coin
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,col="x1",by=None):
        def f(s):
            s=s.dropna(); n=len(s)
            return pd.Series({"n":n,"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
        return df.groupby(by,observed=True)[col].apply(f).unstack()
    out={}
    dn=D[D.r0<0].copy()
    dn["rq3"]=dn.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,3,labels=["rlo","rmid","rhi"]))
    dn["fq3"]=pd.qcut(dn["fc"].rank(method="first"),3,labels=["flo","fmid","fhi"])
    out["down days fc x range"]=g(dn,by=["fq3","rq3"])
    dn["vq"]=dn.groupby("coin")["volr"].transform(lambda s: pd.qcut(s,2,labels=["calm","stressed"]))
    out["down days range x volratio"]=g(dn,by=["vq","rq3"])
    dn["zq"]=pd.cut(dn["z0"],[-99,-1.5,-0.5,0],labels=["big","mid","small"])
    out["down days range x fall size"]=g(dn,by=["zq","rq3"])
    out["down days range 3d grid"]=g(dn[dn.pos%3==0],col="x3",by="rq3")
    up=D[D.r0>0].copy()
    up["rq3"]=up.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,3,labels=["rlo","rmid","rhi"]))
    up["vq3"]=up.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=["vlo","vmid","vhi"]))
    out["up days range x volume"]=g(up,by=["rq3","vq3"])
    hi=dn[dn.rq3=="rhi"]
    out["down hi-range: drift-free total vs excess"]=pd.Series({"excess%":100*hi.x1.mean(),"n":hi.x1.notna().sum()})
    return out
