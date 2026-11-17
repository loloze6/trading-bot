def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        grid=[]
        for w,b in ws.items():
            c=b.sort_values("timestamp")["close"].values
            for i in range(0,len(c)-2,2):
                grid.append(c[i+2]/c[i]-1)
        m2=np.mean(grid)
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]; v=b["volume"].astype(float)
            r=c.pct_change(); r2=c.pct_change(2)
            sc=r.abs().rolling(60,min_periods=20).mean()
            vrel=v/v.rolling(60,min_periods=20).mean()
            vwk=(v+v.shift(1))/(2*v.rolling(60,min_periods=20).mean())
            for i in range(2,len(b)-2):
                if ts[i].weekday()!=6: continue
                rows.append(dict(coin=coin,year=ts[i].year,r=r[i],r2=r2[i],z=r[i]/sc[i],z2=r2[i]/sc[i],
                    vrel=vrel[i],vwk=vwk[i],f2=c[i+2]/c[i]-1-m2))
    d=pd.DataFrame(rows).dropna()
    out={}
    def tt(x): return pd.Series(dict(n=len(x),mean=x.mean(),t=stats.ttest_1samp(x,0).statistic))
    up=d[d.r>0].copy()
    up["vq"]=pd.qcut(up.vwk,4,labels=False)
    out["sunup_by_weekendvol_q"]=up.groupby("vq")["f2"].apply(tt).unstack()
    dn=d[d.r<0].copy()
    dn["vq"]=pd.qcut(dn.vwk,4,labels=False)
    out["sundown_by_weekendvol_q"]=dn.groupby("vq")["f2"].apply(tt).unstack()
    # signed weekend 2-day return
    d["q2"]=pd.qcut(d.z2,6,labels=False)
    out["by_weekend2d_zq"]=d.groupby("q2").agg(n=("f2","size"),z2=("z2","mean"),ex2=("f2","mean"))
    # sign-only gain: -sign(r)*f2
    g=-np.sign(d.r)*d.f2
    out["signonly_gain"]=tt(g).to_frame().T
    out["signonly_by_year"]=g.groupby(d.year).apply(tt).unstack()
    # slope of f2 on -z within all Sundays, and on z*low-volume
    sl=stats.linregress(d.z.clip(-4,4),d.f2)
    out["slope_all_sun"]=pd.Series(dict(slope=sl.slope,t=sl.slope/sl.stderr,n=len(d)))
    g2=-np.sign(d.r)*d.f2
    d["vq"]=pd.qcut(d.vwk,4,labels=False)
    out["signonly_by_vol_q"]=g2.groupby(d.vq).apply(tt).unstack()
    return out
