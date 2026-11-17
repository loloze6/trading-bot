def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        grid=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values
            n=len(c)
            for i in range(0,n-2,2):
                grid.append(c[i+2]/c[i]-1)
        m2=np.mean(grid)
        grid1=[]
        for w,b in ws.items():
            c=b.sort_values("timestamp")["close"].values
            grid1+=list(c[1:]/c[:-1]-1)
        m1=np.mean(grid1)
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]
            r=c.pct_change()
            sc=r.abs().rolling(60,min_periods=20).mean()
            z=r/sc
            year=ts.dt.year
            for i in range(1,len(b)-2):
                rows.append(dict(coin=coin,w=w,year=year[i],wd=ts[i].weekday(),r=r[i],z=z[i],
                    f=b["forecast"][i],f1=c[i+1]/c[i]-1-m1,f2=c[i+2]/c[i]-1-m2))
    d=pd.DataFrame(rows).dropna(subset=["z"])
    s=d[d.wd==6].copy()
    out={}
    up=s[s.r>0].copy()
    up["q"]=pd.qcut(up.z,5,labels=False)
    out["sun_up_by_zq"]=up.groupby("q").agg(n=("f2","size"),z=("z","mean"),ex1=("f1","mean"),ex2=("f2","mean"))
    s["q"]=pd.qcut(s.z,6,labels=False)
    out["sun_all_by_zq"]=s.groupby("q").agg(n=("f2","size"),z=("z","mean"),ex1=("f1","mean"),ex2=("f2","mean"))
    def tt(x): return pd.Series(dict(n=len(x),mean=x.mean(),t=stats.ttest_1samp(x,0).statistic))
    out["up_ex2_by_coin"]=up.groupby("coin")["f2"].apply(tt).unstack()
    out["up_ex2_by_year"]=up.groupby("year")["f2"].apply(tt).unstack()
    out["up_ex1"]=tt(up.f1).to_frame().T
    out["down_ex2"]=tt(s[s.r<0].f2).to_frame().T
    # all weekdays: sign of day's return vs next 2-day excess, rises only, slope on z
    res=[]
    for wd,g in d[d.r>0].groupby("wd"):
        sl=stats.linregress(g.z,g.f2)
        res.append(dict(wd=wd,n=len(g),mean_ex2=g.f2.mean(),t=stats.ttest_1samp(g.f2,0).statistic,slope=sl.slope,slope_t=sl.slope/sl.stderr))
    out["rises_by_weekday"]=pd.DataFrame(res)
    res=[]
    for wd,g in d[d.r<0].groupby("wd"):
        sl=stats.linregress(g.z,g.f2)
        res.append(dict(wd=wd,n=len(g),mean_ex2=g.f2.mean(),t=stats.ttest_1samp(g.f2,0).statistic,slope=sl.slope,slope_t=sl.slope/sl.stderr))
    out["falls_by_weekday"]=pd.DataFrame(res)
    return out
