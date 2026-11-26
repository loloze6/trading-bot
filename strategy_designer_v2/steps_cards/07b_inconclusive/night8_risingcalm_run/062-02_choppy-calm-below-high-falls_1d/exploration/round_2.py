def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(b)
            hi5=pd.Series(c).rolling(5,min_periods=5).max().values
            r=pd.Series(c).pct_change()
            sd30=r.rolling(30,min_periods=20).std().values
            raw=(c-hi5)/hi5/sd30
            ts=pd.to_datetime(b["timestamp"])
            for h in (5,10):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=ts.iloc[i].year,day=ts.iloc[i].normalize(),
                        fc=b["forecast"].iloc[i],raw=raw[i],regime=b["regime"].iloc[i],fwd=c[i+h]/c[i]-1))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex_%":g.ex.mean()*100,"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    ip=d[(d.regime=="unknown")&d.raw.notna()].copy()
    ip["below"]=ip.raw<-1e-12
    out["inprof_below_by_year_h5"]=ip[ip.h==5].groupby(["year","below"]).apply(summ)
    def slope(g,x):
        g=g.dropna(subset=[x,"ex"])
        dd=g.groupby("day")[[x,"ex"]].mean()
        s=stats.linregress(dd[x],dd.ex)
        return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n_days":len(dd)})
    res={}
    for h in (5,10):
        g=ip[ip.h==h]
        res[f"h{h}_raw_all_inprof"]=slope(g,"raw")
        res[f"h{h}_raw_below_only"]=slope(g[g.below],"raw")
        res[f"h{h}_fc_all_inprof"]=slope(g,"fc")
        res[f"h{h}_raw_excl2018"]=slope(g[g.year!=2018],"raw")
    out["slopes_dayp"]=pd.DataFrame(res).T
    g10=ip[(ip.h==10)&ip.below].copy()
    g10["q"]=pd.qcut(g10.raw.rank(method="first"),3,labels=["deep","mid","shallow"])
    out["h10_below_terciles"]=g10.groupby("q").apply(summ)
    out["h10_athigh_vs_below"]=ip[ip.h==10].groupby("below").apply(summ)
    return out
