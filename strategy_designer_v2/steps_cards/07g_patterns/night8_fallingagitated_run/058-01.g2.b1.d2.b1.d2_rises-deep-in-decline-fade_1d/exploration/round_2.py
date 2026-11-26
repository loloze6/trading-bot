def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            tr=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z":r/sd,"z3":(c/c.shift(3)-1)/(sd*np.sqrt(3)),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "inp":(b["regime"]=="unknown").values,"tr":tr,
                "clo":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "pos":b["postRebalance_current_allocation"].astype(float)})
            d["g3"]=(np.arange(len(d))%3==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["u1"]=D.f1-D.groupby("coin")["f1"].transform("mean")
    dr3=D[D.g3].groupby("coin")["f3"].mean(); D["u3"]=D.f3-D.coin.map(dr3)
    def st(g,col):
        x=g.dropna(subset=[col]); s=x.groupby("day")[col].sum()
        return pd.Series({"cases":len(x),"days":len(s),"mean%":100*x[col].mean(),
            "t_days":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    P=D[D.inp]; U=P[P.z>0].copy()
    U["zb"]=pd.cut(U.z,[0,0.5,1,99]); U["cb"]=pd.cut(U.clo,[0,0.5,0.75,1.01])
    out["in-prof up days u1 by rise x close loc"]=U.groupby(["zb","cb"]).apply(lambda g:st(g,"u1"))
    U["score"]=U.z.clip(upper=1.5)*U.clo
    out["in-prof up u1 by rise*closeloc quartile"]=U.groupby(pd.qcut(U.score,4)).apply(lambda g:st(g,"u1"))
    G=D[D.g3]; GP=G[G.inp]; GU=GP[GP.z3>0]
    out["in-prof 3d rise u3 by z3 tercile"]=GU.groupby(pd.qcut(GU.z3,3)).apply(lambda g:st(g,"u3"))
    GO=G[~G.inp]
    out["out-prof 3d u3 by z3"]=GO.groupby(pd.cut(GO.z3,[-99,-1.5,-0.5,0.5,1.5,99])).apply(lambda g:st(g,"u3"))
    GO2=GO.copy(); GO2["trb"]=pd.cut(GO2.tr,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["out-prof 3d u3 rises>0.5 by trend"]=GO2[GO2.z3>0.5].groupby("trb").apply(lambda g:st(g,"u3"))
    out["out-prof 3d u3 falls<-0.5 by trend"]=GO2[GO2.z3<-0.5].groupby("trb").apply(lambda g:st(g,"u3"))
    out["book pnl by pos sign in prof"]=P.assign(g=P.pos*P.f1).groupby(np.sign(P.pos)).apply(lambda g:pd.Series({"n":len(g),"mean_gain%":100*g.g.mean()}))
    return out
