import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            r14=c/c.shift(14)-1
            r60=c/c.shift(60)-1
            z=r14/(vol30*np.sqrt(14))
            f7=c.shift(-7)/c-1
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            vrank=vol30.rolling(120,min_periods=60).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"z":z,"r1":r1,"r1z":r1/vol30,
                            "r60":r60,"vrank":vrank,"f7":f7,"f3":f3,"f1":f1,
                            "regime":b["regime"].values,"fc":b["forecast"].values,
                            "alloc":b["postRebalance_current_allocation"].values,
                            "wd":ts.dt.weekday,"year":ts.dt.year})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    drift7=A.loc[A.pos%7==0,"f7"].mean()
    G=A[(A.pos%7==0)].dropna(subset=["z","f7"]).copy()
    G["u7"]=G.f7-drift7
    G["zq"]=pd.qcut(G.z,5,labels=False)
    G["inprof"]=(G.regime=="unknown")
    def summ(g,col="u7"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["drift7"]=drift7
    out["u7 by z quintile x inprofile"]=G.groupby(["inprof","zq"]).apply(summ).unstack(0)
    G["tr"]=pd.cut(G.r60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["ag"]=np.where(G.vrank>0.5,"ag","calm")
    G["sz"]=np.sign(G.z)*G.u7
    out["signed carry by trend x ag (|z|>1)"]=G[G.z.abs()>1].groupby(["tr","ag"]).apply(lambda g:summ(g,"sz")).unstack()
    out["u7 by z quintile x trend"]=G.groupby(["tr","zq"]).apply(summ)["t"].unstack()
    # daily
    D=A.dropna(subset=["r1z","f1"]).copy()
    D["dq"]=pd.qcut(D.r1z,5,labels=False)
    D["u3"]=D.f3-A.loc[A.pos%3==0,"f3"].mean()
    D3=D[D.pos%3==0]
    out["u3 by 1d move quintile (grid3)"]=D3.groupby("dq").apply(lambda g:summ(g,"u3"))
    out["u3 by 1d quintile x vol half"]=D3.assign(ag=np.where(D3.vrank>0.5,"ag","calm")).groupby(["ag","dq"]).apply(lambda g:summ(g,"u3"))["t"].unstack()
    out["next-day ret by weekday"]=D.groupby("wd").apply(lambda g:summ(g,"f1"))
    out["u7 by vol rank tercile"]=G.assign(vq=pd.qcut(G.vrank,3,labels=False)).groupby("vq").apply(summ)
    return out
