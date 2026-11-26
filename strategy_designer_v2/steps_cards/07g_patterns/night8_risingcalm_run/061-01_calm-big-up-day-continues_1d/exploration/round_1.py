def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=30).std()
            z=r/sd
            fwd=c.shift(-H)/c-1
            tr=c/c.shift(60)-1
            r5p=c/c.shift(5)-1
            ts=pd.to_datetime(b["timestamp"])
            calm=(b["regime"]!="chop")
            for i in range(0,len(b),H):
                rows.append(dict(coin=coin,w=w,z=z.iloc[i],fwd=fwd.iloc[i],calm=calm.iloc[i],
                                 tr=tr.iloc[i],r5p=r5p.iloc[i],year=ts.iloc[i].year,wd=ts.iloc[i].weekday(),
                                 day=ts.iloc[i].normalize(),sdv=sd.iloc[i]))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d=d.dropna(subset=["z"])
    d["dex"]=d["ex"]*np.sign(d["z"])
    def tt(x):
        x=x.dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    d["zq"]=pd.qcut(d["z"],5,labels=False)
    out["ex by z quintile x calm"]=d.groupby(["calm","zq"])["ex"].apply(tt).unstack()
    d["tb"]=np.where(d["tr"]>0.10,"rising",np.where(d["tr"]<-0.10,"falling",np.where(d["tr"].isna(),"na","choppy")))
    def slope(g):
        g=g.dropna(subset=["z","ex"])
        if len(g)<20: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        s=stats.linregress(g["z"],g["ex"]); return pd.Series(dict(n=len(g),slope=s.slope,t=s.slope/s.stderr))
    out["slope ex on z by calm x trend"]=d.groupby(["calm","tb"]).apply(slope)
    d["sg"]=np.sign(d["z"])
    out["dex by calm x sign, |z|>1"]=d[d["z"].abs()>1].groupby(["calm","sg"])["dex"].apply(tt).unstack()
    out["dex calm |z|>1 by year"]=d[(d["z"].abs()>1)&d["calm"]].groupby("year")["dex"].apply(tt).unstack()
    # prior 5-day return vs next
    d["pq"]=pd.qcut(d["r5p"]/(d["sdv"]*np.sqrt(5)),5,labels=False)
    out["ex by prior-5d scaled quintile x calm"]=d.groupby(["calm","pq"])["ex"].apply(tt).unstack()
    # book / coin daily by weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
    out["coin ret by weekday"]=dd.groupby("wd")["coin_return"].apply(tt).unstack()
    out["book ret by weekday"]=dd.groupby("wd")["book_return"].apply(tt).unstack()
    tr_=[]
    for coin,ws in data["trades"].items():
        for w,x in ws.items():
            if len(x): tr_.append(x)
    tr_=pd.concat(tr_)
    out["trades by side"]=tr_.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
