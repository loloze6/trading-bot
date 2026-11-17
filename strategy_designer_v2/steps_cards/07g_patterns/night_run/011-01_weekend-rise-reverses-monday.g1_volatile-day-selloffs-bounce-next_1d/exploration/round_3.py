def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change()
            sd=r.rolling(60,min_periods=60).std()
            nxt=c.shift(-1)/c-1
            n2=c.shift(-2)/c-1
            cl=(c-l)/(h-l).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":r/sd,"sd":sd,"nxt":nxt,"n2":n2,"cl":cl,
                            "uw":(h-c)/c/sd,"lw":(c-l)/c/sd,"fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm); D["ex2"]=D["n2"]-2*D["coin"].map(cm)
    E=D.dropna(subset=["z","ex","cl"]).copy()
    def tab(g):
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    out={}
    E["cb"]=E.groupby("coin")["cl"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["all days: next1 by close-location quintile"]=tab(E.groupby("cb")["ex"])
    E["side"]=np.where(E["z"]<-1,"fall",np.where(E["z"]>1,"rise","mid"))
    E["c3"]=E.groupby("coin")["cl"].transform(lambda s: pd.qcut(s,3,labels=False))
    out["side x close-location tercile"]=tab(E.groupby(["side","c3"])["ex"])
    F=E[E["z"]<-1].copy()
    X=np.column_stack([np.ones(len(F)),F["z"],F["cl"],F["sd"]/F.groupby("coin")["sd"].transform("median")]); y=F["ex"].values
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta; cov=e@e/(len(y)-4)*np.linalg.inv(X.T@X)
    out["falls OLS ex~z+cl+relvol"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z","cl","relvol"])
    F["half"]=np.where(F["w"].str[1:].astype(int)<=12,"w1-12","w13-24")
    F["c3"]=pd.qcut(F["cl"],3,labels=False)
    out["falls cl tercile x half"]=tab(F.groupby(["half","c3"])["ex"])
    out["falls near-low by coin"]=tab(F[F["c3"]<=1].groupby("coin")["ex"])
    G=F[F["pos"]%2==0].dropna(subset=["ex2"])
    out["falls next2 by cl tercile (grid2)"]=tab(G.groupby("c3")["ex2"])
    A=E[E["fc"]>=5].copy(); A["c3"]=pd.qcut(A["cl"],3,labels=False)
    out["active fc>=5 by cl tercile"]=tab(A.groupby("c3")["ex"])
    return out
