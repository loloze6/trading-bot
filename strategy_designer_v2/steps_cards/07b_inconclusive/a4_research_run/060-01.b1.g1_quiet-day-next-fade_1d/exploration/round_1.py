def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        allnext=[]
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"]
            nr=c.shift(-1)/c-1
            allnext.append(nr.dropna())
        drift=pd.concat(allnext).mean()
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"]; r=c.pct_change()
            s=r.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"day":pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "fc":df["forecast"],"sc":(r.abs()/s),"r0":r,
                "clv":(c-df["low"])/(df["high"]-df["low"]),
                "tr60":c/c.shift(60)-1,"ag":r.rolling(30).std()/r.rolling(120,min_periods=60).std()})
            for h in [1,2,3,5]:
                d[f"a{h}"]=(c.shift(-h)/c-1)-drift*h
            d["year"]=d["day"].dt.year
            rows.append(d)
    D=pd.concat(rows)
    D["case"]=D["fc"]<0
    def ct(x,col):
        x=x.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x),"mean%":np.nan,"t":np.nan})
        dev=x[col]-x[col].mean()
        g=dev.groupby(x["day"]).sum(); n=len(g)
        se=np.sqrt((g**2).sum()*n/(n-1))/len(x)
        return pd.Series({"n":len(x),"mean%":x[col].mean()*100,"t":x[col].mean()/se})
    C=D[D.case]
    out={}
    out["cases_by_h"]=pd.DataFrame({f"h{h}":ct(C,f"a{h}") for h in [1,2,3,5]}).T
    out["flat_vs_not_h1"]=D.groupby("case").apply(lambda x:ct(x,"a1"))
    out["by_coin"]=C.groupby("coin").apply(lambda x:ct(x,"a1"))
    out["by_year"]=C.groupby("year").apply(lambda x:ct(x,"a1"))
    C=C.copy()
    C["trend"]=pd.cut(C["tr60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    C["agit"]=np.where(C["ag"]>1,"agit","calm")
    out["by_trend"]=C.groupby("trend").apply(lambda x:ct(x,"a1"))
    out["by_trend_agit"]=C.groupby(["trend","agit"]).apply(lambda x:ct(x,"a1"))
    C["fq"]=pd.qcut(C["fc"],4,labels=False,duplicates="drop")
    out["by_fc_quart(0=most neg)"]=C.groupby("fq").apply(lambda x:ct(x,"a1"))
    C["cq"]=pd.cut(C["clv"],[-0.01,0.33,0.67,1.01],labels=["low","mid","high"])
    out["by_closeloc"]=C.groupby("cq").apply(lambda x:ct(x,"a1"))
    out["by_prevsign"]=C.groupby(np.sign(C["r0"])).apply(lambda x:ct(x,"a1"))
    return out
