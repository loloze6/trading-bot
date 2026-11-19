def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r":r,"z":r/sd,"f1":c.shift(-1)/c-1,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "vol":b["volume"].astype(float),
                "vol720":r.rolling(720,min_periods=720).std(),
                "r24":c/c.shift(24)-1,"r4":c/c.shift(4)-1,
                "f4":c.shift(-4)/c-1,"f24":c.shift(-24)/c-1,
                "pos":np.arange(len(b))})
            d["volrel"]=d["vol"]/d["vol"].rolling(168,min_periods=48).median()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["hour"]=D.ts.dt.hour; D["wd"]=D.ts.dt.weekday
    D["year"]=D.ts.dt.year
    cm=D.groupby("coin")["f1"].transform("mean")
    D["ex"]=D["f1"]-cm
    D["rev"]=-np.sign(D["z"])*D["ex"]
    out={}
    def tstat(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    D["zq"]=pd.qcut(D["z"],10,labels=False,duplicates="drop")
    out["next1h_by_z_decile"]=D.groupby("zq").apply(lambda g:pd.Series({"z":g.z.mean(),**tstat(g.ex).to_dict()}))
    out["rev_by_hour"]=D.groupby("hour")["rev"].apply(tstat).unstack()
    out["rev_by_weekday"]=D.groupby("wd")["rev"].apply(tstat).unstack()
    out["rev_by_coin"]=D.groupby("coin")["rev"].apply(tstat).unstack()
    out["rev_by_year"]=D.groupby("year")["rev"].apply(tstat).unstack()
    D["vq"]=D.groupby("coin")["vol720"].transform(lambda s:pd.qcut(s,4,labels=False,duplicates="drop"))
    out["rev_by_vol720_quartile"]=D.groupby("vq")["rev"].apply(tstat).unstack()
    D["vlq"]=pd.qcut(D["volrel"],5,labels=False,duplicates="drop")
    out["rev_by_relvolume_quintile"]=D.groupby("vlq")["rev"].apply(tstat).unstack()
    # 4h grid: next 4h vs last 4h ; 24h grid
    g4=D[D.pos%4==0].copy(); g4["f4ex"]=g4.f4-g4.groupby("coin").f4.transform("mean")
    g4["q"]=pd.qcut(g4.r4,5,labels=False)
    out["next4h_by_last4h_quintile"]=g4.groupby("q")["f4ex"].apply(tstat).unstack()
    g24=D[D.pos%24==0].copy(); g24["f24ex"]=g24.f24-g24.groupby("coin").f24.transform("mean")
    g24["q"]=pd.qcut(g24.r24,5,labels=False)
    out["next24h_by_last24h_quintile"]=g24.groupby("q")["f24ex"].apply(tstat).unstack()
    # hour mean return and volume
    out["hour_mean_ret_and_relvol"]=D.groupby("hour").agg(ret_bp=("ex",lambda x:x.mean()*1e4),relvol=("volrel","median"))
    # funding: hour return vs 24h trend sign
    D["trendrev"]=-np.sign(D["r24"].shift(0))*D["ex"]
    out["against_24h_trend_by_hour"]=D.groupby("hour")["trendrev"].apply(tstat).unstack()
    return out
