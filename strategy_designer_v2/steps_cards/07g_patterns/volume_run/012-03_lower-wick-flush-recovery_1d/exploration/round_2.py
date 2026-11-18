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
            rng=(b.high-b.low).replace(0,np.nan)
            wick=(np.minimum(b.open,b.close)-b.low)/rng
            f3=cl.shift(-3)/cl-1
            n=len(b)
            d=pd.DataFrame(dict(coin=c,w=w,wn=int(w[1:]),pos=np.arange(n),z=z,r1=r1,vr=vr,wick=wick,f3=f3,
                yr=pd.to_datetime(b.timestamp).dt.year))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    m3=D[D.pos%3==0].groupby("coin").f3.mean()
    D["ex3"]=D.f3-D.coin.map(m3)
    D["lvr"]=np.log(D.vr)
    G=D[D.pos%3==0].dropna(subset=["ex3","lvr","z"]).copy()
    out={}
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex3.mean(),t=g.ex3.mean()/(g.ex3.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    G["vq"]=pd.cut(G.vr,[0,1,1.5,2,3,5,999])
    G["dir"]=np.where(G.r1>0,"up","down")
    out["grid ex3 by volratio x dir"]=G.groupby(["dir","vq"]).apply(summ)
    def slope(g,x):
        r=stats.linregress(g[x],g.ex3); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    out["slope ex3 on log volratio by coin"]=G.groupby("coin").apply(lambda g:slope(g,"lvr"))
    out["slope ex3 on log volratio all"]=slope(G,"lvr")
    G["half"]=np.where(G.wn<=12,"w1-12","w13-24")
    out["slope by half"]=G.groupby("half").apply(lambda g:slope(g,"lvr"))
    out["slope by year"]=G.groupby("yr").apply(lambda g:slope(g,"lvr"))
    hi=G[G.vr>=2]
    out["burst grid by coin"]=hi.groupby("coin").apply(summ)
    # wick among non-burst sharp falls, grid sample
    F=G[(G.z<=-1.5)].copy()
    F["burst"]=F.vr>=2
    out["falls z<=-1.5 slope ex3 on wick by burst"]=F.groupby("burst").apply(lambda g:slope(g,"wick"))
    # control: slope on lvr adding z and |z|
    import numpy.linalg as la
    X=np.column_stack([np.ones(len(G)),G.lvr,G.z,G.z.abs()]); y=G.ex3.values
    b=la.lstsq(X,y,rcond=None)[0]; res=y-X@b; s2=res@res/(len(y)-4); se=np.sqrt(np.diag(s2*la.inv(X.T@X)))
    out["multireg lvr,z,|z| t"]=pd.Series(b/se,index=["c","lvr","z","absz"])
    return out
