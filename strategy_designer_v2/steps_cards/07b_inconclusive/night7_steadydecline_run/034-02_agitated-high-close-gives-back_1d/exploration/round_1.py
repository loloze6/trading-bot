def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy().reset_index(drop=True)
            rng=(d["high"]-d["low"])
            d["clv"]=np.where(rng>0,(d["close"]-d["low"])/rng,np.nan)
            for h in (1,2,3,5):
                d[f"r{h}"]=d["close"].shift(-h)/d["close"]-1
            d["agit"]=(d["regime"]!="chop")
            d["coin"]=coin; d["win"]=w
            d["year"]=pd.to_datetime(d["timestamp"]).dt.year
            d["pos"]=d.index
            d["absret"]=(d["close"]/d["close"].shift(1)-1).abs()
            rows.append(d[["coin","win","year","pos","clv","r1","r2","r3","r5","agit","forecast","postRebalance_current_allocation","absret","timestamp"]])
    A=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,5):
        A[f"x{h}"]=A[f"r{h}"]-A.groupby("coin")[f"r{h}"].transform("mean")
    A["q"]=pd.qcut(A["clv"],5,labels=False)
    out={}
    def summ(g,col="x1"):
        v=g[col].dropna()
        return pd.Series({"n":len(v),"mean%":v.mean()*100,"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
    out["by_quintile_agit"]=A.groupby(["agit","q"]).apply(summ)
    # correlation clv vs x1 by regime, coin
    def corr(g,col="x1"):
        s=g[["clv",col]].dropna()
        r,p=stats.pearsonr(s["clv"],s[col]) if len(s)>10 else (np.nan,np.nan)
        return pd.Series({"n":len(s),"corr":r,"t":r*np.sqrt((len(s)-2)/(1-r*r)) if len(s)>10 else np.nan})
    out["corr_by_agit_coin"]=A.groupby(["agit","coin"]).apply(corr)
    out["corr_by_agit_year"]=A.groupby(["agit","year"]).apply(corr)
    # horizons, non-overlap grid
    res=[]
    for h in (1,2,3,5):
        S=A[(A["pos"]%h==0)]
        for ag in (True,False):
            s=S[S["agit"]==ag][["clv",f"x{h}"]].dropna()
            r=s.corr().iloc[0,1]
            res.append({"h":h,"agit":ag,"n":len(s),"corr":r,"t":r*np.sqrt((len(s)-2)/(1-r*r))})
    out["horizons"]=pd.DataFrame(res)
    # agitated, split by size of day's move tercile
    Ag=A[A["agit"]].copy()
    Ag["mv"]=Ag.groupby("coin")["absret"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["agit_by_movetercile"]=Ag.groupby("mv").apply(corr)
    # top vs bottom side: clv>0.5 short; clv<0.5 long
    Ag["side_hi"]=Ag["clv"]>0.5
    out["agit_side_mean_x1"]=Ag.groupby("side_hi").apply(summ)
    return out
