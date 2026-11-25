def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            hi=c.shift(1).rolling(20).max()
            sd=r.rolling(20).std()
            dist=(c/hi-1)/sd
            ret60=c/c.shift(60)-1
            sd30=r.rolling(30).std()
            agit=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            rising=(df["regime"]!="chop")
            n=len(df)
            ts=pd.to_datetime(df["timestamp"])
            for h in [5,10]:
                fwd=c.shift(-h)/c-1
                for i in range(0,n,h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(dist.iloc[i]): continue
                    r60=ret60.iloc[i]
                    if rising.iloc[i]: tr="rising"
                    elif pd.isna(r60): tr="notrising_unk"
                    elif r60< -0.10: tr="falling"
                    else: tr="choppy"
                    a=agit.iloc[i]
                    ag="na" if pd.isna(a) else ("agitated" if a>0.5 else "calm")
                    rows.append(dict(coin=coin,w=w,h=h,fwd=fwd.iloc[i],dist=dist.iloc[i],tr=tr,ag=ag,
                                     day=ts.iloc[i].normalize(),yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    def summ(g):
        b=g[g.dist<0]
        out=dict(n=len(b))
        if len(b)<15: return pd.Series(out)
        l=stats.linregress(b.dist,b.ex)
        out.update(slope=l.slope,t_slope=l.slope/l.stderr,mean_ex=b.ex.mean())
        dd=b.groupby("day").ex.sum()
        out["t_day"]=b.ex.mean()*len(b)/ (np.sqrt(((dd - b.groupby('day').ex.count()*b.ex.mean())**2).sum())) if len(dd)>1 else np.nan
        out["days"]=len(dd)
        deep=b[b.dist<=-2.5]
        out["deep_n"]=len(deep); out["deep_mean"]=deep.ex.mean()
        out["deep_t"]=deep.ex.mean()/(deep.ex.std()/np.sqrt(len(deep))) if len(deep)>2 else np.nan
        return pd.Series(out)
    res={}
    res["by_trend"]=d.groupby(["h","tr"]).apply(summ)
    res["by_trend_ag"]=d[d.h==5].groupby(["tr","ag"]).apply(summ)
    f=d[(d.h==5)&(d.tr=="falling")]
    res["falling_by_year"]=f.groupby("yr").apply(summ)
    res["falling_by_coin"]=f.groupby("coin").apply(summ)
    s5=d[(d.h==5)&(d.tr=="falling")]
    s5=s5.assign(b=pd.cut(s5.dist,[-99,-4,-2.5,-1.5,-0.75,0,99]))
    res["falling_bins"]=s5.groupby("b").ex.agg(["count","mean","std"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    s5=d[(d.h==5)&(d.tr=="choppy")]
    s5=s5.assign(b=pd.cut(s5.dist,[-99,-4,-2.5,-1.5,-0.75,0,99]))
    res["choppy_bins"]=s5.groupby("b").ex.agg(["count","mean","std"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    return res
