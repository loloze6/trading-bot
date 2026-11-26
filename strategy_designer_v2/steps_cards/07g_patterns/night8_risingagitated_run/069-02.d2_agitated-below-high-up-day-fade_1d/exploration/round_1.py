def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            r1=c.pct_change()
            nxt=c.shift(-1)/c-1
            vol20=r1.rolling(20,min_periods=15).std()
            hh20=h.rolling(20,min_periods=15).max(); ll20=l.rolling(20,min_periods=15).min()
            depth=(hh20-c)/hh20/vol20
            pos=(c-ll20)/(hh20-ll20)
            rng=(h-l)/c/vol20
            clv=(c-l)/(h-l)
            ret5=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"r1":r1,"z1":r1/vol20,"nxt":nxt,
                "depth":depth,"pos":pos,"rng":rng,"clv":clv,"z5":ret5/(vol20*np.sqrt(5)),
                "ag":(b["regime"]!="chop").astype(int),"regime":b["regime"],
                "alloc":b["postRebalance_current_allocation"],"fc":b["forecast"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["ts"]=pd.to_datetime(d["ts"])
    d["day"]=d["ts"].dt.floor("D")
    d["wd"]=d["ts"].dt.weekday
    mu=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-mu
    d=d.dropna(subset=["ex","z1","depth","pos"])
    def g(sub,key):
        def f(x):
            # day-clustered t
            s=x.groupby("day")["ex"].sum(); n=len(x); m=x["ex"].mean()
            se=np.sqrt(((x.groupby("day")["ex"].apply(lambda v:(v-m).sum()))**2).sum())/n
            return pd.Series({"n":n,"mean%":m*100,"t_cl":m/se if se>0 else np.nan})
        return sub.groupby(key).apply(f)
    out={}
    d["up"]=(d["r1"]>0).astype(int)
    d["z1q"]=pd.qcut(d["z1"],5,labels=False)
    d["posq"]=pd.qcut(d["pos"],5,labels=False)
    d["depthq"]=pd.qcut(d["depth"],5,labels=False)
    d["rngq"]=pd.qcut(d["rng"],4,labels=False)
    d["clvq"]=pd.qcut(d["clv"],4,labels=False)
    d["z5q"]=pd.qcut(d["z5"],5,labels=False)
    out["ag_up"]=g(d,["ag","up"])
    out["ag_z1q"]=g(d,["ag","z1q"])
    out["ag_up_posq"]=g(d,["ag","up","posq"])
    out["ag_z5q"]=g(d,["ag","z5q"])
    out["ag_up_clvq"]=g(d,["ag","up","clvq"])
    out["ag_rngq"]=g(d,["ag","rngq"])
    out["wd"]=g(d,["wd"])
    out["coin_ag_up"]=g(d,["coin","ag","up"]).reset_index().query("ag==1")
    return out
