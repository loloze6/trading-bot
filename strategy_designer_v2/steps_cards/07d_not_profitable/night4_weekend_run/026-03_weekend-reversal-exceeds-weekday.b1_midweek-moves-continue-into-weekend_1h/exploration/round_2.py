def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; out={}
    drift={}; usual={}
    for c in bars:
        g=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-48,48)
            g+=list(cl[idx+48]/cl[idx]-1)
        drift[c]=np.mean(g); usual[c]=np.std(g)
    rows=[]; allrows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"]); cl=df["close"].values
            wd=ts.dt.weekday.values; hr=ts.dt.hour.values
            al=df["postRebalance_current_allocation"].values
            for i in np.where(hr==23)[0]:
                if i<48 or i+96>=len(cl): continue
                raw=cl[i]/cl[i-48]-1
                r24=cl[i+24]/cl[i]-1; r48=cl[i+48]/cl[i]-1; r96=cl[i+96]/cl[i]-1
                ret14=cl[i]/cl[i-336]-1 if i>=336 else np.nan
                vr=np.std(np.diff(np.log(cl[i-48:i+1])))/ (np.std(np.diff(np.log(cl[max(0,i-720):i+1]))))
                s=np.sign(raw)
                rec=dict(coin=c,wd=wd[i],z=raw/usual[c],r24=s*r24,r48=s*r48,r96=s*r96,
                         u48=s*(r48-drift[c]),side="up" if s>0 else "down",
                         trend=np.sign(ret14)==s if not np.isnan(ret14) else np.nan,vr=vr,
                         alloc=abs(al[i]))
                allrows.append(rec)
    d=pd.DataFrame(allrows)
    d["zq"]=d.groupby("wd")["z"].transform(lambda x:pd.qcut(x.abs(),5,labels=False))
    t=lambda x:x.mean()/x.std()*np.sqrt(len(x))
    th=d[d.wd==3]
    out["Thu cases: |z| quintile x side, r48"]=th.groupby(["zq","side"]).agg(n=("r48","size"),r48=("r48","mean"),t=("r48",t))
    out["Thu cases: |z| quintile, r24 r48 r96"]=th.groupby("zq").agg(r24=("r24","mean"),r48=("r48","mean"),r96=("r96","mean"),t96=("r96",t),alloc=("alloc","mean"))
    out["all weekdays top |z| quintile: r48 by weekday"]=d[d.zq==4].groupby("wd").agg(n=("r48","size"),r48=("r48","mean"),t=("r48",t))
    out["all weekdays top two quintiles: r48 by side"]=d[d.zq>=3].groupby("side").agg(n=("r48","size"),r48=("r48","mean"),t=("r48",t))
    th2=th.dropna(subset=["trend"])
    out["Thu: move along 14d trend?"]=th2.groupby(["trend"]).agg(n=("r48","size"),r48=("r48","mean"),t=("r48",t))
    th["vq"]=pd.qcut(th.vr,3,labels=False)
    out["Thu: by 48h vol / 30d vol tercile"]=th.groupby("vq").agg(n=("r48","size"),r48=("r48","mean"),t=("r48",t))
    tr=pd.concat([x.assign(coin=c) for c in data["trades"] for x in data["trades"][c].values()])
    tr["et"]=pd.to_datetime(tr.entry_time)
    tr["ewd"]=tr.et.dt.weekday; tr["eh"]=tr.et.dt.hour
    out["trades by entry weekday"]=tr.groupby("ewd").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes",lambda x:x.mean()/60))
    tr["fq"]=pd.qcut(tr.entry_forecast.abs(),4,labels=False,duplicates="drop")
    out["trades by |entry forecast| quartile"]=tr.groupby("fq").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    return out
