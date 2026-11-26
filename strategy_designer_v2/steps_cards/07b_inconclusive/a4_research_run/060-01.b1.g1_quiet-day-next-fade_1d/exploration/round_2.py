def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        allnext=[]
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"]; allnext.append((c.shift(-1)/c-1).dropna())
        drift=pd.concat(allnext).mean()
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"]; r=c.pct_change()
            s=r.rolling(20).std()
            v30=r.rolling(30).std()
            pct=v30.expanding(min_periods=30).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d=pd.DataFrame({"coin":coin,"win":w,"day":pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "fc":df["forecast"],"sc":(r.abs()/s),"r0":r,
                "tr60":c/c.shift(60)-1,"tr30":c/c.shift(30)-1,"pct":pct,
                "ag120":v30/r.rolling(120,min_periods=60).std()})
            d["a1"]=(c.shift(-1)/c-1)-drift
            d["year"]=d["day"].dt.year
            rows.append(d)
    D=pd.concat(rows)
    D["case"]=D["fc"]<0
    def ct(x,col="a1"):
        x=x.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x),"mean%":np.nan,"t":np.nan,"days":np.nan})
        dev=x[col]-x[col].mean()
        g=dev.groupby(x["day"]).sum(); n=len(g)
        se=np.sqrt((g**2).sum()*n/(n-1))/len(x)
        return pd.Series({"n":len(x),"mean%":x[col].mean()*100,"t":x[col].mean()/se,"days":n})
    out={}
    D["fall"]=D["tr60"]<-0.1
    D["agp"]=D["pct"]>0.5
    D["fa_pct"]=D["fall"]&D["agp"]
    D["fa_120"]=D["fall"]&(D["ag120"]>1)
    out["fa_pct: case x inprofile"]=D.dropna(subset=["tr60","pct"]).groupby(["fa_pct","case"]).apply(ct)
    out["fa_120: case x inprofile"]=D.dropna(subset=["tr60","ag120"]).groupby(["fa_120","case"]).apply(ct)
    F=D[D.fa_120&D.case].copy()
    out["fa120 cases by coin"]=F.groupby("coin").apply(ct)
    out["fa120 cases by year"]=F.groupby("year").apply(ct)
    F["half"]=np.where(F["sc"]<=F["sc"].median(),"flatter","less flat")
    out["fa120 cases by flatness half"]=F.groupby("half").apply(ct)
    out["fa120 cases by prevsign"]=F.groupby(np.sign(F["r0"])).apply(ct)
    # graded within falling-agitated across all days: scaled move bins
    G=D[D.fa_120].copy()
    G["scb"]=pd.cut(G["sc"],[0,0.25,0.5,1,2,99])
    out["fa120 all days by |r|/s"]=G.groupby("scb").apply(ct)
    P=D[D.fa_pct&D.case].copy()
    out["fa_pct cases by coin"]=P.groupby("coin").apply(ct)
    return out
