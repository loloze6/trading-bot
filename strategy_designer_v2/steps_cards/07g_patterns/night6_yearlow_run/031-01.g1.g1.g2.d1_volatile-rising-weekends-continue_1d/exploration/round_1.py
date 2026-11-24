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
            f2=c.shift(-2)/c-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"day":ts.dt.floor("D"),
                "wd":ts.dt.weekday,"year":ts.dt.year,"vr":vr,"r14":r14,"pos60":pos60,"r1":r,
                "f1":f1,"f2":f2,"f5":f5,"fc":b["forecast"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    # drifts on non-overlapping grids
    def drift(h,col):
        g=D[D.i%h==0]
        return g.groupby("coin")[col].mean()
    d1=drift(1,"f1");d2=drift(2,"f2");d5=drift(5,"f5")
    D["u1"]=D.f1-D.coin.map(d1);D["u2"]=D.f2-D.coin.map(d2);D["u5"]=D.f5-D.coin.map(d5)
    def tclus(s,days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).dropna()
        if len(x)<5: return (np.nan,np.nan,len(x),0)
        ds=x.groupby("d").v.sum(); n=len(ds)
        t=ds.mean()/(ds.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan
        return (x.v.mean(),t,len(x),n)
    out={}
    # Friday->Sunday by vr and r14 sign (one per week, nonoverlapping)
    F=D[D.wd==4].copy()
    F["vrg"]=np.where(F.vr>1,"vr>1","vr<=1"); F["rg"]=np.where(F.r14>0,"rise","fall")
    res=[]
    for k,g in F.groupby(["vrg","rg"]):
        m,t,n,nd=tclus(g.u2,g.day); res.append([*k,m,t,n,nd])
    out["fri_2d_unusual_by_vr_r14"]=pd.DataFrame(res,columns=["vr","r14","mean","t","cases","days"])
    # every weekday: 2-day unusual return conditioned vr>1 & rise, one grid per weekday (weekly)
    res=[]
    for wd in range(7):
        g=D[(D.wd==wd)]
        for lab,gg in [("all",g),("vr>1&rise",g[(g.vr>1)&(g.r14>0)]),("vr<=1&rise",g[(g.vr<=1)&(g.r14>0)])]:
            m,t,n,nd=tclus(gg.u2,gg.day); res.append([wd,lab,m,t,n])
    out["weekday_2d_unusual"]=pd.DataFrame(res,columns=["wd","grp","mean","t","n"])
    # graded: Fri vr>1 rise, quintiles of r14*vr
    G=F[(F.vr>1)&(F.r14>0)].copy(); G["s"]=G.r14*G.vr
    G["q"]=pd.qcut(G.s,4,labels=False)
    out["fri_active_quartile"]=G.groupby("q").agg(mean_u2=("u2","mean"),n=("u2","size"),s_med=("s","median"))
    # whole sample: pos60 quintiles, 5-day unusual (grid 5)
    g5=D[D.i%5==0].dropna(subset=["pos60","u5"]).copy()
    g5["q"]=pd.qcut(g5.pos60,5,labels=False)
    res=[]
    for q,g in g5.groupby("q"):
        m,t,n,nd=tclus(g.u5,g.day); res.append([q,m,t,n])
    out["pos60_quintile_5d"]=pd.DataFrame(res,columns=["q","mean","t","n"])
    # after large daily moves: r1 deciles, next 2d unusual (grid 2)
    g2=D[D.i%2==0].dropna(subset=["r1","u2"]).copy()
    g2["z"]=g2.r1/g2.groupby("coin").r1.transform("std")
    g2["q"]=pd.cut(g2.z,[-99,-2,-1,0,1,2,99])
    res=[]
    for q,g in g2.groupby("q",observed=True):
        m,t,n,nd=tclus(g.u2,g.day); res.append([str(q),m,t,n])
    out["after_move_2d"]=pd.DataFrame(res,columns=["z","mean","t","n"])
    # vr quintiles all days, 2d unusual
    g2v=g2.dropna(subset=["vr"]).copy(); g2v["q"]=pd.qcut(g2v.vr,5,labels=False)
    res=[]
    for q,g in g2v.groupby("q"):
        m,t,n,nd=tclus(g.u2,g.day); res.append([q,g.vr.median(),m,t,n])
    out["vr_quintile_2d"]=pd.DataFrame(res,columns=["q","vr_med","mean","t","n"])
    return out
