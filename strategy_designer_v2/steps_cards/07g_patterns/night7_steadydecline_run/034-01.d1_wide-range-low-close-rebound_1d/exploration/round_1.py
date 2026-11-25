def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            rng=(h-l)
            clv=((c-l)/rng.replace(0,np.nan))
            rr=rng/c
            rmean=rr.shift(1).rolling(60,min_periods=20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "clv":clv,"rw":rr/rmean,"ret0":c.pct_change(),
                "r1":c.shift(-1)/c-1,"r2":c.shift(-2)/c-1,"r3":c.shift(-3)/c-1,
                "ret5":c/c.shift(5)-1,"gap1":o.shift(-1)/c-1,
                "agit":(b["regime"]=="mean_reversion"),
                "fc":b["forecast"].astype(float),"alloc":b["postRebalance_current_allocation"].astype(float)})
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean()
    D["x1"]=D["r1"]-D["coin"].map(mu)
    D["day"]=D["ts"].dt.floor("D")
    def tday(s,df):
        g=df.assign(v=s).dropna(subset=["v"]).groupby("day")["v"].sum()
        n=df["v"].notna().sum() if "v" in df else None
        return g
    def summ(df,col="x1"):
        x=df.dropna(subset=[col])
        if len(x)<10: return pd.Series({"n":len(x),"mean":np.nan,"t_day":np.nan})
        g=x.groupby("day")[col].mean()
        return pd.Series({"n":len(x),"days":len(g),"mean":x[col].mean(),"t_day":g.mean()/(g.std()/np.sqrt(len(g)))})
    out={}
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    out["clv_quint_by_regime"]=D.groupby(["agit","clvq"]).apply(summ).round(4)
    D["rwq"]=pd.qcut(D["rw"],4,labels=False)
    A=D[D.agit]
    out["agit_clv_low_high_by_rangewidth"]=A.assign(cl=(A.clv<0.5)).groupby(["rwq","cl"]).apply(summ).round(4)
    D["r0q"]=pd.qcut(D["ret0"],5,labels=False)
    out["ret0_quint_by_regime"]=D.groupby(["agit","r0q"]).apply(summ).round(4)
    D["r5q"]=pd.qcut(D["ret5"],5,labels=False)
    out["ret5_quint_by_regime"]=D.groupby(["agit","r5q"]).apply(summ).round(4)
    # horizon decay in agitated, low clv quintile vs high, non-overlap grid
    hz={}
    for hh,col in [(1,"r1"),(2,"r2"),(3,"r3")]:
        sub=D[(D.pos%hh==0)].copy()
        m=sub.groupby("coin")[col].mean(); sub["xx"]=sub[col]-sub.coin.map(m)
        for a in [True,False]:
            for q in [0,4]:
                s=sub[(sub.agit==a)&(sub.clvq==q)]
                hz[(hh,a,q)]=summ(s,"xx")
    out["horizon_clv_extremes"]=pd.DataFrame(hz).T.round(4)
    D["wd"]=D["ts"].dt.weekday
    out["weekday"]=D.groupby("wd").apply(summ).round(4)
    out["weekday_agit_lowclv"]=D[D.agit&(D.clv<0.4)].groupby("wd").apply(summ).round(4)
    # gap vs intraday of next day for low-clv agitated
    s=D[D.agit&(D.clvq==0)]
    out["lowclv_agit_gap_mean"]=float(s["gap1"].mean())
    # book days: by coin regime share
    out["agit_share"]=D.groupby("coin")["agit"].mean().round(3)
    # book returns days split by allocation size
    D["held"]=D.alloc.abs()>0
    out["held_next_by_clvq_agit"]=D[D.agit].groupby(["held","clvq"]).apply(summ).round(4)
    return out
