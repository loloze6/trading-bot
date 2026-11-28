def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change(); sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"prof":(b["regime"]=="unknown"),"r":r,"z":r/sd,
                "clv":(c-l)/(h-l).replace(0,np.nan),"rng":(h-l)/c.shift(1)/sd,
                "r3p":c.shift(1)/c.shift(4)-1,"r10p":c.shift(1)/c.shift(11)-1,
                "dd30":c/c.rolling(30,min_periods=10).max()-1,
                "r60":c/c.shift(60)-1,"f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["f1"].mean()
    D["x1"]=D["f1"]-D["coin"].map(drift)
    U=D[D.prof&(D.z>0)&D.f1.notna()].copy()
    out={"n_up":len(U)}
    s=U.groupby("day")["x1"].sum()
    out["up_mean_x1_t_dayclustered"]=pd.Series({"mean":U.x1.mean(),"t":s.mean()/s.std()*np.sqrt(len(s))*1.0 if False else U.x1.sum()/np.sqrt((s**2).sum()),"days":len(s)})
    res={}
    for v in ["z","r","clv","rng","r3p","r10p","dd30","r60"]:
        V=U[U[v].notna()]
        if len(V)<30: continue
        q=pd.qcut(V[v].rank(method="first"),3,labels=False)
        g=V.groupby(q)["x1"].agg(["mean","size"])
        res[v]={"n":len(V),"corr":np.corrcoef(V[v],V.x1)[0,1],"lo":g["mean"].iloc[0],"mid":g["mean"].iloc[1],"hi":g["mean"].iloc[2],
                "vmean_lo":V[v][q==0].mean(),"vmean_hi":V[v][q==2].mean()}
    out["up_day_terciles_by_var"]=pd.DataFrame(res).T
    # combined: z * (1-clv) i.e. rise that closed off highs
    U["give"]=U.z*(1-U.clv)
    V=U[U.give.notna()]; q=pd.qcut(V.give.rank(method="first"),4,labels=False)
    out["give_quartiles"]=V.groupby(q).agg(n=("x1","size"),give=("give","mean"),x1=("x1","mean"),f2=("f2","mean"))
    # all profile days: next-day x1 by clv
    P=D[D.prof&D.f1.notna()&D.clv.notna()]
    q=pd.qcut(P.clv.rank(method="first"),4,labels=False)
    out["profile_all_by_clv"]=P.groupby(q).agg(n=("x1","size"),clv=("clv","mean"),z=("z","mean"),x1=("x1","mean"))
    return out
