def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].astype(float).pct_change().shift(-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            hi=b["high"].astype(float).rolling(20).max(); lo=b["low"].astype(float).rolling(20).min()
            pos=2*(c-lo)/(hi-lo)-1
            r1=c.pct_change(); nxt=c.shift(-1)/c-1
            r60=c/c.shift(60)-1
            sd=r1.rolling(30).std()
            case=(b["forecast"]<0).values
            for i in range(len(b)):
                if np.isnan(nxt.iloc[i]) or not (r1.iloc[i]>0) or not (pos.iloc[i]<-0.6): continue
                rows.append(dict(coin=coin,win=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,case=case[i],
                    ex=-(nxt.iloc[i]-mu),r3=c.iloc[i]/c.iloc[i-3]-1 if i>=3 else np.nan,
                    r5=c.iloc[i]/c.iloc[i-5]-1 if i>=5 else np.nan,
                    r10=c.iloc[i]/c.iloc[i-10]-1 if i>=10 else np.nan,
                    r20=c.iloc[i]/c.iloc[i-20]-1 if i>=20 else np.nan,
                    r60=r60.iloc[i],sd=sd.iloc[i]))
    d=pd.DataFrame(rows)
    d["r5n"]=d.r5/d.sd
    out={}
    def slope(x,y):
        k=x.notna()&y.notna(); r=stats.linregress(x[k],y[k]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":int(k.sum()),"spearman":stats.spearmanr(x[k],y[k])[0]})
    def tm(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    cs=d[d.case]
    out["case_slopes"]=pd.DataFrame({k:slope(cs[k],cs.ex) for k in ["r3","r5","r10","r20","r5n"]}).T
    w=cs.copy(); w["exw"]=w.ex.clip(w.ex.quantile(.02),w.ex.quantile(.98))
    out["case_r5_winsor"]=slope(w.r5,w.exw)
    out["case_r5_by_year"]=cs.groupby("year").apply(lambda g: slope(g.r5,g.ex) if len(g)>10 else pd.Series(dtype=float))
    out["case_r5_by_coin"]=cs.groupby("coin").apply(lambda g: slope(g.r5,g.ex))
    out["case_r5_by_window"]=cs.groupby("win").apply(lambda g: slope(g.r5,g.ex) if len(g)>8 else pd.Series(dtype=float))
    fall=d[d.r60< -0.10]; nonf=d[d.r60>=-0.10]
    out["falling_all_r5"]=slope(fall.r5,fall.ex)
    out["notfalling_r5"]=slope(nonf.r5,nonf.ex)
    out["any_profile_r5"]=slope(d.r5,d.ex)
    q=pd.qcut(fall.r5.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["falling_r5_quart"]=fall.groupby(q).ex.apply(tm).unstack()
    q2=pd.qcut(nonf.r5.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["notfalling_r5_quart"]=nonf.groupby(q2).ex.apply(tm).unstack()
    return out
