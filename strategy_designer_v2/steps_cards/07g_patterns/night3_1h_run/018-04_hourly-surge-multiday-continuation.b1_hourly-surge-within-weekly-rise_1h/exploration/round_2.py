def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=120
    rows=[]; hr=[]; big=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1=c.pct_change()
            hi=c.rolling(720,min_periods=200).max(); lo=c.rolling(720,min_periods=200).min()
            pos=(c-lo)/(hi-lo)
            vol=r1.rolling(720,min_periods=120).std()
            volrel=vol/vol.rolling(2160,min_periods=500).mean()
            r24=c/c.shift(24)-1
            z=r24/r24.abs().rolling(720,min_periods=120).mean().shift(1)
            f120=c.shift(-H)/c-1; f240=c.shift(-240)/c-1
            idx=np.arange(0,len(c),H)
            wn=int(w[1:])
            rows.append(pd.DataFrame({"coin":coin,"half":"early" if wn<=12 else "late",
                "pos":pos.iloc[idx].values,"volrel":volrel.iloc[idx].values,"z":z.iloc[idx].values,
                "f120":f120.iloc[idx].values,"f240":f240.iloc[idx].values}))
            # hour 21-22 vs rest per day: 2h return from close of hour 20 bar
            h=ts.dt.hour
            hr.append(pd.DataFrame({"coin":coin,"half":"early" if wn<=12 else "late","h":h,"r":r1.values}))
            # large 1h moves standardised
            zs=r1/vol.shift(1)
            f24=c.shift(-24)/c-1
            g=pd.DataFrame({"coin":coin,"zs":zs,"f24":f24}).iloc[::24]
            big.append(g)
    D=pd.concat(rows).dropna(subset=["f120"])
    D["u"]=D["f120"]-D.groupby("coin")["f120"].transform("mean")
    D2=D.dropna(subset=["f240"]).copy()
    D2["u240"]=D2["f240"]-D2.groupby("coin")["f240"].transform("mean")
    out={}
    def topq(col,ucol,X):
        x=X.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        x=x[x["q"]==4]
        g=x.groupby(["coin"])[ucol].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g2=x.groupby(["half"])[ucol].agg(["mean","count","std"]); g2["t"]=g2["mean"]/(g2["std"]/np.sqrt(g2["count"]))
        return pd.concat([g,g2]).round(4)
    out["pos top quintile u120 by coin/half"]=topq("pos","u",D)
    out["pos top quintile u240 by coin/half"]=topq("pos","u240",D2)
    out["volrel top quintile u120"]=topq("volrel","u",D)
    out["z top quintile u120"]=topq("z","u",D)
    Hh=pd.concat(hr).dropna()
    Hh["u"]=Hh["r"]-Hh.groupby("coin")["r"].transform("mean")
    sel=Hh[Hh["h"].isin([21,22])]
    g=sel.groupby(["coin"])["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g2=sel.groupby(["half"])["u"].agg(["mean","count","std"]); g2["t"]=g2["mean"]/(g2["std"]/np.sqrt(g2["count"]))
    out["hours 21-22 bps"]=(pd.concat([g,g2]).assign(mean=lambda d:d["mean"]*1e4)).round(2)
    B=pd.concat(big).dropna()
    B["u"]=B["f24"]-B.groupby("coin")["f24"].transform("mean")
    B["b"]=pd.cut(B["zs"],[-99,-3,-1.5,0,1.5,3,99])
    g=B.groupby("b")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["24h after 1h move (sd units)"]=g.round(4)
    # book's largest losses: day before/after
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["prev"]=d["book_return"].shift(1); d["next"]=d["book_return"].shift(-1); d["coin"]=coin
            dd.append(d)
    Dd=pd.concat(dd).dropna(subset=["book_return"])
    q=Dd["book_return"].quantile([0.02,0.98])
    lo=Dd[Dd["book_return"]<=q.iloc[0]]; hi_=Dd[Dd["book_return"]>=q.iloc[1]]
    out["around extreme book days bps"]=pd.DataFrame({"worst":[lo["prev"].mean()*1e4,lo["book_return"].mean()*1e4,lo["next"].mean()*1e4,len(lo)],
        "best":[hi_["prev"].mean()*1e4,hi_["book_return"].mean()*1e4,hi_["next"].mean()*1e4,len(hi_)]},index=["prev","day","next","n"]).round(1)
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["fb"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades net by entry forecast quartile"]=T.groupby("fb")[["entry_forecast","net_profit_loss_percent"]].agg(["mean","count"]).round(3)
    return out
