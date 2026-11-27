def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            n=len(b); rng=h-l
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            agit=(b["regime"]!="chop").values
            ts=pd.to_datetime(b["timestamp"])
            rr=rng/c
            rr20=pd.Series(rr).rolling(20).mean().values
            r30=np.r_[[np.nan]*30,c[30:]/c[:-30]-1] if n>30 else np.full(n,np.nan)
            for t in range(n):
                f17=c[t+7]/c[t+1]-1 if t+7<n else np.nan
                f1=c[t+1]/c[t]-1 if t+1<n else np.nan
                rows.append(dict(coin=coin,w=w,pos=t,cl=cl[t],agit=agit[t],f17=f17,f1=f1,
                    day=ts.iloc[t].normalize(),yr=ts.iloc[t].year,wrel=rr[t]/rr20[t] if rr20[t]>0 else np.nan,r30=r30[t]))
    d=pd.DataFrame(rows)
    out={}
    # grid offset robustness: 7 offsets, mean over all of them, clustered by day
    res=[]
    for off in range(7):
        g=d[(d.pos%7==off)].copy()
        dr=g.groupby("coin").f17.mean()
        g["u"]=g.f17-g.coin.map(dr)
        g=g[g.agit].dropna(subset=["u","cl"])
        g["sc"]=(g.cl-0.5)*2  # signed score, +1 at high, -1 at low
        for name,sub in [("low<.2",g[g.cl<0.2]),("high>=.8",g[g.cl>=0.8])]:
            dev=sub.u-0
            m=dev.mean(); s=dev.groupby(sub.day).sum()
            se=np.sqrt((s-s.groupby(level=0).size()*0).pow(2).sum())/len(dev)
            # proper: deviations from mean
            s2=(dev-m).groupby(sub.day).sum(); se=np.sqrt((s2**2).sum())/len(dev)
            res.append(dict(off=off,grp=name,mean=m,t=m/se,n=len(dev),days=sub.day.nunique()))
        # graded slope: regression of u on cl, clustered
        x=g.cl-g.cl.mean(); beta=(x*g.u).sum()/(x*x).sum()
        e=(g.u-g.u.mean()-beta*x)*x; s=e.groupby(g.day).sum(); se=np.sqrt((s**2).sum())/(x*x).sum()
        res.append(dict(off=off,grp="slope",mean=beta,t=beta/se,n=len(g),days=g.day.nunique()))
    R=pd.DataFrame(res)
    out["by offset clustered"]=R
    out["avg over offsets"]=R.groupby("grp")[["mean","t"]].mean()
    # all bars (overlapping) for splits; low close agit by year and by window
    dr=d.groupby("coin").f17.mean(); d["u"]=d.f17-d.coin.map(dr)
    a=d[d.agit].dropna(subset=["u","cl"])
    lo=a[a.cl<0.2]; hi=a[a.cl>=0.8]
    out["low close u17 by year (overlapping)"]=lo.groupby("yr").u.agg(["mean","count"])
    out["high close u17 by year (overlapping)"]=hi.groupby("yr").u.agg(["mean","count"])
    out["low close u17 by window"]=lo.groupby("w").u.agg(["mean","count"])
    # by 30d trend in agit
    a=a.assign(tr=pd.cut(a.r30,[-9,-0.1,0.1,99],labels=["fall","chop","rise"]),
               wq=pd.qcut(a.wrel,3,labels=["narrow","mid","wide"]),
               cb=pd.cut(a.cl,[-.01,.2,.8,1.01],labels=["lo","mid","hi"]))
    out["u17 by trend x close (agit, overl.)"]=a.groupby(["tr","cb"]).u.agg(["mean","count"]).unstack()
    out["u17 by width x close (agit, overl.)"]=a.groupby(["wq","cb"]).u.agg(["mean","count"]).unstack()
    out["f1 by width x close (agit)"]=a.groupby(["wq","cb"]).f1.agg(["mean","count"]).unstack()
    return out
