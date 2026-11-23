def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            raw=b.get("debug_info.components.low_prox.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(b)
            for H in (5,10,20):
                for i in range(0,n-H,H):
                    rows.append(dict(coin=coin,w=w,H=H,i=i,yr=yr[i],af=abs(f[i]),raw=raw[i],
                                     ret=c[i+H]/c[i]-1,
                                     past20=c[i]/c[i-20]-1 if i>=20 else np.nan,
                                     ts=b["timestamp"].iloc[i]))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","H"])["ret"].transform("mean")
    d["sg"]=-(d["ret"]-d["drift"])
    d["dist"]=1/d["raw"]-1   # percent distance above low
    d["logprox"]=-np.log1p(d["dist"].clip(lower=0))
    out={}
    def slope(g,x):
        g=g.dropna(subset=[x,"sg"])
        if len(g)<10 or g[x].std()==0: return pd.Series(dict(n=len(g)))
        r=stats.linregress(g[x],g["sg"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    for x in ("af","raw","logprox"):
        out[f"slope_{x}_byH"]=d.groupby("H").apply(lambda g: slope(g,x))
    # within-year demeaned slope
    d["sg_dm"]=d["sg"]-d.groupby(["H","yr"])["sg"].transform("mean")
    def slope_dm(g):
        g=g.dropna(subset=["af","sg_dm"]); r=stats.linregress(g["af"],g["sg_dm"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    out["within_year_slope_byH"]=d.groupby("H").apply(slope_dm)
    # top quintile per H: mean, day-clustered t, by year, by coin
    res=[];yrs=[];cns=[]
    for H in (5,10,20):
        dh=d[d.H==H].copy()
        thr=dh["af"].quantile(0.8)
        top=dh[dh.af>=thr]
        day=top.groupby(pd.to_datetime(top.ts).dt.floor("D"))["sg"].sum()
        # day-clustered t: sum per day / n
        nn=len(top); m=top.sg.mean()
        se=np.sqrt(((day - top.groupby(pd.to_datetime(top.ts).dt.floor("D"))["sg"].size()*m)**2).sum())/nn
        res.append(dict(H=H,n=nn,days=len(day),mean=m,t_cl=m/se,rest_mean=dh[dh.af<thr].sg.mean()))
        g=top.groupby("yr")["sg"].agg(["size","mean"]); g["H"]=H; yrs.append(g.reset_index())
        g=top.groupby("coin")["sg"].agg(["size","mean"]); g["H"]=H; cns.append(g.reset_index())
    out["top_q_summary"]=pd.DataFrame(res)
    out["top_q_by_year_20"]=yrs[2]
    out["top_q_by_coin_20"]=cns[2]
    out["top_q_by_coin_10"]=cns[1]
    # buckets of raw distance at 20 and 10
    for H in (10,20):
        dh=d[d.H==H].copy()
        dh["db"]=pd.cut(dh["dist"],[-1,0.05,0.15,0.3,0.6,1.5,1e9])
        out[f"dist_bucket_{H}"]=dh.groupby("db").agg(n=("sg","size"),sg=("sg","mean"),sd=("sg","std"))
    # top quintile split by past 20d return
    dh=d[d.H==20].copy(); thr=dh.af.quantile(0.8)
    t=dh[dh.af>=thr].copy(); t["pd"]=np.where(t.past20<0,"down","up")
    out["top20_by_past20"]=t.groupby("pd")["sg"].agg(["size","mean","std"])
    return out
