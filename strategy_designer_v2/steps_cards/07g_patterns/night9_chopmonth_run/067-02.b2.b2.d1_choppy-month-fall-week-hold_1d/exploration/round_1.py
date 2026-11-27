import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(c)
            r30h=b.get("debug_info.components.month_fall.last_history_value")
            for i in range(0,n-7,7):
                fwd=c[i+7]/c[i]-1
                r30=c[i]/c[i-30]-1 if i>=30 else np.nan
                if r30h is not None and not pd.isna(r30h.iloc[i]): r30=r30h.iloc[i]/100
                r7=c[i]/c[i-7]-1 if i>=7 else np.nan
                r1=c[i]/c[i-1]-1 if i>=1 else np.nan
                rng=(b["high"].iloc[i]-b["low"].iloc[i])/c[i]
                vol=np.std(np.diff(np.log(c[max(0,i-20):i+1]))) if i>=10 else np.nan
                rows.append(dict(coin=coin,w=w,day=str(b["timestamp"].iloc[i])[:10],
                    chop=b["regime"].iloc[i]=="unknown",fwd=fwd,r30=r30,r7=r7,r1=r1,rng=rng,vol=vol,
                    wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["un"]=d["fwd"]-d["drift"]
    d["z"]=d["un"]/d.groupby("coin")["fwd"].transform("std")
    def summ(g):
        g=g.dropna(subset=["un"])
        s=g.groupby("day")["un"].sum(); m=g["un"].mean()
        dev=g.groupby("day")["un"].apply(lambda x:(x-m).sum())
        G=len(dev); se=np.sqrt(G/(G-1)*(dev**2).sum())/len(g) if G>1 else np.nan
        return pd.Series(dict(n=len(g),days=G,mean_un=m,mean_fwd=g["fwd"].mean(),t=m/se if se else np.nan,z=g["z"].mean()))
    out={}
    dd=d.dropna(subset=["r30"]).copy()
    dd["q30"]=pd.qcut(dd["r30"],5,labels=False)
    out["r30 quintile x chop"]=dd.groupby(["chop","q30"]).apply(summ)
    for v in ["r7","r1","rng","vol"]:
        x=d.dropna(subset=[v]).copy(); x["q"]=pd.qcut(x[v],5,labels=False)
        out[v+" quintile x chop"]=x.groupby(["chop","q"]).apply(summ)
    out["weekday"]=d.groupby("wd").apply(summ)
    out["year chop"]=d[d.chop].groupby("yr").apply(summ)
    return out
