def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sc=r.abs().shift(1).rolling(60,min_periods=20).mean()
            vol20=r.rolling(20,min_periods=10).std()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.dayofweek,"year":ts.dt.year,"z":r/sc,"r":r,
                            "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"vol20":vol20,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["x1"]=D["f1"]-D.groupby("coin")["f1"].transform("mean")
    def slope(g,y="x1",x="z"):
        g=g[[x,y]].dropna()
        if len(g)<30: return pd.Series({"n":len(g)})
        res=stats.linregress(g[x],g[y])
        return pd.Series({"n":len(g),"slope_bp":res.slope*1e4,"t":res.slope/res.stderr})
    out={}
    A=D.dropna(subset=["z","x1","vol20"]).copy()
    A["volq"]=A.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    A["wkend"]=A.wd.isin([5,6])
    out["volterc_x_weekend_slope"]=A.groupby(["wkend","volq"]).apply(slope)
    out["highvol_weekday_only_by_year"]=A[(A.volq==2)&(~A.wkend)].groupby("year").apply(slope)
    out["lowvol_weekday_only_by_year"]=A[(A.volq==0)&(~A.wkend)].groupby("year").apply(slope)
    # graded: z * vol interaction on weekdays
    W=A[~A.wkend].copy()
    W["zv"]=W["z"]*W.groupby("coin")["vol20"].transform(lambda s:(s-s.mean())/s.std())
    X=W[["z","zv"]].values; X=np.column_stack([np.ones(len(X)),X]); y=W["x1"].values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["weekday_interaction_z_zxvol"]=pd.DataFrame({"coef_bp":beta*1e4,"t":beta/se},index=["const","z","z_x_volz"])
    # Saturday own-return by year and per coin
    S=D[D.wd==5].dropna(subset=["r"])
    f=lambda s:pd.Series({"n":s.count(),"mean_bp":s.mean()*1e4,"t":s.mean()/s.std()*np.sqrt(s.count())})
    out["sat_ret_by_year"]=S.groupby("year")["r"].apply(f).unstack()
    out["sat_ret_by_coin"]=S.groupby("coin")["r"].apply(f).unstack()
    out["wed_ret_by_year"]=D[D.wd==2].dropna(subset=["r"]).groupby("year")["r"].apply(f).unstack()
    out["fri_signal_slope_by_year"]=D[D.wd==4].groupby("year").apply(slope)
    out["sat_signal_slope_by_year"]=D[D.wd==5].groupby("year").apply(slope)
    return out
