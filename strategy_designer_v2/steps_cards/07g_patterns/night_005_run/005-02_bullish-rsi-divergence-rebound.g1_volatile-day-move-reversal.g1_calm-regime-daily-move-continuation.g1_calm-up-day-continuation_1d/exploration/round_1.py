def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            sc=r1/r1.abs().rolling(20,min_periods=10).mean().shift(1)
            vol=r1.rolling(10,min_periods=8).std()
            vr=vol.rolling(40,min_periods=20).rank(pct=True)
            r5p=c/c.shift(5)-1
            r20p=c/c.shift(20)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            raw=b.get("debug_info.components.calm_up.last_history_value")
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),r1=r1,sc=sc,vr=vr,r5p=r5p,r20p=r20p,f5=f5,f1=f1,
                raw=raw,fc=b["forecast"],alloc=b["postRebalance_current_allocation"],wd=ts.dt.weekday,yr=ts.dt.year))
            rows.append(d)
    D=pd.concat(rows)
    G=D[(D.pos%5==0)].dropna(subset=["f5"])
    out={}
    def tab(g,col,q=5):
        x=g.dropna(subset=[col])
        x=x.assign(b=pd.qcut(x[col],q,labels=False,duplicates="drop"))
        t=x.groupby("b")["f5"].agg(["count","mean","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["lo"]=x.groupby("b")[col].min();t["hi"]=x.groupby("b")[col].max()
        return t
    out["f5 by scaled 1d move"]=tab(G,"sc")
    out["f5 by raw comp"]=tab(G,"raw")
    out["f5 by prior 5d ret"]=tab(G,"r5p")
    out["f5 by prior 20d ret"]=tab(G,"r20p")
    out["f5 by vol rank"]=tab(G,"vr")
    # interaction: sign of move x vol rank half
    x=G.dropna(subset=["sc","vr"]).copy()
    x["up"]=x.sc>0; x["calm"]=x.vr<0.5
    out["f5 by up x calm"]=x.groupby(["up","calm"])["f5"].agg(["count","mean"])
    # slope f5 on sc within calm vs volatile
    res={}
    for k,g in x.groupby("calm"):
        s=stats.linregress(g.sc,g.f5); res[f"calm={k}"]=(s.slope,s.slope/s.stderr,len(g))
    out["slope f5~sc by calm"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # by coin
    out["f5 by coin x raw>0"]=G.assign(p=G.raw>0).groupby(["coin","p"])["f5"].agg(["count","mean"])
    # weekday daily f1 all bars
    a=D.dropna(subset=["f1"])
    t=a.groupby("wd")["f1"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["f1 by weekday"]=t
    # book decomposition
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd.append(d.assign(coin=coin,w=w))
    Dd=pd.concat(dd).dropna(subset=["book_return"])
    out["book mean, coin mean daily, sd"]=pd.Series(dict(book=Dd.book_return.mean(),coin=Dd.coin_return.mean(),bsd=Dd.book_return.std(),csd=Dd.coin_return.std()))
    ga=D.dropna(subset=["f1","alloc"])
    mu=ga.groupby("coin")["f1"].mean()
    ga["mkt"]=ga.alloc*ga.coin.map(mu);ga["gain"]=ga.alloc*ga.f1
    out["gain decomposition per bar"]=pd.Series(dict(gain=ga.gain.mean(),market=ga.mkt.mean(),timing=ga.gain.mean()-ga.mkt.mean(),mean_alloc=ga.alloc.mean(),share_in=(ga.alloc.abs()>0.01).mean()))
    out["book by year"]=Dd.assign(yr=pd.to_datetime(Dd.day).dt.year).groupby("yr")[["book_return","coin_return"]].mean()
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=tr.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()),dur_days=("duration_minutes",lambda s:s.mean()/1440))
    return out
