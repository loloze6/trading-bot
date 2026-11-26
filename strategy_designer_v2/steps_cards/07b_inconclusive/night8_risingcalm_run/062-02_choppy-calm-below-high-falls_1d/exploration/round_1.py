def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(b)
            hi5=pd.Series(c).rolling(5,min_periods=5).max().values
            r=pd.Series(c).pct_change()
            sd30=r.rolling(30,min_periods=20).std().values
            raw=(c-hi5)/hi5/sd30
            ts=pd.to_datetime(b["timestamp"])
            for h in (1,3,5,10):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=ts.iloc[i].year,day=ts.iloc[i].normalize(),
                        fc=b["forecast"].iloc[i],raw=raw[i],regime=b["regime"].iloc[i],
                        fwd=c[i+h]/c[i]-1))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    a=d[(d.fc!=0)&d.fc.notna()].copy()
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex_%":g.ex.mean()*100,"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,"mean_raw":g.raw.mean()})
    a5=a[a.h==5].copy()
    a5["fcb"]=pd.cut(a5.fc,[-20.01,-15,-10,-5,-0.01])
    out["by_fc_bucket_h5"]=a5.groupby("fcb").apply(summ)
    a5["rawb"]=pd.qcut(a5.raw.rank(method="first"),4,labels=["q1deep","q2","q3","q4shallow"])
    out["by_raw_quartile_h5"]=a5.groupby("rawb").apply(summ)
    out["by_coin_h5"]=a5.groupby("coin").apply(summ)
    out["by_year_h5"]=a5.groupby("year").apply(summ)
    out["by_h"]=a.groupby("h").apply(summ)
    # slope of ex on raw and fc per horizon
    res={}
    for h,g in a.groupby("h"):
        g=g.dropna(subset=["raw","ex"])
        s1=stats.linregress(g.raw,g.ex); s2=stats.linregress(g.fc,g.ex)
        res[h]=dict(slope_raw=s1.slope,t_raw=s1.slope/s1.stderr,slope_fc=s2.slope,t_fc=s2.slope/s2.stderr,n=len(g))
    out["slopes_by_h"]=pd.DataFrame(res).T
    # in profile with raw==0 (at the high): excess
    inprof=d[(d.h==5)&(d.regime=="unknown")]
    inprof=inprof.copy(); inprof["at_high"]=inprof.raw>=-1e-12
    out["inprofile_athigh_vs_below"]=inprof.groupby("at_high").apply(summ)
    out["fc_raw_corr"]=float(a5[["fc","raw"]].corr().iloc[0,1])
    return out
