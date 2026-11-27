import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=[1,3,5,10,20]
    rows=[]
    drift={}
    # drift per coin per h over all windows (non-overlapping)
    for c,ws in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in ws.items():
                cl=b["close"].values
                for i in range(0,len(cl)-h,h):
                    rr.append(cl[i+h]/cl[i]-1)
            drift[(c,h)]=(np.mean(rr) if rr else np.nan, np.std(rr) if rr else np.nan)
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            # up-run length before
            up=(r>0).astype(int)
            run=np.zeros(len(b)); 
            for i in range(1,len(b)):
                run[i]=run[i-1]+1 if up.iloc[i]==1 else 0
            prevrun=pd.Series(run).shift(1)
            runret=pd.Series(np.nan,index=b.index)
            for i in range(1,len(b)):
                k=int(prevrun.iloc[i]) if not np.isnan(prevrun.iloc[i]) else 0
                if k>0 and not np.isnan(sd.iloc[i]):
                    runret.iloc[i]=(cl.iloc[i-1]/cl.iloc[i-1-k]-1)/sd.iloc[i]
            ra=(b["regime"]=="unknown")
            for h in H:
                seen=set()
                for i in range(len(b)-h):
                    if not ra.iloc[i] or not (r.iloc[i]<0) or np.isnan(z.iloc[i]): continue
                    cell=i//h
                    if cell in seen: continue
                    seen.add(cell)
                    fr=cl.iloc[i+h]/cl.iloc[i]-1
                    rows.append(dict(coin=c,w=w,h=h,z=z.iloc[i],prun=prevrun.iloc[i],runz=runret.iloc[i],
                        yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                        short_unusual=-(fr-drift[(c,h)][0]), short_total=-fr,day=str(pd.Timestamp(b["timestamp"].iloc[i]).date())))
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["short_unusual"]
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, total=g["short_total"].mean()))
    out={}
    out["by_h"]=d.groupby("h").apply(summ)
    d["zq"]=pd.qcut(d["z"].rank(method="first"),3,labels=["deep","mid","shallow"])
    out["h_by_depth"]=d.groupby(["h","zq"]).apply(summ)
    d["first"]=(d["prun"]>=2)
    out["h_first_after_run2"]=d.groupby(["h","first"]).apply(summ)
    out["h_by_coin"]=d.groupby(["h","coin"]).apply(summ)
    out["h10_by_year"]=d[d.h==10].groupby("yr").apply(summ)
    out["corr_z_by_h"]=d.groupby("h").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.z,g.short_unusual)[0], rho_run=stats.spearmanr(g.runz,g.short_unusual,nan_policy='omit')[0])))
    out["profile_share"]=pd.Series({c:np.mean([ (b.regime=="unknown").mean() for b in ws.values()]) for c,ws in data["bars"].items()})
    return out
