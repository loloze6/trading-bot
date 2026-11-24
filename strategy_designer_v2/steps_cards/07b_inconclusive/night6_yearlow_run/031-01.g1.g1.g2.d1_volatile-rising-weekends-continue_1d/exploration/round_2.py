def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        r2=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-2,2)
            r2+=list(c[idx+2]/c[idx]-1)
        drift[coin]=float(np.mean(r2)); usual[coin]=float(np.std(r2,ddof=1))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"].astype(float)
            ret=c.pct_change()
            vr=ret.rolling(20).std()/ret.rolling(60).std()
            r14=c/c.shift(14)-1
            fwd=c.shift(-2)/c-1
            pos=np.arange(len(b))
            df=pd.DataFrame({"coin":coin,"win":w,"day":ts.dt.floor("D").values,"year":ts.dt.year.values,
                             "wd":ts.dt.weekday.values,"fc":b["forecast"].values,"vr":vr.values,
                             "r14":r14.values,"fwd":fwd.values,"grid":(pos%2==0)})
            df=df[df.fwd.notna()]
            df["unus"]=df.fwd-drift[coin]
            df["str"]=df.unus/usual[coin]
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    def summ(x):
        x=x.dropna(subset=["unus"])
        if len(x)<3: return pd.Series({"n":float(len(x))})
        m=x.unus.mean()
        dev=(x.unus-m).groupby(x.day).sum()
        se=np.sqrt((dev**2).sum())/len(x)
        return pd.Series({"n":float(len(x)),"days":float(x.day.nunique()),"mean":m,"t":m/se if se>0 else np.nan,
                          "hit":(x.unus>0).mean(),"strength":x["str"].mean()})
    def grp(x,key):
        return x.groupby(key,observed=True).apply(summ)
    out={}
    fri=d[d.wd==4].copy()
    cases=fri[fri.fc>=2].copy()
    out["cases"]=summ(cases)
    fv=fri.dropna(subset=["vr","r14"]).copy()
    fv["vhi"]=fv.vr>1; fv["up"]=fv.r14>0
    out["fri_by_volhi_up"]=grp(fv,["vhi","up"])
    fv["vrq"]=pd.qcut(fv.vr,5,labels=False)
    out["fri_by_vrq"]=grp(fv,"vrq")
    fv["r14q"]=pd.qcut(fv.r14,5,labels=False)
    out["fri_by_r14q"]=grp(fv,"r14q")
    hv=fv[fv.vhi].copy()
    hv["r14q"]=pd.qcut(hv.r14,5,labels=False)
    out["fri_volhi_by_r14q"]=grp(hv,"r14q")
    cases["fcq"]=pd.qcut(cases.fc.rank(method="first"),4,labels=False)
    out["cases_by_fcq"]=grp(cases,"fcq")
    cases["r14q"]=pd.qcut(cases.r14,4,labels=False)
    out["cases_by_r14q"]=grp(cases,"r14q")
    cases["vrq"]=pd.qcut(cases.vr,4,labels=False)
    out["cases_by_vrq"]=grp(cases,"vrq")
    out["cases_by_coin"]=grp(cases,"coin")
    out["cases_by_year"]=grp(cases,"year")
    # weekend-specific? same condition on other weekdays, grid bars
    a=d.dropna(subset=["vr","r14"])
    a=a[(a.vr>1)&(a.r14>0)&a.grid]
    out["volhi_up_by_weekday"]=grp(a,"wd")
    # all-day baseline by weekday (grid)
    out["all_by_weekday"]=grp(d[d.grid],"wd")
    out["usual"]=pd.Series(usual); out["drift"]=pd.Series(drift)
    return out
