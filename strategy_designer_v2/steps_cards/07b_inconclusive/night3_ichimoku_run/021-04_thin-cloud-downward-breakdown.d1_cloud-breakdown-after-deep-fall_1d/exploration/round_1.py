def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    bars=data["bars"]
    # drift per coin
    drift={}; usual={}
    for c,ws in bars.items():
        r=[]
        for w,df in ws.items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-H,H)
            r+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(r); usual[c]=np.std(r)
    rows=[]
    for c,ws in bars.items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; f=df["forecast"].fillna(0).values
            n=len(cl)
            ts=pd.to_datetime(df["timestamp"])
            used=set()
            for i in range(n):
                if f[i]<0 and (i==0 or f[i-1]>=0 or True):
                    cell=i//H
                    if cell in used: continue
                    # require a new signal: forecast nonzero only on cross bars
                    used.add(cell)
                    rec={"coin":c,"win":w,"year":ts[i].year,"absf":-f[i],
                         "ret26p":cl[i]/cl[max(0,i-26)]-1 if i>=26 else np.nan,
                         "ret60p":cl[i]/cl[i-60]-1 if i>=60 else np.nan}
                    for h in [5,10,26,52]:
                        if i+h<n:
                            rec[f"fwd{h}"]=cl[i+h]/cl[i]-1
                            rec[f"un{h}"]=-(cl[i+h]/cl[i]-1-drift[c]*h/H)
                    rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(g,col="un26"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"hit":(x>0).mean()})
    out={}
    out["all_by_h"]=pd.DataFrame({h:summ(d,f"un{h}") for h in [5,10,26,52]}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    d["fq"]=pd.qcut(d["absf"],3,labels=["low","mid","high"])
    out["by_absf"]=d.groupby("fq").apply(summ)
    d["p26q"]=pd.qcut(d["ret26p"],3,labels=["shallow","mid","deep"])
    out["by_ret26"]=d.groupby("p26q").apply(summ)
    d["p60s"]=np.where(d["ret60p"].isna(),"na",np.where(d["ret60p"]<0,"60neg","60pos"))
    out["by_ret60"]=d.groupby("p60s").apply(summ)
    out["drift"]=pd.DataFrame({"drift":drift,"usual":usual})
    out["n_and_absf"]=pd.Series({"n":len(d),"absf_med":d.absf.median(),"absf_max":d.absf.max()})
    return out
