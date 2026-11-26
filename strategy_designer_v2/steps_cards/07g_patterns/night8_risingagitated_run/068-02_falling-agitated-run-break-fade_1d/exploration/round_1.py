def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            sgn=np.sign(r)
            # prior down run before today (unbroken down days ending yesterday)
            dn=[];up=[];cd=0;cu=0
            for s in sgn.shift(1).fillna(0).values:
                cd=cd+1 if s<0 else 0
                cu=cu+1 if s>0 else 0
                dn.append(cd);up.append(cu)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            pos=(b["close"]-b["low"])/rng
            vol=r.rolling(20).std()
            r3=c/c.shift(3)-1
            df=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"r":r,"nxt":nxt,
                             "dn":dn,"up":up,"pos":pos,"zr":r/vol,"r3z":r3/(vol*np.sqrt(3)),
                             "inprof":(b["regime"]!="chop"),"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r","nxt"])
    drift=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-drift
    def summ(g):
        def f(x):
            s=x.groupby("ts")["ex"].sum(); n=len(x)
            m=x["ex"].mean()
            se=s.std(ddof=1)*np.sqrt(len(s))/n if len(s)>1 else np.nan
            return pd.Series({"n":n,"days":len(s),"mean_ex%":100*m,"t":m/se if se else np.nan})
        return g.apply(f)
    out={}
    P=d[d.inprof]; O=d[~d.inprof]
    out["share_in_profile"]=float(d.inprof.mean())
    P=P.assign(dir=np.where(P.r>0,"up","down"))
    P["dnb"]=pd.cut(P.dn,[-1,0,1,2,30],labels=["0","1","2","3+"])
    P["upb"]=pd.cut(P.up,[-1,0,1,2,30],labels=["0","1","2","3+"])
    out["prof_dir_x_priordownrun"]=summ(P.groupby(["dir","dnb"]))
    out["prof_dir_x_prioruprun"]=summ(P.groupby(["dir","upb"]))
    P["zq"]=pd.qcut(P.zr,5,labels=False)
    out["prof_today_z_quintile"]=summ(P.groupby("zq"))
    P["r3q"]=pd.qcut(P.r3z,5,labels=False)
    out["prof_3day_z_quintile"]=summ(P.groupby("r3q"))
    P["posq"]=pd.qcut(P.pos,5,labels=False,duplicates="drop")
    out["prof_dir_x_closepos"]=summ(P.groupby(["dir","posq"]))
    out["prof_weekday"]=summ(P.groupby("wd"))
    O=O.assign(dir=np.where(O.r>0,"up","down"))
    O["dnb"]=pd.cut(O.dn,[-1,0,1,2,30],labels=["0","1","2","3+"])
    out["outprof_dir_x_priordownrun"]=summ(O.groupby(["dir","dnb"]))
    O["zq"]=pd.qcut(O.zr,5,labels=False)
    out["outprof_today_z_quintile"]=summ(O.groupby("zq"))
    out["prof_by_window_upday"]=summ(P[P.dir=="up"].groupby("w"))
    return out
