import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars=data["bars"]
    G=[]
    for c in bars:
        for w in bars[c]:
            b=bars[c][w].reset_index(drop=True); cl=b["close"]
            r90=cl/cl.shift(90)-1; r20=cl/cl.shift(20)-1
            for h in (5,10,20):
                fwd=cl.shift(-h)/cl-1
                for i in range(0,len(b)-h,h):
                    G.append(dict(coin=c,win=w,h=h,f=b["forecast"].iloc[i],fwd=fwd.iloc[i],r90=r90.iloc[i],r20=r20.iloc[i]))
    G=pd.DataFrame(G)
    G["mu"]=G.groupby(["coin","h"])["fwd"].transform("mean")
    G["sd"]=G.groupby(["coin","h"])["fwd"].transform("std")
    G["ex"]=G.fwd-G.mu; G["st"]=-G.ex/G.sd
    out={}
    A=G[G.f<0]
    out["active_by_h"]=A.groupby("h").agg(n=("ex","size"),fwd=("fwd","mean"),ex=("ex","mean"),strength=("st","mean"))
    out["flat_by_h"]=G[G.f==0].groupby("h").agg(n=("ex","size"),fwd=("fwd","mean"),ex=("ex","mean"))
    A2=A.dropna(subset=["r90"]).copy()
    A2["r90q"]=A2.groupby("h")["r90"].transform(lambda x: pd.qcut(x.rank(method="first"),4,labels=False))
    out["active_by_r90q_h"]=A2.groupby(["h","r90q"]).agg(n=("ex","size"),r90=("r90","mean"),fwd=("fwd","mean"),ex=("ex","mean"),strength=("st","mean")).round(4)
    res={}
    for h in (5,10,20):
        for nm,sub in [("r90<0",A2[(A2.h==h)&(A2.r90<0)]),("r90>=0",A2[(A2.h==h)&(A2.r90>=0)])]:
            s=stats.linregress(sub.f,sub.ex)
            t1=stats.ttest_1samp(sub.fwd,0)
            res[f"h{h}_{nm}"]=pd.Series(dict(n=len(sub),slope=s.slope,t=s.slope/s.stderr,fwd=sub.fwd.mean(),t_fwd=t1.statistic,ex=sub.ex.mean()))
    out["slope_by_r90"]=pd.DataFrame(res).T.round(5)
    # deep 20d fall rebound in active cases
    A3=A.dropna(subset=["r20"]).copy()
    A3["r20q"]=A3.groupby("h")["r20"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["active_by_r20q_h"]=A3.groupby(["h","r20q"]).agg(n=("ex","size"),fwd=("fwd","mean"),ex=("ex","mean")).round(4)
    return out
