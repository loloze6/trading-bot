def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 2-bar return on grid
        g=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-2,2)
            g.append(c[idx+2]/c[idx]-1)
        m2=np.nanmean(np.concatenate(g))
        for w,df in ws.items():
            d=pd.DataFrame({"ts":pd.to_datetime(df["timestamp"]),"c":df["close"].astype(float)})
            d["r2"]=d.c.shift(-2)/d.c-1-m2
            d["r1"]=d.c.shift(-1)/d.c-1-m2/2
            p=d.c/d.c.shift(72)-1
            z=(p-p.rolling(72,min_periods=20).mean())/p.rolling(72,min_periods=20).std()
            d["f"]=np.clip(-z,0,None).clip(upper=20)
            d["fall"]=p
            d["hour"]=d.ts.dt.hour; d["year"]=d.ts.dt.year
            d["coin"]=coin; d["win"]=w
            d["fc"]=df["forecast"].values
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r2","f"])
    def stat(x):
        x=x[x.f>0]
        n=len(x)
        if n<30: return pd.Series({"n":n})
        sl=stats.linregress(x.f,x.r2)
        mt=x.r2.mean()/(x.r2.std()/np.sqrt(n))
        return pd.Series({"n":n,"mean_bp":x.r2.mean()*1e4,"mean_t":mt,"slope_bp":sl.slope*1e4,"slope_t":sl.slope/sl.stderr})
    byhour=D.groupby("hour").apply(stat)
    C=D[D.hour.isin([5,13,21])]
    out={"by_hour_all(f>0, 2h excess)":byhour}
    out["cases by coin"]=C.groupby("coin").apply(stat)
    out["cases by year"]=C.groupby("year").apply(stat)
    out["cases by settlement hour"]=C.groupby("hour").apply(stat)
    Cp=C[C.f>0].copy()
    Cp["q"]=pd.qcut(Cp.f,5,labels=False,duplicates="drop")
    out["cases by f quintile"]=Cp.groupby("q").agg(n=("r2","size"),mean_bp=("r2",lambda s:s.mean()*1e4),t=("r2",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    # raw fall size quintiles on all cases with fall<0
    Cf=C[C.fall<0].copy(); Cf["q"]=pd.qcut(Cf.fall,5,labels=False)
    out["cases by raw 3d fall quintile (0=deepest)"]=Cf.groupby("q").agg(n=("r2","size"),fall=("fall","mean"),mean_bp=("r2",lambda s:s.mean()*1e4),t=("r2",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    # check recorded forecast agreement
    out["share fc>0 at cases"]=float((C.fc>0).mean())
    return out
