def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vr=r.rolling(20).std()/r.rolling(60).std()
            r14=c/c.shift(14)-1
            lo60=c.rolling(60).min(); hi60=c.rolling(60).max()
            pos60=(c-lo60)/(hi60-lo60)
            f2=c.shift(-2)/c-1; f5=c.shift(-5)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"day":ts.dt.floor("D"),
                "wd":ts.dt.weekday,"year":ts.dt.year,"vr":vr,"r14":r14,"pos60":pos60,
                "f2":f2,"f5":f5,"r1":r})
            df["sd14"]=r.rolling(60).std()*np.sqrt(14)
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    d2=D[D.i%2==0].groupby("coin").f2.mean(); d5=D[D.i%5==0].groupby("coin").f5.mean()
    D["u2"]=D.f2-D.coin.map(d2); D["u5"]=D.f5-D.coin.map(d5)
    D["z14"]=D.r14/D.sd14
    def tclus(s,days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).dropna()
        if len(x)<5: return (np.nan,np.nan,len(x),0)
        ds=x.groupby("d").v.sum(); n=len(ds)
        t=ds.mean()/(ds.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan
        return (x.v.mean(),t,len(x),n)
    out={}
    # Friday 2d unusual by z14 quintile (all vol)
    F=D[(D.wd==4)].dropna(subset=["z14","u2"]).copy()
    F["q"]=pd.qcut(F.z14,5,labels=False)
    res=[]
    for q,g in F.groupby("q"):
        m,t,n,nd=tclus(g.u2,g.day); res.append([q,g.z14.median(),m,t,n,nd])
    out["fri_z14_quintile_2d"]=pd.DataFrame(res,columns=["q","z14_med","mean","t","n","days"])
    # same for other weekdays (weekly grid), slope of u2 on z14
    res=[]
    for wd in range(7):
        g=D[D.wd==wd].dropna(subset=["z14","u2"])
        sl,ic,rr,p,se=__import__("scipy").stats.linregress(g.z14,g.u2)
        top=g[g.z14>g.z14.quantile(.8)]; bot=g[g.z14<g.z14.quantile(.2)]
        res.append([wd,sl,sl/se,top.u2.mean(),bot.u2.mean(),len(g)])
    out["weekday_z14_slope_2d"]=pd.DataFrame(res,columns=["wd","slope","t_naive","top20_u2","bot20_u2","n"])
    # Friday z14 top-40% by year and by coin
    Ft=F[F.q>=3]
    out["fri_topz_by_year"]=Ft.groupby("year").u2.agg(["mean","size"])
    out["fri_topz_by_coin"]=Ft.groupby("coin").u2.agg(["mean","size"])
    out["fri_all_by_coin"]=F.groupby("coin").u2.agg(["mean","size"])
    # pos60 quintile 5d: by vr high/low
    g5=D[D.i%5==0].dropna(subset=["pos60","u5","vr"]).copy()
    g5["q"]=pd.qcut(g5.pos60,5,labels=False)
    res=[]
    for (h,q),g in g5.groupby([g5.vr>1,"q"]):
        m,t,n,nd=tclus(g.u5,g.day); res.append([h,q,m,t,n])
    out["pos60_by_vr_5d"]=pd.DataFrame(res,columns=["vr>1","q","mean","t","n"])
    # z14 quintile 5d all days
    g5=D[D.i%5==0].dropna(subset=["z14","u5"]).copy(); g5["q"]=pd.qcut(g5.z14,5,labels=False)
    res=[]
    for q,g in g5.groupby("q"):
        m,t,n,nd=tclus(g.u5,g.day); res.append([q,g.z14.median(),m,t,n])
    out["z14_quintile_5d_all"]=pd.DataFrame(res,columns=["q","z14_med","mean","t","n"])
    # book: daily returns, largest gains/losses by weekday
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["wd"]=pd.to_datetime(dd["day"],utc=True).dt.weekday; dd["coin"]=coin; br.append(dd)
    B=pd.concat(br).dropna(subset=["book_return"])
    B=B[B.book_return!=0]
    out["book_nonzero_by_wd"]=B.groupby("wd").book_return.agg(["mean","size","min","max"])
    return out
