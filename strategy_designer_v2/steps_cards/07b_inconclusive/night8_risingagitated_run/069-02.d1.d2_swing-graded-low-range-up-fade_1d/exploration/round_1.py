def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().shift(-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            hi=b["high"].astype(float).rolling(20).max(); lo=b["low"].astype(float).rolling(20).min()
            pos=2*(c-lo)/(hi-lo)-1
            r1=c.pct_change()
            nxt=c.shift(-1)/c-1
            vr=b.get("debug_info.components.agit.last_history_value")
            r5=c/c.shift(5)-1
            m=b["forecast"]<0
            for i in np.where(m)[0]:
                if np.isnan(nxt.iloc[i]): continue
                rows.append(dict(coin=coin,win=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    f=abs(b["forecast"].iloc[i]),ex=-(nxt.iloc[i]-mu),pos=pos.iloc[i],r1=r1.iloc[i],
                    r5=r5.iloc[i],vr=vr.iloc[i] if vr is not None else np.nan))
    d=pd.DataFrame(rows)
    out={}
    def tm(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["all"]=tm(d.ex)
    out["by_coin"]=d.groupby("coin").ex.apply(tm).unstack()
    out["by_year"]=d.groupby("year").ex.apply(tm).unstack()
    def slope(x,y):
        k=x.notna()&y.notna(); r=stats.linregress(x[k],y[k]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":k.sum()})
    out["slope_f"]=slope(d.f,d.ex)
    out["slope_pos"]=slope(d.pos,d.ex)
    out["slope_r1"]=slope(d.r1,d.ex)
    out["slope_r5"]=slope(d.r5,d.ex)
    out["slope_vr"]=slope(d.vr,d.ex)
    for col in ["f","pos","r1","r5"]:
        q=pd.qcut(d[col].rank(method="first"),3,labels=["lo","mid","hi"])
        out["terc_"+col]=d.groupby(q).ex.apply(tm).unstack()
    return out
