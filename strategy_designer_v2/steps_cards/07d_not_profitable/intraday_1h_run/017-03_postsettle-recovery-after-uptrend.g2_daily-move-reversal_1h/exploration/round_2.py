def explore(data):
    import numpy as np, pandas as pd
    out={}
    # book daily returns from days table
    br=[];cr=[]
    for coin in data["days"]:
        for w,d in data["days"][coin].items():
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
    br=pd.concat(br); cr=pd.concat(cr)
    out["book daily"]=pd.Series(dict(mean=br.mean(),sd=br.std(),n=len(br),hold_mean=cr.mean()))
    # forecast persistence and gain by |forecast| tercile on 24h grid, plus by vol regime
    rows=[]; ac=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            vol=pd.Series(r1).rolling(168,min_periods=42).std().values
            volz=pd.Series(vol).rolling(720,min_periods=168).rank(pct=True).values
            ret24=np.r_[np.full(24,np.nan),c[24:]/c[:-24]-1]
            ret7d=np.r_[np.full(168,np.nan),c[168:]/c[:-168]-1]
            fs=pd.Series(f)
            ac.append(dict(a1=fs.autocorr(1),a6=fs.autocorr(6),a24=fs.autocorr(24)))
            idx=np.arange(0,len(c)-24,24)
            fr=c[idx+24]/c[idx]-1
            for i,j in enumerate(idx):
                rows.append(dict(coin=coin,f=f[j],fr=fr[i],volq=volz[j],t7=ret7d[j],r24=ret24[j]))
    D=pd.DataFrame(rows).dropna()
    D["prod"]=D["f"]/10*(D["fr"]-D.groupby("coin")["fr"].transform("mean"))
    out["forecast autocorr"]=pd.DataFrame(ac).mean()
    D["absq"]=pd.qcut(D["f"].abs(),3,labels=["lo","mid","hi"])
    g=lambda s: pd.Series(dict(mean=s.mean(),t=s.mean()/s.std()*np.sqrt(len(s)),n=len(s)))
    out["prod by |f| tercile"]=D.groupby("absq")["prod"].apply(g).unstack()
    D["vq"]=pd.cut(D["volq"],[0,1/3,2/3,1],labels=["lowvol","midvol","hivol"])
    out["prod by vol tercile"]=D.groupby("vq")["prod"].apply(g).unstack()
    D["agree7"]=np.where(np.sign(D["t7"])==np.sign(D["r24"]),"day with 7d trend","day against 7d trend")
    out["prod by 7d trend agreement"]=D.groupby("agree7")["prod"].apply(g).unstack()
    D["t7q"]=pd.qcut(D["t7"].abs(),3,labels=["weak7","mid7","strong7"])
    out["prod by |7d trend|"]=D.groupby("t7q")["prod"].apply(g).unstack()
    return out
