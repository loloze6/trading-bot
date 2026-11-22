def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values; n=len(b)
            alloc=b["postRebalance_current_allocation"].values
            pv=b["postRebalance_total_value"].values
            lr=pd.Series(np.r_[np.nan,np.diff(np.log(c))])
            vol30=lr.rolling(720,min_periods=200).std().values*np.sqrt(24)
            vol3=lr.rolling(72,min_periods=48).std().values*np.sqrt(24)
            for i in range(n):
                if ts[i].hour==23 and i>=168 and i+48<n:
                    wd=(ts[i]+pd.Timedelta(hours=1)).weekday()
                    j=i-1
                    rows.append(dict(coin=coin,w=w,wd=wd,past24=c[i]/c[i-24]-1,past7d=c[i-24]/c[i-168]-1,
                        f24=c[i+24]/c[i]-1,f48=c[i+48]/c[i]-1,vol=vol30[i],vol3=vol3[i],alloc=alloc[i],
                        bookpnl=pv[min(i+25,n-1)]/pv[j]-1 if j>=0 else np.nan))
    R=pd.DataFrame(rows).dropna(subset=["vol","vol3"])
    out={}
    R["s"]=-np.sign(R.past24); R["fade24"]=R.s*R.f24; R["fade48"]=R.s*R.f48
    R["z"]=R.past24.abs()/R.vol
    R["volratio"]=R.vol3/R.vol
    R["with_trend"]=np.sign(R.past24)==np.sign(R.past7d)
    M=R[R.wd==0].copy()
    M["absalloc"]=M.alloc.abs()
    M["vq"]=pd.qcut(M.volratio,4,labels=False)
    out["mon_by_volratio"]=M.groupby("vq").agg(n=("z","size"),vr=("volratio","mean"),fade24=("fade24","mean"),fade48=("fade48","mean"),absalloc=("absalloc","mean"),bookpnl=("bookpnl","mean"),booksd=("bookpnl","std"),worst=("bookpnl","min"))
    out["mon_by_trend"]=M.groupby("with_trend").agg(n=("z","size"),fade24=("fade24","mean"),fade48=("fade48","mean"),bookpnl=("bookpnl","mean"),booksd=("bookpnl","std"))
    M["zq"]=pd.qcut(M.z,5,labels=False)
    out["mon_book_by_z"]=M.groupby("zq").agg(n=("z","size"),bookpnl=("bookpnl","mean"),booksd=("bookpnl","std"),worst=("bookpnl","min"),share_loss_gt5=("bookpnl",lambda s:(s<-0.05).mean()))
    W=M.sort_values("bookpnl").head(int(len(M)*0.05))
    out["worst5pct_cases"]=pd.Series(dict(n=len(W),z=W.z.mean(),z_all=M.z.mean(),volratio=W.volratio.mean(),vr_all=M.volratio.mean(),with_trend=W.with_trend.mean(),wt_all=M.with_trend.mean(),absalloc=W.absalloc.mean(),aa_all=M.absalloc.mean(),bookpnl=W.bookpnl.mean(),sum_share=W.bookpnl.sum()/M.bookpnl.sum()))
    # all-day fade, excluding Tuesday start and Saturday start
    g=[]
    for name,df in [("all_days",R),("no_tue_sat",R[~R.wd.isin([1,5])]),("monday",M)]:
        x=-(df.past24/df.vol); y=df.f24
        sl=stats.linregress(x,y)
        g.append(dict(set=name,n=len(df),t=sl.slope/sl.stderr,fade24=df.fade24.mean(),fade24_bigz=df[df.z>df.z.median()].fade24.mean()))
    out["fade_sets"]=pd.DataFrame(g)
    return out
