def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            c=b["close"].values
            rr.append(pd.Series(c[1:]/c[:-1]-1))
        drift[coin]=pd.concat(rr).mean()
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            rng=pd.Series(h-l); mr=rng.rolling(20).mean()
            rm=(rng/mr).values
            cl=np.where(h>l,(c-l)/(h-l),np.nan)
            r60=pd.Series(c).pct_change(60).values
            n=len(b)
            for t in range(n-1):
                d={"coin":coin,"w":w,"year":pd.Timestamp(b["timestamp"].iloc[t]).year,
                   "regime":b["regime"].iloc[t],"fc":b["forecast"].iloc[t],
                   "rm":rm[t],"cl":cl[t],"r60":r60[t],"day":str(b["timestamp"].iloc[t])[:10]}
                for H in (1,2,3,5):
                    d[f"u{H}"]=-(c[t+H]/c[t]-1-((1+drift[coin])**H-1)) if t+H<n else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    def tstat(s,days):
        g=s.groupby(days).sum(); D=len(g)
        if D<3: return np.nan
        return s.mean()/ (np.sqrt((g-s.mean()*s.groupby(days).count()).pow(2).sum()*D/(D-1))/len(s))
    def summ(sub):
        out={}
        out["n"]=len(sub)
        for H in (1,2,3,5):
            s=sub[f"u{H}"].dropna()
            out[f"m{H}"]=s.mean(); out[f"t{H}"]=tstat(s,sub.loc[s.index,"day"])
        return pd.Series(out)
    cases=df[df.fc<0].copy()
    res={}
    res["cases_all"]=summ(cases)
    res["by_regime_all_bars"]=df.groupby("regime").apply(summ)
    res["cases_by_coin"]=cases.groupby("coin").apply(summ)
    res["cases_by_window"]=cases.groupby("w").apply(summ)
    cases["trend"]=pd.cut(cases.r60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    res["cases_by_trend"]=cases.groupby("trend").apply(summ)
    cases["fq"]=pd.qcut(cases.fc,4,labels=["q1strong","q2","q3","q4weak"])
    res["cases_by_fc_quart"]=cases.groupby("fq").apply(summ)
    cases["rmq"]=pd.qcut(cases.rm,4,labels=["r1","r2","r3","r4wide"])
    res["cases_by_rm_quart"]=cases.groupby("rmq").apply(summ)
    cases["clq"]=pd.qcut(cases.cl,4,labels=["c1","c2","c3","c4high"])
    res["cases_by_cl_quart"]=cases.groupby("clq").apply(summ)
    # same pattern on calm days and narrow days
    pat=df[(df.rm>=1)&(df.cl>=0.5)]
    res["pattern_by_regime"]=pat.groupby("regime").apply(summ)
    narrow=df[(df.rm<1)&(df.cl>=0.5)&(df.regime!="chop")]
    res["agitated_narrow_high"]=summ(narrow)
    return res
