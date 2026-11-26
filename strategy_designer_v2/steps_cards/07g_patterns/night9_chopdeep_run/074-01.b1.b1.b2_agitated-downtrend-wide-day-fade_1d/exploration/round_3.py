def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            nxt=c.shift(-1)/c-1
            rr=(b["high"]-b["low"]); ratio=rr/rr.rolling(20,min_periods=20).mean()
            sd20=r.rolling(20,min_periods=20).std()
            sd30=r.rolling(30,min_periods=30).std()
            tr60=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"nxt":nxt,"ratio":ratio,"tr60":tr60,"z":r/sd20.shift(1),
                "inprof":b["regime"]!="chop","sd30":sd30})
            d["agi"]=d["sd30"]>d["sd30"].expanding(30).median()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D["coin"].map(D.groupby("coin")["nxt"].mean())
    D["trend"]=np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling",np.where(D.tr60.notna(),"choppy","na")))
    def dt(g,col="ex"):
        x=g[["day",col]].dropna()
        if len(x)<3: return pd.Series({"n":len(x),"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        m=x[col].mean(); s=(x[col]-m).groupby(x.day).sum(); Dn=len(s)
        se=np.sqrt((s**2).sum()*Dn/(Dn-1))/len(x)
        return pd.Series({"n":len(x),"days":Dn,"mean%":m*100,"t_day":m/se})
    out={}
    U=D[(D.r>0)&D.z.notna()&D.ex.notna()]
    res={}
    for k,g in U.groupby(["trend","inprof"]):
        if len(g)>20:
            rho,p=stats.spearmanr(g.z,g.ex); res[str(k)]={"n":len(g),"spearman_z_ex":rho,"p":p}
    out["up_grading_z_by_trend"]=pd.DataFrame(res).T
    # falling, top-quintile z up days, by window sign consistency
    F=U[(U.trend=="falling")]
    F=F.assign(q=pd.qcut(F.z,4,labels=["q1","q2","q3","q4"]))
    out["falling_up_zq_inprof"]=F.groupby(["inprof","q"]).apply(dt)
    top=F[F.q=="q4"]
    out["falling_topq_by_window"]=top.groupby("w").apply(dt)[["n","mean%"]]
    C=U[(U.trend=="choppy")]
    C=C.assign(q=pd.qcut(C.z,4,labels=["q1","q2","q3","q4"]))
    out["choppy_up_zq_agi"]=C.groupby(["agi","q"]).apply(dt)
    # wide down in-profile grading
    Wd=D[(D.r<=0)&D.inprof&D.ex.notna()&D.ratio.notna()]
    rho,p=stats.spearmanr(Wd.ratio,Wd.ex)
    out["inprof_down_ratio_grading"]=pd.Series({"n":len(Wd),"rho":rho,"p":p})
    return out
