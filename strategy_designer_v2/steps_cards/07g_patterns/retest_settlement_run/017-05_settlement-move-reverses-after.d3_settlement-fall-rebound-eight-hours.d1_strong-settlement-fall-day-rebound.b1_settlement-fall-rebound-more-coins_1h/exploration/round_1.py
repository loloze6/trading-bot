def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hrows=[]
    for coin, wins in data["bars"].items():
        # coin drift over 24h on grid
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-24,24)
            g.append(c[idx+24]/c[idx]-1)
        g=np.concatenate(g) if g else np.array([])
        drift=np.nanmean(g); usual=np.nanstd(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; ts=pd.to_datetime(b["timestamp"],utc=True)
            r2=c/c.shift(2)-1
            z=r2/r2.abs().rolling(720,min_periods=200).mean()
            r24p=c/c.shift(24)-1
            z24=r24p/r24p.abs().rolling(720,min_periods=200).mean()
            r168=c/c.shift(168)-1
            vol=(c.pct_change().abs()).rolling(168,min_periods=100).mean()
            volr=vol/(c.pct_change().abs()).rolling(1440,min_periods=500).mean()
            f24=c.shift(-24)/c-1; f1=c.shift(-1)/c-1; f4=c.shift(-4)/c-1
            v=b["volume"]; vrel=v/v.rolling(720,min_periods=200).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"wd":ts.dt.weekday,"year":ts.dt.year,
                "z":z,"z24":z24,"r168":r168,"volr":volr,"f24u":(f24-drift),"f24n":(f24-drift)/usual,
                "f1":f1,"f4":f4,"vrel":vrel,"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"n":n})
    out={}
    # 1: by bar-start hour, falls z<-1, fwd24 unusual (one bar per day per hour => non-overlapping)
    F=D[D.z<-1]
    out["fall_z<-1_by_hour_fwd24u"]=F.groupby("hour")["f24u"].apply(tt).unstack()
    # 2: z bucket, settlement hours (23,15) vs others
    D["zb"]=pd.cut(D.z,[-99,-3,-2,-1,0,1,2,3,99])
    D["sett"]=D.hour.isin([23,15])
    S=D[D.hour%4==3]  # one sample per 4h-ish blocks; mean only
    out["zbucket_fwd24u_sett_vs_other"]=D.groupby(["sett","zb"],observed=True)["f24u"].apply(tt).unstack()
    # 3: hourly 1h return seasonality
    out["f1_by_hour"]=D.groupby("hour")["f1"].apply(tt).unstack()
    # 4: volume by hour
    out["vrel_by_hour"]=D.groupby("hour")["vrel"].mean()
    # 5: daily (hour 23 close) z24 bucket -> fwd24
    E=D[D.hour==23].copy()
    E["z24b"]=pd.cut(E.z24,[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["daily_z24_fwd24u"]=E.groupby("z24b",observed=True)["f24u"].apply(tt).unstack()
    # 6: weekly trend r168 tercile on daily grid
    E["r168q"]=E.groupby("coin")["r168"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["daily_r168q_fwd24u"]=E.groupby("r168q")["f24u"].apply(tt).unstack()
    # 7: fall at settlement by vol regime
    G=D[(D.sett)&(D.z<-1.5)].copy()
    G["vq"]=pd.qcut(G.volr,3,labels=["lowvol","mid","highvol"])
    out["settfall_by_volregime"]=G.groupby("vq",observed=True)["f24u"].apply(tt).unstack()
    out["settfall_by_year"]=G.groupby("year")["f24u"].apply(tt).unstack()
    # 8: weekday daily
    out["daily_fwd24u_by_weekday"]=E.groupby("wd")["f24u"].apply(tt).unstack()
    # 9: book days largest gains/losses: coin return before/after
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["cprev"]=x.coin_return.shift(1); x["cnext"]=x.coin_return.shift(-1); dd.append(x)
    DD=pd.concat(dd)
    DD["bq"]=pd.qcut(DD.book_return.rank(method="first"),10,labels=False)
    out["bookdecile_coin_prev_same_next"]=DD.groupby("bq")[["book_return","cprev","coin_return","cnext"]].mean()
    return out
