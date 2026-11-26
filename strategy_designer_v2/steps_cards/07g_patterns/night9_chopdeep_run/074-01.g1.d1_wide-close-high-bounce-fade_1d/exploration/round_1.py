def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].astype(float); allr.append((c.shift(-1)/c-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            rng=(h-l)/c.shift(1)
            d=pd.DataFrame({
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r1":c/c.shift(1)-1,
                "width":(h-l)/(h-l).rolling(20).mean(),
                "loc":(c-l)/(h-l).replace(0,np.nan),
                "nxt":c.shift(-1)/c-1,
                "nxt2":c.shift(-2)/c.shift(-1)-1,
                "r60":c/c.shift(60)-1,
                "inprof":(b["regime"]!="chop"),
                "regime":b["regime"],
                "alloc":b["postRebalance_current_allocation"].astype(float),
            })
            d["ex"]=d["nxt"]-mu; d["ex2"]=d["nxt2"]-mu
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["r1","width","loc","nxt"])
    D["wd"]=D["day"].dt.weekday
    def st(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"days":0,"mean":np.nan,"t":np.nan})
        s=g.groupby("day")[col].apply(lambda x:(x).sum())
        m=g[col].mean()
        dev=g.assign(dv=g[col]-m).groupby("day")["dv"].sum()
        D_=len(dev); se=np.sqrt((dev**2).sum()*D_/(D_-1))/len(g)
        return pd.Series({"n":len(g),"days":D_,"mean":m,"t":m/se})
    out={}
    D["up"]=D["r1"]>0
    D["wide"]=D["width"]>1
    D["hi"]=D["loc"]>0.5
    D["trend"]=np.where(D["r60"].isna(),"na",np.where(D["r60"]>0.1,"rising",np.where(D["r60"]<-0.1,"falling","choppy")))
    out["cells_inprof"]=D[D.inprof].groupby(["up","wide","hi"]).apply(st)
    out["cells_outprof_by_trend"]=D[~D.inprof].groupby(["trend","up","wide","hi"]).apply(st)
    out["inprof_wideup_hi_width_q"]=D[D.inprof&D.up&D.hi&D.wide].assign(q=lambda x:pd.qcut(x.width,3,labels=False)).groupby("q").apply(st)
    out["inprof_widedown_width_q"]=D[D.inprof&~D.up&D.wide].assign(q=lambda x:pd.qcut(x.width,3,labels=False)).groupby("q").apply(st)
    out["all_wideup_hi_day2"]=D[D.up&D.hi&D.wide].groupby("inprof").apply(lambda g:st(g,"ex2"))
    out["inprof_weekday"]=D[D.inprof].groupby("wd").apply(st)
    out["all_weekday"]=D.groupby("wd").apply(st)
    D["absr"]=pd.qcut(D["r1"],5,labels=False)
    out["r1_quintile_inprof"]=D[D.inprof].groupby("absr").apply(st)
    out["r1_quintile_outprof"]=D[~D.inprof].groupby("absr").apply(st)
    out["regime_share"]=D["regime"].value_counts()
    return out
