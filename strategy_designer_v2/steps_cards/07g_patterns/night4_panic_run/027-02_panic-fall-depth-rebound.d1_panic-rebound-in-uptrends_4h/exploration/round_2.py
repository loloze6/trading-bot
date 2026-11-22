def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=84
    frames=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; ts=pd.to_datetime(b["timestamp"])
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            vol=r.rolling(180).std()
            rng=(b["high"]-b["low"])/c
            ratio=rng.rolling(6).mean()/rng.rolling(180).mean()
            r6=c/c.shift(6)-1
            frames.append(pd.DataFrame(dict(coin=coin,w=w,h=ts.dt.hour,wd=ts.dt.weekday,yr=ts.dt.year,
                nxt=nxt,vol=vol,ratio=ratio,r6=r6,znxt=nxt/vol,alloc=b["postRebalance_current_allocation"])))
    D=pd.concat(frames).dropna(subset=["nxt"])
    def tt(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out={}
    s16=D[D.h==16]
    out["h16 next-bar by coin"]=s16.groupby("coin").nxt.apply(tt).unstack().round(5)
    out["h16 next-bar by year"]=s16.groupby("yr").nxt.apply(tt).unstack().round(5)
    out["h16 minus other bars by coin (welch t)"]=pd.DataFrame({c:dict(diff=D[(D.coin==c)&(D.h==16)].nxt.mean()-D[(D.coin==c)&(D.h!=16)].nxt.mean(),
        t=stats.ttest_ind(D[(D.coin==c)&(D.h==16)].nxt,D[(D.coin==c)&(D.h!=16)].nxt,equal_var=False).statistic) for c in D.coin.unique()}).T.round(5)
    s16v=s16.dropna(subset=["vol"]).copy()
    s16v["vq"]=s16v.groupby("coin").vol.transform(lambda v:pd.qcut(v,3,labels=False))
    out["h16 by own-vol tercile"]=s16v.groupby("vq").agg(n=("nxt","size"),mean=("nxt","mean"),zmean=("znxt","mean")).round(5)
    s16v["pq"]=s16v.groupby("coin").r6.transform(lambda v:pd.qcut(v,3,labels=False))
    out["h16 by prior 24h return tercile"]=s16v.groupby("pq").nxt.apply(tt).unstack().round(5)
    fr=D[D.wd==4]
    out["friday by year"]=fr.groupby("yr").nxt.apply(tt).unstack().round(5)
    out["friday by coin"]=fr.groupby("coin").nxt.apply(tt).unstack().round(5)
    out["weekday x hour mean (x1e4)"]=(D.pivot_table(index="wd",columns="h",values="nxt",aggfunc="mean")*1e4).round(1)
    s20=D[D.h==20]
    out["h20 by year"]=s20.groupby("yr").nxt.apply(tt).unstack().round(5)
    # book exposure by hour
    out["book alloc mean by hour"]=D.groupby("h").alloc.mean().round(4)
    # 14d after high range ratio, continuous, grid
    rows=[]
    for coin,ws in data["bars"].items():
        f=[]
        for w,b in ws.items():
            c=b["close"].values
            f+= [c[i+H]/c[i]-1 for i in range(0,len(c)-H,H)]
        dr=np.mean(f)
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]; rng=(b["high"]-b["low"])/c
            ratio=rng.rolling(6).mean()/rng.rolling(180).mean()
            for s in range(0,len(c)-H,H):
                rows.append(dict(coin=coin,ratio=ratio.iloc[s],un=c.iloc[s+H]/c.iloc[s]-1-dr,yr=pd.to_datetime(b.timestamp.iloc[s]).year))
    G=pd.DataFrame(rows).dropna()
    sl=stats.linregress(np.log(G.ratio),G.un)
    out["grid 14d unusual on log range ratio"]=pd.Series(dict(n=len(G),slope=sl.slope,t=sl.slope/sl.stderr,r=sl.rvalue)).round(4)
    return out
