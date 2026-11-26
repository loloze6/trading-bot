def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    G=[];D=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change(); tr=c/c.shift(60)-1
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            sd30=r1.rolling(30).std()
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            n=len(b)
            for H in (10,20):
                fwd=c.shift(-H)/c-1
                for i in range(0,n-H,H):
                    G.append(dict(H=H,coin=coin,w=w,tr=tr[i],vr=vr[i],fwd=fwd[i],r20b=c[i]/c[i-20]-1 if i>=20 else np.nan,day=day[i]))
            D.append(pd.DataFrame(dict(coin=coin,w=w,tr=tr,vr=vr,sd=sd30,sdz=r1/sd30,f1=c.shift(-1)/c-1,f2=c.shift(-2)/c-1,day=day)))
    g=pd.DataFrame(G)
    g["mu"]=g.groupby(["H","coin"])["fwd"].transform("mean"); g["ex"]=g.fwd-g.mu
    g["prof"]=np.where(g.tr>0.1,"rising",np.where(g.tr<-0.1,"falling","choppy"))
    f=g[(g.prof=="falling")].dropna(subset=["vr","ex"])
    res={}
    for H,s in f.groupby("H"):
        sl=stats.linregress(s.vr,s.ex)
        # day-clustered: sum per day
        X=np.c_[np.ones(len(s)),s.vr.values]; beta=np.linalg.lstsq(X,s.ex.values,rcond=None)[0]
        e=s.ex.values-X@beta; XtXi=np.linalg.inv(X.T@X)
        sc=pd.DataFrame(X*e[:,None]).groupby(s.day.values).sum().values
        V=XtXi@(sc.T@sc)@XtXi
        res[H]=dict(n=len(s),days=s.day.nunique(),slope=sl.slope,t=sl.slope/sl.stderr,t_clustered=beta[1]/np.sqrt(V[1,1]),
                    corr=np.corrcoef(s.vr,s.ex)[0,1])
    out["falling: ex on raw vr by horizon"]=pd.DataFrame(res).T
    f20=f[f.H==20].copy()
    out["falling H20: by coin slope"]=f20.groupby("coin").apply(lambda s: pd.Series(dict(n=len(s),mean_vr=s.vr.mean(),slope=stats.linregress(s.vr,s.ex).slope if len(s)>3 else np.nan,mean_ex_vr_neg=s.ex[s.vr<0].mean(),mean_ex_vr_pos=s.ex[s.vr>0].mean())))
    f20["half"]=np.where(f20.w.isin(["w7","w8","w9","w10","w11","w12"]),"B","C")
    out["falling H20: by fold slope"]=f20.groupby("half").apply(lambda s: pd.Series(dict(n=len(s),slope=stats.linregress(s.vr,s.ex).slope,t=stats.linregress(s.vr,s.ex).slope/stats.linregress(s.vr,s.ex).stderr)))
    f20["vq"]=pd.qcut(f20.vr,4,labels=["q1shrink","q2","q3","q4grow"])
    out["falling H20: ex by vr quartile"]=f20.groupby("vq")["ex"].agg(["count","mean","median"])
    m=stats.linregress(f20.dropna(subset=["r20b"])[["vr","r20b"]].values[:,0],f20.dropna(subset=["r20b"]).ex)
    s2=f20.dropna(subset=["r20b"])
    X=np.c_[np.ones(len(s2)),s2.vr,s2.r20b]; b_=np.linalg.lstsq(X,s2.ex,rcond=None)[0]
    e=s2.ex-X@b_; se=np.sqrt(np.diag(np.linalg.inv(X.T@X))*(e@e)/(len(s2)-3))
    out["falling H20: ex on vr + past20"]=pd.DataFrame(dict(coef=b_,t=b_/se),index=["c","vr","r20b"])
    out["corr vr vs past20 in falling"]=float(np.corrcoef(s2.vr,s2.r20b)[0,1])
    # daily: up days in falling, next day
    d=pd.concat(D,ignore_index=True).dropna(subset=["sdz","f1","tr"])
    d["mu1"]=d.groupby("coin").f1.transform("mean"); d["e1"]=d.f1-d.mu1
    d["mu2"]=d.groupby("coin").f2.transform("mean"); d["e2"]=d.f2-d.mu2
    d["prof"]=np.where(d.tr>0.1,"rising",np.where(d.tr<-0.1,"falling","choppy"))
    d["agit"]=np.where(d.sd>d.groupby("coin").sd.transform("median"),"agit","calm")
    res={}
    for (p,a),s in d[d.sdz>0].groupby(["prof","agit"]):
        for y in ("e1",):
            dd=s.dropna(subset=[y]); daily=dd.groupby("day").apply(lambda q: pd.Series(dict(x=q.sdz.mean(),y=q[y].mean())))
            sl=stats.linregress(daily.x,daily.y)
            res[(p,a)]=dict(n=len(dd),days=len(daily),mean_e1=dd.e1.mean(),slope=sl.slope,t_dayagg=sl.slope/sl.stderr)
    out["up days: next-day ex on z, by profile x agit (day-aggregated)"]=pd.DataFrame(res).T
    res={}
    for (p,a),s in d[d.sdz<0].groupby(["prof","agit"]):
        daily=s.groupby("day").apply(lambda q: pd.Series(dict(x=q.sdz.mean(),y=q.e1.mean())))
        sl=stats.linregress(daily.x,daily.y)
        res[(p,a)]=dict(n=len(s),days=len(daily),mean_e1=s.e1.mean(),slope=sl.slope,t_dayagg=sl.slope/sl.stderr)
    out["down days: next-day ex on z, by profile x agit"]=pd.DataFrame(res).T
    fu=d[(d.prof=="falling")&(d.sdz>0)].copy()
    fu["w2"]=np.where(fu.w.isin(["w7","w8","w9","w10","w11","w12"]),"B","C")
    out["falling up days by fold"]=fu.groupby("w2").apply(lambda s: pd.Series(dict(n=len(s),mean_e1=s.e1.mean(),slope=stats.linregress(s.sdz,s.e1).slope,t=stats.linregress(s.sdz,s.e1).slope/stats.linregress(s.sdz,s.e1).stderr)))
    return out
