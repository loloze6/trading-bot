def explore(data):
    import numpy as np, pandas as pd
    out={}
    # sanity: timestamp spacing
    gaps=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            d=ts.diff().dt.total_seconds().dropna()/3600
            gaps.append(pd.Series(d.values).value_counts())
    g=pd.concat(gaps,axis=1).fillna(0).sum(axis=1).sort_values(ascending=False)
    out["gap_hours_counts"]=g.head(10)
    # placebo: same signed continuation at 23:00 of each weekday, h=12/24/48, plus per-weekday move signs
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in (12,24,48):
            vals=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-h,h); vals.extend(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(vals)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values; v=b["volume"].values
            hr=ts.dt.hour.values; wd=ts.dt.weekday.values
            for i in np.where(hr==23)[0]:
                if i<168 or i+48>=len(c): continue
                r48=c[i]/c[i-48]-1
                d={"coin":coin,"wd":wd[i],"s":np.sign(r48),"vr":v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)}
                for h in (12,24,48):
                    d[f"x{h}"]=np.sign(r48)*(c[i+h]/c[i]-1-drift[(coin,h)])
                # also next-bar-open based to check same-bar alignment
                d["x12_from_next"]=np.sign(r48)*(c[i+13]/c[i+1]-1)
                rows.append(d)
    df=pd.DataFrame(rows)
    def summ(x):
        r={"n":len(x)}
        for k in ("x12","x24","x48","x12_from_next"):
            m=x[k].mean(); r[k+"%"]=m*100; r["t_"+k]=m/(x[k].std()/np.sqrt(len(x)))
        return pd.Series(r)
    out["placebo_by_weekday_of_23h_bar"]=df.groupby("wd").apply(summ)
    sun=df[df.wd==6].copy()
    sun["q_vr"]=pd.qcut(sun["vr"],5,labels=False)
    out["sunday_by_vr_quint"]=sun.groupby("q_vr").apply(summ)
    # book: trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["hrs"]=T["duration_minutes"]/60
    T["fq"]=pd.qcut(T["entry_forecast"].abs().rank(method="first"),4,labels=False)
    out["trades_by_absforecast_q"]=T.groupby("fq").agg(n=("hrs","size"),hrs=("hrs","mean"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),absf=("entry_forecast",lambda s:s.abs().mean()))
    out["trades_by_side"]=T.groupby("side").agg(n=("hrs","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    out["trade_hrs_quantiles"]=T["hrs"].quantile([.1,.5,.9])
    # book falls: daily portfolio (mean over coins) by window, drawdown
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items(): dd.append(d.assign(coin=coin,w=w))
    D=pd.concat(dd); D["day"]=pd.to_datetime(D["day"])
    P=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"]=P["w"].str[1:].astype(int); P=P.sort_values(["wn","day"])
    P["book_return"]=P["book_return"].fillna(0)
    eq=(1+P["book_return"]).cumprod(); dds=eq/eq.cummax()-1
    P["dd"]=dds.values
    out["maxdd"]=float(dds.min())
    P["year"]=P["day"].dt.year
    out["book_by_year"]=P.groupby("year").agg(book_sum=("book_return","sum"),coin_sum=("coin_return","sum"),dd_min=("dd","min"))
    P["wd"]=P["day"].dt.weekday
    mon=P[P.wd==0]
    out["monday_book_days_quantiles"]=mon["book_return"].quantile([.01,.05,.5,.95,.99])
    out["worst10_book_days_share_of_total_loss"]=float(P["book_return"].nsmallest(10).sum())
    out["sum_book"]=float(P["book_return"].sum())
    return out
