def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    sd={}
    for coin,ws in data["bars"].items():
        r3=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-3,3)
            r3+=list(c[idx+3]/c[idx]-1)
        drift[coin]=np.mean(r3); sd[coin]=np.std(r3,ddof=1)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            f=b["forecast"].fillna(0).values; c=b["close"].values
            raw=b.get("debug_info.components.scaled_week_rise.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            ts=pd.to_datetime(b["timestamp"])
            lowest=0.0; cell_done=-1
            for t in range(len(b)):
                if f[t]<=0: lowest=0.0; continue
                lowest=min(lowest,f[t])
                cell=t//3
                if f[t]-lowest>=2 and cell!=cell_done:
                    cell_done=cell; lowest=f[t]
                    rec={"coin":coin,"w":w,"year":ts[t].year,"f":f[t],"raw":raw[t],"day":ts[t].normalize()}
                    for h in [1,3,5,7,10]:
                        rec[f"u{h}"]=(c[t+h]/c[t]-1) if t+h<len(c) else np.nan
                    rows.append(rec)
    d=pd.DataFrame(rows)
    for h in [1,3,5,7,10]:
        # drift per day scaled from 3-day drift
        d[f"x{h}"]=d[f"u{h}"]-d["coin"].map(drift)*h/3
    def summ(g,col="x3"):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    out["overall_by_h"]=pd.DataFrame({h:summ(d,f"x{h}") for h in [1,3,5,7,10]}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    out["by_window"]=d.groupby("w").apply(summ)
    d["fq"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    out["by_forecast_quintile"]=d.groupby("fq").apply(lambda g: pd.concat([summ(g),pd.Series({"fmean":g.f.mean(),"rawmean":g.raw.mean()})]))
    dr=d.dropna(subset=["raw"])
    dr["rq"]=pd.qcut(dr["raw"].rank(method="first"),5,labels=False)
    out["by_raw_quintile"]=dr.groupby("rq").apply(lambda g: pd.concat([summ(g),pd.Series({"rawmean":g.raw.mean()})]))
    out["spearman_f_by_h"]=pd.Series({h:stats.spearmanr(d.f,d[f"x{h}"],nan_policy="omit")[0] for h in [1,3,5,7,10]})
    out["spearman_raw_x3"]=stats.spearmanr(dr.raw,dr.x3)[0]
    out["drift"]=pd.Series(drift); out["sd3"]=pd.Series(sd)
    out["share_pos_x3"]=float((d.x3>0).mean())
    out["median_x3"]=float(d.x3.median())
    return out
