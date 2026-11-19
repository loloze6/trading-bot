def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 2-bar return over all windows (non-overlap grid)
        m2=[]
        for w,b in ws.items():
            c=b["close"].values
            g=c[::2]
            if len(g)>1: m2.extend(list(g[1:]/g[:-1]-1))
        mu2=np.nanmean(m2)
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"]
            r2=c/c.shift(2)-1
            scale=r2.abs().rolling(60,min_periods=20).mean().shift(1)
            z=r2/scale
            f2=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            r1=c/c.shift(1)-1
            vol=b["volume"]
            vrel=vol/vol.rolling(168,min_periods=48).mean()
            rv=r1.abs().rolling(168,min_periods=48).mean()
            rows.append(pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,
                "z":z.values,"f2x":(f2-mu2).values,"f1":f1.values,"r1":r1.values,"vrel":vrel.values,"rv":rv.values,
                "alloc":b["postRebalance_current_allocation"].values,"fc":b["forecast"].values}))
    d=pd.concat(rows,ignore_index=True).dropna(subset=["z","f2x"])
    d["s"]=-np.clip(d["z"],-3,3)*d["f2x"]
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x))})
    byhour=d.groupby("hour")["s"].apply(tt).unstack()
    byhour["mean1h_bp"]=d.groupby("hour")["f1"].mean()*1e4
    byhour["vrel"]=d.groupby("hour")["vrel"].mean()
    # settlement bars (hour 7,15,23 start) by vol tercile
    st=d[d.hour.isin([7,15,23])].copy()
    st["vt"]=st.groupby("coin")["rv"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    byvol=st.groupby("vt")["s"].apply(tt).unstack()
    bycoin=st.groupby("coin")["s"].apply(tt).unstack()
    bywd=st.groupby("wd")["s"].apply(tt).unstack()
    # non-settlement general reversal
    ns=d[~d.hour.isin([7,15,23])]
    # book costs
    tr=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    trades={"n":len(tr),"gross_mean_pct":tr["profit_loss_percent"].mean(),"net_mean_pct":tr["net_profit_loss_percent"].mean(),
            "gross_t":tr["profit_loss_percent"].mean()/tr["profit_loss_percent"].std()*np.sqrt(len(tr)),
            "dur_mean_min":tr["duration_minutes"].mean()}
    return {"by_hour":byhour,"settle_by_vol":byvol,"settle_by_coin":bycoin,"settle_by_wd":bywd,
            "nonsettle_all":tt(ns["s"]),"trades":pd.Series(trades)}
