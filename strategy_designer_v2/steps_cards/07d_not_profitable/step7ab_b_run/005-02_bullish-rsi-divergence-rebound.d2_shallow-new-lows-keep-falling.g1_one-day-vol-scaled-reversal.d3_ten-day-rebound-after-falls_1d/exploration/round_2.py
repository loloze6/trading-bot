def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; coins=list(bars.keys())
    B=[]
    for c in coins:
        mu=pd.concat([b.close.pct_change() for b in bars[c].values()]).mean()
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy(); cl=b.close
            b["ret1"]=cl.pct_change(); b["nxt"]=cl.shift(-1)/cl-1
            b["fwd10"]=cl.shift(-10)/cl-1
            b["r20"]=cl/cl.shift(20)-1; b["r5"]=cl/cl.shift(5)-1
            b["vol20"]=b.ret1.rolling(20).std()
            b["z1"]=b.ret1/b.vol20.shift(1)
            b["hi20"]=cl/cl.rolling(20).max()-1
            b["lo20"]=cl/cl.rolling(20).min()-1
            b["newlow"]=(cl<=cl.rolling(20).min())
            b["alloc"]=b.postRebalance_current_allocation
            b["gain"]=b.alloc*b.nxt
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(len(b)); b["mu"]=mu
            B.append(b)
    B=pd.concat(B)
    C=B[(B.pos%10==0)&B.fwd10.notna()].copy()
    C["ex"]=C.fwd10-C.groupby("coin").fwd10.transform("mean")
    D=C[C.ret1<0].dropna(subset=["z1","r20","hi20"]).copy()
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    D["r20q"]=pd.qcut(D.r20,3,labels=["down","mid","up"])
    out["down-day cells excess by 20d return tercile"]=D.groupby("r20q",observed=True).ex.apply(tt).unstack().round(4)
    D["hiq"]=pd.qcut(D.hi20,3,labels=["far_below_high","mid","near_high"])
    out["down-day cells excess by distance to 20d high"]=D.groupby("hiq",observed=True).ex.apply(tt).unstack().round(4)
    out["down-day cells excess, new 20d low vs not"]=D.groupby("newlow").ex.apply(tt).unstack().round(4)
    res={}
    for k,g in D.groupby("r20q",observed=True):
        sl=stats.linregress(-g.z1,g.ex); res[k]=[len(g),sl.slope,sl.slope/sl.stderr]
    out["slope of excess on fall size by 20d tercile"]=pd.DataFrame(res,index=["n","slope","t"]).T.round(4)
    # all cells (up days too): excess by 20d return tercile -> trend continuation?
    A=C.dropna(subset=["r20"]).copy(); A["r20q"]=pd.qcut(A.r20,3,labels=["down","mid","up"])
    out["all cells excess by 20d tercile"]=A.groupby("r20q",observed=True).ex.apply(tt).unstack().round(4)
    sl=stats.linregress(A.r20/A.vol20,A.ex); out["all cells slope ex on r20/vol t"]=f"{sl.slope/sl.stderr:.2f}, n {len(A)}"
    # book bar gain by 20d tercile
    Bb=B.dropna(subset=["r20","nxt"]).copy(); Bb["r20q"]=pd.qcut(Bb.r20,3,labels=["down","mid","up"])
    out["bars by 20d tercile"]=Bb.groupby("r20q",observed=True).agg(alloc=("alloc","mean"),gain=("gain","mean"),coin=("nxt","mean"),n=("nxt","size")).round(5)
    # worst 5% book bars: context
    Bb["worst"]=Bb.gain<=Bb.gain.quantile(0.05)
    out["context worst 5% bars vs rest"]=Bb.groupby("worst")[["r20","hi20","alloc","vol20"]].mean().round(4)
    # bars whose forecast was zero but long held (holding period effect)
    out["share long bars with forecast 0"]=f"{((Bb.alloc>0.01)&(Bb.forecast<=0)).mean():.3f}"
    return out
