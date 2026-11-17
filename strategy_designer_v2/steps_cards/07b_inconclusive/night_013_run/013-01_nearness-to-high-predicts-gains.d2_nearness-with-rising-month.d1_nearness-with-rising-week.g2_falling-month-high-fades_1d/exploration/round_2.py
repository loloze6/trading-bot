def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            ret30=pd.Series(c).pct_change(30).values
            ret7=pd.Series(c).pct_change(7).values
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            raw=df.get("debug_info.components.dist_high.last_history_value")
            raw=raw.values if raw is not None else np.full(n,np.nan)
            for h in [3,7,14]:
                for i in range(0,n-h,h):
                    act=(ret30[i]<0) if not np.isnan(ret30[i]) else (df["regime"].iloc[i]=="mean_reversion")
                    rows.append(dict(coin=coin,w=w,h=h,fwd=c[i+h]/c[i]-1,act=act,fc=df["forecast"].iloc[i],
                                     raw=raw[i],yr=yr[i],r30=ret30[i],r7=ret7[i]))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby(["coin","h"])["fwd"].transform("mean")
    a=d[d.act & d.fc.notna() & d.raw.notna()].copy()
    out={}
    out["raw_describe"]=a[a.h==7].raw.describe()
    out["corr_fc_raw"]=float(a[a.h==7][["fc","raw"]].corr().iloc[0,1])
    def sl(g,x):
        if len(g)<10 or g[x].std()==0: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        s=stats.linregress(g[x],g.ex); return pd.Series(dict(n=len(g),slope=s.slope,t=s.slope/s.stderr))
    out["raw_by_h"]=a.groupby("h").apply(lambda g: sl(g,"raw"))
    a7=a[a.h==7].copy()
    a7["q"]=pd.qcut(a7.raw.rank(method="first"),3,labels=False)
    out["raw_terc7"]=a7.groupby("q").agg(n=("ex","size"),raw=("raw","mean"),ex=("ex","mean"),sd=("ex","std"))
    out["raw_by_coin7"]=a7.groupby("coin").apply(lambda g: sl(g,"raw"))
    out["raw_by_year7"]=a7.groupby("yr").apply(lambda g: sl(g,"raw"))
    a7["r7s"]=np.where(a7.r7<0,"week_down","week_up")
    out["raw_by_week7"]=a7.groupby("r7s").apply(lambda g: sl(g,"raw"))
    out["fc_by_week7"]=a7.groupby("r7s").apply(lambda g: sl(g,"fc"))
    out["mean_ex_active7"]=pd.Series(dict(mean=a7.ex.mean(),t=a7.ex.mean()/(a7.ex.std()/np.sqrt(len(a7))),n=len(a7)))
    return out
