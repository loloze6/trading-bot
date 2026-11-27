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
            lo20=c.rolling(20,min_periods=20).min()
            sd20=r.rolling(20,min_periods=20).std()
            depth=(hi20-c)/hi20/sd20
            hgt=(c-lo20)/lo20/sd20
            tr60=c/c.shift(60)-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"nxt":nxt,"depth":depth,"hgt":hgt,"tr60":tr60,
                            "sd20":sd20,"rng_s":rng/sd20,"clv":clv,
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D=D.dropna(subset=["nxt","depth","r"])
    D["trend"]=np.where(D["tr60"].isna(),"na",np.where(D["tr60"]>0.1,"rising",np.where(D["tr60"]<-0.1,"falling","choppy")))
    D["up"]=np.where(D["r"]>0,"up","down")
    D["dq"]=pd.qcut(D["depth"].rank(method="first"),5,labels=False)
    def summ(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    out["trend_up_dq"]=D[D.trend!="na"].groupby(["trend","up","dq"]).apply(summ).reset_index()
    sl=[]
    for (tr,u),g in D.groupby(["trend","up"]):
        s=stats.linregress(g["depth"],g["ex"]); sl.append({"trend":tr,"up":u,"n":len(g),"slope%":s.slope*100,"t":s.slope/s.stderr})
    out["slope_depth"]=pd.DataFrame(sl)
    D["hq"]=pd.qcut(D["hgt"].rank(method="first"),5,labels=False)
    out["trend_hq"]=D[D.trend!="na"].groupby(["trend","hq"]).apply(summ).reset_index()
    D["rq"]=pd.qcut(D["rng_s"].rank(method="first"),5,labels=False)
    D["cq"]=pd.cut(D["clv"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=False)
    out["rq_cq_extremes"]=D[D.rq.isin([0,4])].groupby(["rq","cq"]).apply(summ).reset_index()
    D["rz"]=pd.qcut((D["r"]/D["sd20"]).rank(method="first"),5,labels=False)
    out["trend_rz"]=D[D.trend!="na"].groupby(["trend","rz"]).apply(summ).reset_index()
    out["weekday"]=D.groupby("wd").apply(summ).reset_index()
    return out
