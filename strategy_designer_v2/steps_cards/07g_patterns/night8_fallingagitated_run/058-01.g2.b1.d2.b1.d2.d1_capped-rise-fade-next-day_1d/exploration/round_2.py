def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r,"sd":sd})
            d["z1"]=r/sd
            d["clv"]=(c-l)/(h-l)
            d["uw"]=((h-c)/c)/sd
            d["lw"]=((c-l)/c)/sd
            d["z3"]=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            d["n1"]=c.shift(-1)/c-1
            d["n2"]=c.shift(-2)/c-1
            d["pos"]=np.arange(len(b))
            d["inprof"]=b["regime"].isin(["mean_reversion","unknown"]).values
            d["regime"]=b["regime"].values
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["u1"]=D["n1"]-D.groupby("coin")["n1"].transform("mean")
    dr2=D[D.pos%2==0].groupby("coin")["n2"].mean()
    D["u2"]=D["n2"]-D["coin"].map(dr2)
    def summ(g,col):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    P=D[D.inprof].dropna(subset=["u1","z1","clv"]).copy()
    P["clvb"]=pd.cut(P["clv"],[0,0.33,0.67,1.0],include_lowest=True)
    P["sideb"]=np.where(P.z1>0,"up","down")
    out["u1 by side x clv in profile"]=P.groupby(["sideb","clvb"],observed=True).apply(summ,"u1")
    # OLS u1 on z1 and clv in profile
    X=np.column_stack([np.ones(len(P)),P.z1.clip(-3,3),P.clv-0.5])
    y=P.u1.values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["ols u1~z1+clv in profile"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z1","clv"])
    Q=D[~D.inprof].dropna(subset=["u1","z1","clv"])
    X=np.column_stack([np.ones(len(Q)),Q.z1.clip(-3,3),Q.clv-0.5]); y=Q.u1.values
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["ols u1~z1+clv out profile"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z1","clv"])
    P["lwb"]=pd.qcut(P["lw"],5)
    out["u1 by distance above low (sd) in profile"]=P.groupby("lwb",observed=True).apply(summ,"u1")
    P["uwb"]=pd.qcut(P["uw"],5)
    out["u1 by distance below high (sd) in profile"]=P.groupby("uwb",observed=True).apply(summ,"u1")
    hi=P[P.clv>0.67]
    out["u1 high close in profile by year"]=hi.groupby("yr").apply(summ,"u1")
    lo=P[P.clv<0.33]
    out["u1 low close in profile by year"]=lo.groupby("yr").apply(summ,"u1")
    # 2-day horizon by clv, grid 2
    G=D[(D.pos%2==0)&D.inprof].dropna(subset=["clv","u2"]).copy()
    G["clvb"]=pd.cut(G["clv"],[0,0.33,0.67,1.0],include_lowest=True)
    out["u2 by clv in profile grid2"]=G.groupby("clvb",observed=True).apply(summ,"u2")
    # multi-day rise every bar in profile next-day
    P["z3b"]=pd.cut(P["z3"],[-99,-1,0,0.5,1,1.5,2,99])
    out["u1 by z3 in profile"]=P.groupby("z3b",observed=True).apply(summ,"u1")
    return out
