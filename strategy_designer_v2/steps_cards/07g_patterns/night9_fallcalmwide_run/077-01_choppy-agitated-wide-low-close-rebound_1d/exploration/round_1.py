def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            if len(b)<35: continue
            h,l,c,o=b.high,b.low,b.close,b.open
            rng=(h-l)
            r=c.pct_change()
            s30=r.rolling(30).std()
            mbr=(rng/c).rolling(30).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b.timestamp).dt.normalize(),
                "wd":pd.to_datetime(b.timestamp).dt.weekday,
                "clv":(c-l)/rng.replace(0,np.nan),
                "width":(rng/c)/mbr,
                "wsd":(rng/c)/s30,
                "r0":r,"r0z":r/s30,
                "r5":c/c.shift(5)-1,
                "r20":c/c.shift(20)-1,
                "nxt":c.shift(-1)/c-1,
                "nxt2":c.shift(-2)/c-1,
                "regime":b.regime,"alloc":b.postRebalance_current_allocation})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["clv","width","nxt"])
    mu=d.groupby("coin").nxt.mean()
    d["ex"]=d.nxt-d.coin.map(mu)
    d["inprof"]=d.regime!="chop"
    def summ(g):
        dd=g.groupby("day").ex.sum(); n=len(g)
        t=g.ex.mean()/ (dd.std(ddof=1)*np.sqrt(len(dd))/n) if len(dd)>2 else np.nan
        return pd.Series({"n":n,"mean_ex":g.ex.mean(),"t":t})
    d["clvq"]=pd.cut(d.clv,[-.01,.25,.5,.75,1.01],labels=["low","ml","mh","high"])
    d["widq"]=pd.cut(d.width,[0,.7,1,1.5,99],labels=["narrow","mid","wide","vwide"])
    out={}
    out["regime counts"]=d.regime.value_counts()
    out["inprof clv x width"]=d[d.inprof].groupby(["clvq","widq"]).apply(summ).reset_index()
    out["outprof clv x width"]=d[~d.inprof].groupby(["clvq","widq"]).apply(summ).reset_index()
    d["r0q"]=pd.qcut(d.r0z,5,labels=False)
    out["all by r0z quintile"]=d.groupby("r0q").apply(summ)
    out["inprof by r0z quintile"]=d[d.inprof].groupby("r0q").apply(summ)
    out["weekday all"]=d.groupby("wd").apply(summ)
    d["r20q"]=pd.qcut(d.r20,5,labels=False)
    out["r20 quintile all"]=d.dropna(subset=["r20"]).groupby("r20q").apply(summ)
    d["r5q"]=pd.qcut(d.r5,5,labels=False)
    out["r5 quintile all"]=d.dropna(subset=["r5"]).groupby("r5q").apply(summ)
    out["year mean_ex wide high clv all"]=d[(d.clvq=="high")&(d.width>=1)].assign(y=d.day.dt.year).groupby("y").apply(summ)
    out["year wide low clv all"]=d[(d.clvq=="low")&(d.width>=1)].assign(y=d.day.dt.year).groupby("y").apply(summ)
    return out
