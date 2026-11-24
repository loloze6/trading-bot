def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 30: continue
            o,h,l,c = b.open,b.high,b.low,b.close
            rng = (h-l)
            rr = rng / rng.rolling(20).mean()
            flat = 1 - (c-o).abs()/rng.replace(0,np.nan)
            clv = (c-l)/rng.replace(0,np.nan)
            body = (c-o)/rng.replace(0,np.nan)
            p5 = c/c.shift(5)-1
            p20 = c/c.shift(20)-1
            r1 = c/c.shift(1)-1
            vol20 = r1.rolling(20).std()
            vrat = vol20 / r1.rolling(60, min_periods=30).std()
            f5 = c.shift(-5)/c-1
            f1 = c.shift(-1)/c-1
            ts = pd.to_datetime(b.timestamp)
            d = pd.DataFrame(dict(coin=coin,win=w,pos=np.arange(len(b)),rr=rr,flat=flat,clv=clv,body=body,
                p5=p5,p20=p20,r1=r1,vol20=vol20,vrat=vrat,f5=f5,f1=f1,
                day=ts.dt.floor("D"),wd=ts.dt.weekday,yr=ts.dt.year,fc=b.forecast))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    g = D[(D.pos%5==0)&D.f5.notna()].copy()
    drift = g.groupby("coin").f5.mean()
    sd = g.groupby("coin").f5.std()
    g["u5"] = g.f5 - g.coin.map(drift)
    g["s5"] = g.u5 / g.coin.map(sd)
    def ct(x):
        x = x.dropna(subset=["u5"])
        n=len(x)
        if n<5: return pd.Series(dict(n=n))
        m=x.u5.mean()
        ds=(x.u5-m).groupby(x.day).sum()
        se=np.sqrt((ds**2).sum())/n
        return pd.Series(dict(n=n,days=len(ds),mean_u5=m,str=x.s5.mean(),t=m/se if se>0 else np.nan))
    out={}
    out["drift_by_coin"]=pd.DataFrame(dict(drift=drift,usual=sd))
    for f in ["rr","flat","clv","body","p5","p20","r1","vol20","vrat"]:
        q=g.dropna(subset=[f]).copy()
        q["b"]=q.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        out["q_"+f]=q.groupby("b").apply(ct)
    out["weekday"]=g.groupby("wd").apply(ct)
    out["year"]=g.groupby("yr").apply(ct)
    # wide days (rr>=1.5) by sign of p5 and clv tercile
    wd_=g[g.rr>=1.5].copy()
    wd_["up5"]=wd_.p5>0
    wd_["clvb"]=pd.cut(wd_.clv,[0,1/3,2/3,1.0001],labels=["lowclose","mid","highclose"],include_lowest=True)
    out["wide_by_p5_clv"]=wd_.groupby(["up5","clvb"]).apply(ct)
    # wide flat days, by p5 sign (all bars counted here, not grid -> use grid anyway)
    wf=g[(g.rr>=1.5)&(g.flat>=0.8)].copy(); wf["up5"]=wf.p5>0
    out["wideflat_by_p5"]=wf.groupby("up5").apply(ct)
    # spearman on all grid
    sp={}
    for f in ["rr","flat","clv","body","p5","p20","r1","vol20","vrat"]:
        q=g.dropna(subset=[f,"s5"])
        sp[f]=stats.spearmanr(q[f],q.s5)[0]
    out["spearman_s5"]=pd.Series(sp)
    # 1-day horizon all bars
    a=D.dropna(subset=["f1","clv","r1"]).copy()
    a["u1"]=a.f1-a.coin.map(D.groupby("coin").f1.mean())
    a["clvb"]=a.groupby("coin").clv.transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["clv_q_next1d"]=a.groupby("clvb").u1.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    return out
