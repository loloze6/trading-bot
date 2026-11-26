def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change()
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            pos=(c-(hh+ll)/2)/((hh-ll)/2)
            tr60=c/c.shift(60)-1
            sd30=r1.rolling(30).std()
            fwd=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"r1":r1,"pos":pos,"tr60":tr60,"sd30":sd30,"fwd":fwd,
                "day":ts.dt.normalize(),"yr":ts.dt.year,"wd":ts.dt.weekday,"fc":b["forecast"]}))
    d=pd.concat(rows,ignore_index=True)
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    d["sdc"]=d.groupby("coin")["r1"].transform("std")
    d["z"]=d.r1/d.sdc
    d["agit"]=np.where(d.sd30>d.groupby("coin")["sd30"].transform("median"),"agit","calm")
    d=d.dropna(subset=["fwd","tr60","r1","sd30"])
    d["trend"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    def daytt(g,col="ex"):
        s=g.groupby("day")[col].sum()
        return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    def summ(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"days":g["day"].nunique(),"mean_ex%":100*x.mean(),
                          "t_day":daytt(g)})
    def slope(g):
        if len(g)<20: return pd.Series({"n":len(g)})
        r=stats.linregress(g["z"],g["ex"])
        return pd.Series({"n":len(g),"slope%perz":100*r.slope,"t":r.slope/r.stderr})
    out={}
    f=d[d.trend=="falling"].copy()
    f["zq"]=pd.cut(f.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["falling_z_by_agit"]=f.groupby(["agit","zq"]).apply(summ)
    out["falling_slope_by_agit"]=f.groupby("agit").apply(slope)
    out["falling_up_slope_by_agit"]=f[f.r1>0].groupby("agit").apply(slope)
    out["falling_down_slope_by_agit"]=f[f.r1<0].groupby("agit").apply(slope)
    out["slope_by_trend_agit"]=d.groupby(["trend","agit"]).apply(slope)
    fu=f[f.z>1]
    out["falling_bigup_by_coin"]=fu.groupby("coin").apply(summ)
    out["falling_bigup_by_year"]=fu.groupby("yr").apply(summ)
    out["falling_bigup_by_w"]=fu.groupby("w").apply(summ)
    fd=f[f.z<-1]
    out["falling_bigdown_by_agit_year"]=fd.groupby(["agit","yr"]).apply(summ)
    fu2=f[f.r1>0].copy()
    fu2["posq"]=pd.cut(fu2.pos,[-1.01,-0.2,0.2,1.01])
    fu2["zq"]=pd.cut(fu2.z,[0,1,99])
    out["falling_up_pos_z"]=fu2.groupby(["zq","posq"]).apply(summ)
    out["wd_all"]=d.groupby("wd").apply(summ)
    return out
