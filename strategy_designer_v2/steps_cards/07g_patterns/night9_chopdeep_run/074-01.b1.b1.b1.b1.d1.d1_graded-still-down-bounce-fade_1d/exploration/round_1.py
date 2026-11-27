def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            df["r1"]=c.pct_change(); df["r5"]=c/c.shift(5)-1
            df["tr60"]=c/c.shift(60)-1
            df["width"]=rng/rng.rolling(20).mean()
            df["clv"]=((c-b["low"])/(b["high"]-b["low"])).replace([np.inf,-np.inf],np.nan)
            df["n1"]=c.shift(-1)/c-1
            df["n2_5"]=c.shift(-5)/c.shift(-1)-1
            df["vol30"]=df["r1"].rolling(30).std()
            df["alloc"]=b["postRebalance_current_allocation"]
            df["fc"]=b["forecast"]
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["n1"].mean()
    D["a1"]=D["n1"]-D["coin"].map(drift)
    D["vrank"]=D.groupby("coin")["vol30"].rank(pct=True)
    D["trend"]=np.where(D.tr60<-0.10,"falling",np.where(D.tr60>0.10,"rising",np.where(D.tr60.notna(),"choppy","na")))
    D["day"]=np.where(D.r1>0,"up","down")
    D["wq"]=D.groupby("coin")["width"].transform(lambda x: pd.qcut(x,3,labels=["narrow","mid","wide"]))
    D["wd"]=D.ts.dt.dayofweek
    D["agit"]=np.where(D.vrank>0.5,"agit","calm")
    def stat(g,col="a1"):
        g=g.dropna(subset=[col])
        n=len(g)
        if n<20: return pd.Series({"n":n,"mean%":np.nan,"t":np.nan,"days":0})
        m=g[col].mean(); s=g.groupby("ts")[col].apply(lambda x:(x-m).sum())
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"mean%":100*m,"t":m/se,"days":g.ts.nunique()})
    E=D[D.trend!="na"]
    out={}
    out["trend_day_width"]=E.groupby(["trend","day","wq"]).apply(stat)
    out["falling_up_r5sign_width"]=E[(E.trend=="falling")&(E.day=="up")].assign(r5s=lambda x:np.where(x.r5<0,"r5neg","r5pos")).groupby(["r5s","wq"]).apply(stat)
    out["trend_agit_down_wide"]=E[(E.day=="down")].groupby(["trend","agit","wq"]).apply(stat)
    out["falling_up_clv"]=E[(E.trend=="falling")&(E.day=="up")].assign(cq=lambda x:pd.qcut(x.clv,3,labels=["lowclose","mid","highclose"])).groupby("cq").apply(stat)
    out["weekday_all"]=D.groupby("wd").apply(stat)
    bk=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            bk.append(d.assign(coin=coin,w=w))
    B=pd.concat(bk); B["day"]=pd.to_datetime(B["day"])
    bd=B.groupby("day")["book_return"].mean().dropna()
    out["book_by_year"]=bd.groupby(bd.index.year).agg(["count","mean","std"]).assign(sh=lambda x:x["mean"]/x["std"]*np.sqrt(365))
    out["book_by_weekday"]=bd.groupby(bd.index.dayofweek).agg(["count","mean"])
    return out
