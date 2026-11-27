def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            hi20=c.rolling(20,min_periods=20).max()
            sd20=r.rolling(20,min_periods=20).std()
            sd30=r.rolling(30,min_periods=30).std()
            depth=(hi20-c)/hi20/sd20
            tr60=c/c.shift(60)-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"r":r,"nxt":nxt,"depth":depth,"tr60":tr60,
                "sd20":sd20,"sd30":sd30,"rng_s":rng/sd20,"clv":clv,"yr":ts.dt.year}))
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D["agit"]=np.where(D["sd30"]>D.groupby("coin")["sd30"].transform("median"),"agit","calm")
    D=D.dropna(subset=["nxt","depth","r","tr60","sd30"])
    D["trend"]=np.where(D["tr60"]>0.1,"rising",np.where(D["tr60"]<-0.1,"falling","choppy"))
    D["up"]=np.where(D["r"]>0,"up","down")
    def slope(g):
        if len(g)<30: return pd.Series({"n":len(g),"slope%":np.nan,"t":np.nan})
        s=stats.linregress(g["depth"],g["ex"]); return pd.Series({"n":len(g),"slope%":s.slope*100,"t":s.slope/s.stderr})
    def summ(g):
        x=g["ex"]; return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    out["slope_trend_agit"]=D.groupby(["trend","agit"]).apply(slope).reset_index()
    out["slope_trend_agit_up"]=D.groupby(["trend","agit","up"]).apply(slope).reset_index()
    C=D[D.trend=="choppy"]
    out["choppy_slope_by_window"]=C.groupby("w").apply(slope).reset_index()
    out["choppy_slope_by_year"]=C.groupby("yr").apply(slope).reset_index()
    C=C.copy(); C["dq"]=pd.qcut(C["depth"].rank(method="first"),3,labels=False)
    out["choppy_agit_dq3"]=C.groupby(["agit","dq"]).apply(summ).reset_index()
    W=D[D.rng_s>=D.rng_s.quantile(0.8)].copy()
    W["cq"]=pd.cut(W["clv"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=False)
    out["wide_lowclose_by_trend_agit"]=W[W.cq==0].groupby(["trend","agit"]).apply(summ).reset_index()
    return out
