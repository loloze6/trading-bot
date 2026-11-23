def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            if len(b)<30: continue
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); v=b["volume"].astype(float)
            rng=(h-l).replace(0,np.nan)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["pos"]=np.arange(len(b))
            d["loc"]=(h-c)/rng
            d["vr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            d["r0"]=c/c.shift(1)-1
            d["r5p"]=c/c.shift(5)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["rngrel"]=(h-l)/c
            d["rngratio"]=d["rngrel"]/d["rngrel"].shift(1).rolling(20).mean()
            for k in (1,3,5):
                d[f"f{k}"]=c.shift(-k)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values; d["yr"]=ts.dt.year.values
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in (1,3,5):
        g=D[D["pos"]%k==0].groupby("coin")[f"f{k}"].mean()
        D[f"x{k}"]=D[f"f{k}"]-D["coin"].map(g)
    def tab(df,g,col="x1",k=1):
        df=df[df["pos"]%k==0].dropna(subset=[col])
        r=df.groupby(g,observed=True)[col].agg(["mean","count","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r[["mean","count","t"]].round(5)
    out={}
    D["locq"]=pd.cut(D["loc"],[-.01,.25,.5,.75,1.01],labels=["top","mh","ml","low"])
    D["vrb"]=pd.cut(D["vr"],[0,0.7,1,1.5,2,3,100],labels=["a<.7","b.7-1","c1-1.5","d1.5-2","e2-3","f>3"])
    D["g"]=D["vrb"].astype(str)+"_"+D["locq"].astype(str)
    out["x1 by vr bucket x loc quartile"]=tab(D.dropna(subset=["vrb","locq"]),"g")
    hv=D[D["vr"]>=2]
    out["heavy: x3 by locq"]=tab(hv,"locq","x3",3)
    out["heavy: x5 by locq"]=tab(hv,"locq","x5",5)
    hl=hv[hv["loc"]>=0.75].copy()
    hl["r0q"]=pd.qcut(hl["r0"],4,labels=False)
    out["heavy low: x1 by day return quartile"]=tab(hl,"r0q")
    out["heavy low: day return quartile means"]=hl.groupby("r0q")["r0"].mean().round(4)
    hl["rrq"]=pd.qcut(hl["rngratio"],3,labels=False)
    out["heavy low: x1 by range ratio tercile"]=tab(hl,"rrq")
    hl["r5q"]=pd.qcut(hl["r5p"],3,labels=False)
    out["heavy low: x1 by prior 5d tercile"]=tab(hl,"r5q")
    out["heavy low: x1 by year"]=tab(hl,"yr")
    out["heavy low: x1 by coin"]=tab(hl,"coin")
    D["z"]=D["r0"]/D["vol20"]
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    out["all: x1 by day z"]=tab(D.dropna(subset=["zb"]),"zb")
    D["zl"]=D["zb"].astype(str)+"_"+D["locq"].astype(str)
    out["all: x1 by z x locq"]=tab(D.dropna(subset=["zb","locq"]),"zl")
    out["all: x1 by weekday"]=tab(D,"wd")
    s=[]
    for bkt,gq in D.dropna(subset=["x1","loc","vr"]).groupby("vrb",observed=True):
        r=stats.linregress(gq["loc"],gq["x1"]); s.append((str(bkt),r.slope,r.slope/r.stderr,len(gq)))
    out["slope x1 on loc by vr"]=pd.DataFrame(s,columns=["vr","slope","t","n"]).round(5)
    # book days: largest gains/losses
    bd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bd.append(dd[["book_return","coin_return"]].assign(coin=coin))
    B=pd.concat(bd).dropna()
    B=B[B["book_return"]!=0]
    q=B["book_return"].quantile([.05,.95])
    out["book active days: share of gain from top5%/bottom5%"]=pd.Series({
        "n_active":len(B),"sum_all":B["book_return"].sum(),
        "sum_top5":B[B.book_return>=q[.95]]["book_return"].sum(),
        "sum_bot5":B[B.book_return<=q[.05]]["book_return"].sum()}).round(4)
    return out
