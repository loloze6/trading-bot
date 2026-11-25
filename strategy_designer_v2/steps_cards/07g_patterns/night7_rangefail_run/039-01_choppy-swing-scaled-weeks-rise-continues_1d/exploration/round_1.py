def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].values
            n=len(c)
            for i in range(0,n-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(allr) if allr else 0.0
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r=c.pct_change()
            ret20=c/c.shift(20)-1
            sd20=r.rolling(20).std()
            z20=np.log(c/c.shift(20))/(sd20*np.sqrt(20))
            ret5=c/c.shift(5)-1
            z5=np.log(c/c.shift(5))/(sd20*np.sqrt(5))
            r1z=r/sd20.shift(1)
            ts=pd.to_datetime(b["timestamp"])
            vol_rank=sd20.rank(pct=True)
            fwd=c.shift(-H)/c-1
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,win=w,z20=z20[i],z5=z5[i],r1z=r1z[i],ret20=ret20[i],
                    sd20=sd20[i],vr=vol_rank[i],fwd=fwd[i],ex=fwd[i]-drift[coin],
                    reg=b["regime"].iloc[i],fc=b["forecast"].iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],
                    wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year,
                    rng=(b["high"].iloc[i]-b["low"].iloc[i])/c[i]/sd20[i] if sd20[i]>0 else np.nan,
                    clpos=(c[i]-b["low"].iloc[i])/(b["high"].iloc[i]-b["low"].iloc[i]) if b["high"].iloc[i]>b["low"].iloc[i] else np.nan))
    df=pd.DataFrame(rows).dropna(subset=["z20","ex"])
    def grp(d,col,q=5):
        d=d.copy(); d["bin"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        g=d.groupby("bin")
        o=g.agg(n=("ex","size"),mean_x=(col,"mean"),ex=("ex","mean"),sd=("ex","std"))
        o["t"]=o["ex"]/(o["sd"]/np.sqrt(o["n"])); return o.drop(columns="sd").round(4)
    def slope(d,col):
        d=d.dropna(subset=[col,"ex"])
        if len(d)<20: return np.nan
        s=stats.linregress(d[col],d["ex"]); return f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(d)}"
    ch=df[df.reg=="unknown"]; nc=df[df.reg!="unknown"]
    out={}
    out["z20 quint choppy"]=grp(ch,"z20")
    out["z20 quint non-choppy"]=grp(nc,"z20")
    out["slopes"]=pd.Series({"z20 choppy":slope(ch,"z20"),"z20 nonchoppy":slope(nc,"z20"),
        "z5 choppy":slope(ch,"z5"),"z5 all":slope(df,"z5"),"r1z all":slope(df,"r1z"),
        "z20 all":slope(df,"z20"),"rng all":slope(df,"rng"),"clpos all":slope(df,"clpos"),
        "vr all":slope(df,"vr")})
    out["z5 quint all"]=grp(df,"z5")
    out["r1z quint all"]=grp(df,"r1z")
    out["clpos quint all"]=grp(df,"clpos")
    out["vol rank quint all"]=grp(df,"vr")
    out["rng quint all"]=grp(df,"rng")
    w=df.groupby("wd")["ex"].agg(["size","mean","std"]); w["t"]=w["mean"]/(w["std"]/np.sqrt(w["size"]))
    out["weekday"]=w.round(4)
    y=df.groupby("yr")["ex"].agg(["size","mean"]); out["year"]=y.round(4)
    # choppy, by side
    ch2=ch.copy(); ch2["side"]=np.sign(ch2.z20)
    out["choppy dir ex by side"]=ch2.assign(dx=ch2.ex*ch2.side).groupby("side")["dx"].agg(["size","mean","std"]).round(4)
    # book daily: largest days
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd.append(d.assign(coin=coin)[["book_return","coin_return","coin"]])
    D=pd.concat(dd).dropna()
    out["book vs coin corr"]=float(D.book_return.corr(D.coin_return))
    q=D.book_return.quantile([0.01,0.99])
    out["book tail days coin_ret"]=pd.Series({"worst1% n":int((D.book_return<=q.iloc[0]).sum()),
        "worst1% mean coin ret":D.coin_return[D.book_return<=q.iloc[0]].mean(),
        "best1% mean coin ret":D.coin_return[D.book_return>=q.iloc[1]].mean(),
        "worst1% share coin up":(D.coin_return[D.book_return<=q.iloc[0]]>0).mean()}).round(4)
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t)
    T=pd.concat(T)
    T["absf"]=T.entry_forecast.abs()
    T["fb"]=pd.qcut(T.absf,4,labels=False,duplicates="drop")
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["size","mean","median"]).round(3)
    out["trades by |forecast| q"]=T.groupby("fb")["net_profit_loss_percent"].agg(["size","mean"]).round(3)
    return out
