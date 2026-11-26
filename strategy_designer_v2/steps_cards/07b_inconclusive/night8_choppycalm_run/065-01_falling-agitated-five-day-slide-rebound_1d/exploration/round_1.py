def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            s5=c/c.shift(5)-1
            z=(s5-s5.rolling(60,min_periods=20).mean())/s5.rolling(60,min_periods=20).std()
            fc=(-z).clip(lower=0)
            prof=(b["regime"]=="unknown")
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            for h in (1,2,3,5):
                b[f"f{h}"]=c.shift(-h)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"year":day.dt.year,"day":day,"prof":prof,"s5":s5,"r1":r1,"fc":fc,
                            "f1":b["f1"],"f2":b["f2"],"f3":b["f3"],"f5":b["f5"],"pos":np.arange(len(b)),
                            "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu={h:D.groupby("coin")[f"f{h}"].mean() for h in (1,2,3,5)}
    for h in (1,2,3,5):
        D[f"x{h}"]=D[f"f{h}"]-D["coin"].map(mu[h])
    def clus_slope(d,y,x):
        d=d.dropna(subset=[y,x])
        if len(d)<30: return (np.nan,np.nan,len(d))
        X=d[x]-d[x].mean(); Y=d[y]-d[y].mean()
        b=(X*Y).sum()/(X*X).sum()
        e=Y-b*X
        g=(X*e).groupby(d["day"]).sum()
        se=np.sqrt((g**2).sum())/(X*X).sum()
        return (b,b/se,len(d))
    out={}
    P=D[D.prof&(D.fc>0)]
    res=[]
    for h in (1,2,3,5):
        sub=P[P.pos%h==0]
        b,t,n=clus_slope(sub,f"x{h}","fc")
        res.append([h,b,t,n,sub[f"x{h}"].mean()])
    out["horizon_slope_in_profile"]=pd.DataFrame(res,columns=["h","slope","t","n","mean_x"])
    # outside profile
    Q=D[(~D.prof)&(D.fc>0)]
    res=[]
    for h in (1,3):
        sub=Q[Q.pos%h==0]; b,t,n=clus_slope(sub,f"x{h}","fc"); res.append([h,b,t,n,sub[f"x{h}"].mean()])
    out["outside_profile"]=pd.DataFrame(res,columns=["h","slope","t","n","mean_x"])
    # buckets
    P2=P.copy(); P2["q"]=pd.qcut(P2.fc,4,labels=False,duplicates="drop")
    out["fc_quartile"]=P2.groupby("q").agg(n=("x1","size"),fc=("fc","mean"),x1=("x1","mean"),x3=("x3","mean"))
    # raw s5 slope and single-day
    Pa=D[D.prof].copy()
    Pa["neg5"]=-Pa.s5; Pa["neg1"]=-Pa.r1
    res=[]
    for x in ("neg5","neg1"):
        for h in (1,3):
            sub=Pa[Pa.pos%h==0]; b,t,n=clus_slope(sub,f"x{h}",x); res.append([x,h,b,t,n])
    # multivar
    sub=Pa.dropna(subset=["x1","neg5","neg1"])
    import numpy.linalg as la
    X=np.column_stack([np.ones(len(sub)),sub.neg5,sub.neg1]); y=sub.x1.values
    beta=la.lstsq(X,y,rcond=None)[0]; e=y-X@beta
    XtXi=la.inv(X.T@X); G=pd.DataFrame(X*e[:,None]).groupby(sub.day.values).sum().values
    V=XtXi@(G.T@G)@XtXi; tt=beta/np.sqrt(np.diag(V))
    res.append(["joint_neg5",1,beta[1],tt[1],len(sub)]); res.append(["joint_neg1",1,beta[2],tt[2],len(sub)])
    out["raw_depth_vs_lastday_profile"]=pd.DataFrame(res,columns=["x","h","slope","t","n"])
    out["by_coin"]=P.groupby("coin").apply(lambda g: pd.Series(dict(zip(["slope","t","n"],clus_slope(g,"x1","fc")))+[]) if False else pd.Series(dict(zip(["slope","t","n"],clus_slope(g,"x1","fc")))))
    out["by_year"]=P.groupby("year").apply(lambda g: pd.Series(dict(zip(["slope","t","n"],clus_slope(g,"x1","fc")))))
    out["by_window"]=P.groupby("w").apply(lambda g: pd.Series({"n":len(g),"x1":g.x1.mean(),"fcw":(g.x1*g.fc).sum()/g.fc.sum()}))
    return out
