def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(pd.Series(b["close"].values).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            width=(b["high"]-b["low"])/c.shift(1)/sd
            loc=(b["high"]-c)/(b["high"]-b["low"])
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"reg":b["regime"],
                "width":width,"loc":loc,"f1":c.shift(-1)/c-1-mu,"raw1":c.shift(-1)/c-1,
                "tr60":c/c.shift(60)-1,"day":ts.dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["width","loc","f1"])
    D["s"]=D.width*(D["loc"]-0.5)*2   # positive = wide low close, negative = wide high close
    def summ(g):
        ds=g.groupby("day").f1.sum()
        n=len(ds)
        return pd.Series({"cases":len(g),"days":n,"f1":g.f1.mean(),
            "t_day":ds.mean()/(ds.std()/np.sqrt(n)) if n>2 else np.nan})
    P=D[D.reg.isin(["mean_reversion","unknown"])].copy()
    out={}
    out["inprof all"]=summ(P)
    P["sb"]=pd.cut(P.s,[-100,-2,-1,-0.3,0.3,1,2,100])
    out["inprof by signed score s"]=P.groupby("sb").apply(summ)
    rho,p=stats.spearmanr(P.s,P.f1)
    out["inprof spearman s vs f1"]=pd.Series({"rho":rho,"p":p,"n":len(P)})
    # relative to in-profile mean that day-type: f1 minus inprof mean
    pm=P.f1.mean()
    hi=P[P.s<=-1]; lo=P[P.s>=1]
    out["inprof s<=-1 (wide high close) by year"]=hi.groupby("year").apply(summ)
    out["inprof s>=1 (wide low close) by year"]=lo.groupby("year").apply(summ)
    out["inprof high-close minus inprof mean"]=pd.Series({"diff":hi.f1.mean()-pm,
        "welch_t":stats.ttest_ind(hi.f1,P[(P.s>-1)&(P.s<1)].f1,equal_var=False).statistic,
        "n_hi":len(hi)})
    out["inprof low-close minus mid"]=pd.Series({"diff":lo.f1.mean()-P[(P.s>-1)&(P.s<1)].f1.mean(),
        "welch_t":stats.ttest_ind(lo.f1,P[(P.s>-1)&(P.s<1)].f1,equal_var=False).statistic,"n_lo":len(lo)})
    # outside profile, wide low close, by in-window 60d trend
    O=D[(D.reg=="chop")&(D["loc"]>=0.8)&(D.width>=2)].dropna(subset=["tr60"])
    O["tb"]=pd.cut(O.tr60,[-10,-0.1,0.1,100])
    out["outside prof wide low close by 60d trend"]=O.groupby("tb").apply(summ)
    return out
