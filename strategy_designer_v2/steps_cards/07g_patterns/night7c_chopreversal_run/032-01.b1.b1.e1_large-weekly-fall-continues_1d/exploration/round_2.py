def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(30).std().shift(1)  # past 30 days before today's move
            z=r/vol
            ts=pd.to_datetime(b["timestamp"])
            volrank=vol/vol.rolling(180,min_periods=60).median()
            er=(c/c.shift(14)-1).abs()/r.abs().rolling(14).sum()
            for h in (1,3):
                fwd=c.shift(-h)/c-1
                for i in range(0,len(c)-h,h):
                    rows.append(dict(h=h,coin=coin,w=w,day=ts[i].normalize(),z=z[i],fwd=fwd[i],
                                     fz=fwd[i]/(vol[i]*np.sqrt(h)) if vol[i]>0 else np.nan,
                                     vr=volrank[i],er=er[i],wd=ts[i].dayofweek,yr=ts[i].year))
    d=pd.DataFrame(rows).dropna(subset=["z","fwd"])
    out={}
    def clus_t(g,col):
        dev=g[col]-g[col].mean()
        s=dev.groupby(g.day).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/len(g)
        return g[col].mean()/se, G
    def summ(g):
        t,G=clus_t(g,"fwd")
        return pd.Series(dict(n=len(g),days=G,mean=g.fwd.mean(),t_day=t,mean_fz=g.fz.mean()))
    for h in (1,3):
        dh=d[d.h==h].copy()
        dh["zb"]=pd.cut(dh.z,[-np.inf,-2,-1,0,1,2,np.inf])
        out[f"h{h} fwd by scaled day move"]=dh.groupby("zb").apply(summ)
        # graded: slope of fz on z, clustered t via per-day
        dn=dh.dropna(subset=["fz"])
        sl=np.polyfit(dn.z.clip(-5,5),dn.fz,1)[0]
        dn=dn.assign(p=-dn.z.clip(-5,5)*dn.fz)
        t,G=clus_t(dn,"p")
        out[f"h{h} reversal product -z*fz"]=pd.Series(dict(slope=sl,mean=dn.p.mean(),t_day=t,days=G))
        out[f"h{h} reversal product by year"]=dn.groupby("yr").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=clus_t(g,"p")[0])))
        out[f"h{h} reversal product by coin"]=dn.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=clus_t(g,"p")[0])))
        dv=dn.dropna(subset=["vr"]).copy()
        dv["vT"]=pd.qcut(dv.vr,3,labels=["calm","mid","agitated"])
        out[f"h{h} reversal product by vol tercile"]=dv.groupby("vT").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=clus_t(g,"p")[0])))
        de=dn.dropna(subset=["er"]).copy()
        de["eT"]=pd.qcut(de.er,3,labels=["chop","mid","trend"])
        out[f"h{h} reversal product by ER tercile"]=de.groupby("eT").apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=clus_t(g,"p")[0])))
        # down vs up side
        out[f"h{h} reversal product down vs up day"]=dn.groupby(dn.z<0).apply(lambda g: pd.Series(dict(n=len(g),mean=g.p.mean(),t=clus_t(g,"p")[0])))
    d1=d[d.h==1]
    out["h1 weekday by year mean"]=d1.groupby(["wd","yr"]).fwd.mean().unstack()
    out["h1 weekday clustered"]=d1.groupby("wd").apply(summ)
    return out
