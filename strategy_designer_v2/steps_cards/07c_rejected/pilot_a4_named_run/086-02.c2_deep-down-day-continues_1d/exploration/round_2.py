import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=[5,10,15,20]
    drift={}
    for c,ws in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in ws.items():
                cl=b["close"].values
                for i in range(0,len(cl)-h,h):
                    rr.append(cl[i+h]/cl[i]-1)
            drift[(c,h)]=(np.mean(rr), np.std(rr))
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            up=(r>0).values
            run=np.zeros(len(b))
            for i in range(1,len(b)):
                run[i]=run[i-1]+1 if up[i] else 0
            ra=(b["regime"]=="unknown").values
            hi=b["high"].values; lo=b["low"].values; op=b["open"].values
            for h in H:
                seen=set()
                for i in range(1,len(b)-h):
                    if not ra[i] or not (r.iloc[i]<0) or np.isnan(sd.iloc[i]): continue
                    k=int(run[i-1])
                    if k<1: continue
                    cell=i//h
                    if cell in seen: continue
                    seen.add(cell)
                    runz=(cl.iloc[i-1]/cl.iloc[i-1-k]-1)/sd.iloc[i] if i-1-k>=0 else np.nan
                    r10=(cl.iloc[i-1]/cl.iloc[max(0,i-11)]-1)/(sd.iloc[i]*np.sqrt(10))
                    fr=cl.iloc[i+h]/cl.iloc[i]-1
                    rows.append(dict(coin=c,w=w,h=h,k=k,runz=runz,r10=r10,z=r.iloc[i]/sd.iloc[i],
                        clpos=(cl.iloc[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,
                        su=-(fr-drift[(c,h)][0]), st=-fr, strg=-(fr-drift[(c,h)][0])/drift[(c,h)][1],
                        day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                        yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["su"]
        dd=g.groupby("day")["su"].sum(); n=len(dd)
        t=dd.mean()*n/len(x)/(dd.std()/np.sqrt(n))*1 if n>2 else np.nan
        tt=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(dict(n=len(x),mean=x.mean(),t=tt,strength=g.strg.mean(),total=g.st.mean()))
    out={}
    out["first_dd_by_h"]=d.groupby("h").apply(summ)
    d["kb"]=pd.cut(d.k,[0,1,2,3,100],labels=["1","2","3","4+"])
    out["by_runlen"]=d.groupby(["h","kb"]).apply(summ)
    d["rq"]=d.groupby("h")["runz"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_runz_terc"]=d.groupby(["h","rq"]).apply(summ)
    d["r10q"]=d.groupby("h")["r10"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_r10_terc"]=d.groupby(["h","r10q"]).apply(summ)
    out["spearman"]=d.groupby("h").apply(lambda g: pd.Series(dict(runz=stats.spearmanr(g.runz,g.su,nan_policy='omit')[0],
        r10=stats.spearmanr(g.r10,g.su,nan_policy='omit')[0], k=stats.spearmanr(g.k,g.su)[0], clpos=stats.spearmanr(g.clpos,g.su,nan_policy='omit')[0], n=len(g))))
    sub=d[(d.h==20)]
    out["h20_runz_terc_by_coin"]=sub.groupby(["coin","rq"]).apply(summ)
    out["h20_runz_top_by_year"]=sub[sub.rq==2].groupby("yr").apply(summ)
    out["h10_runz_top_by_year"]=d[(d.h==10)&(d.rq==2)].groupby("yr").apply(summ)
    return out
