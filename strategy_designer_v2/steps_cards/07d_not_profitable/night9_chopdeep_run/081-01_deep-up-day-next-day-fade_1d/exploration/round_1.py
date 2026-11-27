def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r.rolling(20,min_periods=20).std()
            depth=(c-hi)/hi/sd
            tr60=c/c.shift(60)-1
            n=len(b)
            for h in [1,2,3,5]:
                b[f"f{h}"]=c.shift(-h)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"r":r,"depth":depth,
                "rawdepth":b.get("debug_info.components.depth.last_history_value"),
                "alloc":b["postRebalance_current_allocation"],"prev":b["previous_allocation"],
                "tr60":tr60,"f1":b["f1"],"f2":b["f2"],"f3":b["f3"],"f5":b["f5"]})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    mu={h:D[f"f{h}"].mean() for h in [1,2,3,5]}  # approx drift (overlapping, fine for mean)
    D["up"]=D["r"]>0
    out={}
    U=D[D.up & D.depth.notna() & D.f1.notna()].copy()
    U["q"]=pd.qcut(U.depth,5,labels=["q1deep","q2","q3","q4","q5shallow"])
    g=U.groupby("q").agg(n=("f1","size"),depth=("depth","mean"),f1=("f1","mean"),f2=("f2","mean"),f3=("f3","mean"),f5=("f5","mean"))
    out["up_by_depth_quintile_fwd_returns"]=g
    Dn=D[(~D.up)&D.depth.notna()&D.f1.notna()].copy()
    Dn["q"]=pd.qcut(Dn.depth,5,labels=["q1deep","q2","q3","q4","q5shallow"])
    out["down_by_depth_quintile"]=Dn.groupby("q").agg(n=("f1","size"),f1=("f1","mean"),f3=("f3","mean"))
    out["drift"]=pd.Series(mu)
    # trend
    U["trend"]=pd.cut(U.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["up_q_by_trend_f1"]=U.groupby(["trend","q"]).f1.agg(["size","mean"]).unstack()
    t2=D[D.f1.notna()].copy(); t2["trend"]=pd.cut(t2.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["all_bars_by_trend_f1"]=t2.groupby("trend").f1.agg(["size","mean"])
    # up-day size
    U["upsz"]=pd.qcut(U.r,3,labels=["small","mid","big"])
    out["deep_half_by_upsize_f1"]=U[U.depth<U.depth.median()].groupby("upsz").f1.agg(["size","mean"])
    # position gain per bar on short days & by window
    D["gain"]=D.alloc*D.f1
    D["turn"]=(D.alloc-D.prev).abs()
    out["book_gain_turnover_by_window"]=D.groupby("w").agg(gain=("gain","mean"),turn=("turn","mean"),held=("alloc",lambda x:(x!=0).mean()))
    out["mean_abs_alloc_when_held"]=float(D.loc[D.alloc!=0,"alloc"].abs().mean())
    out["share_active_days_followed_by_flat"]=float(((D.alloc!=0)&(D.groupby(["coin","w"]).alloc.shift(-1)==0)).sum()/(D.alloc!=0).sum())
    return out
