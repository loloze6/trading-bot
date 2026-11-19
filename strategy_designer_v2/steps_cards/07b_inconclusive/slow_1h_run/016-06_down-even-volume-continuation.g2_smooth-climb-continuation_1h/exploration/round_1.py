import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    H=[24,72,168]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].astype(float).values
            v=df["volume"].astype(float).values
            n=len(c)
            ts=pd.to_datetime(df["timestamp"])
            ad=np.abs(np.diff(c,prepend=np.nan))
            s=pd.Series(ad).rolling(72).sum().values
            past=np.full(n,np.nan); past[72:]=c[72:]/c[:-72]-1
            net=np.full(n,np.nan); net[72:]=c[72:]-c[:-72]
            er=np.abs(net)/s
            vs=pd.Series(v).rolling(72)
            vcv=(vs.std()/vs.mean()).values
            for h in H:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,year=ts.iloc[i].year,h=h,past=past[i],er=er[i],
                                     vcv=vcv[i],fwd=c[i+h]/c[i]-1,fc=df["debug_info.components.er72.post_pipeline_value"].iloc[i] if h==72 else np.nan))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby(["coin","h"])["fwd"].transform("mean")
    out={}
    def slope(g,x="er"):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<10: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[x],g["ex"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    up=d[d.past>0]; dn=d[d.past<0]
    out["up by h (raw er)"]=up.groupby("h").apply(slope)
    out["down by h (raw er)"]=dn.groupby("h").apply(slope)
    out["up h72 forecast"]=slope(up[up.h==72],"fc")
    u72=up[up.h==72].copy(); d72=dn[dn.h==72].copy()
    out["up72 by coin"]=u72.groupby("coin").apply(slope)
    out["up72 by year"]=u72.groupby("year").apply(slope)
    u72["pq"]=pd.qcut(u72.past,3,labels=["small","mid","big"])
    out["up72 by past size"]=u72.groupby("pq").apply(slope)
    u72["eq"]=pd.qcut(u72.er,5,labels=False)
    out["up72 ex by er quintile"]=u72.groupby("eq")["ex"].agg(["count","mean","median"])
    d72["eq"]=pd.qcut(d72.er,5,labels=False)
    out["down72 ex by er quintile"]=d72.groupby("eq")["ex"].agg(["count","mean"])
    # multivariate: er beyond past size
    g=u72.dropna(subset=["er","past","ex"])
    X=np.column_stack([np.ones(len(g)),g.er,g.past]); b,res,_,_=np.linalg.lstsq(X,g.ex,rcond=None)
    e=g.ex-X@b; se=np.sqrt(np.diag(np.sum(e**2)/(len(g)-3)*np.linalg.inv(X.T@X)))
    out["up72 multi er,past: b,t"]=pd.DataFrame(dict(b=b,t=b/se),index=["c","er","past"])
    out["up72 vcv slope (volume unevenness)"]=slope(u72,"vcv")
    allh=d[d.h==72].copy(); allh["signed"]=np.sign(allh.past)*allh.er
    out["all72 signed er"]=slope(allh,"signed")
    out["all72 signed er by year"]=allh.groupby("year").apply(lambda g: slope(g,"signed"))
    return out
