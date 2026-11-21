import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=72
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        # normal drift and usual move per horizon
        for h in (24,72,168):
            rets=[]
            for w,b in wins.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rets.extend(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=(np.mean(rets),np.std(rets))
        for w,b in wins.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            raw=b.get("debug_info.components.fall24.last_history_value")
            raw=raw.values if raw is not None else np.full(len(c),np.nan)
            r30=pd.Series(c).pct_change(720).values
            r24=pd.Series(c).pct_change(24).values
            n=len(c); lo=0.0; lastcell=-1
            for t in range(n):
                if f[t]<=0: lo=0.0; continue
                lo=min(lo,f[t])
                if f[t]-lo>=2:
                    cell=t//H
                    if cell!=lastcell:
                        lastcell=cell
                        r={"coin":coin,"win":w,"year":pd.Timestamp(b["timestamp"].iloc[t]).year,
                           "f":f[t],"raw":raw[t],"r30":r30[t],"r24":r24[t],
                           "hour":pd.Timestamp(b["timestamp"].iloc[t]).hour}
                        for h in (24,72,168):
                            if t+h<n:
                                m,s=drift[(coin,h)]
                                r[f"u{h}"]=c[t+h]/c[t]-1-m
                                r[f"s{h}"]=(c[t+h]/c[t]-1-m)/s
                        rows.append(r)
                    lo=f[t]
    d=pd.DataFrame(rows).dropna(subset=["u72"])
    def agg(g):
        x=g["u72"]; 
        return pd.Series({"n":len(x),"mean_u72":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),
                          "u24":g["u24"].mean(),"u168":g["u168"].mean(),"str72":g["s72"].mean()})
    out={}
    out["all"]=agg(d).to_frame().T
    out["by_coin"]=d.groupby("coin").apply(agg)
    out["by_year"]=d.groupby("year").apply(agg)
    d["fq"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    out["by_forecast_quintile"]=d.groupby("fq").apply(agg).join(d.groupby("fq")["f"].mean().rename("f_mean")).join(d.groupby("fq")["raw"].mean().rename("raw_mean"))
    dr=d.dropna(subset=["raw"])
    dr["rq"]=pd.qcut(dr["raw"].rank(method="first"),5,labels=False)
    out["by_raw_quintile"]=dr.groupby("rq").apply(agg).join(dr.groupby("rq")["raw"].mean().rename("raw_mean"))
    dd=d.dropna(subset=["r30"]).copy()
    dd["r30q"]=pd.qcut(dd["r30"].rank(method="first"),5,labels=False)
    out["by_r30_quintile"]=dd.groupby("r30q").apply(agg).join(dd.groupby("r30q")["r30"].mean().rename("r30_mean"))
    out["spearman_f_u72"]=str(stats.spearmanr(d["f"],d["u72"]))
    out["spearman_raw_u72"]=str(stats.spearmanr(dr["raw"],dr["u72"]))
    out["spearman_r30_u72"]=str(stats.spearmanr(dd["r30"],dd["u72"]))
    out["f_describe"]=d["f"].describe()
    return out
