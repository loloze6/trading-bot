def explore(data):
    import numpy as np, pandas as pd
    H=[1,2,3,6]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rr.append(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.concatenate(rr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change()
            sc=r1/r1.abs().rolling(720,min_periods=120).mean()
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b); f=b["forecast"]
            fw={h:(c.shift(-h)/c-1) for h in H}
            cell=np.arange(n)//6
            m=(f<=-2).values
            sel=pd.Series(np.arange(n))[m].groupby(cell[m]).first().values
            for i in sel:
                d={"coin":coin,"yr":yr[i],"f":f[i],"sc":sc[i]}
                for h in H: d[f"r{h}"]=-(fw[h][i]-drift[(coin,h)])
                rows.append(d)
    df=pd.DataFrame(rows).dropna(subset=["r6","sc"])
    def summ(x,col):
        x=x[col].dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    df["sb"]=pd.cut(df["sc"],[-np.inf,0,1,2,3,5,np.inf])
    out["cases by own-hour scaled rise: h2 and h6"]=df.groupby("sb",observed=True).apply(lambda x:pd.Series({**summ(x,"r2").add_prefix("h2_").to_dict(),**summ(x,"r6").add_prefix("h6_").to_dict()}))
    out["h2 by year"]=df.groupby("yr").apply(lambda x:summ(x,"r2"))
    out["h2 by coin"]=df.groupby("coin").apply(lambda x:summ(x,"r2"))
    out["share of cases with sc<=0"]=float((df.sc<=0).mean())
    out["corr sc vs r2, r6"]=pd.Series({"r2":df.sc.corr(df.r2),"r6":df.sc.corr(df.r6)})
    return out
