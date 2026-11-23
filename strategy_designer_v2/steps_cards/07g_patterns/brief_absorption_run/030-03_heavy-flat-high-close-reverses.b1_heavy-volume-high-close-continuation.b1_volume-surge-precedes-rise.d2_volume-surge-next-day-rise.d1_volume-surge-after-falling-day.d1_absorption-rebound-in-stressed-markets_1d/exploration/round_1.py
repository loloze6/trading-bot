def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            allr.append((c.shift(-1)/c-1).dropna())
        drift=pd.concat(allr).mean()
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; d=pd.DataFrame()
            d["r0"]=c/c.shift(1)-1
            d["r1"]=c.shift(-1)/c-1
            d["x1"]=d["r1"]-drift
            d["r3"]=c.shift(-3)/c-1-3*drift
            d["r5"]=c.shift(-5)/c-1-5*drift
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(c-b["low"])/rng
            d["vr"]=b["volume"]/b["volume"].shift(1).rolling(20,min_periods=10).mean()
            d["sd20"]=d["r0"].shift(1).rolling(20,min_periods=10).std()
            d["z0"]=d["r0"]/d["sd20"]
            d["rngz"]=(rng/c)/(rng/c).shift(1).rolling(20,min_periods=10).mean()
            d["fc"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["pos"]=np.arange(len(b))
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year
            d["coin"]=coin; d["win"]=w
            d["gain"]=d["alloc"]*d["r1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,col="x1",by=None):
        def f(s):
            s=s.dropna(); n=len(s)
            return pd.Series({"n":n,"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
        return df.groupby(by,observed=True)[col].apply(f).unstack()
    out={}
    D["vrq"]=D.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=["vlo","vmid","vhi"]))
    D["clvq"]=pd.cut(D["clv"],[-.01,1/3,2/3,1.01],labels=["clow","cmid","chigh"])
    D["flat"]=D["z0"].abs()<0.5
    out["flat days: next-day excess by volume x close location"]=g(D[D.flat],by=["vrq","clvq"])
    out["all days: by volume x close location"]=g(D,by=["vrq","clvq"])
    D["zq"]=pd.cut(D["z0"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["next-day by day return in sd units"]=g(D,by="zq")
    out["next-day by day return sd units, high volume only"]=g(D[D.vrq=="vhi"],by="zq")
    out["3-day (grid) by day return sd units"]=g(D[D.pos%3==0],col="r3",by="zq")
    out["down days: next-day by close location"]=g(D[D.r0<0],by="clvq")
    D["rq"]=D.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,3,labels=["rlo","rmid","rhi"]))
    out["down days: by range expansion"]=g(D[D.r0<0],by="rq")
    out["by weekday"]=g(D,by="wd")
    out["fc>0 by year"]=g(D[D.fc>0],by="year")
    out["fc>0 by coin"]=g(D[D.fc>0],by="coin")
    gn=D.dropna(subset=["gain"])
    q=gn["gain"].quantile([0.02,0.98])
    worst=gn[gn.gain<=q.iloc[0]]; best=gn[gn.gain>=q.iloc[1]]
    out["worst/best 2% position-bars: profile"]=pd.DataFrame({
        "worst":[len(worst),worst.z0.mean(),worst.vr.mean(),worst.clv.mean(),worst.rngz.mean(),worst.fc.mean()],
        "best":[len(best),best.z0.mean(),best.vr.mean(),best.clv.mean(),best.rngz.mean(),best.fc.mean()],
        "all held":[len(gn[gn.alloc!=0]),gn[gn.alloc!=0].z0.mean(),gn[gn.alloc!=0].vr.mean(),gn[gn.alloc!=0].clv.mean(),gn[gn.alloc!=0].rngz.mean(),gn[gn.alloc!=0].fc.mean()]},
        index=["n","z0","vr","clv","rngz","fc"])
    return out
