def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values.astype(float)
            n=len(b)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            vs=pd.Series(v)
            top3=vs.rolling(H).apply(lambda x: np.sort(x)[-3:].sum()/x.sum() if x.sum()>0 else np.nan, raw=True).values
            rs=pd.Series(r1)
            absr=rs.abs().rolling(H).sum().values
            past=np.r_[[np.nan]*H, c[H:]/c[:-H]-1]
            eff=np.abs(np.log(1+past))/pd.Series(np.log(1+rs)).abs().rolling(H).sum().values
            vol=rs.rolling(H).std().values
            past24=np.r_[[np.nan]*24, c[24:]/c[:-24]-1]
            ts=pd.to_datetime(b["timestamp"])
            for t in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,past=past[t],past24=past24[t],top3=top3[t],eff=eff[t],vol=vol[t],
                                 fwd=c[t+H]/c[t]-1,wd=ts.iloc[t].dayofweek,hr=ts.iloc[t].hour,
                                 alloc=b["postRebalance_current_allocation"].iloc[t]))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def tq(g,col,q=5):
        g=g.dropna(subset=[col,"ex"]).copy()
        g["q"]=g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        s=g.groupby("q")["ex"].agg(["mean","count","std"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"])); return s
    out["ex by past72 quintile"]=tq(d,"past")
    out["ex by top3 quintile, all"]=tq(d,"top3")
    out["ex by top3 quintile, risen"]=tq(d[d.past>0],"top3")
    out["ex by top3 quintile, fallen"]=tq(d[d.past<0],"top3")
    out["ex by eff quintile, risen"]=tq(d[d.past>0],"eff")
    out["ex by eff quintile, fallen"]=tq(d[d.past<0],"eff")
    out["ex by vol quintile"]=tq(d,"vol")
    out["ex by past24 quintile"]=tq(d,"past24")
    # signed: continuation by efficiency: ex*sign(past)
    d["sx"]=d["ex"]*np.sign(d["past"])
    g=d.dropna(subset=["eff","sx"]).copy(); g["q"]=g.groupby("coin")["eff"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    s=g.groupby("q")["sx"].agg(["mean","count","std"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"])); out["signed cont by eff q"]=s
    # per coin past72 slope
    pc=[]
    for coin,g in d.dropna(subset=["past","ex"]).groupby("coin"):
        sl=stats.linregress(g["past"],g["ex"]); pc.append(dict(coin=coin,slope=sl.slope,t=sl.slope/sl.stderr,n=len(g)))
    out["per coin past72->ex slope"]=pd.DataFrame(pc)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    bars=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); r=b["close"].shift(-1)/b["close"]-1
            bars.append(pd.DataFrame(dict(coin=coin,a=b["postRebalance_current_allocation"],r=r,reg=b["regime"])))
    B=pd.concat(bars)
    B["g"]=B["a"]*B["r"]
    mr=B.groupby("coin")["r"].mean()
    B["mkt"]=B["a"]*B["coin"].map(mr)
    out["bar gain: total, market part, per coin"]=B.groupby("coin")[["g","mkt","a"]].mean()
    out["book daily by coin"]=D.groupby("coin")["book_return"].agg(["mean","std","count"])
    out["book daily mean by window"]=D.groupby("w")["book_return"].mean()
    return out
