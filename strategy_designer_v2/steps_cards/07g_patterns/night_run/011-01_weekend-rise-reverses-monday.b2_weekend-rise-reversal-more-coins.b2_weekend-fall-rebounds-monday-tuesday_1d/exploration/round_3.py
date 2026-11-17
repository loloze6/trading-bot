def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            b["wd"]=ts.dt.weekday.values; b["yr"]=ts.dt.year.values
            b["dkey"]=(ts.astype("int64")//86400_000_000_000).values
            c=b["close"].astype(float)
            b["r1"]=c.pct_change()
            b["f1"]=c.shift(-1)/c-1
            b["f2"]=c.shift(-2)/c-1
            b["sd"]=b["r1"].rolling(60,min_periods=20).std().shift(1)
            b["z1"]=b["r1"]/b["sd"]; b["az"]=b["z1"].abs()
            pos=np.arange(len(b)); b["g2"]=(pos%2==0)
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","wd","yr","dkey","r1","f1","f2","z1","az","sd","g2"]])
    df=pd.concat(rows,ignore_index=True)
    cm=df.groupby("coin")["f1"].mean()
    df["cm"]=df["coin"].map(cm)
    df["x1"]=df["f1"]-df["cm"]; df["x2"]=df["f2"]-2*df["cm"]
    df["xr"]=df["r1"]-df["cm"]
    def tt(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    dm=df.dropna(subset=["xr"]).groupby(["dkey","wd","yr"])["xr"].mean().reset_index()
    out["own-day excess by weekday, date-averaged"]=dm.groupby("wd")["xr"].apply(tt).unstack()
    out["own-day excess date-avg weekday x year"]=dm.pivot_table(index="yr",columns="wd",values="xr",aggfunc="mean")
    pc=[]
    for coin,g in df.dropna(subset=["xr"]).groupby("coin"):
        a=g[g.wd.isin([2,4,5])].xr; o=g[~g.wd.isin([2,4,5])].xr
        t=stats.ttest_ind(a,o,equal_var=False)
        pc.append([coin,a.mean()-o.mean(),t.statistic])
    out["per coin Wed/Fri/Sat minus others"]=pd.DataFrame(pc,columns=["coin","diff","t"]).set_index("coin")
    sun=df[(df.wd==6)].dropna(subset=["z1","x2"]); sun=sun[sun.az<8]
    sun=sun.copy(); sun["x2d"]=sun.x2-sun.groupby("dkey").x2.transform("mean"); sun["zd"]=sun.z1-sun.groupby("dkey").z1.transform("mean")
    s=stats.linregress(sun.zd,sun.x2d); out["sunday within-date x2 on z"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(sun)}"
    sd_=sun.groupby("dkey").agg(z=("z1","mean"),x2=("x2","mean"))
    s=stats.linregress(sd_.z,sd_.x2); out["sunday date-level x2 on mean z"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(sd_)}"
    out["sunday fall x2 by year"]=sun[sun.z1<0].groupby("yr")["x2"].apply(tt).unstack()
    # V shape on 2-day grid, non-overlapping
    a=df[df.g2].dropna(subset=["az","x2"]); a=a[a.az<8].copy()
    a["aq"]=pd.qcut(a.az,5,labels=False)
    out["grid |z| quintile -> x2 by sign"]=a.pivot_table(index="aq",columns=np.sign(a.z1),values="x2",aggfunc="mean")
    out["grid |z| quintile -> x2 t"]=a.groupby("aq")["x2"].apply(tt).unstack()
    r=[]
    for y,g in a.groupby("yr"):
        s=stats.linregress(g.az,g.x2); r.append([y,len(g),s.slope,s.slope/s.stderr])
    out["grid x2 on |z| by year"]=pd.DataFrame(r,columns=["yr","n","slope","t"]).set_index("yr")
    a["x2d"]=a.x2-a.groupby("dkey").x2.transform("mean"); a["azd"]=a.az-a.groupby("dkey").az.transform("mean")
    s=stats.linregress(a.azd,a.x2d); out["grid within-date x2 on |z|"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(a)}"
    dd=a.groupby("dkey").agg(az=("az","mean"),x2=("x2","mean"))
    s=stats.linregress(dd.az,dd.x2); out["grid date-level x2 on mean |z|"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(dd)}"
    r=[]
    for coin,g in a.groupby("coin"):
        s=stats.linregress(g.az,g.x2); r.append([coin,len(g),s.slope,s.slope/s.stderr])
    out["grid x2 on |z| by coin"]=pd.DataFrame(r,columns=["coin","n","slope","t"]).set_index("coin")
    return out
