def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]; drift={}; usual={}; allbars=[]
    for coin,wd in data["bars"].items():
        rets=[]
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(c)
            for i in range(0,n-H,H):
                rets.append(c[i+H]/c[i]-1)
            # recompute depth
            hi=b["high"].rolling(20,min_periods=20).max()
            r1=b["close"].pct_change()
            sd=r1.rolling(20,min_periods=20).std()
            depth=(hi-b["close"])/hi/sd
            ret60=b["close"]/b["close"].shift(60)-1
            vol30=r1.rolling(30).std()
            volpct=vol30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            f=b["forecast"].values
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n,H):
                cell=range(i,min(i+H,n))
                for j in cell:
                    if f[j]<=-2:
                        if j+H<n:
                            out={}
                            for h in (1,3,5,10,20):
                                out["r%d"%h]=c[j+h]/c[j]-1 if j+h<n else np.nan
                            rows.append(dict(coin=coin,w=w,year=ts[j].year,day=ts[j].normalize(),f=f[j],
                                depth=depth[j],up=r1[j],ret60=ret60[j],volpct=volpct[j],**out))
                        break
            # all-bar grid comparison: up vs down days in choppy, by depth
            for i in range(20,n-H,H):
                allbars.append(dict(coin=coin,up=r1[i]>0,depth=depth[i],r10=c[i+H]/c[i]-1,ret60=ret60[i],
                                    chop=(abs(ret60[i])<=0.10) if not np.isnan(ret60[i]) else np.nan))
        drift[coin]=np.mean(rets); usual[coin]=np.std(rets)
    d=pd.DataFrame(rows)
    for h in (1,3,5,10,20):
        # per-coin drift per h approx scaled
        d["u%d"%h]=-(d["r%d"%h]-d["coin"].map(drift)*h/10)
    def tday(s,days):
        g=s.groupby(days).sum(); dev=(s-s.mean()).groupby(days).sum()
        D=len(g); se=np.sqrt((dev**2).sum()*D/(D-1))/len(s)
        return s.mean()/se
    out={}
    out["n_cases"]=len(d)
    out["horizons"]=pd.DataFrame({h:{"mean":d["u%d"%h].mean(),"t":tday(d["u%d"%h].dropna(),d.loc[d["u%d"%h].notna(),"day"]),
                                    "total_mean":-d["r%d"%h].mean()} for h in (1,3,5,10,20)}).T
    def grp(k):
        return d.groupby(k)["u10"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["by_coin"]=grp("coin"); out["by_window"]=grp("w"); out["by_year"]=grp("year")
    d["fq"]=pd.qcut(-d["f"],4,labels=False,duplicates="drop"); out["by_forecast_q"]=grp("fq")
    d["dq"]=pd.qcut(d["depth"],4,labels=False,duplicates="drop"); out["by_rawdepth_q"]=grp("dq")
    d["agit"]=np.where(d["volpct"]>0.5,"agit","calm"); out["by_agitation"]=grp("agit")
    d["trend_sign"]=np.where(d["ret60"]>0,"pos60","neg60"); out["by_ret60sign"]=grp("trend_sign")
    out["drift10"]=pd.Series(drift); out["usual10"]=pd.Series(usual)
    a=pd.DataFrame(allbars).dropna()
    a=a[a["chop"]==True]
    a["dq"]=a.groupby("up")["depth"].transform(lambda x:pd.qcut(x,4,labels=False,duplicates="drop"))
    a["u"]=-(a["r10"]-a["coin"].map(drift))
    out["allchop_grid_up_by_depth"]=a.groupby(["up","dq"])["u"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    return out
