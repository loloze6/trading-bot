def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];o=b["open"];h=b["high"];l=b["low"];v=b["volume"]
            d=pd.DataFrame({"coin":coin,"win":w})
            d["ret1"]=c.pct_change()
            d["ret3"]=c/c.shift(3)-1
            d["vr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            rng=(h-l).replace(0,np.nan)
            d["clv"]=(c-l)/rng
            d["lwick"]=(np.minimum(o,c)-l)/rng
            d["uwick"]=(h-np.maximum(o,c))/rng
            d["vol20"]=d["ret1"].rolling(20,min_periods=20).std()
            d["nxt"]=c.shift(-1)/c-1
            d["nxt2"]=c.shift(-2)/c.shift(-1)-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["fc"]=b["forecast"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["ret1"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D["ex2"]=D["nxt2"]-D["coin"].map(mu)
    D=D.dropna(subset=["ex","ret1","vr","vol20"])
    def st(g,col="ex"):
        x=g[col].dropna();n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["rq"]=pd.qcut(D.groupby("coin")["ret1"].rank(pct=True),5,labels=["r1low","r2","r3","r4","r5high"])
    D["heavy"]=np.where(D["vr"]>=1,"heavy","light")
    out["ret quintile x volume"]=D.groupby(["rq","heavy"]).apply(st)
    dn=D[D.ret1<0]
    dn=dn.assign(clvb=pd.cut(dn.clv,[0,0.33,0.66,1.0001],include_lowest=True,labels=["lowclose","mid","highclose"]))
    out["down days clv x volume"]=dn.groupby(["clvb","heavy"]).apply(st)
    up=D[D.ret1>=0]
    up=up.assign(clvb=pd.cut(up.clv,[0,0.33,0.66,1.0001],include_lowest=True,labels=["lowclose","mid","highclose"]))
    out["up days clv x volume"]=up.groupby(["clvb","heavy"]).apply(st)
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=["lowvol","midvol","highvol"]))
    out["bottom ret quintile x vol tercile"]=D[D.rq=="r1low"].groupby(["volq","heavy"]).apply(st)
    out["top ret quintile x vol tercile"]=D[D.rq=="r5high"].groupby(["volq","heavy"]).apply(st)
    out["active bars day2 excess"]=st(D[D.fc>0],"ex2")
    out["weekday all"]=D.groupby("wd").apply(st)
    out["weekday active"]=D[D.fc>0].groupby("wd").apply(st)
    D["r3q"]=pd.qcut(D.groupby("coin")["ret3"].rank(pct=True),5,labels=["a","b","c","d","e"])
    out["3d ret quintile"]=D.groupby("r3q").apply(st)
    dn2=dn.assign(lw=pd.qcut(dn.lwick.rank(method="first"),3,labels=["smallwick","mid","bigwick"]))
    out["down days lower wick"]=dn2.groupby(["lw","heavy"]).apply(st)
    out["active by coin"]=D[D.fc>0].groupby("coin").apply(st)
    out["active by year"]=D[D.fc>0].groupby("yr").apply(st)
    out["light down days by coin bottom quintile"]=D[(D.rq=="r1low")&(D.heavy=="light")].groupby("coin").apply(st)
    return out
