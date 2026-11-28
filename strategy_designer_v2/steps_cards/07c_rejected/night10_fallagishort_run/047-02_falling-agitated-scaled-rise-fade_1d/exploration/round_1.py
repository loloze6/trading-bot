def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            z=r/sd
            raw=b.get("debug_info.components.scaled_rise.last_history_value")
            for h in [1,2,3,5,10]:
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,len(b),h)
                for i in idx:
                    if i+h>=len(b): continue
                    rows.append(dict(coin=coin,w=w,h=h,z=z.iloc[i],ret=fwd.iloc[i],
                        inprof=b["regime"].iloc[i]=="unknown",r1=r.iloc[i],
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    drift=d.groupby(["coin","h"])["ret"].mean().rename("drift")
    d=d.join(drift,on=["coin","h"]); d["unus"]=d["ret"]-d["drift"]
    d=d.dropna(subset=["z","unus"])
    d["zb"]=pd.cut(d["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    def agg(g):
        m=g["unus"].mean(); s=g["unus"].std(); n=len(g)
        return pd.Series({"n":n,"mean_unus":m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["by_h_prof_zb"]=d[d.h.isin([1,3,5])].groupby(["h","inprof","zb"]).apply(agg).unstack(0)
    # slope of unusual on z, by h and profile
    sl=[]
    for (h,p),g in d.groupby(["h","inprof"]):
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(h=h,inprof=p,n=len(g),slope=res.slope,t=res.slope/res.stderr))
    out["slope_z"]=pd.DataFrame(sl)
    up=d[(d.h==3)&d.inprof&(d.z>0)]
    out["up_inprof_h3_by_coin"]=up.groupby("coin").apply(agg)
    out["up_inprof_h3_by_year"]=up.groupby("year").apply(agg)
    out["inprof_share"]=d[d.h==1].groupby("coin")["inprof"].mean()
    return out
