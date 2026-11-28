def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); rng=(b["high"]-b["low"]).astype(float)
            mr=rng.rolling(30,min_periods=10).mean()
            sc=(c-c.shift(1))/mr
            prof=(b["regime"]=="unknown")
            n=len(b)
            for h in [1,2,3,5,10]:
                fwd=c.shift(-h)/c-1
                for i in range(0,n,h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(sc.iloc[i]): continue
                    rows.append(dict(coin=coin,w=w,h=h,i=i,sc=sc.iloc[i],prof=bool(prof.iloc[i]),r=fwd.iloc[i],
                                     yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    out={}
    p=d[d.prof]
    # baseline per coin,h in profile
    base=p.groupby(["coin","h"]).r.mean().rename("base")
    p=p.join(base,on=["coin","h"]); p["u"]=p.r-p.base
    p["bk"]=pd.cut(p.sc,[-99,-1.5,-0.75,-0.25,0,0.25,0.75,1.5,99])
    g=p.groupby(["h","bk"],observed=True).u.agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan])
    g.columns=["mean_u","n","t"]
    out["profile_bucket_by_h"]=g
    # outside profile, h=3
    q=d[~d.prof & (d.h==3)].copy()
    q=q.join(q.groupby("coin").r.mean().rename("base"),on="coin"); q["u"]=q.r-q.base
    q["bk"]=pd.cut(q.sc,[-99,-1.5,-0.75,-0.25,0,0.25,0.75,1.5,99])
    out["outside_h3"]=q.groupby("bk",observed=True).u.agg(["mean","count"])
    # correlation sc vs u by h in profile
    cr=[]
    for h,gg in p.groupby("h"):
        r,pv=stats.spearmanr(gg.sc,gg.u); cr.append(dict(h=h,rho=r,n=len(gg),p=pv,mean_raw=gg.r.mean()))
    out["spearman_profile"]=pd.DataFrame(cr)
    up=p[(p.h==3)&(p.sc>0)]
    out["up_h3_by_coin"]=up.groupby("coin").u.agg(["mean","count"])
    out["up_h3_by_year"]=up.groupby("yr").u.agg(["mean","count"])
    dn=p[(p.h==3)&(p.sc<0)]
    out["down_h3_by_coin"]=dn.groupby("coin").u.agg(["mean","count"])
    out["profile_share"]=d[d.h==1].groupby("coin").prof.mean()
    return out
