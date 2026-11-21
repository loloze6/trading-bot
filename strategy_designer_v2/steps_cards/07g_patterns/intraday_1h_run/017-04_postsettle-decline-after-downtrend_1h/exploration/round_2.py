def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            c=df["close"].values; g.append(c[2::2]/c[:-2:2]-1)
        mu2=np.nanmean(np.concatenate(g))
        for w,df in ws.items():
            d=pd.DataFrame({"ts":pd.to_datetime(df["timestamp"]),"c":df["close"].astype(float),
                            "a":df["postRebalance_current_allocation"].astype(float)})
            d["r72"]=d.c/d.c.shift(72)-1
            m=d.r72.rolling(73,min_periods=20).mean(); s=d.r72.rolling(73,min_periods=20).std()
            d["z"]=(d.r72-m)/s
            d["f2"]=d.c.shift(-2)/d.c-1-mu2
            d["f3"]=d.c.shift(-3)/d.c-1
            d["r1"]=d.c.shift(-1)/d.c-1
            d["pnl"]=d.a*d.r1
            d["hr"]=(d.ts+pd.Timedelta(hours=1)).dt.hour
            d["yr"]=d.ts.dt.year; d["wd"]=(d.ts+pd.Timedelta(hours=1)).dt.dayofweek
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    D=pd.concat(rows)
    out={}
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    E=D.dropna(subset=["f2"])
    out["h21_by_year"]=E[E.hr==21].groupby("yr").f2.apply(tt).unstack().round(2)
    out["h21_by_coin"]=E[E.hr==21].groupby("coin").f2.apply(tt).unstack().round(2)
    out["h21_by_wd"]=E[E.hr==21].groupby("wd").f2.apply(tt).unstack().round(2)
    out["h1_3_f3_by_year"]=D[D.hr==1].groupby("yr").f3.apply(tt).unstack().round(2)
    out["h1_3_f3_by_coin"]=D[D.hr==1].groupby("coin").f3.apply(tt).unstack().round(2)
    def sl(g):
        g=g.dropna(subset=["z","f2"]); g=g[g.z<0]
        r=stats.linregress(g.z,g.f2); return pd.Series({"n":len(g),"slope_bp":r.slope*1e4,"t":r.slope/r.stderr})
    out["h12_13_zneg_by_year"]=E[E.hr.isin([12])].groupby("yr").apply(sl).round(2)
    out["h12_zneg_by_coin"]=E[E.hr==12].groupby("coin").apply(sl).round(2)
    out["book_pnl_by_hour"]=D[D.a.abs()>0].groupby("hr").pnl.apply(tt).unstack().round(2)
    return out
