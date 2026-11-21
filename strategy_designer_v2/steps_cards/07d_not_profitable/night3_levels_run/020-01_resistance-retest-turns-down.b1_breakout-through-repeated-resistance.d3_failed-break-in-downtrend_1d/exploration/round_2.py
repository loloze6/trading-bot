def explore(data):
    import numpy as np, pandas as pd
    H=10
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values; idx=np.arange(0,len(c)-H,H); allr+=list(c[idx+H]/c[idx]-1)
        dr=np.mean(allr); us=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"].values; f=b["forecast"].fillna(0).values
            r60=pd.Series(c).pct_change(60).values
            brk=b.get("debug_info.components.break.last_history_value",pd.Series(np.nan,index=b.index)).values
            seen=set()
            for t in range(1,len(c)-H):
                if f[t]<0 and (f[t-1]-f[t])>=2:
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    fr=c[t+H]/c[t]-1
                    rows.append(dict(coin=coin,r60=r60[t],brk=brk[t],u=-(fr-dr),tot=-fr,s=-(fr-dr)/us,
                                     path5=-(c[t+5]/c[t]-1-dr/2)))
    d=pd.DataFrame(rows).dropna()
    def summ(g):
        return pd.Series(dict(n=len(g),total=g.tot.mean(),unus=g.u.mean(),strength=g.s.mean(),
                              t=g.u.mean()/(g.u.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out={}
    d["up60"]=(d.r60>0).astype(int); d["smallbrk"]=(d.brk<d.brk.median()).astype(int)
    out["r60xbrk"]=d.groupby(["up60","smallbrk"]).apply(summ)
    d["q60"]=pd.qcut(d.r60,3,labels=False)
    out["r60_terciles_in_smallbrk"]=d[d.smallbrk==1].groupby("q60").apply(summ)
    out["corr"]=pd.Series(dict(r60_u=d[["r60","u"]].corr().iloc[0,1],brk_u=d[["brk","u"]].corr().iloc[0,1],
                               brk_r60=d[["brk","r60"]].corr().iloc[0,1]))
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    T["fq"]=pd.qcut(T.entry_forecast.abs(),4,labels=False,duplicates="drop")
    out["trades_by_fc"]=T.groupby("fq").agg(n=("side","size"),gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),dur=("duration_minutes",lambda x:x.mean()/1440),fc=("entry_forecast","mean"))
    out["trade_gross_quantiles"]=T.profit_loss_percent.quantile([.05,.25,.5,.75,.95])
    return out
