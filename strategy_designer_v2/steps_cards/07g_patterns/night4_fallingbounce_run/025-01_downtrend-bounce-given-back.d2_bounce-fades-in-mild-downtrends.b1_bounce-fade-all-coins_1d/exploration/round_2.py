def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change(); sd20=r1.rolling(20).std()
            fwd=c.shift(-H)/c-1
            ret20=c/c.shift(20)-1
            volz=df["volume"]/df["volume"].rolling(20).mean()
            f90=df.get("debug_info.components.fall90.last_history_value")
            idx=np.arange(0,len(df),H)
            ts=pd.to_datetime(df["timestamp"]).iloc[idx]
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":idx,"fwd":fwd.iloc[idx].values,
                "ret20s":(ret20/(sd20*np.sqrt(20))).iloc[idx].values,"ret20":ret20.iloc[idx].values,
                "z":(r1/sd20).iloc[idx].values,"volz":volz.iloc[idx].values,
                "f90":(f90.iloc[idx].values if f90 is not None else np.nan),
                "reg":df["regime"].iloc[idx].values,"yr":ts.dt.year.values}))
    A=pd.concat(rows).dropna(subset=["fwd"])
    drift=A.groupby("coin")["fwd"].mean()
    A["u"]=A["fwd"]-A["coin"].map(drift)
    A["down"]=A["reg"]=="mean_reversion"
    res={}
    # regression of u on ret20 scaled, per regime, with per-year slopes
    out=[]
    for d in [False,True]:
        for yr in ["all"]+sorted(A["yr"].unique().tolist()):
            B=A[(A["down"]==d)].dropna(subset=["ret20s"])
            if yr!="all": B=B[B["yr"]==yr]
            if len(B)<30: continue
            s=stats.linregress(B["ret20s"],B["u"])
            out.append({"down":d,"yr":yr,"n":len(B),"slope":s.slope,"t":s.slope/s.stderr,"mean_u":B["u"].mean()})
    res["u_on_ret20scaled_by_regime_year"]=pd.DataFrame(out).round(4)
    # regime mean u, clustered by grid date: average over coins per (w,pos) then t over cells
    cl=A.groupby(["w","pos","down"])["u"].mean().reset_index()
    g=cl.groupby("down")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    res["regime_u_clustered"]=g.round(4)
    # ret20 quintile within down regime, clustered per (w,pos)
    B=A[A["down"]].dropna(subset=["ret20s"]).copy()
    B["q"]=pd.qcut(B["ret20s"],5,labels=False)
    cq=B.groupby(["q","w","pos"])["u"].mean().reset_index()
    g=cq.groupby("q")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["x"]=B.groupby("q")["ret20s"].mean()
    res["down_ret20s_quintile_clustered"]=g.round(4)
    B=A[~A["down"]].dropna(subset=["ret20s"]).copy()
    B["q"]=pd.qcut(B["ret20s"],5,labels=False)
    cq=B.groupby(["q","w","pos"])["u"].mean().reset_index()
    g=cq.groupby("q")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["x"]=B.groupby("q")["ret20s"].mean()
    res["up_ret20s_quintile_clustered"]=g.round(4)
    # fall90 depth within down regime
    B=A[A["down"]].dropna(subset=["f90"]).copy()
    B["q"]=pd.qcut(B["f90"],5,labels=False,duplicates="drop")
    g=B.groupby("q")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["x"]=B.groupby("q")["f90"].mean()
    res["down_fall90_quintile"]=g.round(4)
    # volume ratio in down regime, slope and per year
    out=[]
    for d in [False,True]:
        B=A[A["down"]==d].dropna(subset=["volz"])
        s=stats.linregress(np.log(B["volz"]),B["u"])
        out.append({"down":d,"n":len(B),"slope_logvol":s.slope,"t":s.slope/s.stderr})
    res["u_on_logvolume"]=pd.DataFrame(out).round(4)
    # weekday: cross-coin mean per day, then by weekday and by year
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            d=df.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D).dropna(subset=["coin_return"])
    M=D.groupby(["w","day"])["coin_return"].mean().reset_index()
    M["wd"]=pd.to_datetime(M["day"]).dt.dayofweek; M["yr"]=pd.to_datetime(M["day"]).dt.year
    g=M.groupby("wd")["coin_return"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    res["weekday_crosscoin"]=g.round(5)
    M["wfs"]=M["wd"].isin([2,4,5])
    yy=M.groupby(["yr","wfs"])["coin_return"].mean().unstack()
    yy["diff"]=yy[True]-yy[False]
    res["wed_fri_sat_minus_rest_by_year"]=yy.round(5)
    # by coin
    D["wfs"]=pd.to_datetime(D["day"]).dt.dayofweek.isin([2,4,5])
    cc=D.groupby(["coin","wfs"])["coin_return"].mean().unstack(); cc["diff"]=cc[True]-cc[False]
    res["wfs_diff_by_coin"]=cc[["diff"]].round(5)
    return res
