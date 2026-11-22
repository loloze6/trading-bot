def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=84
    bars=data["bars"]
    rows=[]; G=[]
    for coin,ws in bars.items():
        rets=[]
        for w,df in ws.items():
            c=df["close"].values
            for i in range(0,len(c)-H,H): rets.append(c[i+H]/c[i]-1)
        rets=np.array(rets)
        if len(rets)<3: continue
        drift=rets.mean(); usual=rets.std()
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            h=df["high"];l=df["low"];c=df["close"]
            rng=(h.rolling(6).max()-l.rolling(6).min())/(h-l).rolling(180,min_periods=60).mean()
            r6=c/c.shift(6)-1
            z6=r6/r6.abs().rolling(180,min_periods=60).mean()
            lr=np.log(c).diff()
            volr=lr.rolling(42).std()/lr.rolling(540,min_periods=180).std()
            r84b=c/c.shift(84)-1
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(df["timestamp"])
            n=len(df)
            for g in range(0,n,H):
                if not np.isnan(fwd.iloc[g]):
                    G.append(dict(coin=coin,w=w,year=ts.iloc[g].year,volr=volr.iloc[g],r84b=r84b.iloc[g],
                                  st=(fwd.iloc[g]-drift)/usual))
                for i in range(g,min(g+H,n)):
                    if rng.iloc[i]>=7.5 and r6.iloc[i]>0 and not np.isnan(fwd.iloc[i]):
                        rows.append(dict(coin=coin,w=w,year=ts.iloc[i].year,z6=z6.iloc[i],rng=rng.iloc[i],
                                         volr=volr.iloc[i],r84b=r84b.iloc[i],st=(fwd.iloc[i]-drift)/usual,
                                         ex=fwd.iloc[i]-drift)); break
    P=pd.DataFrame(rows); G=pd.DataFrame(G)
    def s(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out={}
    out["rise panic spearman z6/rng/volr/r84b vs st"]=pd.DataFrame({k:stats.spearmanr(P[k],P.st,nan_policy="omit") for k in ["z6","rng","volr","r84b"]},index=["rho","p"]).T
    out["rise panic by year"]=P.groupby("year")["st"].apply(s).unstack()
    out["rise panic by coin"]=P.groupby("coin")["st"].apply(s).unstack()
    out["rise panic median of coin means>0 share"]=float((P.groupby("coin")["st"].mean()>0).mean())
    Gv=G.dropna(subset=["volr"])
    out["grid volr spearman"]=pd.Series(stats.spearmanr(Gv.volr,Gv.st)[:2],index=["rho","p"])
    Gv["vq"]=pd.qcut(Gv.volr,5,labels=False)
    out["grid volr quintile by year (mean st)"]=Gv.groupby(["year","vq"])["st"].mean().unstack()
    out["grid volr rho by coin"]=Gv.groupby("coin").apply(lambda d:pd.Series(dict(n=len(d),rho=stats.spearmanr(d.volr,d.st)[0])))
    out["grid volr rho by coin share>0"]=float((out["grid volr rho by coin"].rho>0).mean())
    # volr within r84b sign
    Gv["up14"]=np.where(Gv.r84b>0,"up14","down14")
    out["grid volr quint x prior14 sign"]=Gv.groupby(["up14","vq"])["st"].apply(s).unstack()
    # book: days in position vs out
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items(): D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book daily by year"]=D.groupby(pd.to_datetime(D.day).dt.year)[["book_return","coin_return"]].mean()
    return out
