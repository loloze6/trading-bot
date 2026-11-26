def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change()
            vol=r1.rolling(30,min_periods=20).std()
            hi5=c.rolling(5,min_periods=5).max()
            dist=(c-hi5)/hi5/vol
            lo5=c.rolling(5,min_periods=5).min()
            distlo=(c-lo5)/lo5/vol
            p5=(c/c.shift(5)-1)/vol
            p1=r1/vol
            vrank=vol.rolling(60,min_periods=30).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            for h in (1,5):
                f=c.shift(-h)/c-1
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,fwd=f.iloc[i],dist=dist.iloc[i],distlo=distlo.iloc[i],
                        p5=p5.iloc[i],p1=p1.iloc[i],vr=vrank.iloc[i],reg=b["regime"].iloc[i],
                        wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year,fc=b["forecast"].iloc[i],
                        day=ts.iloc[i].normalize(),rng=((b["high"]-b["low"])/c/vol).iloc[i],
                        clpos=((c-b["low"])/(b["high"]-b["low"])).iloc[i]))
    D=pd.DataFrame(rows)
    D["ex"]=D["fwd"]-D.groupby(["coin","h"])["fwd"].transform("mean")
    def summ(g):
        g=g.dropna(subset=["ex"])
        m=g["ex"].mean(); s=g["ex"].std(); k=len(g)
        return pd.Series(dict(n=k,mean_ex_pct=100*m,t=m/(s/np.sqrt(k)) if k>2 else np.nan))
    out={}
    D5=D[D.h==5].copy(); D1=D[D.h==1].copy()
    D5["inprof"]=D5.reg=="unknown"; D1["inprof"]=D1.reg=="unknown"
    for nm,col in [("dist",'dist'),("distlo","distlo"),("p5","p5"),("p1","p1"),("vr","vr"),("rng","rng"),("clpos","clpos")]:
        for H,DD in [("5d",D5),("1d",D1)]:
            x=DD.dropna(subset=[col]).copy()
            x["q"]=pd.qcut(x[col],5,labels=False,duplicates="drop")
            out[f"{H} by {nm} quintile x inprofile"]=x.groupby(["inprof","q"]).apply(summ).round(3)
    out["5d by regime"]=D5.groupby("reg").apply(summ).round(3)
    out["1d by weekday"]=D1.groupby("wd").apply(summ).round(3)
    out["5d by year inprof"]=D5[D5.inprof].groupby("yr").apply(summ).round(3)
    # book
    B=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; B.append(dd)
    B=pd.concat(B)
    bd=B.groupby(["w","day"])["book_return"].mean().dropna()
    out["book daily by window"]=bd.groupby(level=0).agg(["count","mean","std"]).assign(mean=lambda x:x["mean"]*100)
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; T.append(tt)
    T=pd.concat(T)
    T["fq"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades by entry forecast q"]=T.groupby(["side","fq"])["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    return out
