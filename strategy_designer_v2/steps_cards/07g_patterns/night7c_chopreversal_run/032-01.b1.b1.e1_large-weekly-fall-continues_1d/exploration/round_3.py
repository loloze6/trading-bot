def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        # coin drift per horizon over all windows (non-overlapping)
        drift={}
        for h in (1,2,3):
            a=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                a+=list(c[idx+h]/c[idx]-1)
            drift[h]=np.mean(a)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(30).std().shift(1)
            z1=r/vol
            z2=(c/c.shift(2)-1)/(vol*np.sqrt(2))
            z3=(c/c.shift(3)-1)/(vol*np.sqrt(3))
            volrank=vol/vol.rolling(180,min_periods=60).median()
            ts=pd.to_datetime(b["timestamp"])
            for h in (1,2,3):
                fwd=c.shift(-h)/c-1
                for i in range(0,len(c)-h,h):
                    rows.append(dict(h=h,coin=coin,w=w,day=ts[i].normalize(),z1=z1[i],z2=z2[i],z3=z3[i],
                        un=fwd[i]-drift[h],fz=(fwd[i]-drift[h])/(vol[i]*np.sqrt(h)) if vol[i]>0 else np.nan,
                        vr=volrank[i],yr=ts[i].year))
    d=pd.DataFrame(rows).dropna(subset=["z1","un","fz"])
    def ct(g,col):
        dev=g[col]-g[col].mean(); s=dev.groupby(g.day).sum(); G=len(s)
        if G<2: return np.nan,G
        se=np.sqrt((s**2).sum()*G/(G-1))/len(g)
        return g[col].mean()/se,G
    def summ(g,col="un"):
        t,G=ct(g,col)
        return pd.Series(dict(n=len(g),days=G,mean=g[col].mean(),t_day=t,mean_fz=g.fz.mean()))
    out={}
    for h in (1,2,3):
        dh=d[d.h==h].copy()
        dn=dh[dh.z1<0].copy()
        dn["zb"]=pd.cut(dn.z1,[-np.inf,-3,-2,-1.5,-1,-0.5,0])
        out[f"h{h} down day: unusual fwd by z1"]=dn.groupby("zb").apply(summ)
        dn=dn.assign(p=-dn.z1.clip(-5,0)*dn.fz)
        out[f"h{h} down-day graded product"]=pd.Series(dict(zip(["t_day","days"],ct(dn,"p")),mean=dn.p.mean()))
    d1=d[(d.h==1)&(d.z1<0)].copy().assign(p=lambda x:-x.z1.clip(-5,0)*x.fz)
    out["h1 down product by year"]=d1.groupby("yr").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=ct(g,"p")[0])))
    out["h1 down product by coin"]=d1.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=ct(g,"p")[0])))
    dv=d1.dropna(subset=["vr"]).copy(); dv["vT"]=pd.qcut(dv.vr,3,labels=["calm","mid","agitated"])
    out["h1 down product by vol tercile"]=dv.groupby("vT").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=ct(g,"p")[0])))
    out["h1 z1<=-2 by year"]=d[(d.h==1)&(d.z1<=-2)].groupby("yr").apply(summ)
    for k in ("z2","z3"):
        dk=d[(d.h==1)].dropna(subset=[k]).copy()
        dk["b"]=pd.cut(dk[k],[-np.inf,-2,-1,0,1,2,np.inf])
        out[f"h1 unusual by {k}"]=dk.groupby("b").apply(summ)
    return out
