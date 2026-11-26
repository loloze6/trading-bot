def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,3,5,10]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs,ddof=1))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            n=len(b)
            prior=pd.Series(lo).shift(1).rolling(30,min_periods=30).min().values
            r60=pd.Series(c).pct_change(60).values
            reclaim=(lo<prior)&(c>prior)
            active=(b["forecast"].values>0)
            loc=np.where(hi>lo,(hi-c)/np.where(hi>lo,hi-lo,1),np.nan)
            year=pd.to_datetime(b["timestamp"]).dt.year.values
            for t in range(n):
                if not (reclaim[t] or active[t]): continue
                rec=dict(coin=coin,w=w,t=t,cell=t//5,reclaim=bool(reclaim[t]),active=bool(active[t]),
                         loc=loc[t],r60=r60[t],year=year[t],fc=b["forecast"].values[t],
                         day=str(b["timestamp"].iloc[t])[:10])
                for h in H:
                    rec[f"r{h}"]=c[t+h]/c[t]-1 if t+h<n else np.nan
                    rec[f"u{h}"]=rec[f"r{h}"]-drift[(coin,h)][0] if t+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    out={}
    def summ(g,h=5):
        x=g[f"u{h}"].dropna()
        if len(x)<2: return pd.Series(dict(n=len(x)))
        dd=g.dropna(subset=[f"u{h}"]).groupby("day")[f"u{h}"].sum()
        return pd.Series(dict(n=len(x),mean=x.mean(),days=len(dd),t_day=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>1 else np.nan,win=(x>0).mean()))
    act=d[d.active].sort_values(["coin","w","t"]).groupby(["coin","w","cell"]).head(1)
    out["active cases by horizon"]=pd.DataFrame({h:summ(act,h) for h in H}).T
    out["active by coin h5"]=act.groupby("coin").apply(summ)
    out["active by window h5"]=act.groupby("w").apply(summ)
    act=act.copy(); act["locq"]=pd.qcut(act["loc"],3,labels=["closeHigh","mid","closeLow"])
    out["active by close loc h5"]=act.groupby("locq").apply(summ)
    rc=d[d.reclaim].sort_values(["coin","w","t"]).groupby(["coin","w","cell"]).head(1).copy()
    rc["trend"]=pd.cut(rc["r60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["all reclaims by horizon"]=pd.DataFrame({h:summ(rc,h) for h in H}).T
    out["all reclaims by trend h5"]=rc.groupby("trend").apply(summ)
    out["all reclaims by trend h10"]=rc.groupby("trend").apply(lambda g: summ(g,10))
    rc["locq"]=pd.qcut(rc["loc"],3,labels=["closeHigh","mid","closeLow"])
    out["all reclaims by loc h5"]=rc.groupby("locq").apply(summ)
    out["all reclaims by year h5"]=rc.groupby("year").apply(summ)
    out["usual move h5"]=pd.Series({k[0]:v[1] for k,v in drift.items() if k[1]==5})
    return out
