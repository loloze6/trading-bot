def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,2,3,6,12]
    rows=[]; grid=[]
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
            vr=b["volume"]/b["volume"].rolling(720,min_periods=120).mean()
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b)
            fw={h:(c.shift(-h)/c-1) for h in H}
            f=b["forecast"]
            # cases: first bar per 6-grid cell with forecast<=-2
            cell=np.arange(n)//6
            m=(f<=-2)
            sel=pd.Series(np.arange(n))[m.values].groupby(cell[m.values]).first().values
            for i in sel:
                d={"coin":coin,"w":w,"yr":yr[i],"f":f[i],"sc":sc[i],"vr":vr[i]}
                for h in H: d[f"r{h}"]=-(fw[h][i]-drift[(coin,h)])
                rows.append(d)
            # grid sample of all bars at 6h grid
            for i in range(0,n-6,6):
                d={"coin":coin,"yr":yr[i],"sc":sc[i],"vr":vr[i]}
                for h in [1,3,6]: d[f"g{h}"]=fw[h][i]-drift[(coin,h)]
                grid.append(d)
    df=pd.DataFrame(rows).dropna(subset=["r6"]); g=pd.DataFrame(grid).dropna()
    def summ(x,col):
        x=x[col].dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["cases by horizon (short-signed, drift removed)"]=pd.DataFrame({f"h{h}":summ(df,f"r{h}") for h in H}).T
    out["cases by coin h6"]=df.groupby("coin").apply(lambda x:summ(x,"r6"))
    out["cases by year h6"]=df.groupby("yr").apply(lambda x:summ(x,"r6"))
    df["fq"]=pd.qcut(df["f"].abs().rank(method="first"),5,labels=False)
    out["cases by |forecast| quintile h6"]=df.groupby("fq").apply(lambda x:pd.concat([summ(x,"r6"),pd.Series({"sc_med":x["sc"].median()})]))
    out["cases by |forecast| quintile h1,h3"]=df.groupby("fq").apply(lambda x:pd.Series({"h1%":100*x.r1.mean(),"t1":summ(x,"r1")["t"],"h3%":100*x.r3.mean(),"t3":summ(x,"r3")["t"]}))
    # grid: sign-aware continuation by size and volume bins
    g["sb"]=pd.cut(g["sc"],[-np.inf,-4,-2,-1,1,2,4,np.inf])
    g["vb"]=pd.cut(g["vr"],[0,0.5,1.5,3,np.inf])
    def gs(x):
        s=summ(x,"g6"); return pd.Series({"n":s["n"],"g6%":s["mean%"],"t6":s["t"],"g1%":100*x.g1.mean()})
    out["grid: next-6h raw move (drift removed) by hour scaled return x volume"]=g.groupby(["vb","sb"],observed=True).apply(gs)
    return out
