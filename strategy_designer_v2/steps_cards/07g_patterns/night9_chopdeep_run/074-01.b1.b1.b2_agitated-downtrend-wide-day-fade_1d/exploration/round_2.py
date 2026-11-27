def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            nxt=c.shift(-1)/c-1
            nxt2=c.shift(-2)/c.shift(-1)-1
            nxt3=c.shift(-3)/c-1
            rr=(b["high"]-b["low"]); ratio=rr/rr.rolling(20,min_periods=20).mean()
            sd30=r.rolling(30,min_periods=30).std()
            sd20=r.rolling(20,min_periods=20).std()
            tr60=c/c.shift(60)-1
            clpos=(c-b["low"])/rr.replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"nxt":nxt,"nxt2":nxt2,"nxt3":nxt3,"ratio":ratio,"tr60":tr60,
                "z":r/sd20.shift(1),"sd30":sd30,"inprof":b["regime"]!="chop","clpos":clpos})
            # agitation proxy within window: sd30 vs its expanding median in-window (rough)
            d["agi"]=d["sd30"]>d["sd30"].expanding(30).median()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in ["nxt","nxt2","nxt3"]:
        D["ex_"+k]=D[k]-D["coin"].map(D.groupby("coin")[k].mean())
    D["trend"]=np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling",np.where(D.tr60.notna(),"choppy","na")))
    def dt(g,col="ex_nxt"):
        x=g[["day",col]].dropna()
        if len(x)<3: return pd.Series({"n":len(x),"days":x.day.nunique(),"mean%":np.nan,"t_day":np.nan})
        m=x[col].mean(); s=(x[col]-m).groupby(x.day).sum(); Dn=len(s)
        se=np.sqrt((s**2).sum()*Dn/(Dn-1))/len(x)
        return pd.Series({"n":len(x),"days":Dn,"mean%":m*100,"t_day":m/se})
    out={}
    up=D[(D.r>0)&D.z.notna()]
    up=up.assign(zb=pd.cut(up.z,[0,0.5,1,1.5,2.5,99],labels=["0-.5",".5-1","1-1.5","1.5-2.5",">2.5"]))
    out["up_z_by_trend_inprof"]=up.groupby(["trend","inprof","zb"]).apply(dt).unstack(0)["mean%"] if False else up[up.trend.isin(["falling","choppy"])].groupby(["trend","inprof","zb"]).apply(dt)
    out["choppy_up_z_by_agi"]=up[up.trend=="choppy"].groupby(["agi","zb"]).apply(dt)
    W=D[(D.ratio>1)&D.inprof&(D.r>0)]
    out["inprof_wideup_day2_day3"]=pd.DataFrame({k:dt(W,"ex_"+k) for k in ["nxt","nxt2","nxt3"]}).T
    Wd=D[(D.ratio>1)&D.inprof&(D.r<=0)]
    out["inprof_widedown_day2_day3"]=pd.DataFrame({k:dt(Wd,"ex_"+k) for k in ["nxt","nxt2","nxt3"]}).T
    # in profile wide up: grading by return size vs width
    W=W.assign(rb=pd.qcut(W.r,3,labels=["smallr","midr","bigr"]),wbb=pd.qcut(W.ratio,3,labels=["lw","mw","hw"]))
    out["inprof_wideup_by_rsize"]=W.groupby("rb").apply(dt)
    out["inprof_wideup_by_width"]=W.groupby("wbb").apply(dt)
    # falling calm vs agitated wide up
    F=D[(D.trend=="falling")&(D.ratio>1)&(D.r>0)]
    out["falling_wideup_by_agi_inprof"]=F.groupby(["inprof"]).apply(dt)
    return out
