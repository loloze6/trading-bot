def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        for H in (1,3,5,10):
            rs=[]
            for w,b in wins.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H):
                    rs.append(c[i+H]/c[i]-1)
            drift[(coin,H)]=(np.mean(rs),np.std(rs))
        for w,b in wins.items():
            c=b["close"].reset_index(drop=True)
            r=c.pct_change()
            hi=c.shift(1).rolling(20,min_periods=20).max()
            sd=r.rolling(20,min_periods=20).std()
            dep=(c/hi-1)/sd
            ret60=c/c.shift(60)-1
            ret10=c/c.shift(10)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            for i in range(0,n-5,5):
                d=dep.iloc[i]
                if not np.isfinite(d) or d>-2: continue
                row=dict(coin=coin,w=w,year=yr[i],dep=d,r60=ret60.iloc[i],r10=ret10.iloc[i],day=b["timestamp"].iloc[i],
                         fc=b["forecast"].iloc[i])
                for H in (1,3,5,10):
                    if i+H<n:
                        m,s=drift[(coin,H)]
                        u=-(c.iloc[i+H]/c.iloc[i]-1-m)
                        row[f"u{H}"]=u; row[f"s{H}"]=u/s
                        row[f"tot{H}"]=-(c.iloc[i+H]/c.iloc[i]-1)
                rows.append(row)
    df=pd.DataFrame(rows)
    def tcl(g,col="u5"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series(dict(n=len(g),mean=np.nan,t=np.nan))
        dd=g.groupby(g["day"].astype(str))[col].sum()-0
        dev=g[col]-g[col].mean()
        ds=dev.groupby(g["day"].astype(str)).sum()
        G=len(ds); se=np.sqrt((ds**2).sum()*G/(G-1))/len(g)
        return pd.Series(dict(n=len(g),days=G,mean=g[col].mean(),t=g[col].mean()/se,str=g[col.replace('u','s')].mean() if col.startswith('u') else np.nan))
    out={}
    out["horizons"]=pd.DataFrame({H:tcl(df,f"u{H}") for H in (1,3,5,10)}).T
    out["total_by_H"]=pd.DataFrame({H:tcl(df,f"tot{H}") for H in (1,3,5,10)}).T
    df["trend"]=np.where(df.r60>0.1,"rising",np.where(df.r60<-0.1,"falling",np.where(df.r60.notna(),"choppy","na")))
    out["by_trend"]=df.groupby("trend").apply(tcl)
    df["dq"]=pd.qcut(df.dep,4,labels=["deepest","q2","q3","shallow"])
    out["by_depth"]=df.groupby("dq").apply(tcl)
    out["by_year"]=df.groupby("year").apply(tcl)
    out["by_coin"]=df.groupby("coin").apply(tcl)
    df["r10q"]=pd.qcut(df.r10,3,labels=["bigfall","mid","small"])
    out["by_r10"]=df.groupby("r10q").apply(tcl)
    out["trend_H10"]=df.groupby("trend").apply(lambda g: tcl(g,"u10"))
    return out
