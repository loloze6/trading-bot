def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            z=(c/c.shift(14)-1)/(sd*np.sqrt(14))
            f7=c.shift(-7)/c-1
            f1=r.shift(-1)
            r1z=r/sd.shift(1)
            ret60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"f7":f7,"f1":f1,"r1z":r1z,
                             "inprof":b["regime"].isin(["unknown","mean_reversion"]).values,
                             "regime":b["regime"].values,"sd":sd,"ret60":ret60,
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday.values})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    g=d[d.pos%7==0].dropna(subset=["f7"]).copy()
    drift=g.groupby("coin").f7.mean()
    g["u"]=g.f7-g.coin.map(drift)
    out={}
    out["regime_share"]=d.regime.value_counts(normalize=True)
    gz=g.dropna(subset=["z"]).copy()
    gz["zb"]=pd.cut(gz.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    def summ(x):
        return pd.Series({"n":len(x),"mean_u":x.u.mean(),"t":x.u.mean()/(x.u.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["z_bins_inprof"]=gz[gz.inprof].groupby("zb").apply(summ)
    out["z_bins_outprof"]=gz[~gz.inprof].groupby("zb").apply(summ)
    res={}
    for k,sub in [("in",gz[gz.inprof]),("out",gz[~gz.inprof])]:
        s=stats.linregress(sub.z,sub.u); res[k]=(len(sub),s.slope,s.slope/s.stderr)
    out["slope_u_on_z"]=pd.DataFrame(res,index=["n","slope","t"]).T
    # trend sub-profiles by 60d return (agitation unknown out of profile)
    gz["tr"]=pd.cut(gz.ret60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    res={}
    for (tr,ip),sub in gz.dropna(subset=["tr"]).groupby(["tr","inprof"]):
        if len(sub)>10:
            s=stats.linregress(sub.z,sub.u); res[f"{tr}_{ip}"]=(len(sub),s.slope,s.slope/s.stderr)
    out["slope_by_trend"]=pd.DataFrame(res,index=["n","slope","t"]).T
    # one-day move scaled -> next day
    d1=d.dropna(subset=["r1z","f1"]).copy()
    d1["b"]=pd.cut(d1.r1z,[-99,-2,-1,1,2,99])
    out["r1z_next_day"]=d1.groupby(["inprof","b"]).f1.agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # weekday
    out["weekday_ret"]=d.dropna(subset=["f1"]).groupby("wd").f1.agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # vol level quintile across coin: sd rank within coin
    gz["sdq"]=gz.groupby("coin").sd.rank(pct=True)
    gz["sdb"]=pd.cut(gz.sdq,[0,0.2,0.4,0.6,0.8,1])
    out["u_by_vol_quint"]=gz.groupby("sdb").apply(summ)
    res={}
    for k,sub in gz.groupby("sdb"):
        s=stats.linregress(sub.z,sub.u); res[str(k)]=(len(sub),s.slope,s.slope/s.stderr)
    out["slope_by_vol"]=pd.DataFrame(res,index=["n","slope","t"]).T
    return out
