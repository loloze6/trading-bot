def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,3,5,10,20]
    rows=[]
    for coin,ws in data["bars"].items():
        # drift per horizon
        dr={}
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rr+=list(c[idx+h]/c[idx]-1)
            dr[h]=np.mean(rr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            tr=(b["regime"]=="trending").values
            raw=b.get("debug_info.components.ma_dist.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            sma=pd.Series(c).rolling(50,min_periods=20).mean().values
            dist=c/sma-1
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            low=0; seen=set(); seen_all=set()
            for t in range(len(b)):
                if f[t]<=0: low=0
                isbet=False
                if tr[t] and f[t]>0 and f[t]-low>=2:
                    isbet=True; low=f[t]
                elif f[t]>0: low=min(low,f[t]) if low>0 else low
                cell=t//5
                rec=None
                if tr[t] and cell not in seen_all:
                    seen_all.add(cell)
                    rec=dict(coin=coin,w=w,yr=yr[t],f=f[t],bet=isbet,anytr=True,raw=raw[t],dist=dist[t])
                if isbet and cell not in seen:
                    seen.add(cell)
                    rec2=dict(coin=coin,w=w,yr=yr[t],f=f[t],bet=True,anytr=False,raw=raw[t],dist=dist[t])
                    for h in H:
                        rec2[f"x{h}"]=c[t+h]/c[t]-1-dr[h] if t+h<len(c) else np.nan
                    rows.append(rec2)
                if rec is not None:
                    for h in H:
                        rec[f"x{h}"]=c[t+h]/c[t]-1-dr[h] if t+h<len(c) else np.nan
                    rows.append(rec)
    d=pd.DataFrame(rows)
    cases=d[~d.anytr].dropna(subset=["x5"])
    alltr=d[d.anytr].dropna(subset=["x5"])
    def summ(g,col="x5"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["cases_by_h"]=pd.DataFrame({h:summ(cases,f"x{h}") for h in H}).T
    out["alltrend_by_h"]=pd.DataFrame({h:summ(alltr,f"x{h}") for h in H}).T
    alltr=alltr.assign(pos=alltr.f>0)
    out["alltrend_f_pos_vs_zero"]=alltr.groupby("pos").apply(summ)
    cases=cases.assign(fq=pd.qcut(cases.f.rank(method="first"),5,labels=False),
                       dq=pd.qcut(cases.dist.rank(method="first"),5,labels=False))
    out["by_forecast_q"]=cases.groupby("fq").apply(lambda g: pd.concat([summ(g),pd.Series({"f":g.f.mean(),"dist":g.dist.mean(),"x10":g.x10.mean()})]))
    out["by_dist_q"]=cases.groupby("dq").apply(lambda g: pd.concat([summ(g),pd.Series({"dist":g.dist.mean(),"x10":g.x10.mean(),"x20":g.x20.mean()})]))
    alltr=alltr.assign(dq=pd.qcut(alltr.dist.rank(method="first"),5,labels=False))
    out["alltrend_by_dist_q"]=alltr.groupby("dq").apply(lambda g: pd.concat([summ(g),pd.Series({"dist":g.dist.mean(),"x10":g.x10.mean()})]))
    out["by_coin"]=cases.groupby("coin").apply(summ)
    out["by_year"]=cases.groupby("yr").apply(summ)
    out["by_window"]=cases.groupby("w").apply(summ)
    out["slope_f"]=stats.linregress(cases.f,cases.x5).slope
    cc=cases.dropna(subset=["dist"])
    out["corr_dist_x5"]=stats.spearmanr(cc.dist,cc.x5).correlation
    return out
