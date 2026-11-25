def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            ret60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"z":z,"sd":sd,"ret60":ret60,"regime":b["regime"].astype(str),
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,
                "r5":c/c.shift(5)-1,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos":b["postRebalance_current_allocation"].astype(float),
                "rng":(b["high"]-b["low"])/c,"clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r"].mean()
    D["dr"]=D["coin"].map(drift)
    D["x1"]=D["f1"]-D["dr"]
    D["fa"]=D["regime"]=="unknown"
    def cl_slope(d,y,x):
        d=d[[y,x,"day"]].dropna()
        if len(d)<30: return (np.nan,np.nan,len(d))
        X=d[x]-d[x].mean(); Y=d[y]
        b=(X*Y).sum()/(X*X).sum(); a=Y.mean()-b*d[x].mean()
        e=Y-a-b*d[x]
        g=(X*e).groupby(d["day"]).sum()
        se=np.sqrt((g**2).sum())/(X*X).sum()
        return (b,b/se,len(d))
    def cl_mean(d,y):
        d=d[[y,"day"]].dropna()
        g=d[y].groupby(d["day"]).sum()
        m=d[y].mean(); 
        dev=(d[y]-m).groupby(d["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(d)
        return m, m/se, len(d)
    out={}
    res=[]
    for reg,dd in [("fallagit",D[D.fa]),("other",D[~D.fa]),("all",D)]:
        for side,s in [("up",dd[dd.z>0]),("down",dd[dd.z<0]),("both",dd)]:
            for h,y in [("h1","x1")]:
                b,t,n=cl_slope(s,y,"z")
                m,tm,_=cl_mean(s,y)
                res.append([reg,side,b,t,n,m,tm])
    out["slope next-day excess on z"]=pd.DataFrame(res,columns=["reg","side","slope","t","n","mean","t_mean"])
    # quintile table of z by regime
    D["zq"]=pd.qcut(D["z"],10,labels=False)
    q=D.groupby(["fa","zq"]).agg(n=("x1","count"),zmean=("z","mean"),x1=("x1","mean"),f2=("f2","mean")).reset_index()
    out["decile z next day by fa"]=q
    # weekday
    wdt=[]
    for wd,s in D.groupby("wd"):
        m,t,n=cl_mean(s,"x1"); wdt.append([wd,m,t,n])
    out["weekday next-day excess (x1 of bar wd)"]=pd.DataFrame(wdt,columns=["wd","mean","t","n"])
    # vol level: sd quintile per coin
    D["sdq"]=D.groupby("coin")["sd"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    vt=[]
    for k,s in D.groupby("sdq"):
        m,t,n=cl_mean(s,"x1"); b,tb,_=cl_slope(s,"x1","z"); vt.append([k,m,t,b,tb,n])
    out["by vol quintile: mean x1, slope on z"]=pd.DataFrame(vt,columns=["sdq","mean","t","slope","tslope","n"])
    # 5-day return and clv
    ot=[]
    for x in ["r5","clv","rng","ret60"]:
        for reg,dd in [("fa",D[D.fa]),("other",D[~D.fa])]:
            b,t,n=cl_slope(dd,"x1",x); ot.append([x,reg,b,t,n])
    out["slopes x1 on other features"]=pd.DataFrame(ot,columns=["x","reg","slope","t","n"])
    out["regime counts"]=D["regime"].value_counts()
    return out
