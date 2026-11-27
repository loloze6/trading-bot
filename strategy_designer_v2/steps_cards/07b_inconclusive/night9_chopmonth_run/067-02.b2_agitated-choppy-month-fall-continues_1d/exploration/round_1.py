def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,ret=c[i+h]/c[i]-1,fc=b["forecast"].iloc[i],
                        reg=b["regime"].iloc[i],raw=b.get("debug_info.components.fall30.last_history_value",pd.Series([np.nan]*n)).iloc[i],
                        r30=r30[i],yr=pd.to_datetime(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["ex"]=d["ret"]-d["drift"]
    out={}
    def summ(g):
        x=-g["ex"]; n=len(x)
        sl=stats.linregress(g["fc"],g["ex"]) if n>5 and g["fc"].std()>0 else None
        return pd.Series(dict(n=n,short_unusual=x.mean(),t=x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,
                              slope_t=(sl.slope/sl.stderr) if sl is not None else np.nan))
    s=d[d.fc<0]
    out["by_h"]=s.groupby("h").apply(summ)
    s7=s[s.h==7].copy()
    out["by_year"]=s7.groupby("yr").apply(summ)
    out["by_coin"]=s7.groupby("coin").apply(summ)
    s7["q"]=pd.qcut(s7["fc"],3,labels=["deep","mid","shallow"])
    out["by_tercile"]=s7.groupby("q").apply(summ)
    # in profile, rises (unknown regime, forecast 0)
    u=d[(d.h==7)&(d.reg=="unknown")].copy()
    u["side"]=np.where(u.raw<0,"fall","rise")
    def lsumm(g):
        x=g["ex"]; n=len(x)
        sl=stats.linregress(g["raw"],g["ex"]) if n>5 else None
        return pd.Series(dict(n=n,mean_ex=x.mean(),t=x.mean()/(x.std()/np.sqrt(n)),slope_t=sl.slope/sl.stderr if sl else np.nan))
    out["inprofile_by_side_raw"]=u.groupby("side").apply(lsumm)
    # outside profile: 30d return falls, by regime
    o=d[(d.h==7)&d.r30.notna()].copy()
    o["inprof"]=o.reg=="unknown"
    o["side"]=np.where(o.r30<0,"fall","rise")
    def osumm(g):
        x=g["ex"]; n=len(x)
        sl=stats.linregress(g["r30"],g["ex"])
        return pd.Series(dict(n=n,mean_ex=x.mean(),slope=sl.slope,slope_t=sl.slope/sl.stderr))
    out["r30_by_profile_side"]=o.groupby(["inprof","side"]).apply(osumm)
    out["regimes"]=d[d.h==7]["reg"].value_counts()
    return out
