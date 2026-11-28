def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); rng=(b["high"]-b["low"]).astype(float)
            mr=rng.rolling(30,min_periods=10).mean()
            sc=(c-c.shift(1))/mr
            ret1=c/c.shift(1)-1
            sd30=ret1.rolling(30,min_periods=10).std()
            zs=ret1/sd30
            f=b["forecast"].astype(float)
            fd=f.diff()
            prof=(b["regime"]=="unknown")
            n=len(b)
            for h in [1,3]:
                fwd=c.shift(-h)/c-1
                for off in range(h):
                    for i in range(off,n,h):
                        if pd.isna(fwd.iloc[i]) or pd.isna(sc.iloc[i]): continue
                        rows.append(dict(coin=coin,w=w,h=h,off=off,i=i,sc=sc.iloc[i],zs=zs.iloc[i],f=f.iloc[i],
                                         fd=fd.iloc[i],prof=bool(prof.iloc[i]),r=fwd.iloc[i],
                                         day=str(b["timestamp"].iloc[i])[:10],yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    p=d[d.prof].copy()
    p=p.join(p.groupby(["coin","h","off"]).r.mean().rename("base"),on=["coin","h","off"]); p["u"]=p.r-p.base
    def tday(x):
        s=x.groupby("day").u.sum(); m=x.u.mean(); G=len(s)
        if G<3: return pd.Series(dict(mean=m,n=len(x),days=G,t=np.nan))
        dev=x.u-m; sd=dev.groupby(x.day).sum()
        se=np.sqrt((sd**2).sum())/len(x)*np.sqrt(G/(G-1))
        return pd.Series(dict(mean=m,n=len(x),days=G,t=m/se))
    p["bk"]=pd.cut(p.sc,[-99,-0.5,0,0.25,0.5,0.75,99])
    out["h3_by_offset_bucket"]=p[p.h==3].groupby(["off","bk"],observed=True).apply(tday)
    out["h3_allofs_bucket"]=p[p.h==3].groupby("bk",observed=True).apply(tday)
    out["h1_bucket"]=p[p.h==1].groupby("bk",observed=True).apply(tday)
    out["mean_raw_h3_profile"]=p[p.h==3].r.mean()
    # forecast-case like: forecast negative and dropped
    q=p[(p.h==3)&(p.fd<=-2)]
    out["fcase_h3"]=tday(q)
    q2=q.copy(); q2["sbk"]=pd.cut(q2.sc,[0,0.25,0.5,99])
    out["fcase_h3_by_sc"]=q2.groupby("sbk",observed=True).apply(tday)
    up=p[(p.h==3)&(p.sc>0)].copy()
    out["corr_f_sc_up"]=up[["f","sc","zs"]].corr()
    # graded by z of return vs 30d std
    up["zbk"]=pd.cut(up.zs,[0,0.5,1,1.5,99])
    out["up_h3_by_zs"]=up.groupby("zbk",observed=True).apply(tday)
    big=p[(p.h==3)&(p.sc>0.25)]
    out["big_up_h3_by_coin"]=big.groupby("coin").apply(tday)
    out["big_up_h3_by_year"]=big.groupby("yr").apply(tday)
    return out
