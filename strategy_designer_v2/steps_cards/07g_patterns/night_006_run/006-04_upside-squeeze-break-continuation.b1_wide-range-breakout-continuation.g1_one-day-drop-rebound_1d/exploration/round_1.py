def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r1=c.pct_change(); fwd=c.shift(-1)/c-1
            sd=r1.rolling(60,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            rngz=rng.rolling(5).mean()/rng.rolling(60,min_periods=20).mean()
            volz=b["volume"].rolling(5).mean()/b["volume"].rolling(60,min_periods=20).mean()
            r5=c/c.shift(5)-1
            vlev=sd/ r1.rolling(60,min_periods=20).std().expanding().median()
            df=pd.DataFrame({"coin":coin,"w":w,"z":r1/sd,"r1":r1,"fwd":fwd,"absfwd":fwd.abs()/sd,
                "rngz":rngz,"volz":volz,"z5":r5/(sd*np.sqrt(5)),"sd":sd,
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"yr":pd.to_datetime(b["timestamp"]).dt.year,
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["fwd","z"])
    mu=d.groupby("coin")["fwd"].mean()
    d["ex"]=d["fwd"]-d["coin"].map(mu)
    def g(col,q=5):
        x=d.dropna(subset=[col]).copy()
        x["b"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        o=x.groupby("b")["ex"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        o["absfwd"]=x.groupby("b")["absfwd"].mean()
        return o.drop(columns="std")
    out={}
    out["by z1 decile"]=g("z",10)
    out["by z5 quint"]=g("z5")
    out["by range compression quint"]=g("rngz")
    out["by volume ratio quint"]=g("volz")
    out["by vol level quint"]=g("sd")
    wd=d.groupby("wd")["ex"].agg(["mean","count","std"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday"]=wd.drop(columns="std")
    # slope of ex on clipped -z by coin and by year
    def sl(x):
        x=x[x["z"]<0]
        if len(x)<30: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(x)})
        r=stats.linregress(-x["z"],x["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(x)})
    out["fall slope by coin"]=d.groupby("coin").apply(sl)
    out["fall slope by year"]=d.groupby("yr").apply(sl)
    def slu(x):
        x=x[x["z"]>0]
        r=stats.linregress(x["z"],x["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(x)})
    out["rise slope by coin"]=d.groupby("coin").apply(slu)
    # interaction: fall slope by vol level tercile
    d["vt"]=d.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fall slope by vol tercile"]=d.dropna(subset=["vt"]).groupby("vt").apply(sl)
    d["rt"]=d.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fall slope by range-compression tercile"]=d.dropna(subset=["rt"]).groupby("rt").apply(sl)
    return out
