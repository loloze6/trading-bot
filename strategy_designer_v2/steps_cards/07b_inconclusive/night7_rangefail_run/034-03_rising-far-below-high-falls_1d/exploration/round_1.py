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
            rising=(df["regime"]!="chop")
            n=len(df)
            for h in [1,3,5,10,20]:
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,n,h)
                for i in idx:
                    if pd.isna(fwd.iloc[i]) or pd.isna(dist.iloc[i]): continue
                    rows.append(dict(coin=coin,w=w,h=h,i=i,fwd=fwd.iloc[i],dist=dist.iloc[i],
                                     rising=bool(rising.iloc[i]),fc=df["forecast"].iloc[i],
                                     sd30=sd30.iloc[i],yr=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    out={}
    res=[]
    for h in [1,3,5,10,20]:
        s=d[(d.h==h)&d.rising]
        below=s[s.dist<0]
        sl=stats.linregress(below.dist,below.ex)
        for lab,g in [("all_rising",s),("below",below),("at_or_above",s[s.dist>=0])]:
            res.append(dict(h=h,grp=lab,n=len(g),mean_ex=g.ex.mean(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))))
        res.append(dict(h=h,grp="slope_ex_on_dist_below",n=len(below),mean_ex=sl.slope,t=sl.slope/sl.stderr))
        sl2=stats.linregress(s.dist,s.ex)
        res.append(dict(h=h,grp="slope_ex_on_dist_all",n=len(s),mean_ex=sl2.slope,t=sl2.slope/sl2.stderr))
    out["by_h"]=pd.DataFrame(res)
    s5=d[(d.h==5)]
    s5=s5.assign(b=pd.cut(s5.dist,[-99,-4,-2.5,-1.5,-0.75,0,0.5,99]))
    out["bins5_rising"]=s5[s5.rising].groupby("b").ex.agg(["count","mean","std"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    out["bins5_notrising"]=s5[~s5.rising].groupby("b").ex.agg(["count","mean","std"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    b=s5[s5.rising&(s5.dist<0)]
    def slp(g):
        if len(g)<15: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan,mean_ex=g.ex.mean()))
        l=stats.linregress(g.dist,g.ex); return pd.Series(dict(n=len(g),slope=l.slope,t=l.slope/l.stderr,mean_ex=g.ex.mean()))
    out["coin5"]=b.groupby("coin").apply(slp)
    out["win5"]=b.groupby("w").apply(slp)
    out["year5"]=b.groupby("yr").apply(slp)
    return out
