def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change()
            vol=r1.rolling(30,min_periods=20).std()
            hi5=c.rolling(5,min_periods=5).max()
            dist=(c-hi5)/hi5/vol
            tr60=(c/c.shift(60)-1)*100
            vrank=vol.rolling(60,min_periods=30).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            f=c.shift(-5)/c-1
            for i in range(0,n-5,5):
                rows.append(dict(coin=coin,w=w,fwd=f.iloc[i],dist=dist.iloc[i],tr=tr60.iloc[i],
                    vr=vrank.iloc[i],reg=b["regime"].iloc[i],yr=ts.iloc[i].year,
                    day=ts.iloc[i].normalize(),pos=i))
    D=pd.DataFrame(rows).dropna(subset=["fwd"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D["trg"]=pd.cut(D["tr"],[-1e9,-10,10,1e9],labels=["falling","choppy","rising"])
    D["dq"]=pd.cut(D["dist"],[-1e9,-3,-1.5,-0.0001,1e9],labels=["deep<-3","mid","shallow","at_high"])
    D["vq"]=pd.cut(D["vr"],[0,0.2,0.4,0.6,0.8,1.0001],labels=["v1","v2","v3","v4","v5"])
    def summ(g):
        g=g.dropna(subset=["ex"])
        k=len(g)
        if k<3: return pd.Series(dict(n=k,mean_ex_pct=np.nan,t=np.nan,days=np.nan,t_day=np.nan))
        m=g["ex"].mean(); s=g["ex"].std()
        dd=g.groupby("day")["ex"].sum(); nd=len(dd)
        # day-pooled t of mean: sum of deviations per day
        td=dd.sum()/np.sqrt((dd**2).sum()) if nd>2 else np.nan
        return pd.Series(dict(n=k,mean_ex_pct=100*m,t=m/(s/np.sqrt(k)),days=nd,t_day=td))
    out={}
    O=D[D.reg!="unknown"]
    out["out-prof by dist bucket"]=O.groupby("dq").apply(summ).round(3)
    out["all by dist bucket"]=D.groupby("dq").apply(summ).round(3)
    out["out-prof dist x trend"]=O.dropna(subset=["trg"]).groupby(["trg","dq"]).apply(summ).round(3)
    out["out-prof deep by year"]=O[O.dq=="deep<-3"].groupby("yr").apply(summ).round(3)
    out["out-prof deep by coin"]=O[O.dq=="deep<-3"].groupby("coin").apply(summ).round(3)
    out["out-prof by vr bucket"]=O.groupby("vq").apply(summ).round(3)
    out["out-prof vr x trend"]=O.dropna(subset=["trg"]).groupby(["trg","vq"]).apply(summ).round(3)
    out["out-prof v5 by year"]=O[O.vq=="v5"].groupby("yr").apply(summ).round(3)
    out["out-prof v5 by coin"]=O[O.vq=="v5"].groupby("coin").apply(summ).round(3)
    # graded slope of ex on dist out of profile, day pooled
    x=O.dropna(subset=["dist","ex"])
    g=x.groupby("day")[["dist","ex"]].mean()
    sl=np.polyfit(g["dist"],g["ex"],1)[0]
    res=g["ex"]-np.polyval(np.polyfit(g["dist"],g["ex"],1),g["dist"])
    se=np.sqrt((res**2).sum()/(len(g)-2)/((g["dist"]-g["dist"].mean())**2).sum())
    out["out-prof slope ex on dist (day pooled)"]=pd.Series(dict(slope=sl,t=sl/se,days=len(g)))
    # overlap of deep drops and high vr
    out["out-prof deep x vr"]=O.groupby(["dq","vq"]).apply(summ).round(3)
    return out
