def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([b["close"].pct_change().dropna() for b in ws.values()])
        mu=allr.mean()
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            rng=b["high"]-b["low"]
            b["rm"]=rng/rng.rolling(20,min_periods=20).mean()
            b["cl"]=(b["close"]-b["low"])/rng.replace(0,np.nan)
            b["r1"]=b["close"].pct_change()
            b["f1"]=b["close"].shift(-1)/b["close"]-1-mu
            b["vol"]=b["r1"].rolling(20).std()
            b["vol60"]=b["r1"].rolling(60).std()
            b["vr"]=b["vol"]/b["vol60"]
            ts=pd.to_datetime(b["timestamp"])
            b["day"]=ts.dt.floor("D"); b["yr"]=ts.dt.year
            b["coin"]=coin;b["w"]=w
            b["bret"]=b["postRebalance_total_value"].pct_change().shift(-1)
            rows.append(b)
    d=pd.concat(rows).dropna(subset=["f1","rm","cl","vol"])
    d["vb"]=d.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,3,labels=False))
    def st(g,col="f1"):
        g=g.dropna(subset=[col]); s=g.groupby("day")[col].sum()
        if len(s)<3: return pd.Series({"n":len(g),"days":len(s),"mean":np.nan,"t":np.nan})
        return pd.Series({"n":len(g),"days":len(s),"mean":g[col].mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out={}
    d["clb"]=pd.cut(d["cl"],[-.01,.25,.5,.75,1.01])
    out["all days f1 by vol tercile x closeloc"]=d.groupby(["vb","clb"]).apply(st).reset_index()
    low=d[d.cl<=.25]
    out["lowclose f1 by vol tercile x rangemult>=1.5"]=low.assign(wide=low.rm>=1.5).groupby(["vb","wide"]).apply(st).reset_index()
    wl=d[(d.rm>=1.5)&(d.cl<=.25)]
    out["wide-low f1 by year x hi-vol"]=wl.assign(hv=wl.vb==2).groupby(["yr","hv"]).apply(st).reset_index()
    out["wide-low f1 by vol tercile, per coin"]=wl.groupby(["coin","vb"])["f1"].mean().unstack()
    # continuous: down days (r1<0), f1 vs (vol * -cl') gradients
    dn=d[d.r1<0]
    out["down days spearman f1 vs vol"]=pd.Series({"rho":stats.spearmanr(dn.vol,dn.f1)[0],"n":len(dn)})
    out["down days spearman f1 vs -cl"]=pd.Series({"rho":stats.spearmanr(-dn.cl,dn.f1)[0]})
    out["down days spearman f1 vs rm"]=pd.Series({"rho":stats.spearmanr(dn.rm,dn.f1)[0]})
    dn=dn.assign(volq=dn.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,5,labels=False)))
    out["down lowclose f1 by vol quintile"]=dn[dn.cl<=.25].groupby("volq").apply(st).reset_index()
    out["wide-low f1 by vol20/vol60 tercile"]=wl.assign(q=pd.qcut(wl.vr,3,labels=False)).groupby("q").apply(st).reset_index()
    ac=d[d.postRebalance_current_allocation.abs()>0].dropna(subset=["bret"])
    out["held bars: book bar return by vol tercile"]=ac.groupby("vb")["bret"].agg(["count","mean","sum"])
    return out
