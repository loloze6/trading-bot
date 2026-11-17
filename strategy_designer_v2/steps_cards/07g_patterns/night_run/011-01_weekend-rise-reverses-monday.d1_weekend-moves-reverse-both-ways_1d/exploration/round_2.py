def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol=r.rolling(20,min_periods=20).std()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"dow":ts.dt.dayofweek,"yr":ts.dt.year,
                "r":r,"z":r/vol,"vol":vol,"f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,
                "vlong":r.rolling(120,min_periods=60).std()}))
    D=pd.concat(rows,ignore_index=True)
    m1=D.groupby("coin").f1.mean(); D["e1"]=D.f1-D.coin.map(m1)
    m2=D[D.pos%2==0].groupby("coin").f2.mean(); D["e2"]=D.f2-D.coin.map(m2)
    X=D.dropna(subset=["z","e1"]).copy()
    X["rev1"]=-np.sign(X.z)*X.e1
    X["vq"]=X.groupby("coin").vol.transform(lambda s: pd.qcut(s,3,labels=False))
    X["vrel"]=X.vol/X.vlong
    tt=lambda s: s.mean()/(s.std()/np.sqrt(s.count()))
    out={}
    H=X[X.vq==2].copy(); H["azq"]=pd.qcut(H.z.abs(),3,labels=False)
    g=H.groupby("azq").rev1
    out["high-vol: fade1 by |z| tercile"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    g=H.groupby(np.sign(H.z)).rev1
    out["high-vol: fade1 by sign"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    # non-overlap: use alternate days only to avoid any concern -> 1-day returns already non-overlapping
    g=H.groupby("coin").rev1
    out["high-vol fade1 by coin"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    g=H.groupby("yr").rev1
    out["high-vol fade1 by year"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    H["wk"]=np.where(H.dow>=5,"weekend","weekday")
    g=H.groupby("wk").rev1
    out["high-vol fade1 weekend vs weekday"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    # graded: slope of e1 on z*vol (raw return) by vol tercile
    X["s"]=-X.z*X.e1
    g=X.groupby("vq")
    out["corr(z,e1) by vol tercile"]=pd.DataFrame({"corr":g.apply(lambda x:x.z.corr(x.e1)),"corr_r":g.apply(lambda x:x.r.corr(x.e1)),"n":g.size()})
    X["rq"]=X.groupby("coin").vrel.transform(lambda s: pd.qcut(s,3,labels=False))
    g=X.dropna(subset=["rq"]).groupby("rq").rev1
    out["fade1 by vol20/vol120 tercile"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    # sunday asymmetry stability by year
    S=X[X.dow==6].dropna(subset=["e2"])
    out["sun e2 after rise by year"]=S[S.z>0].groupby("yr").e2.agg(["mean","count"])
    out["sun e2 after fall by year"]=S[S.z<0].groupby("yr").e2.agg(["mean","count"])
    # raw return magnitude in high vol
    H["rq5"]=pd.qcut(H.r,5,labels=False)
    g=H.groupby("rq5").e1
    out["high-vol e1 by raw return quint"]=pd.DataFrame({"m":g.mean(),"t":g.apply(tt),"n":g.count()})
    return out
