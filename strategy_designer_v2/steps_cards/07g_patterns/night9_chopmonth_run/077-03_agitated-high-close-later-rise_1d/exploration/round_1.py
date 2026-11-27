def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values; o=b["open"].values
            n=len(b)
            rng=h-l
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            ret1=np.r_[np.nan,c[1:]/c[:-1]-1]
            agit=(b["regime"]!="chop").values
            ts=pd.to_datetime(b["timestamp"])
            vol20=pd.Series(ret1).rolling(20).std().values
            rng_rel=rng/c
            rngz=pd.Series(rng_rel).rolling(20).apply(lambda x:(x[-1]-x.mean())/x.std() if x.std()>0 else np.nan,raw=True).values
            r20=np.r_[[np.nan]*20,c[20:]/c[:-20]-1] if n>20 else np.full(n,np.nan)
            alloc=b["postRebalance_current_allocation"].values
            for t in range(n):
                f1=c[t+1]/c[t]-1 if t+1<n else np.nan
                f17=c[t+7]/c[t+1]-1 if t+7<n else np.nan
                f7=c[t+7]/c[t]-1 if t+7<n else np.nan
                rows.append(dict(coin=coin,w=w,pos=t,cl=cl[t],agit=agit[t],r1=ret1[t],f1=f1,f17=f17,f7=f7,
                    wd=ts.iloc[t].weekday(),yr=ts.iloc[t].year,vol20=vol20[t],rngz=rngz[t],r20=r20[t],
                    body=(c[t]-o[t])/rng[t] if rng[t]>0 else np.nan,alloc=alloc[t]))
    d=pd.DataFrame(rows)
    # drift per coin over 7 days on grid
    g7=d[d.pos%7==0]
    drift7=g7.groupby("coin").f7.mean(); drift6=g7.groupby("coin").f17.mean()
    d["u7"]=d.f7-d.coin.map(drift7); d["u17"]=d.f17-d.coin.map(drift6)
    d["clq"]=pd.cut(d.cl,[-.01,.2,.4,.6,.8,1.01],labels=["0-.2",".2-.4",".4-.6",".6-.8",".8-1"])
    def tab(sub,col,by):
        x=sub.dropna(subset=[col])
        r=x.groupby(by)[col].agg(["mean","count","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.drop(columns="std")
    gg=d[d.pos%7==0]
    out={}
    out["f17 by cl, agit x grid7"]=tab(gg,"u17",["agit","clq"])
    out["f1 by cl, agit (all bars)"]=tab(d,"f1",["agit","clq"])
    out["u7 by cl agit grid7"]=tab(gg,"u7",["agit","clq"])
    # correlation of cl with u17 by agit
    for a in [True,False]:
        x=gg[gg.agit==a].dropna(subset=["cl","u17"])
        out[f"spearman cl-u17 agit={a}"]=f"{stats.spearmanr(x.cl,x.u17)[0]:.4f} n={len(x)}"
    # after large moves: r1 deciles vs f1 and u7
    d["r1q"]=pd.qcut(d.r1,5,labels=False)
    out["f1 by r1 quintile x agit"]=tab(d,"f1",["agit","r1q"])
    out["u7 by r1 quintile x agit grid7"]=tab(d[d.pos%7==0].assign(r1q=d.r1q),"u7",["agit","r1q"])
    d["vq"]=d.groupby("coin").vol20.transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["f1 by weekday"]=tab(d,"f1","wd")
    out["u7 by r20 quintile grid7"]=tab(d[d.pos%7==0].assign(q=pd.qcut(d.r20,5,labels=False)),"u7","q")
    out["u7 by rngz tercile x cl hi/lo agit grid7"]=tab(gg[gg.agit].assign(rq=pd.qcut(gg.rngz,3,labels=False),hi=gg.cl>=0.5),"u7",["rq","hi"])
    # book days: largest gains/losses
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    D=pd.concat(dd)
    out["book ret by year"]=D.assign(yr=pd.to_datetime(D.day).dt.year).groupby("yr")[["book_return","coin_return"]].mean()
    return out
