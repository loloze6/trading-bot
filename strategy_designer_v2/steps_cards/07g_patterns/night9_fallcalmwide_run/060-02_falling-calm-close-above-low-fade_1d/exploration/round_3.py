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
                "coin":coin,"win":w,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "rng":(b["high"]-b["low"])/b["close"]/sd,
                "clv":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "tr":(b["close"]/b["close"].shift(60)-1)*100,
                "agi":sd>sdl,
                "nx":b["close"].shift(-1)/b["close"]-1,
                "nx2":b["close"].shift(-2)/b["close"]-1,
            })
            d["ex"]=d["nx"]-mu; d["ex2"]=d["nx2"]-2*mu
            d["idx"]=np.arange(len(d))
            d=d[d.tr.notna()&sdl.notna()]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["trg"]=pd.cut(D["tr"],[-1e9,-10,10,1e9],labels=["falling","choppy","rising"])
    D["prof"]=D["trg"].astype(str)+"_"+np.where(D["agi"],"agi","calm")
    def cor(g,col="ex"):
        g=g.dropna(subset=[col,"clv","rng"])
        if len(g)<20: return pd.Series({"n":len(g),"days":np.nan,"r":np.nan,"t":np.nan})
        sc=(g.clv-0.5)*g.rng
        dd=pd.DataFrame({"sc":sc,"ex":g[col],"day":g.day}).groupby("day").mean()
        r=dd.sc.corr(dd.ex); n=len(dd)
        return pd.Series({"n":len(g),"days":n,"r":r,"t":r*np.sqrt(n-2)/np.sqrt(1-r*r)})
    def st(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan,"days":0})
        m=g[col].mean(); s=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n":len(g),"mean%":100*m,"t":m/se if se>0 else np.nan,"days":s.size})
    out={}
    A=D[D.prof.isin(["choppy_agi","falling_agi"])]
    out["agi profiles: high half clv>0.5"]=A[A.clv>0.5].groupby("prof").apply(cor)
    out["agi profiles: low half clv<=0.5"]=A[A.clv<=0.5].groupby("prof").apply(cor)
    out["choppy_agi by year"]=D[D.prof=="choppy_agi"].groupby("yr").apply(cor)
    out["falling_agi by year"]=D[D.prof=="falling_agi"].groupby("yr").apply(cor)
    out["agi profiles 2d grid"]=D[(D.idx%2==0)].groupby("prof").apply(lambda g: cor(g,"ex2"))
    C=D[(D.prof=="choppy_agi")&(D.clv>0.5)].copy()
    C["sq"]=pd.qcut((C.clv-0.5)*C.rng,3,labels=False)
    out["choppy_agi high half, score tercile"]=C.groupby("sq").apply(st)
    out["choppy_agi coins"]=D[D.prof=="choppy_agi"].groupby("coin").size()
    return out
