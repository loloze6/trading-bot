def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        rs=[]
        for w,df in wins.items():
            c=df["close"].values
            for i in range(0,len(c)-7,7):
                rs.append(c[i+7]/c[i]-1)
        drift=np.mean(rs)
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"]
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            z=(c/c.shift(7)-1)/(sd*np.sqrt(7))
            tr=(c/c.shift(60)-1)*100
            prof=(df["regime"]=="unknown")
            n=len(df)
            for i in range(0,n-7,7):
                if np.isnan(z.iloc[i]): continue
                t=tr.iloc[i]
                tc="na" if np.isnan(t) else ("rising" if t>10 else ("falling" if t<-10 else "choppy"))
                rows.append(dict(coin=coin,win=w,day=str(df["timestamp"].iloc[i])[:10],z=z.iloc[i],prof=bool(prof.iloc[i]),
                                 tc=tc,ex=c.iloc[i+7]/c.iloc[i]-1-drift))
    d=pd.DataFrame(rows)
    def summ(g, sign=1.0):
        e=g.ex*sign
        dd=e.groupby(g.day).sum()
        D=len(dd)
        m=e.mean()
        se=np.sqrt((dd-dd.mean()*0).pow(2).sum()*0+((g.assign(dev=e-m).groupby("day").dev.sum())**2).sum()*D/(D-1))/len(g) if D>1 else np.nan
        return pd.Series(dict(n=len(g),days=D,mean=m,t=m/se if se else np.nan,
                              spear=stats.spearmanr(g.z.abs(),e)[0] if len(g)>3 else np.nan))
    out={}
    out["rise_by_trend_zb"]=d[d.z>0].assign(zb=pd.cut(d.z,[0,0.75,1.5,99])).groupby(["prof","tc","zb"]).apply(summ)
    out["fall_by_trend_signed"]=d[d.z<0].groupby(["prof","tc"]).apply(lambda g: summ(g,-1.0))
    out["prof_fall_signed"]=summ(d[(d.prof)&(d.z<0)],-1.0)
    out["prof_rise"]=summ(d[(d.prof)&(d.z>0)])
    out["all_rise"]=summ(d[d.z>0])
    out["all_rise_z_gt1"]=summ(d[d.z>1])
    return out
