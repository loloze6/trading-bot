def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1=c.pct_change()
            hh=h.rolling(30).max(); ll=l.rolling(30).min(); rng=hh-ll
            nm=(c-c.shift(30)).abs()/rng
            stoch=(c-ll)/rng
            r10=c/c.shift(10)-1; r30=c/c.shift(30)-1; r3=c/c.shift(3)-1
            vol=r1.rolling(20).std()
            f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame(dict(coin=coin,w=w,r1=r1,r3=r3,r10=r10,r30=r30,nm=nm,stoch=stoch,vol=vol,f5=f5,
                                 fc=b["forecast"],alloc=b["postRebalance_current_allocation"],wd=ts.dt.weekday))
            df=df.iloc[::5]
            rows.append(df)
        for w,d in data["days"][coin].items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; drows.append(dd)
    g=pd.concat(rows); g=g.dropna(subset=["f5"])
    g["ex"]=g["f5"]-g.groupby("coin")["f5"].transform("mean")
    g["exz"]=g["ex"]/g.groupby("coin")["f5"].transform("std")
    for col in ["r1","r3","r10","r30","vol"]:
        g[col+"z"]=g[col]/g.groupby("coin")[col].transform("std")
    def summ(grp):
        x=grp["exz"].dropna(); n=len(x)
        return pd.Series(dict(n=n,mean_exz=x.mean(),t=x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,mean_ex=grp["ex"].mean()))
    out={}
    gg=g.dropna(subset=["r10z","nm"]).copy()
    gg["q10"]=pd.qcut(gg["r10z"],5,labels=False)
    gg["trend"]=np.where(gg["nm"]>=0.5,"trend","flat")
    gg["side"]=np.where(gg["stoch"]>=0.5,"upper","lower")
    out["r10 quintile x trend"]=gg.groupby(["trend","q10"]).apply(summ)
    out["r10 quintile x side"]=gg.groupby(["side","q10"]).apply(summ)
    gg["qs"]=pd.qcut(gg["stoch"],5,labels=False)
    out["stoch quintile x trend"]=gg.groupby(["trend","qs"]).apply(summ)
    for col in ["r1z","r3z","r30z","volz"]:
        x=g.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],5,labels=False,duplicates="drop")
        out[col+" quintile"]=x.groupby("q").apply(summ)
    out["weekday 5d"]=g.groupby("wd").apply(summ)
    D=pd.concat(drows); D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["weekday daily coin"]=D.groupby("wd")["coin_return"].agg(["mean","count",lambda s:s.mean()/(s.std()/np.sqrt(s.count()))])
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series(dict(mean=bk.book_return.mean(),hold=bk.coin_return.mean(),corr=bk.corr().iloc[0,1]))
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t)
    T=pd.concat(T)
    T["fq"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades by entry fc quartile"]=T.groupby("fq")[["entry_forecast","profit_loss_percent","net_profit_loss_percent"]].mean().assign(n=T.groupby("fq").size())
    return out
