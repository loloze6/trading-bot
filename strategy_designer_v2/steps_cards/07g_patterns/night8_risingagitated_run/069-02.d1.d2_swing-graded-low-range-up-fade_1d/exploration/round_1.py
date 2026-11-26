def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change()
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            pos=(c-(hh+ll)/2)/((hh-ll)/2)
            tr60=c/c.shift(60)-1
            sd30=r1.rolling(30).std()
            vr=sd30/sd30.rolling(180,min_periods=60).mean()
            fwd=c.shift(-1)/c-1
            fwd3=c.shift(-3)/c-1
            rng=(h-l)/c
            clv=(c-l)/(h-l)
            df=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"pos":pos,"tr60":tr60,"vr":vr,"fwd":fwd,"fwd3":fwd3,
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"clv":clv,"rng":rng,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    d=d.dropna(subset=["fwd","pos","tr60","r1"])
    d["trend"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    d["agit"]=np.where(d.vr>1,"agit","calm")
    def summ(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"mean_ex%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    up=d[d.r1>0].copy()
    up["posq"]=pd.cut(up.pos,[-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out={}
    out["up_by_pos_trend"]=up.groupby(["trend","posq"]).apply(summ)
    dn=d[d.r1<0].copy()
    dn["posq"]=pd.cut(dn.pos,[-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out["down_by_pos_trend"]=dn.groupby(["trend","posq"]).apply(summ)
    case=up[(up.pos<-0.6)&(up.trend=="falling")].copy()
    case["r1q"]=pd.qcut(case.r1,3,labels=["small","mid","big"])
    out["case_by_r1size"]=case.groupby("r1q").apply(summ)
    case["clvq"]=pd.cut(case.clv,[0,0.33,0.66,1.0])
    out["case_by_clv"]=case.groupby("clvq").apply(summ)
    out["case_by_agit"]=case.groupby("agit").apply(summ)
    out["case_by_coin"]=case.groupby("coin").apply(summ)
    out["case_by_year"]=case.groupby("yr").apply(summ)
    out["all_by_wd"]=d.groupby("wd").apply(summ)
    # big moves anywhere
    d["z"]=d.r1/d.groupby("coin")["r1"].transform("std")
    d["zq"]=pd.cut(d.z,[-99,-2,-1,1,2,99])
    out["all_by_zmove_trend"]=d.groupby(["trend","zq"]).apply(summ)
    return out
