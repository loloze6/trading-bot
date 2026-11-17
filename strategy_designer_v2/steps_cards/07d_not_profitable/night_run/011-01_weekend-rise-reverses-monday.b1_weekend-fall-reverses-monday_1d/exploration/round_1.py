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
            tr20=cl/cl.shift(20)-1
            vrel=b["volume"]/b["volume"].rolling(20,min_periods=10).mean()
            alloc=b["postRebalance_current_allocation"].fillna(0)
            gain=alloc*f1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df=pd.DataFrame(dict(coin=c,win=w,wd=ts.dt.weekday,year=ts.dt.year,r=r,z=r/sd,f1=f1,f2=f2,tr20=tr20,vrel=vrel,alloc=alloc,gain=gain,fee=fee,fc=b["forecast"]))
            rows.append(df)
    d=pd.concat(rows)
    out={}
    out["mean f1 by weekday of signal bar"]=d.groupby("wd")["f1"].agg(["mean","count"])
    s=d[d.wd==6].dropna(subset=["z","f2"])
    s["zq"]=pd.qcut(s.z,5,labels=False)
    out["sunday z quintile -> f1,f2"]=s.groupby("zq").agg(z=("z","mean"),f1=("f1","mean"),f2=("f2","mean"),n=("f1","size"))
    # weekday comparison
    o=d[d.wd!=6].dropna(subset=["z","f1"]); o["zq"]=pd.qcut(o.z,5,labels=False)
    out["other days z quintile -> f1"]=o.groupby("zq").agg(z=("z","mean"),f1=("f1","mean"),n=("f1","size"))
    held=d[d.alloc>0]
    out["held bars"]=pd.Series(dict(n=len(held),mean_gain=held.gain.mean(),mean_f1=held.f1.mean(),t=stats.ttest_1samp(held.f1.dropna(),0).statistic,mean_alloc=held.alloc.mean(),fee_mean_all_bars=d.fee.mean(),fee_sum_per_held=d.fee.sum()/len(held),coin_mean_daily=d.r.mean()))
    held=held.copy(); held["trq"]=pd.qcut(held.tr20,3,labels=False); held["vq"]=pd.qcut(held.vrel,3,labels=False)
    out["held by 20d trend tercile"]=held.groupby("trq").agg(tr=("tr20","mean"),f1=("f1","mean"),f2=("f2","mean"),n=("f1","size"))
    out["held by sunday vol rel tercile"]=held.groupby("vq").agg(v=("vrel","mean"),f1=("f1","mean"),f2=("f2","mean"),n=("f1","size"))
    out["held by year"]=held.groupby("year").agg(f1=("f1","mean"),n=("f1","size"))
    out["held by coin"]=held.groupby("coin").agg(f1=("f1","mean"),f2=("f2","mean"),n=("f1","size"))
    # book daily
    bd=[]
    for c in data["days"]:
        for w,x in data["days"][c].items(): bd.append(x.assign(coin=c,win=w))
    bd=pd.concat(bd)
    out["book vs coin daily"]=pd.Series(dict(book_mean=bd.book_return.mean(),coin_mean=bd.coin_return.mean(),book_sd=bd.book_return.std(),coin_sd=bd.coin_return.std()))
    return out
