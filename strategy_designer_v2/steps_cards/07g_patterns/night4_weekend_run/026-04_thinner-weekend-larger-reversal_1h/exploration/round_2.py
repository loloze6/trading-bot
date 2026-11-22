def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b[["timestamp","close","volume"]].copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            b=b.sort_values("ts").reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values; n=len(c)
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            hr.append(pd.DataFrame({"coin":coin,"w":w,"year":b.ts.dt.year,"hour":b.ts.dt.hour,"wd":b.ts.dt.weekday,"r":r1}))
            idx=np.where(b.ts.dt.hour.values==23)[0]
            for i in idx:
                if i-167<0 or i+48>=n: continue
                if (b.ts[i+48]-b.ts[i]).total_seconds()!=48*3600 or (b.ts[i]-b.ts[i-167]).total_seconds()!=167*3600: continue
                vr=v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)
                rows.append((coin,w,b.ts[i].year,b.ts[i].weekday(),c[i]/c[i-48]-1,c[i+48]/c[i]-1,c[i+24]/c[i]-1,vr))
    d=pd.DataFrame(rows,columns=["coin","w","year","wd","past","fut","fut24","vr"])
    out={}
    d["pz"]=d.past/d.groupby("coin")["past"].transform("std")
    d["fz"]=(d.fut-d.groupby("coin")["fut"].transform("mean"))/d.groupby("coin")["fut"].transform("std")
    d["f24z"]=(d.fut24-d.groupby("coin")["fut24"].transform("mean"))/d.groupby("coin")["fut24"].transform("std")
    d["pzw"]=d.pz.clip(-3,3); d["fzw"]=d.fz.clip(-3,3)
    # vol ratio tercile within coin and weekday
    d["vq"]=d.groupby(["coin","wd"]).vr.transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    res=[]
    for (wd,q),g in d.groupby(["wd","vq"]):
        s=stats.linregress(g.pzw,g.fzw); res.append((wd,q,len(g),g.vr.mean(),s.slope,s.slope/s.stderr))
    out["winsorised slope fut48 on past48 by weekday x volratio tercile (0=thin)"]=pd.DataFrame(res,columns=["wd","vq","n","vr","b","t"])
    sun=d[(d.wd==6)]
    # continuous interaction on Sunday
    import numpy.linalg as la
    lv=np.log(sun.vr); lvz=(lv-lv.mean())/lv.std()
    X=np.c_[np.ones(len(sun)),sun.pzw,lvz,sun.pzw*lvz]; y=sun.fzw.values
    beta=la.lstsq(X,y,rcond=None)[0]; e=y-X@beta; cov=la.inv(X.T@X)*(e@e)/(len(y)-4)
    out["Sunday fz ~ pz + logvr_z + pz*logvr_z (coef,t)"]=pd.DataFrame({"b":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","pz","lvr","pz*lvr"])
    thin=sun[sun.vq==0]
    res=[]
    for k,g in thin.groupby("year"):
        if len(g)>20: s=stats.linregress(g.pzw,g.fzw); res.append((k,len(g),s.slope,s.slope/s.stderr))
    out["Sunday thin tercile slope by year"]=pd.DataFrame(res,columns=["year","n","b","t"])
    res=[]
    for k,g in thin.groupby("coin"):
        s=stats.linregress(g.pzw,g.fzw); res.append((k,len(g),s.slope,s.slope/s.stderr))
    out["Sunday thin tercile slope by coin"]=pd.DataFrame(res,columns=["coin","n","b","t"])
    # signed-move mean reversal in thin tercile: mean of -sign(past)*fut
    thin=thin.copy(); thin["rev"]=-np.sign(thin.past)*(thin.fut-d.fut.mean())
    out["Sunday thin: mean -sign(past)*fut48 dev, t, n"]=pd.Series({"mean":thin.rev.mean(),"t":thin.rev.mean()/(thin.rev.std()/np.sqrt(len(thin))),"n":len(thin)})
    H=pd.concat(hr).dropna()
    H["rz"]=H.r/H.groupby("coin").r.transform("std")
    e=H[H.hour.isin([20,21])]
    g=e.groupby("year").rz.agg(["mean","std","size"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["hours 20-21 return z by year"]=g[["mean","t","size"]]
    g=e.groupby("coin").rz.agg(["mean","std","size"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["hours 20-21 return z by coin"]=g[["mean","t","size"]]
    g=e.groupby("wd").rz.agg(["mean","std","size"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["hours 20-21 return z by weekday"]=g[["mean","t","size"]]
    # mean raw return hours 20-21 summed per day, pct
    out["hours 20-21 mean raw hourly return"]=e.groupby("coin").r.mean()
    return out
