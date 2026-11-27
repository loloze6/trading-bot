def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];o=b["open"];h=b["high"];l=b["low"];v=b["volume"]
            r1=c.pct_change()
            up=(r1>0).astype(int)
            streak=up.groupby((up!=up.shift()).cumsum()).cumsum()*up
            prevstreak=streak.shift(1).fillna(0)
            f=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "inprof":(b["regime"]!="chop").values,
                "regime":b["regime"].values,
                "r1":r1,"r3p":c/c.shift(3)-1,"r7p":c/c.shift(7)-1,"r20p":c/c.shift(20)-1,
                "upstreak":streak,"dipafter":np.where(r1<0,prevstreak,np.nan),
                "clpos":(c-l)/(h-l).replace(0,np.nan),
                "rng":((h-l)/c)/((h-l)/c).rolling(20).mean(),
                "vol":v/v.rolling(20).mean(),
                "dhi":c/h.rolling(20).max()-1,
                "z1":r1/r1.rolling(30).std(),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday})
            for H in (1,3,7):
                f[f"fw{H}"]=c.shift(-H)/c-1
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    out={}
    out["prof share by coin"]=d.groupby("coin")["inprof"].mean()
    res=[]
    for H in (1,3,7):
        drift=d.groupby("coin")[f"fw{H}"].apply(lambda s: s[d.loc[s.index,"pos"]%H==0].mean())
        g=d[(d.pos%H==0)&d.inprof].copy()
        g["ex"]=-(g[f"fw{H}"]-g.coin.map(drift))   # short-direction unusual move
        g=g.dropna(subset=["ex"])
        res.append(("all",H,len(g),g.ex.mean(),stats.ttest_1samp(g.ex,0).statistic))
        for feat in ["r1","r3p","r7p","r20p","upstreak","dipafter","clpos","rng","vol","dhi","z1"]:
            x=g.dropna(subset=[feat])
            if len(x)<20: continue
            rho,p=stats.spearmanr(x[feat],x.ex)
            n=len(x); t=rho*np.sqrt((n-2)/(1-rho**2))
            q=pd.qcut(x[feat].rank(method="first"),3,labels=False)
            lo=x.ex[q==0].mean(); hi=x.ex[q==2].mean()
            res.append((feat,H,n,rho,t,lo,hi))
    out["feature vs short unusual move"]=pd.DataFrame([r+(np.nan,)*(7-len(r)) for r in res],
        columns=["feat","H","n","rho_or_mean","t","low_third","high_third"]).round(4)
    # weekday in profile, 1-day
    drift1=d.groupby("coin")["fw1"].mean()
    g=d[d.inprof].dropna(subset=["fw1"]).copy(); g["ex"]=-(g.fw1-g.coin.map(drift1))
    out["weekday 1d short ex"]=g.groupby("wd")["ex"].agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    out["trades"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median",lambda s:(s>0).mean()]).round(3)
    return out
