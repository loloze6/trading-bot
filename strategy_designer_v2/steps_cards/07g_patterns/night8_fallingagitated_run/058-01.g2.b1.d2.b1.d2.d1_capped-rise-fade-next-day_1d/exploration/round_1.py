def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r,"sd":sd})
            d["z1"]=r/sd
            d["z3"]=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            d["z5"]=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            d["n1"]=c.shift(-1)/c-1
            d["n3"]=c.shift(-3)/c-1
            d["pos"]=np.arange(len(b))
            d["inprof"]=b["regime"].isin(["mean_reversion","unknown"]).values
            d["regime"]=b["regime"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year.values
            d["rng"]=((b["high"]-b["low"])/c).values/sd
            d["clv"]=((c-b["low"])/(b["high"]-b["low"])).values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift1=D.groupby("coin")["n1"].transform("mean")
    D["u1"]=D["n1"]-drift1
    drift3=D[D.pos%3==0].groupby("coin")["n3"].mean()
    D["u3"]=D["n3"]-D["coin"].map(drift3)
    def summ(g,col):
        x=g[col].dropna()
        n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["z1b"]=pd.cut(D["z1"],[-99,-2,-1,-0.5,0,0.5,1,1.5,2,99])
    out["u1 by z1 in profile"]=D[D.inprof].groupby("z1b",observed=True).apply(summ,"u1")
    out["u1 by z1 out profile"]=D[~D.inprof].groupby("z1b",observed=True).apply(summ,"u1")
    G3=D[D.pos%3==0].copy()
    G3["z3b"]=pd.cut(G3["z3"],[-99,-2,-1,0,1,2,99])
    out["u3 by z3 in profile (grid3)"]=G3[G3.inprof].groupby("z3b",observed=True).apply(summ,"u3")
    out["u3 by z3 out profile (grid3)"]=G3[~G3.inprof].groupby("z3b",observed=True).apply(summ,"u3")
    D["z5b"]=pd.cut(D["z5"],[-99,-2,-1,0,1,2,99])
    out["u1 by z5 in profile"]=D[D.inprof].groupby("z5b",observed=True).apply(summ,"u1")
    out["u1 by z5 out profile"]=D[~D.inprof].groupby("z5b",observed=True).apply(summ,"u1")
    D["clvb"]=pd.cut(D["clv"],[0,0.2,0.4,0.6,0.8,1.0],include_lowest=True)
    out["u1 by close loc in profile"]=D[D.inprof].groupby("clvb",observed=True).apply(summ,"u1")
    out["u1 by close loc out profile"]=D[~D.inprof].groupby("clvb",observed=True).apply(summ,"u1")
    out["u1 by weekday all"]=D.groupby("wd").apply(summ,"u1")
    out["u1 by weekday in profile"]=D[D.inprof].groupby("wd").apply(summ,"u1")
    out["share in profile by year"]=D.groupby("yr")["inprof"].mean()
    act=D[D.regime=="mean_reversion"]
    act=act.assign(s=-act["u1"])
    out["short case u1 by year"]=act.groupby("yr").apply(summ,"s")
    out["short case u1 by coin"]=act.groupby("coin").apply(summ,"s")
    return out
