def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H):
                rs.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(rs); usual[coin]=np.std(rs)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            ts=pd.to_datetime(b["timestamp"])
            n=len(c); low=0.0; seen=set()
            for t in range(1,n):
                if f[t]>=0: low=0.0; continue
                prev=f[t-1] if f[t-1]<0 else 0.0
                # bet: forecast falls by >=2 from last bet level
                if f[t] <= low-2:
                    low=f[t]
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    r={}
                    for h in [3,7,14,26,40]:
                        r[h]=(c[t+h]/c[t]-1) if t+h<n else np.nan
                    past=c[t]/c[t-H]-1 if t>=H else np.nan
                    rows.append(dict(coin=coin,w=w,year=ts[t].year,f=f[t],past=past,
                        r3=r[3],r7=r[7],r14=r[14],r26=r[26],r40=r[40],
                        un26=-(r[26]-drift[coin]) if not np.isnan(r[26]) else np.nan,
                        pct_left=(n-t)/n))
                elif f[t]>low: pass
    d=pd.DataFrame(rows)
    out={}
    def tt(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out["overall_un26"]=tt(d.un26)
    out["by_coin"]=d.groupby("coin").un26.apply(tt).unstack()
    out["by_year"]=d.groupby("year").un26.apply(tt).unstack()
    for h in [3,7,14,26,40]:
        d[f"neg{h}"]=-d[f"r{h}"]
    out["raw_short_by_h"]=pd.DataFrame({h:tt(d[f"neg{h}"]) for h in [3,7,14,26,40]}).T
    d["fq"]=pd.qcut(d.f.rank(method="first"),4,labels=["thinnest","q2","q3","thickest"])
    out["by_thin_q"]=d.groupby("fq").un26.apply(tt).unstack()
    d["pq"]=pd.qcut(d.past.rank(method="first"),3,labels=["pastlow","pastmid","pasthigh"])
    out["by_past26"]=d.groupby("pq").un26.apply(tt).unstack()
    out["corr_f_un"]=stats.spearmanr(d.f,d.un26,nan_policy="omit")[0]
    out["drift_usual"]=pd.DataFrame({"drift":drift,"usual":usual})
    out["ncases"]=len(d)
    return out
