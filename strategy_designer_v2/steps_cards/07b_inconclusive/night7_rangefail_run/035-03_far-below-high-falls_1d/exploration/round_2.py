def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        for H in (5,10):
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
            sd30=r.rolling(30,min_periods=30).std()
            agit=sd30/sd30.expanding(30).median()
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            for i in range(0,n-5,5):
                d=dep.iloc[i]
                if not np.isfinite(d) or d>-2: continue
                row=dict(coin=coin,w=w,year=yr[i],dep=d,r60=ret60.iloc[i],ag=agit.iloc[i],day=b["timestamp"].iloc[i])
                for H in (5,10):
                    if i+H<n:
                        m,s=drift[(coin,H)]
                        u=-(c.iloc[i+H]/c.iloc[i]-1-m)
                        row[f"u{H}"]=u; row[f"s{H}"]=u/s; row[f"tot{H}"]=-(c.iloc[i+H]/c.iloc[i]-1)
                rows.append(row)
    df=pd.DataFrame(rows)
    def tcl(g,col="u5"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series(dict(n=len(g),days=np.nan,mean=np.nan,t=np.nan))
        dev=g[col]-g[col].mean()
        ds=dev.groupby(g["day"].astype(str)).sum()
        G=len(ds); se=np.sqrt((ds**2).sum()*G/(G-1))/len(g)
        return pd.Series(dict(n=len(g),days=G,mean=g[col].mean(),t=g[col].mean()/se))
    df["trend"]=np.where(df.r60>0.1,"rising",np.where(df.r60<-0.1,"falling",np.where(df.r60.notna(),"choppy","na")))
    ch=df[df.trend=="choppy"].copy()
    out={}
    ch["half"]=np.where(ch.dep<=ch.dep.median(),"deeper","shallower")
    out["choppy_depth_u5"]=ch.groupby("half").apply(tcl)
    out["choppy_depth_u10"]=ch.groupby("half").apply(lambda g:tcl(g,"u10"))
    out["choppy_year_u5"]=ch.groupby("year").apply(tcl)
    out["choppy_window_count"]=ch.groupby("w").size()
    out["choppy_tot5"]=tcl(ch,"tot5")
    out["choppy_tot10"]=tcl(ch,"tot10")
    ch["agq"]=np.where(ch.ag>1,"agitated",np.where(ch.ag.notna(),"calm","na"))
    out["choppy_agit"]=ch.groupby("agq").apply(tcl)
    out["choppy_corr_dep_u5"]=float(np.corrcoef(ch.dropna(subset=["u5"]).dep,ch.dropna(subset=["u5"]).u5)[0,1])
    out["all_corr_dep_u5"]=float(np.corrcoef(df.dropna(subset=["u5"]).dep,df.dropna(subset=["u5"]).u5)[0,1])
    out["choppy_coin"]=ch.groupby("coin").apply(tcl)
    return out
