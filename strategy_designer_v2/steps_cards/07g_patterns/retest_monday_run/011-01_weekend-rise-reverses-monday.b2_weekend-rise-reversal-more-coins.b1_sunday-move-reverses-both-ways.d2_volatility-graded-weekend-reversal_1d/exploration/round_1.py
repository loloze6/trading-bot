def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            s20=r.rolling(20).std(); s60=r.rolling(60).std()
            df=pd.DataFrame({"coin":coin,"win":w,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "year":pd.to_datetime(b["timestamp"]).dt.year,
                "r1":r,"r2":c/c.shift(2)-1,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,
                "f5":c.shift(-5)/c-1,
                "s20":s20,"vr":s20/s60,
                "volrel":v/v.rolling(20).mean(),
                "volwk":(v+v.shift(1))/(2*v.rolling(28).mean()),
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["z1"]=d.r1/d.s20; d["z2"]=d.r2/d.s20
    def slope(x,y):
        m=x.notna()&y.notna(); x=x[m];y=y[m]
        if len(x)<30: return (np.nan,np.nan,len(x))
        res=stats.linregress(x,y); return (res.slope,res.slope/res.stderr,len(x))
    out={}
    # reversal by weekday: f2 (scaled by s20) on z1
    t=[]
    for wd in range(7):
        g=d[d.wd==wd]
        for h in ["f1","f2","f3","f5"]:
            s,tt,n=slope(g.z1,g[h]/g.s20); t.append((wd,h,s,tt,n))
    out["z1->fwd by weekday (0=Mon,6=Sun)"]=pd.DataFrame(t,columns=["wd","h","slope","t","n"]).pivot(index="wd",columns="h",values="t")
    t2=pd.DataFrame(t,columns=["wd","h","slope","t","n"]).pivot(index="wd",columns="h",values="slope")
    out["slopes by weekday"]=t2.round(4)
    # two-day weekend return (Sat+Sun) vs Sunday only
    g=d[d.wd==6]
    out["Sun: z2(Sat+Sun) vs f2 / z1"]=pd.DataFrame([slope(g.z2,g.f2/g.s20),slope(g.z1,g.f2/g.s20)],index=["z2","z1"],columns=["slope","t","n"])
    # volume grading on Sunday
    g=g.copy(); g["sr"]=-np.sign(g.r1)*g.f2/g.s20
    g["vq"]=pd.qcut(g.volrel,4,labels=False); g["zq"]=pd.qcut(g.z1.abs(),4,labels=False)
    g["vrq"]=pd.qcut(g.vr,4,labels=False)
    for k in ["vq","zq","vrq"]:
        a=g.groupby(k)["sr"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
        a.columns=["mean_signed_rev_in_s20","n","t"]; out["Sun by "+k]=a.round(3)
    out["Sun signed rev by year"]=g.groupby("year")["sr"].agg(["mean","count"]).round(3)
    # all weekdays: signed reversal by |z1| quartile, other days
    o=d[d.wd!=6].copy(); o["sr"]=-np.sign(o.r1)*o.f2/o.s20
    o["zq"]=pd.qcut(o.z1.abs(),4,labels=False)
    out["nonSun by |z1| q"]=o.groupby("zq")["sr"].agg(["mean","count"]).round(3)
    return out
