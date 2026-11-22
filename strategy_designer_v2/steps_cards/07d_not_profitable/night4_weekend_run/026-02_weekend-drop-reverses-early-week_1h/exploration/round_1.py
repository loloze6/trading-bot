def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift_rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values
            n=len(b)
            # drift grid
            idx=np.arange(0,n-48,48)
            r=c[idx+48]/c[idx]-1
            ok=(ts.values[idx+48]-ts.values[idx])==np.timedelta64(48,'h')
            for v in r[ok]: drift_rows.append((coin,v))
            close_t=ts+pd.Timedelta(hours=1)
            for i in range(48,n-48):
                ct=close_t.iloc[i]
                if ct.hour!=0: continue
                if (ts.iloc[i+48]-ts.iloc[i])!=pd.Timedelta(hours=48) or (ts.iloc[i]-ts.iloc[i-48])!=pd.Timedelta(hours=48): continue
                past=c[i]/c[i-48]-1; fwd=c[i+48]/c[i]-1
                rows.append(dict(coin=coin,window=w,year=ct.year,wd=ct.weekday(),past=past,fwd=fwd,
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows)
    dr=pd.DataFrame(drift_rows,columns=["coin","r"])
    dm=dr.groupby("coin")["r"].mean(); sd=dr.groupby("coin")["r"].std()
    d["unus"]=d["fwd"]-d["coin"].map(dm)
    d["z"]=d["past"]/d["coin"].map(sd)
    out={}
    def grp(x):
        return pd.Series(dict(n=len(x),mean_unus=x.unus.mean(),t=x.unus.mean()/(x.unus.std()/np.sqrt(len(x))),
                              slope=np.polyfit(x.z,x.unus,1)[0] if len(x)>5 else np.nan,
                              corr=np.corrcoef(x.past,x.unus)[0,1]))
    # weekday of the close (0=Mon close: weekend signal)
    out["by_weekday_all"]=d.groupby("wd").apply(grp)
    d["side"]=np.where(d.past<0,"fall","rise")
    out["by_weekday_side"]=d.groupby(["wd","side"]).apply(grp)
    mon=d[d.wd==0].copy()
    mon["q"]=pd.qcut(mon.z,5,labels=False)
    out["mon_by_quintile"]=mon.groupby("q").apply(lambda x: pd.Series(dict(n=len(x),z=x.z.mean(),past=x.past.mean(),unus=x.unus.mean(),fwd=x.fwd.mean(),
                                         t=x.unus.mean()/(x.unus.std()/np.sqrt(len(x))))))
    out["mon_by_year_side"]=mon.groupby(["year","side"]).apply(grp)
    out["mon_by_coin_side"]=mon.groupby(["coin","side"]).apply(grp)
    out["drift_sd"]=pd.DataFrame(dict(drift=dm,sd=sd))
    # book days
    bd=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["window"]=w; x["coin"]=coin; bd.append(x)
    bd=pd.concat(bd)
    bk=bd.groupby(["window","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_by_window"]=bk.groupby("window").agg(mean_book=("book_return","mean"),mean_coin=("coin_return","mean"),n=("book_return","count"))
    return out
