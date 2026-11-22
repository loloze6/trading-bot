def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    dl=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dl.append(d)
    D=pd.concat(dl,ignore_index=True)
    D["dt"]=pd.to_datetime(D["day"]); D["wd"]=D["dt"].dt.dayofweek; D["year"]=D["dt"].dt.year
    D["vol"]=D.groupby(["coin","win"])["coin_return"].transform(lambda s:s.rolling(20,min_periods=15).std().shift(1))
    D["z"]=D["coin_return"]/D["vol"]
    def summ(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    D["sat"]=(D["wd"]==5)
    D["frisat"]=D["wd"].isin([4,5])
    out["coin z by weekday"]=D.groupby("wd")["z"].apply(summ).unstack()
    def diff(d,col):
        a=d.loc[d[col],"coin_return"].dropna(); b=d.loc[~d[col],"coin_return"].dropna()
        r=stats.ttest_ind(a,b,equal_var=False)
        return pd.Series({"nA":len(a),"diff":a.mean()-b.mean(),"t":r.statistic})
    out["sat minus other, by coin"]=D.groupby("coin").apply(lambda d:diff(d,"sat"))
    out["sat minus other, by year"]=D.groupby("year").apply(lambda d:diff(d,"sat"))
    # day-clustered: average across coins per day
    M=D.groupby(["dt"]).agg(r=("coin_return","mean"),z=("z","mean"),wd=("wd","first"),year=("year","first"))
    out["cross-coin day mean by weekday"]=M.groupby("wd")["r"].apply(summ).unstack()
    out["sat minus other, day-mean, by year"]=M.assign(sat=M.wd==5).groupby("year").apply(lambda d:pd.Series({"n":d.sat.sum(),"diff":d.loc[d.sat,"r"].mean()-d.loc[~d.sat,"r"].mean(),"t":stats.ttest_ind(d.loc[d.sat,"r"].dropna(),d.loc[~d.sat,"r"].dropna(),equal_var=False).statistic}))
    # bars: r90 grading and momentum in trending
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy(); c=b["close"].astype(float)
            b["coin"]=coin; b["pos"]=np.arange(len(b))
            b["fwd5"]=c.shift(-5)/c-1
            b["r90"]=c/c.shift(90)-1
            b["r20"]=c/c.shift(20)-1
            b["vol"]=c.pct_change().rolling(20,min_periods=15).std()
            mx=c.rolling(30,min_periods=30).max(); mn=c.rolling(30,min_periods=30).min()
            b["rp"]=(c-mn)/(mx-mn)
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","pos","fwd5","r90","r20","vol","rp","year","regime"]])
    g=pd.concat(rows,ignore_index=True)
    g=g[(g.pos%5==0)&g.fwd5.notna()].copy()
    g["dm"]=g.fwd5-g.groupby("coin").fwd5.transform("mean")
    g["z20"]=g.r20/(g.vol*np.sqrt(20))
    def slope(d,xc):
        d=d[[xc,"dm"]].dropna()
        if len(d)<20: return pd.Series({"n":len(d),"slope":np.nan,"t":np.nan})
        r=stats.linregress(d[xc],d["dm"]); return pd.Series({"n":len(d),"slope":r.slope,"t":r.slope/r.stderr})
    tr=g[g.regime=="trending"].copy()
    tr["r90q"]=tr.groupby("coin").r90.transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["trending rp slope by r90 tercile"]=tr.groupby("r90q").apply(lambda d:slope(d,"rp"))
    out["trending mean dm by r90 tercile"]=tr.groupby("r90q").dm.apply(summ).unstack()
    out["slope r90 on dm, all grid"]=slope(g,"r90")
    g["era"]=np.where(g.year<=2021,"<=2021",">=2022")
    out["trending rp slope by era"]=g[g.regime=="trending"].groupby("era").apply(lambda d:slope(d,"rp"))
    out["trending z20 slope by era"]=g[g.regime=="trending"].groupby("era").apply(lambda d:slope(d,"z20"))
    out["unknown rp slope by era"]=g[g.regime=="unknown"].groupby("era").apply(lambda d:slope(d,"rp"))
    out["unknown z20 slope by era"]=g[g.regime=="unknown"].groupby("era").apply(lambda d:slope(d,"z20"))
    return out
