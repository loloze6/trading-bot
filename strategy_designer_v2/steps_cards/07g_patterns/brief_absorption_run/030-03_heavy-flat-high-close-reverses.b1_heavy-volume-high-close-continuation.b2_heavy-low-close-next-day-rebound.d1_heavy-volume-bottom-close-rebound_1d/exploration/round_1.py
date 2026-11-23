def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            if len(b)<30: continue
            c=b["close"]; h=b["high"]; l=b["low"]; v=b["volume"]
            rng=(h-l).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["pos"]=np.arange(len(b))
            d["loc"]=(h-c)/rng  # 1 at low
            d["vr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            d["r0"]=c/c.shift(1)-1
            d["body"]=(c-b["open"])/rng
            d["r5p"]=c/c.shift(5)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["rngrel"]=(h-l)/c
            d["rngratio"]=d["rngrel"]/d["rngrel"].shift(1).rolling(20).mean()
            for k in (1,3,5):
                d[f"f{k}"]=c.shift(-k)/c-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["fc"]=b["forecast"]; d["alloc"]=b["postRebalance_current_allocation"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu={k:D.groupby("coin")[f"f{k}"].apply(lambda s: s[D.loc[s.index,"pos"]%k==0].mean()) for k in (1,3,5)}
    for k in (1,3,5):
        D[f"x{k}"]=D[f"f{k}"]-D["coin"].map(mu[k])
    def tab(df,g,col="x1",k=1):
        df=df[df["pos"]%k==0].dropna(subset=[col])
        r=df.groupby(g)[col].agg(["mean","count","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r[["mean","count","t"]].round(5)
    out={}
    D["locq"]=pd.cut(D["loc"],[-.01,.25,.5,.75,1.01],labels=["top","mh","ml","low"])
    D["vrb"]=pd.cut(D["vr"],[0,0.7,1,1.5,2,3,100],labels=["<.7",".7-1","1-1.5","1.5-2","2-3",">3"])
    D["g"]=D["vrb"].astype(str)+"_"+D["locq"].astype(str)
    out["x1 by vr bucket x loc quartile"]=tab(D,"g")
    hv=D[D["vr"]>=2]
    out["heavy: x3 by locq"]=tab(hv,"locq","x3",3)
    out["heavy: x5 by locq"]=tab(hv,"locq","x5",5)
    # low-close heavy days, by day's return sign / size
    hl=hv[hv["loc"]>=0.75].copy()
    hl["r0q"]=pd.qcut(hl["r0"],4,labels=False)
    out["heavy low-close: x1 by day return quartile"]=tab(hl,"r0q")
    hl["rrq"]=pd.qcut(hl["rngratio"],3,labels=False)
    out["heavy low-close: x1 by range ratio tercile"]=tab(hl,"rrq")
    hl["r5q"]=pd.qcut(hl["r5p"],3,labels=False)
    out["heavy low-close: x1 by prior 5d tercile"]=tab(hl,"r5q")
    # all days: next-day after large moves by vol
    D["z"]=D["r0"]/D["vol20"]
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    out["all: x1 by day z"]=tab(D,"zb")
    out["all: x1 by locq (any volume)"]=tab(D,"locq")
    out["all: x1 by weekday"]=tab(D,"wd")
    out["heavy low: x1 by year"]=tab(hl,"yr")
    out["heavy low: x1 by coin"]=tab(hl,"coin")
    # slope of x1 on loc, by vr bucket
    s=[]
    for bkt,gq in D.dropna(subset=["x1","loc","vr"]).groupby("vrb"):
        r=stats.linregress(gq["loc"],gq["x1"]); s.append((str(bkt),r.slope,r.slope/r.stderr,len(gq)))
    out["slope x1 on loc by vr"]=pd.DataFrame(s,columns=["vr","slope","t","n"]).round(5)
    return out
