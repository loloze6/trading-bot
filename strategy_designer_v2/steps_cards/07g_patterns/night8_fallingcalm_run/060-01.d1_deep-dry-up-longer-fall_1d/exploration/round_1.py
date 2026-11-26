def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=20
    rows=[]; drow=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            tr=c/c.shift(60)-1
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            sd30=r1.rolling(30).std()
            sdmed=sd30.rolling(365,min_periods=120).median()
            ag=(sd30>sdmed).astype(float).where(sdmed.notna())
            r5=c/c.shift(5)-1
            r20b=c/c.shift(20)-1
            fwd=c.shift(-H)/c-1
            fc=b["forecast"].astype(float)
            n=len(b)
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,tr=tr[i],vr=vr[i],ag=ag[i],r5=r5[i],r20b=r20b[i],
                                 fwd=fwd[i],fc=fc[i],sd=sd30[i],wd=pd.Timestamp(b["timestamp"][i]).weekday(),
                                 yr=pd.Timestamp(b["timestamp"][i]).year))
            # daily next-day
            f1=c.shift(-1)/c-1
            for i in range(0,n-1):
                pass
            drow.append(pd.DataFrame(dict(coin=coin,w=w,tr=tr,vr=vr,ag=ag,r1=r1,f1=f1,f5=c.shift(-5)/c-1,
                                          sdz=r1/sd30,wd=pd.to_datetime(b["timestamp"]).dt.weekday)))
    g=pd.DataFrame(rows)
    g["mu"]=g.groupby("coin")["fwd"].transform("mean")
    g["ex"]=g["fwd"]-g["mu"]
    g["prof"]=np.where(g.tr>0.1,"rising",np.where(g.tr<-0.1,"falling","choppy"))
    g["agit"]=np.where(g.ag==1,"agit","calm")
    out={}
    def tt(x):
        x=x.dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    # volume ratio terciles by profile, excess fwd 20d
    gg=g.dropna(subset=["vr","ex"]).copy()
    gg["vq"]=gg.groupby("coin")["vr"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=["shrink","mid","grow"]))
    out["ex20 by profile x vol tercile"]=gg.groupby(["prof","vq"])["ex"].apply(tt).unstack()
    out["ex20 by profile x agit"]=gg.groupby(["prof","agit"])["ex"].apply(tt).unstack()
    # slope of ex on vr per profile
    res={}
    for p,s in gg.groupby("prof"):
        sl=stats.linregress(s.vr,s.ex); res[p]=dict(n=len(s),slope=sl.slope,t=sl.slope/sl.stderr)
    out["slope ex20 on vr by profile"]=pd.DataFrame(res).T
    # past 20d return grading
    res={}
    for p,s in gg.dropna(subset=["r20b"]).groupby("prof"):
        sl=stats.linregress(s.r20b,s.ex); res[p]=dict(n=len(s),slope=sl.slope,t=sl.slope/sl.stderr)
    out["slope ex20 on past20 by profile"]=pd.DataFrame(res).T
    out["ex20 by window"]=gg.groupby("w")["ex"].apply(tt).unstack()
    # daily
    d=pd.concat(drow,ignore_index=True)
    d["prof"]=np.where(d.tr>0.1,"rising",np.where(d.tr<-0.1,"falling","choppy"))
    d=d.dropna(subset=["sdz","f1"])
    d["zq"]=pd.cut(d.sdz,[-99,-2,-1,0,1,2,99])
    d["mu1"]=d.groupby("coin")["f1"].transform("mean")
    d["e1"]=d.f1-d.mu1
    out["next-day ex by z of today's move x profile (overlap-free 1d)"]=d.groupby(["prof","zq"])["e1"].apply(tt).unstack()
    out["next-day ex by weekday"]=d.groupby("wd")["e1"].apply(tt).unstack()
    # book
    days=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            days.append(x.assign(coin=coin,w=w))
    D=pd.concat(days)
    out["book daily by window"]=D.groupby("w")["book_return"].apply(tt).unstack()
    tr_=pd.concat([t.assign(coin=c,w=w) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades by coin"]=tr_.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
