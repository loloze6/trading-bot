def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            r=b["close"].pct_change()
            b["ret"]=r
            b["std30"]=r.rolling(30,min_periods=20).std()
            b["width"]=(b["high"]-b["low"])/b["close"]/b["std30"]
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["high"]-b["close"])/rng  # 1 = close at low
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["nxt3"]=b["close"].shift(-3)/b["close"]-1
            b["tr60"]=b["close"]/b["close"].shift(60)-1
            b["inprof"]=(b["regime"]!="chop")
            b["dow"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d=pd.concat(rows)
    drift=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(drift)
    d["std1"]=d.groupby("coin")["nxt"].transform("std")
    d["z"]=d["ex"]/d["std1"]
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g)})
        s=g.groupby("day")[col].sum(); G=len(s)
        t=g[col].mean()/(np.sqrt((s**2).sum()*G/(G-1))/len(g)) if G>1 else np.nan
        return pd.Series({"n":len(g),"days":G,"mean":g[col].mean(),"t":t})
    out={}
    d2=d.dropna(subset=["width","loc","nxt"])
    d2["wb"]=pd.cut(d2["width"],[0,1,1.5,2,3,5,100])
    d2["lb"]=pd.cut(d2["loc"],[-0.01,0.2,0.5,0.8,1.01])
    out["in_profile width x loc (z)"]=d2[d2.inprof].groupby(["wb","lb"]).apply(lambda g:summ(g,"z")).reset_index()
    out["out_profile width x loc (z)"]=d2[~d2.inprof].groupby(["wb","lb"]).apply(lambda g:summ(g,"z")).reset_index()
    # large moves
    d2["rz"]=d2["ret"]/d2["std30"]
    d2["rb"]=pd.cut(d2["rz"],[-100,-3,-2,-1,0,1,2,3,100])
    out["by prior-day return z, all"]=d2.groupby("rb").apply(lambda g:summ(g,"z")).reset_index()
    out["by prior-day return z, in profile"]=d2[d2.inprof].groupby("rb").apply(lambda g:summ(g,"z")).reset_index()
    out["by weekday all"]=d2.groupby("dow").apply(lambda g:summ(g,"z")).reset_index()
    d2["trb"]=pd.cut(d2["tr60"],[-10,-0.3,-0.1,0.1,0.3,0.6,100])
    out["by 60d trend all"]=d2.groupby("trb").apply(lambda g:summ(g,"z")).reset_index()
    out["regime counts"]=d["regime"].value_counts()
    # 3-day after wide low close in profile
    sel=d2[d2.inprof&(d2.width>=2)&(d2["loc"]>0.5)]
    out["3d ex after situation"]=pd.Series({"mean3":(sel["nxt3"]).mean(),"n":sel["nxt3"].notna().sum(),"mean1":sel["nxt"].mean()})
    return out
