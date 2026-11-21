def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 2-bar return over non-overlapping grid
        g=[]
        for w,df in ws.items():
            c=df["close"].values
            r=c[2::2]/c[:-2:2]-1
            g.append(r)
        mu2=np.nanmean(np.concatenate(g))
        for w,df in ws.items():
            d=pd.DataFrame({"ts":pd.to_datetime(df["timestamp"]),"c":df["close"].astype(float),"v":df["volume"].astype(float)})
            d["r72"]=d.c/d.c.shift(72)-1
            m=d.r72.rolling(73,min_periods=20).mean(); s=d.r72.rolling(73,min_periods=20).std()
            d["z"]=(d.r72-m)/s
            d["f2"]=d.c.shift(-2)/d.c-1-mu2
            d["p2"]=d.c/d.c.shift(2)-1-mu2
            d["r24"]=d.c/d.c.shift(24)-1
            d["vrel"]=d.v/d.v.rolling(168,min_periods=48).median()
            d["hr"]=(d.ts+pd.Timedelta(hours=1)).dt.hour
            d["yr"]=d.ts.dt.year
            d["coin"]=coin; d["w"]=w
            rows.append(d.dropna(subset=["z","f2"]))
    D=pd.concat(rows)
    out={}
    def sl(x,y):
        if len(x)<30: return (np.nan,np.nan)
        r=stats.linregress(x,y); return (r.slope*1e4, r.slope/r.stderr)
    res=[]
    for h,g in D.groupby("hr"):
        neg=g[g.z<0]
        s_all=sl(g.z,g.f2); s_neg=sl(neg.z,neg.f2)
        s_p=sl(g.z,g.p2.fillna(0))
        res.append(dict(hr=h,n=len(g),meanf2_bp=g.f2.mean()*1e4,t_mean=stats.ttest_1samp(g.f2,0).statistic,
            slope_z_bp=s_all[0],t_slope=s_all[1],slope_zneg_bp=s_neg[0],t_zneg=s_neg[1],vrel=g.vrel.median()))
    out["by_close_hour"]=pd.DataFrame(res).round(3)
    D["settle"]=D.hr.isin([0,8,16])
    res=[]
    for (st,y),g in D.groupby(["settle","yr"]):
        s=sl(g.z,g.f2); res.append(dict(settle=st,yr=y,n=len(g),slope_bp=s[0],t=s[1]))
    out["slope_by_year"]=pd.DataFrame(res).round(3)
    res=[]
    for (st,cn),g in D.groupby(["settle","coin"]):
        s=sl(g.z,g.f2); res.append(dict(settle=st,coin=cn,n=len(g),slope_bp=s[0],t=s[1]))
    out["slope_by_coin"]=pd.DataFrame(res).round(3)
    # z quintiles at settle vs other
    D["zq"]=pd.qcut(D.z,5,labels=False)
    out["f2_by_zq_settle"]=(D.groupby(["settle","zq"]).f2.agg(["count","mean","std"]).assign(mean_bp=lambda x:x["mean"]*1e4,t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))).round(3)
    return out
