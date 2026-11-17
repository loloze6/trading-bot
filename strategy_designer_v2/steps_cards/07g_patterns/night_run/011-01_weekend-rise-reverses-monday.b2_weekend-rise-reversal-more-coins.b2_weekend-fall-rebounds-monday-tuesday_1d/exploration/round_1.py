def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            b["wd"]=ts.dt.weekday.values
            c=b["close"].astype(float)
            b["r1"]=c.pct_change()
            b["r2p"]=c/c.shift(2)-1
            b["f1"]=c.shift(-1)/c-1
            b["f2"]=c.shift(-2)/c-1
            b["f35"]=c.shift(-5)/c.shift(-2)-1
            sd=b["r1"].rolling(60,min_periods=20).std().shift(1)
            b["z1"]=b["r1"]/sd
            b["sd"]=sd
            v=b["volume"].astype(float)
            b["relvol"]=v/v.rolling(28,min_periods=10).mean().shift(1)
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","wd","r1","r2p","f1","f2","f35","z1","sd","relvol","forecast"]])
    df=pd.concat(rows,ignore_index=True)
    cm=df.groupby("coin")["f1"].mean()
    df["cm"]=df["coin"].map(cm)
    df["x1"]=df["f1"]-df["cm"]; df["x2"]=df["f2"]-2*df["cm"]
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    out["next1 excess by weekday of bar"]=df.groupby("wd")["x1"].apply(tt).unstack()
    # reversal slope by weekday: regress x2 on z1
    res=[]
    for d,g in df.groupby("wd"):
        g=g.dropna(subset=["x2","z1"])
        g=g[g.z1.abs()<8]
        sl=stats.linregress(g.z1,g.x2)
        gn=g[g.z1<0]; gp=g[g.z1>0]
        s1=stats.linregress(gn.z1,gn.x2); s2=stats.linregress(gp.z1,gp.x2)
        res.append([d,len(g),sl.slope,sl.slope/sl.stderr,s1.slope,s1.slope/s1.stderr,s2.slope,s2.slope/s2.stderr])
    out["x2 on own-day z, by weekday (all, falls, rises)"]=pd.DataFrame(res,columns=["wd","n","slope","t","slope_fall","t_fall","slope_rise","t_rise"])
    sun=df[(df.wd==6)].dropna(subset=["z1","x2"]).copy()
    sun["q"]=pd.qcut(sun.z1,5,labels=False)
    out["sunday z quintile: x1, x2, f35"]=sun.groupby("q").agg(z=("z1","mean"),n=("x2","size"),x1=("x1","mean"),x2=("x2","mean"),f35=("f35","mean"))
    for d in [2,4,5]:
        g=df[df.wd==d].dropna(subset=["z1","x2"]).copy(); g["q"]=pd.qcut(g.z1,5,labels=False)
        out[f"wd{d} z quintile x2"]=g.groupby("q").agg(z=("z1","mean"),n=("x2","size"),x2=("x2","mean"))
    # 2-day weekend return (Fri close->Sun close)
    g=df[df.wd==6].dropna(subset=["r2p","x2","sd"]).copy()
    g["z2"]=g.r2p/(g.sd*np.sqrt(2)); g["q"]=pd.qcut(g.z2,5,labels=False)
    out["sun 2day-weekend z quintile x2"]=g.groupby("q").agg(z=("z2","mean"),x2=("x2","mean"),n=("x2","size"))
    # volume interaction on sunday falls
    f=sun[sun.z1<0].dropna(subset=["relvol"]).copy()
    f["vq"]=pd.qcut(f.relvol,3,labels=False)
    out["sun falls by relvol tercile"]=f.groupby("vq").agg(rv=("relvol","mean"),z=("z1","mean"),x2=("x2","mean"),n=("x2","size"))
    # vol regime
    a=df.dropna(subset=["sd","x1"]).copy()
    a["sdq"]=a.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["next1 excess by vol tercile"]=a.groupby("sdq")["x1"].apply(tt).unstack()
    # all-day big moves reversal
    a["zq"]=pd.qcut(a.z1.clip(-8,8),10,labels=False)
    out["all days z decile -> x1"]=a.groupby("zq").agg(z=("z1","mean"),x1=("x1","mean"),n=("x1","size"))
    # book by weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["wd"]=pd.to_datetime(d["day"]).dt.weekday; dd.append(d[["wd","book_return","coin_return"]])
    dd=pd.concat(dd)
    out["book daily return by weekday"]=dd.groupby("wd")["book_return"].apply(tt).unstack()
    out["coin daily return by weekday"]=dd.groupby("wd")["coin_return"].apply(tt).unstack()
    return out
