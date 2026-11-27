def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            rng=h-l; n=len(b)
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            for H in (1,2,3,5,7,10):
                f=np.full(n,np.nan); f[:n-H]=c[H:]/c[:n-H]-1; b[f"f{H}"]=f
            r60=np.full(n,np.nan); r60[60:]=c[60:]/c[:-60]-1
            lr=np.full(n,np.nan); lr[1:]=np.log(c[1:]/c[:-1])
            v30=pd.Series(lr).rolling(30).std().values
            v60m=pd.Series(v30).rolling(60,min_periods=30).median().values
            b["cl"]=cl; b["r60"]=r60; b["agi"]=(v30>v60m).astype(float); b.loc[np.isnan(v60m),"agi"]=np.nan
            b["rngrel"]=rng/c
            b["rngz"]=b["rngrel"]/pd.Series(rng/c).rolling(20,min_periods=10).mean().shift(1)
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(n)
            b["inprof"]=(b["regime"]!="chop").astype(int)
            ts=pd.to_datetime(b["timestamp"]); b["yr"]=ts.dt.year; b["day"]=ts.dt.floor("D")
            rows.append(b)
    A=pd.concat(rows,ignore_index=True)
    def tcl(x,d):
        z=pd.DataFrame({"x":x,"d":d}).dropna()
        n=len(z)
        if n<8: return np.nan,np.nan,n
        m=z.x.mean(); s=(z.x-m).groupby(z.d).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/n
        return m,m/se,n
    for H in (1,2,3,5,7,10):
        dr=A[A.pos%H==0].groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"]=A[f"f{H}"]-A.coin.map(dr)
    A["hi"]=(A.cl>=0.8).astype(int); A["lo"]=(A.cl<=0.2).astype(int)
    out={}
    res=[]
    for H in (1,2,3,5,7,10):
        g=A[A.pos%H==0]
        for name,m in [("inprof hi",(g.inprof==1)&(g.hi==1)),("inprof lo",(g.inprof==1)&(g.lo==1)),("out hi",(g.inprof==0)&(g.hi==1)),("out lo",(g.inprof==0)&(g.lo==1))]:
            mm,t,n=tcl(g.loc[m,f"u{H}"].values,g.loc[m,"day"].values)
            res.append({"H":H,"set":name,"mean_u":mm,"t":t,"n":n})
    out["by horizon hi/lo CL"]=pd.DataFrame(res)
    # graded: per-case product of centred CL and u1, all bars grid 1
    res=[]
    g=A.copy(); g["clc"]=g.cl-0.5
    g["trend"]=np.where(g.r60>0.10,"rising",np.where(g.r60<-0.10,"falling",np.where(g.r60.notna(),"choppy",None)))
    g["ag"]=np.where(g.agi==1,"agit",np.where(g.agi==0,"calm",None))
    for H in (1,2):
        gg=g[g.pos%H==0]
        for (tr,ag),q in gg.dropna(subset=["trend","ag"]).groupby(["trend","ag"]):
            # slope u on clc
            x=q.clc; y=q[f"u{H}"]; ok=x.notna()&y.notna(); x=x[ok]; y=y[ok]
            b1=((x-x.mean())*(y-y.mean())).sum()/((x-x.mean())**2).sum()
            e=y-y.mean()-b1*(x-x.mean())
            sc=((x-x.mean())*e).groupby(q.day[ok]).sum()
            se=np.sqrt((sc**2).sum())/((x-x.mean())**2).sum()
            mh,th,nh=tcl(q.loc[q.hi==1,f"u{H}"].values,q.loc[q.hi==1,"day"].values)
            res.append({"H":H,"trend":tr,"ag":ag,"slope_u_on_CL":b1,"t_slope":b1/se,"n":len(x),"hi_mean_u":mh,"hi_t":th,"hi_n":nh})
    out["CL slope by own profile (r60, vol vs 60d median)"]=pd.DataFrame(res)
    # hi CL combined with wide range, all bars, 1d
    res=[]
    gg=g[(g.hi==1)].copy()
    gg["rq"]=pd.qcut(gg.rngz,4,labels=False)
    for q,s in gg.groupby("rq"):
        for H in (1,2):
            s2=s[s.pos%H==0]; mm,t,n=tcl(s2[f"u{H}"].values,s2.day.values)
            res.append({"H":H,"rngz_q":q,"mean_u":mm,"t":t,"n":n})
    out["hi CL by relative range quartile"]=pd.DataFrame(res)
    res=[]
    for yr,s in g[(g.pos%1==0)].groupby("yr"):
        x=s.clc; y=s.u1; ok=x.notna()&y.notna(); x=x[ok]; y=y[ok]
        b1=((x-x.mean())*(y-y.mean())).sum()/((x-x.mean())**2).sum()
        e=y-y.mean()-b1*(x-x.mean()); sc=((x-x.mean())*e).groupby(s.day[ok]).sum()
        se=np.sqrt((sc**2).sum())/((x-x.mean())**2).sum()
        res.append({"yr":yr,"slope":b1,"t":b1/se,"n":len(x)})
    out["1d CL slope by year, all bars"]=pd.DataFrame(res)
    return out
