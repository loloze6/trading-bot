def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,3,5,10,20]
    bars=data["bars"]
    drift={}; usual={}
    for c in bars:
        for h in H:
            rs=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                idx=np.arange(0,len(cl)-h,h)
                rs+=list(cl[idx+h]/cl[idx]-1)
            drift[(c,h)]=np.mean(rs); usual[(c,h)]=np.std(rs)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            f=df["forecast"].fillna(0).values; cl=df["close"].values
            brk=df.get("debug_info.components.break.last_history_value")
            run=df.get("debug_info.components.runup.last_history_value")
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            low=f[0] if len(f) else 0; bets=[]
            for i in range(len(f)):
                low=min(low,f[i])
                if f[i]>0 and f[i]-low>=2:
                    bets.append(i); low=f[i]
            for h in H:
                seen=set()
                for i in bets:
                    cell=i//5  # plan's grid (5)
                    if cell in seen: continue
                    seen.add(cell)
                    if i+h>=len(cl): continue
                    r=cl[i+h]/cl[i]-1
                    rows.append(dict(coin=c,win=w,year=yr[i],h=h,f=f[i],
                        brk=np.nan if brk is None else brk.iloc[i],
                        run=np.nan if run is None else run.iloc[i],
                        un=r-drift[(c,h)],st=(r-drift[(c,h)])/usual[(c,h)]))
    d=pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g),mean=g.un.mean(),t=g.un.mean()/(g.un.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,strength=g.st.mean(),hit=(g.un>0).mean()))
    out={}
    out["by_h"]=d.groupby("h").apply(agg)
    d5=d[d.h==5].copy()
    out["by_coin"]=d5.groupby("coin").apply(agg)
    out["by_year"]=d5.groupby("year").apply(agg)
    out["by_win"]=d5.groupby("win").apply(agg)
    d5["fq"]=pd.qcut(d5.f.rank(method="first"),4,labels=False)
    out["by_f_q"]=d5.groupby("fq").apply(agg)
    d5["bq"]=pd.qcut(d5.brk.rank(method="first"),4,labels=False)
    out["by_brk_q"]=d5.groupby("bq").apply(agg)
    d5["rq"]=pd.qcut(d5.run.rank(method="first"),4,labels=False)
    out["by_run_q"]=d5.groupby("rq").apply(agg)
    d10=d[d.h==10].copy(); d10["rq"]=pd.qcut(d10.run.rank(method="first"),4,labels=False)
    out["h10_by_run_q"]=d10.groupby("rq").apply(agg)
    out["h10_by_coin"]=d10.groupby("coin").apply(agg)
    out["trimmed_h5"]=pd.Series(dict(median=d5.un.median(),mean_clip=d5.un.clip(d5.un.quantile(.05),d5.un.quantile(.95)).mean(),sd=d5.un.std()))
    return out
