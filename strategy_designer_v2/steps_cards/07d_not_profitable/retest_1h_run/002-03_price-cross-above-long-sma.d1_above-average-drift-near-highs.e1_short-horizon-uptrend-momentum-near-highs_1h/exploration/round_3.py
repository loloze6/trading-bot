def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    # book decomposition: market-rise part vs timing
    cm={}
    for coin in data["days"]:
        cm[coin]=pd.concat([d.coin_return for d in data["days"][coin].values()]).mean()
    D=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.copy(); b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            a=b.groupby("day").postRebalance_current_allocation.mean().fillna(0)
            D.append(pd.DataFrame({"a":a.values,"mkt":a.values*cm[coin]}))
    D=pd.concat(D)
    out["decomp"]=pd.Series({"mean_alloc":D.a.mean(),"market_part":D.mkt.mean(),"book_mean":-0.001761,"timing_part":-0.001761-D.mkt.mean()})
    # slower signals: return and high over L bars, unstandardised; slope at 336 grid; persistence of on/off
    recs=[];sw={}
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            c=b["close"].reset_index(drop=True)
            sma=c.rolling(200).mean()
            idx=np.arange(0,len(c)-336,336)
            for L in [20,168,480]:
                ret=c/c.shift(L)-1; hi=c.rolling(L).max(); dist=(hi/c-1)*100
                sig=(ret*(1/(1+dist))**2).clip(lower=0)
                on=((sig>0)&(c>sma)).astype(int).values
                s=sw.setdefault(L,[0,0]); s[0]+=np.abs(np.diff(on)).sum(); s[1]+=len(on)
                for i in idx:
                    if c[i]>sma[i] and not np.isnan(sig[i]):
                        recs.append((coin,L,sig[i],c[i+336]/c[i]-1))
    R=pd.DataFrame(recs,columns=["coin","L","s","fr"])
    R["ex"]=R.fr-R.groupby("coin").fr.transform("mean")
    res={}
    for L,g in R.groupby("L"):
        sl=stats.linregress(g.s,g.ex)
        g=g.assign(q=pd.qcut(g.s.rank(method="first"),3,labels=["lo","mid","hi"]))
        m=g.groupby("q").ex.mean()
        res[L]=dict(n=len(g),slope_t=sl.slope/sl.stderr,lo=m["lo"],mid=m["mid"],hi=m["hi"],switches_per_day=sw[L][0]/sw[L][1]*24)
    out["slow_raw_336"]=pd.DataFrame(res).T
    return out
