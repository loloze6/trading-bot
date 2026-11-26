def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            o,h,l,c=b["open"],b["high"],b["low"],b["close"]
            rng=(h-l)
            d["cl"]=np.where(rng>0,(c-l)/rng,np.nan)
            d["rm"]=rng/rng.rolling(20,min_periods=20).mean()
            d["ret"]=c.pct_change()
            d["tr60"]=c/c.shift(60)-1
            d["v30"]=d["ret"].rolling(30).std()
            d["nxt"]=c.shift(-1)/c-1
            d["nxt2"]=c.shift(-2)/c-1
            d["fa"]=b["regime"].isin(["mean_reversion","unknown"])
            d["bk"]=b["postRebalance_total_value"].pct_change()
            d["pos"]=b["postRebalance_current_allocation"]
            d["coin"]=coin; d["w"]=w; d["yr"]=d["day"].dt.year
            d["i"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D["ex2"]=D["nxt2"]-D.groupby("coin")["nxt2"].transform("mean")
    def summ(g,col="ex"):
        x=g.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x)})
        pd_=x.groupby("day")[col].mean()
        t=pd_.mean()/(pd_.std()/np.sqrt(len(pd_)))
        return pd.Series({"n":len(x),"days":len(pd_),"mean%":x[col].mean()*100,"t_day":t})
    out={}
    N=D[(~D["fa"])].copy()
    N["tr"]=pd.cut(N["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    FC=N[N["tr"].isin(["fall","chop"])]
    out["fall+chop nonfa cl quintile"]=FC.groupby(pd.qcut(FC["cl"],5)).apply(summ)
    out["fall+chop nonfa cl quintile 2d"]=FC.groupby(pd.qcut(FC["cl"],5)).apply(lambda g:summ(g[g["i"]%2==0],"ex2"))
    hc=FC[FC["cl"]>0.5]
    out["fall+chop hi close by year"]=hc.groupby("yr").apply(summ)
    out["fall+chop hi close by coin"]=hc.groupby("coin").apply(summ)
    out["fall+chop hi close by rm tercile"]=hc.groupby(pd.qcut(hc["rm"],3)).apply(summ)
    # agitation proxy: v30 vs coin median of v30 in folds
    FC=FC.assign(ag=FC["v30"]>FC.groupby("coin")["v30"].transform("median"))
    out["fall+chop x agit proxy x cl>0.5"]=FC.groupby(["tr","ag",FC["cl"]>0.5],observed=True).apply(summ)
    R=N[N["tr"]=="rise"]
    out["rise cl quintile"]=R.groupby(pd.qcut(R["cl"],5)).apply(summ)
    # FA tested effect by year
    F=D[D["fa"]&(D["cl"]>0.5)]
    out["fa hi close by year"]=F.groupby("yr").apply(summ)
    # book concentration
    bk=D.dropna(subset=["bk"])
    top=bk.groupby(["day"])["bk"].mean().sort_values()
    out["book top10 days share of sum"]=float(top.tail(10).sum()/top.sum())
    out["book bottom10 days sum"]=float(top.head(10).sum())
    out["book w14 by coin"]=D[D["w"]=="w14"].groupby("coin")["bk"].sum()
    return out
