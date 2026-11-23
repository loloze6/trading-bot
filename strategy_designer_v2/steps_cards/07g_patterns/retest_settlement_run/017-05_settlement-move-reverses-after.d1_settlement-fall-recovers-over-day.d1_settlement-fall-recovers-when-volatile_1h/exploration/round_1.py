def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=c.pct_change()
            vol7=r1.rolling(168,min_periods=100).std()
            vol30=r1.rolling(720,min_periods=400).std()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "hc":((ts+pd.Timedelta(hours=1)).dt.hour).values,
                "wd":((ts+pd.Timedelta(hours=1)).dt.weekday).values,
                "r1":r1.values,
                "r2z":(c/c.shift(2)-1).values/(vol7.values*np.sqrt(2)),
                "r24z":(c/c.shift(24)-1).values/(vol7.values*np.sqrt(24)),
                "r72z":(c/c.shift(72)-1).values/(vol7.values*np.sqrt(72)),
                "vr":(vol7/vol30).values,
                "f24":(c.shift(-24)/c-1).values,
                "f72":(c.shift(-72)/c-1).values,
                "fc":b["forecast"].values,
                "alloc":b["postRebalance_current_allocation"].values,
                "vol":b["volume"].astype(float).values})
            df["vrel"]=df["vol"]/pd.Series(df["vol"]).rolling(168,min_periods=100).median().values
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    # drifts
    g24=A[A.pos%24==0].dropna(subset=["f24"]); d24=g24.groupby("coin").f24.mean()
    g72=A[A.pos%72==0].dropna(subset=["f72"]); d72=g72.groupby("coin").f72.mean()
    A["x24"]=A.f24-A.coin.map(d24); A["x72"]=A.f72-A.coin.map(d72)
    out={}
    # hour of close: mean hourly return and t, relative volume
    h=A.dropna(subset=["r1"]).groupby("hc").agg(m=("r1","mean"),s=("r1","std"),n=("r1","size"),vrel=("vrel","median"))
    h["t"]=h.m/(h.s/np.sqrt(h.n)); out["hour_ret"]=h[["m","t","vrel"]]
    wdd=A.dropna(subset=["r1"]).groupby("wd").r1.agg(["mean","std","size"]); wdd["t"]=wdd["mean"]/(wdd["std"]/np.sqrt(wdd["size"]))
    out["weekday_ret"]=wdd
    # slope of x24 on -r2z by close hour, sampled at that hour (one per day per hour)
    res=[]
    for hh in range(24):
        s=A[(A.hc==hh)].dropna(subset=["r2z","x24"])
        # non-overlap: one per day per hour already
        if len(s)<100: continue
        sl=stats.linregress(-s.r2z.clip(-5,5),s.x24)
        res.append((hh,len(s),sl.slope,sl.slope/sl.stderr))
    out["rev2h_by_hour"]=pd.DataFrame(res,columns=["hc","n","slope","t"])
    # 24h and 72h past return deciles -> forward, grid
    for lab,col,f,g in [("r24z_f24","r24z","x24",24),("r72z_f72","r72z","x72",72),("r24z_f72","r24z","x72",72)]:
        s=A[A.pos%g==0].dropna(subset=[col,f]).copy()
        s["q"]=pd.qcut(s[col],10,labels=False)
        t=s.groupby("q").agg(m=(f,"mean"),sd=(f,"std"),n=(f,"size")); t["t"]=t.m/(t.sd/np.sqrt(t.n))
        out[lab]=t[["m","t","n"]]
    # vol ratio quintiles -> x24, and abs move
    s=g24.dropna(subset=["vr"]).copy(); s["x24"]=s.f24-s.coin.map(d24)
    s["q"]=pd.qcut(s.vr,5,labels=False)
    t=s.groupby("q").agg(vr=("vr","mean"),m=("x24","mean"),sd=("x24","std"),n=("x24","size")); t["t"]=t.m/(t.sd/np.sqrt(t.n)); out["vr_f24"]=t
    # forecast buckets
    s=A[(A.fc>0)].dropna(subset=["x24"]).copy(); s["cell"]=s.pos//24
    s=s.groupby(["coin","w","cell"]).head(1)
    s["q"]=pd.cut(s.fc,[0,1,2,3,5,21])
    t=s.groupby("q").agg(m=("x24","mean"),sd=("x24","std"),n=("x24","size")); t["t"]=t.m/(t.sd/np.sqrt(t.n)); out["fc_buckets"]=t
    # per coin size of reversal at settlement
    return out
