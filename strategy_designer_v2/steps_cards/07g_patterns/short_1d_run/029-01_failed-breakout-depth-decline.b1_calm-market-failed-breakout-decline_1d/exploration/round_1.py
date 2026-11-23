def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]; rows1=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float); op=b["open"].astype(float)
            r=c.pct_change()
            vol20=r.rolling(20).std()
            r5=c/c.shift(5)-1; r20=c/c.shift(20)-1
            ph=c.shift(1).rolling(20).max(); pl=c.shift(1).rolling(20).min()
            dist_hi=(c/ph-1)/vol20
            dist_lo=(c/pl-1)/vol20
            bo=(c>ph)
            fb=pd.Series(False,index=b.index)
            for k in (1,2,3):
                fb|= bo.shift(k,fill_value=False)&(c<ph.shift(k))
            rng=(hi-lo)/c
            clv=((c-lo)/(hi-lo)).replace([np.inf,-np.inf],np.nan)
            vchg=np.log(vol20/vol20.shift(20))
            volu=np.log(b["volume"].astype(float)/b["volume"].astype(float).rolling(20).mean())
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            fwd=c.shift(-H)/c-1
            for i in range(0,len(b),H):
                if i+H>=len(b): break
                rows.append(dict(coin=coin,w=w,fwd=fwd[i],r5z=r5[i]/(vol20[i]*np.sqrt(5)) if vol20[i]>0 else np.nan,
                    r20z=r20[i]/(vol20[i]*np.sqrt(20)) if vol20[i]>0 else np.nan,vol=vol20[i],dist_hi=dist_hi[i],dist_lo=dist_lo[i],
                    bo=bo[i],fb=fb[i],rng=rng[i]/vol20[i] if vol20[i]>0 else np.nan,clv=clv[i],vchg=vchg[i],volu=volu[i],wd=wd[i],
                    r1z=r[i]/vol20[i] if vol20[i]>0 else np.nan))
            f1=c.shift(-1)/c-1
            for i in range(len(b)-1):
                rows1.append(dict(coin=coin,w=w,fwd=f1[i],wd=wd[i],r1z=r[i]/vol20[i] if vol20[i]>0 else np.nan))
    d=pd.DataFrame(rows); d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d1=pd.DataFrame(rows1); d1["ex"]=d1["fwd"]-d1.groupby("coin")["fwd"].transform("mean")
    def summ(df,key):
        g=df.dropna(subset=[key,"ex"]).groupby(key)["ex"]
        out=pd.DataFrame({"n":g.size(),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))})
        return out.round(3)
    res={}
    for f in ["r5z","r20z","vol","dist_hi","dist_lo","rng","clv","vchg","volu","r1z"]:
        d[f+"_q"]=d.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        res[f+" quintile->5d"]=summ(d,f+"_q")
    res["breakout today ->5d"]=summ(d,"bo"); res["failed bo ->5d"]=summ(d,"fb")
    res["weekday->5d"]=summ(d,"wd"); res["weekday->1d"]=summ(d1,"wd")
    d1["r1q"]=d1.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    res["r1z quintile ->1d"]=summ(d1,"r1q")
    res["coin mean 5d %"]=(d.groupby("coin")["fwd"].agg(["mean","std","size"])*[100,100,1]).round(3)
    return res
