def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"z":r/sd,
                "z3":(c/c.shift(3)-1)/(sd*np.sqrt(3)),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "dep":c/c.rolling(20,min_periods=10).max()-1,
                "inp":(b["regime"]=="unknown").values,
                "pos":b["postRebalance_current_allocation"].astype(float),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "rng":(b["high"]-b["low"])/c/sd,
                "clo":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            d["g3"]=(np.arange(len(d))%3==0)
            d["vr"]=sd/r.rolling(90,min_periods=60).std()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    dr1=D.groupby("coin")["f1"].transform("mean"); dr3=D[D.g3].groupby("coin")["f3"].mean()
    D["u1"]=D.f1-dr1; D["u3"]=D.f3-D.coin.map(dr3)
    def summ(g,col):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    D["zb"]=pd.cut(D.z,[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["u1 by z, profile"]=D.groupby(["inp","zb"]).apply(lambda g:summ(g,"u1")).unstack(0)
    G=D[D.g3].copy(); G["z3b"]=pd.cut(G.z3,[-99,-1.5,-0.5,0,0.5,1.5,99])
    out["u3 by 3d rise z3, profile (grid)"]=G.groupby(["inp","z3b"]).apply(lambda g:summ(g,"u3")).unstack(0)
    P=D[D.inp]
    P2=P.copy(); P2["db"]=pd.qcut(P2.dep,4)
    out["in-prof u1 by depth x updown"]=P2.groupby(["db",P2.z>0]).apply(lambda g:summ(g,"u1")).unstack(1)
    out["in-prof u1 by close loc (up/down)"]=P.groupby([pd.cut(P.clo,[0,.25,.5,.75,1.01]),P.z>0]).apply(lambda g:summ(g,"u1")).unstack(1)
    out["u1 by weekday, profile"]=D.groupby(["wd","inp"]).apply(lambda g:summ(g,"u1")).unstack(1)
    out["in-prof u1 by range z (up days)"]=P[P.z>0].groupby(pd.qcut(P[P.z>0].rng,4)).apply(lambda g:summ(g,"u1"))
    out["out-prof u1 by vol ratio"]=D.groupby([D.inp,pd.qcut(D.vr,4)]).apply(lambda g:summ(g,"u1")).unstack(0)
    out["by window in-prof up days"]=P[P.z>0.5].groupby("w").apply(lambda g:summ(g,"u1"))
    return out
