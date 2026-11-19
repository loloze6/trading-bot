def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=168
    out={}
    # hour effect by coin and year
    hrows=[]
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            s=pd.Series(b["close"].astype(float).values); lr=np.log(s).diff()
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            hrows.append(pd.DataFrame({"coin":coin,"yr":ts.dt.year.values,"h":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":lr.values,"rng":(np.log(b["high"].astype(float))-np.log(b["low"].astype(float))).values}))
            n=len(s)
            if n<2*H: continue
            v=pd.Series(b["volume"].astype(float).values)
            r720=s/s.shift(720)-1; r24=s/s.shift(24)-1; r168=s/s.shift(168)-1
            vr=v.rolling(24).mean()/v.rolling(720,min_periods=240).mean()
            hi=s.rolling(1440,min_periods=720).max(); dist=1-s/hi
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,yr=ts.iloc[i].year,fwd=s.iloc[i+H]/s.iloc[i]-1,r720=r720.iloc[i],r24=r24.iloc[i],r168=r168.iloc[i],vr=vr.iloc[i],dist=dist.iloc[i]))
    h=pd.concat(hrows).dropna(subset=["r"])
    h["eve"]=h["h"].isin([21,22])
    # per coin: mean of hours 21-22 minus other hours
    pc=h.groupby(["coin","eve"])["r"].mean().unstack()
    pc["diff"]=pc[True]-pc[False]
    out["eve_by_coin"]=pc
    py=h.groupby(["yr","eve"])["r"].mean().unstack(); py["diff"]=py[True]-py[False]
    py["n_eve"]=h[h.eve].groupby("yr").size()
    out["eve_by_year"]=py
    # cross-coin averaged per hour-of-day per day? per (yr) t of eve sum per day
    h22=h[h.h.isin([21,22])].groupby(["coin","wd"])["r"].mean().groupby("wd").mean()
    out["eve_by_weekday"]=h22
    out["range_by_hour"]=h.groupby("h")["rng"].mean()
    # weekday by year (coin daily returns averaged across coins per day)
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d[["day","coin_return","book_return"]].copy(); D.append(dd)
    D=pd.concat(D).dropna(); D["day"]=pd.to_datetime(D["day"])
    m=D.groupby("day")[["coin_return","book_return"]].mean().reset_index()
    m["wd"]=m.day.dt.weekday; m["yr"]=m.day.dt.year
    t=m.groupby("wd")["coin_return"].agg(["size","mean","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["size"]))
    out["weekday_xsec_mean"]=t
    out["weekday_by_year"]=m.pivot_table(index="yr",columns="wd",values="coin_return",aggfunc="mean")
    g=pd.DataFrame(rows); g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    up=g[g.r720>0].dropna(subset=["r24","vr","ex","dist"])
    X=np.column_stack([np.ones(len(up)),stats.zscore(up.r24),stats.zscore(np.log(up.vr)),stats.zscore(up.dist)])
    beta,res,_,_=np.linalg.lstsq(X,up.ex.values,rcond=None)
    e=up.ex.values-X@beta; s2=e@e/(len(e)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["up_reg_r24_logvr_dist"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","r24","logvr","dist"])
    out["up_n"]=len(up)
    # vr top quintile in up regime by year and coin share positive
    up=up.copy(); up["q"]=pd.qcut(up.vr.rank(method="first"),5,labels=False)
    out["up_vr_top_by_year"]=up[up.q==4].groupby("yr")["ex"].agg(["size","mean"])
    cc=up.groupby(["coin","q"])["ex"].mean().unstack()
    out["up_vr_top_minus_bottom_coins_pos"]=f"{(cc[4]>cc[0]).sum()} of {cc[[0,4]].dropna().shape[0]}"
    dn=g[g.r720<=0].dropna(subset=["r24","vr","ex","dist","r168"])
    X=np.column_stack([np.ones(len(dn)),stats.zscore(dn.r168),stats.zscore(np.log(dn.vr)),stats.zscore(dn.dist)])
    beta,_,_,_=np.linalg.lstsq(X,dn.ex.values,rcond=None)
    e=dn.ex.values-X@beta; s2=e@e/(len(e)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["dn_reg_r168_logvr_dist"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","r168","logvr","dist"])
    return out
