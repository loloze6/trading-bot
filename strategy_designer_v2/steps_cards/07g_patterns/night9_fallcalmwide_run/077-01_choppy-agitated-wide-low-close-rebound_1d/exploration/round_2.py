def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            if len(b)<35: continue
            h,l,c=b.high,b.low,b.close
            rng=(h-l)
            r=c.pct_change()
            s30=r.rolling(30).std()
            mbr=(rng/c).rolling(30).mean()
            ts=pd.to_datetime(b.timestamp)
            df=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.normalize(),
                "wd":ts.dt.weekday,"y":ts.dt.year,
                "clv":(c-l)/rng.replace(0,np.nan),
                "width":(rng/c)/mbr,
                "r0z":r/s30,
                "r5":c/c.shift(5)-1,
                "r20":c/c.shift(20)-1,
                "vol":s30,
                "nxt":c.shift(-1)/c-1,
                "nxt2":c.shift(-2)/c-1,
                "regime":b.regime.astype(str)})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True).dropna(subset=["clv","width","nxt","r0z"]).reset_index(drop=True)
    mu=d.groupby("coin").nxt.mean()
    d["ex"]=d.nxt-d.coin.map(mu)
    mu2=d.groupby("coin").nxt2.mean()
    d["ex2"]=d.nxt2-d.coin.map(mu2)
    d["inprof"]=d.regime!="chop"
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        n=len(g)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan})
        dd=g.groupby("day")[col].sum()
        se=dd.std(ddof=1)*np.sqrt(len(dd))/n
        return pd.Series({"n":n,"days":len(dd),"mean":g[col].mean(),"t":g[col].mean()/se})
    d["clvq"]=pd.cut(d.clv,[-.01,.25,.5,.75,1.01],labels=["low","ml","mh","high"])
    d["widq"]=pd.cut(d.width,[0,.7,1,1.5,99],labels=["narrow","mid","wide","vwide"])
    out={}
    out["regime counts"]=d.regime.value_counts()
    out["inprof clv x width"]=d[d.inprof].groupby(["clvq","widq"],observed=True).apply(summ).reset_index()
    out["outprof clv x width"]=d[~d.inprof].groupby(["clvq","widq"],observed=True).apply(summ).reset_index()
    out["outprof clv x width ex2"]=d[~d.inprof].groupby(["clvq","widq"],observed=True).apply(lambda g:summ(g,"ex2")).reset_index()
    d["r0q"]=pd.qcut(d.r0z,5,labels=False)
    out["all by r0z quintile"]=d.groupby("r0q").apply(summ)
    out["inprof by r0z quintile"]=d[d.inprof].groupby("r0q").apply(summ)
    out["weekday all"]=d.groupby("wd").apply(summ)
    e=d.dropna(subset=["r20"]).copy(); e["q"]=pd.qcut(e.r20,5,labels=False)
    out["r20 quintile all"]=e.groupby("q").apply(summ)
    e=d.dropna(subset=["r5"]).copy(); e["q"]=pd.qcut(e.r5,5,labels=False)
    out["r5 quintile all"]=e.groupby("q").apply(summ)
    out["r5 quintile ex2"]=e.groupby("q").apply(lambda g:summ(g,"ex2"))
    e=d.dropna(subset=["vol"]).copy(); e["q"]=e.groupby("coin").vol.transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
    out["vol tercile x clvq wide"]=e[e.width>=1].groupby(["q","clvq"],observed=True).apply(summ).reset_index()
    out["year wide high clv"]=d[(d.clvq=="high")&(d.width>=1)].groupby("y").apply(summ)
    out["year wide low clv"]=d[(d.clvq=="low")&(d.width>=1)].groupby("y").apply(summ)
    return out
