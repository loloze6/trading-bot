def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        r2=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-2,2)
            r2+=list(c[idx+2]/c[idx]-1)
        drift[coin]=np.mean(r2); usual[coin]=np.std(r2,ddof=1)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]
            ret=c.pct_change()
            vr=ret.rolling(20).std()/ret.rolling(60).std()
            r14=c/c.shift(14)-1
            fwd=c.shift(-2)/c-1
            r1=c.shift(-1)/c-1
            df=pd.DataFrame({"coin":coin,"win":w,"day":ts.dt.floor("D"),"year":ts.dt.year,"wd":ts.dt.weekday,
                             "fc":b["forecast"],"vr":vr,"r14":r14,"fwd":fwd,"r1":r1})
            df=df[(df.wd==4)&df.fwd.notna()]
            df["unus"]=df.fwd-drift[coin]
            rows.append(df)
    d=pd.concat(rows)
    def summ(x):
        if len(x)<3: return pd.Series({"n":len(x)})
        g=x.groupby("day").unus.sum(); days=len(g)
        m=x.unus.mean(); se=np.sqrt((g-g.mean()*0).pow(2).sum())/len(x) if False else None
        # clustered t: sum per day deviations
        dev=(x.unus-m).groupby(x.day).sum()
        se=np.sqrt((dev**2).sum())/len(x)
        return pd.Series({"n":len(x),"days":days,"mean":m,"t":m/se if se>0 else np.nan,"hit":(x.unus>0).mean()})
    out={}
    cases=d[d.fc>=2]
    out["cases"]=summ(cases)
    hv=d[d.vr>1]
    out["volFri_by_sign14"]=hv.groupby(np.sign(hv.r14)).apply(summ)
    lv=d[d.vr<=1]
    out["calmFri_by_sign14"]=lv.groupby(np.sign(lv.r14)).apply(summ)
    out["allFri_by_vrbin"]=d.dropna(subset=["vr"]).groupby(pd.qcut(d.vr,5)).apply(summ)
    out["allFri_by_r14bin"]=d.dropna(subset=["r14"]).groupby(pd.qcut(d.r14,5)).apply(summ)
    out["cases_by_fcq"]=cases.groupby(pd.qcut(cases.fc,4,duplicates="drop")).apply(summ)
    out["cases_by_r14q"]=cases.groupby(pd.qcut(cases.r14,4)).apply(summ)
    out["cases_by_vrq"]=cases.groupby(pd.qcut(cases.vr,4)).apply(summ)
    out["cases_by_coin"]=cases.groupby("coin").apply(summ)
    out["cases_by_year"]=cases.groupby("year").apply(summ)
    # all days, vol regime, by weekday
    out["vol_rising_by_wd_proxy"]=summ(d[(d.vr>1)&(d.r14>0)&(d.fc<2)])
    out["usual"]=pd.Series(usual)
    out["drift"]=pd.Series(drift)
    return out
