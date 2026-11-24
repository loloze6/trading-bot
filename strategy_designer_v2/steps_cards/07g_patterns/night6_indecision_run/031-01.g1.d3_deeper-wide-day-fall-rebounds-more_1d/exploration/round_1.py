def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values; allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            rng=b["high"]-b["low"]
            b["rm"]=rng/rng.rolling(20,min_periods=20).mean()
            b["cl"]=(b["close"]-b["low"])/rng.replace(0,np.nan)
            b["r1"]=b["close"].pct_change()
            b["r5"]=b["close"]/b["close"].shift(5)-1
            b["f1"]=b["close"].shift(-1)/b["close"]-1-mu
            b["f3"]=b["close"].shift(-3)/b["close"]-1-3*mu
            b["vol"]=b["r1"].rolling(20).std()
            b["z"]=(b["r1"]-b["r1"].rolling(60,min_periods=20).mean())/b["r1"].rolling(60,min_periods=20).std()
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["pos"]=b["postRebalance_current_allocation"]
            b["coin"]=coin;b["w"]=w
            b["g3"]=(np.arange(len(b))%3==0)
            rows.append(b)
    d=pd.concat(rows)
    def st(g,col="f1"):
        g=g.dropna(subset=[col])
        s=g.groupby("day")[col].sum()
        n=len(g)
        if len(s)<3: return pd.Series({"n":n,"mean":np.nan,"t":np.nan})
        return pd.Series({"n":n,"days":len(s),"mean":g[col].mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    d["rmb"]=pd.cut(d["rm"],[0,0.7,1,1.5,2,3,99])
    d["clb"]=pd.cut(d["cl"],[-.01,.25,.5,.75,1.01])
    out={}
    out["f1 by rangemult x closeloc"]=d.groupby(["rmb","clb"]).apply(st).reset_index()
    d["zb"]=pd.cut(d["z"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["f1 by z of day return"]=d.groupby("zb").apply(st).reset_index()
    wl=d[(d.rm>=1.5)&(d.cl<=.25)]
    out["wide-low f1 by z"]=wl.groupby("zb").apply(st).reset_index()
    out["wide-low f3 (grid) by z"]=wl[wl.g3].groupby("zb").apply(lambda g:st(g,"f3")).reset_index()
    d["r5b"]=pd.qcut(d["r5"],5)
    out["wide-low f1 by prior 5d ret quint"]=wl.assign(r5b=pd.qcut(wl["r5"],4)).groupby("r5b").apply(st).reset_index()
    d["vb"]=d.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,3,labels=False))
    out["wide-low f1 by vol tercile"]=d[(d.rm>=1.5)&(d.cl<=.25)].groupby("vb").apply(st).reset_index()
    out["all f1 by weekday"]=d.groupby("wd").apply(st).reset_index()
    out["wide-low f1 by coin"]=wl.groupby("coin").apply(st).reset_index()
    wh=d[(d.rm>=1.5)&(d.cl>=.75)]
    out["wide-high f1 by z"]=wh.groupby("zb").apply(st).reset_index()
    return out
