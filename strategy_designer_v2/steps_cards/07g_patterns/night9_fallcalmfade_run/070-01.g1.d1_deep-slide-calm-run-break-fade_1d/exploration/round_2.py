def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            r=pd.Series(c).pct_change().values
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            nxt2=np.r_[c[2:]/c[:-2]-1,np.nan,np.nan]
            run=np.zeros(len(c),int); k=0
            for i in range(len(c)):
                k=k+1 if (i>0 and r[i]<0) else 0
                run[i]=k
            prevrun=np.r_[0,run[:-1]]
            sd20=pd.Series(r).rolling(20).std().values
            ret60=pd.Series(c).pct_change(60).values
            ret20=pd.Series(c).pct_change(20).values
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame(dict(coin=coin,w=w,r=r,nxt=nxt,nxt2=nxt2,prevrun=prevrun,sd20=sd20,ret60=ret60,
                z20=ret20/(sd20*np.sqrt(20)),clpos=(c-l)/np.where(h>l,h-l,np.nan),reg=b["regime"].values,
                day=ts.dt.floor("D").values,yr=ts.dt.year.values)))
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean(); d["ex"]=d["nxt"]-d["coin"].map(mu)
    mu2=d.groupby("coin")["nxt2"].mean(); d["ex2"]=d["nxt2"]-d["coin"].map(mu2)
    d["sdz"]=d.r/d.sd20
    d["t60"]=pd.cut(d.ret60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    def S(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series(dict(n=len(g),days=np.nan,mean=np.nan,tday=np.nan,wpos=np.nan,nw=np.nan))
        s=g.groupby("day")[col].sum(); cnt=g.groupby("day")[col].count()
        m=g[col].mean(); dev=(g[col]-m).groupby(g["day"]).sum()
        t=m*len(g)/np.sqrt((dev**2).sum())
        wm=g.groupby("w")[col].mean()
        return pd.Series(dict(n=len(g),days=len(s),mean=m,tday=t,wpos=(wm>0).sum(),nw=len(wm)))
    out={}
    up=d[d.r>0].copy()
    out["up days by trend, day-clustered"]=up.groupby("t60").apply(S)
    out["up days by trend, 2-day"]=up.groupby("t60").apply(lambda g:S(g,"ex2"))
    ch=up[up.t60=="chop"].copy()
    ch["q"]=pd.qcut(ch.sdz,3,labels=False)
    out["chop up days by sd-size tercile"]=ch.groupby("q").apply(S)
    ch["cq"]=pd.qcut(ch.clpos,3,labels=False)
    out["chop up days by close pos tercile"]=ch.groupby("cq").apply(S)
    ch["rb"]=ch.prevrun.clip(upper=3)
    out["chop up days by prev down run"]=ch.groupby("rb").apply(S)
    ch["zq"]=pd.qcut(ch.z20,3,labels=False)
    out["chop up days by z20 tercile"]=ch.groupby("zq").apply(S)
    out["chop up days by year"]=ch.groupby("yr").apply(S)
    fa=up[up.t60=="fall"].copy()
    fa["rb"]=fa.prevrun.clip(upper=4)
    out["fall up days by prev run"]=fa.groupby("rb").apply(S)
    fa["fc"]=fa.reg.isin(["trending","unknown"])
    out["fall up days calm(regime) vs other"]=fa.groupby("fc").apply(S)
    fa["q"]=pd.qcut(fa.sdz,3,labels=False)
    out["fall up days by sd-size tercile"]=fa.groupby("q").apply(S)
    dn=d[d.r<0].copy()
    out["down days by trend"]=dn.groupby("t60").apply(S)
    hi=d[d.clpos>=0.8]
    out["high close (>=0.8) by trend"]=hi.groupby("t60").apply(S)
    return out
