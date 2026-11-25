def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        # drift: mean non-overlapping 7d return over all windows
        f7all=[]
        for w,b in ws.items():
            c=b["close"].reset_index(drop=True)
            idx=np.arange(0,len(c)-7,7)
            f7all+=list(c.values[idx+7]/c.values[idx]-1)
        drift=np.mean(f7all)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(30).std()
            r7=c/c.shift(7)-1
            vsr=r7/(vol*np.sqrt(7))
            er=(c-c.shift(14)).abs()/r.abs().mul(c.shift(1)).rolling(14).sum().replace(0,np.nan)
            er=(c/c.shift(14)-1).abs()/r.abs().rolling(14).sum()
            volrank=vol/vol.rolling(180,min_periods=60).median()
            fwd=c.shift(-7)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(c)-7,7):
                rows.append(dict(coin=coin,w=w,day=ts[i].normalize(),vsr=vsr[i],er=er[i],vr=volrank[i],
                                 un=fwd[i]-drift,fwd=fwd[i],wd=ts[i].dayofweek,yr=ts[i].year))
            nr=r.shift(-1)
            for i in range(len(c)-1):
                drows.append(dict(coin=coin,r=r[i]/vol[i] if vol[i]>0 else np.nan,nr=nr[i],wd=ts[i].dayofweek,yr=ts[i].year,vsr=vsr[i]))
    d=pd.DataFrame(rows).dropna(subset=["vsr","un"])
    def summ(g):
        n=len(g); m=g.un.mean(); s=g.un.std()
        return pd.Series(dict(n=n,mean_un=m,t=m/(s/np.sqrt(n)) if n>1 else np.nan))
    out={}
    d["vbin"]=pd.cut(d.vsr,[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf])
    out["fwd7 unusual by vsr bin"]=d.groupby("vbin").apply(summ)
    d2=d.dropna(subset=["er"])
    d2["erT"]=pd.qcut(d2.er,3,labels=["chop","mid","trend"])
    out["corr vsr vs fwd by ER tercile"]=d2.groupby("erT").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.vsr,g.un)[0],p=stats.spearmanr(g.vsr,g.un)[1])))
    d3=d.dropna(subset=["vr"])
    d3["vT"]=pd.qcut(d3.vr,3,labels=["calm","mid","agitated"])
    out["corr vsr vs fwd by vol tercile"]=d3.groupby("vT").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.vsr,g.un)[0],p=stats.spearmanr(g.vsr,g.un)[1])))
    out["fwd7 unusual by vol tercile"]=d3.groupby("vT").apply(summ)
    out["corr vsr fwd by coin"]=d.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.vsr,g.un)[0])))
    out["corr vsr fwd by year"]=d.groupby("yr").apply(lambda g: pd.Series(dict(n=len(g),rho=stats.spearmanr(g.vsr,g.un)[0])))
    dd=pd.DataFrame(drows).dropna()
    dd["rbin"]=pd.cut(dd.r,[-np.inf,-3,-2,-1,0,1,2,3,np.inf])
    out["next day ret by scaled day move"]=dd.groupby("rbin").nr.agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["next day ret by weekday"]=dd.groupby("wd").nr.agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # book
    br=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            br.append(t[["book_return","coin_return"]].assign(coin=coin))
    br=pd.concat(br).dropna()
    nz=br[br.book_return.abs()>1e-9]
    out["book days nonzero"]=pd.Series(dict(n=len(nz),mean=nz.book_return.mean(),corr_coin=nz.book_return.corr(nz.coin_return)))
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    if len(tr):
        out["trades by coin"]=tr.groupby("coin").net_profit_loss_percent.agg(["count","mean","sum"])
    return out
