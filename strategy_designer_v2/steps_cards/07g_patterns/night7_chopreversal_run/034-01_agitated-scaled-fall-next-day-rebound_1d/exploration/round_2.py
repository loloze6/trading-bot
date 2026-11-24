def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r":r,"z":r/sd,
                "n1":c.shift(-1)/c-1,
                "z3":(c/c.shift(3)-1)/(sd*np.sqrt(3)),
                "z5":(c/c.shift(5)-1)/(sd*np.sqrt(5)),
                "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "ag":(b["regime"]!="chop").astype(int),
                "pos":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["x1"]=D["n1"]-D.groupby("coin")["n1"].transform("mean")
    D=D.dropna(subset=["z","x1"])
    D["day"]=D["ts"].dt.floor("D"); D["wd"]=D["ts"].dt.weekday; D["yr"]=D["ts"].dt.year
    def ct(g,col="x1"):
        x=g[[col,"day"]].dropna()
        if len(x)<3: return pd.Series({"n":len(x),"days":x.day.nunique(),"mean%":np.nan,"t_day":np.nan})
        dev=x[col]-0  # excess already
        s=dev.groupby(x["day"]).sum()
        G=len(s); m=dev.mean()
        se=np.sqrt((s-m*x.groupby("day").size()).pow(2).sum()*G/(G-1))/len(x)
        return pd.Series({"n":len(x),"days":G,"mean%":100*m,"t_day":m/se})
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,99])
    out["A next-day by z, ag, day-clustered"]=D.groupby(["ag","zb"],observed=True).apply(ct).round(3)
    # convexity: regress on fall and fall^2 among falls
    F=D[D.z<0].copy(); F["f"]=-F.z
    for a in [0,1]:
        G=F[F.ag==a]
        X=np.column_stack([np.ones(len(G)),G.f,G.f**2]); y=G.x1.values
        beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
        XtX=np.linalg.inv(X.T@X)
        sc=pd.DataFrame(X*e[:,None]).groupby(G.day.values).sum().values
        V=XtX@(sc.T@sc)@XtX
        out[f"B falls ag={a}: OLS x1 on fall, fall^2 (coef, t_day)"]=pd.DataFrame({"coef":beta,"t":beta/np.sqrt(np.diag(V))},index=["c","fall","fall2"]).round(5)
    # close location among falls z<-1.5
    big=D[D.z<-1.5].copy()
    big["lowclose"]=(big.clv<=0.25).astype(int)
    out["C falls z<-1.5 by low close, ag"]=big.groupby(["ag","lowclose"]).apply(ct).round(3)
    # multi-day falls
    D["z3b"]=pd.cut(D["z3"],[-99,-2.5,-2,-1.5,-1,0,99])
    out["D next-day by 3d scaled move, ag"]=D.groupby(["ag","z3b"],observed=True).apply(ct).round(3)
    D["z5b"]=pd.cut(D["z5"],[-99,-2.5,-2,-1.5,-1,0,99])
    out["E next-day by 5d scaled move, ag"]=D.groupby(["ag","z5b"],observed=True).apply(ct).round(3)
    # weekday, clustered
    out["F all bars by weekday clustered"]=D.groupby("wd").apply(ct).round(3)
    dn=D[D.z<-1]
    out["G falls z<-1 by weekday clustered"]=dn.groupby("wd").apply(ct).round(3)
    out["H falls z<-1 Thursday by year"]=dn[dn.wd==3].groupby("yr").apply(ct).round(3)
    out["I falls z<-1 not Thursday by ag"]=dn[dn.wd!=3].groupby("ag").apply(ct).round(3)
    # small-move reversal in agitated, clustered, by year
    sm=D[(D.ag==1)&(D.z.abs()<1)].copy(); sm["sgn"]=np.sign(sm.z)
    sm["xs"]=-sm.sgn*sm.x1
    out["J ag small moves |z|<1: reversal (x1 * -sign) by year"]=sm.groupby("yr").apply(lambda g:ct(g,"xs")).round(3)
    out["J2 all ag small moves reversal"]=ct(sm,"xs").round(3)
    smc=D[(D.ag==0)&(D.z.abs()<1)].copy(); smc["xs"]=-np.sign(smc.z)*smc.x1
    out["J3 calm small moves reversal"]=ct(smc,"xs").round(3)
    # big fall by year (ag, z<-2)
    out["K ag falls z<-2 by year"]=D[(D.ag==1)&(D.z<-2)].groupby("yr").apply(ct).round(3)
    out["K2 calm falls z<-1 by year"]=D[(D.ag==0)&(D.z<-1)].groupby("yr").apply(ct).round(3)
    return out
