def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; hb=[]
    for coin,ws in data["bars"].items():
        # coin drift and usual move over all windows, grid 18
        g=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-H,H)
            g.append(c[idx+H]/c[idx]-1)
        g=np.concatenate(g); drift=g.mean(); sd=g.std()
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"]; v=df["volume"]
            r1=c.pct_change()
            ma=r1.abs().rolling(180,min_periods=60).mean()
            vol180=r1.rolling(180,min_periods=60).std()
            ret6=c/c.shift(6)-1; ret18=c/c.shift(18)-1; ret42=c/c.shift(42)-1
            sgn=np.sign(r1.fillna(0)).values
            streak=np.zeros(len(c))
            for i in range(1,len(c)):
                if sgn[i]!=0 and sgn[i]==np.sign(streak[i-1]): streak[i]=streak[i-1]+sgn[i]
                else: streak[i]=sgn[i]
            vrel=v/v.rolling(42,min_periods=20).mean()
            rng=(df["high"]-df["low"])/c
            rngrel=rng/rng.rolling(180,min_periods=60).mean()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(df["timestamp"])
            idx=np.arange(0,len(c)-H,H)
            for i in idx:
                rows.append(dict(coin=coin,w=w,f6=ret6[i]/ma[i] if ma[i] else np.nan,
                  f18=ret18[i]/ma[i] if ma[i] else np.nan,f42=ret42[i]/ma[i] if ma[i] else np.nan,
                  streak=streak[i],vol=vol180[i],vrel=vrel[i],rngrel=rngrel[i],
                  fc=df["forecast"][i],s=(fwd[i]-drift)/sd,raw=fwd[i]))
            f1=c.shift(-1)/c-1
            hb.append(pd.DataFrame(dict(coin=coin,hour=ts.dt.hour,wd=ts.dt.weekday,r=f1/ (r1.abs().mean()), s6=c.shift(-6)/c-1)))
    R=pd.DataFrame(rows)
    out={}
    def grp(col,q=5):
        d=R.dropna(subset=[col,"s"]).copy()
        d["b"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        a=d.groupby("b")["s"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        a["mean_feat"]=d.groupby("b")[col].mean()
        return a.round(4)
    for col in ["f6","f18","f42","vol","vrel","rngrel"]:
        out["strength by "+col+" quintile"]=grp(col)
    d=R.dropna(subset=["s"]).copy(); d["st"]=d["streak"].clip(-5,5)
    a=d.groupby("st")["s"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); out["strength by streak (signed, clipped 5)"]=a.round(4)
    d["fb"]=pd.cut(d["fc"],[-0.1,0.01,5,10,15,20.1])
    a=d.groupby("fb")["s"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); out["strength by forecast bin"]=a.round(4)
    # vol interaction with f18
    d=R.dropna(subset=["f18","vol","s"]).copy()
    d["vq"]=d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    d["fq"]=d.groupby("coin")["f18"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["mean strength vol tercile x f18 tercile"]=d.pivot_table(index="vq",columns="fq",values="s",aggfunc="mean").round(4)
    out["count vol x f18"]=d.pivot_table(index="vq",columns="fq",values="s",aggfunc="count")
    HB=pd.concat(hb).dropna()
    a=HB.groupby("hour")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); out["next-bar return /mean abs, by hour"]=a.round(4)
    a=HB.groupby("wd")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); out["next-bar return /mean abs, by weekday"]=a.round(4)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            x=df.copy(); x["coin"]=coin; x["w"]=w; D.append(x)
    D=pd.concat(D).dropna(subset=["book_return","coin_return"])
    dd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book daily corr with coin"]=float(dd["book_return"].corr(dd["coin_return"]))
    q=dd["book_return"].quantile([0.02,0.98])
    out["coin ret on book worst 2% days"]=float(dd[dd.book_return<=q.iloc[0]]["coin_return"].mean())
    out["coin ret on book best 2% days"]=float(dd[dd.book_return>=q.iloc[1]]["coin_return"].mean())
    dd["yr"]=pd.to_datetime(dd["day"]).dt.year
    a=dd.groupby("yr")[["book_return","coin_return"]].mean()*1e4; out["mean daily bp by year"]=a.round(2)
    return out
