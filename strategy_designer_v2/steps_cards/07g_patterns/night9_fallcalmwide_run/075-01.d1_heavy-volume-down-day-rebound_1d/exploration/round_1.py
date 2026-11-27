def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            nxt2=c.shift(-2)/c-1
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()
            rng=(b["high"]-b["low"])/c.shift(1)
            pos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            vol20=r.rolling(20,min_periods=15).std()
            tr60=c/c.shift(60)-1
            r5=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"w":w,"r":r,"nxt":nxt,"nxt2":nxt2,"vr":vr,"rng":rng,"pos":pos,
                             "z":r/vol20,"tr60":tr60,"r5":r5,
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].transform("mean")
    d["ex"]=d["nxt"]-drift
    d=d.dropna(subset=["nxt","r","vr"])
    def agg(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"mean_ex%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    d["down"]=np.where(d["r"]<0,"down","up")
    d["vrq"]=pd.qcut(np.log(d["vr"]),5,labels=["q1light","q2","q3","q4","q5heavy"])
    out={}
    out["dir_x_volq"]=d.groupby(["down","vrq"]).apply(agg)
    dd=d[d.r<0].copy()
    dd["zq"]=pd.qcut(dd["z"],4,labels=["bigfall","f2","f3","smallfall"])
    out["down_zq_x_heavy"]=dd.groupby(["zq",dd["vr"]>1]).apply(agg)
    dd["posq"]=pd.qcut(dd["pos"],3,labels=["lowclose","mid","highclose"])
    out["down_close_pos_x_heavy"]=dd.groupby(["posq",dd["vr"]>1]).apply(agg)
    d["trend"]=pd.cut(d["tr60"],[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["trend_dir_heavy"]=d[d.vr>1].groupby(["trend","down"]).apply(agg)
    out["trend_dir_light"]=d[d.vr<=1].groupby(["trend","down"]).apply(agg)
    up=d[d.r>0].copy()
    up["posq"]=pd.qcut(up["pos"],3,labels=["lowclose","mid","highclose"])
    out["up_heavy_by_closepos"]=up[up.vr>1.5].groupby("posq").apply(agg)
    out["weekday_all"]=d.groupby("wd").apply(agg)
    out["year_heavydown"]=d[(d.r<0)&(d.vr>1)].groupby("yr").apply(agg)
    # 2-day after heavy down
    hd=d[(d.r<0)&(d.vr>1)]
    out["heavydown_nxt2_mean%"]=100*hd["nxt2"].mean()
    out["r5q_heavy_down"]=hd.assign(q=pd.qcut(hd["r5"],4,labels=["r5low","2","3","r5high"])).groupby("q").apply(agg)
    return out
