import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(20).std()
            z=r/sd
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r":r,
                "n1":c.shift(-1)/c-1,"n3":c.shift(-3)/c-1,
                "fa":(b["regime"]=="unknown").astype(int),
                "tr60":c/c.shift(60)-1,
                "rng":(b["high"]-b["low"])/c/sd,
                "clpos":(c-b["low"])/(b["high"]-b["low"]),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "pos":b["postRebalance_current_allocation"],
                "pos3":(np.arange(len(b))%3==0)})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","n1"])
    mu=D.groupby("coin")["n1"].mean(); D["x1"]=D["n1"]-D["coin"].map(mu)
    mu3=D[D.pos3].groupby("coin")["n3"].mean(); D["x3"]=D["n3"]-D["coin"].map(mu3)
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    def agg(g,col="x1"):
        s=g[col].dropna(); 
        return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan})
    out={}
    out["next1 by z, falling-agitated"]=D[D.fa==1].groupby("zb").apply(agg)
    out["next1 by z, other profiles"]=D[D.fa==0].groupby("zb").apply(agg)
    out["next3 by z, falling-agitated (grid)"]=D[(D.fa==1)&D.pos3].groupby("zb").apply(lambda g:agg(g,"x3"))
    out["next3 by z, other (grid)"]=D[(D.fa==0)&D.pos3].groupby("zb").apply(lambda g:agg(g,"x3"))
    D["tb"]=pd.cut(D["tr60"],[-9,-0.3,-0.1,0.1,0.3,9])
    out["next1 by 60d trend, up days z>1"]=D[D.z>1].groupby("tb").apply(agg)
    out["next1 by 60d trend, down days z<-1"]=D[D.z<-1].groupby("tb").apply(agg)
    up=D[(D.fa==1)&(D.z>0)].copy(); up["cb"]=pd.cut(up["clpos"],[-0.01,0.33,0.66,1.01])
    out["FA up days by close position"]=up.groupby("cb").apply(agg)
    out["FA up days by year"]=up.groupby("yr").apply(agg)
    out["FA up days by window"]=up.groupby("w").apply(agg)
    out["FA up days by weekday"]=up.groupby("wd").apply(agg)
    out["all by weekday"]=D.groupby("wd").apply(agg)
    out["FA up days by coin"]=up.groupby("coin").apply(agg)
    D["rb"]=pd.qcut(D["rng"],4)
    out["next1 by range/sd quartile x down day"]=D[D.z<0].groupby("rb").apply(agg)
    out["next1 by range/sd quartile x up day"]=D[D.z>0].groupby("rb").apply(agg)
    return out
