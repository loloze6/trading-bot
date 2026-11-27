def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            rng=b.high-b.low
            mr=rng.rolling(20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b.timestamp)})
            d["prod"]=(b.close-(b.high+b.low)/2)/mr
            d["wid"]=rng/mr
            d["loc"]=(b.close-b.low)/rng.replace(0,np.nan)
            d["r0"]=b.close.pct_change()
            d["r0s"]=d.r0/d.r0.rolling(20).std()
            d["nxt"]=b.close.shift(-1)/b.close-1
            d["nxt3"]=b.close.shift(-3)/b.close-1
            d["inprof"]=(b.regime!="chop")
            d["reg"]=b.regime
            d["alloc"]=b.postRebalance_current_allocation
            rows.append(d)
    D=pd.concat(rows)
    drift=D.groupby("coin").nxt.mean()
    D["ab"]=D.nxt-D.coin.map(drift)
    D=D.dropna(subset=["prod","ab"])
    out={}
    def tab(g):
        return g.ab.agg(["mean","count"]).assign(t=g.ab.mean()/(g.ab.std()/np.sqrt(g.ab.count())) if False else np.nan)
    def summ(df,key):
        g=df.groupby(key).ab
        r=pd.DataFrame({"mean%":g.mean()*100,"n":g.count(),"t":g.mean()/(g.std()/np.sqrt(g.count()))})
        return r.round(3)
    D["pq"]=pd.qcut(D["prod"],10,labels=False)
    out["prod decile x inprofile"]=summ(D,["inprof","pq"])
    D["wq"]=pd.qcut(D["wid"],5,labels=False)
    D["lq"]=pd.cut(D["loc"],[0,.2,.4,.6,.8,1.0001],include_lowest=True,labels=False)
    out["wide x loc, all bars"]=summ(D,["wq","lq"])
    out["wide x loc, inprofile"]=summ(D[D.inprof],["wq","lq"])
    D["rq"]=pd.qcut(D["r0s"],10,labels=False)
    out["scaled ret decile"]=summ(D,["rq"])
    D["wd"]=D.ts.dt.weekday
    out["weekday"]=summ(D,["wd"])
    D["yr"]=D.ts.dt.year
    out["corr prod nxt by inprof"]=D.groupby("inprof").apply(lambda g: pd.Series(stats.spearmanr(g["prod"],g.ab)[:2],index=["rho","p"])).round(4)
    return out
