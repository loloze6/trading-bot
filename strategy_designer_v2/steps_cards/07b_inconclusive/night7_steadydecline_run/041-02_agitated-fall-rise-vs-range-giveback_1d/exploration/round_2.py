def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            allr.append(df["close"].astype(float).pct_change().dropna())
        drift=pd.concat(allr).mean()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); h=df["high"].astype(float); l=df["low"].astype(float); o=df["open"].astype(float)
            ret=c.pct_change()
            rng=(h-l).shift(1).rolling(30,min_periods=30).mean()
            sd=ret.shift(1).rolling(30,min_periods=30).std()
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "inprof":(df["regime"]=="unknown"),
                "mv_rng":(c-c.shift(1))/rng,"mv_sd":ret/sd,"ret":ret,
                "dayrng":(h-l)/rng,"cloc":(c-l)/(h-l).replace(0,np.nan),
                "up3":(ret>0).astype(int).rolling(3).sum(),
                "ret5":c/c.shift(5)-1,"ret60":c/c.shift(60)-1,
                "r1":c.shift(-1)/c-1-drift,"fc":df["forecast"].astype(float)})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["mv_rng","r1","mv_sd"])
    P=D[D.inprof]; U=P[P.ret>0].copy()
    out={}
    def cl_slope(X,x,y="r1"):
        X=X.dropna(subset=[x,y])
        xv=X[x].values-X[x].mean(); yv=X[y].values
        b=(xv*(yv-yv.mean())).sum()/(xv**2).sum()
        e=yv-yv.mean()-b*xv
        g=pd.Series(xv*e).groupby(X["day"].values).sum()
        G=len(g); se=np.sqrt((g**2).sum()*G/(G-1))/(xv**2).sum()
        return pd.Series({"n":len(X),"days":G,"slope":b,"t":b/se,"spearman":stats.spearmanr(X[x],X[y]).correlation})
    res={}
    for x in ["mv_rng","mv_sd","ret","dayrng","cloc","up3","ret5","ret60"]:
        res[x]=cl_slope(U,x)
    out["up-days in profile: slope of r1 on each grader (clustered by day)"]=pd.DataFrame(res).T
    Dn=P[P.ret<0].copy(); res2={}
    for x in ["mv_rng","mv_sd","ret","dayrng","cloc","ret5"]:
        res2[x]=cl_slope(Dn,x)
    out["down-days in profile: slope of r1"]=pd.DataFrame(res2).T
    out["all profile days: slope r1 on mv_sd"]=cl_slope(P,"mv_sd")
    out["all profile days: slope r1 on mv_rng"]=cl_slope(P,"mv_rng")
    # up-days: day-level mean r1 t
    g=U.groupby("day").r1.mean()
    out["up-days: mean r1 day-pooled"]=pd.Series({"mean%":g.mean()*100,"t":g.mean()/g.std()*np.sqrt(len(g)),"days":len(g)})
    U["cq"]=pd.qcut(U.cloc,3,labels=False,duplicates="drop")
    out["up-days by close location tercile"]=U.groupby("cq").r1.agg(["size","mean"]).assign(mean=lambda x:x["mean"]*100)
    U["up3q"]=U.up3
    out["up-days by up-days in last 3"]=U.groupby("up3q").r1.agg(["size","mean"]).assign(mean=lambda x:x["mean"]*100)
    U["sq"]=pd.qcut(U.mv_sd,4,labels=False)
    out["up-days by mv_sd quartile"]=U.groupby("sq").r1.agg(["size","mean"]).assign(mean=lambda x:x["mean"]*100)
    out["up-days by window"]=U.groupby("w").r1.agg(["size","mean"]).assign(mean=lambda x:x["mean"]*100)
    return out
