def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std()
            v=b["volume"].astype(float)
            vr=v/v.rolling(20,min_periods=15).mean()
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"wd":ts.dt.weekday,"r":r,"z":r/vol,"vol":vol,
                            "vr":vr,"f1":f1,"f2":f2,"f5":f5,"r5":c/c.shift(5)-1,"r20":c/c.shift(20)-1,
                            "alloc":b["postRebalance_current_allocation"].astype(float),"fc":b["forecast"].astype(float),
                            "year":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in ["f1","f2","f5"]:
        D[h+"x"]=D[h]-D.groupby("coin")[h].transform("mean")
    out={}
    # reversal by weekday: next 1 day (every bar independent at h=1)
    def stat(g,col):
        x=(-np.sign(g["z"])*g[col]).dropna()
        sl=stats.linregress(g.dropna(subset=["z",col])["z"].clip(-4,4),g.dropna(subset=["z",col])[col]) if len(x)>10 else None
        return pd.Series({"n":len(x),"mean_fade":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"slope":sl.slope if sl else np.nan,"slope_t":sl.slope/sl.stderr if sl else np.nan})
    out["fade_1d_by_weekday"]=D.groupby("wd").apply(lambda g:stat(g,"f1x"))
    # 2d on even grid
    G=D[D.pos%2==0]
    out["fade_2d_by_weekday_grid"]=G.groupby("wd").apply(lambda g:stat(g,"f2x"))
    # Sunday: vol-ratio terciles
    S=D[D.wd==6].copy()
    S["vrq"]=pd.qcut(S["vr"],3,labels=["lowvol","mid","highvol"])
    out["sun_fade1_by_volume"]=S.groupby("vrq").apply(lambda g:stat(g,"f1x"))
    S["zq"]=pd.qcut(S["z"],5,labels=False)
    out["sun_f1x_by_zquint"]=S.groupby("zq")[["z","f1x","f2x"]].mean()
    # all days: z quintile by volatility tercile on next 1d
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["fade1_by_voltercile"]=D.groupby("volq").apply(lambda g:stat(g,"f1x"))
    # 5d return and next 1d/5d
    G5=D[D.pos%5==0].copy()
    G5["z5"]=G5["r5"]/(G5["vol"]*np.sqrt(5))
    G5["q"]=pd.qcut(G5["z5"],5,labels=False)
    out["next5_by_past5_quint"]=G5.groupby("q").agg(n=("f5x","count"),z5=("z5","mean"),f5x=("f5x","mean"),sd=("f5x","std"))
    # weekday mean returns (next day) 
    out["next1_by_weekday_mean"]=D.groupby("wd")["f1x"].agg(["count","mean","std"]).assign(t=lambda x:x["mean"]/x["std"]*np.sqrt(x["count"]))
    # book by weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; dd.append(t)
    DD=pd.concat(dd); DD["wd"]=pd.to_datetime(DD["day"]).dt.weekday
    out["book_ret_by_weekday"]=DD.groupby("wd")[["book_return","coin_return"]].mean()
    out["sun_fade1_by_year"]=S.groupby("year").apply(lambda g:stat(g,"f1x"))
    return out
