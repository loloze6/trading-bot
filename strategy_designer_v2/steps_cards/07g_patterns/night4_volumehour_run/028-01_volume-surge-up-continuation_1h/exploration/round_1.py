def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r1=c.pct_change()
            sd=r1.rolling(720,min_periods=720).std().shift(1)
            vr=b["volume"]/b["volume"].rolling(720,min_periods=720).mean().shift(1)
            r24=c/c.shift(24)-1
            sd24=r1.rolling(24).std()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            df=pd.DataFrame({"coin":coin,"w":w,"z":r1/sd,"vr":vr,"z24":r24/(sd*np.sqrt(24)),
                 "volrel":sd24/sd,"f6":c.shift(-6)/c-1,"f2":c.shift(-2)/c-1,"f1":c.shift(-1)/c-1,
                 "f24":c.shift(-24)/c-1,"hour":ts.dt.hour,"wd":ts.dt.weekday,"pos":np.arange(len(b)),
                 "yr":ts.dt.year,"alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    def tstat(s):
        s=s.dropna(); 
        return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # 6h grid
    g6=d[d.pos%6==0].copy()
    g6["ex6"]=g6.f6-g6.groupby("coin").f6.transform("mean")
    g6["zb"]=pd.cut(g6.z,[-99,-4,-2.5,-1.5,1.5,2.5,4,99])
    g6["vb"]=pd.cut(g6.vr,[0,0.7,1.5,3,99])
    out["ex6 by z x volratio"]=g6.groupby(["zb","vb"],observed=True).ex6.apply(tstat).unstack()
    # signed continuation: sign(z)*ex6 for |z|>2.5, by vr bucket and coin
    big=g6[g6.z.abs()>2.5].copy(); big["cont"]=np.sign(big.z)*big.ex6
    out["big hour continuation by vr,coin"]=big.groupby(["coin","vb"],observed=True).cont.apply(tstat).unstack()
    # 1h grid hour-of-day
    d["ex1"]=d.f1-d.groupby("coin").f1.transform("mean")
    out["next hour by hour of day"]=d.groupby("hour").ex1.apply(tstat).unstack()
    g24=d[d.pos%24==0].copy(); g24["ex24"]=g24.f24-g24.groupby("coin").f24.transform("mean")
    g24["z24b"]=pd.qcut(g24.z24,5)
    out["24h after 24h move quintile"]=g24.groupby(["z24b"],observed=True).ex24.apply(tstat).unstack()
    g6["volb"]=pd.qcut(g6.volrel,5)
    out["ex6 by vol level quintile"]=g6.groupby("volb",observed=True).ex6.apply(tstat).unstack()
    g6["z24b"]=pd.qcut(g6.z24,5)
    out["ex6 by 24h move quintile"]=g6.groupby("z24b",observed=True).ex6.apply(tstat).unstack()
    out["ex24 by weekday"]=g24.groupby("wd").ex24.apply(tstat).unstack()
    # book days
    dd=pd.concat([x.assign(coin=c) for c in data["days"] for x in data["days"][c].values()])
    dd=dd.dropna(subset=["book_return"])
    out["book daily by year"]=dd.assign(yr=pd.to_datetime(dd.day).dt.year).groupby("yr").book_return.apply(tstat).unstack()
    tr=pd.concat([x.assign(coin=c) for c in data["trades"] for x in data["trades"][c].values()])
    out["trades"]=pd.Series({"n":len(tr),"mean gross%":tr.profit_loss_percent.mean(),"mean net%":tr.net_profit_loss_percent.mean(),"win%":(tr.profit_loss_percent>0).mean()*100,"med dur h":tr.duration_minutes.median()/60})
    return out
