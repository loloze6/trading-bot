def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=b["high"]-b["low"]
            r1=c.pct_change()
            rm=rng/rng.rolling(20,min_periods=20).mean()
            body=(c-b["open"])/rng.replace(0,np.nan)
            clpos=(c-b["low"])/rng.replace(0,np.nan)
            nxt=c.shift(-1)/c-1
            nx3=c.shift(-3)/c-1
            vol20=r1.rolling(20).std()
            df=pd.DataFrame({"coin":coin,"w":w,"day":b["timestamp"].dt.floor("D"),
                "wd":b["timestamp"].dt.dayofweek,"r1":r1,"rm":rm,"clpos":clpos,
                "nxt":nxt,"nx3":nx3,"vol20":vol20,"falling":(b["regime"]!="chop"),
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].transform("mean")
    d["un"]=d["nxt"]-drift
    d["unz"]=d["un"]/d.groupby("coin")["nxt"].transform("std")
    d=d.dropna(subset=["un","rm","r1"])
    def summ(g):
        s=g.groupby("day")["un"].sum(); n=g["day"].nunique()
        t=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":n,"mean_un":g["un"].mean(),"t_day":t,"mean_z":g["unz"].mean()})
    d["up"]=np.where(d["r1"]>0,"up","down")
    d["rmq"]=pd.cut(d["rm"],[0,0.6,0.8,1.0,1.3,1.7,10])
    d["prof"]=np.where(d["falling"],"falling","notfalling")
    out={}
    out["by_prof_dir_width"]=d.groupby(["prof","up","rmq"]).apply(summ)
    # close position within range for wide days
    d["cq"]=pd.cut(d["clpos"],[-0.01,0.2,0.4,0.6,0.8,1.01])
    wide=d[d["rm"]>=1.3]
    out["wide_by_prof_closepos"]=wide.groupby(["prof","cq"]).apply(summ)
    out["by_prof_weekday"]=d.groupby(["prof","wd"]).apply(summ)
    d["r1q"]=pd.qcut(d["r1"]/d["vol20"],7,duplicates="drop")
    out["by_prof_scaled_r1"]=d.groupby(["prof","r1q"]).apply(summ)
    # 3-day after, wide up falling
    f=d[(d.prof=="falling")&(d.up=="up")]
    out["falling_up_next3_by_width"]=f.groupby("rmq")["nx3"].agg(["count","mean"])
    out["window_falling_wideup"]=d[(d.prof=="falling")&(d.up=="up")&(d.rm>=1)].groupby("w").apply(summ)
    return out
