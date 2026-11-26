import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            ret60=c/c.shift(60)-1
            vp=sd.rolling(len(b),min_periods=20).rank(pct=True)  # within-window proxy
            n=len(b)
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"r":r,"z":z,"f1":f1,"f3":f3,
                "inprof":(b["regime"]=="unknown").values,"ret60":ret60,"rng_z":rng/(rng.rolling(30,min_periods=20).mean()),
                "clv":clv,"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "fc":b["forecast"].astype(float),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    mu1=d.groupby("coin")["f1"].transform("mean")
    d["x1"]=d["f1"]-mu1
    g3=d[d["pos"]%3==0].copy()
    mu3=g3.groupby("coin")["f3"].transform("mean"); g3["x3"]=g3["f3"]-mu3
    def summ(s):
        s=s.dropna(); 
        return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    d["zb"]=pd.cut(d["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["next1 excess by z bucket, in profile"]=d[d.inprof].groupby("zb")["x1"].apply(summ).unstack()
    out["next1 excess by z bucket, out of profile"]=d[~d.inprof].groupby("zb")["x1"].apply(summ).unstack()
    g3["zb"]=pd.cut(g3["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["next3 excess by z, in profile (grid3)"]=g3[g3.inprof].groupby("zb")["x3"].apply(summ).unstack()
    out["next3 excess by z, out profile (grid3)"]=g3[~g3.inprof].groupby("zb")["x3"].apply(summ).unstack()
    d["trend"]=pd.cut(d["ret60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["next1 excess, z>1, by trend"]=d[d.z>1].groupby("trend")["x1"].apply(summ).unstack()
    out["next1 excess, z<-1, by trend"]=d[d.z<-1].groupby("trend")["x1"].apply(summ).unstack()
    up=d[(d.inprof)&(d.z>0)].copy(); up["cb"]=pd.cut(up["clv"],[-0.01,0.33,0.66,1.01])
    out["in prof up days: next1 by close loc"]=up.groupby("cb")["x1"].apply(summ).unstack()
    out["in prof by weekday next1"]=d[d.inprof].groupby("wd")["x1"].apply(summ).unstack()
    out["all by weekday next1"]=d.groupby("wd")["x1"].apply(summ).unstack()
    d["rb"]=pd.qcut(d["rng_z"],5)
    out["next1 by range vs 30d, in profile"]=d[d.inprof].groupby("rb")["x1"].apply(summ).unstack()
    bk=data["days"]
    return out
