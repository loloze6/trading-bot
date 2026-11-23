def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        means={}
        for h in (2,8):
            vals=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-h,h)
                vals.append(c[idx+h]/c[idx]-1)
            means[h]=np.concatenate(vals).mean()
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values; n=len(c); hr=ts.dt.hour.values
            r1=np.r_[np.nan,np.diff(np.log(c))]
            vol=pd.Series(r1).rolling(168).std().values
            for t in np.where(np.isin(hr,[23,7,15]))[0]:
                if t<24 or t+8>=n: continue
                pre=c[t]/c[t-2]-1; r24=c[t]/c[t-24]-1; d=np.sign(r24)
                if d==0 or not np.isfinite(vol[t]): continue
                rows.append(dict(coin=coin,hr=hr[t],ct=pre*r24<0,side=d,
                    z24=abs(r24)/(vol[t]*np.sqrt(24)),zpre=abs(pre)/(vol[t]*np.sqrt(2)),
                    x2=d*(c[t+2]/c[t]-1-means[2]),tot2=d*(c[t+2]/c[t]-1),
                    x8=d*(c[t+8]/c[t]-1-means[8]),tot8=d*(c[t+8]/c[t]-1)))
    df=pd.DataFrame(rows)
    q24=df.z24.quantile([.6,.8]).values; qp=df[df.ct].zpre.quantile([.6,.8]).values
    df["strong"]=(df.z24>=q24[0])&(df.zpre>=qp[0])
    df["prod"]=df.z24*df.zpre
    def summ(g):
        o={}
        for k in ("x2","tot2","x8","tot8"):
            x=g[k]; o[k+"%"]=x.mean()*100; o["t_"+k]=x.mean()/x.std()*np.sqrt(len(x))
        o["n"]=len(g); return pd.Series(o)
    res={}
    ct=df[df.ct]
    res["ct_side"]=ct.groupby("side").apply(summ)
    res["ct_side_hour"]=ct.groupby(["side","hr"]).apply(summ)
    res["ct_strong_side"]=ct[ct.strong].groupby("side").apply(summ)
    res["ct_strong_hr"]=ct[ct.strong].groupby("hr").apply(summ)
    c2=ct.copy(); c2["qp"]=pd.qcut(c2["prod"],10,labels=False)
    res["ct_prod_decile"]=c2.groupby("qp").apply(summ)
    # condition alone: strong pre-move WITH trend (no ct) and strong trend no ct
    nc=df[~df.ct]
    res["notct_strong"]=nc[(nc.z24>=q24[0])&(nc.zpre>=nc.zpre.quantile(.6))].groupby("side").apply(summ)
    # book holdings
    sh=[];held=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"].fillna(0).values
            f=b["forecast"].fillna(0).values
            sh.append((a!=0).mean()); held.append(((a!=0)&(f==0)).mean())
    res["share_bars_in_position"]=float(np.mean(sh))
    res["share_bars_pos_no_forecast"]=float(np.mean(held))
    tr=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    tr["long"]=tr.duration_minutes>180
    res["trades_by_dur"]=tr.groupby(["side","long"])[["profit_loss_percent","net_profit_loss_percent"]].agg(["mean","count"])
    return res
