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
            uw=(b.high-np.maximum(b.open,b.close))/rng
            f3=cl.shift(-3)/cl-1
            f1=cl.shift(-1)/cl-1
            r5=cl/cl.shift(5)-1
            n=len(b)
            d=pd.DataFrame(dict(coin=c,w=w,pos=np.arange(n),z=z,vr=vr,wick=wick,uw=uw,f3=f3,f1=f1,vol=vol,r5=r5,
                wd=pd.to_datetime(b.timestamp).dt.weekday,yr=pd.to_datetime(b.timestamp).dt.year,
                alloc=b.postRebalance_current_allocation,fc=b.forecast,reg=b.regime))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    m3=D[D.pos%3==0].groupby("coin").f3.mean()
    D["ex3"]=D.f3-D.coin.map(m3)
    G=D[(D.pos%3==0)].dropna(subset=["ex3","z"])
    out={}
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex3.mean(),t=g.ex3.mean()/(g.ex3.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    G["zb"]=pd.cut(G.z,[-99,-2,-1,0,1,2,99])
    out["grid ex3 by z of day"]=G.groupby("zb").apply(summ)
    G["vb"]=G.groupby("coin").vol.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["grid ex3 by vol quintile"]=G.groupby("vb").apply(summ)
    G["vrb"]=pd.cut(G.vr,[0,0.7,1,1.5,2,99])
    out["grid ex3 by volratio"]=G.groupby("vrb").apply(summ)
    G["r5b"]=G.groupby("coin").r5.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["grid ex3 by 5d ret quintile"]=G.groupby("r5b").apply(summ)
    # events: all sharp falls, dedupe within 3 bars
    E=D[(D.z<=-2)].dropna(subset=["ex3"]).copy()
    E["burst"]=E.vr>=2
    E["wt"]=pd.qcut(E.wick,3,labels=["lowW","midW","hiW"])
    out["sharp falls by burst x wick (overlap ok)"]=E.groupby(["burst","wt"]).apply(summ)
    E["ub"]=pd.qcut(E.uw,3,labels=["lowU","midU","hiU"])
    out["sharp falls by upper wick"]=E.groupby("ub").apply(summ)
    S=D[(D.z>=2)].dropna(subset=["ex3"]).copy()
    S["burst"]=S.vr>=2
    out["sharp rises by burst"]=S.groupby("burst").apply(summ)
    # weekday daily return
    Wd=D.dropna(subset=["f1"])
    out["next-day ret by weekday of bar"]=Wd.groupby("wd").f1.agg(["count","mean",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))])
    # book
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    DD["inpos"]=DD.book_return.abs()>1e-12
    out["book days in/out"]=DD.groupby("inpos").agg(n=("book_return","size"),mean=("book_return","mean"),coinmean=("coin_return","mean"))
    out["active share & by coin pnl"]=D.assign(act=D.alloc.abs()>0).groupby("coin").agg(act=("act","mean"),fcpos=("fc",lambda s:(s>0).mean()))
    return out
