def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            mx=c.rolling(20).max(); mn=c.rolling(20).min()
            rp=2*(c-mn)/(mx-mn)-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            r60=c/c.shift(60)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"rp":rp,"r1":r1,"r60":r60,
                            "vol20":vol20,"f5":f5,"f1":f1,"reg":b["regime"].values,
                            "alloc":b["postRebalance_current_allocation"].astype(float),
                            "day":ts.dt.floor("D"),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # weekday: per day mean across coins, then t over days
    D1=D.dropna(subset=["f1"])
    dm=D1.groupby(["day"]).agg(f1=("f1","mean"),wd=("wd","first"),yr=("yr","first"))
    out["f1 by weekday, day-clustered"]=dm.groupby("wd")["f1"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    dm["thfr"]=dm.wd.isin([3,4])
    out["thu+fri bar next-day by year"]=dm.groupby(["yr","thfr"])["f1"].mean().unstack()
    # r1 effect in rising, clustered by day
    G=D[D.pos%5==0].dropna(subset=["f5","r1","vol20"]).copy()
    drift=G.groupby("coin")["f5"].mean()
    G["ex5"]=G["f5"]-G["coin"].map(drift)
    G["z"]=G.r1/G.vol20
    G["rising"]=G.reg=="unknown"
    def cl(g,x):
        g=g.dropna(subset=[x,"ex5"])
        xc=g[x]-g[x].mean()
        b=(xc*g["ex5"]).sum()/(xc**2).sum()
        e=g["ex5"]-g["ex5"].mean()-b*xc
        s=(xc*e).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/(xc**2).sum()
        return pd.Series({"n":len(g),"days":g.day.nunique(),"slope":b,"t_cl":b/se})
    out["z1 slope rising/not, clustered"]=G.groupby("rising").apply(lambda g:cl(g,"z"))
    out["rp slope rising/not, clustered"]=G.groupby("rising").apply(lambda g:cl(g,"rp"))
    # rp and z jointly in rising
    R=G[G.rising].dropna(subset=["rp"])
    X=np.column_stack([np.ones(len(R)),R.rp,R.z]); y=R.ex5.values
    bb,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@bb
    XtXi=np.linalg.inv(X.T@X)
    S=pd.DataFrame(X*e[:,None]).groupby(R.day.values).sum().values
    V=XtXi@(S.T@S)@XtXi
    out["rising joint rp+z (clustered t)"]=pd.DataFrame({"b":bb,"t":bb/np.sqrt(np.diag(V))},index=["c","rp","z"])
    # not-rising: choppy vs falling by r60
    N=G[~G.rising].dropna(subset=["r60","rp"]).copy()
    N["tr"]=np.where(N.r60<-0.10,"falling","choppy")
    out["rp slope not-rising by trend"]=N.groupby("tr").apply(lambda g:cl(g,"rp"))
    out["z slope not-rising by trend"]=N.groupby("tr").apply(lambda g:cl(g,"z"))
    # vol: vol20 relative to coin median
    G["vt"]=G.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,2,labels=["calm","agit"]))
    out["rp slope by vol half x rising"]=G.dropna(subset=["rp"]).groupby(["rising","vt"]).apply(lambda g:cl(g,"rp"))
    # book long/short contribution
    D["g"]=D.alloc*D.f1
    D["side"]=np.sign(D.alloc)
    out["bar gain by side"]=D.dropna(subset=["g"]).groupby("side")["g"].agg(["count","mean","sum"])
    return out
