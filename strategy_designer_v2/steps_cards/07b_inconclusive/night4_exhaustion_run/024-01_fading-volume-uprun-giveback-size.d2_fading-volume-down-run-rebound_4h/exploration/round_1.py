def explore(data):
    import numpy as np, pandas as pd
    H=[6,12,18,36]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
        for w,b in ws.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            raw=b.get("debug_info.components.streak_loss.last_history_value")
            raw=raw.values if raw is not None else np.full(len(c),np.nan)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c); lo=0.0; lastcell=-1
            for t in range(n):
                if f[t]<=0: lo=0.0
                if f[t]-lo>=2 and t//18!=lastcell:
                    lastcell=t//18; 
                    r={"coin":coin,"w":w,"yr":yr[t],"f":f[t],"raw":raw[t]}
                    for h in H:
                        if t+h<n:
                            r[f"u{h}"]=c[t+h]/c[t]-1-drift[(coin,h)][0]
                            r[f"s{h}"]=r[f"u{h}"]/drift[(coin,h)][1]
                    # prior 30-day (180 bar) return
                    r["p180"]=c[t]/c[max(0,t-180)]-1 if t>=60 else np.nan
                    rows.append(r); lo=f[t]
                else:
                    lo=min(lo,f[t]) if f[t]>0 else 0.0
    d=pd.DataFrame(rows)
    def st(g,col="u18"):
        x=g[col].dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    out["all_by_h"]=pd.DataFrame({h:st(d,f"u{h}") for h in H}).T
    d["fq"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    out["by_fq"]=pd.concat({h:d.groupby("fq").apply(lambda g:st(g,f"u{h}")) for h in [6,18,36]},axis=1)
    d["rq"]=pd.qcut(d["raw"].rank(method="first"),5,labels=False)
    out["by_rawq"]=d.groupby("rq").apply(st)
    out["raw_med_by_rq"]=d.groupby("rq")["raw"].median()
    out["by_coin"]=d.groupby("coin").apply(st)
    out["by_year"]=d.groupby("yr").apply(st)
    d["pq"]=pd.qcut(d["p180"],3,labels=False)
    out["by_prior30d_tercile"]=d.groupby("pq").apply(st)
    out["top_fq_by_coin"]=d[d.fq==4].groupby("coin").apply(st)
    out["top_fq_by_year"]=d[d.fq==4].groupby("yr").apply(st)
    out["strength_all"]=d["s18"].mean()
    return out
