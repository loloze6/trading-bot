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
            sd=b["r1"].rolling(60,min_periods=20).std().shift(1)
            b["z1"]=b["r1"]/sd; b["az"]=b["z1"].abs()
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","wd","yr","dkey","r1","f1","f2","z1","az","sd"]])
    df=pd.concat(rows,ignore_index=True)
    cm=df.groupby("coin")["f1"].mean()
    df["cm"]=df["coin"].map(cm)
    df["x1"]=df["f1"]-df["cm"]; df["x2"]=df["f2"]-2*df["cm"]
    df["xr"]=df["r1"]-df["cm"]
    def tt(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    # date-clustered weekday effect of own-day return
    dm=df.dropna(subset=["xr"]).groupby(["dkey","wd","yr"])["xr"].mean().reset_index()
    out["own-day excess return by weekday, date-averaged"]=dm.groupby("wd")["xr"].apply(tt).unstack()
    out["own-day excess, date-avg, weekday x year (mean)"]=dm.pivot_table(index="yr",columns="wd",values="xr",aggfunc="mean")
    # per coin t of Wed/Fri/Sat minus others
    pc=[]
    for coin,g in df.dropna(subset=["xr"]).groupby("coin"):
        a=g[g.wd.isin([2,4,5])].xr; o=g[~g.wd.isin([2,4,5])].xr
        t=stats.ttest_ind(a,o,equal_var=False)
        pc.append([coin,a.mean()-o.mean(),t.statistic])
    out["per coin Wed/Fri/Sat minus others"]=pd.DataFrame(pc,columns=["coin","diff","t"]).set_index("coin")
    # Sunday reversal by year, date-clustered: x2 on z, per date demeaned? use per-year slope
    sun=df[(df.wd==6)].dropna(subset=["z1","x2"]); sun=sun[sun.az<8]
    r=[]
    for y,g in sun.groupby("yr"):
        s=stats.linregress(g.z1,g.x2); r.append([y,len(g),s.slope,s.slope/s.stderr])
    out["sunday x2 on z by year"]=pd.DataFrame(r,columns=["yr","n","slope","t"]).set_index("yr")
    # Sunday rises: x2 by year
    sr=sun[sun.z1>0]; sf=sun[sun.z1<0]
    out["sunday rise x2 by year"]=sr.groupby("yr")["x2"].apply(tt).unstack()
    out["sunday fall x2 by year"]=sf.groupby("yr")["x2"].apply(tt).unstack()
    # V shape: next-day excess by abs-z quintile, all days and per weekday group
    a=df.dropna(subset=["az","x1"]); a=a[a.az<8].copy()
    a["aq"]=pd.qcut(a.az,5,labels=False)
    out["all days |z| quintile -> x1, sign split"]=a.pivot_table(index="aq",columns=np.sign(a.z1),values="x1",aggfunc="mean")
    out["all days |z| quintile -> x1 t"]=a.groupby("aq")["x1"].apply(tt).unstack()
    r=[]
    for y,g in a.groupby("yr"):
        s=stats.linregress(g.az,g.x1); r.append([y,len(g),s.slope,s.slope/s.stderr])
    out["x1 on |z| by year"]=pd.DataFrame(r,columns=["yr","n","slope","t"]).set_index("yr")
    # date-clustered V: per date mean of x1*... use cross-sectional: per date regress? simpler: per-date mean x1 vs per-date mean |z|
    dd=a.groupby("dkey").agg(az=("az","mean"),x1=("x1","mean"),z=("z1","mean"))
    s=stats.linregress(dd.az,dd.x1); out["date-level x1 on mean |z|"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(dd)}"
    # within-date: demean by date
    a["x1d"]=a.x1-a.groupby("dkey").x1.transform("mean"); a["azd"]=a.az-a.groupby("dkey").az.transform("mean")
    s=stats.linregress(a.azd,a.x1d); out["within-date x1 on |z|"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(a)}"
    # vol level -> next 1 day by year
    return out
