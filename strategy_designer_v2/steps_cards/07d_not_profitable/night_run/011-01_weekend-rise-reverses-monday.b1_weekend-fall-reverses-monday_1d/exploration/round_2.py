def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"].astype(float)
            r=cl.pct_change()
            sd=r.rolling(20,min_periods=10).std()
            f1=cl.shift(-1)/cl-1; f2=cl.shift(-2)/cl-1
            wk=cl/cl.shift(2)-1  # Fri close -> Sun close (on Sunday bar)
            vol=b["volume"].astype(float)
            vrel=(vol+vol.shift(1))/(2*vol.rolling(20,min_periods=10).mean())
            df=pd.DataFrame(dict(coin=c,win=w,wd=ts.dt.weekday,year=ts.dt.year,r=r,z=r/sd,zw=wk/(sd*np.sqrt(2)),f1=f1,f2=f2,vrel=vrel,
                                 alloc=b["postRebalance_current_allocation"].fillna(0)))
            rows.append(df)
    d=pd.concat(rows)
    mu2=d.groupby("coin")["f2"].mean()  # approx coin mean 2-bar
    out={}
    s=d[d.wd==6].dropna(subset=["z","f2","zw"]).copy()
    s["ex2"]=s.f2-s.coin.map(mu2)
    fall=s[s.z<0]; rise=s[s.z>0]
    out["sunday fall vs rise"]=pd.DataFrame({
        "fall":[len(fall),fall.f1.mean(),fall.ex2.mean(),stats.ttest_1samp(fall.ex2,0).statistic],
        "rise":[len(rise),rise.f1.mean(),rise.ex2.mean(),stats.ttest_1samp(rise.ex2,0).statistic]},index=["n","f1","ex2","t_ex2"])
    out["welch fall minus rise ex2"]=float(stats.ttest_ind(fall.ex2,rise.ex2,equal_var=False).statistic)
    sl=stats.linregress(s.z,s.ex2); out["slope ex2 on signed z (all sundays)"]=pd.Series(dict(slope=sl.slope,t=sl.slope/sl.stderr,n=len(s)))
    sl2=stats.linregress(s.zw,s.ex2); out["slope ex2 on 2-day weekend z"]=pd.Series(dict(slope=sl2.slope,t=sl2.slope/sl2.stderr))
    s["sgn"]=-np.sign(s.z)
    s["ls2"]=s.sgn*s.ex2
    out["long-short sunday ex2 by year"]=s.groupby("year").agg(m=("ls2","mean"),n=("ls2","size"))
    out["long-short by coin"]=s.groupby("coin").agg(m=("ls2","mean"),n=("ls2","size"))
    s["vq"]=pd.qcut(s.vrel,3,labels=False)
    out["ls by weekend vol tercile"]=s.groupby("vq").agg(v=("vrel","mean"),m=("ls2","mean"),fall_ex2=("ex2",lambda x: x[s.loc[x.index,"z"]<0].mean()),n=("ls2","size"))
    # other days sign split, non-overlapping weekly grid per weekday
    o=d[(d.wd!=6)].dropna(subset=["z","f1"]).copy()
    o["ls1"]=-np.sign(o.z)*(o.f1-d.f1.mean())
    out["sign-reversal f1 by weekday"]=pd.concat([o.groupby("wd")["ls1"].mean(),
        s.assign(ls1=s.sgn*(s.f1-d.f1.mean())).groupby("wd")["ls1"].mean()])
    # all-coin exposure share
    out["share of bars held"]=float((d.alloc>0).mean())
    return out
