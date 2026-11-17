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
            vol90=r.rolling(90,min_periods=40).std()
            v=b["volume"].astype(float)
            vr=v/v.rolling(20,min_periods=15).mean()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"wd":ts.dt.weekday,"r":r,"z":r/vol,"vol":vol,
                            "vrel":vol/vol90,"vr":vr,"f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,
                            "year":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in ["f1","f2","f3"]:
        D[h+"x"]=D[h]-D.groupby("coin")[h].transform("mean")
    D["fade1"]=-np.sign(D["z"])*D["f1x"]
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    D["vrelq"]=pd.qcut(D["vrel"],3,labels=False)
    out={}
    def st(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    # high-vol fade by weekday, excluding nothing
    out["fade1_volq_x_weekday_t"]=D.groupby(["volq","wd"])["fade1"].apply(lambda x:st(x)["t"]).unstack()
    out["fade1_volq_x_weekday_mean"]=D.groupby(["volq","wd"])["fade1"].mean().unstack()
    # vol relative to own 90d (known at close)
    out["fade1_by_vrel_tercile"]=D.groupby("vrelq")["fade1"].apply(st).unstack()
    # graded: z quintile within high-vol tercile, all weekdays except Sunday
    H=D[(D.volq==2)&(D.wd!=6)].copy()
    H["zq"]=pd.qcut(H["z"],5,labels=False)
    out["highvol_nonSun_by_zquint"]=H.groupby("zq").agg(n=("f1x","count"),z=("z","mean"),f1x=("f1x","mean"))
    # high-vol fade by year
    out["highvol_fade1_by_year"]=D[D.volq==2].groupby("year")["fade1"].apply(st).unstack()
    out["lowvol_fade1_by_year"]=D[D.volq==0].groupby("year")["fade1"].apply(st).unstack()
    # per coin high-vol fade
    pc=D[D.volq==2].groupby("coin")["fade1"].apply(st).unstack()
    out["highvol_per_coin"]=pc
    # 2d / 3d on grid for high vol
    for h,k in [("f2x",2),("f3x",3)]:
        G=D[(D.pos%k==0)]
        G=G.assign(fd=-np.sign(G["z"])*G[h])
        out["fade_"+h+"_by_volq_grid"]=G.groupby("volq")["fd"].apply(st).unstack()
    # Welch: Sunday high volume vs low volume fade
    S=D[D.wd==6].copy()
    S["vrq"]=pd.qcut(S["vr"],3,labels=False)
    a=S[S.vrq==2]["fade1"].dropna(); b_=S[S.vrq==0]["fade1"].dropna()
    out["sun_highvolume_minus_low_welch_t"]=float(stats.ttest_ind(a,b_,equal_var=False).statistic)
    # all days: volume ratio tercile fade
    D["vrq"]=pd.qcut(D["vr"],3,labels=False)
    out["fade1_by_volume_tercile_all"]=D.groupby("vrq")["fade1"].apply(st).unstack()
    # Sunday vs other days within high-vol: Welch
    hv=D[D.volq==2]
    out["highvol_sun_minus_other_welch_t"]=float(stats.ttest_ind(hv[hv.wd==6]["fade1"].dropna(),hv[hv.wd!=6]["fade1"].dropna(),equal_var=False).statistic)
    # weekend (Sat+Sun bars) vs weekday in all
    out["weekend_minus_weekday_fade1_welch_t"]=float(stats.ttest_ind(D[D.wd>=5]["fade1"].dropna(),D[D.wd<5]["fade1"].dropna(),equal_var=False).statistic)
    return out
