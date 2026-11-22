def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].astype(float).reset_index(drop=True)
            r1 = c.pct_change(); sd = r1.rolling(20).std(); z1 = r1/sd
            r30 = c/c.shift(30)-1; z30 = r30/(sd*np.sqrt(30))
            r20 = c/c.shift(20)-1
            f5 = c.shift(-5)/c-1
            rows.append(pd.DataFrame({"coin":coin,"w":w,"z1":z1,"r30":r30,"z30":z30,"r20":r20,"f5":f5,
                "reg":b["regime"].values,"fc":b["forecast"].values,
                "alloc":b["postRebalance_current_allocation"].values,"pos":np.arange(len(c))}))
    d = pd.concat(rows, ignore_index=True)
    out = {}
    out["regime counts"] = d.reg.value_counts()
    out["z1>=2 bars all, by regime"] = d[d.z1>=2].reg.value_counts()
    grid = d[(d.pos%5==0)&d.f5.notna()].copy()
    drift = grid.groupby("coin").f5.mean()
    grid["u5"] = grid.f5-grid.coin.map(drift)
    res=[]
    for th in [1.0,1.5,2.0]:
        for nm,m in [("r30<0",grid.r30<0),("r30>0",grid.r30>0),("r20<0",grid.r20<0),("r20>0",grid.r20>0)]:
            g=grid[(grid.z1>=th)&m]; n=len(g)
            res.append({"th":th,"reg":nm,"n":n,"u5":g.u5.mean(),"t":g.u5.mean()/(g.u5.std()/np.sqrt(n)) if n>2 else np.nan})
    out["rises by 30/20d regime"]=pd.DataFrame(res)
    # rises >=1 with r30<0 graded by z30 depth before rise (z30 includes rise; use z30 of previous bar)
    g=grid[(grid.z1>=1)&(grid.r30<0)].copy()
    if len(g)>15:
        g["q"]=pd.qcut(g.z30,3,labels=False,duplicates="drop")
        out["rise>=1 r30<0 by z30 tercile"]=g.groupby("q").agg(n=("u5","size"),z30=("z30","mean"),u5=("u5","mean"))
        out["slope u5 on z30 (rise>=1,r30<0)"]=pd.Series(stats.linregress(g.z30,g.u5)._asdict())
    # book days
    dd=pd.concat([x.assign(coin=c,w=w) for c in days for w,x in days[c].items()],ignore_index=True)
    bk=dd.groupby(["w","day"]).book_return.mean().dropna()
    out["book daily mean by window"]=bk.groupby(level=0).agg(["mean","count"]).assign(sum=lambda x:x["mean"]*x["count"])
    # trades by coin and window outcome
    tr=pd.concat([t.assign(coin=c,w=w) for c in trades for w,t in trades[c].items() if len(t)],ignore_index=True)
    tr["dur"]=tr.duration_minutes/1440
    out["trade net pct quantiles"]=tr.net_profit_loss_percent.describe()
    out["trades by entry forecast tercile"]=tr.assign(q=pd.qcut(tr.entry_forecast,3,labels=False,duplicates="drop")).groupby("q").agg(n=("net_profit_loss_percent","size"),fc=("entry_forecast","mean"),net=("net_profit_loss_percent","mean"),dur=("dur","mean"))
    out["trades by duration"]=tr.assign(b=pd.cut(tr.dur,[0,5.5,7,100])).groupby("b").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"))
    out["trades per window"]=tr.groupby("w").net_profit_loss_percent.agg(["size","mean"])
    return out
