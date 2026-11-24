def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            if len(b)<30: continue
            c=b["close"]; o=b["open"]; h=b["high"]; l=b["low"]
            rng=(h-l)/c
            rm=(h-l)/(h-l).rolling(20,min_periods=10).mean().shift(1)
            ret5=c/c.shift(5)-1
            ret1=c/c.shift(1)-1
            ret20=c/c.shift(20)-1
            vol20=ret1.rolling(20,min_periods=10).std()
            body=(c-o)/(h-l).replace(0,np.nan)
            clv=((c-l)/(h-l).replace(0,np.nan))
            fwd3=c.shift(-3)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),
                "wd":ts.dt.dayofweek,"year":ts.dt.year,"rm":rm,"ret5":ret5,"ret1":ret1,"ret20":ret20,
                "vol20":vol20,"body":body,"clv":clv,"fwd3":fwd3,"fwd1":fwd1,"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%3==0)&D.fwd3.notna()].copy()
    drift=G.groupby("coin").fwd3.mean(); sd=G.groupby("coin").fwd3.std()
    G["ex"]=G.fwd3-G.coin.map(drift)
    G["z"]=G.ex/G.coin.map(sd)
    def summ(g):
        dm=g.groupby("day").ex.sum()
        n=len(g); m=g.ex.mean()
        se=np.sqrt((dm**2).sum())/n if n>1 else np.nan  # day-clustered se of mean around 0 approx
        dd=g.ex-m; dsum=dd.groupby(g.day).sum(); se=np.sqrt((dsum**2).sum())/n
        return pd.Series({"n":n,"days":g.day.nunique(),"mean_ex%":100*m,"t":m/se if se>0 else np.nan,"strength":g.z.mean()})
    out={}
    G["rmq"]=pd.qcut(G.rm,5,labels=False)
    G["r5q"]=pd.qcut(G.ret5,5,labels=False)
    out["by ret5 quintile"]=G.groupby("r5q").apply(summ)
    out["by range-mult quintile"]=G.groupby("rmq").apply(summ)
    up=G[G.ret5>0].copy()
    up["absbody"]=up.body.abs()
    up["bq"]=pd.qcut(up.absbody,3,labels=["flat","mid","big"])
    up["rq"]=pd.qcut(up.rm,3,labels=["narrow","mid","wide"])
    out["up-run: rangemult x body"]=up.groupby(["rq","bq"]).apply(summ)
    up["clvq"]=pd.qcut(up.clv,3,labels=["closeLow","mid","closeHigh"])
    out["up-run wide: by close location"]=up[up.rq=="wide"].groupby("clvq").apply(summ)
    dn=G[G.ret5<0].copy(); dn["rq"]=pd.qcut(dn.rm,3,labels=["narrow","mid","wide"])
    out["down-run by rangemult"]=dn.groupby("rq").apply(summ)
    G["vq"]=G.groupby("coin").vol20.transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["by vol tercile (coin-rel)"]=G.groupby("vq").apply(summ)
    G["r20q"]=pd.qcut(G.ret20,5,labels=False)
    out["by ret20 quintile"]=G.groupby("r20q").apply(summ)
    out["by weekday"]=G.groupby("wd").apply(summ)
    out["by year"]=G.groupby("year").apply(summ)
    G["fcq"]=pd.cut(G.fc,[-0.01,0.0001,5,10,15,20.1])
    out["by forecast bin"]=G.groupby("fcq").apply(summ)
    return out
