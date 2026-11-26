def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            sd20=r1.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"fc":b["forecast"].astype(float),"f5":c.shift(-5)/c-1,
                "sc":(c/c.shift(20)-1)/sd20,"r60":c/c.shift(60)-1,"sd30":r1.rolling(30).std(),
                "r1z":r1/sd20.shift(1),"pos":np.arange(len(b)),"yr":ts.dt.year,"day":ts.dt.floor("D"),
                "alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A.pos%5==0)&A.f5.notna()].copy()
    G["ex"]=G.f5-G.groupby("coin").f5.transform("mean")
    # agitation proxy: sd30 vs trailing-365 median within window can't; use coin-level expanding rank within data
    G["volr"]=G.sd30/G.groupby("coin").sd30.transform("median")
    G["calm"]=G.volr<=1
    out={}
    def slope(g,x="fc"):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g.ex); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    def daysure(g,x="fc"):
        g=g.dropna(subset=[x,"ex"]); g=g[g[x]!=0]
        v=np.sign(g[x])*g.ex; s=v.groupby(g.day).sum()
        return pd.Series({"cases":len(g),"days":len(s),"mean_signed%":100*v.mean(),"t_day":s.mean()/(s.std()/np.sqrt(len(s)))})
    C=G[G.calm]; Ag=G[~G.calm]
    out["calm daysure"]=daysure(C); out["agit daysure"]=daysure(Ag)
    out["calm slope by year"]=C.groupby("yr").apply(slope)
    out["agit slope by year"]=Ag.groupby("yr").apply(slope)
    out["calm slope by coin"]=C.groupby("coin").apply(slope)
    C=C.copy(); C["fq"]=pd.qcut(C.fc.rank(method="first"),5,labels=False)
    out["calm fc quintile ex5%"]=C.groupby("fq").ex.agg(["size",lambda s:100*s.mean(),lambda s:s.mean()/(s.std()/np.sqrt(len(s)))])
    out["calm slope by side"]=C.groupby(np.sign(C.fc)).apply(slope)
    # graded: slope of ex on fc scaled by calmness
    G["fc_calm"]=G.fc*(1/G.volr)
    out["slope fc/volr all"]=slope(G,"fc_calm"); out["slope fc all"]=slope(G,"fc")
    # 1d z move continuation
    G["zq"]=pd.qcut(G.r1z.rank(method="first"),5,labels=False)
    out["r1z slope by year"]=G.groupby("yr").apply(lambda g: slope(g,"r1z"))
    out["r1z slope calm/agit"]=G.groupby("calm").apply(lambda g: slope(g,"r1z"))
    out["r1z slope ctrl fc"]=pd.Series(dict(zip(["b_fc","b_r1z"],np.linalg.lstsq(np.c_[np.ones(len(G.dropna(subset=['fc','r1z','ex']))),G.dropna(subset=['fc','r1z','ex'])[['fc','r1z']].values],G.dropna(subset=['fc','r1z','ex']).ex.values,rcond=None)[0][1:])))
    # book by calm
    A["volr"]=A.sd30/A.groupby("coin").sd30.transform("median")
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D); D["day"]=pd.to_datetime(D["day"])
    m=D.merge(A[["coin","w","day","volr"]].drop_duplicates(["coin","w","day"]),on=["coin","w","day"],how="left")
    m["calm"]=m.volr<=1
    out["book by calm (coin-days)"]=m.dropna(subset=["book_return"]).groupby("calm").agg(n=("book_return","size"),
        book_pct=("book_return",lambda s:100*s.mean()),hold_pct=("coin_return",lambda s:100*s.mean()),
        t=("book_return",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    return out
