def explore(data):
    import numpy as np, pandas as pd
    H=[24,120,240]
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-h,h); rr+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(rr); drift[(coin,h,'sd')]=np.std(rr)
        for w,b in ws.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            s=pd.Series(c)
            r24=s.pct_change(24); ratio=(r24/r24.abs().rolling(720,min_periods=120).mean()).values
            r168=s.pct_change(168).values
            r720=s.pct_change(720).values
            n=len(c)
            for st in range(0,n,120):
                e=min(st+120,n); lo=np.inf
                for i in range(st,e):
                    lo=min(lo,f[i])
                    if f[i]>=2 and f[i]-lo>=2:
                        d={"coin":coin,"year":yr[i],"f":f[i],"ratio":ratio[i],"r168":r168[i],"r720":r720[i]}
                        for h in H:
                            d["x%d"%h]=(c[i+h]/c[i]-1-drift[(coin,h)]) if i+h<n else np.nan
                            d["z%d"%h]=d["x%d"%h]/drift[(coin,h,'sd')] if i+h<n else np.nan
                        rows.append(d); break
    df=pd.DataFrame(rows)
    def summ(g):
        out={}
        for h in H:
            x=g["x%d"%h].dropna(); out["m%d"%h]=x.mean(); out["t%d"%h]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
            out["z%d"%h]=g["z%d"%h].mean()
        out["n"]=len(g); return pd.Series(out)
    df["rb"]=pd.cut(df.ratio,[-10,1,1.5,2,2.5,3,4,100])
    df["wk"]=pd.qcut(df.r168,4,labels=False)
    df["mo"]=np.where(df.r720>0,"r30d_up","r30d_down")
    cap=df[df.f>=19.99]
    return {"by_ratio":df.groupby("rb").apply(summ),
            "cap_by_week_q":cap.groupby("wk").apply(summ),
            "cap_by_year":cap.groupby("year").apply(summ),
            "cap_by_coin":cap.groupby("coin").apply(summ),
            "all_by_30d":df.groupby("mo").apply(summ),
            "cap_by_30d":cap.groupby("mo").apply(summ),
            "corr_ratio_x120":pd.Series({"spearman":df[["ratio","x120"]].corr("spearman").iloc[0,1],"n":df[["ratio","x120"]].dropna().shape[0]})}
