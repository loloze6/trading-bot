def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    # book daily decomposition
    D=[]
    for coin in data["days"]:
        for w,d in data["days"][coin].items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book_daily"]=pd.Series({"book_mean":D.book_return.mean(),"coin_mean":D.coin_return.mean(),
        "n_days":D.book_return.notna().sum()})
    # slow vs fast proximity momentum at 336 grid, trending only
    recs=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]
            sma=c.rolling(200).mean()
            for L in [20,120,336]:
                ret=c/c.shift(L)-1
                hi=c.rolling(L).max()
                dist=(hi/c-1)*100
                sig=ret*(1/(1+dist))**2
                idx=np.arange(0,len(c)-336,336)
                for i in idx:
                    if c[i]>sma[i] and not np.isnan(sig[i]):
                        recs.append((coin,L,sig[i],c[i+336]/c[i]-1,b["forecast"].iloc[i]))
    R=pd.DataFrame(recs,columns=["coin","L","sig","fr","f"])
    R["ex"]=R.fr-R.groupby("coin").fr.transform("mean")
    res={}
    for L,g in R.groupby("L"):
        g=g.copy(); g["s"]=g.sig.clip(lower=0)
        sl=stats.linregress(g.s,g.ex)
        g["q"]=pd.qcut(g.s.rank(method="first"),3,labels=["lo","mid","hi"])
        m=g.groupby("q").ex.mean()
        res[L]=dict(n=len(g),slope_t=sl.slope/sl.stderr,lo=m["lo"],mid=m["mid"],hi=m["hi"])
    out["slow_vs_fast_336"]=pd.DataFrame(res).T
    # forecast flips: how often the hourly forecast changes sign per day
    fl=[];ch=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            f=b["forecast"].fillna(0).values
            fl.append(((f[1:]>0)!=(f[:-1]>0)).sum()); ch.append(len(f))
    out["onoff_switches_per_day"]=sum(fl)/sum(ch)*24
    return out
