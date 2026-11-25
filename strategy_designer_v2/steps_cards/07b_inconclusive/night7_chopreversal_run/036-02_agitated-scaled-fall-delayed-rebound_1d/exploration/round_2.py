import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            r=pd.Series(c).pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=(r/sd).values
            ag=(b["regime"]!="chop").astype(int).values
            fc=b["forecast"].astype(float).values
            n=len(b)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for t in range(n):
                rows.append(dict(coin=coin,w=w,year=yr[t],t=t,z=z[t],ag=ag[t],fc=fc[t],
                    f1=c[t+1]/c[t]-1 if t+1<n else np.nan,
                    f23=c[t+3]/c[t+1]-1 if t+3<n else np.nan))
    d=pd.DataFrame(rows)
    out={}
    # day1, grid h=1, all bars
    d["x1"]=d["f1"]-d.groupby("coin")["f1"].transform("mean")
    s1=d[(d.ag==1)&(d.z<0)].dropna(subset=["z","x1"]).copy()
    s1["fz"]=(-s1.z).clip(upper=3)
    o=[]
    for nm,q in [("all",s1),("z<=3",s1[s1.z>=-3])]:
        lr=stats.linregress(q.fz,q.x1); rho=stats.spearmanr(-q.z,q.x1)
        o.append(dict(sub=nm,n=len(q),slope=lr.slope,t=lr.slope/lr.stderr,spearman=rho.correlation,sp_p=rho.pvalue))
    out["d1_ag_robust"]=pd.DataFrame(o)
    o=[]
    for k in ["coin","year"]:
        for key,q in s1.groupby(k):
            lr=stats.linregress(q.fz,q.x1)
            o.append(dict(by=k,key=key,n=len(q),slope=lr.slope,t=lr.slope/lr.stderr))
    out["d1_ag_by_group_capped"]=pd.DataFrame(o)
    # d2-3 grid on test's start (t-1 fall); use z at t (fall day), f23 from t
    g=d[d.t%2==0].copy(); g["x"]=g["f23"]-g.groupby("coin")["f23"].transform("mean")
    s=g[(g.ag==1)&(g.z<0)].dropna(subset=["z","x"]).copy()
    s["fz"]=(-s.z).clip(upper=3)
    o=[]
    for k in ["coin","year"]:
        for key,q in s.groupby(k):
            lr=stats.linregress(q.fz,q.x)
            o.append(dict(by=k,key=key,n=len(q),slope=lr.slope,t=lr.slope/lr.stderr))
    out["d23_ag_by_group_capped"]=pd.DataFrame(o)
    rho=stats.spearmanr(-s.z,s.x)
    out["d23_ag_spearman"]=pd.Series(dict(n=len(s),rho=rho.correlation,p=rho.pvalue))
    # test forecast vs raw z correlation on active bars
    a=d[(d.fc>0)].dropna(subset=["z"])
    d["zlag"]=d.groupby(["coin","w"])["z"].shift(1)
    a=d[d.fc>0].dropna(subset=["zlag"])
    out["fc_vs_zlag"]=pd.Series(dict(n=len(a),corr=np.corrcoef(a.fc,-a.zlag)[0,1],share_zlag_neg=(a.zlag<0).mean()))
    return out
