def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; allbrk=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        rr=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rr); usual[coin]=np.std(rr)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            f=b["forecast"].fillna(0).values
            n=len(c)
            ts=pd.to_datetime(b["timestamp"])
            minlo=pd.Series(lo).shift(1).rolling(12).min().values
            S=(pd.Series(hi).shift(1).rolling(12).max()-pd.Series(lo).shift(1).rolling(12).min()).values
            br=pd.Series(hi-lo).rolling(180).mean().values
            ret180=pd.Series(c).pct_change(180).values
            lowest=0.0; seen=set()
            for t in range(n):
                s=-f[t] if f[t]<0 else 0.0
                if f[t]>=0:
                    lowest=0.0
                    continue
                if s-lowest>=2:
                    lowest=s
                    cell=t//H
                    if cell in seen or t+H>=n:
                        continue
                    seen.add(cell)
                    rec={"coin":coin,"year":ts[t].year,"fc":abs(f[t]),
                         "nar":S[t]/br[t] if br[t]>0 else np.nan,"r180":ret180[t]}
                    for h in [6,12,18,36,60]:
                        rec[f"m{h}"]=-(c[t+h]/c[t]-1) if t+h<n else np.nan
                    rec["u18"]=rec["m18"]+drift[coin]
                    rows.append(rec)
                else:
                    lowest=min(lowest,s)
            seen2=set()
            for t in range(180,n-H):
                if c[t]<minlo[t]:
                    cell=t//H
                    if cell in seen2: continue
                    seen2.add(cell)
                    allbrk.append({"coin":coin,"up":bool(ret180[t]>0),"nar":S[t]/br[t] if br[t]>0 else np.nan,
                                   "u18":-(c[t+H]/c[t]-1)+drift[coin],"r180":ret180[t]})
    d=pd.DataFrame(rows).dropna(subset=["u18"])
    a=pd.DataFrame(allbrk).dropna()
    def summ(g,col="u18"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),
                          "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["overall"]=summ(d)
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    d["narq"]=pd.qcut(d["nar"],4,labels=False)
    out["by_narrow_q(0=narrowest)"]=d.groupby("narq").apply(summ)
    d["rq"]=pd.qcut(d["r180"],4,labels=False)
    out["by_r180_q(0=smallest rise)"]=d.groupby("rq").apply(summ)
    d["fq"]=pd.qcut(d["fc"].rank(method="first"),4,labels=False)
    out["by_forecast_q(3=largest)"]=d.groupby("fq").apply(summ)
    hz={}
    for h in [6,12,18,36,60]:
        x=d[f"m{h}"].dropna(); hz[h]=[len(x),x.mean(),x.mean()/(x.std()/np.sqrt(len(x)))]
    out["horizons_total_short_move"]=pd.DataFrame(hz,index=["n","mean","t"]).T
    a["narq"]=pd.qcut(a["nar"],4,labels=False)
    out["allbreaks_by_month_up"]=a.groupby("up").apply(summ)
    out["allbreaks_up_narq"]=a[a.up].groupby("narq").apply(summ)
    out["allbreaks_down_narq"]=a[~a.up].groupby("narq").apply(summ)
    out["spearman_nar_u18"]=float(stats.spearmanr(d["nar"],d["u18"],nan_policy="omit")[0])
    return out
