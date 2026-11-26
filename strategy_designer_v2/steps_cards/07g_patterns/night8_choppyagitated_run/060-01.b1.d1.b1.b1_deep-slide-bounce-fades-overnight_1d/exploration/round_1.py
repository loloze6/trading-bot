def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"vol":vol,
                "s1":r1/vol,
                "f5":(c.shift(1)/c.shift(6)-1)/vol.shift(1),
                "fwd1":c.shift(-1)/c-1,
                "fwd3":c.shift(-3)/c-1,
                "pos":np.arange(len(b)),
                "regime":b["regime"].values,
                "alloc":b["postRebalance_current_allocation"].astype(float).values,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "year":pd.to_datetime(b["timestamp"]).dt.year.values,
                "rng":((b["high"]-b["low"])/c).values/vol,
                "clpos":((c-b["low"])/(b["high"]-b["low"])).values})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D").values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["r1"].mean()
    D["x1"]=D["fwd1"]-D["coin"].map(cm)
    D["x3"]=D["fwd3"]-3*D["coin"].map(cm)
    D["prof"]=D["regime"].isin(["mean_reversion","unknown"])
    def summ(g,col="x1"):
        v=g[col].dropna()
        if len(v)<3: return pd.Series({"n":len(v),"mean%":np.nan,"t":np.nan})
        # day-summed t
        s=g.dropna(subset=[col]).groupby("day")[col].mean()
        return pd.Series({"n":len(v),"days":len(s),"mean%":100*v.mean(),"t_day":s.mean()/(s.std()/np.sqrt(len(s)))})
    out={}
    out["regimes"]=D["regime"].value_counts()
    P=D[D.prof]; O=D[~D.prof & D.s1.notna()]
    P=P.assign(q=pd.qcut(P.s1,5,labels=False,duplicates="drop"))
    out["prof_by_s1_quintile_x1"]=P.groupby("q").apply(summ)
    out["prof_s1q_range"]=P.groupby("q")["s1"].agg(["min","max"])
    G3=P[P.pos%3==0]
    out["prof_by_s1_quintile_x3grid"]=G3.groupby("q").apply(lambda g:summ(g,"x3"))
    O=O.assign(q=pd.qcut(O.s1,5,labels=False))
    out["outprof_by_s1_quintile_x1"]=O.groupby("q").apply(summ)
    U=P[(P.r1>0)&(P.f5<0)].copy()
    U["q"]=pd.qcut(U.f5,4,labels=False)
    out["case_by_f5_quartile_x1"]=U.groupby("q").apply(summ)
    U["qs"]=pd.qcut(U.s1,4,labels=False)
    out["case_by_s1_quartile_x1"]=U.groupby("qs").apply(summ)
    out["case_by_clpos_tercile"]=U.assign(k=pd.qcut(U.clpos,3,labels=False)).groupby("k").apply(summ)
    out["prof_upday_f5pos_x1"]=summ(P[(P.r1>0)&(P.f5>=0)])
    out["prof_by_weekday"]=P.groupby("wd").apply(summ)
    out["all_by_weekday"]=D[D.x1.notna()].groupby("wd").apply(summ)
    out["prof_by_range_tercile"]=P.assign(k=pd.qcut(P.rng,3,labels=False)).groupby("k").apply(summ)
    out["prof_by_clpos_tercile"]=P.assign(k=pd.qcut(P.clpos,3,labels=False)).groupby("k").apply(summ)
    out["case_by_year"]=U.groupby("year").apply(summ)
    # book
    bd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            bd.append(t.assign(coin=coin,w=w))
    B=pd.concat(bd)
    B["day"]=pd.to_datetime(B["day"])
    bk=B.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["count","mean","std"])
    pc=B.groupby("coin")["book_return"].agg(["mean","count"])
    pc["sum"]=B.groupby("coin")["book_return"].sum()
    out["book_by_coin"]=pc
    return out
