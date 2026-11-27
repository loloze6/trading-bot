def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change()
            allr.append(r.dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change()
            sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({
                "coin":coin,"win":w,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "fc":b["regime"].astype(str).eq("unknown"),
                "rng":(b["high"]-b["low"])/b["close"]/sd,
                "clv":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "r0":r/sd,
                "nx":b["close"].shift(-1)/b["close"]-1,
                "nx3":b["close"].shift(-3)/b["close"]-1,
                "pos":b["postRebalance_current_allocation"],
                "fcst":b["forecast"],
            })
            d["ex"]=d["nx"]-mu
            d["ex3"]=d["nx3"]-3*mu
            d["pnl"]=d["pos"]*d["nx"]
            d["idx"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def st(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan,"days":0})
        m=g[col].mean()
        s=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n":len(g),"mean%":100*m,"t":m/se if se>0 else np.nan,"days":s.size})
    out={}
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    D["rngq"]=pd.qcut(D["rng"],5,labels=False)
    D["r0q"]=pd.qcut(D["r0"],5,labels=False)
    out["clv quintile, all"]=D.groupby("clvq").apply(st)
    out["clv quintile, falling calm"]=D[D.fc].groupby("clvq").apply(st)
    out["clv quintile, other"]=D[~D.fc].groupby("clvq").apply(st)
    out["range quintile, all"]=D.groupby("rngq").apply(st)
    out["range q x top clv (q4), all"]=D[D.clvq==4].groupby("rngq").apply(st)
    out["range q x bottom clv (q0), all"]=D[D.clvq==0].groupby("rngq").apply(st)
    out["r0 quintile (day ret/std), all"]=D.groupby("r0q").apply(st)
    out["r0 quintile, falling calm"]=D[D.fc].groupby("r0q").apply(st)
    out["r0 quintile, other"]=D[~D.fc].groupby("r0q").apply(st)
    out["weekday all"]=D.groupby("wd").apply(st)
    D3=D[D.idx%3==0]
    out["r0 quintile 3d ex (grid), all"]=D3.groupby("r0q").apply(lambda g: st(g,"ex3"))
    out["fc share"]=float(D.fc.mean())
    P=D[D.pos.fillna(0)!=0]
    out["book pos: pnl by clvq"]=P.groupby("clvq").apply(lambda g: st(g,"pnl"))
    out["book pos: pnl by rngq"]=P.groupby("rngq").apply(lambda g: st(g,"pnl"))
    out["pos long share"]=float((P.pos>0).mean())
    return out
