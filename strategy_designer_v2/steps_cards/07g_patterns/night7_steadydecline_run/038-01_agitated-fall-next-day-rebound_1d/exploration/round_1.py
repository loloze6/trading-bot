def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            m=r.rolling(60,min_periods=20).mean(); s=r.rolling(60,min_periods=20).std()
            z=(r-m)/s
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"r":r,"z":z,
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"n3":c.shift(-3)/c-1,"n5":c.shift(-5)/c-1,
                "reg":b["regime"].astype(str),"fc":b["forecast"],
                "clv":(b["close"]-b["low"])/(b["high"]-b["low"]),
                "rng":(b["high"]-b["low"])/c.shift(1),
                "tr60":c/c.shift(60)-1,"vol30":r.rolling(30).std(),
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["mu"]=D["coin"].map(mu)
    for h in [1,2,3,5]: D[f"x{h}"]=D[f"n{h}"]-h*D["mu"]
    D["day"]=D["ts"].dt.floor("D")
    D["prof"]=np.where(D["reg"]=="unknown","FA","other")
    D.loc[(D.prof=="other")&(D.tr60< -0.10),"prof"]="other_falling"
    D["zb"]=pd.cut(D["z"],[-99,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,99])
    def tday(g,col):
        g=g.dropna(subset=[col]); dm=g.groupby("day")[col].mean()
        n=len(dm); 
        return pd.Series({"mean%":g[col].mean()*100,"t_day":dm.mean()/(dm.std()/np.sqrt(n)) if n>2 else np.nan,"cases":len(g),"days":n})
    out={}
    out["regime counts"]=D["prof"].value_counts()
    out["x1 by prof x zbucket"]=D.groupby(["prof","zb"],observed=True).apply(lambda g:tday(g,"x1")).round(3)
    fa=D[(D.prof=="FA")&(D.r<0)]
    out["FA falls: horizons"]=pd.DataFrame({h:tday(fa,h) for h in ["x1","x2","x3","x5"]}).round(3)
    fa2=fa.copy(); fa2["clvb"]=pd.qcut(fa2["clv"],3,labels=["lowclose","mid","highclose"])
    out["FA falls x1 by close location"]=fa2.groupby("clvb",observed=True).apply(lambda g:tday(g,"x1")).round(3)
    fa2["big"]=fa2["z"]< -1
    out["FA falls x1 by big x clv"]=fa2.groupby(["big","clvb"],observed=True).apply(lambda g:tday(g,"x1")).round(3)
    fa2["wd"]=fa2["ts"].dt.dayofweek
    out["FA falls x1 by weekday"]=fa2.groupby("wd").apply(lambda g:tday(g,"x1")).round(3)
    out["FA falls x1 by coin"]=fa2.groupby("coin").apply(lambda g:tday(g,"x1")).round(3)
    up=D[(D.prof=="FA")&(D.r>0)]
    out["FA up days x1 by z"]=up.groupby("zb",observed=True).apply(lambda g:tday(g,"x1")).round(3)
    # book days
    bd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bd.append(dd.assign(coin=coin,w=w))
    B=pd.concat(bd); bk=B.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["mean","std","count"]).assign(mean_bp=lambda x:x["mean"]*1e4).round(5)
    return out
