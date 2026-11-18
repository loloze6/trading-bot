import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change()
            vol=r1.rolling(20).std().shift(1)
            z=r1/vol
            vr=b.volume/b.volume.shift(1).rolling(20).median()
            f3=cl.shift(-3)/cl-1; f1=cl.shift(-1)/cl-1
            ts=pd.to_datetime(b.timestamp)
            d=pd.DataFrame(dict(coin=c,wn=int(w[1:]),pos=np.arange(len(b)),z=z,r1=r1,vr=vr,f3=f3,f1=f1,
                yr=ts.dt.year,wd=ts.dt.weekday))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    m3=D[D.pos%3==0].groupby("coin").f3.mean()
    D["ex3"]=D.f3-D.coin.map(m3)
    m1=D.groupby("coin").f1.mean()
    D["ex1"]=D.f1-D.coin.map(m1)
    D["lvr"]=np.log(D.vr)
    G=D[D.pos%3==0].dropna(subset=["ex3","lvr","z"]).copy()
    out={}
    def slope(g,x):
        if len(g)<10: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[x],g.ex3); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    Dn=G[G.r1<0].copy(); Up=G[G.r1>0].copy()
    out["down days slope ex3 on lvr"]=slope(Dn,"lvr")
    out["up days slope ex3 on lvr"]=slope(Up,"lvr")
    out["down slope by coin"]=Dn.groupby("coin").apply(lambda g:slope(g,"lvr"))
    out["down slope by year"]=Dn.groupby("yr").apply(lambda g:slope(g,"lvr"))
    Dn["half"]=np.where(Dn.wn<=12,"w1-12","w13-24")
    out["down slope by half"]=Dn.groupby("half").apply(lambda g:slope(g,"lvr"))
    import numpy.linalg as la
    X=np.column_stack([np.ones(len(Dn)),Dn.lvr,Dn.z]); y=Dn.ex3.values
    b=la.lstsq(X,y,rcond=None)[0]; res=y-X@b; s2=res@res/(len(y)-3); se=np.sqrt(np.diag(s2*la.inv(X.T@X)))
    out["down multireg lvr,z t"]=pd.Series(b/se,index=["c","lvr","z"])
    # weekday robustness, daily excess return of next day
    W=D.dropna(subset=["ex1"]).copy()
    W["thfr"]=W.wd.isin([3,4])
    W["half"]=np.where(W.wn<=12,"w1-12","w13-24")
    def tm(s): return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s)))))
    out["next-day ex1 Thu/Fri bar by half"]=W[W.thfr].groupby("half").ex1.apply(tm).unstack()
    out["next-day ex1 Thu/Fri bar by coin"]=W[W.thfr].groupby("coin").ex1.apply(tm).unstack()
    out["next-day ex1 Thu/Fri by year"]=W[W.thfr].groupby("yr").ex1.apply(tm).unstack()
    return out
