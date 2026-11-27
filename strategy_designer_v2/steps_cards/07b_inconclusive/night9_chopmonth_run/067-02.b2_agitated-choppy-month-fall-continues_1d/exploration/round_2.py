def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            r60=np.full(n,np.nan); r60[60:]=c[60:]/c[:-60]-1
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,ret=c[i+h]/c[i]-1,fc=b["forecast"].iloc[i],
                        reg=b["regime"].iloc[i],r30=r30[i],r60=r60[i],
                        yr=pd.to_datetime(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["ex"]=d["ret"]-d["drift"]
    d["usual"]=d.groupby(["coin","h"])["ret"].transform("std")
    d=d[d.r30.notna()]
    d["choppy"]=d.r60.abs()<=0.10
    d["agit"]=d.reg=="unknown"
    def summ(g):
        n=len(g)
        if n<6: return pd.Series(dict(n=n))
        sl=stats.linregress(g["r30"],g["ex"])
        x=-g["ex"]
        return pd.Series(dict(n=n,short_unusual=x.mean(),t=x.mean()/(x.std()/np.sqrt(n)),
                              strength=(x/g["usual"]).mean(),slope=sl.slope,slope_t=sl.slope/sl.stderr))
    f=d[d.r30<0]
    out={}
    out["falls_choppy_by_agit_h"]=f[f.r60.notna()].groupby(["choppy","agit","h"]).apply(summ)
    ch=f[f.choppy==True]
    out["falls_choppy_any_by_h"]=ch.groupby("h").apply(summ)
    c7=ch[ch.h==7].copy()
    out["choppy_falls_by_year"]=c7.groupby("yr").apply(summ)
    if len(c7)>9:
        c7["q"]=pd.qcut(c7["r30"],3,labels=["deep","mid","shallow"])
        out["choppy_falls_tercile"]=c7.groupby("q").apply(summ)
    out["all_falls_by_h"]=f.groupby("h").apply(summ)
    return out
