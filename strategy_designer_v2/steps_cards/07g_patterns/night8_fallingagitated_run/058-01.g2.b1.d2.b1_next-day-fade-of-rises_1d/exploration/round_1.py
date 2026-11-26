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
            d=pd.DataFrame({"coin":coin,"win":w,"r":r,"z":r/v,
                "z3":(c/c.shift(3)-1)/(v*np.sqrt(3)),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "tr60":c/c.shift(60)-1,
                "rng":(b["high"]-b["low"])/c/v,
                "clpos":(c-b["low"])/(b["high"]-b["low"]),
                "inprof":(b["regime"]=="unknown"),
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos":np.arange(len(b)),"day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r"].mean()
    D["u1"]=D["f1"]-D["coin"].map(drift)
    D["u3"]=D["f3"]-3*D["coin"].map(drift)
    def summ(g,col):
        x=g[col].dropna()
        if len(x)<5: return pd.Series({"n":len(x),"mean":np.nan,"t":np.nan})
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["u1 by z bucket x inprof"]=D.groupby(["inprof","zb"]).apply(summ,"u1").unstack(0) if False else D.groupby(["inprof","zb"]).apply(lambda g: summ(g,"u1"))
    G=D[D.pos%3==0].copy()
    G["z3b"]=pd.cut(G["z3"],[-99,-1.5,-0.5,0.5,1.5,99])
    out["u3 grid by 3d rise bucket x inprof"]=G.groupby(["inprof","z3b"]).apply(lambda g: summ(g,"u3"))
    # outside profile split by trend (60d within window)
    O=D[~D.inprof].copy()
    O["trend"]=pd.cut(O["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    O["up"]=pd.cut(O["z"],[-99,-1,1,99],labels=["dn","mid","up"])
    out["out-prof u1 by trend x z"]=O.groupby(["trend","up"]).apply(lambda g: summ(g,"u1"))
    P=D[D.inprof]
    out["inprof u1 by weekday"]=P.groupby("wd").apply(lambda g: summ(g,"u1"))
    P2=P[P.z>1].copy()
    P2["cl"]=pd.cut(P2["clpos"],[-0.01,0.5,0.8,1.01])
    out["inprof up>1sd u1 by close position"]=P2.groupby("cl").apply(lambda g: summ(g,"u1"))
    out["inprof up>1sd u1 by window"]=P2.groupby("win").apply(lambda g: summ(g,"u1"))
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["win"]=w;dd.append(t)
    DY=pd.concat(dd)
    bk=DY.groupby(["win","day"])["book_return"].mean().dropna()
    out["book days"]=pd.Series({"n":len(bk),"mean":bk.mean(),"std":bk.std(),"top5 share of sum":bk.nlargest(int(len(bk)*0.05)).sum()/bk.sum(),"bottom5 sum/total":bk.nsmallest(int(len(bk)*0.05)).sum()/bk.sum()})
    out["book by window"]=bk.groupby(level=0).agg(["mean","count","sum"])
    out["share inprof"]=D.inprof.mean()
    return out
