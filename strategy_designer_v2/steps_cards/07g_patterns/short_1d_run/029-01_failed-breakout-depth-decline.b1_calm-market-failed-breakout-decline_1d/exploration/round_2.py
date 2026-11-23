def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]; rows1=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change(); vol20=r.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"]); yr=ts.dt.year; wd=ts.dt.weekday
            ph=c.shift(1).rolling(20).max()
            fwd=c.shift(-H)/c-1; f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1
            vq=vol20.rank(pct=True)
            for i in range(0,len(b),H):
                if i+H>=len(b): break
                rows.append(dict(coin=coin,w=w,yr=yr[i],fwd=fwd[i],r1z=r[i]/vol20[i] if vol20[i]>0 else np.nan,
                                 bo=bool(c[i]>ph[i]) if not np.isnan(ph[i]) else np.nan,vol=vol20[i],
                                 pos=b["postRebalance_current_allocation"][i]))
            for i in range(len(b)-1):
                rows1.append(dict(coin=coin,w=w,yr=yr[i],wd=wd[i],fwd=f1[i],r1z=r[i]/vol20[i] if vol20[i]>0 else np.nan,vol=vol20[i]))
    d=pd.DataFrame(rows); d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d1=pd.DataFrame(rows1); d1["ex"]=d1["fwd"]-d1.groupby("coin")["fwd"].transform("mean")
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    res={}
    d["q"]=d.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    d1["q"]=d1.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    top=d[d.q==4]; low1=d1[d1.q==0]
    res["5d after top r1z quintile, by coin"]=top.groupby("coin")["ex"].apply(tt).unstack().round(3)
    res["5d after top r1z quintile, by year"]=top.groupby("yr")["ex"].apply(tt).unstack().round(3)
    res["1d after bottom r1z quintile, by coin"]=low1.groupby("coin")["ex"].apply(tt).unstack().round(3)
    res["1d after bottom r1z quintile, by year"]=low1.groupby("yr")["ex"].apply(tt).unstack().round(3)
    # graded slope: regress 5d excess (in vol units) on r1z per coin
    d["exz"]=d["ex"]/(d["vol"]*np.sqrt(5))
    sl={}
    for coin,g in d.dropna(subset=["r1z","exz"]).groupby("coin"):
        x=g.r1z.clip(-4,4); y=g.exz; b_=np.polyfit(x,y,1)[0]; cr=np.corrcoef(x,y)[0,1]
        sl[coin]={"slope":b_,"corr":cr,"t":cr*np.sqrt((len(g)-2)/(1-cr**2)),"n":len(g)}
    res["5d excess (vol units) on r1z, per coin"]=pd.DataFrame(sl).T.round(3)
    d1["exz"]=d1["ex"]/d1["vol"]
    sl={}
    for coin,g in d1.dropna(subset=["r1z","exz"]).groupby("coin"):
        x=g.r1z.clip(-4,4); y=g.exz; cr=np.corrcoef(x,y)[0,1]
        sl[coin]={"corr":cr,"t":cr*np.sqrt((len(g)-2)/(1-cr**2)),"n":len(g)}
    res["1d excess on r1z, per coin"]=pd.DataFrame(sl).T.round(3)
    res["5d after breakout, by coin"]=d[d.bo==True].groupby("coin")["ex"].apply(tt).unstack().round(3)
    res["5d after breakout, by year"]=d[d.bo==True].groupby("yr")["ex"].apply(tt).unstack().round(3)
    res["1d Friday by coin"]=d1[d1.wd==4].groupby("coin")["ex"].apply(tt).unstack().round(3)
    res["1d Friday by year"]=d1[d1.wd==4].groupby("yr")["ex"].apply(tt).unstack().round(3)
    # book
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    D=pd.concat(dd)
    D["inpos"]=D["book_return"].abs()>0
    res["book daily by coin"]=D.groupby("coin").agg(mean_book=("book_return","mean"),mean_coin=("coin_return","mean"),share_active=("inpos","mean")).mul([100,100,1]).round(4)
    ap=pd.concat([b.assign(coin=c) for c,ws in data["bars"].items() for b in ws.values()])
    a=ap["postRebalance_current_allocation"]
    res["allocation stats"]=pd.Series({"share short":(a<0).mean(),"mean when short":a[a<0].mean()}).round(3)
    return res
