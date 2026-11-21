def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[24,48,120,240]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        # drift per horizon over all windows, non-overlapping
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rr+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(rr); drift[(coin,h,'sd')]=np.std(rr)
        for w,b in ws.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            r168=pd.Series(c).pct_change(168).values
            n=len(c)
            for s in range(0,n,120):
                e=min(s+120,n)
                lo=np.inf
                for i in range(s,e):
                    lo=min(lo,f[i])
                    if f[i]>=2 and f[i]-lo>=2:
                        d={"coin":coin,"w":w,"year":yr[i],"f":f[i],"r168":r168[i],"hour":i}
                        for h in H:
                            d["x%d"%h]=(c[i+h]/c[i]-1-drift[(coin,h)]) if i+h<n else np.nan
                            d["z%d"%h]=d["x%d"%h]/drift[(coin,h,'sd')] if i+h<n else np.nan
                        rows.append(d); break
    df=pd.DataFrame(rows)
    def summ(g):
        out={}
        for h in H:
            x=g["x%d"%h].dropna()
            out["m%d"%h]=x.mean(); out["t%d"%h]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"]=len(g); return pd.Series(out)
    df["fb"]=pd.cut(df.f,[0,5,10,15,19.99,20.1])
    df["wk"]=pd.qcut(df.r168,4,labels=False)
    res={"all":summ(df).to_frame().T,
         "by_coin":df.groupby("coin").apply(summ),
         "by_year":df.groupby("year").apply(summ),
         "by_fbucket":df.groupby("fb").apply(summ),
         "by_week_quartile":df.groupby("wk").apply(summ),
         "strength_by_fb":df.groupby("fb")[["z24","z120","z240"]].mean()}
    return res
