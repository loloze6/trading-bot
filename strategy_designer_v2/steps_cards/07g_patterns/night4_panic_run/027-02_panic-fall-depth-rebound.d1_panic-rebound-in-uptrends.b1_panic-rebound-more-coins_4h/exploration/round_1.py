def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=84
    bars=data["bars"]
    rows=[]; allgrid=[]; hourly=[]
    for coin,ws in bars.items():
        # drift/usual
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
            sc=r6.abs().rolling(180,min_periods=60).mean()
            z6=r6/sc
            r540=c/c.shift(540)-1
            r84b=c/c.shift(84)-1
            vol=(np.log(c).diff()).rolling(42).std()
            volr=vol/(np.log(c).diff()).rolling(540,min_periods=180).std()
            fwd=c.shift(-H)/c-1
            fwd6=c.shift(-6)/c-1
            ts=pd.to_datetime(df["timestamp"])
            n=len(df)
            for g in range(0,n,H):
                seg=range(g,min(g+H,n))
                # grid point
                if not np.isnan(fwd.iloc[g]):
                    allgrid.append(dict(coin=coin,w=w,z6=z6.iloc[g],r84b=r84b.iloc[g],volr=volr.iloc[g],rng=rng.iloc[g],
                        ex=(fwd.iloc[g]-drift)/usual,exr=fwd.iloc[g]-drift))
                for i in seg:
                    if rng.iloc[i]>=7.5 and not np.isnan(fwd.iloc[i]):
                        rows.append(dict(coin=coin,w=w,z6=z6.iloc[i],r6=r6.iloc[i],r540=r540.iloc[i],r84b=r84b.iloc[i],
                            rng=rng.iloc[i],ex=fwd.iloc[i]-drift,st=(fwd.iloc[i]-drift)/usual,ex6=fwd6.iloc[i],
                            year=ts.iloc[i].year))
                        break
    P=pd.DataFrame(rows); G=pd.DataFrame(allgrid)
    def summ(d,col="ex"):
        x=d[col].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,strength=d.loc[x.index,"st"].mean() if "st" in d else np.nan))
    out={}
    P["dir"]=np.where(P.r6<0,"fall","rise")
    out["panic by dir"]=P.groupby("dir").apply(summ)
    P["trend"]=np.where(P.r540.isna(),"na",np.where(P.r540>0,"up90","down90"))
    out["panic dir x trend"]=P.groupby(["dir","trend"]).apply(summ)
    P["zq"]=pd.qcut(P.z6,5,labels=False)
    out["panic by z6 quintile"]=P.groupby("zq").apply(lambda d:pd.concat([summ(d),pd.Series({"z6":d.z6.mean()})]))
    P["rq"]=pd.qcut(P.rng,4,labels=False)
    out["panic by range quartile"]=P.groupby("rq").apply(lambda d:pd.concat([summ(d),pd.Series({"rng":d.rng.mean()})]))
    P["bq"]=pd.qcut(P.r84b,4,labels=False)
    out["panic by prior14d quartile"]=P.groupby("bq").apply(lambda d:pd.concat([summ(d),pd.Series({"r84b":d.r84b.mean()})]))
    out["panic by year"]=P.groupby("year").apply(summ)
    out["panic next24h by dir"]=P.groupby("dir")["ex6"].agg(["count","mean"])
    # all grid
    G["zq"]=pd.qcut(G.z6,5,labels=False)
    out["grid by z6 quintile (strength)"]=G.groupby("zq")["ex"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    G["bq"]=pd.qcut(G.r84b,5,labels=False)
    out["grid by prior14d quintile (strength)"]=G.groupby("bq")["ex"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    G["vq"]=pd.qcut(G.volr,5,labels=False)
    out["grid by volratio quintile (strength)"]=G.groupby("vq")["ex"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # book: trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    out["trades"]=pd.Series(dict(n=len(T),mean_net=T.net_profit_loss_percent.mean(),win=(T.net_profit_loss_percent>0).mean(),
        med_dur_days=T.duration_minutes.median()/1440))
    return out
