def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            r=b["close"].pct_change()
            b["ret"]=r
            b["std30"]=r.rolling(30,min_periods=20).std()
            b["width"]=(b["high"]-b["low"])/b["close"]/b["std30"]
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["high"]-b["close"])/rng
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["tr60"]=b["close"]/b["close"].shift(60)-1
            b["inprof"]=(b["regime"]!="chop")
            b["coin"]=coin; b["w"]=w
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["rz"]=r/b["std30"]
            b["vr"]=b["std30"]/r.rolling(90,min_periods=60).std()
            b["alloc"]=b["postRebalance_current_allocation"]
            rows.append(b)
    d=pd.concat(rows)
    drift=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(drift)
    d["z"]=d["ex"]/d.groupby("coin")["nxt"].transform("std")
    d=d.dropna(subset=["width","loc","nxt"])
    d["sig"]=(d["loc"]-0.5)*d["width"]   # + = wide low close, - = wide high close
    def summ(g,col="z"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g)})
        s=g.groupby("day")[col].sum(); G=len(s)
        t=g[col].mean()/(np.sqrt((s**2).sum()*G/(G-1))/len(g))
        return pd.Series({"n":len(g),"days":G,"mean":g[col].mean(),"t":t})
    def slope(g,x):
        g=g.dropna(subset=[x,"z"])
        X=g[x]-g[x].mean(); y=g["z"]
        b=(X*y).sum()/(X**2).sum()
        e=y-y.mean()-b*X
        s=(X*e).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/(X**2).sum()
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"slope":b,"t":b/se})
    out={}
    out["inprof wide>=2 by loc"]=d[d.inprof&(d.width>=2)].groupby(pd.cut(d["loc"],[-0.01,0.2,0.5,0.8,1.01])).apply(summ)
    d["trb"]=pd.cut(d["tr60"],[-10,-0.1,0.1,100],labels=["fall","chop","rise"])
    d["vb"]=pd.cut(d["vr"],[0,1,100],labels=["calm","agit"])
    out["slope sig by trend x volratio"]=d.groupby(["trb","vb"]).apply(lambda g:slope(g,"sig"))
    out["slope sig by inprof"]=d.groupby("inprof").apply(lambda g:slope(g,"sig"))
    out["slope sig all"]=slope(d,"sig")
    out["slope rz by trend x vr"]=d.groupby(["trb","vb"]).apply(lambda g:slope(g,"rz"))
    big=d[d["width"]>=2]
    out["wide>=2 sig slope by window"]=big.groupby("w").apply(lambda g:slope(g,"sig"))
    out["wide>=2 sig slope by coin"]=big.groupby("coin").apply(lambda g:slope(g,"sig"))
    out["outprof wide>=2 high close (loc<0.2) by trend"]=d[(~d.inprof)&(d.width>=2)&(d["loc"]<0.2)].groupby("trb").apply(summ)
    return out
