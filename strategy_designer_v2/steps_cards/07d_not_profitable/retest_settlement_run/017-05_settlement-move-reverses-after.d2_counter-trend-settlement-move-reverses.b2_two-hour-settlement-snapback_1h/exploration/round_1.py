def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean h-returns on grid pooled
        means={}
        for h in (2,4,8,24):
            vals=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                vals.append(c[idx+h]/c[idx]-1)
            v=np.concatenate(vals); means[h]=(v.mean(),v.std())
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"].values; n=len(c)
            hr=ts.dt.hour.values
            hi=b["high"].values; lo=b["low"].values
            lr=np.log(c); r1=np.r_[np.nan,np.diff(lr)]
            vol24=pd.Series(r1).rolling(24*7).std().values
            for t in np.where(np.isin(hr,[23,7,15]))[0]:
                if t<24 or t+24>=n: continue
                pre=c[t]/c[t-2]-1; r24=c[t]/c[t-24]-1
                d=np.sign(r24)
                if d==0: continue
                rec=dict(coin=coin,w=w,yr=ts.iloc[t].year,hr=hr[t],ct=pre*r24<0,
                         pre=pre,r24=r24,vol=vol24[t],fc=b["forecast"].values[t],
                         year=ts.iloc[t].year)
                for h in (2,4,8,24):
                    rec[f"x{h}"]=d*(c[t+h]/c[t]-1-means[h][0])
                    rec[f"tot{h}"]=d*(c[t+h]/c[t]-1)
                rows.append(rec)
    df=pd.DataFrame(rows)
    df["z24"]=df.r24.abs()/(df.vol*np.sqrt(24))
    df["zpre"]=df.pre.abs()/(df.vol*np.sqrt(2))
    def summ(g):
        out={}
        for h in (2,4,8,24):
            x=g[f"x{h}"]; out[f"m{h}%"]=x.mean()*100; out[f"t{h}"]=x.mean()/x.std()*np.sqrt(len(x))
        out["n"]=len(g); return pd.Series(out)
    res={}
    res["ct_vs_not"]=df.groupby("ct").apply(summ)
    ct=df[df.ct].copy()
    ct["q24"]=pd.qcut(ct.z24,5,labels=False)
    ct["qpre"]=pd.qcut(ct.zpre,5,labels=False)
    res["ct_by_trend_quintile"]=ct.groupby("q24").apply(summ)
    res["ct_by_pre_quintile"]=ct.groupby("qpre").apply(summ)
    nc=df[~df.ct].copy(); nc["q24"]=pd.qcut(nc.z24,5,labels=False)
    res["notct_by_trend_quintile"]=nc.groupby("q24").apply(summ)
    ct["both"]=(ct.q24>=3)&(ct.qpre>=3)
    res["ct_strong_both"]=ct.groupby("both").apply(summ)
    res["ct_by_coin"]=ct.groupby("coin").apply(summ)
    res["ct_by_hour"]=ct.groupby("hr").apply(summ)
    res["ct_by_year"]=ct.groupby("year").apply(summ)
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            tr.append(t[["profit_loss_percent","net_profit_loss_percent","duration_minutes","side"]])
    tr=pd.concat(tr)
    res["trades"]=tr.groupby("side").agg(["mean","count"])
    res["dur_desc"]=tr.duration_minutes.describe()
    return res
