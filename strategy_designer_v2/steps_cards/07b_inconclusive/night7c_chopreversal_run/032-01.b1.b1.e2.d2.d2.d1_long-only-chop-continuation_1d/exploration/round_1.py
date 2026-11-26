def explore(data):
    import numpy as np, pandas as pd
    H=7
    rows=[]; allgrid={}
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values; n=len(c)
            for i in range(0,n-H,H):
                g.append(c[i+H]/c[i]-1)
        allgrid[coin]=np.mean(g)
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            er=(c-c.shift(30)).abs()/c.diff().abs().rolling(30).sum()
            vol30=r.rolling(30).std()
            sr=(c/c.shift(7)-1)/(vol30*np.sqrt(7))
            r30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b)
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    f=b["forecast"].iloc[i]
                    if not (f>0): continue
                    rows.append(dict(coin=coin,w=w,h=h,year=yr.iloc[i],f=f,er=er.iloc[i],
                        vol=vol30.iloc[i],sr=sr.iloc[i],r30=r30.iloc[i],
                        ret=c.iloc[i+h]/c.iloc[i]-1,
                        day=str(b["timestamp"].iloc[i])[:10]))
    d=pd.DataFrame(rows)
    def st(x):
        x=x.dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    for h in (3,7,14):
        dh=d[d.h==h].copy()
        dh["u"]=dh.ret-dh.coin.map(allgrid)*h/7
        out[f"h{h}_all"]=st(dh.u)
    d7=d[d.h==7].copy(); d7["u"]=d7.ret-d7.coin.map(allgrid)
    out["by_coin"]=d7.groupby("coin").u.apply(st).unstack()
    out["by_window"]=d7.groupby("w").u.apply(st).unstack()
    out["by_year"]=d7.groupby("year").u.apply(st).unstack()
    for col in ["f","er","vol","sr","r30"]:
        q=pd.qcut(d7[col],3,labels=False,duplicates="drop")
        out[f"tercile_{col}"]=d7.groupby(q).u.apply(st).unstack()
    out["coin_mean7"]=pd.Series(allgrid)
    return out
