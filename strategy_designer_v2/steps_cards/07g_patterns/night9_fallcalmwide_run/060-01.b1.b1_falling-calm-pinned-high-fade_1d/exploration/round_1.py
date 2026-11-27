def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"])})
            d["r"]=r
            d["fwd1"]=c.shift(-1)/c-1
            d["fwd3"]=c.shift(-3)/c-1
            sd=r.rolling(30,min_periods=20).std()
            d["sd30"]=sd
            rng=(b["high"]-b["low"])
            d["width"]=(rng/c)/sd
            d["loc"]=((c-b["low"])/rng.replace(0,np.nan))
            d["ret60"]=c/c.shift(60)-1
            d["rz"]=r/sd.shift(1)
            d["fc"]=b["forecast"]
            d["pos"]=b["postRebalance_current_allocation"]
            d["vol"]=b["volume"]; d["volz"]=b["volume"]/b["volume"].rolling(30,min_periods=20).mean().shift(1)
            d["wkd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["fwd1"].transform("mean")
    D["u1"]=D["fwd1"]-drift
    D["sdm"]=D.groupby("coin")["sd30"].transform("median")
    D["agit"]=D["sd30"]>D["sdm"]
    D["trend"]=np.where(D["ret60"]>0.1,"rising",np.where(D["ret60"]<-0.1,"falling",np.where(D["ret60"].isna(),"na","choppy")))
    def ct(g,col="u1"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan})
        dd=g.groupby("ts")[col].sum(); dev=g[col]
        m=dev.mean(); s=dd-dd.mean()*0
        # clustered se
        se=np.sqrt(((g.groupby("ts")[col].sum()-g.groupby("ts")[col].count()*m)**2).sum())/len(g)
        return pd.Series({"n":len(g),"days":g["ts"].nunique(),"mean%":m*100,"t":m/se if se>0 else np.nan})
    out={}
    X=D.dropna(subset=["width","loc","u1"]).copy()
    X["wq"]=pd.qcut(X["width"],4,labels=["w1","w2","w3","w4"])
    X["lq"]=pd.cut(X["loc"],[-0.01,0.1,0.3,0.7,0.9,1.01],labels=["l0-.1","l.1-.3","l.3-.7","l.7-.9","l.9-1"])
    out["u1 by width q x loc (all)"]=X.groupby(["wq","lq"]).apply(ct).reset_index()
    out["u1 by trend x agit x loc, wide (w4)"]=X[X.wq=="w4"].groupby(["trend","agit","lq"]).apply(ct).reset_index()
    X["rzq"]=pd.cut(X["rz"],[-99,-3,-2,-1,0,1,2,3,99])
    out["u1 by rz (all)"]=X.groupby("rzq").apply(ct).reset_index()
    out["u1 by trend x rz"]=X.groupby(["trend","rzq"]).apply(ct).reset_index()
    out["u1 by weekday"]=X.groupby("wkd").apply(ct).reset_index()
    out["u1 by volz q"]=X.groupby(pd.qcut(X["volz"],5)).apply(ct).reset_index()
    act=X[X["fc"]<0]
    out["active cases by year"]=act.groupby("year").apply(ct).reset_index()
    out["active by coin"]=act.groupby("coin").apply(ct).reset_index()
    return out
