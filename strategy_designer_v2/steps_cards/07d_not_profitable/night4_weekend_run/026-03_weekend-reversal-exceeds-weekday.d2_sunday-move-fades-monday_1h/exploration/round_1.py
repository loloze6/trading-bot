def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]; ddrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values; n=len(b)
            alloc=b["postRebalance_current_allocation"].values
            r1=np.r_[np.diff(c)/c[:-1],np.nan]
            # 24h vol from hourly
            vol=pd.Series(np.r_[np.nan,np.diff(np.log(c))]).rolling(24*30,min_periods=200).std().values*np.sqrt(24)
            for i in range(n):
                if ts[i].hour==23 and i>=48 and i+48<n:
                    wd=(ts[i]+pd.Timedelta(hours=1)).weekday()
                    rows.append(dict(coin=coin,w=w,wd=wd,past24=c[i]/c[i-24]-1,past48=c[i]/c[i-48]-1,
                        f6=c[i+6]/c[i]-1,f12=c[i+12]/c[i]-1,f24=c[i+24]/c[i]-1,f48=c[i+48]/c[i]-1,
                        vol=vol[i],alloc=alloc[i],fc=b["forecast"].iloc[i]))
            d=data["days"][coin][w]
            br=d["book_return"]; cr=d["coin_return"]
            v=d["book_value"].values; dd=(v/np.maximum.accumulate(v)-1).min()
            ddrows.append(dict(coin=coin,w=w,dd=dd,ret=v[-1]/v[0]-1,coinret=d["close"].values[-1]/d["close"].values[0]-1))
            drows.append(pd.DataFrame({"br":br,"cr":cr,"wd":pd.to_datetime(d["day"]).dt.weekday}))
    R=pd.DataFrame(rows).dropna(subset=["vol"])
    out={}
    # fade signal strength by weekday of the day that starts
    def fade(df,past,fwd):
        s=-np.sign(df[past]); return (s*df[fwd])
    g=[]
    for wd,df in R.groupby("wd"):
        x=-(df.past24/df.vol); y=df.f24
        sl=stats.linregress(x,y)
        g.append(dict(day_start=wd,n=len(df),slope=sl.slope,t=sl.slope/sl.stderr,
            fade24=fade(df,"past24","f24").mean(),fade6=fade(df,"past24","f6").mean(),
            fade12=fade(df,"past24","f12").mean(),fade48=fade(df,"past24","f48").mean(),
            fade48of48=fade(df,"past48","f48").mean()))
    out["fade_by_day_starting"]=pd.DataFrame(g)
    M=R[R.wd==0].copy()
    M["z"]=(M.past24.abs()/M.vol)
    M["q"]=pd.qcut(M.z,5,labels=False)
    M["fade24"]=fade(M,"past24","f24"); M["fade48"]=fade(M,"past24","f48"); M["fade48_48"]=fade(M,"past48","f48")
    M["absalloc"]=M.alloc.abs()
    out["monday_by_size_quintile"]=M.groupby("q").agg(n=("z","size"),z=("z","mean"),absmove=("past24",lambda s:s.abs().mean()),
        fade24=("fade24","mean"),fade48=("fade48","mean"),fade48_48=("fade48_48","mean"),absalloc=("absalloc","mean"))
    out["monday_by_window"]=M.groupby("w").agg(n=("z","size"),fade24=("fade24","mean")).T
    out["monday_by_coin"]=M.groupby("coin").agg(n=("z","size"),fade24=("fade24","mean"),fade48=("fade48","mean"),absalloc=("absalloc","mean"))
    D=pd.concat(drows).dropna()
    out["book_by_weekday"]=D.groupby("wd").agg(br=("br","mean"),cr=("cr","mean"),n=("br","size"),brsd=("br","std"))
    DD=pd.DataFrame(ddrows)
    out["dd_worst"]=DD.sort_values("dd").head(10)
    out["dd_summary"]=DD[["dd","ret","coinret"]].describe()
    return out
