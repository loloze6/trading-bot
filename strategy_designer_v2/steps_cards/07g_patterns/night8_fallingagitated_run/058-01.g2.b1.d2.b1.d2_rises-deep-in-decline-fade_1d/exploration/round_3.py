def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z":r/sd,"f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "inp":(b["regime"]=="unknown").values,"tr":c/c.shift(60)-1,
                "dep":c/c.rolling(20,min_periods=10).max()-1,
                "vr":sd/r.rolling(90,min_periods=60).std(),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            d["g3"]=(np.arange(len(d))%3==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["u1"]=D.f1-D.groupby("coin")["f1"].transform("mean")
    dr3=D[D.g3].groupby("coin")["f3"].mean(); D["u3"]=D.f3-D.coin.map(dr3)
    D["trb"]=pd.cut(D.tr,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    def st(g,col):
        x=g.dropna(subset=[col]); s=x.groupby("day")[col].sum()
        return pd.Series({"cases":len(x),"days":len(s),"mean%":100*x[col].mean(),
            "t_days":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    P=D[D.inp]; Dn=P[P.z<0]
    out["in-prof down days u1 by z (day t)"]=Dn.groupby(pd.cut(Dn.z,[-99,-2,-1,-0.5,0])).apply(lambda g:st(g,"u1"))
    out["in-prof down days u1 by depth quartile"]=Dn.groupby(pd.qcut(Dn.dep,4)).apply(lambda g:st(g,"u1"))
    Dn2=Dn.assign(s=(-Dn.z).clip(upper=2)*(-Dn.dep))
    out["in-prof down u1 by fall*depth quartile"]=Dn2.groupby(pd.qcut(Dn2.s,4)).apply(lambda g:st(g,"u1"))
    out["in-prof down u1 by year"]=Dn[Dn.z<-0.5].groupby("yr").apply(lambda g:st(g,"u1"))
    O=D[~D.inp]
    out["out-prof u1 by vr quintile (day t)"]=O.groupby(pd.qcut(O.vr,5)).apply(lambda g:st(g,"u1"))
    Ol=O[O.vr<0.8]
    out["out-prof low vr u1 by trend"]=Ol.groupby("trb").apply(lambda g:st(g,"u1"))
    out["out-prof low vr u1 by year"]=Ol.groupby("yr").apply(lambda g:st(g,"u1"))
    out["u1 by weekday out-prof (day t)"]=O.groupby("wd").apply(lambda g:st(g,"u1"))
    out["u1 by weekday in-prof (day t)"]=P.groupby("wd").apply(lambda g:st(g,"u1"))
    return out
