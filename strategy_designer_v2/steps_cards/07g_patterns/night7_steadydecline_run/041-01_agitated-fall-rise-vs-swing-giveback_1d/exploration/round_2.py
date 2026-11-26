def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            df=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "r":r,"z":r/sd,"regime":b["regime"].astype(str),
                "f1":c.shift(-1)/c-1,"g2":c.shift(-2)/c.shift(-1)-1,"g3":c.shift(-3)/c.shift(-2)-1,
                "rng":(b["high"]-b["low"])/c/sd,
                "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "bret":b["postRebalance_total_value"].astype(float).pct_change().shift(-1)})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    dr=D.groupby("coin")["r"].mean()
    D["dr"]=D["coin"].map(dr)
    for k in ["f1","g2","g3"]: D["x"+k]=D[k]-D["dr"]
    D["fa"]=D["regime"]=="unknown"
    def cl_slope(d,y,x):
        d=d[[y,x,"day"]].dropna()
        if len(d)<25: return (np.nan,np.nan,len(d))
        X=d[x]-d[x].mean(); Y=d[y]
        b=(X*Y).sum()/(X*X).sum(); a=Y.mean()-b*d[x].mean()
        e=Y-a-b*d[x]; g=(X*e).groupby(d["day"]).sum()
        se=np.sqrt((g**2).sum())/(X*X).sum(); return (b,b/se,len(d))
    def cl_mean(d,y):
        d=d[[y,"day"]].dropna(); m=d[y].mean()
        dev=(d[y]-m).groupby(d["day"]).sum(); se=np.sqrt((dev**2).sum())/len(d)
        return m,m/se,len(d)
    out={}
    F=D[D.fa]; Dn=F[F.z<0].copy(); Dn["az"]=-Dn["z"]
    Up=F[F.z>0].copy()
    t=[]
    for y in ["xf1","xg2","xg3"]:
        for nm,s in [("down",Dn),("up",Up)]:
            b,tb,n=cl_slope(s,y,"z"); m,tm,_=cl_mean(s,y); t.append([nm,y,b,tb,m,tm,n])
    out["fa: horizons day1/day2/day3 separately"]=pd.DataFrame(t,columns=["side","y","slope","t","mean","tmean","n"])
    t=[]
    for w,s in Dn.groupby("w"):
        b,tb,n=cl_slope(s,"xf1","az"); m,_,_=cl_mean(s,"xf1"); t.append([w,b,tb,m,n])
    out["fa down: by window slope on |z|"]=pd.DataFrame(t,columns=["w","slope","t","mean","n"])
    t=[]
    for cn,s in Dn.groupby("coin"):
        b,tb,n=cl_slope(s,"xf1","az"); m,tm,_=cl_mean(s,"xf1"); t.append([cn,b,tb,m,tm,n])
    out["fa down: by coin"]=pd.DataFrame(t,columns=["coin","slope","t","mean","tmean","n"])
    t=[]
    for yv,s in Dn.groupby("yr"):
        b,tb,n=cl_slope(s,"xf1","az"); m,tm,_=cl_mean(s,"xf1"); t.append([yv,b,tb,m,tm,n])
    out["fa down: by year"]=pd.DataFrame(t,columns=["yr","slope","t","mean","tmean","n"])
    # within fa down days: clv and range
    t=[]
    for x in ["clv","rng"]:
        b,tb,n=cl_slope(Dn,"xf1",x); t.append(["down",x,b,tb,n])
        b,tb,n=cl_slope(Up,"xf1",x); t.append(["up",x,b,tb,n])
    out["fa: clv/range slopes within side"]=pd.DataFrame(t,columns=["side","x","slope","t","n"])
    # down-day bounce outside fa
    O=D[~D.fa]; On=O[O.z<0].copy(); On["az"]=-On["z"]
    b,tb,n=cl_slope(On,"xf1","az"); m,tm,_=cl_mean(On,"xf1")
    out["other down: slope on |z|, mean"]=pd.Series({"slope":b,"t":tb,"mean":m,"tmean":tm,"n":n})
    # book: worst/best days context
    B=D.dropna(subset=["bret"]); B=B[B.bret!=0]
    B["q"]=pd.qcut(B["bret"],5,labels=False,duplicates="drop")
    out["book bar return quintiles: mean z, fa share"]=B.groupby("q").agg(n=("z","count"),z=("z","mean"),bret=("bret","mean"),fa=("fa","mean"))
    return out
