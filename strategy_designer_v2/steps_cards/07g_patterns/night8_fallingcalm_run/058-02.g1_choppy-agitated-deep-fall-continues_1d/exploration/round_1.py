def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values; v=b["volume"].astype(float).values
            n=len(c)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            s=pd.Series(r1)
            sd20=s.rolling(20).std().values
            vr=(pd.Series(v).rolling(5).mean()/pd.Series(v).rolling(30).mean()).values
            ts=pd.to_datetime(b["timestamp"])
            reg=b["regime"].values
            fc=b["forecast"].astype(float).values
            for t in range(0,n-5,5):
                r30=c[t]/c[t-30]-1 if t>=30 else np.nan
                r60=c[t]/c[t-60]-1 if t>=60 else np.nan
                r5=c[t]/c[t-5]-1 if t>=5 else np.nan
                rows.append(dict(coin=coin,w=w,f5=c[t+5]/c[t]-1,r30=r30,r60=r60,r5=r5,
                    z30=r30/(sd20[t]*np.sqrt(30)) if t>=30 else np.nan,sd=sd20[t],vr=vr[t],
                    reg=reg[t],fc=fc[t]))
            for t in range(20,n-1):
                daily.append(dict(coin=coin,w=w,r1=r1[t],z1=r1[t]/sd20[t-1] if t>=21 else np.nan,
                    f1=r1[t+1],wd=ts[t].dayofweek,sd=sd20[t],vr=vr[t]))
    g=pd.DataFrame(rows); d=pd.DataFrame(daily)
    g["ex"]=g["f5"]-g.groupby("coin")["f5"].transform("mean")
    d["ex1"]=d["f1"]-d.groupby("coin")["f1"].transform("mean")
    def tab(df,col,key,q=5):
        x=df.dropna(subset=[col,key]).copy()
        x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("b")[key].agg(mean="mean",n="count",t=lambda y:y.mean()/(y.std()/np.sqrt(len(y)))).assign(lo=x.groupby("b")[col].min())
    out={}
    out["z30 quint all"]=tab(g,"z30","ex")
    out["z30 quint regime unknown"]=tab(g[g.reg=="unknown"],"z30","ex",3)
    out["z30 quint other regime"]=tab(g[g.reg!="unknown"],"z30","ex")
    fall=g[g.r30<0]
    out["falls: volume ratio quint"]=tab(fall,"vr","ex")
    out["r60 quint all"]=tab(g,"r60","ex")
    out["r5 quint all"]=tab(g,"r5","ex")
    out["sd quint 5d"]=tab(g,"sd","ex")
    out["z1 quint next day"]=tab(d,"z1","ex1",10)
    out["vr quint next day"]=tab(d,"vr","ex1")
    out["weekday next day"]=d.groupby("wd")["ex1"].agg(mean="mean",n="count",t=lambda y:y.mean()/(y.std()/np.sqrt(len(y))))
    out["regime counts"]=g["reg"].value_counts()
    # book: days with largest gains/losses
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book by window"]=D.groupby("w")["book_return"].agg(mean="mean",n="count")
    out["book by year"]=D.groupby("yr")["book_return"].agg(mean="mean",sum="sum")
    return out
