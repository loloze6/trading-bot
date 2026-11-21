def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=96
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rs+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rs)
        for w,b in wins.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            raw=b["debug_info.components.plunge_in_uptrend.last_history_value"].values
            r30=pd.Series(c).pct_change(720).values
            r24=pd.Series(c).pct_change(24).values
            low=0.0; seen=set()
            n=len(c)
            for t in range(n):
                if f[t]<=0: low=0.0
                if f[t]-low>=2:
                    cell=t//H
                    low=f[t]
                    if cell not in seen and t+H<n:
                        seen.add(cell)
                        rec={"coin":coin,"win":int(w[1:]),"year":b["timestamp"].iloc[t].year if hasattr(b["timestamp"].iloc[t],"year") else pd.Timestamp(b["timestamp"].iloc[t]).year,
                             "f":f[t],"raw":raw[t],"r30":r30[t],"r24":r24[t]}
                        for h in (24,48,96,192):
                            rec[f"u{h}"]=(c[min(t+h,n-1)]/c[t]-1) if t+h<n else np.nan
                        rec["u96"]=c[t+H]/c[t]-1-drift[coin]
                        rows.append(rec)
                else:
                    low=min(low,f[t])
    d=pd.DataFrame(rows)
    def g(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["overall"]=g(d.u96)
    out["f_desc"]=d.f.describe()
    out["share_f20"]=float((d.f>=19.99).mean())
    out["median_f"]=float(d.f.median())
    d["fq"]=pd.qcut(d.f.rank(method="first"),5,labels=False)
    out["by_f_quint"]=d.groupby("fq").apply(lambda x: pd.concat([g(x.u96),pd.Series({"fmean":x.f.mean()})]))
    d["rq"]=pd.qcut(d.raw.rank(method="first"),5,labels=False)
    out["by_raw_quint"]=d.groupby("rq").apply(lambda x: pd.concat([g(x.u96),pd.Series({"raw":x.raw.mean()})]))
    d["r30q"]=pd.qcut(d.r30.rank(method="first"),5,labels=False)
    out["by_r30_quint"]=d.groupby("r30q").apply(lambda x: pd.concat([g(x.u96),pd.Series({"r30":x.r30.mean(),"r24":x.r24.mean()})]))
    d["r24q"]=pd.qcut(d.r24.rank(method="first"),5,labels=False)
    out["by_r24_quint"]=d.groupby("r24q").apply(lambda x: pd.concat([g(x.u96),pd.Series({"r24":x.r24.mean()})]))
    out["by_coin"]=d.groupby("coin").apply(lambda x: g(x.u96))
    out["by_year"]=d.groupby("year").apply(lambda x: g(x.u96))
    hz={}
    for h in (24,48,96,192):
        x=d[f"u{h}"].dropna(); hz[h]=g(x)
    out["raw_total_by_horizon"]=pd.DataFrame(hz).T
    return out
