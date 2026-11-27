def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"w":w})
            d["nxt"]=c.shift(-1)/c-1
            d["r1"]=c/c.shift(1)-1
            d["fc"]=b["forecast"]
            v=b["volume"]
            d["vr"]=v/v.shift(1).rolling(20).mean()-1
            d["tr60"]=c/c.shift(60)-1
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["drift"]=D.groupby("coin")["nxt"].transform("mean")
    D["u"]=-(D["nxt"]-D["drift"])  # short direction unusual
    D=D.dropna(subset=["nxt"])
    def st(g):
        s=g.groupby("day")["u"].sum(); n=g["u"].count()
        nd=len(s)
        t=g["u"].mean()*n/ (s.std()*np.sqrt(nd)) if nd>2 else np.nan
        return pd.Series({"n":n,"days":nd,"mean_u":g["u"].mean(),"t":t})
    out={}
    up=D[D["r1"]>0].copy()
    cases=D[D["fc"]<=-2].copy()
    out["cases_all"]=st(cases)
    out["up_all"]=st(up)
    out["up_heavyvol_fc0"]=st(up[up["vr"]>=0])
    out["up_lightvol"]=st(up[up["vr"]<0])
    out["down_all"]=st(D[D["r1"]<0])
    up["vrq"]=pd.qcut(up["vr"],5,labels=False,duplicates="drop")
    out["up_by_vr_quintile"]=up.groupby("vrq").apply(st)
    cases["fq"]=pd.qcut(cases["fc"].abs().rank(method="first"),5,labels=False)
    out["cases_by_absfc_quint"]=cases.groupby("fq").apply(st)
    up["r1q"]=pd.qcut(up["r1"],5,labels=False)
    out["up_by_r1_quint"]=up.groupby("r1q").apply(st)
    cases["r1q"]=pd.qcut(cases["r1"],3,labels=False)
    out["cases_by_r1_terc"]=cases.groupby("r1q").apply(st)
    out["cases_by_coin"]=cases.groupby("coin").apply(st)
    out["cases_by_window"]=cases.groupby("w").apply(st)
    cases["trend"]=np.where(cases["tr60"]>0.1,"rising",np.where(cases["tr60"]<-0.1,"falling",np.where(cases["tr60"].notna(),"choppy","na")))
    out["cases_by_trend"]=cases.groupby("trend").apply(st)
    out["corr_up_vr_u"]=float(up[["vr","u"]].corr().iloc[0,1])
    return out
