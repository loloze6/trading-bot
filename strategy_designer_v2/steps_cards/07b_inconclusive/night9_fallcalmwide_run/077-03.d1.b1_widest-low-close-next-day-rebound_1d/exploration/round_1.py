def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values; allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            rng=(b["high"]-b["low"])/c.shift(1)
            width=rng/sd
            loc=(b["high"]-c)/(b["high"]-b["low"])
            for h in (1,2,3,5):
                b[f"f{h}"]=c.shift(-h)/c-1-h*mu
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "reg":b["regime"],"alloc":b["postRebalance_current_allocation"],"fc":b["forecast"],
                "width":width,"loc":loc,"f1":b["f1"],"f2":b["f2"],"f3":b["f3"],"f5":b["f5"],
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    out["regime counts"]=D["reg"].value_counts()
    inprof=D[D.reg.isin(["mean_reversion","unknown"])].dropna(subset=["width","loc","f1"])
    cases=D[(D.alloc>0)].dropna(subset=["f1"])
    def summ(g):
        return pd.Series({"n":len(g),"f1":g.f1.mean(),"t1":g.f1.mean()/(g.f1.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                          "f2":g.f2.mean(),"f3":g.f3.mean(),"f5":g.f5.mean()})
    out["cases all"]=summ(cases)
    out["cases by coin"]=cases.groupby("coin").apply(summ)
    out["cases by year"]=cases.groupby("year").apply(summ)
    med=cases.fc.median()
    out["cases by fc half"]=cases.groupby(cases.fc>med).apply(summ)
    # in-profile, all bars, by loc bins and width
    inprof=inprof.assign(lb=pd.cut(inprof["loc"],[-0.01,0.2,0.4,0.6,0.8,1.01]),
                         wb=pd.cut(inprof["width"],[0,1,2,3,100]))
    out["inprof by loc (1=low close)"]=inprof.groupby("lb").apply(summ)
    out["inprof low-close by width"]=inprof[inprof["loc"]>=0.8].groupby("wb").apply(summ)
    out["inprof high-close by width"]=inprof[inprof["loc"]<=0.2].groupby("wb").apply(summ)
    # all bars any profile low close wide
    allb=D.dropna(subset=["width","loc","f1"])
    out["all profiles low-close wide>=2 by reg"]=allb[(allb["loc"]>=0.8)&(allb.width>=2)].groupby("reg").apply(summ)
    return out
