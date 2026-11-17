def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20,min_periods=15).std()
            df=pd.DataFrame({"coin":coin,"w":w,"wn":int(w[1:]),"year":ts.dt.year,"dow":ts.dt.dayofweek,
                             "r":r,"z":r/sd,"vol":b["volume"].astype(float),"pos":np.arange(len(b))})
            df["vrel"]=df["vol"]/df["vol"].rolling(28,min_periods=10).median()
            for h in (1,2,3,5):
                df[f"f{h}"]=c.shift(-h)/c-1
            df["fc"]=b["forecast"].astype(float)
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    # coin mean h returns on grid
    for h in (1,2,3,5):
        m=d[d.pos%h==0].groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"]=d[f"f{h}"]-d["coin"].map(m)
    def reg(s,x,y):
        s=s[[x,y]].dropna()
        if len(s)<10: return (np.nan,np.nan,len(s))
        res=stats.linregress(s[x],s[y]); return (res.slope,res.slope/res.stderr,len(s))
    out={}
    # by weekday: slope of next-h excess return on z (all sizes, both sides)
    t=[]
    for dw in range(7):
        s=d[d.dow==dw]
        row={"dow":dw}
        for h in (1,2,3,5):
            sl,tt,n=reg(s,"z",f"x{h}"); row[f"slope{h}"]=sl;row[f"t{h}"]=tt
        row["n"]=n; t.append(row)
    out["slope fwd excess on z, by weekday (6=Sun)"]=pd.DataFrame(t).round(4)
    sun=d[d.dow==6]
    t=[]
    for side,s in (("fall",sun[sun.z<0]),("rise",sun[sun.z>0])):
        row={"side":side,"n":len(s)}
        for h in (1,2,3,5):
            sl,tt,n=reg(s,"z",f"x{h}");row[f"slope{h}"]=sl;row[f"t{h}"]=tt
            row[f"mean{h}"]=s[f"x{h}"].mean()
        t.append(row)
    out["sunday by side"]=pd.DataFrame(t).round(4)
    t=[]
    for k,s in sun.groupby("coin"):
        row={"coin":k}
        for h in (1,2,3):
            sl,tt,n=reg(s,"z",f"x{h}");row[f"t{h}"]=tt
        f=s[s.z<0]; sl,tt,n=reg(f,"z","x2"); row["fall_t2"]=tt
        t.append(row)
    out["sunday by coin"]=pd.DataFrame(t).round(3)
    t=[]
    for k,s in sun.groupby("year"):
        sl,tt,n=reg(s,"z","x2"); f=s[s.z<0]; sl2,tt2,n2=reg(f,"z","x2")
        t.append({"year":k,"t2_all":tt,"n":n,"t2_fall":tt2,"nfall":n2})
    out["sunday by year"]=pd.DataFrame(t).round(3)
    # quintiles of z on Sunday
    s=sun.dropna(subset=["z","x2"]).copy(); s["q"]=pd.qcut(s.z,5,labels=False)
    out["sunday z quintile"]=s.groupby("q").agg(zmean=("z","mean"),x1=("x1","mean"),x2=("x2","mean"),x3=("x3","mean"),n=("x2","size")).round(4)
    # volume interaction: sunday+saturday volume relative
    s=sun.dropna(subset=["z","x2","vrel"]).copy(); s["lowvol"]=s.vrel<s.vrel.median()
    t=[]
    for k,g in s.groupby("lowvol"):
        sl,tt,n=reg(g,"z","x2"); sl1,tt1,_=reg(g,"z","x1")
        t.append({"lowvol":k,"t1":tt1,"t2":tt,"n":n})
    out["sunday by vol"]=pd.DataFrame(t).round(3)
    # weekend 2-day (sat+sun) return as situation
    return out
