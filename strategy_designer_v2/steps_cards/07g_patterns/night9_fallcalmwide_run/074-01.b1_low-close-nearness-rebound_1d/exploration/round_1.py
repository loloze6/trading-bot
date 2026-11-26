def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            rw=rng/sd
            cl=(b["high"]-c)/(b["high"]-b["low"]).replace(0,np.nan)
            ret60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"win":w,"rw":rw,"cl":cl,"r0":r,"ret60":ret60,
                "inprof":b["regime"]!="chop","regime":b["regime"],
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"pos":b["postRebalance_current_allocation"]})
            df["i"]=np.arange(len(df))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["f1"].mean()
    d["u1"]=d["f1"]-d["coin"].map(drift)
    def summ(g,col="u1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    d["wide"]=pd.cut(d["rw"],[0,1,1.5,2,3,100])
    d["clq"]=pd.cut(d["cl"],[-.01,.25,.5,.75,1.01])
    d["trend"]=pd.cut(d["ret60"],[-10,-.1,.1,100],labels=["fall","chop","rise"])
    out["wide x closeloc, all"]=d.groupby(["wide","clq"],observed=True).apply(summ).unstack()
    out["wide>=2 by clq x inprof"]=d[d.rw>=2].groupby(["inprof","clq"],observed=True).apply(summ)
    out["wide>=2 by clq x trend60"]=d[d.rw>=2].groupby(["trend","clq"],observed=True).apply(summ)
    out["weekday"]=d.groupby("wd").apply(summ)
    out["weekday inprof"]=d[d.inprof].groupby("wd").apply(summ)
    d["r0q"]=pd.qcut(d["r0"]/d["rw"].pipe(lambda s: (d["rng_dummy"] if False else 1)),10,labels=False) if False else pd.qcut(d["r0"],10,labels=False)
    out["r0 decile -> u1 by inprof"]=d.groupby(["inprof","r0q"]).apply(summ)["mean"].unstack(0)
    out["r0 decile t by inprof"]=d.groupby(["inprof","r0q"]).apply(summ)["t"].unstack(0)
    out["share inprof, regimes"]=d["regime"].value_counts()
    return out
