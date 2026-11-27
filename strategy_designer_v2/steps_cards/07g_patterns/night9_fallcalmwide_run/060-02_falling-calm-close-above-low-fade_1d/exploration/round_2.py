def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change()
            sd=r.rolling(30,min_periods=20).std()
            sdl=r.rolling(90,min_periods=60).std()
            d=pd.DataFrame({
                "coin":coin,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "fc":b["regime"].astype(str).eq("unknown"),
                "rng":(b["high"]-b["low"])/b["close"]/sd,
                "clv":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "r0":r/sd,
                "tr":(b["close"]/b["close"].shift(60)-1)*100,
                "agi":sd>sdl,
                "nx":b["close"].shift(-1)/b["close"]-1,
                "nx2":b["close"].shift(-2)/b["close"]-1,
                "pos":b["postRebalance_current_allocation"],
            })
            d["ex"]=d["nx"]-mu
            d["ex2"]=d["nx2"]-2*mu
            d["idx"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def st(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan,"days":0})
        m=g[col].mean(); s=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n":len(g),"mean%":100*m,"t":m/se if se>0 else np.nan,"days":s.size})
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    D["rngq"]=pd.qcut(D["rng"],5,labels=False)
    D["trg"]=pd.cut(D["tr"],[-1e9,-10,10,1e9],labels=["falling","choppy","rising"])
    D["prof"]=D["trg"].astype(str)+"_"+np.where(D["agi"],"agi","calm")
    D=D[D.tr.notna()&D.agi.notna()]
    out={}
    out["profile counts"]=D["prof"].value_counts()
    out["clvq4 by profile"]=D[D.clvq==4].groupby("prof").apply(st)
    out["clvq0 by profile"]=D[D.clvq==0].groupby("prof").apply(st)
    # graded: high close x wide, by profile
    H=D[(D.clvq==4)&(D.rngq>=3)]
    out["wide high close by profile"]=H.groupby("prof").apply(st)
    out["wide high close by profile 2d grid"]=D[(D.clvq==4)&(D.rngq>=3)&(D.idx%2==0)].groupby("prof").apply(lambda g: st(g,"ex2"))
    # correlation of score clv*rng with ex in choppy agitated / falling agitated
    res={}
    for p,g in D.groupby("prof"):
        g=g.dropna(subset=["ex","clv","rng"])
        sc=(g.clv-0.5)*g.rng
        dd=pd.DataFrame({"sc":sc,"ex":g.ex,"day":g.day}).groupby("day").mean()
        r=dd.sc.corr(dd.ex); n=len(dd)
        res[p]=pd.Series({"days":n,"r":r,"t":r*np.sqrt(n-2)/np.sqrt(1-r*r)})
    out["corr (clv-0.5)*range vs next ex, by profile (day means)"]=pd.DataFrame(res).T
    out["clvq4 by year"]=D[D.clvq==4].groupby("yr").apply(st)
    out["clvq4 falling calm 2d grid"]=D[(D.clvq==4)&D.fc&(D.idx%2==0)].groupby("rngq").apply(lambda g: st(g,"ex2"))
    return out
