def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=30).std()
            z1=r/sd
            fwd=c.shift(-H)/c-1
            tr=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            calm=(b["regime"]!="chop")
            zs={}
            for L in (3,5,10,20):
                zs[L]=(c/c.shift(L)-1)/(sd*np.sqrt(L))
            for i in range(0,len(b),H):
                d=dict(coin=coin,w=w,z1=z1.iloc[i],fwd=fwd.iloc[i],calm=calm.iloc[i],tr=tr.iloc[i],
                       year=ts.iloc[i].year,day=ts.iloc[i].normalize())
                for L in zs: d["z%d"%L]=zs[L].iloc[i]
                rows.append(d)
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    def cl_slope(g,x):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<30: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan,days=np.nan))
        X=g[x].values; y=g["ex"].values
        Xm=X-X.mean(); b=(Xm*y).sum()/(Xm**2).sum(); a=y.mean()-b*X.mean()
        e=y-a-b*X
        sc=pd.Series(Xm*e).groupby(g["day"].values).sum()
        G=len(sc); v=(sc**2).sum()/((Xm**2).sum()**2)*G/(G-1)
        return pd.Series(dict(n=len(g),slope=b,t=b/np.sqrt(v),days=G))
    out={}
    res=[]
    for L in ("z1","z3","z5","z10","z20"):
        for cm in (True,False):
            s=cl_slope(d[d["calm"]==cm],L); s["lb"]=L; s["calm"]=cm; res.append(s)
    out["clustered slope by lookback x calm"]=pd.DataFrame(res)
    # multivariate in calm: z1 and z5 together
    g=d[d["calm"]].dropna(subset=["z1","z5","z20","ex"])
    X=np.column_stack([np.ones(len(g)),g["z1"],g["z5"],g["z20"]])
    beta,_,_,_=np.linalg.lstsq(X,g["ex"].values,rcond=None)
    e=g["ex"].values-X@beta
    XtXi=np.linalg.inv(X.T@X)
    S=pd.DataFrame(X*e[:,None]).groupby(g["day"].values).sum().values
    V=XtXi@(S.T@S)@XtXi
    out["calm joint z1 z5 z20"]=pd.DataFrame(dict(beta=beta,t=beta/np.sqrt(np.diag(V))),index=["c","z1","z5","z20"])
    d["tb"]=np.where(d["tr"]>0.10,"rising",np.where(d["tr"]<-0.10,"falling",np.where(d["tr"].isna(),"na","choppy")))
    out["calm z5 slope by trend"]=d[d["calm"]].groupby("tb").apply(lambda g:cl_slope(g,"z5"))
    out["calm z5 slope by year"]=d[d["calm"]].groupby("year").apply(lambda g:cl_slope(g,"z5"))
    out["calm z5 slope by coin"]=d[d["calm"]].groupby("coin").apply(lambda g:cl_slope(g,"z5"))
    gg=d[d["calm"]].dropna(subset=["z5"]).copy()
    gg["dex"]=gg["ex"]*np.sign(gg["z5"])
    gg["q"]=pd.qcut(gg["z5"].abs(),3,labels=False)
    gg["sg"]=np.sign(gg["z5"])
    out["calm dex by |z5| tercile x sign"]=gg.groupby(["sg","q"])["dex"].agg(["count","mean"])
    # book: long vs short gain
    bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"].astype(float)
            rr=b["close"].astype(float).shift(-1)/b["close"].astype(float)-1
            bk.append(pd.DataFrame(dict(a=a,g=a*rr)))
    bk=pd.concat(bk).dropna()
    bk["side"]=np.sign(bk["a"])
    out["bar gain by side"]=bk.groupby("side")["g"].agg(["count","mean","sum"])
    return out
