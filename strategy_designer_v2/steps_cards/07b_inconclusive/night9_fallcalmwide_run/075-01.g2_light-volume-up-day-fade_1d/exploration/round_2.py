def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["w"]=w
            d["nxt"]=c.shift(-1)/c-1
            d["r1"]=c/c.shift(1)-1
            d["fc"]=b["forecast"].astype(float)
            v=b["volume"].astype(float)
            d["vr"]=v/v.shift(1).rolling(20).mean()-1
            d["tr60"]=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            d["year"]=ts.dt.year
            d["day"]=ts.dt.floor("D")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["nxt"])
    D["drift"]=D.groupby("coin")["nxt"].transform("mean")
    D["u"]=-(D["nxt"]-D["drift"])
    def st(g):
        g=g.dropna(subset=["u"])
        s=g.groupby("day")["u"].sum(); n=len(g); nd=len(s)
        t=g["u"].mean()*n/(s.std()*np.sqrt(nd)) if nd>2 else np.nan
        return pd.Series({"n":n,"days":nd,"mean_u":g["u"].mean(),"t":t})
    def grp(df,key):
        return pd.DataFrame({k:st(g) for k,g in df.groupby(key)}).T
    out={}
    up=D[D["r1"]>0].copy()
    cases=D[D["fc"]<=-2].copy()
    out["summary"]=pd.DataFrame({"cases_fc<=-2":st(cases),"up_all":st(up),
        "up_vr>=0":st(up[up["vr"]>=0]),"up_vr<0":st(up[up["vr"]<0]),
        "down_all":st(D[D["r1"]<0]),"all_days":st(D)}).T
    up["vrq"]=pd.qcut(up["vr"],5,labels=False,duplicates="drop")
    out["up_by_vr_quintile"]=grp(up,"vrq")
    cases["fq"]=pd.qcut(cases["fc"].abs().rank(method="first"),5,labels=False)
    out["cases_by_absfc_quint"]=grp(cases,"fq")
    up["r1q"]=pd.qcut(up["r1"],5,labels=False)
    out["up_by_r1_quint"]=grp(up,"r1q")
    cases["r1q"]=pd.qcut(cases["r1"],3,labels=False)
    out["cases_by_r1_terc"]=grp(cases,"r1q")
    out["cases_by_coin"]=grp(cases,"coin")
    out["cases_by_window"]=grp(cases,"w")
    cases["trend"]=np.where(cases["tr60"]>0.1,"rising",np.where(cases["tr60"]<-0.1,"falling",np.where(cases["tr60"].notna(),"choppy","na")))
    out["cases_by_trend"]=grp(cases,"trend")
    up["trend"]=np.where(up["tr60"]>0.1,"rising",np.where(up["tr60"]<-0.1,"falling",np.where(up["tr60"].notna(),"choppy","na")))
    out["up_light_by_trend"]=grp(up[up["vr"]<0],"trend")
    out["up_heavy_by_trend"]=grp(up[up["vr"]>=0],"trend")
    out["corr_up_vr_u"]=float(up[["vr","u"]].corr().iloc[0,1])
    out["corr_cases_fc_u"]=float(cases[["fc","u"]].corr().iloc[0,1])
    return out
