def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.reset_index(drop=True)
            c=d["close"].astype(float)
            low30=c.shift(1).rolling(30).min()
            depth=c/low30-1
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            ret60=c/c.shift(60)-1
            ret5=c/c.shift(5)-1
            n=len(d)
            for h in (1,3,5,10):
                pass
            fw={h:c.shift(-h)/c-1 for h in (1,3,5,10)}
            for i in range(0,n,3):
                rows.append(dict(coin=coin,win=w,ts=d["timestamp"].iloc[i],depth=depth.iloc[i],
                    r1z=r1.iloc[i]/vol30.iloc[i] if vol30.iloc[i]>0 else np.nan,ret60=ret60.iloc[i],ret5=ret5.iloc[i],
                    vol30=vol30.iloc[i],regime=d["regime"].iloc[i],
                    f1=fw[1].iloc[i],f3=fw[3].iloc[i],f5=fw[5].iloc[i],f10=fw[10].iloc[i],
                    wd=pd.Timestamp(d["timestamp"].iloc[i]).dayofweek))
    g=pd.DataFrame(rows).dropna(subset=["f3"])
    g["day"]=pd.to_datetime(g["ts"]).dt.floor("D")
    drift=g.groupby("coin")["f3"].mean()
    g["u3"]=g["f3"]-g["coin"].map(drift)
    def summ(sub,col="u3"):
        s=sub.dropna(subset=[col])
        if len(s)<5: return pd.Series(dict(n=len(s),days=0,mean=np.nan,t=np.nan))
        dd=s.groupby("day")[col].sum()
        nd=len(dd); m=s[col].mean()
        se=np.sqrt((dd-dd.mean()*0).pow(2).sum())/len(s) if False else None
        # day-pooled t: deviations summed per day
        dev=(s[col]-m).groupby(s["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(s)
        return pd.Series(dict(n=len(s),days=nd,mean=m,t=m/se))
    out={}
    g["brk"]=g["depth"]<0
    g["trend"]=pd.cut(g["ret60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    # vol tercile within coin
    g["volq"]=g.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x,2,labels=["calm","agit"]) if x.notna().sum()>10 else np.nan)
    tab={}
    for (tr,vq,b),s in g.groupby(["trend","volq","brk"],observed=True):
        tab[f"{tr}-{vq}-{'brk' if b else 'no'}"]=summ(s)
    out["u3 by trend/vol/break"]=pd.DataFrame(tab).T
    br=g[g.brk].copy()
    br["dq"]=pd.qcut(br["depth"],4,labels=["deepest","q2","q3","shallow"])
    out["breaks by depth quartile"]=pd.DataFrame({k:summ(s) for k,s in br.groupby("dq",observed=True)}).T
    for h in ("f1","f5","f10"):
        dr=g.groupby("coin")[h].mean(); g["u"+h]=g[h]-g["coin"].map(dr)
    fa=g[(g.trend=="fall")&g.brk]
    out["fall+break horizons"]=pd.DataFrame({h:summ(fa,"u"+h) for h in ("f1","f5","f10")}|{"f3":summ(fa)}).T
    g["zq"]=pd.cut(g["r1z"],[-99,-2,-1,1,2,99])
    out["u3 by 1-day move z"]=pd.DataFrame({str(k):summ(s) for k,s in g.groupby("zq",observed=True)}).T
    g["r5q"]=g.groupby("coin")["ret5"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["u3 by 5d return quintile"]=pd.DataFrame({k:summ(s) for k,s in g.groupby("r5q")}).T
    out["u3 by weekday"]=pd.DataFrame({k:summ(s) for k,s in g.groupby("wd")}).T
    out["u3 by window"]=pd.DataFrame({k:summ(s) for k,s in g.groupby("win")}).T
    return out
