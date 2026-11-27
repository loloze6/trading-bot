def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            rr.append(pd.Series(c[1:]/c[:-1]-1))
        drift[coin]=pd.concat(rr).mean()
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); h=b["high"].values.astype(float); l=b["low"].values.astype(float)
            rng=pd.Series(h-l); mr=rng.rolling(20).mean()
            rm=(rng/mr).values
            cl=np.where(h>l,(c-l)/np.where(h>l,h-l,1),np.nan)
            r60=pd.Series(c).pct_change(60).values
            r1=pd.Series(c).pct_change(1).values
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for t in range(n-1):
                d={"coin":coin,"w":w,"year":ts.iloc[t].year,
                   "regime":b["regime"].iloc[t],"fc":b["forecast"].iloc[t],
                   "rm":rm[t],"cl":cl[t],"r60":r60[t],"r1":r1[t],"day":str(ts.iloc[t])[:10]}
                for H in (1,2,3,5):
                    d[f"u{H}"]=-(c[t+H]/c[t]-1-((1+drift[coin])**H-1)) if t+H<n else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    def tstat(s,days):
        if len(s)<5: return np.nan
        m=s.mean()
        g=(s-m).groupby(days).sum(); D=len(g)
        if D<3: return np.nan
        se=np.sqrt((g**2).sum()*D/(D-1))/len(s)
        return m/se if se>0 else np.nan
    def summ(sub):
        out={"n":len(sub)}
        for H in (1,2,3,5):
            s=sub[f"u{H}"].dropna()
            out[f"m{H}"]=s.mean() if len(s) else np.nan
            out[f"t{H}"]=tstat(s,sub.loc[s.index,"day"])
        return pd.Series(out)
    def q(x,k,lab):
        return pd.qcut(x.rank(method="first"),k,labels=lab)
    cases=df[df.fc<0].copy()
    res={}
    res["cases_all"]=summ(cases)
    res["by_regime_all_bars"]=df.groupby("regime").apply(summ)
    res["cases_by_coin"]=cases.groupby("coin").apply(summ)
    res["cases_by_window"]=cases.groupby("w").apply(summ)
    res["cases_by_year"]=cases.groupby("year").apply(summ)
    cases["trend"]=pd.cut(cases.r60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    res["cases_by_trend"]=cases.groupby("trend").apply(summ)
    cases["fq"]=q(cases.fc,4,["q1strong","q2","q3","q4weak"])
    res["cases_by_fc_quart"]=cases.groupby("fq").apply(summ)
    cases["rmq"]=q(cases.rm,4,["r1","r2","r3","r4wide"])
    res["cases_by_rm_quart"]=cases.groupby("rmq").apply(summ)
    cases["clq"]=q(cases.cl,4,["c1","c2","c3","c4high"])
    res["cases_by_cl_quart"]=cases.groupby("clq").apply(summ)
    cases["upday"]=np.where(cases.r1>0,"up","down")
    res["cases_by_dayreturn_sign"]=cases.groupby("upday").apply(summ)
    pat=df[(df.rm>=1)&(df.cl>=0.5)]
    res["pattern_by_regime"]=pat.groupby("regime").apply(summ)
    narrow=df[(df.rm<1)&(df.cl>=0.5)&(df.regime!="chop")]
    res["agitated_narrow_high"]=summ(narrow)
    return res
