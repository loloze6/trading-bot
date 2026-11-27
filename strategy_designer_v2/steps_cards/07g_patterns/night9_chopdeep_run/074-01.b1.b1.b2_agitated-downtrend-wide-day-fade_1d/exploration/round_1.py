def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])/c.shift(1)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            nxt2=c.shift(-2)/c.shift(-1)-1
            rr=(b["high"]-b["low"])
            ratio=rr/rr.rolling(20,min_periods=20).mean()
            tr60=c/c.shift(60)-1
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"nxt":nxt,"nxt2":nxt2,"ratio":ratio,
                            "tr60":tr60,"regime":b["regime"],"clpos":clpos,
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(drift)
    D["inprof"]=D["regime"]!="chop"
    D["trend"]=np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling",np.where(D.tr60.notna(),"choppy","na")))
    D["up"]=np.where(D.r>0,"up","down")
    D["wb"]=pd.cut(D.ratio,[0,0.7,1.0,1.4,2.0,99],labels=["<0.7","0.7-1","1-1.4","1.4-2",">2"])
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean_ex%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["inprof_up_width"]=D[D.inprof].groupby(["up","wb"]).apply(summ)
    out["outprof_up_width"]=D[~D.inprof].groupby(["up","wb"]).apply(summ)
    out["trend_up_wide"]=D[(D.ratio>1.0)].groupby(["trend","up","inprof"]).apply(summ)
    W=D[(D.ratio>1)&D.inprof&(D.r>0)]
    W=W.assign(cb=pd.cut(W.clpos,[-0.01,0.33,0.66,1.01],labels=["lowclose","mid","highclose"]))
    out["inprof_wideup_closepos"]=W.groupby("cb").apply(summ)
    W2=D[(D.ratio>1)&(D.r>0)].assign(cb=lambda x: pd.cut(x.clpos,[-0.01,0.33,0.66,1.01],labels=["low","mid","high"]))
    out["all_wideup_closepos_trend"]=W2.groupby(["trend","cb"]).apply(summ)
    out["inprof_wideup_nxt2"]=pd.Series({"mean_nxt2%":W["nxt2"].mean()*100,"t":W["nxt2"].mean()/(W["nxt2"].std()/np.sqrt(W["nxt2"].notna().sum())),"n":W["nxt2"].notna().sum()})
    out["inprof_wideup_by_window"]=W.groupby("w").apply(summ)
    out["inprof_wideup_by_coin"]=W.groupby("coin").apply(summ)
    out["all_by_weekday"]=D.groupby("wd").apply(summ)
    # big moves
    D["rq"]=pd.qcut(D.r,10,labels=False,duplicates="drop")
    out["rdecile_by_trend"]=D.groupby(["trend","rq"]).apply(summ).unstack(0)["mean_ex%"]
    return out
