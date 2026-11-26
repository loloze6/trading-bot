def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            s=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c/s
            loc=(b["high"]-c)/(b["high"]-b["low"]).replace(0,np.nan)
            nxt=c.shift(-1)/c-1
            nxt3=c.shift(-3)/c-1
            tr60=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"wd":ts.dt.weekday,
                "inprof":(b["regime"]!="chop").astype(int),"regime":b["regime"],
                "rng":rng,"loc":loc,"r":r,"rz":r/s,"nxt":nxt,"nxt3":nxt3,"tr60":tr60,
                "fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            df["i"]=np.arange(len(df))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-drift
    def tday(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan,"days":0})
        dev=g[col]-g[col].mean()
        sd=dev.groupby(g["day"]).sum()
        se=np.sqrt((sd**2).sum())/len(g)
        return pd.Series({"n":len(g),"mean%":100*g[col].mean(),"t":g[col].mean()/se if se>0 else np.nan,"days":g["day"].nunique()})
    d["rb"]=pd.cut(d["rng"],[0,1,1.5,2,3,100],labels=["<1","1-1.5","1.5-2","2-3",">3"])
    d["lb"]=pd.cut(d["loc"],[-0.01,0.333,0.667,1.01],labels=["highclose","mid","lowclose"])
    out={}
    out["inprof_rng_loc"]=d.groupby(["inprof","rb","lb"],observed=True).apply(tday)
    # trend split for out-of-profile (tr60 computable)
    d["tb"]=pd.cut(d["tr60"],[-10,-0.1,0.1,100],labels=["fall","chop","rise"])
    out["trend_lowclose_wide"]=d[(d.rng>=2)].groupby(["tb","lb"],observed=True).apply(tday)
    # large moves: next-day after rz
    d["zb"]=pd.cut(d["rz"],[-100,-2,-1,0,1,2,100])
    out["rz_by_prof"]=d.groupby(["inprof","zb"],observed=True).apply(tday)
    out["wd_by_prof"]=d.groupby(["inprof","wd"]).apply(tday)
    out["3d_inprof_wide"]=d[(d.inprof==1)&(d.rng>=2)].groupby("lb",observed=True).apply(lambda g:tday(g,"nxt3"))
    out["regime_counts"]=d["regime"].value_counts()
    return out
