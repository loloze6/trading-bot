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
                "f1":c.shift(-1)/c-1,
                "rng":(b["high"]-b["low"])/c/sd,
                "lw":(np.minimum(b["open"],c)-b["low"])/c/sd})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D["dr"]=D["coin"].map(D.groupby("coin")["r"].mean())
    D["x1"]=D["f1"]-D["dr"]
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
    Dn["raz"]=Dn.groupby("coin")["az"].rank(pct=True)
    Dn["rrng"]=Dn.groupby("coin")["rng"].rank(pct=True)
    t=[]
    for nm,s in [("all",Dn),("no2020",Dn[Dn.yr!=2020]),("no_w16",Dn[Dn.w!="w16"])]:
        for x in ["az","raz","rng","rrng","lw"]:
            b,tb,n=cl_slope(s,"x1",x); t.append([nm,x,b,tb,n])
    out["fa down slopes, robustness"]=pd.DataFrame(t,columns=["set","x","slope","t","n"])
    Dn["q"]=pd.qcut(Dn["az"],4,labels=False)
    out["fa down: |z| quartiles next-day excess"]=Dn.groupby("q").agg(n=("x1","count"),az=("az","mean"),x1=("x1","mean"),f1=("f1","mean"))
    Dn["qr"]=pd.qcut(Dn["rng"],4,labels=False)
    out["fa down: range quartiles"]=Dn.groupby("qr").agg(n=("x1","count"),rng=("rng","mean"),x1=("x1","mean"))
    # both together
    d=Dn[["x1","az","rng","day"]].dropna()
    X=np.column_stack([np.ones(len(d)),d.az,d.rng]); y=d.x1.values
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
    XtXi=np.linalg.inv(X.T@X); G=pd.DataFrame(X*e[:,None]).groupby(d.day.values).sum().values
    V=XtXi@(G.T@G)@XtXi; out["fa down: x1 on az + rng"]=pd.Series({"b_az":beta[1],"t_az":beta[1]/np.sqrt(V[1,1]),"b_rng":beta[2],"t_rng":beta[2]/np.sqrt(V[2,2]),"n":len(d)})
    # other regimes, range on down days
    O=D[(~D.fa)&(D.z<0)]
    b,tb,n=cl_slope(O,"x1","rng"); out["other down: slope on rng"]=pd.Series({"slope":b,"t":tb,"n":n})
    return out
