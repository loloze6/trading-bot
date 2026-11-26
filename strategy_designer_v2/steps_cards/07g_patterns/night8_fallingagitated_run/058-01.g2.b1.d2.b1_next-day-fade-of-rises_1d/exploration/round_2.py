import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            v=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"r":r,"z":r/v,"v":v,
                "f1":c.shift(-1)/c-1,"tr60":c/c.shift(60)-1,
                "inprof":(b["regime"]=="unknown"),"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            for k in (2,3,5):
                d[f"z{k}"]=(c/c.shift(k)-1)/(v*np.sqrt(k))
                d[f"f{k}"]=c.shift(-k)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r"].mean()
    for k in (1,2,3,5):
        D[f"u{k}"]=D[f"f{k}"]-k*D["coin"].map(drift)
    def pooled(g,col):
        x=g[["day",col]].dropna()
        if len(x)<5: return pd.Series({"n":len(x),"days":x.day.nunique(),"mean":np.nan,"t_day":np.nan})
        dev=(x[col]-0).groupby(x["day"]).sum()
        m=x[col].mean(); se=np.sqrt((dev**2).sum())/len(x)
        return pd.Series({"n":len(x),"days":len(dev),"mean":m,"t_day":m/se})
    out={}
    P=D[D.inprof]
    res=[]
    for k in (2,3,5):
        G=P[P.pos%k==0]
        G=G[G[f"z{k}"]>0]
        s=pooled(G,f"u{k}")
        rho,pv=stats.spearmanr(G[f"z{k}"],G[f"u{k}"],nan_policy="omit")
        s["spearman"]=rho; s["p"]=pv; s.name=f"k{k}"
        res.append(s)
    out["inprof k-day rise -> next k-day u (rises only)"]=pd.DataFrame(res)
    G=P[P.pos%3==0].copy(); G=G[G.z3>0]
    G["q"]=pd.qcut(G["z3"],3,labels=["lo","mid","hi"])
    out["inprof 3d rise terciles u3"]=G.groupby("q").apply(lambda g: pooled(g,"u3"))
    out["inprof 3d rise>0.5 u3 by window"]=G[G.z3>0.5].groupby("win").apply(lambda g: pooled(g,"u3"))
    out["inprof 3d rise>0.5 u3 by coin"]=G[G.z3>0.5].groupby("coin").apply(lambda g: pooled(g,"u3"))
    # out of profile 3d continuation
    O=D[(~D.inprof)&(D.pos%3==0)].copy()
    O["trend"]=pd.cut(O["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    Oup=O[O.z3>0.5]
    out["outprof 3d rise>0.5 u3 by trend"]=Oup.groupby("trend").apply(lambda g: pooled(g,"u3"))
    # falling outside profile, up days next day
    F=D[(~D.inprof)&(D.tr60<-0.1)&(D.z>0)].copy()
    F["q"]=pd.qcut(F["z"],3,labels=["lo","mid","hi"])
    out["fall-outprof up days u1 terciles"]=F.groupby("q").apply(lambda g: pooled(g,"u1"))
    out["fall-outprof up>1 u1 by window"]=F[F.z>1].groupby("win").apply(lambda g: pooled(g,"u1"))
    # in-profile 1-day up days terciles, pooled
    U=P[P.z>0].copy(); U["q"]=pd.qcut(U["z"],3,labels=["lo","mid","hi"])
    out["inprof up days u1 terciles"]=U.groupby("q").apply(lambda g: pooled(g,"u1"))
    return out
