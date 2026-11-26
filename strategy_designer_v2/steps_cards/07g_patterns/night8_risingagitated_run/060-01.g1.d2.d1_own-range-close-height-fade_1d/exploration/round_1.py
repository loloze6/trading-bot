def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<30: continue
            rng=(b.high-b.low)
            loc=(b.close-b.low)/rng.replace(0,np.nan)
            width=rng/rng.rolling(20).mean()
            r1=b.close.shift(-1)/b.close-1
            r0=b.close/b.close.shift(1)-1
            ret60=b.close/b.close.shift(60)-1
            vol30=r0.rolling(30).std()
            volrel=vol30/vol30.expanding(30).median()
            inprof=b.regime.isin(["mean_reversion","unknown"])
            wd=pd.to_datetime(b.timestamp).dt.weekday
            df=pd.DataFrame(dict(coin=coin,w=w,loc=loc,width=width,r1=r1,r0=r0,ret60=ret60,
                volrel=volrel,inprof=inprof,wd=wd,regime=b.regime,alloc=b.postRebalance_current_allocation))
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1","loc"])
    drift=d.groupby("coin").r1.mean()
    d["ex"]=d.r1-d.coin.map(drift)
    d["locq"]=pd.cut(d["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True,labels=["q1low","q2","q3","q4","q5high"])
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex.mean(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out={}
    out["regime_counts"]=d.regime.value_counts()
    out["loc_by_inprof"]=d.groupby(["inprof","locq"]).apply(summ)
    d["trend"]=np.where(d.ret60>0.10,"rising",np.where(d.ret60<-0.10,"falling","choppy"))
    d.loc[d.ret60.isna(),"trend"]="na"
    d["agit"]=np.where(d.volrel>1,"agit","calm"); d.loc[d.volrel.isna(),"agit"]="na"
    dd=d[(d.trend!="na")&(d.agit!="na")]
    out["loc_by_trend_agit_q1q5"]=dd[dd.locq.isin(["q1low","q5high"])].groupby(["trend","agit","locq"]).apply(summ)
    d["wideq"]=pd.qcut(d.width,4,labels=["n1","n2","n3","w4"])
    out["wide_loc_outprof"]=d[~d.inprof & d.locq.isin(["q1low","q5high"])].groupby(["wideq","locq"]).apply(summ)
    d["r0q"]=pd.qcut(d.r0,5,labels=["dn5","d4","m","u2","up1"])
    out["after_r0_by_prof"]=d.groupby(["inprof","r0q"]).apply(summ)
    out["weekday_all"]=d.groupby("wd").apply(summ)
    out["by_window_inprof_q5"]=d[d.inprof&(d.locq=="q5high")].groupby("w").apply(summ)
    return out
