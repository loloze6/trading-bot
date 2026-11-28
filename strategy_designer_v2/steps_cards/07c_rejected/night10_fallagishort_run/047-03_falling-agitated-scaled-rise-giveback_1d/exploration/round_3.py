def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change(); sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"prof":(b["regime"]=="unknown"),"r":r,"z":r/sd,
                "rng":(h-l)/c.shift(1)/sd,"dd30":c/c.rolling(30,min_periods=10).max()-1,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in [1,2,3]:
        dr=D.groupby("coin")[f"f{k}"].mean()
        D[f"x{k}"]=D[f"f{k}"]-D["coin"].map(dr)
    U=D[D.prof&(D.z>0)&D.f1.notna()].copy()
    def slope_t(V,v,y):
        V=V[V[v].notna()&V[y].notna()]
        x=V[v]-V[v].mean(); yy=V[y]
        b=(x*yy).sum()/(x**2).sum(); a=yy.mean()-b*V[v].mean()
        e=yy-a-b*V[v]
        s=(x*e).groupby(V["day"]).sum()
        se=np.sqrt((s**2).sum())/(x**2).sum()
        return pd.Series({"n":len(V),"days":V.day.nunique(),"slope":b,"t":b/se})
    out={}
    res={}
    for v in ["z","rng","dd30"]:
        for y in ["x1","x2","x3"]:
            res[f"{v}_{y}"]=slope_t(U,v,y)
    out["up_slopes_dayclustered"]=pd.DataFrame(res).T
    res={}
    for coin,V in U.groupby("coin"):
        for v in ["rng","dd30"]:
            res[f"{coin}_{v}"]=slope_t(V,v,"x1")
    out["up_slopes_by_coin"]=pd.DataFrame(res).T
    q=pd.qcut(U.rng.rank(method="first"),4,labels=False)
    out["up_rng_quart"]=U.groupby(q).agg(n=("x1","size"),rng=("rng","mean"),z=("z","mean"),x1=("x1","mean"),x2=("x2","mean"),x3=("x3","mean"))
    q=pd.qcut(U.dd30.rank(method="first"),4,labels=False)
    out["up_dd30_quart"]=U.groupby(q).agg(n=("x1","size"),dd30=("dd30","mean"),x1=("x1","mean"),x3=("x3","mean"))
    s=U.groupby("day")["x1"].sum()
    out["up_x1"]=pd.Series({"mean":U.x1.mean(),"t":U.x1.sum()/np.sqrt(((s-s*0)**2).sum()),"days":len(s)})
    return out
