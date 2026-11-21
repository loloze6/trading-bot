def explore(data):
    import numpy as np, pandas as pd
    H=18
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        rr=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rr)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            n=len(c); ts=pd.to_datetime(b["timestamp"])
            minlo=pd.Series(lo).shift(1).rolling(12).min().values
            S=(pd.Series(hi).shift(1).rolling(12).max()-pd.Series(lo).shift(1).rolling(12).min()).values
            br=pd.Series(hi-lo).rolling(180).mean().values
            r180=pd.Series(c).pct_change(180).values
            seen=set()
            for t in range(180,n-H):
                if c[t]<minlo[t] and r180[t]>0 and br[t]>0:
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    rec={"coin":coin,"year":ts[t].year,"win":w,"nar":S[t]/br[t],"r180":r180[t],
                         "depth":(minlo[t]-c[t])/br[t]}
                    for h in [6,12,18,36]:
                        rec[f"long{h}"]=(c[t+h]/c[t]-1) if t+h<n else np.nan
                    rec["ulong18"]=rec["long18"]-drift[coin]
                    rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(g,col="ulong18"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),
                          "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    d["narq"]=pd.qcut(d["nar"],4,labels=False)
    wide=d[d.narq==3]
    out={}
    out["drift18"]=pd.Series(drift)
    out["narq_long_unusual"]=d.groupby("narq").apply(summ)
    out["narq_long_total"]=d.groupby("narq").apply(lambda g: summ(g,"long18"))
    out["wide_by_coin"]=wide.groupby("coin").apply(summ)
    out["wide_by_year"]=wide.groupby("year").apply(summ)
    out["wide_horizons_total"]=pd.DataFrame({h:summ(wide,f"long{h}") for h in [6,12,18,36]}).T
    out["nar_quartile_edges"]=d["nar"].quantile([0.25,0.5,0.75])
    d["narq8"]=pd.qcut(d["nar"],8,labels=False)
    out["narq8_long_unusual"]=d.groupby("narq8").apply(summ)
    out["spearman_nar_ulong"]=float(d[["nar","ulong18"]].corr(method="spearman").iloc[0,1])
    out["corr_by_coin"]=d.groupby("coin").apply(lambda g: g[["nar","ulong18"]].corr(method="spearman").iloc[0,1])
    out["corr_by_year"]=d.groupby("year").apply(lambda g: g[["nar","ulong18"]].corr(method="spearman").iloc[0,1])
    return out
