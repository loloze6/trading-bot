import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=72
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        rets=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rets.extend(c[idx+H]/c[idx]-1)
        drift[coin]=(np.mean(rets),np.std(rets))
        for w,b in wins.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            raw=b["debug_info.components.fall24.last_history_value"].values
            r30=pd.Series(c).pct_change(720).values
            n=len(c); lo=0.0; lastcell=-1
            for t in range(n):
                if f[t]<=0: lo=0.0; continue
                lo=min(lo,f[t])
                if f[t]-lo>=2:
                    cell=t//H
                    if cell!=lastcell and t+H<n:
                        lastcell=cell
                        m,s=drift[coin]
                        rows.append({"coin":coin,"win":w,"year":pd.Timestamp(b["timestamp"].iloc[t]).year,
                                     "f":f[t],"raw":raw[t],"r30":r30[t],"u72":c[t+H]/c[t]-1-m})
                    lo=f[t]
    d=pd.DataFrame(rows).dropna(subset=["raw","u72"])
    def agg(g):
        x=g["u72"]
        return pd.Series({"n":len(x),"mean_u72":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    d["deep"]=np.where(d["raw"]<=d["raw"].median(),"deeper","shallower")
    out["raw_half_by_coin"]=d.groupby(["coin","deep"]).apply(agg).unstack()
    out["raw_half_by_year"]=d.groupby(["year","deep"]).apply(agg).unstack()
    dd=d.dropna(subset=["r30"]).copy()
    dd["trend"]=np.where(dd["r30"]>dd["r30"].median(),"strong","weak")
    out["raw_half_x_trend"]=dd.groupby(["trend","deep"]).apply(agg).unstack()
    hi=d[d.deep=="deeper"]["u72"]; lo_=d[d.deep=="shallower"]["u72"]
    out["deeper_minus_shallower"]=pd.Series({"diff":hi.mean()-lo_.mean(),"welch_t":stats.ttest_ind(hi,lo_,equal_var=False).statistic})
    out["spearman_raw_f"]=str(stats.spearmanr(d["raw"],d["f"]))
    out["per_coin_spearman_raw_u72"]=d.groupby("coin").apply(lambda g: stats.spearmanr(g["raw"],g["u72"]).statistic)
    return out
