def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]; drift={}; usual={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(allr); usual[coin]=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            n=len(c)
            r20=pd.Series(c).pct_change(20).values
            r60=pd.Series(c).pct_change(60).values
            hi90=pd.Series(c).rolling(90,min_periods=30).max().values
            ma50=pd.Series(c).rolling(50,min_periods=30).mean().values
            seen=set()
            for t in range(1,n-H):
                if f[t]<0 and (f[t-1]-f[t])>=2:
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    fr=c[t+H]/c[t]-1
                    rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                        fc=abs(f[t]),r20=r20[t],r60=r60[t],dhi=c[t]/hi90[t]-1 if hi90[t]==hi90[t] else np.nan,
                        ma=c[t]/ma50[t]-1,
                        brk=b.get("debug_info.components.break.last_history_value",pd.Series(np.nan,index=b.index)).iloc[t],
                        short_total=-fr, short_unus=-(fr-drift[coin])))
    d=pd.DataFrame(rows)
    out={}
    def summ(g):
        return pd.Series(dict(n=len(g),total=g.short_total.mean(),unus=g.short_unus.mean(),
            t=g.short_unus.mean()/(g.short_unus.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["all"]=summ(d)
    for col in ["fc","r20","r60","dhi","ma","brk"]:
        dd=d.dropna(subset=[col])
        dd=dd.assign(q=pd.qcut(dd[col],5,labels=False,duplicates="drop"))
        out["by_"+col]=dd.groupby("q").apply(lambda g: pd.concat([summ(g),pd.Series({"mid":g[col].median()})]))
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    # book daily
    dr=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dr.append(x.assign(coin=coin,w=w,year=pd.to_datetime(x["day"]).dt.year))
    D=pd.concat(dr)
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["book_by_coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=pd.Series(dict(n=len(T),mean_gross=T.profit_loss_percent.mean(),mean_net=T.net_profit_loss_percent.mean(),
        win=(T.profit_loss_percent>0).mean(),dur_days=T.duration_minutes.mean()/1440, short_share=(T.side=="SHORT").mean()))
    return out
