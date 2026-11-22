def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b[["timestamp","close","volume"]].copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            b=b.sort_values("ts").reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            hh=pd.DataFrame({"coin":coin,"hour":b.ts.dt.hour,"wd":b.ts.dt.weekday,"r":r1})
            # past 24h abs return for vol level
            hr.append(hh)
            idx=np.where(b.ts.dt.hour.values==23)[0]
            for i in idx:
                if i-48<0 or i+48>=n: continue
                # check contiguity
                if (b.ts[i+48]-b.ts[i]).total_seconds()!=48*3600 or (b.ts[i]-b.ts[i-48]).total_seconds()!=48*3600: continue
                vratio=b.volume.values[i-47:i+1].mean()/max(b.volume.values[max(0,i-167):i-47].mean(),1e-12)
                rows.append((coin,w,b.ts[i].weekday(),c[i]/c[i-48]-1,c[i+48]/c[i]-1,c[i+24]/c[i]-1,vratio))
    d=pd.DataFrame(rows,columns=["coin","w","wd","past","fut","fut24","vr"])
    out={}
    # per weekday: slope of fut on past (in z by coin)
    sd=d.groupby("coin")["fut"].transform("std")
    d["pz"]=d.past/d.groupby("coin")["past"].transform("std"); d["fz"]=(d.fut-d.groupby("coin")["fut"].transform("mean"))/sd
    d["f24z"]=(d.fut24-d.groupby("coin")["fut24"].transform("mean"))/d.groupby("coin")["fut24"].transform("std")
    res=[]
    for wd,g in d.groupby("wd"):
        s=stats.linregress(g.pz,g.fz); s2=stats.linregress(g.pz,g.f24z)
        res.append((wd,len(g),s.slope,s.slope/s.stderr,s2.slope,s2.slope/s2.stderr))
    out["slope fut48z/fut24z on past48z by weekday of 23h bar (6=Sun)"]=pd.DataFrame(res,columns=["wd","n","b48","t48","b24","t24"])
    sun=d[d.wd==6]
    res=[]
    for coin,g in sun.groupby("coin"):
        s=stats.linregress(g.pz,g.fz); res.append((coin,len(g),s.slope,s.slope/s.stderr))
    out["Sunday slope by coin"]=pd.DataFrame(res,columns=["coin","n","b","t"])
    sun=sun.copy(); sun["q"]=pd.qcut(sun.groupby("coin").pz.rank(pct=True),5,labels=False)
    out["Sunday by past quintile: mean fut48 z"]=sun.groupby("q").agg(n=("fz","size"),fz=("fz","mean"),fut=("fut","mean"),past=("past","mean"))
    sun["vq"]=pd.qcut(sun.groupby("coin").vr.rank(pct=True),3,labels=False)
    res=[]
    for q,g in sun.groupby("vq"):
        s=stats.linregress(g.pz,g.fz); res.append((q,len(g),g.vr.mean(),s.slope,s.slope/s.stderr))
    out["Sunday slope by weekend/weekday vol ratio tercile"]=pd.DataFrame(res,columns=["vq","n","vr","b","t"])
    H=pd.concat(hr).dropna()
    H["rz"]=H.r/H.groupby("coin").r.transform("std")
    g=H.groupby("hour").rz.agg(["mean","std","size"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["hourly return z by hour"]=g[["mean","t","size"]]
    g=H.groupby("wd").rz.agg(["mean","std","size"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["hourly return z by weekday"]=g[["mean","t","size"]]
    return out
