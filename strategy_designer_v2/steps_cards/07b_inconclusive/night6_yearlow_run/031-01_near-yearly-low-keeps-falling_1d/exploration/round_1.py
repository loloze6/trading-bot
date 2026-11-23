def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            raw=b.get("debug_info.components.low_prox.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(b)
            for H in (5,10,20,40):
                for i in range(0,n-H,H):
                    past20 = c[i]/c[i-20]-1 if i>=20 else np.nan
                    rows.append(dict(coin=coin,w=w,H=H,i=i,yr=yr[i],af=abs(f[i]),raw=raw[i],
                                     ret=c[i+H]/c[i]-1,past20=past20))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","H"])["ret"].transform("mean")
    d["sg"]=-(d["ret"]-d["drift"])
    out={}
    def slope(g):
        g=g.dropna(subset=["af","sg"])
        if len(g)<10 or g["af"].std()==0: return pd.Series(dict(n=len(g)))
        r=stats.linregress(g["af"],g["sg"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr,mean_sg=g["sg"].mean()))
    out["by_horizon"]=d.groupby("H").apply(slope)
    d20=d[d.H==20].copy()
    out["by_coin_20"]=d20.groupby("coin").apply(slope)
    out["by_year_20"]=d20.groupby("yr").apply(slope)
    d20["q"]=pd.qcut(d20["af"].rank(method="first"),5,labels=False)
    out["quintile_20"]=d20.groupby("q").agg(n=("sg","size"),af=("af","mean"),raw=("raw","mean"),
        sg=("sg","mean"),sd=("sg","std"),ret=("ret","mean"))
    for H in (5,10,40):
        dh=d[d.H==H].copy(); dh["q"]=pd.qcut(dh["af"].rank(method="first"),5,labels=False)
        out[f"quintile_{H}"]=dh.groupby("q").agg(n=("sg","size"),sg=("sg","mean"),sd=("sg","std"))
    d20["pastdown"]=np.where(d20["past20"]<0,"past20<0","past20>=0")
    out["by_past20_20"]=d20.groupby("pastdown").apply(slope)
    out["raw_describe"]=d20["raw"].describe()
    out["af_describe"]=d20["af"].describe()
    return out
