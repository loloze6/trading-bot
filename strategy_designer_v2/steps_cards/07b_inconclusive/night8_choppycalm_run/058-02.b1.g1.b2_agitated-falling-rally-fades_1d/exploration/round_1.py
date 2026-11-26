import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        allf=[]
        tmp=[]
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=20).std()
            z=r/vol
            fwd=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,"day":ts.dt.floor("D"),
                            "r":r,"z":z,"fwd":fwd,"inprof":b["regime"].astype(str)=="unknown",
                            "fc":b["forecast"].astype(float)})
            tmp.append(d); allf.append(fwd.dropna())
        mu=pd.concat(allf).mean()
        for d in tmp:
            d["ex"]=d["fwd"]-mu
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd","r"])
    def summ(g):
        s=-g["ex"]  # short-direction unusual move
        n=len(s)
        return pd.Series({"n":n,"days":g["day"].nunique(),"short_move_pct":100*s.mean(),
                          "t":s.mean()/(s.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan})
    P=D[D.inprof]
    out={}
    out["inprof_up_vs_down"]=P.assign(side=np.where(P.r>0,"up","down")).groupby("side").apply(summ)
    out["outprof_up_vs_down"]=D[~D.inprof].assign(side=np.where(D[~D.inprof].r>0,"up","down")).groupby("side").apply(summ)
    U=P[(P.r>0)&P.z.notna()].copy()
    U["zq"]=pd.qcut(U.z,4,labels=["q1","q2","q3","q4"])
    out["inprof_up_by_z_quartile"]=U.groupby("zq").apply(summ)
    U2=P[(P.r<=0)&P.z.notna()].copy()
    U2["zq"]=pd.qcut(U2.z,4,labels=["q1low","q2","q3","q4"])
    out["inprof_down_by_z_quartile"]=U2.groupby("zq").apply(summ)
    out["inprof_up_by_coin"]=U.groupby("coin").apply(summ)
    out["inprof_up_by_year"]=U.groupby("year").apply(summ)
    out["inprof_all_by_year"]=P.groupby("year").apply(summ)
    out["share_inprof"]=float(D.inprof.mean())
    return out
