def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    H=72
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values; f=b["forecast"].values
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for i in range(0,n,H):
                past = c[i]/c[i-H]-1 if i>=H else np.nan
                r24 = c[i+24]/c[i]-1 if i+24<n else np.nan
                r72 = c[i+72]/c[i]-1 if i+72<n else np.nan
                r168 = c[i+168]/c[i]-1 if i+168<n else np.nan
                rows.append((coin,w,ts.iloc[i].year,f[i],past,r24,r72,r168))
    d=pd.DataFrame(rows,columns=["coin","w","year","f","past","r24","r72","r168"])
    for h in ["r24","r72","r168"]:
        d["x"+h]=d[h]-d.groupby("coin")[h].transform("mean")
    def slope(g,y="xr72",x="f"):
        g=g.dropna(subset=[x,y])
        if len(g)<20 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["all"]=slope(d)
    # sign of past move from forecast/ components: use price past (needs i>=72)
    d["side"]=np.where(d["past"]>0,"up",np.where(d["past"]<0,"down","na"))
    out["by_side_r72"]=d.groupby("side").apply(slope)
    out["by_side_r24"]=d.groupby("side").apply(lambda g: slope(g,"xr24"))
    out["by_side_r168"]=d.groupby("side").apply(lambda g: slope(g,"xr168"))
    out["by_coin"]=d.groupby("coin").apply(slope)
    out["by_year"]=d.groupby("year").apply(slope)
    d["q"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    out["quint"]=d.groupby(["q"]).agg(n=("f","size"),f=("f","mean"),xr72=("xr72","mean"),sd=("xr72","std"))
    out["quint_side"]=d.groupby(["side","q"])["xr72"].agg(["size","mean"]).unstack(0)
    # signed past return regression
    d["z"]=d.groupby("coin")["past"].transform(lambda s:(s-s.mean())/s.std())
    out["signed_past"]=slope(d,"xr72","z")
    # book timing by coin
    bt=[]
    for coin,wins in data["bars"].items():
        days=[];
        for w,b in wins.items():
            dd=data["days"][coin][w]
            ts=pd.to_datetime(b["timestamp"]).dt.floor("D")
            al=b.groupby(ts)["postRebalance_current_allocation"].mean()
            x=dd.copy(); x["day"]=pd.to_datetime(x["day"]); x["al"]=x["day"].map(al)
            days.append(x)
        x=pd.concat(days).dropna(subset=["book_return","coin_return"])
        mu=x["coin_return"].mean()
        bt.append((coin,x["book_return"].mean(),(x["al"]*mu).mean(),x["al"].mean(),x["book_return"].mean()-(x["al"]*mu).mean()))
    out["book_by_coin"]=pd.DataFrame(bt,columns=["coin","book","market","alloc","timing"]).set_index("coin")
    return out
