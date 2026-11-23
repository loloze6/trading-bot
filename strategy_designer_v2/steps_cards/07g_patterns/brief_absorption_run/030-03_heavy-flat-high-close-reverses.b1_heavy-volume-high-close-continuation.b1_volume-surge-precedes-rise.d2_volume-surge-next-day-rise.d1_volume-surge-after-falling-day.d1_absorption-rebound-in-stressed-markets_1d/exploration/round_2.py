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
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(c-b["low"])/rng
            d["vr"]=b["volume"]/b["volume"].shift(1).rolling(20,min_periods=10).mean()
            d["sd20"]=d["r0"].shift(1).rolling(20,min_periods=10).std()
            d["z0"]=d["r0"]/d["sd20"]
            rr=rng/c
            d["rngz"]=rr/rr.shift(1).rolling(20,min_periods=10).mean()
            d["rngsd"]=rr/d["sd20"]
            d["lw"]=(np.minimum(b["open"],c)-b["low"])/rng
            d["fc"]=b["forecast"].values
            d["pos"]=np.arange(len(b))
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,col="x1",by=None):
        def f(s):
            s=s.dropna(); n=len(s)
            return pd.Series({"n":n,"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
        return df.groupby(by,observed=True)[col].apply(f).unstack()
    out={}
    D["rq"]=D.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,3,labels=["rlo","rmid","rhi"]))
    D["vrq"]=D.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=["vlo","vmid","vhi"]))
    D["zb"]=pd.cut(D["z0"],[-99,-1,-0.3,0.3,1,99],labels=["z<-1","-1..-.3","flat","+.3..1","z>1"])
    out["range x day-return bin"]=g(D,by=["zb","rq"])
    dn=D[D.r0<0]
    out["down days: range x volume"]=g(dn,by=["rq","vrq"])
    out["down days high range: by year"]=g(dn[dn.rq=="rhi"],by="year")
    out["down days high range: by coin"]=g(dn[dn.rq=="rhi"],by="coin")
    dn2=dn.copy(); dn2["rq5"]=dn2.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["down days: range quintile, 1d and 2d(grid)"]=pd.concat([g(dn2,by="rq5"),g(dn2[dn2.pos%2==0],col="x2",by="rq5").add_prefix("2d_")],axis=1)
    # regression on down days with fc>0 : x1 on z0, log vr, log rngz
    s=dn.dropna(subset=["x1","z0","vr","rngz","clv"]).copy()
    X=np.column_stack([np.ones(len(s)),s.z0,np.log(s.vr),np.log(s.rngz),s.clv])
    beta,res,_,_=np.linalg.lstsq(X,s.x1.values,rcond=None)
    e=s.x1.values-X@beta; s2=(e@e)/(len(s)-X.shape[1]); cov=s2*np.linalg.inv(X.T@X)
    out["down days OLS x1 ~ z0+logvr+logrng+clv"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z0","logvr","logrng","clv"])
    up=D[D.r0>0].dropna(subset=["x1","z0","vr","rngz","clv"])
    X=np.column_stack([np.ones(len(up)),up.z0,np.log(up.vr),np.log(up.rngz),up.clv])
    beta,_,_,_=np.linalg.lstsq(X,up.x1.values,rcond=None)
    e=up.x1.values-X@beta; s2=(e@e)/(len(up)-5); cov=s2*np.linalg.inv(X.T@X)
    out["up days OLS"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z0","logvr","logrng","clv"])
    D["lwq"]=pd.cut(D["lw"],[-.01,.15,.35,1.01],labels=["lw_small","lw_mid","lw_big"])
    out["down days: lower wick share"]=g(D[D.r0<0],by="lwq")
    return out
