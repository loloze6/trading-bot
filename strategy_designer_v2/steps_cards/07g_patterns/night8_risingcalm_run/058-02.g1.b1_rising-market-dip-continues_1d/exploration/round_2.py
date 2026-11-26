def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30).std()
            mx5=c.rolling(5).max()
            mx10=c.rolling(10).max()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "dip":(c-mx5)/mx5/sd30,"dip10":(c-mx10)/mx10/sd30,"sd30":sd30,
                "r60":c/c.shift(60)-1,"r1":r1,"z1":r1/sd30,"z3":(c/c.shift(3)-1)/sd30,
                "fwd5":c.shift(-5)/c-1,"fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,
                "ts":ts,"wd":ts.dt.weekday,
                "fc":b["forecast"].values})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    # agitation: coin sd30 vs its own median of sd30 over trailing year (approx within window, fallback coin median)
    A["agit"]=A["sd30"]>A["coin"].map(A.groupby("coin")["sd30"].median())
    A["trend"]=np.where(A.r60>0.1,"rising",np.where(A.r60<-0.1,"falling",np.where(A.r60.notna(),"choppy","na")))
    A["prof"]=A["trend"]+np.where(A["agit"]," agit"," calm")
    def clus(g,col):
        x=g.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x),"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        d=x.groupby("ts")[col].sum()
        n=len(x); m=x[col].mean()
        se=np.sqrt(((d - x.groupby("ts")[col].count()*m)**2).sum())/n
        return pd.Series({"n":n,"days":len(d),"mean%":100*m,"t_day":m/se})
    G=A[A.pos%5==0].copy()
    G["ex5"]=G["fwd5"]-G["coin"].map(G.groupby("coin")["fwd5"].mean())
    G=G[G.trend!="na"]
    G["dipb"]=pd.cut(G["dip"],[-99,-4,-2,-0.5,-1e-9,0.1],labels=["<-4","-4..-2","-2..-.5","-.5..0","at high"])
    out={}
    out["profile x dip bin, ex5, day-clustered"]=G.groupby(["prof","dipb"]).apply(lambda g:clus(g,"ex5")).round(3)
    # slope of ex5 on raw dip per profile
    res={}
    for p,g in G.dropna(subset=["ex5","dip"]).groupby("prof"):
        x=g["dip"];y=g["ex5"]
        b=np.cov(x,y)[0,1]/x.var()
        e=y-y.mean()-b*(x-x.mean())
        # day clustered se
        u=(x-x.mean())*e
        s=u.groupby(g["ts"]).sum()
        se=np.sqrt((s**2).sum())/((x-x.mean())**2).sum()
        res[p]=[len(g),g.ts.nunique(),b*100,b/se]
    out["slope ex5 on raw dip (pct per unit), clustered t"]=pd.DataFrame(res,index=["n","days","slope%","t"]).T.round(3)
    # forecast vs raw dip
    act=A[A.fc!=0].dropna(subset=["dip"])
    out["corr forecast vs raw dip (active bars)"]=float(np.corrcoef(act.fc,act.dip)[0,1])
    out["share active bars at raw dip==0"]=float((act.dip>-1e-9).mean())
    # 3-day scaled move continuation by profile
    G["z3b"]=pd.cut(G["z3"],[-99,-3,-1,1,3,99])
    out["profile x 3d scaled move, ex5"]=G.groupby(["prof","z3b"]).apply(lambda g:clus(g,"ex5")).round(3)
    # weekday next-day clustered
    D=A.dropna(subset=["fwd1"]).copy()
    D["ex1"]=D["fwd1"]-D["coin"].map(D.groupby("coin")["fwd1"].mean())
    out["weekday ex1 clustered"]=D.groupby("wd").apply(lambda g:clus(g,"ex1")).round(3)
    out["weekday ex1 by year-half proxy (window parity)"]=D.assign(par=D.w.str[1:].astype(int)%2).groupby(["par","wd"]).apply(lambda g:clus(g,"ex1")).round(3)
    return out
