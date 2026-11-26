def explore(data):
    import numpy as np, pandas as pd
    import numpy.linalg as la
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            d=pd.DataFrame({"coin":coin,"w":w,"year":day.dt.year,"day":day,"prof":(b["regime"]=="unknown"),
                            "r1":c.pct_change(),"pos":np.arange(len(b))})
            for p in (3,5,10,20):
                s=c/c.shift(p)-1
                d[f"s{p}"]=s
                z=(s-s.rolling(60,min_periods=20).mean())/s.rolling(60,min_periods=20).std()
                d[f"z{p}"]=(-z).clip(lower=0)
            for h in (1,2,3,5):
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,5):
        D[f"x{h}"]=D[f"f{h}"]-D["coin"].map(D.groupby("coin")[f"f{h}"].mean())
    def ols(d,y,xs):
        d=d.dropna(subset=[y]+xs)
        if len(d)<30: return [np.nan]*len(xs),[np.nan]*len(xs),len(d)
        X=np.column_stack([np.ones(len(d))]+[d[x].values for x in xs]); Y=d[y].values
        XtXi=la.inv(X.T@X); be=XtXi@X.T@Y; e=Y-X@be
        G=pd.DataFrame(X*e[:,None]).groupby(d["day"].values).sum().values
        V=XtXi@(G.T@G)@XtXi; t=be/np.sqrt(np.diag(V))
        return list(be[1:]),list(t[1:]),len(d)
    out={}
    P=D[D.prof]
    res=[]
    for p in (3,5,10,20):
        for h in (1,3):
            sub=P[P.pos%h==0].copy(); sub["n"]=-sub[f"s{p}"]; sub["n1"]=-sub.r1
            b,t,n=ols(sub,f"x{h}",["n"]); bj,tj,nj=ols(sub,f"x{h}",["n","n1"])
            res.append([p,h,b[0],t[0],bj[0],tj[0],bj[1],tj[1],n])
    out["depth_period_alone_and_joint_lastday"]=pd.DataFrame(res,columns=["p","h","b","t","b_joint","t_joint","b_last","t_last","n"])
    # deep slide with small last day vs shallow slide big last day
    Q=P.dropna(subset=["s5","r1","x1"]).copy()
    Q["deep"]=Q.s5<Q.s5.median(); Q["bigday"]=Q.r1<Q.r1.median()
    def mt(g):
        gg=g.groupby("day").x1.mean(); 
        return pd.Series({"n":len(g),"days":len(gg),"x1":g.x1.mean(),"t":gg.mean()/(gg.std()/np.sqrt(len(gg))) if len(gg)>2 else np.nan})
    out["deep_x_bigday_profile"]=Q.groupby(["deep","bigday"]).apply(mt)
    Q2=D[~D.prof].dropna(subset=["s5","r1","x1"]).copy()
    Q2["deep"]=Q2.s5<Q2.s5.median(); Q2["bigday"]=Q2.r1<Q2.r1.median()
    out["deep_x_bigday_outside"]=Q2.groupby(["deep","bigday"]).apply(mt)
    # last-day fall graded, in profile, side check: single-day fall quartiles
    Q["q1"]=pd.qcut(-Q.r1,4,labels=False)
    out["lastday_quartile_profile"]=Q.groupby("q1").apply(mt)
    out["lastday_by_year"]=P.assign(n1=-P.r1).groupby("year").apply(lambda g: pd.Series({"t":ols(g,"x1",["n1"])[1][0],"n":len(g)}))
    return out
