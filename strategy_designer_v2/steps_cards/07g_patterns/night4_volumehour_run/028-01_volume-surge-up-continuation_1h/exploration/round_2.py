def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change()
            sd=r1.rolling(720,min_periods=720).std().shift(1)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r24=c/c.shift(24)-1
            r3=c/c.shift(3)-1
            df=pd.DataFrame({"coin":coin,"w":w,"f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,
               "f24":c.shift(-24)/c-1,"hour":ts.dt.hour,"wd":ts.dt.weekday,"yr":ts.dt.year,
               "pos":np.arange(len(b)),"z24":r24/(sd*np.sqrt(24)),"r1":r1,"sd":sd,
               "alloc":b["postRebalance_current_allocation"],"pv":b["postRebalance_total_value"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    def tstat(s):
        s=s.dropna()
        return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    d["ex1"]=d.f1-d.groupby("coin").f1.transform("mean")
    d["exs"]=d.ex1/d.sd
    # bars closing at 20 and 21 UTC (hour = bar start) -> two-hour move from close of hour 19 bar
    h19=d[d.hour==19].copy(); h19["ex2"]=h19.f2-d.groupby("coin").f2.transform("mean")[h19.index]
    out["2h after hour19 close by coin,year"]=h19.groupby(["yr","coin"]).ex2.apply(tstat).unstack()
    out["2h after hour19 close by coin"]=h19.groupby("coin").ex2.apply(tstat).unstack()
    out["hour20 scaled next-hour by coin"]=d[d.hour.isin([20,21])].groupby(["coin","hour"]).exs.apply(tstat).unstack()
    out["hour2 next-hour by coin"]=d[d.hour.isin([0,1,2])].groupby(["coin","hour"]).ex1.apply(tstat).unstack()
    # does the hour-19 effect scale with the prior 24h move sign? (gradedness candidate)
    h19["zb"]=pd.qcut(h19.z24,5)
    out["2h after h19 by z24 quintile"]=h19.groupby("zb",observed=True).ex2.apply(tstat).unstack()
    # weekday by coin and by year (24h grid)
    g24=d[d.pos%24==0].copy(); g24["ex24"]=g24.f24-g24.groupby("coin").f24.transform("mean")
    out["thursday 24h by coin"]=g24[g24.wd==3].groupby("coin").ex24.apply(tstat).unstack()
    out["24h reversal bottom quintile by coin"]=g24.assign(q=pd.qcut(g24.z24,5,labels=False)).groupby(["coin","q"]).ex24.apply(tstat).unstack()
    # book: gross position gain by hour of day
    d["pg"]=d.alloc*d.f1
    out["book gross gain per bar by hour (bp)"]=d.groupby("hour").pg.mean().mul(1e4).to_frame("bp").T.round(2).T
    out["share bars long"]=pd.Series({"share long":(d.alloc>0).mean(),"mean alloc when long":d.alloc[d.alloc>0].mean()})
    tr=pd.concat([x.assign(coin=c) for c in data["trades"] for x in data["trades"][c].values()])
    out["trade pnl quantiles"]=tr.profit_loss_percent.describe()
    return out
