def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            c = b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1 = c/c.shift(1)-1
            d = pd.DataFrame({
                "coin":coin,"win":w,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                "nxt":(c.shift(-1)/c-1)-mu,
                "nxt2":(c.shift(-2)/c.shift(-1)-1)-mu,
                "r1":r1,"r5":c/c.shift(5)-1,"r60":c/c.shift(60)-1,
                "vol20":r1.rolling(20).std(),"vol30":r1.rolling(30).std(),
                "rng":(h-l)/c, "clv":(c-l)/(h-l).replace(0,np.nan),
                "alloc":b["postRebalance_current_allocation"].astype(float),
            })
            d["rngz"]=d["rng"]/d["rng"].shift(1).rolling(20).mean()
            d["z1"]=d["r1"]/d["vol20"]
            d["z5"]=d["r5"]/d["vol20"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["agit"]=D.groupby("coin")["vol30"].transform(lambda s: np.where(s.isna(),"na",np.where(s>s.median(),"agit","calm")))
    D["trend"]=np.where(D.r60>0.10,"rising",np.where(D.r60<-0.10,"falling","choppy"))
    D.loc[D.r60.isna(),"trend"]="na"
    def tday(x, day):
        m = x.notna(); x=x[m]; day=day[m]
        n=len(x)
        if n<10: return (n, np.nan, np.nan, 0)
        mean=x.mean(); dev=(x-mean).groupby(day).sum(); Dn=len(dev)
        se=np.sqrt((dev**2).sum()*Dn/(Dn-1))/n
        return (n, mean, mean/se, Dn)
    def tab(df, keys, col="nxt"):
        out=[]
        for k,g in df.groupby(keys):
            n,m,t,dn=tday(g[col], g["day"])
            out.append((str(k),n,dn,m,t))
        return pd.DataFrame(out,columns=["grp","n","days","mean","t"]).set_index("grp")
    res={}
    up=D[(D.r1>0)&(D.trend!="na")&(D.agit!="na")]
    dn=D[(D.r1<0)&(D.trend!="na")&(D.agit!="na")]
    res["up days nxt by trend x agit"]=tab(up,["trend","agit"])
    res["down days nxt by trend x agit"]=tab(dn,["trend","agit"])
    upA=up[up.agit=="agit"].copy()
    upA["z1q"]=pd.qcut(upA.z1,3,labels=False)
    res["agitated up days nxt by z1 tercile"]=tab(upA,["z1q"])
    res["agitated up days nxt by trend x z1 tercile"]=tab(upA,["trend","z1q"])
    upA["rq"]=pd.qcut(upA.rngz,3,labels=False)
    res["agitated up days nxt by range tercile"]=tab(upA,["rq"])
    f=D[(D.trend=="falling")&(D.r1>0)&(D.r5<0)].copy()
    f["z5q"]=pd.qcut(f.z5,3,labels=False); f["rq"]=pd.qcut(f.rngz,3,labels=False); f["cq"]=pd.qcut(f.clv,3,labels=False)
    res["falling still-down up: z5 tercile"]=tab(f,["z5q"])
    res["falling still-down up: range tercile"]=tab(f,["rq"])
    res["falling still-down up: clv tercile"]=tab(f,["cq"])
    res["falling still-down up: day-2 move by z5 tercile"]=tab(f,["z5q"],"nxt2")
    res["falling still-down up: agit"]=tab(f[f.agit!="na"],["agit"])
    # book gains
    D["gain"]=D.alloc*D.nxt
    h=D[D.alloc.abs()>1e-9].copy()
    h["gq"]=pd.qcut(h.gain.rank(method="first"),10,labels=False)
    res["held: deciles of gain, mean r1 z1 rngz clv"]=h.groupby("gq")[["gain","z1","z5","rngz","clv"]].mean()
    return res
